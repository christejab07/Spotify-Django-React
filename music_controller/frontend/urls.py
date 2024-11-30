from django.urls import path
from .views import index

app_name = 'frontend'

urlpatterns = [
    path('', index,  name='index'),
    path("join/", index,  name='join'),
    path("create/", index,   name='create'),
    path("room/<str:roomCode>/", index,   name='room'),
]
