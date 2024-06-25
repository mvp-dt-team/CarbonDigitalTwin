from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:block_id>/management_panel",
        views.management_panel,
        name="management_panel",
    ),
    path("block_list", views.block_list, name="block_list"),
    path("add_block", views.add_block, name="add_block"),
    path("<int:block_id>/toggle_block", views.toggle_block, name="toggle_block"),
    path(
        "<int:block_id>/<int:n_predictions>/get_predictions",
        views.get_predictions,
        name="get_predictions",
    ),
]
