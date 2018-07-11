from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
import json
import time
import random
my_angle = 0.0

objects = []

def home(request):
    return HttpResponse("Hello!")


def editor(request):
    return HttpResponse("Editor!!!!")

def properties(request):
	random.seed(20)
	t = time.time() % 30 * 2
	global my_angle
	
	my_angle = my_angle + 5.0
	if len(objects) == 0:
		for i in range(1000):
			objects.append({
				'id': random.randint(0,2),
				'x': random.randint(-300,300),
				'y': random.randint(0,600),
				'a': random.randint(0,360),
				'r': random.randint(10,25),
				'w': random.randint(25,50),
				'h': random.randint(25,50)

			})

	for o in objects:
		o['x'] = o['x'] + 10
		o['a'] = my_angle
		if (o['x'] > 800):
			o['x'] = 0

	data = [{'id' : 1, 'x': 100 + 10 * t, 'y': 100, 'a': my_angle , 'r':25},
			{'id': 1, 'x': 100 + 20 * (t%30), 'y': 200, 'a': 45.0, 'r':20},
			{'id': 1, 'x': 100 + 30 * (t % 15), 'y': 300, 'a': 0.0, 'r': 15},
			{'id': 1, 'x': 100 + 40 * (t % 10), 'y': 400, 'a': 0.0, 'r': 10},
			{'id': 2, 'x': 400, 'y': 400, 'a': 25.0, 'w':100, 'h': 25},
			]
	return HttpResponse(json.dumps(objects))

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'strl_app/signup.html'
