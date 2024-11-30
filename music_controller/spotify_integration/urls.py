from django.urls import path
from .views import *

urlpatterns = [
    path('get-auth-url/', AuthURL.as_view(), name='auth-url'),
    path('redirect/', spotify_callback, name='spotify-callback'),
    path('is-authenticated/', IsAuthenticated.as_view(), name='is-authenticated'),
    path('current-song', CurrentSong.as_view()),
    path('pause', PauseSong.as_view(), name='pause_song'),
    path('play', PlaySong.as_view(), name='play_song'),
    path('skip', SkipSong.as_view(), name='skip_song'),
]