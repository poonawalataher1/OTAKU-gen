# OTAKU gen

**OTAKU gen** is a retro-futuristic web application that brings your manga, anime, and comic ideas to life! Powered by Stable Diffusion and built with Django, it allows users to generate stunning anime-style illustrations and comic panels based on their prompts and storylines. With features like **panel layout selection**, **character consistency**, and **Story Mode**, OTAKU gen is your personal manga creation assistant.

![OTAKU gen UI preview](preview.png) <!-- Replace with actual screenshot -->

---

## Features

- **Prompt-based Anime Image Generation**  
  Describe a scene and watch it turn into an anime-style illustration.

-  **Comic Panel Layouts**  
  Choose from predefined layouts (1, 2, 4, 6, 9 panels) for manga-style storytelling.

-  **Story Mode**  
  Build a consistent storyline with persistent characters and scene-by-scene panel generation.

- **Character Sidebar Preview**  
  Visual reference for maintaining consistent characters across your story.

-  **Auto-Stitching Panels**  
  Panels are automatically merged into a single manga-style page based on layout.

-  **Session Saving**  
  Save your stories and continue them anytime.

---

## Tech Stack

- **Frontend:** HTML, Tailwind CSS, Alpine.js  
- **Backend:** Django (Python), Pillow  
- **AI Model:** Stable Diffusion XL with LoRA fine-tuning  
- **Image Handling:** Diffusers, Transformers, CPU Offload

---

## How It Works

1. User inputs a prompt and selects a panel layout.
2. Stable Diffusion (via Hugging Face Diffusers) generates anime-style images.
3. Selected layout coordinates guide image placement using Pillow.
4. Final image is stitched and displayed in comic/manga format.

---

## Example Use Case

1. Select **Story Mode**.
2. Name your story and introduce characters via prompts.
3. For each scene, input a description.
4. Generate the next panel — the app maintains visual consistency for your characters.
5. Continue generating until your manga is complete!

---

##Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/otaku-gen.git
   cd otaku-gen
2. **Create a Virtual Enviroment**
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

3. **Install Dependencies**
pip install -r requirements.txt

4.**Run Django server**
python manage.py runserver

5.**Go to**
http://localhost:8000/


## Project Structure
otaku-gen/
│
├── core/                    # Django views, models, logic
├── static/                  # Tailwind CSS, JS, images
├── templates/               # HTML templates
├── media/                   # Generated image storage
├── storymode/               # Story mode logic and character previews
├── manage.py
└── requirements.txt

