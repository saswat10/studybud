from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room_page/<str:id>/", views.room, name="room"),
    path("create-room", views.createRoom, name="create_room"),
]
