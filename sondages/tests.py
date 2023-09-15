from django.test import TestCase

# Use : python manage.py test sondages

# Create your tests here.
import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """
    S'il n'y a aucune question, un message approprié s'affiche.
    """
    def test_no_questions(self):
        response = self.client.get(reverse("sondages:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucun sondage n'est disponible.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    """
    Les questions avec une pub_date dans le passé sont affichées sur le
    sommaire.
    """
    def test_past_question(self):
        question = create_question(question_text="Question passée.", days=-30)
        response = self.client.get(reverse("sondages:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    """
    Les questions avec une pub_date dans le futur ne sont pas affichées sur
    la page d'index.
    """
    def test_future_question(self):
        create_question(question_text="Question à venir.", days=30)
        response = self.client.get(reverse("sondages:index"))
        self.assertContains(response, "Aucun sondage n'est disponible.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    """
    Même si des questions passées et futures existent, seules les questions passées
    sont affichés.
    """
    def test_future_question_and_past_question(self):
        question = create_question(question_text="Question passée.", days=-30)
        create_question(question_text="Question à venir.", days=30)
        response = self.client.get(reverse("sondages:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    """
    La page d'index des questions peut afficher plusieurs questions.
    """
    def test_two_past_questions(self):
        question1 = create_question(question_text="Question précédente 1.", days=-30)
        question2 = create_question(question_text="Question précédente 2.", days=-5)
        response = self.client.get(reverse("sondages:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    """
    La vue détaillée d'une question avec une pub_date dans le futur
    renvoie un 404 introuvable.
    """
    def test_future_question(self):
        future_question = create_question(question_text="Question à venir.", days=5)
        url = reverse("sondages:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    """
    La vue détaillée d'une question avec une pub_date dans le passé
    affiche le texte de la question.
    """
    def test_past_question(self):
        past_question = create_question(question_text="Question passée.", days=-5)
        url = reverse("sondages:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionModelTests(TestCase):
    """
    was_published_recently() renvoie False pour les questions dont pub_date
    est âgé de plus d’un jour.
    """
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    """
    was_published_recently() renvoie True pour les questions dont pub_date
    est dans le dernier jour.
    """
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    """
    was_published_recently() renvoie False pour les questions dont pub_date
    est dans le futur.
    """
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now