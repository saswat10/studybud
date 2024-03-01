from django.shortcuts import render


# Create your views here.

rooms = [
    {'id': 1, 'title':"Let's learn Python"},
    {'id': 2, 'title':"Let's learn C++"},
    {'id': 3, 'title':"Let's learn Rust"},
    {'id': 4, 'title':"Let's learn GOLang"},
]

def home(request):
    context = {'rooms': rooms}
    return render(request, "base/home.html", context)


def room(request, id):
    room = None
    for i in rooms: 
        if i['id'] == int(id):
            room = i
    context = {'room': room}
    return render(request, "base/room.html", context)
