import datetime

class Play():
    def __init__(self, date, time, artist, song):
        self.played_at = datetime.datetime.strptime("{0} {1}".format(date.strftime("%m/%d/%Y"), time), "%m/%d/%Y %I:%M %p")
        self.artist = artist
        self.song = song

    def pretty_print(self):
        return "Time: {0}\nArtist: {1}\nSong: {2}\n".format(self.played_at, self.artist, self.song)

