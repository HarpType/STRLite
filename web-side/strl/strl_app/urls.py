from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('editor/', views.editor, name='editor'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('testrequest/', views.testrequest, name='testrequest'),
    path('editor/create', views.create, name='create'),
    path('worlds/', views.projects, name='worlds'),
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# TemplateView.as_view(template_name='home.html')