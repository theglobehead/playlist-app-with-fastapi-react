# Playlists with Flask

## Database diagram

```mermaid
classDiagram
    class user{
        id: in
        uuid: uuid
        user_name: varchar<350>
        hashed_password: varchar<64>
        passsword_salt: varchar<8>
        modified: timestamp
        created: timestamp
        is_deleted: bool
    }

    class playlist{
        id: int
        user_id: int
        name: varchar<350>
        modified: timestamp
        created: timestamp
        is_deleted: bool
    }

    class song{
        id: int
        name: varchar<350>
        artist_id: int
        album: str
        audio_path: uuid
        modified: timestamp
        created: timestamp
        is_deleted: bool
    }

    class artist{
        id: int
        name: varchar<350>
        modified: timestamp
        created: timestamp
        is_deleted: bool
    }

    class tag{
        id: int
        name: varchar<350>
        modified: timestamp
        created: timestamp
        is_deleted: bool
    }

    class tags_in_artists{
        id: int
        tag_id: int
        artist_id: int
        created: timestamp
        is_deleted: bool
    }

    class tags_in_songs{
        id: int
        tag_id: int
        songs_id: int
        created: timestamp
        is_deleted: bool
    }

    class tags_in_playlists{
        id: int
        tag_id: int
        playlist_id: int
        created: timestamp
        is_deleted: bool
    }

    class songs_in_playlists{
        id: int
        song_id: int
        playlist_id: int
        created: timestamp
        is_deleted: bool
    }

    tags_in_playlists o-- playlist
    tags_in_playlists o-- tag

    tags_in_songs o-- tag
    tags_in_songs o-- song

    tags_in_artists o-- tag
    tags_in_artists o-- artist

    songs_in_playlists o-- song
    songs_in_playlists o-- playlist

    playlist --* user
    song --* artist
```

## Models diagram

```mermaid
classDiagram
    class User{
        playlists: ~Playlist~

        id: int
        uuid: str
        user_name: str
        hashed_password: str
        passsword_salt: str
        modified: datetime
        created: datetime
        is_deleted: bool
    }

    class Playlist{
        songs: ~Song~
        owner: User
        tags: ~Tags~

        id: int
        user_id: int
        name: str
        modified: datetime
        created: datetime
        is_deleted: bool
    }

    class Song{
        tags: ~Tags~

        id: int
        name: str
        artist_id: int
        album: str
        audio_path: str
        modified: datetime
        created: datetime
        is_deleted: bool
    }

    class Artist{
        songs: ~Song~
        tags: ~Tags~

        id: int
        name: str
        modified: datetime
        created: datetime
        is_deleted: bool
    }

    class Tag{
        id: int
        name: str
        modified: datetime
        created: datetime
        is_deleted: bool
    }

    User *-- Playlist
    Playlist *-- Song
    Song *-- Artist
    Song *-- Tag
    Playlist *-- Tag
```
