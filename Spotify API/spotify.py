import csv
import requests
import base64

# Spotify API credentials
CLIENT_ID = "b0ad7e3196664e03af1ce3c52f88033b"
CLIENT_SECRET = "32b748b5f0404810a92298243ccc1170"

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
with open("artist_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Artist", "Genres", "Popularity"])
    writer.writerow([artist["name"], ", ".join(artist["genres"]), artist["popularity"]])
    
    writer.writerow([])
    writer.writerow(["Top Tracks"])
    writer.writerow(["Name", "Album", "Popularity"])
    for track in tracks:
        writer.writerow([track["name"], track["album"]["name"], track["popularity"]])
        
    writer.writerow([])
    writer.writerow(["Related Artists"])
    writer.writerow(["Name", "Genres", "Popularity"])
    for related_artist in related_artists:
        writer.writerow([related_artist["name"], ", ".join(related_artist["genres"]), related_artist["popularity"]])
