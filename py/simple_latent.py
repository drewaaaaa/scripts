#тупа нода для комфи, чтобы удобно в один клик менять высоту с шириной, а то какова хуя они это убрали
#just simple latent node for comfyui for one-click swap width and height
import torch

class SimpleEmptyLatent:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 8192, "step": 64}),
                "height": ("INT", {"default": 512, "min": 64, "max": 8192, "step": 64}),
                "flip": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "generate"
    CATEGORY = "latent"

    def generate(self, width, height, flip):
        if flip:
            width, height = height, width
        
        latent = torch.zeros([1, 4, height // 8, width // 8])
        return ({"samples": latent}, )

NODE_CLASS_MAPPINGS = {
    "SimpleEmptyLatent": SimpleEmptyLatent
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleEmptyLatent": "Simple Empty Latent (Flip)"
}
