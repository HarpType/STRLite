from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
import json


def home(request):
    return HttpResponse("Hello!")


def editor(request):
    return HttpResponse("Editor!!!!")


def properties(request):
    return HttpResponse(json.dumps({'x': 100, 'y': 100}))


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
