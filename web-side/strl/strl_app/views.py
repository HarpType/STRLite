from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
import json
import time
my_angle = 0.0

def home(request):
    return HttpResponse("Hello!")


def editor(request):
    return HttpResponse("Editor!!!!")

def properties(request):
	t = time.time() % 60
	global my_angle
	
	my_angle = my_angle + 5.0
	data = [{'id' : 1, 'x': 100 + 10 * t, 'y': 100, 'a': my_angle , 'r':25},
			{'id': 1, 'x': 100 + 20 * (t%30), 'y': 200, 'a': 0.0, 'r':20},
			{'id': 2, 'x': 400, 'y': 400, 'a': my_angle / 2.0, 'w':100, 'h': 25},
			]
	return HttpResponse(json.dumps(data))

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'strl_app/signup.html'
