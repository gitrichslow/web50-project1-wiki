from django.urls import path

from . import views

urlpatterns = [
    path("new_entry", views.new_entry, name="new_entry"),
    path("search_entry", views.search_entry, name="search_entry"),
    path("", views.index, name="index"),
    path("edit_entry", views.edit_entry, name="edit_entry"),
    path("<str:entry>", views.full_entry, name="full_entry"),
]
