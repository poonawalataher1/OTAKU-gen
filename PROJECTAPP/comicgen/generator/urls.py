
from django.contrib import admin
from django.urls import path
from generator import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generator/', views.generate_view, name='generate'),
    path('', views.landing_view, name='landing'),
    path('story/',views.story_mode,name="story_mode"),
    path('save_story/', views.save_story_session, name='save_story'),
    path('generate_panel/', views.generate_next_panel, name='generate_panel'),
]

# This serves media files (your generated images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


