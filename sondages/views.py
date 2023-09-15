# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from sondages.models import Question, Choice


class IndexView(generic.ListView):
    template_name = "sondages/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Renvoie les cinq dernières questions publiées (sans compter celles qui doivent être
        publié à l’avenir).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

class DetailView(generic.DetailView):
    model = Question
    template_name = "sondages/detail.html"

    """
    Exclut toutes les questions qui ne sont pas encore publiées.
    """
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "sondages/results.html"

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