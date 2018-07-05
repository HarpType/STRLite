from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

import json
import ast

import subprocess
from queue import Queue, Empty
from threading import Thread

from relation import files


# home view is just from template in urls
# editor view is just from template in urls

def stop(request):
    files.proc.stdout.write('Stop\n')
    files.proc.terminate()
    return HttpResponse('')


def properties(request):
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
