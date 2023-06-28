from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki_page, name="wiki_page"),
    path("search/", views.search_article, name="search"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.random_article, name="random"),
]
