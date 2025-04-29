import os
import uuid
import json
from PIL import Image

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .pipeline import get_pipe
from .models import StorySession, Character
import io
import torch
from diffusers import StableDiffusionPipeline

# ----- Constants -----

STYLES = [
    ("anime", "Anime", "images/anime_frame.png"),
    ("manga", "Manga", "images/Manga.JPG"),
    ("comic", "Comic", "images/COMIC.JPG"),
    ("oldbook", "Old Book", "images/oldbook.JPG"),  
    ("3d-art", "3D Art", "images/3d-art-style.JPG"),
]


LAYOUT_COORDS = {
    "2_panel_horizontal": [
    (0, 0, 512, 1024),   # Left half
    (512, 0, 1024, 1024) # Right half
    ],
    "4_panel_grid": [
        (0, 0, 512, 512), (512, 0, 1024, 512),
        (0, 512, 512, 1024), (512, 512, 1024, 1024)
    ],
    "3_panel_vertical": [
        (0, 0, 1024, 341), (0, 341, 1024, 682), (0, 682, 1024, 1024)
    ],
    "6_panel_combo": [
        (0, 0, 341, 512), (341, 0, 682, 512), (682, 0, 1024, 512),
        (0, 512, 341, 1024), (341, 512, 682, 1024), (682, 512, 1024, 1024)
    ],
}

LAYOUTS = {
    key: {
        "name": name,
        "preview": f"images/layout_previews/{key}.jpg"
    }
    for key, name in {
        "4_panel_grid": "4-Panel Grid",
        "3_panel_vertical": "3-Panel Vertical",
        "6_panel_combo": "6-Panel Combo"
    }.items()
}

# ----- Utility -----

def stitch_images(images, layout):
    layout_coords = LAYOUT_COORDS[layout]
    final_image = Image.new("RGB", (1024, 1024), color="white")
    for img, (x1, y1, x2, y2) in zip(images, layout_coords):
        img = img.resize((x2 - x1, y2 - y1))
        final_image.paste(img, (x1, y1))
    return final_image

# ----- Views -----

def landing_view(request):
    return render(request, 'landing.html')

def generate_view(request):
    if request.method == 'POST':
        prompt = request.POST.get("prompt", "")
        style = request.POST.get("style", "anime")

        pipe = get_pipe(style)
        if pipe is None:
            return render(request, "generate.html", {"error": "Model load failed", "styles": STYLES})

        image = pipe(prompt).images[0]
        filename = f"{uuid.uuid4()}.png"
        save_path = os.path.join(settings.MEDIA_ROOT, filename)
        image.save(save_path)

        return render(request, "generate.html", {
            "image_url": settings.MEDIA_URL + filename,
            "styles": STYLES
        })

    return render(request, "generate.html", {"styles": STYLES})

def story_mode_view(request):
    if request.method == "POST":
        story_name = request.POST.get("story_name")
        prompt = request.POST.get("prompt")
        style = request.POST.get("style", "anime")
        layout_name = request.POST.get("layout", "4_panel_grid")

        layout_coords = LAYOUT_COORDS.get(layout_name)
        if not layout_coords:
            return render(request, "story_mode.html", {
                "error": "Invalid layout selected",
                "styles": STYLES,
                "layouts": LAYOUTS,
            })

        pipe = get_pipe(style)
        if pipe is None:
            return render(request, "story_mode.html", {
                "error": "Model load failed",
                "styles": STYLES,
                "layouts": LAYOUTS,
            })

        panel_dir = os.path.join(settings.MEDIA_ROOT, "panels")
        os.makedirs(panel_dir, exist_ok=True)

        images = []
        panel_urls = []

        for i in range(len(layout_coords)):
            img = pipe(prompt).images[0]
            filename = f"{uuid.uuid4().hex}_panel_{i}.png"
            path = os.path.join(panel_dir, filename)
            img.save(path)
            images.append(img)
            panel_urls.append(os.path.join(settings.MEDIA_URL, "panels", filename))

        stitched = stitch_images(images, layout_name)
        final_name = f"{uuid.uuid4().hex}_page.png"
        final_path = os.path.join(settings.MEDIA_ROOT, "stories", final_name)
        os.makedirs(os.path.dirname(final_path), exist_ok=True)
        stitched.save(final_path)
        final_url = os.path.join(settings.MEDIA_URL, "stories", final_name)

        return render(request, "story_mode.html", {
            "generated_image_url": final_url,
            "individual_panels": panel_urls,
            "story_name": story_name,
            "styles": STYLES,
            "layouts": LAYOUTS,
            "selected_style": style,
            "selected_layout": layout_name
        })

    return render(request, "story_mode.html", {
        "styles": STYLES,
        "layouts": LAYOUTS
    })


# def generate_panel(character, scene_prompt):
#     full_prompt = f"{character.base_prompt}, {scene_prompt}"
#     generator = torch.manual_seed(character.seed)

#     image = pipe(prompt=full_prompt, generator=generator).images[0]
#     return image


# def generate_character_preview(character):
#     generator = torch.manual_seed(character.seed)
#     image = pipe(prompt=character.base_prompt, generator=generator).images[0]

#     # Save to character.preview_image
#     buffer = BytesIO()
#     image.save(buffer, format="PNG")
#     character.preview_image.save(f"{character.name}_preview.png", ContentFile(buffer.getvalue()))


@csrf_exempt
def save_story_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        story_name = data.get('name')
        characters = data.get('characters', [])

        session = StorySession.objects.create(name=story_name)

        for char in characters:
            Character.objects.create(
                session=session,
                name=char['name'],
                role=char['role'],
                image_url=char['image']
            )

        return JsonResponse({'status': 'success', 'session_id': session.id})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def generate_next_panel(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        prompt = data.get('prompt')
        style = data.get('style', 'anime')

        pipe = get_pipe(style)
        if pipe is None:
            return JsonResponse({'error': 'Pipeline failed'}, status=500)

        img = pipe(prompt).images[0]
        filename = f"{uuid.uuid4().hex}_nextpanel.png"
        save_path = os.path.join(settings.MEDIA_ROOT, "panels", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        img.save(save_path)

        return JsonResponse({'image_url': os.path.join(settings.MEDIA_URL, "panels", filename)})

    return JsonResponse({'error': 'Invalid method'}, status=405)

def story_mode(request):
    return render(request, 'story_mode.html')

def landing(request):
    return render(request, 'landing.html')


def story_mode_2panel(request):
    if request.method == "POST":
        story_name = request.POST.get("story_name")
        prompt = request.POST.get("prompt")
        style = request.POST.get("style", "anime")
        layout_name = request.POST.get("layout", "2_panel_horizontal")

        pipe = get_pipe(style)
        if pipe is None:
            return render(request, "story_mode.html", {
                "error": "Model load failed",
                "styles": STYLES,
                "layouts": LAYOUTS
            })

        panel_dir = os.path.join(settings.MEDIA_ROOT, "panels")
        os.makedirs(panel_dir, exist_ok=True)

        # Generate the panel
        image = pipe(prompt).images[0]

        if "panel1_path" not in request.session:
            # First panel
            filename1 = f"{uuid.uuid4().hex}_panel1.png"
            path1 = os.path.join(panel_dir, filename1)
            image.save(path1)
            request.session["panel1_path"] = path1
            panel_urls = [f"{settings.MEDIA_URL}panels/{filename1}"]
            return render(request, "story_mode.html", {
                "message": "First panel saved! Now generate the second.",
                "panel1_url": panel_urls[0],
                "story_name": story_name,
                "styles": STYLES,
                "layouts": LAYOUTS,
                "selected_style": style,
                "selected_layout": layout_name
            })
        else:
            # Second panel
            panel1_path = request.session.get("panel1_path")
            image1 = Image.open(panel1_path)
            image2 = image

            stitched = Image.new("RGB", (1024, 1024), "white")
            layout_coords = LAYOUT_COORDS[layout_name]
            image1 = image1.resize((layout_coords[0][2] - layout_coords[0][0], layout_coords[0][3] - layout_coords[0][1]))
            image2 = image2.resize((layout_coords[1][2] - layout_coords[1][0], layout_coords[1][3] - layout_coords[1][1]))

            stitched.paste(image1, (layout_coords[0][0], layout_coords[0][1]))
            stitched.paste(image2, (layout_coords[1][0], layout_coords[1][1]))

            final_name = f"{uuid.uuid4().hex}_2panel_page.png"
            final_path = os.path.join(settings.MEDIA_ROOT, "stories", final_name)
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
            stitched.save(final_path)
            final_url = f"{settings.MEDIA_URL}stories/{final_name}"

            # Clear session
            del request.session["panel1_path"]

            return render(request, "story_mode.html", {
                "generated_image_url": final_url,
                "story_name": story_name,
                "styles": STYLES,
                "layouts": LAYOUTS,
                "selected_style": style,
                "selected_layout": layout_name
            })

    return render(request, "story_mode.html", {
        "styles": STYLES,
        "layouts": LAYOUTS
    })
