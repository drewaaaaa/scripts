#bridge between areas (https://github.com/Serilum/Areas/) and bluemap (https://github.com/BlueMap-Minecraft/BlueMap/) mods for minecraft JE
#automatically adds poi-markers on map
#requires enable-rcon=true in server.properties and set rcon.port with rcon.password; нужно вписать enable-rcon=true в server.properties и задать rcon.port и rcon.password там же

import os, anvil, asyncio, math #pip install anvil-parser and AFTER pip install anvil-parser2; надо по очереди поставить anvil-parser, а после него anvil-parser2
import time as t
from aiomcrcon import Client
from pyhocon import ConfigFactory, HOCONConverter
from datetime import datetime, date, time

world_name = "world-1" #change it to your world name; впиши имя мира сюда
world_path = os.path.join(os.getcwd(), world_name)
region_paths = { #if your world has many dimensions, you need to edit that dict; если у тебя измерения не как в ванилле, то поправь под свои
    "overworld": os.path.join(world_path, "region"), 
    "the_nether": os.path.join(world_path, "DIM-1", "region"), 
    "the_end": os.path.join(world_path, "DIM1", "region"),
}
keywords = {"[area]", "[na]", "[region]", "[zone]"} # https://github.com/Serilum/Areas/blob/9e2207e0f3d90a0c2376916f7046f54497c26cdd/Common/src/main/java/com/natamus/areas/functions/ZoneFunctions.java#L12
file_list = {("file", "dimension"): 0.0} #collect timestamps for files to avoid re-read unchanged files; сохраняет время изменения файлов, чтобы не проверять файлы без изменений
signs_list = {("dimension", 0, 0, 0): {"text": "text", "radius": 0, "src": "file"}}

color_palette = [ #using for "circles" and its lines; эта палитра нужна чисто для кругов и их обводки
    {"r": 255, "g": 0, "b": 0}, #red; красный
    {"r": 255, "g": 159, "b": 0}, #orange; оранжевый
    {"r": 255, "g": 255, "b": 0}, #yellow; жёлтый
    {"r": 0, "g": 128, "b": 0}, #darkgreen; тёмно-зелёный
    {"r": 125, "g": 249, "b": 255}, #lightblue; голубой
    {"r": 0, "g": 0, "b": 255}, #blue; синий
    {"r": 128, "g": 0, "b": 128}, #violet/purple/patriarch; фиолетовый
    {"r": 211, "g": 211, "b": 211}, #lightgray; светло-серый
    {"r": 255, "g": 255, "b": 255}, #white; белый
    {"r": 255, "g": 0, "b": 255}, #fuchsia/pink/lightviolet; типа розовый
    {"r": 255, "g": 218, "b": 185}, #peach; пэрсиковый
    {"r": 224, "g": 255, "b": 255}, #light cyan; бледно-голубой
    {"r": 240, "g": 230, "b": 140}, #light khaki; светлый хаки
    {"r": 64, "g": 224, "b": 208}, #light/medium turquoise; бирюзовый (сине-зелёный)
    {"r": 240, "g": 255, "b": 255}, #azure; небесный
    {"r": 69, "g": 69, "b": 69}, #darkgray; тёмно-серый
    {"r": 0, "g": 255, "b": 0}, #green; кислотный зелёный
    {"r": 115, "g": 0, "b": 0}, #maroon; бордовый
    {"r": 128, "g": 128, "b": 0}, #olive; оливковый
    {"r": 107, "g": 68, "b": 35}, #darkbrown; коричневый
]

def update_file_list() -> dict: #dictionary with changed *.mca files
    global file_list
    changed_files = {}
    for dim, folder in region_paths.items():
        if not os.path.exists(folder): continue
        for file_name in os.listdir(folder):
            if not file_name.endswith(".mca"): continue
            file_path = os.path.join(folder, file_name)
            key = (dim, file_path)
            modified_time = os.path.getmtime(file_path)
            if key not in file_list or modified_time != file_list[key]:
                changed_files[key] = modified_time
                file_list[key] = modified_time
    return changed_files

def scan_signs(files_to_scan: dict) -> dict: #monstrous signs searcher; эта огромная ебала и ищет таблички с зонами
    result = {}
    for (dim, file_path) in files_to_scan:
        print(f"Обработка {file_path}")
        try:
            region = anvil.Region.from_file(file_path)
            for cx in range(32):
                for cz in range(32):
                    offset, sectors = region.chunk_location(cx, cz)
                    if offset == 0 or not region.chunk_location(cx, cz): continue
                    try:
                        chunk = region.get_chunk(cx, cz)
                        if hasattr(chunk, "tile_entities") and chunk.tile_entities:
                            for tile in chunk.tile_entities:
                                if "id" in tile and tile["id"].value == "minecraft:sign":
                                    all_sign_texts = ""
                                    radius = None
                                    if "front_text" in tile and "messages" in tile["front_text"]:
                                        if any(kw.lower() in tile["front_text"]["messages"][0].value.lower() for kw in keywords):
                                            radius = "".join(c for c in tile["front_text"]["messages"][0].value if c.isdigit())
                                            for msg in tile["front_text"]["messages"][1:]:
                                                if msg.value:
                                                    text = msg.value.strip()
                                                    if text: all_sign_texts += text
                                    if all_sign_texts and radius:
                                        all_sign_texts = all_sign_texts.replace('"', ' ')
                                        pos = (dim, tile["x"].value, tile["y"].value, tile["z"].value)
                                        result[pos] = {
                                            "text": all_sign_texts.strip(),
                                            "radius": radius,
                                            "src": file_path
                                        }
                    except Exception as e: print(f"Ошибка в {file_path}, чанк {cx}, {cz}: {e}")
        except Exception as e:
            print(f"Ошибка в {file_path}: {e}")
            continue
    return result

def signs_list_updater(new_signs: dict, file_list: dict) -> dict:
    global signs_list
    old_signs_list = signs_list.copy()
    for (_, file) in file_list.keys():
        for key, signsrc in old_signs_list.items():
            if signsrc["src"] and signsrc["src"] == file:
                signs_list.pop(key)
    signs_list.update(new_signs)

def printor(signs_to_conf: dict): #write POI markers in *.conf files; вписывает маркеры-метки в конфиги
    by_dimension = {}
    for idx, ((dim, x, y, z), data) in enumerate(signs_to_conf.items()):
        marker_id = f"auto-marker-{idx}"
        markers = by_dimension.setdefault(dim, {})
        markers[marker_id] = {
            "type": "poi",
            "position": {"x": x, "y": y, "z": z},
            "label": data.get("text", "Безымянный маркер"),
            "sorting": 0,
            "listed": True,
            "min-distance": 5,
            "max-distance": 10000000
        }
    for dim, markers in by_dimension.items():
        config = {
            "automarkers": {
                "label": "Маркеры из скрипта",
                "toggleable": True,
                "default-hidden": False,
                "sorting": 0,
                "markers": markers
            }
        }
        filename = f"automarkers-{dim}.conf"
        output_path = os.path.join("config", "bluemap", "maps", filename)
        configtxt = HOCONConverter.to_hocon(ConfigFactory.from_dict(config))
        with open(output_path, "w") as f:
            f.write(configtxt)

def printor_shape(signs_to_conf: dict): #write shapes markers in *.conf files; вписывает маркеры в виде кругов-зон в конфиги
    by_dimension = {}
    for idx, ((dim, x, y, z), data) in enumerate(signs_to_conf.items()):
        marker_id = f"auto-marker-{idx}"
        markers = by_dimension.setdefault(dim, {})
        radius =int(data.get("radius", 1))
        shape_coords = [ # 16 dots is enough for smth like circle, isn't it? 16 точек для типа круга
            {
                "x": x + radius * math.cos(2 * math.pi * i / 16),
                "z": z + radius * math.sin(2 * math.pi * i / 16)
            }
            for i in range(16)
        ]
        markers[marker_id] = {
            "type": "shape",
            "position": {"x": x, "y": y, "z": z},
            "label": data.get("text", "Безымянный маркер"),
            "shape":shape_coords,
            "shape-y": y,
            "sorting": 0,
            "listed": True,
            "depth-test": False,
            "line-color": {**color_palette[(abs(x + y + z) % 20)], "a": 1.0}, #вычисляет цвет на базе координат, просто чтобы не было всё в одинаковых кругах
            "fill-color": {**color_palette[(abs(x + y + z) % 20)], "a": 0.3}, #calculating color by coordinates for variety of colors
            "min-distance": 5,
            "max-distance": 10000000
        }
    for dim, markers in by_dimension.items():
        config = {
            "automarkers": {
                "label": "Маркеры из скрипта",
                "toggleable": True,
                "default-hidden": False,
                "sorting": 0,
                "markers": markers
            }
        }
        filename = f"automarkers-{dim}.conf"
        output_path = os.path.join("config", "bluemap", "maps", filename)
        configtxt = HOCONConverter.to_hocon(ConfigFactory.from_dict(config))
        with open(output_path, "w") as f:
            f.write(configtxt)

def bm_rld(command="bluemap reload light", host="localhost", port=11111, password="P455w0rD"): #CHANGE HOST, PORT AND PASSWORD; впиши свои пароль и порт
    async def run_command():
        client = Client(host, port, password)
        await client.connect()
        try: response = await client.send_cmd(command)
        finally: await client.close()
    try: asyncio.run(run_command())
    except Exception as e: print("Ошибка в bm_rld:", e)

def uberfunction():
    files = update_file_list()
    signs = scan_signs(files)
    signs_list_updater(signs, files)
    #printor(signs_list) #uncomment for only POI
    printor_shape(signs_list) #comment for only POI
    if len(files) > 0: bm_rld()
    print(f"{datetime.now().strftime('%d.%m.%Y %X')} Обработано {len(files)} файлов.")

def main_loop():
    file_list.clear()
    signs_list.clear()
    files = update_file_list()
    signs = scan_signs(files)
    signs_list_updater(signs, files)
    #printor(signs_list) #uncomment for only POI
    printor_shape(signs_list) #comment for only POI
    bm_rld()
    t.sleep(20) #first run always long and heavy, so...; первый запуск обычно долгий и тяжёлый, так что 20 секунд на отдохнуть
    while True:
        uberfunction()
        t.sleep(60)

if __name__ == "__main__":
    main_loop()
