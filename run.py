from parser import PlayParser
from retriever import Retriever
import sqlite3

print("Starting...")
retriever = Retriever()

def query(c, sql, args=[]):
    print(sql)
    c.execute(sql, args)

latest_files = retriever.latest_two_filenames()
latest_dates = [retriever.today, retriever.yesterday]

for (filename, date) in zip(latest_files, latest_dates):
    print ("Importing {0} for date {1}".format(filename, date.strftime("%Y%m%d")))
    parser = PlayParser(date, filename)
    plays = parser.parse()

    conn = sqlite3.connect('db/top40.db')

    for play in plays:
        c = conn.cursor()

        # find/insert artist
        query(c, 'select artist_id from artists where name=?', [play.artist])
        rows = c.fetchall()
        print(len(rows))
        if len(rows) < 1:
            query(c, 'insert into artists (name) values (?)', [play.artist])
            conn.commit()

        query(c, 'select artist_id, name from artists where name=?', [play.artist])
        artist = c.fetchone()
        print("We now have 1 artist with name {0}".format(artist[1]))
        artist_id = artist[0]

        # find/insert song
        query(c, 'select song_id from songs where name=? and artist_id=?', [play.song, artist_id])
        rows = c.fetchall()
        print(len(rows))
        if len(rows) < 1:
            query(c, 'insert into songs (name, artist_id) values (?,?)', [play.song, artist_id])
            conn.commit()

        query(c, 'select song_id, name, artist_id from songs where name=? and artist_id=?', [play.song, artist_id])
        song = c.fetchone()
        print("We now have 1 song named {0}".format(song[1]))
        song_id = song[0]

        # find/insert play
        query(c, 'select play_id from plays where played_at=? and song_id=?', [play.played_at, song_id])
        rows = c.fetchall()
        print(len(rows))
        if len(rows) < 1:
            query(c, 'insert into plays (played_at, song_id) values (?,?)', [play.played_at, song_id])
            conn.commit()

        query(c, 'select play_id from plays where played_at=? and song_id=?', [play.played_at, song_id])
        play = c.fetchone()
        print("We now have a play with play_id {0}".format(play[0]))

