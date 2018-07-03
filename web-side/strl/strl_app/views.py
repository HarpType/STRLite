from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello!")


def editor(request):
    return HttpResponse("Editor!!!!")
