from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

import json
import ast

import subprocess
from queue import Queue, Empty
from threading import Thread


#for communication between server and gravity
from relation import files, bridge


# home view is just from template in urls
# editor view is just from template in urls

def stop(request):
    # stop reading thread
    bridge.stop_bridge = True
    # bridge.proc.stdout.write('Stop\n')
    # stop gravity.py
    bridge.proc.terminate()
    return HttpResponse('')


def properties(request):
    try:
        str_data = bridge.q.get(timeout=1)
    except Empty:
        return HttpResponse('[]')
    else:
        data_to_send = ast.literal_eval(str_data[:-1])
        for i in data_to_send:
            i["id"] = 1
            i["a"] = 0
        return HttpResponse(json.dumps(data_to_send))


def start(request):
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


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
