from django.shortcuts import render
from .models import Room

# Create your views here.

rooms = [
    {'id': 1, 'name':"Let's learn Python"},
    {'id': 2, 'name':"Let's learn C++"},
    {'id': 3, 'name':"Let's learn Rust"},
    {'id': 4, 'name':"Let's learn GOLang"},
]

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, "base/home.html", context)


def room(request, id):
    room = Room.objects.get(id=id)
    context = {'room': room}
    return render(request, "base/room.html", context)
