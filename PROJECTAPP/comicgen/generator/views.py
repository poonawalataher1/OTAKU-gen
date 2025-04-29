# Create your views here.
from django.shortcuts import render
from .forms import PromptForm
from .pipeline import get_pipe
from PIL import Image
import uuid, os
from django.conf import settings

panel_layouts = {
    "1 Panel": (1, 1),
    "2 Panel": (1, 2),
    "4 Panel": (2, 2),
    "6 Panel": (2, 3),
    "9 Panel": (3, 3)
}

def generate_comic(prompt, layout_name):
    pipe = get_pipe()
    rows, cols = panel_layouts[layout_name]
    panel_size = 512
    comic_page = Image.new("RGB", (cols * panel_size, rows * panel_size), color="white")

    for i in range(rows):
        for j in range(cols):
            image = pipe(prompt=prompt, num_inference_steps=50, height=1024, width=1024, guidance_scale=7.0).images[0]
            image = image.resize((panel_size, panel_size))
            comic_page.paste(image, (j * panel_size, i * panel_size))

    uid = uuid.uuid4().hex[:8]
    file_name = f"comic_{uid}.png"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    comic_page.save(file_path)
    return settings.MEDIA_URL + file_name

def generate_view(request):
    image_url = None
    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            layout = form.cleaned_data['layout']
            image_url = generate_comic(prompt, layout)
    else:
        form = PromptForm()

    return render(request, 'generate.html', {'form': form, 'image_url': image_url})
