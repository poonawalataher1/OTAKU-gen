from django import forms
import random

STYLE_CHOICES = [
    ("anime", "Anime"),
    ("manga", "Manga"),
    ("comic", "Comic"),
    ("oldbook", "Old Book Illustration"),
    ("3d-art", "3D Art")
]

class PromptForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea, label="Enter your prompt")
    style = forms.ChoiceField(choices=STYLE_CHOICES, widget=forms.RadioSelect)

# # forms.py
# class CharacterForm(forms.ModelForm):
#     class Meta:
#         model = Character
#         fields = ['name', 'base_prompt']  # You can auto-generate or let user input


def save(self, *args, **kwargs):
    if not self.seed:
        self.seed = random.randint(10000, 99999)
    super().save(*args, **kwargs)
