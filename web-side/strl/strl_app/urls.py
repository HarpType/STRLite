from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', views.home, name='home'),
    path('editor/', views.editor, name='editor'),
    path('editor/<int:world_id>', views.make_world_active, name='active'),
    path('editor/save/', views.save_world_properties, name='save'),
    path('worlds/', views.worlds, name='worlds'),
    path('<int:world_id>/delete', views.delete_world, name='delete'),
]