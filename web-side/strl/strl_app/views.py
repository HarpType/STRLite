from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

import json

import subprocess
import mmap

import pickle

from relation import files


# home view is just from template in urls
# editor view is just from template in urls

def stop(request):
    files.data2[:1] = b'S'
    code = files.proc.wait()
    files.data1.close()
    files.data2.close()
    files.f1.close()
    files.f2.close()
    return HttpResponse('')


def properties(request):
    size = int(files.data1[2:6])
    print('size: ', size)
    str_data = files.data1[6:6+size]
    data_to_send = pickle.loads(str_data)
    print('properties: ', data_to_send)
    return HttpResponse(json.dumps(data_to_send))


def start(request):
    files.f1 = open('relation/c_to_p.dat', 'r+')
    files.f2 = open('relation/p_to_c.dat', 'r+')

    size = 1024

    files.data1 = mmap.mmap(files.f1.fileno(), size)
    files.data2 = mmap.mmap(files.f2.fileno(), size)

    files.proc = subprocess.Popen(['python3', str(files.child_path)])

    print("proc")
    while True:
        if files.data1[:1] == b'R':
            print("LOL")
            files.data2[:1] = b'R'
            return HttpResponse(json.dumps({'st': 'ready'}))


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
