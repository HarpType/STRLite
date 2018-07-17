from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404

from strl_app.models import World

import json


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return HttpResponseRedirect('/login/?next=%s' % request.path)


def worlds(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('world_name')
            if name == '':
                w = World(owner=request.user, init_info="[]")
            else:
                w = World(owner=request.user, init_info="[]", name=name)
            w.save()
            worlds_qs = World.objects.filter(owner=request.user)
            context = {'world_list': worlds_qs}
            return render(request, 'worlds.html', context)
        else:
            worlds_qs = World.objects.filter(owner=request.user)
            context = {'world_list': worlds_qs}
            return render(request, 'worlds.html', context)
    else:
        return HttpResponseRedirect('/login/')


def delete_world(request, world_id):
    if request.user.is_authenticated:
        world = get_object_or_404(World, pk=world_id, owner=request.user)
        world.delete()
        return HttpResponseRedirect('/worlds/')
    else:
        return HttpResponseRedirect('/login/')


def make_world_active(request, world_id):
    if request.user.is_authenticated:
        world = get_object_or_404(World, pk=world_id, owner=request.user)
        request.session['current_world_id'] = world_id
        print(request.session.get('current_world_id'))
        return HttpResponseRedirect('/editor/')
    else:
        return HttpResponseRedirect('/login/')


def editor(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            world_id = request.session.get('current_world_id')
            world = get_object_or_404(World, pk=world_id, owner=request.user)
            j = world.init_info
            scene = json.loads(j)
            info_to_client = json.dumps({'id': world_id, 'scene': scene})
            return HttpResponse(info_to_client)
        else:
            return render(request, 'editor.html')
    else:
        return HttpResponseRedirect('/login/?next=%s' % request.path)


def save_world_properties(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            init_json = request.POST.get('scene')
            print(json.loads(init_json))
            # w = World(owner=request.user, init_info=init_json)
            world_id = request.session.get('current_world_id')
            w = World.objects.get(pk=world_id)
            w.init_info = init_json
            w.save()
            return HttpResponse('')
        else:
            return Http404("Nothing to create.")
    else:
        return HttpResponseRedirect('/login/')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'





