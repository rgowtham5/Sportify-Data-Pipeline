import spotipy
import spotipy.util as util
import pandas as pd

# Set the necessary Spotify API credentials
client_id = "b0ad7e3196664e03af1ce3c52f88033b"
client_secret = "32b748b5f0404810a92298243ccc1170"
redirect_uri = "http://localhost:3000/callback"
username = "Eden"

# Authenticate with the Spotify API
scope = 'user-library-read'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
sp = spotipy.Spotify(auth=token)

# Get the user's saved tracks
results = sp.current_user_saved_tracks()
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

# Convert the track information to a pandas DataFrame
df = pd.json_normalize(tracks)

# Print the DataFrame
print(df.head())
