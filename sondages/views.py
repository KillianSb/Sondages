from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def sondages(request):
    return HttpResponse("Bonjour le monde. Vous êtes à l'index des sondages.")