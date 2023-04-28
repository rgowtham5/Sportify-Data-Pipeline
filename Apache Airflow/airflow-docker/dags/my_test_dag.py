from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import datetime as dt

from database import Database

import csv
import requests
import base64


def run_this_func():
    print('I am coming first')

def run_also_this_func():
    print('I am coming last')


def extract():
    # Spotify API credentials
    CLIENT_ID = "0bcfa60152dc401986d2ace5df9c1a41"
    CLIENT_SECRET = "de849ca553f24df4b97e633f68561724"

    # Base64-encoded string of "client_id:client_secret"
    BASE64_AUTH = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    # Get access token
    auth_response = requests.post("https://accounts.spotify.com/api/token", headers={"Authorization": f"Basic {BASE64_AUTH}"}, data={"grant_type": "client_credentials"})
    access_token = auth_response.json()["access_token"]

    # Artist to search for
    artist_name = "Lil baby"

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
    with open("spotify_artist_insights_Lil_baby.csv", "w", newline="") as csvfile:
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


def postres_conn():
    db = Database()

    db.create_connection()

args = {
    'owner': 'Caffeinated Quantum Squadron',
    'start_date': dt.datetime(2020, 4, 22),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}


# Define the DAG.
dag = DAG(
    dag_id = 'alfi9',
    description='N/A',
    default_args=args,
    schedule_interval='@once'
)


run_this_task = PythonOperator(
    task_id='run_this_task',
    python_callable = run_this_func,
    dag=dag
)

run_this_task_too = PythonOperator(
    task_id='run_this_task_too',
    python_callable = run_also_this_func,
    dag=dag
)

extract_task = PythonOperator(
    task_id='extract_task',
    python_callable = extract,
    dag=dag
)

connection_task= PythonOperator(
    task_id='connection_task',
    python_callable = postres_conn,
    dag=dag
)

run_this_task >> run_this_task_too >> extract_task >> connection_task

if __name__ == "__main__":
    dag.cli()