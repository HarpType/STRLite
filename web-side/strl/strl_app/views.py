from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

import json
import ast

import subprocess
import sys
from queue import Queue, Empty
from threading import Thread

import pickle

from relation import files


# home view is just from template in urls
# editor view is just from template in urls

def stop(request):
    files.proc.stdout.write('Stop\n')
    files.proc.terminate()
    # files.data1.close()
    # files.data2.close()
    # files.f1.close()
    # files.f2.close()
    return HttpResponse('')


def properties(request):
    # size = int(files.data1[2:6])
    # print('size: ', size)
    # str_data = files.data1[6:6+size]
    # data_to_send = pickle.loads(str_data)
    # print('properties: ', data_to_send)
    try:
        str_data = files.q.get(timeout=1)
    except Empty:
        print('no output yet')
        return HttpResponse('ERROR')
    else:
        data_to_send = ast.literal_eval(str_data[:-1])
        print('properties: ', data_to_send)
        return HttpResponse(json.dumps(data_to_send))


def start(request):
    # files.f1 = open('relation/c_to_p.dat', 'r+')
    # files.f2 = open('relation/p_to_c.dat', 'r+')

    # size = 1024

    # files.data1 = mmap.mmap(files.f1.fileno(), size)
    # files.data2 = mmap.mmap(files.f2.fileno(), size)

    files.proc = subprocess.Popen(['python3', str(files.child_path)], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, universal_newlines=True,
                                  bufsize=1)
    files.q = Queue()
    reading = Thread(target=files.enqueue_output(), args=(files.proc.stdout, files.q))
    reading.daemon = True
    reading.start()
    try:
        line = files.q.get(timeout=1)
    except Empty:
        print('no output yet')
        return HttpResponse('ERROR')
    else:
        if line == 'Ready\n':
            return HttpResponse(json.dumps({'st': 'ready'}))
        else:
            return HttpResponse("ERROR")


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
