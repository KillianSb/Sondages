# Create your views here.

from django.http import Http404
from django.shortcuts import get_object_or_404, render

from sondages.models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "sondages/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "sondages/detail.html", {"question": question})


def results(request, question_id):
    response = "Vous regardez les résultats de la question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("Vous votez sur la question %s." % question_id)