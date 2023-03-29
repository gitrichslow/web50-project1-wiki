from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.full_entry, name="full_entry"),
    path("search_form", views.search_entry, name="search_form")
]
