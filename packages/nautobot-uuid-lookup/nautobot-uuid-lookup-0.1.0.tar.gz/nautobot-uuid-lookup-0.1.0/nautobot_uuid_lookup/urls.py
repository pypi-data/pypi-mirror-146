"""Urls for nautobot_uuid_lookup."""

from django.urls import path

from nautobot_uuid_lookup import views

urlpatterns = [
    # path('random/', views.RandomAnimalView.as_view(), name='random_animal'),
    path('<uuid:pk>/', views.redirect_uuid)
]