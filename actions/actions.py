import requests
import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Last.fm API Configuration
LASTFM_API_KEY = "ADD_LASTFMKEY_HERE"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def fetch_from_lastfm(params):
    """Helper function to make Last.fm API requests."""
    response = requests.get(BASE_URL, params)
    if response.status_code == 200:
        return response.json()
    return None


class ActionListSimilarSongs(Action):
    def name(self):
        return "action_list_similar_songs"

    def run(self, dispatcher, tracker, domain):
        track_name = tracker.get_slot("track_name")
        artist_name = tracker.get_slot("artist_name")

        # Check if slots are missing
        if not track_name and not artist_name:
            dispatcher.utter_message("I need both the song name and the artist name. Can you provide them?")
            return []
        if not track_name:
            dispatcher.utter_message("I have the artist name, but I need the song name. Please tell me the song name.")
            return []
        if not artist_name:
            dispatcher.utter_message("I have the song name, but I need the artist name. Please tell me the artist name.")
            return []

        # Fetch similar songs from Last.fm
        params = {
            "method": "track.getsimilar",
            "track": track_name,
            "artist": artist_name,
            "api_key": LASTFM_API_KEY,
            "format": "json",
        }
        data = fetch_from_lastfm(params)

        if data and "similartracks" in data:
            similar_songs = [
                f"{track['name']} by {track['artist']['name']}"
                for track in data["similartracks"]["track"][:5]
            ]
            dispatcher.utter_message(
                f"Songs similar to '{track_name}' by {artist_name}: {', '.join(similar_songs)}"
            )
        else:
            dispatcher.utter_message("Sorry, I couldn't find similar songs at the moment.")
        return []



class ActionListSimilarArtists(Action):
    def name(self):
        return "action_list_similar_artists"

    def run(self, dispatcher, tracker, domain):
        artist_name = tracker.get_slot("artist_name")

        if not artist_name:
            dispatcher.utter_message("Please provide the name of the artist.")
            return []

        params = {
            "method": "artist.getsimilar",
            "artist": artist_name,
            "api_key": LASTFM_API_KEY,
            "format": "json",
        }
        data = fetch_from_lastfm(params)

        if data and "similarartists" in data:
            similar_artists = [artist["name"] for artist in data["similarartists"]["artist"][:5]]
            message = (
                f"Artists similar to {artist_name}: {', '.join(similar_artists)}"
                if similar_artists
                else f"No similar artists found for {artist_name}."
            )
        else:
            message = "Sorry, I couldn't fetch similar artists at the moment."

        dispatcher.utter_message(message)
        return []


class ActionListTopSongsByGenre(Action):
    def name(self):
        return "action_list_top_songs_by_genre"

    def run(self, dispatcher, tracker, domain):
        genre = tracker.get_slot("genre")

        if not genre:
            dispatcher.utter_message("Please specify a genre.")
            return []

        params = {
            "method": "tag.gettoptracks",
            "tag": genre,
            "api_key": LASTFM_API_KEY,
            "format": "json",
        }
        data = fetch_from_lastfm(params)

        if data and "tracks" in data:
            top_songs = [
                f"{track['name']} by {track['artist']['name']}"
                for track in data["tracks"]["track"][:5]
            ]
            message = (
                f"Top songs in the {genre} genre: {', '.join(top_songs)}"
                if top_songs
                else f"No top songs found for the genre {genre}."
            )
        else:
            message = "Sorry, I couldn't fetch top songs at the moment."

        dispatcher.utter_message(message)
        return []


class ActionRecommendRandomSong(Action):
    def name(self):
        return "action_recommend_random_song"

    def run(self, dispatcher, tracker, domain):
        genres = ["pop", "rock", "hip-hop", "jazz", "classical", "electronic", "metal", "reggae", "country"]
        random_genre = random.choice(genres)

        params = {
            "method": "tag.gettoptracks",
            "tag": random_genre,
            "api_key": LASTFM_API_KEY,
            "format": "json",
        }
        data = fetch_from_lastfm(params)

        if data and "tracks" in data:
            tracks = data["tracks"]["track"]
            if tracks:
                random_track = random.choice(tracks)
                song_name = random_track["name"]
                artist_name = random_track["artist"]["name"]
                message = f"Here's a random song recommendation: '{song_name}' by {artist_name} (Genre: {random_genre})."
            else:
                message = f"Sorry, no tracks found for the genre {random_genre}."
        else:
            message = "Sorry, I couldn't fetch a random song at the moment."

        dispatcher.utter_message(message)
        return []
    
    

from rasa_sdk import Action
from rasa_sdk.events import UserUtteranceReverted

class ActionDefaultFallback(Action):
    def name(self) -> str:
        return "action_default_fallback"

    async def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="I'm sorry, I didn't understand that. Can you rephrase?")
        return [UserUtteranceReverted()]
