from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home-page"),
    path("room/<int:pk>/", views.rooms, name="room-page"),
    path("create-room/", views.create_room, name="create-room")
]
