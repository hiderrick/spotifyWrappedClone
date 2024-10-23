import requests
from collections import Counter
from datetime import datetime, timedelta
from django.http import JsonResponse

# Create your views here.
def get_user_data(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    top_tracks_response = requests.get(
        "https://api.spotify.com/v1/me/top/tracks?limit=5",
        headers=headers
    )
    top_tracks_json = top_tracks_response.json().get('items', [])
    top_tracks = []
    for track in top_tracks_json:
        top_tracks.append(track['name'])
    top_artists_response = requests.get(
        "https://api.spotify.com/v1/me/top/artists?limit=5",
        headers=headers
    )
    top_artists_json = top_artists_response.json().get('items', [])
    top_artists = []
    for artist in top_artists_json:
        top_artists.append(artist['name'])

    top_genres = get_top_genres(top_artists_json)
    total_mins_listened = get_total_minutes_listened(headers)
    return {"top_tracks":top_tracks,
            "top_artists":top_artists,
            "top_genres":top_genres,
            "total_mins_listened":total_mins_listened}

def get_top_genres(artists):
    all_genres = [genre for artist in artists for genre in artist['genres']]
    genre_counts = Counter(all_genres)
    top_genres = genre_counts.most_common(5)  # Get top 5 genres
    return [{"genre": genre, "count": count} for genre, count in top_genres]



def get_total_minutes_listened(headers):
    # Spotify API endpoint for recently played tracks
    url = "https://api.spotify.com/v1/me/player/recently-played"

    params = {
        "limit": 50,  # Maximum allowed by Spotify API
        "after": int((datetime.now() - timedelta(days=365)).timestamp() * 1000)  # 1 year ago
    }

    total_ms = 0
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return JsonResponse({"error": "Failed to fetch data from Spotify API"}, status=400)

        data = response.json()
        items = data.get("items", [])

        if not items:
            break

        for item in items:
            total_ms += item["track"]["duration_ms"]

        # Update the 'after' parameter for the next request
        params["after"] = items[-1]["played_at"]

    total_minutes = total_ms / (1000 * 60)  # Convert milliseconds to minutes
    return round(total_minutes)
