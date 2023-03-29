from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search_entry", views.search_entry, name="search_entry"),
    path("<str:entry>", views.full_entry, name="full_entry")
]
