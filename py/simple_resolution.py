class SimpleResolutionNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 64}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 64}),
                "swap": ("BOOLEAN", {"default": False, "tooltip": "Поменять местами ширину и высоту"}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "calculate"
    CATEGORY = "utilities"

    def calculate(self, width, height, swap):
        if swap:
            width, height = height, width
        return (width, height)

NODE_CLASS_MAPPINGS = {
    "SimpleResolutionNode": SimpleResolutionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleResolutionNode": "Simple Resolution"
}