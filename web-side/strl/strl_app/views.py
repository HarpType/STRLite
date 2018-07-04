from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
import json
import time


def home(request):
    return HttpResponse("Hello!")


def editor(request):
    return HttpResponse("Editor!!!!")

def properties(request):
	t = time.time() % 20 * 3
	data = [{'x': 100 + 10 * t, 'y': 100, 'a': 0.0, 'r':25},
			{'x': 100 + 20 * (t%30), 'y': 200, 'a': 0.0, 'r':20},
			{'x': 100 + 30 * (t%20), 'y': 300, 'a': 0.0, 'r':15},
			{'x': 100 + 40 * (t%15), 'y': 400, 'a': 0.0, 'r':10}]
	return HttpResponse(json.dumps(data))

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'strl_app/signup.html'
