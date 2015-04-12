# -*- coding: utf-8 -*-
from flask import render_template
import jsonrpclib, ast, os



@app.route('/recently_added_episodes/<server_id>')
def recently_added_episodes(server_id):
    return render_recently_added_episodes(server_id)


@app.route('/recently_added_movies/<server_id>')
def recently_added_movies(server_id):
    return render_recently_added_movies(server_id)


@app.route('/recently_added_albums/<server_id>')
def xhr_recently_added_albums(server_id):
    return render_recently_added_albums(server_id)


def render_recently_added_episodes(server_id):
    xbmc = jsonrpclib.Server(get_recent_xbmc_api_url('recently_added_server'))
    recently_added_episodes = get_recently_added_episodes(xbmc, server)

    return render_template('recently_added/tv.html',
                            recently_added_episodes = recently_added_episodes)


def render_recently_added_movies(server_id):
    xbmc = jsonrpclib.Server(get_recent_xbmc_api_url('recently_added_movies_server'))
    recently_added_movies = get_recently_added_movies(xbmc, server)

    return render_template('recently_added/movies.html',
                            recently_added_movies = recently_added_movies)


def render_recently_added_albums(server_id):
    xbmc = jsonrpclib.Server(get_recent_xbmc_api_url('recently_added_albums_server'))
    recently_added_albums = get_recently_added_albums(xbmc, server)


    return render_template('recently_added/albums.html',
                            recently_added_albums = recently_added_albums)


def get_recently_added_episodes(xbmc, server):
    num_recent_videos = 28

    try:
        recently_added_episodes = xbmc.VideoLibrary.GetRecentlyAddedEpisodes(properties = ['title', 'season', 'episode', 'showtitle', 'playcount', 'thumbnail', 'tvshowid'])['episodes']
    except:
        recently_added_episodes = []

    return recently_added_episodes


def get_recently_added_movies(xbmc, server):
    num_recent_videos = 28

    try:
        recently_added_movies = xbmc.VideoLibrary.GetRecentlyAddedMovies(properties = ['title', 'year', 'rating', 'playcount', 'thumbnail'])['movies']
    except:
        recently_added_movies = []

    return recently_added_movies

def get_recently_added_albums(xbmc, server):
    num_recent_albums = 28

    try:
        recently_added_albums = xbmc.AudioLibrary.GetRecentlyAddedAlbums(properties = ['title', 'year', 'rating', 'artist', 'thumbnail'])['albums']
        for album in recently_added_albums:
            if 'artist' in album and isinstance(album['artist'], list): #Frodo
                album['artist'] = " / ".join(album['artist'])
    except:
        recently_added_albums = []

    return recently_added_albums

