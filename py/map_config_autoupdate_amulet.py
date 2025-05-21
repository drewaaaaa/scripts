#too heavy and too slow script for being bridge between areas and bluemap mods for minecraft JE
#I won't update it. It only scans (~40 minutes for 37k chunks).

from amulet import load_level
from amulet_nbt import NamedTag
from amulet.api.block_entity import BlockEntity
import os, logging

class FilterNonVanillaWarnings(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "If this is not a vanilla block ignore this message" not in record.getMessage()
    
for name in logging.root.manager.loggerDict:
    logger = logging.getLogger(name)
    logger.addFilter(FilterNonVanillaWarnings())

world_path = "world-1"
keywords = {"[area]", "[na]", "[region]", "[zone]"}

def scan_signs(world_path: str) -> list[dict]:
    result = []
    if not os.path.isdir(world_path):
        raise FileNotFoundError(f"Мир не найден по пути: {world_path}")
    level = load_level(world_path)
    print(len(level.all_chunk_coords(level.dimensions[0])))
    for cx, cz in level.all_chunk_coords(level.dimensions[0]):
        chunk = level.get_chunk(cx, cz, level.dimensions[0])
        if not chunk.block_entities: continue
        print(cx, cz)
        for block_entity in chunk.block_entities.values():
            if "sign" not in block_entity.base_name:
                continue
            x, y, z = block_entity.location
            text_lines = []
            utags = block_entity.nbt.compound.get("utags")
            if not utags: continue
            for side in ("front_text", "back_text"):
                side_data = utags.get(side)
                if not side_data: continue
                messages = side_data.get("messages")
                if not messages: continue
                for msg in messages:
                    text = msg.py_str.strip('"')
                    if text: text_lines.append(text)
            full_text = " ".join(text_lines).lower()
            if any(kw in full_text for kw in keywords):
                result.append({
                    "x": x,
                    "y": y,
                    "z": z,
                    "text": "\n".join(text_lines)
                })
    level.close()
    return result

def main_loop():
    signs = scan_signs(world_path)
    with open("signs.txt", "w") as f:
        if signs:
            for sign in signs:
                print(f"{sign['x']}, {sign['y']}, {sign['z']}: {sign['text']}")
                print(f"{sign['x']}, {sign['y']}, {sign['z']}: {sign['text']}", file=f)
            else:
                print("none")

if __name__ == "__main__":
    main_loop()
