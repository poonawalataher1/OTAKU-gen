from diffusers import StableDiffusionPipeline
# import torch


# def get_pipe(style="anime"):
#     print(f"Loading model for style: {style}")
#     model_map = {
#     "anime": "gsdf/Counterfeit-V2.5",
#     "manga": "gsdf/Counterfeit-V2.5",
#     "oldbook": "runwayml/stable-diffusion-v1-5",
#     "3d-art": "stabilityai/stable-diffusion-2-1",
#     "comic": "Comic-Diffusion/comic-diffusion-v2"
# }

#     model_id = model_map.get(style, "gsdf/Counterfeit-V2.5")
#     try:
#         pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
#         pipe.enable_model_cpu_offload()
#         print("Pipeline loaded successfully.")
#         return pipe
#     except Exception as e:
#         print("Failed to load pipeline:", e)
#         return None


# pipeline.py
from diffusers import DiffusionPipeline
import torch

pipe_cache = {}

def get_pipe(style):
    if style in pipe_cache:
        return pipe_cache[style]

    if style == "oldbook":
        pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        ).to("cpu")
        pipe.enable_model_cpu_offload()
        pipe.load_lora_weights("AdamLucek/sdxl-base-1.0-oldbookillustrations-lora")
        pipe_cache[style] = pipe
        return pipe


    print(f"Loading model for style: {style}")
    model_map = {
    "anime": "gsdf/Counterfeit-V2.5",
    "manga": "gsdf/Counterfeit-V2.5",
    "oldbook": "runwayml/stable-diffusion-v1-5",
    "3d-art": "stabilityai/stable-diffusion-2-1",
    "comic": "Comic-Diffusion/comic-diffusion-v2"
}

    model_id = model_map.get(style, "gsdf/Counterfeit-V2.5")
    try:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
        pipe.enable_model_cpu_offload()
        print("Pipeline loaded successfully.")
        return pipe
    except Exception as e:
        print("Failed to load pipeline:", e)
    # Default: load any other existing styles (anime, manga, etc.)
    # This part is assumed to be handled in your existing pipeline.py logic
    # You can expand it to add other styles if needed

    return None  # Return None if style not found
