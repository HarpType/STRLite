from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', views.home, name='home'),
    path('editor/', views.editor, name='editor'),
    path('editor/<int:world_id>', views.make_world_active, name='active'),
    path('editor/save/', views.save_world_properties, name='save'),
    path('worlds/', views.worlds, name='worlds'),
    path('worlds/create/', views.create_world, name='create'),
    # path('<int:world_id>/', views.player, name='player'),
    path('<int:world_id>/delete', views.delete_world, name='delete'),
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# TemplateView.as_view(template_name='home.html')