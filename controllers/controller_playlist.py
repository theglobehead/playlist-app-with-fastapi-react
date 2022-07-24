from typing import List

from controllers.controller_song import ControllerSong
from models.playlist import Playlist
from utils.common_utils import CommonUtils


class ControllerPlaylist:
    @staticmethod
    def get_user_playlists(user_id: id) -> List[Playlist]:
        result = []

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT playlist_id, playlist_name, playlist_uuid, modified, created, is_deleted "
                    "FROM playlists "
                )
                playlists = cur.fetchall()

                if playlists:
                    for playlist_id, playlist_name, playlist_uuid, modified, created, is_deleted in playlists:
                        playlist_songs = ControllerSong.get_playlist_songs(playlist_id)
                        new_playlist = Playlist(
                            id=playlist_id,
                            uuid=str(playlist_uuid),
                            name=playlist_name,
                            songs=playlist_songs,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
                        result.append(new_playlist)
        return result

    @staticmethod
    def get_playlist_by_uuid(uuid: str):
        result = None

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT playlist_id, playlist_name, playlist_uuid, modified, created, is_deleted "
                    "FROM playlists "
                    "WHERE playlist_uuid = %(uuid)s",
                    {"uuid": uuid}
                )
                result = cur.fetchone()

                if result:
                    playlist_id, playlist_name, playlist_uuid, modified, created, is_deleted = result
                    playlist_songs = ControllerSong.get_playlist_songs(playlist_id)
                    result = Playlist(
                        id=playlist_id,
                        uuid=str(playlist_uuid),
                        name=playlist_name,
                        songs=playlist_songs,
                        modified=modified,
                        created=created,
                        is_deleted=is_deleted,
                    )
        return result
