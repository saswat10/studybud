from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

# Create your views here.


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("pass")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username and password does not match")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def registerUser(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured during registration")

    context = {"form": form}
    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(description__icontains=q)
        | Q(host__username__icontains=q)
    )

    room_count = rooms.count
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    topics = Topic.objects.all()
    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


def room(request, id):
    room = Room.objects.get(id=id)
    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", id=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def userProfile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "topics": topics,
        "room_messages": room_messages,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="/login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You're not allowed here!!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("home")

    context = {"form": form, 'topics': topics, 'room': room}
    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def deleteRoom(request, id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse("You're not allowed here!!")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="/login")
def deleteMessage(request, id):
    message = Message.objects.get(id=id)

    if request.user != message.user:
        return HttpResponse("You're not allowed here!!")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": message})
