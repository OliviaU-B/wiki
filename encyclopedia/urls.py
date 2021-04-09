from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.get_entry, name="get_entry"),
    path("search", views.search, name="search"),
    path("random", views.random_search, name="random"),
    path("create-entry", views.create_entry, name="create_entry"),
    path("edit/<title>", views.edit, name="edit"),
]
