# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from sondages.models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "sondages/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "sondages/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "sondages/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Réafficher le formulaire de vote des questions.
        return render(
            request,
            "sondages/detail.html",
            {
                "question": question,
                "error_message": "Vous n'avez pas sélectionné de choix.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Renvoyez toujours un HttpResponseRedirect après avoir traité avec succès
        # avec les données POST. Cela évite que les données soient enregistrées deux fois si un
        # utilisateur clique sur le bouton Retour.
        return HttpResponseRedirect(reverse("sondages:results", args=(question.id,)))