
from django.urls import path
from .views import RoomView, CreateRoomView, GetRoom, JoinRoom, delete_room_by_id, UserInRoom, LeaveRoom, UpdateRoom

urlpatterns = [
    path('home/', RoomView.as_view()),
    path('create-room/', CreateRoomView.as_view()),
    path('get-room/', GetRoom.as_view()),
    path('join-room/', JoinRoom.as_view()),
    path('delete/<int:id>/', delete_room_by_id),
    path('user-in-room/', UserInRoom.as_view()),
    path('leave-room/', LeaveRoom.as_view()),
    path('update-room/', UpdateRoom.as_view())
]
