from django.db import models

# Create your models here.
from django.db import models

class StorySession(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Character(models.Model):
    session = models.ForeignKey(StorySession, related_name='characters', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image_url = models.URLField()
from django.db import models

class Story(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Character(models.Model):
    name = models.CharField(max_length=100)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    base_prompt = models.TextField(default="")  # NEW
    seed = models.IntegerField(default=0)       # NEW
    preview_image = models.ImageField(upload_to='character_previews/', null=True, blank=True)

