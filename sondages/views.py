from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader

from sondages.models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("sondages/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    return HttpResponse("Vous regardez la question %s." % question_id)


def results(request, question_id):
    response = "Vous regardez les résultats de la question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("Vous votez sur la question %s." % question_id)