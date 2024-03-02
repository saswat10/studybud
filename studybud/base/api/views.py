from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Room
from .serializers import RoomSerailizer


@api_view(["GET"])
def getRoutes(request):
    routes = ["GET /api", "GET /api/rooms", "GET /api/rooms/:id"]
    return Response(routes)


@api_view(["GET"])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerailizer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getRoom(request, id):
    rooms = Room.objects.filter(id=id)
    serializer = RoomSerailizer(rooms, many=True)
    return Response(serializer.data)
