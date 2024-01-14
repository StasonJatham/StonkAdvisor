from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("advice", views.advice, name="advice"),
    path("not-advice", views.not_fin_advice, name="not-advice"),
]
