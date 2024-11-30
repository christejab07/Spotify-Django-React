from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class CreateRoom(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        # Check if the session key was created successfully
        host = self.request.session.session_key
        print(f"Session key created: {host}")

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            guest_can_pause = serializer.validated_data.get("guest_can_pause")
            votes_to_skip = serializer.validated_data.get("votes_to_skip")
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])

                # Save the room code in the session
                self.request.session["room_code"] = room.code
                print(f"Updated Room: Host = {room.host}, Code = {room.code}")

                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip,
                )
                room.save()

                # Save the room code in the session
                self.request.session["room_code"] = room.code
                print(f"New Room Created: Host = {room.host}, Code = {room.code}")
                return Response(
                    RoomSerializer(room).data, status=status.HTTP_201_CREATED
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = "code"

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code is not None:
            try:
                room = Room.objects.get(code=code)
                session_key = self.request.session.session_key
                host = room.host

                # Debug info
                print(f"Session Key: {session_key}")
                print(f"Room Host: {host}")

                data = RoomSerializer(room).data
                data["is_host"] = self.request.session.session_key == room.host
                return Response(data, status=status.HTTP_200_OK)
            except Room.DoesNotExist:
                return Response(
                    {"Room not found": "Invalid room code."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {"Bad request": "code parameter not found in request"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class JoinRoom(APIView):
    lookup_url_kwarg = "code"

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session["room_code"] = code
                return Response({"message": "room joined!"}, status=status.HTTP_200_OK)
            return Response(
                {"bad request": "invalid room code"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"bad request": "invalid post data, did not find a code key"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@csrf_exempt
def delete_room_by_id(request, id):
    if request.method == "DELETE":
        room = get_object_or_404(Room, id=id)
        room.delete()
        return JsonResponse({"message": "Room deleted successfully"}, status=204)
    return JsonResponse({"error": "Invalid request method"}, status=405)


class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {"code": self.request.session.get("room_code")}
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    def post(self, request, format=None):
        if "room_code" in self.request.session:
            self.request.session.pop("room_code")
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()

        return Response({"message": "room left!"}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer
    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            room_code = serializer.data.get("code")
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')

            queryset = Room.objects.filter(code=room_code)
            if not queryset.exists():
                return Response({'message': 'room not found'}, status=status.HTTP_404_NOT_FOUND)
            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({'message': 'you are not the host of this room.'}, status=status.HTTP_403_FORBIDDEN)
            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        
        return Response({"bad request": 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)