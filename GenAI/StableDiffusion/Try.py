from torch import autocast
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
	"CompVis/stable-diffusion-v1-4",
#     revision='fp32',
    # revision='fp16',
    revision='fp16',
	use_auth_token=True
).to("cuda")


print(pipe)

prompt = 'a photo of a chinese woman riding a horse on mars'

with autocast('cuda'):
    output = pipe(prompt)
