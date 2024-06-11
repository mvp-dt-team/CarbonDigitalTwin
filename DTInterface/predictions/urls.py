from django.urls import path

from . import views

urlpatterns = [
    path("<int:module_id>/panel", views.module, name="module"),
]
