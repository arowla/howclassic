#!/usr/bin/env python

from lxml import etree
from play import Play

class PlayParser():
    def __init__(self, date, filename):
        self.date = date
        self.filename = filename

    def parse(self):
        parser = etree.HTMLParser()
        tree = etree.parse(self.filename, parser)
        result = etree.tostring(tree.getroot(), pretty_print=True, method="html")

        rows = tree.findall(".//tr")
        plays = []

        for tr in rows:
            cells = list(tr)
            # see if we can skip non-song rows this way
            if len(cells) < 5: continue
            # the time cell is bare, no span
            time = cells[0].text

            # we need to get past the span element in both the other cells
            artist_cell = list(cells[2])

            # some rows can be empty, so skip those
            if len(artist_cell) < 1: continue
            artist = artist_cell[0].text

            song_cell = list(cells[4])
            song = song_cell[0].text

            plays.append(Play(self.date, time, artist, song))

        return plays
