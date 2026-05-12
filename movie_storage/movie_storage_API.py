import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
FILE_PATH = f"http://www.omdbapi.com/?apikey={API_KEY}"

def get_movie_details(movie_name):
    try:
        res = requests.get(FILE_PATH, params={'t': movie_name}, timeout=20)
        data = res.json()

        if data.get("Response") == "False":
            print(f"Movie not found: {movie_name}")
            return None

        return data

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the movie API.")

    except requests.exceptions.Timeout:
        print("Error: The request timed out.")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Unexpected request error: {e}")

    return None

def get_movie_link(movie_name):
    data = get_movie_details(movie_name)
    if data.get("Response") == "True":
        imdb_id = data["imdbID"]
        imdb_link = f"https://www.imdb.com/title/{imdb_id}/"

        return imdb_link
    else:
        return "Error:", data.get("Error")
