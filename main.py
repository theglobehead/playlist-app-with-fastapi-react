from loguru import logger

import uvicorn
from fastapi import FastAPI, Form, status, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from controllers.controller_song import ControllerSong
from controllers.controller_user import ControllerUser
from controllers.controller_database import ControllerDatabase
from models.artist import Artist
from models.playlist import Playlist
from models.user import User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register_user", status_code=status.HTTP_406_NOT_ACCEPTABLE)
def register_user(
        response: Response,
        name: str = Form(""),
        password1: str = Form(""),
        password2: str = Form(""),
):
    is_form_valid = ControllerUser.validate_register_form(name, password1, password2)

    if is_form_valid:
        try:
            user = ControllerUser.create_user(name=name, password=password1)
            response.status_code = status.HTTP_201_CREATED
            return {"user_uuid": user.user_uuid}
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            logger.exception(e)
    else:
        return {"reason": "form not valid"}
        


@app.get("/get_user_playlists", status_code=status.HTTP_200_OK)
def get_user_playlists(user_uuid: str):
    user_id = ControllerDatabase.get_user_id_by_uuid(user_uuid)
    user = User(user_id=user_id)
    user_playlists = ControllerDatabase.get_user_playlists(user=user)

    user_playlists = [user_playlist.to_dict() for user_playlist in user_playlists]

    return user_playlists


@app.get("/get_playlist", status_code=status.HTTP_200_OK)
def get_playlist(playlist_uuid: str):
    playlist = ControllerDatabase.get_playlist_by_uuid(playlist_uuid)

    return playlist.to_dict()


@app.post("/save_playlist", status_code=status.HTTP_200_OK)
def save_playlist(user_uuid: str, playlist_name: str):
    user = ControllerDatabase.get_user_by_uuid(user_uuid)
    ControllerDatabase.insert_playlist(Playlist(playlist_name=playlist_name, owner_user_id=user.user_id))


@app.delete("/delete_playlist", status_code=status.HTTP_200_OK)
def delete_playlist(playlist_uuid: str):
    playlist_id = ControllerDatabase.get_playlist_id_by_uuid(playlist_uuid)
    ControllerDatabase.delete_playlist(playlist_id)


@app.delete("/delete_playlist", status_code=status.HTTP_200_OK)
def remove_song(playlist_uuid: str, song_uuid: str):
    song_id = ControllerDatabase.get_song_id_by_uuid(song_uuid)
    playlist_id = ControllerDatabase.get_playlist_id_by_uuid(playlist_uuid)

    ControllerDatabase.remove_song_from_playlist(playlist_id, song_id)


@app.post("/login", status_code=status.HTTP_200_OK)
def login(
        response: Response,
        name: str = Form(...),
        password: str = Form(...),
        remember_me: bool = Form(...)
):
    print("name:", name)
    user = ControllerUser.log_user_in(name, password, remember_me)

    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return

    return {
        "user_uuid": user.user_uuid,
        "token_uuid": user.token.token_uuid,
    }


@app.post("/add_song", status_code=status.HTTP_200_OK)
def add_song(playlist_uuid: str, song_uuid: str):
    playlist_id = ControllerDatabase.get_playlist_id_by_uuid(playlist_uuid)
    song_id = ControllerDatabase.get_song_id_by_uuid(song_uuid)

    ControllerDatabase.add_song_to_playlist(playlist_id, song_id)


@app.get("/get_songs_in_page", status_code=status.HTTP_200_OK)
def get_songs_in_page(page: int = 1):
    page_size = 6
    songs = ControllerDatabase.get_songs(
        page_offset=page - 1,
        page_size=page_size
    )

    songs = [song.to_dict() for song in songs]
    return songs


@app.get("/get_song_artist", status_code=status.HTTP_200_OK)
def get_song_artist(song_uuid: str):
    song_id = ControllerDatabase.get_song_id_by_uuid(song_uuid)
    song = ControllerDatabase.get_song(song_id)

    return song.artist.to_dict()


@app.post("/upload_song", status_code=status.HTTP_200_OK)
def upload_song(
        song_name: str,
        album_name: str,
        song_image: UploadFile,
        song_audio: UploadFile,
):
    ControllerSong.upload_song(
        name=song_name,
        album=album_name,
        audio=song_audio,
        image=song_image,
    )


@app.get("/get_artists", status_code=status.HTTP_200_OK)
def get_artists():
    page_size = 50
    artists_list = ControllerDatabase.get_artists(page_size)

    artists_list = [artist.to_dict() for artist in artists_list]
    return artists_list


@app.get("/create_artist", status_code=status.HTTP_200_OK)
def create_artist(artist_name: str, parent_artist_name: str):
    parent_artist = ControllerDatabase.get_artist_by_name(artist_name=parent_artist_name)
    ControllerDatabase.insert_artist(
        artist=Artist(artist_name=artist_name),
        parent_artist=parent_artist
    )


@app.get("/check_if_artist_exists", status_code=status.HTTP_200_OK)
def check_if_artist_exists(artist_name: str):
    artist = ControllerDatabase.get_artist_by_name(artist_name)
    result = bool(artist)

    return {"result": result}


if __name__ == "__main__":
    uvicorn.run(app='main:app', reload=True)
