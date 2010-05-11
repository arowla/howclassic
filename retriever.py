#!/usr/bin/env python

import datetime
import mechanize
import codecs
import os

SOURCE_FILE_ENCODING = 'iso-8859-1'
URL_FORMAT_STR = "http://www.mediabase.com/whatsong/whatsong.asp?var_s=087066073071045070077&MONDTE=%s"
DATA_DIR = "data"

class Retriever():
    def __init__(self):
        self.today = datetime.datetime.now()
        one_day = datetime.timedelta(days=1)
        self.yesterday = (self.today - one_day)

    def format_date_for_url(self, dt):
        return dt.strftime("%m/%d/%Y")

    def format_date_for_file(self, dt):
        return dt.strftime("%Y%m%d")

    def filename_for_date(self, dt):
        return os.path.join(DATA_DIR, "{0}.html".format(self.format_date_for_file(dt)))

    def open_file_for_date(self, dt, mode):
        return open(self.filename_for_date(dt), mode)

    def latest_two_filenames(self):
        filenames = []
        for date in [self.today, self.yesterday]:
            name = self.filename_for_date(date)
            if os.path.isfile(name):
                filenames.append(name)
            else:
                raise IOError("You must run the retriever first, as we don't have current files.")

        return filenames

    def retrieve(self):
        for date in [self.today, self.yesterday]:
            if os.path.isfile(self.filename_for_date(date)):
                continue

            file = self.open_file_for_date(date, "w")
            url = URL_FORMAT_STR % self.format_date_for_url(date)
            browser = mechanize.Browser()
            data = browser.open(url).get_data()
            file.write(data)
            file.close()


if __name__== '__main__':
    retriever = Retriever()
    retriever.retrieve()

