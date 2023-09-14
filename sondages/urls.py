from django.urls import path

from . import views

app_name = "sondages"
urlpatterns = [
    # ex: /index/
    path("", views.index, name="index"),
    # ex: /sondages/5/
    # la valeur 'name' appelée par la balise de modèle {% url %}
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /sondages/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /sondages/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]