from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now

from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from requests import get, post, put

BASE_URL = "https://api.spotify.com/v1/me"


def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(
    session_id, access_token, token_type, expires_in, refresh_token=None
):
    tokens = get_user_tokens(session_id)
    expires_in = expires_in if expires_in is not None else 3600
    expires_in = now() + timedelta(seconds=expires_in)

    if tokens:
        # Update existing token
        tokens.access_token = access_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        
        # Only update the refresh_token if it's provided
        if refresh_token:
            tokens.refresh_token = refresh_token
        
        print(tokens.access_token, tokens.refresh_token, tokens.expires_in)
        tokens.save(
            update_fields=["access_token", "expires_in", "token_type"] +
            (["refresh_token"] if refresh_token else [])  # Add refresh_token to update_fields only if not None
        )
    else:
        # Create a new token entry
        tokens = SpotifyToken(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
            expires_in=expires_in,
        )
        tokens.save()


def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id=session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)

        return True

    return False


def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token
    response = post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    ).json()

    access_token = response.get("access_token")
    token_type = response.get("token_type")
    expires_in = response.get("expires_in")
    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token
    )


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    headers = {
        "Authorization": f"Bearer {tokens.access_token}",
        "Content-Type": "application/json",
    }
    if post_:
        post(BASE_URL + endpoint, headers)
    if put_:
        put(BASE_URL + endpoint, headers)

    response = get(BASE_URL + endpoint, headers=headers)
    try:
        return response.json()
    except:
        return {"Error": "issue with request"}
    
def play_song(session_id):
    response = execute_spotify_api_request(session_id, "player/play", put_=True)
    print(f"Play song response: {response}")  # Debugging
    return response

def pause_song(session_id):
    response = execute_spotify_api_request(session_id, "player/pause", put_=True)
    print(f"Pause song response: {response}")  # Debugging
    return response

def skip_song(session_id):
    response = execute_spotify_api_request(session_id, "player/next", post_=True)
    print(f"Skip song response: {response}")  # Debugging
    return response