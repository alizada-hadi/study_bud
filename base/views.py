from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


def login_page(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home-page")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User dose not exists")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully ")
            return redirect("/")
        else:
            messages.error(request, "Username or password in invalid ")
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def register_page(request):
    page = "register"
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(
                request, f"New account has been created successfully for user {user} ")
            login(request, user)
            return redirect("home-page")
        else:
            messages.error(
                request, "Ooops, something went wrong please try again later")

    context = {
        "form": form
    }
    return render(request, "base/login_register.html", context)


def logout_page(request):
    logout(request)
    return redirect("/")


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(desc__icontains=q)
                                )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count
    }
    return render(request, "base/home.html", context)


def rooms(request, pk):
    room = Room.objects.get(pk=pk)
    context = {
        "room": room
    }
    return render(request, "base/room.html", context)


@login_required(login_url="/login")
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def update_room(request, pk):

    room = Room.objects.get(pk=pk)

    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("you are not allowed to do that.")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {
        "form": form
    }
    return render(request, "base/room_form.html", context)


def delete_room(request, pk):
    obj = Room.objects.get(pk=pk)
    if request.user != room.host:
        return HttpResponse("you are not allowed to do that.")
    if request.method == "POST":

        obj.delete()
        return redirect("/")
    return render(request, "base/delete_room.html", {"obj": obj})
