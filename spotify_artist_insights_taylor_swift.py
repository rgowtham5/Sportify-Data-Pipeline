import csv
import requests
import base64

# Spotify API credentials
CLIENT_ID = "b0ad7e3196664e03af1ce3c52f88033b"
CLIENT_SECRET = "c1a7d4d0fc714204bedee9f671f73d99"

# Base64-encoded string of "client_id:client_secret"
BASE64_AUTH = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

# Get access token
auth_response = requests.post("https://accounts.spotify.com/api/token", headers={"Authorization": f"Basic {BASE64_AUTH}"}, data={"grant_type": "client_credentials"})
access_token = auth_response.json()["access_token"]

# Artist to search for
artist_name = "Taylor Swift"

# Search for artist
artist_response = requests.get(f"https://api.spotify.com/v1/search?q={artist_name}&type=artist", headers={"Authorization": f"Bearer {access_token}"})
artist = artist_response.json()["artists"]["items"][0]

# Get top tracks
tracks_response = requests.get(f"https://api.spotify.com/v1/artists/{artist['id']}/top-tracks?market=US", headers={"Authorization": f"Bearer {access_token}"})
tracks = tracks_response.json()["tracks"]

# Get related artists
related_response = requests.get(f"https://api.spotify.com/v1/artists/{artist['id']}/related-artists", headers={"Authorization": f"Bearer {access_token}"})
related_artists = related_response.json()["artists"]

# Write data to CSV file
with open("spotify_artist_insights_taylor_swift.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    # Write artist information
    writer.writerow(["Artist", "Genres", "Popularity", "Followers", "URL"])
    writer.writerow([artist["name"], ", ".join(artist["genres"]), artist["popularity"], artist["followers"]["total"], artist["external_urls"]["spotify"]])
    
    writer.writerow([])
    
    # Write top tracks information
    writer.writerow(["Top Tracks"])
    writer.writerow(["Name", "Album", "Popularity", "Danceability", "Energy", "Speechiness", "Acousticness", "Instrumentalness"])
    for track in tracks:
        audio_features_response = requests.get(f"https://api.spotify.com/v1/audio-features/{track['id']}", headers={"Authorization": f"Bearer {access_token}"})
        audio_features = audio_features_response.json()
        writer.writerow([track["name"], track["album"]["name"], track["popularity"], audio_features["danceability"], audio_features["energy"], audio_features["speechiness"], audio_features["acousticness"], audio_features["instrumentalness"]])
    
    writer.writerow([])
    
    # Write related artists information
    writer.writerow(["Related Artists"])
    writer.writerow(["Name", "Genres", "Popularity", "Related Popularity"])
    for related_artist in related_artists:
        related_artist_response = requests.get(f"https://api.spotify.com/v1/artists/{related_artist['id']}", headers={"Authorization": f"Bearer {access_token}"})
        related_artist_info = related_artist_response.json()
        writer.writerow([related_artist["name"], ", ".join(related_artist["genres"]), related_artist["popularity"], related_artist_info["popularity"]])
