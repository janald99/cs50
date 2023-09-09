from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit_page"),
    path("search", views.search, name="search"),
    path("new", views.new_page, name="new_page"),
    path("random", views.random_page, name="random_page")
]
