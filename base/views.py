from django.shortcuts import render
from django.http import HttpResponse

from .models import Room


def home(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms
    }
    return render(request, "base/home.html", context)


def rooms(request, pk):
    room = Room.objects.get(pk=pk)
    context = {
        "room": room
    }
    return render(request, "base/room.html", context)


def create_room(request):
    context = {}
    return render(request, "base/room_form.html", context)
