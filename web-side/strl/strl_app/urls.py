from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    #!ниже можно удалить наверное одну строчку
    path('', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('editor/', TemplateView.as_view(template_name='editor.html'), name='editor'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('editor/properties', views.properties, name='properties')
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)