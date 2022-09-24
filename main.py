import datetime
import json
from json import JSONEncoder

import uvicorn
from fastapi import FastAPI, Form, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from controllers.controller_user import ControllerUser
from controllers.controller_database import ControllerDatabase
from models.user import User

app = FastAPI()
templates = Jinja2Templates(directory="static")

origins = [
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/register_user", status_code=status.HTTP_201_CREATED)
def register_user(
        response: Response,
        name: str = Form(""),
        password1: str = Form(""),
        password2: str = Form(""),
):
    is_form_valid = ControllerUser.validate_register_form(name, password1, password2)

    if is_form_valid:
        try:
            ControllerUser.create_user(name=name, password=password1)
            response.status_code = status.HTTP_201_CREATED
        except Exception as e:
            logger.exception(e)


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


if __name__ == "__main__":
    uvicorn.run(app='main:app', reload=True)
