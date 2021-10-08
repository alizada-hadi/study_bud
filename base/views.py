from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Message, Room, Topic, User
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, MyUserCreationForm


def login_page(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home-page")
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User dose not exists")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully ")
            return redirect("/")
        else:
            messages.error(request, "Username or password in invalid ")
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect("home-page")
    page = "register"
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
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
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages
    }
    return render(request, "base/home.html", context)


def rooms(request, pk):
    room = Room.objects.get(pk=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    all_member = room.participants.all().count()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room-page", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
        "all_member": all_member
    }
    return render(request, "base/room.html", context)


def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    context = {"user": user, "rooms": rooms,
               "room_messages": room_messages, "topics": topics}
    return render(request, "base/profile.html", context)


@login_required(login_url="/login")
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            desc=request.POST.get("desc")
        )
        messages.success(request, "New Room Created Successfully ")
        return redirect("/")
    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def update_room(request, pk):

    room = Room.objects.get(pk=pk)
    topics = Topic.objects.all()

    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("you are not allowed to do that.")
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.desc = request.POST.get("desc")
        room.save()
        messages.success(
            request, f"{room.name} Room has been updated sucessfully ")
        return redirect("/")
    context = {
        "form": form,
        "topics": topics,
        "room": room
    }
    return render(request, "base/room_form.html", context)


def delete_room(request, pk):
    obj = Room.objects.get(pk=pk)
    if request.user != obj.host:
        return HttpResponse("you are not allowed to do that.")
    if request.method == "POST":

        obj.delete()
        messages.success(request, f"{obj.name} Room has been deleted ")
        return redirect("/")
    return render(request, "base/delete_room.html", {"obj": obj})


def delete_message(request, pk):
    message = Message.objects.get(pk=pk)
    if request.user != message.user:
        return HttpResponse("you are not allowed to do that.")
    if request.method == "POST":

        message.delete()
        return redirect("/")
    return render(request, "base/delete_room.html", {"obj": message})


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=user.id)
    context = {"form": form}
    return render(request, "base/update-user.html", context)


def topics_page(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "base/topics.html", {"topics": topics})


def activity_page(request):
    activities = Message.objects.all()
    return render(request, "base/activity.html", {"activities": activities})
