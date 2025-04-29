from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16"
).to("cuda")

pipe.load_lora_weights("AdamLucek/sdxl-base-1.0-oldbookillustrations-lora")
pipe.enable_model_cpu_offload()

def get_pipe():
    return pipe
