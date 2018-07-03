from django.urls import path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', TemplateView.as_view(template_name='strl_app/home.html'), name='home'),
    path('editor/', TemplateView.as_view(template_name='strl_app/editor.html'), name='editor'),
    path('signup/', views.SignUp.as_view(), name='signup'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)