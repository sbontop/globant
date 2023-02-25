# berries/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path("all_berry_stats", views.all_berry_stats, name="all_berry_stats"),
    path(
        "plot_growth_time_frequency",
        views.plot_growth_time_frequency,
        name="plot_growth_time_frequency",
    ),
]
