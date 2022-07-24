from typing import List

from models.song import Song
from utils.common_utils import CommonUtils


class ControllerSong:
    @staticmethod
    def get_playlist_songs(playlist_id: id) -> List[Song]:
        result = []

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT songs.song_id, song_uuid, song_name, album, modified, songs.created, songs.is_deleted "
                    "FROM songs "
                    "INNER JOIN songs_in_playlists sip on songs.song_id = sip.song_id AND sip.playlist_id = %(playlist_id)s ",
                    {"playlist_id": playlist_id}
                )
                playlists = cur.fetchall()

                if playlists:
                    for song_id, song_uuid, song_name, album, modified, created, is_deleted in playlists:
                        new_song = Song(
                            id=song_id,
                            uuid=str(song_uuid),
                            name=song_name,
                            album=album,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
                        result.append(new_song)
        return result
