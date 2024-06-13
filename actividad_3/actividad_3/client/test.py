import requests

url = 'http://localhost:8000/api/movie_complete/'

new_movie = {
    "title": "Django Unchained",
    "release_date": "2012-12-25",
    "genre": "Western",
    "director": {
        "name": "Quentin Tarantino",
        "birth_date": "1963-03-27",
        "nationality": "American"
    }
}

response = requests.post(url, json=new_movie)


