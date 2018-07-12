from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from strl_app.models import World

import json


@csrf_exempt
def testrequest(request):
    if request.method == 'POST':
        # post_text = request.POST.get()
        print(request.body)
        data = json.loads(request.body.decode())
        print(data)
        # print(post_text)
        return HttpResponse("GEEEHELEOE")


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
        return HttpResponseRedirect('/login/')


def projects(request):
    if request.user.is_authenticated:
        worlds_qs = World.objects.filter(owner=request.user)
        id_dicts = worlds_qs.values('id')
        # id_list[i]['id'] - получение нужного id
        id_list = []
        for i in id_dicts:
            id_list.append(i['id'])
        print(id_list)
        context = {'id_list': id_list}
        return render(request, 'worlds.html', context)
    else:
        return HttpResponseRedirect('/login/')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'




