# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import requests
import random
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

# Last.fm API Configuration
LASTFM_API_KEY = "bd37cd7c48bd201b726aee7962538c03"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

class ActionListSimilarArtists(Action):
    def name(self):
        return "action_list_similar_artists"

    def run(self, dispatcher, tracker, domain):
        artist_name = tracker.get_slot("artist_name")
        response = requests.get(BASE_URL, {
            "method": "artist.getsimilar",
            "artist": artist_name,
            "api_key": LASTFM_API_KEY,
            "format": "json"
        })

        if response.status_code == 200 and "similarartists" in response.json():
            data = response.json()
            similar_artists = [artist["name"] for artist in data["similarartists"]["artist"][:5]]
            if similar_artists:
                dispatcher.utter_message(f"Artists similar to {artist_name}: {', '.join(similar_artists)}")
            else:
                dispatcher.utter_message(f"No similar artists found for {artist_name}.")
        else:
            dispatcher.utter_message("Sorry, I couldn't fetch similar artists at the moment.")
        return []

class ActionListSimilarSongs(Action):
    def name(self):
        return "action_list_similar_songs"

    def run(self, dispatcher, tracker, domain):
        track_name = tracker.get_slot("track_name")
        artist_name = tracker.get_slot("artist_name")

        if not track_name or not artist_name:
            dispatcher.utter_message("Please provide both the song name and the artist name.")
            return []

        response = requests.get(BASE_URL, {
            "method": "track.getsimilar",
            "track": track_name,
            "artist": artist_name,
            "api_key": LASTFM_API_KEY,
            "format": "json"
        })

        if response.status_code == 200 and "similartracks" in response.json():
            data = response.json()
            similar_tracks = [f"{track['name']} by {track['artist']['name']}" 
                              for track in data["similartracks"]["track"][:5]]
            if similar_tracks:
                dispatcher.utter_message(f"Songs similar to '{track_name}' by {artist_name}: {', '.join(similar_tracks)}")
            else:
                dispatcher.utter_message(f"No similar songs found for '{track_name}' by {artist_name}.")
        else:
            dispatcher.utter_message("Sorry, I couldn't fetch similar songs at the moment.")
        return []

class ActionListTopSongsByGenre(Action):
    def name(self):
        return "action_list_top_songs_by_genre"

    def run(self, dispatcher, tracker, domain):
        genre = tracker.get_slot("genre")
        response = requests.get(BASE_URL, {
            "method": "tag.gettoptracks",
            "tag": genre,
            "api_key": LASTFM_API_KEY,
            "format": "json"
        })

        if response.status_code == 200 and "tracks" in response.json():
            data = response.json()
            top_songs = [track["name"] + " by " + track["artist"]["name"] for track in data["tracks"]["track"][:5]]
            if top_songs:
                dispatcher.utter_message(f"Top songs in the {genre} genre: {', '.join(top_songs)}")
            else:
                dispatcher.utter_message(f"No top songs found for the genre {genre}.")
        else:
            dispatcher.utter_message("Sorry, I couldn't fetch top songs at the moment.")
        return []

class ActionRecommendRandomSong(Action):
    def name(self):
        return "action_recommend_random_song"

    def run(self, dispatcher, tracker, domain):
        genres = ["pop", "rock", "hip-hop", "jazz", "classical", "electronic", "metal", "reggae", "country"]
        random_genre = random.choice(genres)

        response = requests.get(BASE_URL, {
            "method": "tag.gettoptracks",
            "tag": random_genre,
            "api_key": LASTFM_API_KEY,
            "format": "json"
        })

        if response.status_code == 200 and "tracks" in response.json():
            data = response.json()
            tracks = data["tracks"]["track"]
            if tracks:
                random_track = random.choice(tracks)
                song_name = random_track["name"]
                artist_name = random_track["artist"]["name"]
                dispatcher.utter_message(
                    f"Here's a random song recommendation: '{song_name}' by {artist_name} (Genre: {random_genre})."
                )
            else:
                dispatcher.utter_message("Sorry, I couldn't fetch a random song at the moment.")
        else:
            dispatcher.utter_message("Sorry, I couldn't fetch a random song at the moment.")
        return []

