from django.shortcuts import redirect
from decouple import config
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from requests import Request, post
from api.models import Room
from .models import Vote
from .util import *


class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
        url = (
            Request(
                "GET",
                "https://accounts.spotify.com/authorize",
                params={
                    "scope": scopes,
                    "response_type": "code",
                    "redirect_uri": config('REDIRECT_URI'),
                    "client_id": config('CLIENT_ID'),
                },
            )
            .prepare()
            .url
        )

        return Response({"url": url}, status=status.HTTP_200_OK)


# check after running with self
def spotify_callback(request, format=None):
    code = request.GET.get("code")
    error = request.GET.get("error")

    response = post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config("REDIRECT_URI"),
            "client_id": config("CLIENT_ID"),
            "client_secret": config("CLIENT_SECRET"),
        },
    ).json()
    print(response)

    access_token = response.get("access_token")
    token_type = response.get("token_type")
    refresh_token = response.get("refresh_token")
    expires_in = response.get("expires_in")
    error = response.get("error")
    if not request.session.exists(request.session.session_key):
        request.session.create()
    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token
    )

    return redirect("frontend:index")


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({"status": is_authenticated}, status=status.HTTP_200_OK)


class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
        else:
            return Response(
                {"error": "Room does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        host = room.host
        endpoint = "/player/currently-playing"
        response = execute_spotify_api_request(host, endpoint)

        if "error" in response or "item" not in response:
            print("Spotify API response:", response)  # Debugging log
            return Response({"error": "No active song"}, status=status.HTTP_200_OK)

        item = response.get("item")
        duration = item.get("duration_ms")
        progress = response.get("progress_ms")
        album_cover = item.get("album").get("images")[0].get("url")
        is_playing = response.get("is_playing")
        song_id = item.get("id")

        artist_string = ", ".join(artist.get("name") for artist in item.get("artists"))
        votes = len(Vote.objects.filter(room=room, song_id=room.current_song))
        song = {
            "title": item.get("name"),
            "artist": artist_string,
            "duration": duration,
            "progress": progress,
            "image_url": album_cover,
            "is_playing": is_playing,
            "votes": votes,
            "votes_required": room.votes_to_skip,
            "song_id": song_id,
        }
        self.update_room_song(room, song_id)
        return Response(song, status=status.HTTP_200_OK)
    def update_room_song(self, room, song_id):
        current_song = room.current_song

        if current_song != song_id:
            room.current_song = song_id
            room.save(update_fields=["current_song"])
            votes = Vote.objects.filter(room=room).delete()


class PauseSong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code).first()
        if not room:
            return Response(
                {"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if self.request.session.session_key == room.host or room.guest_can_pause:
            pause_song(room.host)
            return Response(
                {"message": "Song paused successfully"}, status=status.HTTP_200_OK
            )

        return Response({"error": "Action forbidden"}, status=status.HTTP_403_FORBIDDEN)


class PlaySong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code).first()
        if not room:
            return Response(
                {"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if self.request.session.session_key == room.host or room.guest_can_pause:
            play_song(room.host)
            return Response(
                {"message": "Song played successfully"}, status=status.HTTP_200_OK
            )

        return Response({"error": "Action forbidden"}, status=status.HTTP_403_FORBIDDEN)


class SkipSong(APIView):
    def post(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code).first()
        votes = Vote.objects.filter(room=room, song_id=room.current_song)
        votes_needed= room.votes_to_skip
        if not room:
            return Response(
                {"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if self.request.session.session_key == room.host or len(votes) + 1 >= votes_needed:
            votes.delete()
            skip_song(room.host)
        else:
            vote = Vote(user=self.request.session.session_key, room=room, song_id=room.current_song)
            vote.save()
        return Response({"message": "Song skipped successfully"}, status=status.HTTP_200_OK)
    
# python manage.py runserver 0.0.0.0:8000 run on other devices within the same network