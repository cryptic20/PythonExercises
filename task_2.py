# ========= Your classes ==========
import random


class Settings:
    def __init__(self, shuffle, repeat):
        self.repeat = repeat
        self.shuffle = shuffle


class Song:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.title == other.title and self.artist == other.artist and self.duration == other.duration

    def __str__(self):
        return f'{self.title} - {self.artist}: {self.duration}'


class Playlist:
    def __init__(self, title, songs):
        self.__title = title
        self.__songs = songs
        self.__index = 0

    def get_title(self):
        return self.__title

    def get_song_titles(self):
        return [song.title for song in self.__songs]

    def load_song_by_title(self, title):
        for x in self.__songs:
            if x.title == title:
                return x
        return None

    def load_next_song(self, shuffle, repeat):
        if shuffle:
            index = random.randint(0, len(self.__songs))
            return self.__songs[index]
        elif repeat:
            if self.__songs[self.__index] == self.__songs[-1]:
                self.__index = 0
                return self.__songs[self.__index]  # return to start
            else:
                self.__index += 1
                return self.__songs[self.__index]
        elif not shuffle and not repeat:
            if self.__index < 0:
                self.__index = 0
                return None
            elif self.__index < len(self.__songs):
                next_song = self.__songs[self.__index]
                self.__index += 1  # increment
                return next_song
            elif self.__index == len(self.__songs):
                self.__index = -1



class Spotify:
    def __init__(self, playlist, settings):
        self.__playlist = playlist
        self.__settings = settings
        self.__current_song = None
        self.__is_playing = False
        self.__is_paused = False

    def get_current_song(self):
        return self.__current_song

    def is_playing(self):
        return self.__is_playing

    def get_playlist_title(self):
        return playlist.get_title()

    def play(self, title=''):
        if title:
            self.__current_song = self.__playlist.load_song_by_title(title)
            self.__is_playing = True
        elif self.__current_song is None:
            song = self.__playlist.load_next_song(self.__settings.shuffle, self.__settings.repeat)
            self.__current_song = song
            self.__is_playing = True
        elif self.__current_song:
            self.__is_playing = True

    def pause(self):
        self.__is_paused = True
        self.__is_playing = False

    def next(self):
        next_song = self.__playlist.load_next_song(self.__settings.shuffle, self.__settings.repeat)
        if next_song:
            self.play(title=next_song.title)
        elif next_song is None:
            self.__current_song = None
            self.__is_playing = False

# =================================


if __name__ == '__main__':
    no_repeat_no_shuffle = Settings(False, False)

    songs = [Song("Hotel California", "Eagles", 390),
             Song("Harder Better Faster Stronger", "Daft Punk", 224),
             Song("2112", "Rush", 1233)]
    playlist = Playlist("MyPlaylist", songs)

    player = Spotify(playlist, no_repeat_no_shuffle)

    assert player.get_playlist_title() == "MyPlaylist"

    assert playlist.get_song_titles() == ["Hotel California", "Harder Better Faster Stronger", "2112"]

    assert playlist.load_next_song(False, False) == Song("Hotel California", "Eagles", 390)
    assert playlist.load_next_song(False, False) == Song("Harder Better Faster Stronger", "Daft Punk", 224)
    assert playlist.load_next_song(False, False) == Song("2112", "Rush", 1233)
    assert not playlist.load_next_song(False, False)
    assert playlist.load_song_by_title("2112") == Song("2112", "Rush", 1233)

    # Reset playlist
    playlist = Playlist("MyPlaylist", songs)
    player = Spotify(playlist, no_repeat_no_shuffle)

    player.play()
    assert player.get_current_song() == songs[0]
    assert player.is_playing()

    # Should not change song or playing
    player.play()
    assert player.get_current_song() == songs[0]
    assert player.is_playing()

    # Should not change song, playing is False
    player.pause()
    assert player.get_current_song() == songs[0]
    assert not player.is_playing()

    # Should not change song, playing back to True
    player.play()
    assert player.get_current_song() == songs[0]
    assert player.is_playing()

    # Should change song, playing True
    player.next()
    assert player.get_current_song() == songs[1]
    assert player.is_playing()

    # Should change song, playing True
    player.next()
    assert player.get_current_song() == songs[2]
    assert player.is_playing()

    # No songs left, song == None and playing False
    player.next()
    assert not player.get_current_song()
    assert not player.is_playing()

    # Load song by title
    player.play("2112")
    assert player.get_current_song() == songs[2]
    assert player.is_playing()

    # Previous song was last in playlist, next should return None, playing False
    player.next()
    assert not player.get_current_song()
    assert not player.is_playing()

    # Start playlist
    player.play()
    assert player.get_current_song() == songs[0]
    assert player.is_playing()

    player.next()
    player.next()
    player.next()
    assert not player.get_current_song()
    assert not player.is_playing()

    # When playlist is finished, calling next starts playlist again.
    player.next()
    assert player.get_current_song() == songs[0]
    assert player.is_playing()
