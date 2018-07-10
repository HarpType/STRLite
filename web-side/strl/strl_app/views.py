from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render
from django import forms

from strl_app.models import World

import json
import ast

import subprocess
from queue import Queue, Empty
from threading import Thread


#for communication between server and gravity
from relation import files, bridge


# home view is just from template in urls

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return HttpResponseRedirect('/login/?next=%s' % request.path)

def editor(request):
    if request.user.is_authenticated:
        return render(request, 'editor.html')
    else:
        return HttpResponseRedirect('/login/?next=%s' % request.path)


"""def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        data = request.POST.copy()
        errors = form.get_validation_errors(data)
        if not errors:
            new_user = form.save(data)
            return HttpResponseRedirect("/books/")
    else:
        data, errors = {}, {}

    return render_to_response("registration/register.html", {
        'form': forms.FormWrapper(form, data, errors)
    })
"""


@csrf_exempt
def testrequest(request):
    if request.method == 'POST':
        # post_text = request.POST.get()
        print(request.body)
        data = json.loads(request.body.decode())
        print(data)
        # print(post_text)
        return HttpResponse("GEEEHELEOE")


def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # принимаю от Паши данные
            # init_json = request.POST.data
            init_json = {'some': 'thing'}
            w = World(owner=request.user, init_info=init_json)
            w.save()
            return HttpResponse(str(w.id))
        else:
            return HttpResponse("Nothing to create")
    else:
        return HttpResponseRedirect('/login/?next=%s' % request.path)


def stop(request):
    if request.user.is_authenticated:
        # stop reading thread
        bridge.stop_bridge = True
        # bridge.proc.stdout.write('Stop\n')
        # stop gravity.py
        bridge.proc.terminate()
        return HttpResponse('')
    else:
        return HttpResponseRedirect('/login/')


def properties(request):
    if request.user.is_authenticated:
        try:
            str_data = bridge.q.get(timeout=1)
        except Empty:
            return HttpResponse('[]')
        else:
            data_to_send = ast.literal_eval(str_data[:-1])
            return HttpResponse(json.dumps(data_to_send))
    else:
        return HttpResponseRedirect('/login/')


def start(request):
    if request.user.is_authenticated:
        bridge.proc = subprocess.Popen(['python3', str(files.child_path)], stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, universal_newlines=True,
                                      bufsize=1)
        bridge.q = Queue()
        bridge.stop_bridge = False
        reading = Thread(target=bridge.enqueue_output, args=(bridge.proc.stdout, bridge.q))
        reading.daemon = True
        reading.start()
        try:
            line = bridge.q.get(timeout=3)
        except Empty:
            # stop reading thread
            # bridge.proc.stdout.write('Stop\n')
            bridge.stop_bridge = True
            return HttpResponse('ERROR')
        else:
            if line == 'Ready\n':
                return HttpResponse(json.dumps({'st': 'ready'}))
            else:
                # stop reading thread
                # bridge.proc.stdout.write('Stop\n')
                bridge.stop_bridge = True
                return HttpResponse('ERROR')
    else:
        return HttpResponseRedirect('/login/')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
