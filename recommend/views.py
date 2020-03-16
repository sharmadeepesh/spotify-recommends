from django.shortcuts import render, HttpResponse
import requests
import json
import spotipy
import spotipy.util as util
from random import randint

client_id = "94f8b776bcbe42b0a3c8dd46f94303b1"
client_secret = "55852e22c6b0414eb121890ecdc51692"

random_lyrics = [
    'Girl, you got that "Yummy" Yum',
    'And it all keeps "Rushing Back"',
    'And we want someone to "Lean On"',
    'And all your "Little Things"',
    'Your "Sugar", yes please',
    '"Shaayad", Mai hi hu, shaayad mai nahi',
    'These are my only "Intentions',
    'You know that I wont stop until I "Make Your Mine"',
    'I am standing here "Naked"',
    'You cant "Roll Like This" like..',
    '"Girls Like You" run round with guys like me',
]


# Create your views here.
def homepage(request):
    value = randint(0, 10)
    lyrics = random_lyrics[value]
    context = {
        'lyrics':lyrics,
    }
    return render(request,'song/song_search.html', context=context)

def artist_detail(request, artist_name = ''):
    if request.method == "POST":
        artist_name = request.POST.get('name')
        token =util.oauth2.SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
        access_token = token.get_access_token()    
        get_id_url = "https://api.spotify.com/v1/search?q={}&type=artist&limit=1&access_token={}"
        artist_list = requests.get(get_id_url.format(artist_name,access_token)).json()
        artist_list = artist_list['artists']
        artist_list = artist_list['items']
        artist_list = artist_list[0]
        name = get_name(artist_list)
        followers = get_followers(artist_list)
        picture = get_picture(artist_list)
        artist_id = get_id(artist_list)
        popularity = get_popularity(artist_list)
        user_type = get_user_type(artist_list)
        genres = get_genres(artist_list)
        artist_details = {
            'name': name,
            'picture': picture,
            'artist_id': artist_id,
            'link': 'https://open.spotify.com/artist/{}'.format(artist_id),
            'popularity':popularity,
            'user_type':user_type,
            'genres' : genres,
            'followers':followers,
        }
        return render(request,'artists/artist_details.html', {'artist_details':artist_details})
    else:
        if artist_name == '':
            value = randint(0, 10)
            lyrics = random_lyrics[value]
            context = {
                'lyrics':lyrics,
            }
            return render(request, 'artists/artist_search.html',context=context)
        else:
            token =util.oauth2.SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
            access_token = token.get_access_token()    
            get_id_url = "https://api.spotify.com/v1/search?q={}&type=artist&limit=1&access_token={}"
            artist_list = requests.get(get_id_url.format(artist_name,access_token)).json()
            artist_list = artist_list['artists']
            artist_list = artist_list['items']
            artist_list = artist_list[0]
            name = get_name(artist_list)
            followers = get_followers(artist_list)
            picture = get_picture(artist_list)
            artist_id = get_id(artist_list)
            popularity = get_popularity(artist_list)
            user_type = get_user_type(artist_list)
            genres = get_genres(artist_list)
            artist_details = {
                'name': name,
                'picture': picture,
                'artist_id': artist_id,
                'link': 'https://open.spotify.com/artist/{}'.format(artist_id),
                'popularity':popularity,
                'user_type':user_type,
                'genres' : genres,
                'followers':followers,
            }
            return render(request,'artists/artist_details.html', {'artist_details':artist_details})

def song_search(request):
    songs = []
    track = []
    if request.method == "POST":
        token =util.oauth2.SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
        access_token = token.get_access_token()    
        song_name = request.POST.get('name')
        get_song_details_url = "https://api.spotify.com/v1/search?q={}&type=track&access_token={}"
        tracks = requests.get(get_song_details_url.format(song_name,access_token)).json()
        for song in tracks['tracks']['items']:
            songs.append(song['name'])
            songs.append(song['popularity'])
            songs.append(song['href'])
            songs.append(song['artists'][0]['name'])
            songs.append(song['album']['name'])
            songs.append(song['album']['images'][0]['url'])
            songs.append(song['name'] + ' ' + song['artists'][0]['name'])
            track.append(songs)
            songs = []
        context = {
            'tracks':track,
        }
        return render(request,'song/song_results.html', context=context)
    else:
        value = randint(0, 10)
        lyrics = random_lyrics[value]
        context = {
            'lyrics':lyrics,
        }
        return render(request,'song/song_search.html', context=context)


def song_detail(request, song_name):
    token =util.oauth2.SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    access_token = token.get_access_token()
    get_song_details_url = "https://api.spotify.com/v1/search?q={}&type=track&access_token={}"
    track = requests.get(get_song_details_url.format(song_name,access_token)).json()
    track_id = track['tracks']['items'][0]['id']
    get_track_detail_url = "https://api.spotify.com/v1/tracks/{}?access_token={}"
    track = requests.get(get_track_detail_url.format(track_id,access_token)).json()
    context = {
        'name':track['name'],
        'popularity':track['popularity'],
        'link':"https://open.spotify.com/track/" + track_id,
        'explicit':track['explicit'],
        'artist':track['artists'][0]['name'],
        'album':track['album']['name'],
        'image':track['album']['images'][0]['url'],
    }
    return render(request, 'song/song_details.html', context=context)

def recommend_songs(request, song_name=""):
    songs = []
    track = []
    if request.method == "POST":
        song_name=request.POST.get('name')
        token =util.oauth2.SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
        access_token = token.get_access_token()
        get_song_details_url = "https://api.spotify.com/v1/search?q={}&type=track&access_token={}"
        track_response = requests.get(get_song_details_url.format(song_name,access_token)).json()
        track_id = track_response['tracks']['items'][0]['id']
        get_recommend_url = "https://api.spotify.com/v1/recommendations?seed_tracks={}&access_token={}"
        tracks = requests.get(get_recommend_url.format(track_id,access_token)).json()
        for song in tracks['tracks']:
            songs.append(song['name'])
            songs.append(song['popularity'])
            songs.append("https://open.spotify.com/track/" + track_id),
            songs.append(song['artists'][0]['name'])
            songs.append(song['album']['name'])
            songs.append(song['album']['images'][0]['url'])
            track.append(songs)
            songs = []
        context = {
            'tracks':track,
        }
        return render(request,'song/recommend_results.html', context=context)
    else:
        if song_name == '':
            value = randint(0, 10)
            lyrics = random_lyrics[value]
            context = {
                'lyrics':lyrics,
            }
            return render(request,'song/recommend_search.html', context=context)
        else:
            token =util.oauth2.SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
            access_token = token.get_access_token()
            get_song_details_url = "https://api.spotify.com/v1/search?q={}&type=track&access_token={}"
            track_response = requests.get(get_song_details_url.format(song_name,access_token)).json()
            track_id = track_response['tracks']['items'][0]['id']
            get_recommend_url = "https://api.spotify.com/v1/recommendations?seed_tracks={}&access_token={}"
            tracks = requests.get(get_recommend_url.format(track_id,access_token)).json()
            for song in tracks['tracks']:
                songs.append(song['name'])
                songs.append(song['popularity'])
                songs.append("https://open.spotify.com/track/" + track_id),
                songs.append(song['artists'][0]['name'])
                songs.append(song['album']['name'])
                songs.append(song['album']['images'][0]['url'])
                track.append(songs)
                songs = []
            context = {
                'tracks':track,
            }
            return render(request,'song/recommend_results.html', context=context)


def recommend_artists(request, artist_name = ""):
    songs = []
    track = []
    if request.method == "POST":
        artist_name=request.POST.get('name')
        token =util.oauth2.SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
        access_token = token.get_access_token()
        get_artist_details_url = "https://api.spotify.com/v1/search?q={}&type=artist&access_token={}"
        artist_response = requests.get(get_artist_details_url.format(artist_name,access_token)).json()
        artist_id = artist_response['artists']['items'][0]['id']
        get_recommend_url = "https://api.spotify.com/v1/recommendations?seed_artists={}&access_token={}"
        artist_response = requests.get(get_recommend_url.format(artist_id,access_token)).json()
        for song in artist_response['tracks']:
            songs.append(song['name'])
            songs.append(song['popularity'])
            songs.append("https://open.spotify.com/artist/" + artist_id,)
            songs.append(song['artists'][0]['name'])
            songs.append(song['album']['name'])
            songs.append(song['album']['images'][0]['url'])
            track.append(songs)
            songs = []
        context = {
            'tracks':track,
        }
        return render(request,'song/recommend_results.html', context=context)
    else:
        if artist_name == '':
            value = randint(0, 10)
            lyrics = random_lyrics[value]
            context = {
                'lyrics':lyrics,
            }
            return render(request,'artists/recommended_search.html', context=context)
        else:
            token =util.oauth2.SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
            access_token = token.get_access_token()
            get_artist_details_url = "https://api.spotify.com/v1/search?q={}&type=artist&access_token={}"
            artist_response = requests.get(get_artist_details_url.format(artist_name,access_token)).json()
            artist_id = artist_response['artists']['items'][0]['id']
            get_recommend_url = "https://api.spotify.com/v1/recommendations?seed_artists={}&access_token={}"
            artist_response = requests.get(get_recommend_url.format(artist_id,access_token)).json()
            for song in artist_response['tracks']:
                songs.append(song['name'])
                songs.append(song['popularity'])
                songs.append("https://open.spotify.com/artist/" + artist_id,)
                songs.append(song['artists'][0]['name'])
                songs.append(song['album']['name'])
                songs.append(song['album']['images'][0]['url'])
                track.append(songs)
                songs = []
            context = {
                'tracks':track,
            }
            return render(request,'song/recommend_results.html', context=context)


def get_followers(artist_list):
    artist_list = artist_list['followers']
    followers = artist_list['total']
    return followers

def get_name(artist_list):
    name = artist_list['name']
    return name

def get_picture(artist_list):
    picture = artist_list['images'][0]['url']
    return picture

def get_id(artist_list):
    artist_id = artist_list['id']
    return artist_id

def get_popularity(artist_list):
    popularity = artist_list['popularity']
    return popularity

def get_user_type(artist_list):
    user_type = artist_list['type']
    return user_type

def get_genres(artist_list):
    genres = artist_list['genres']
    return genres