from ftplib import FTP
import os
import logging
from os import listdir
import datetime
import argparse
import shlex
from operator import itemgetter
from random import randint
from pprint import pprint

path = "./resources/images"
current_day_drinkDay_state = 1
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format,
                    level=logging.INFO,
                    datefmt="%H:%M:%S")

#TODO: sort out date time weirdness - what is "to object"?



class Sync(object):
    # sync local image files with remote ftp

    def __init__(self, path):
        print("init sync")
        self.path = path
        self.absolute_download_path = os.path.join(os.path.dirname(__file__), 'resources/images')
        self.sync_files()

    def sync_files(self):
        address = 'ftp.rojanasakul.com'
        account = 'rjnskl@rojanasakul.com'
        password = '+1nWVNaIL|D"XS'

        ignore = ['.', '..']
        listing = []
        files = []
        ftp = FTP(address)
        ftp.login(account, password)
        ftp.cwd('drinkDay')
        ftp.retrlines("LIST", listing.append)
        number_of_downloades = 0

        for l in listing:
            filename = l.split(None, 8)[-1].lstrip()

            if not filename in ignore and not filename in self.list_downloaded_images(self.path):
                local_filename = os.path.join(self.absolute_download_path, filename)
                lf = open(local_filename, "wb")
                ftp.retrbinary("RETR " + filename, lf.write, 8 * 1024)
                lf.close()
                files.append(filename)
                logging.info(f"downloaded {l}")
                number_of_downloades += 1

        logging.info(f"downloaded {number_of_downloades} images")

    def list_downloaded_images(self, path):
        files = [x for x in os.listdir(path) if x[0] != '.']
        return files


class DrinkImage(object):

    # class to hold the image and associated meta data, also calculates score

    def __init__(self, name, file_name, priority=0, specified_date=None, drink_day_state=None, score=0):
        self.name = name
        self.file_name = file_name
        self.priority = priority
        self.specified_date = specified_date
        self.drink_day_state = drink_day_state
        self.score = score

        self.score_image()

    def score_image(self):
        #TODO: add some more scoring logic
        #TODO: will it know the current drinkday state?

        if self.drink_day_state == current_day_drinkDay_state:
            self.score = 3

        if self.specified_date == datetime.date.today():
            self.score += 5


class Parse(object):

    # class to find images and parse the arguments into DrinkImage objects
    # TODO: maybe incorporate into the DrinkImage class

    def __init__(self, path):
        self.path = path
        self.found_image_files = self.find_images()
        self.drink_image_list = []

        for i in self.found_image_files:
            self.drink_image_list.append(self.parse_image_arguments(i))

    def find_images(self):
        self.found_image_files = [x for x in listdir(self.path) if x[0] != '.']
        return self.found_image_files

    def parse_image_arguments(self, file_name):
        argument_list = shlex.split(file_name)

        parser = argparse.ArgumentParser(description='drinkDay parser')
        parser.add_argument('-z', '--drinkDay', type=int)
        parser.add_argument('-p', '--priority', type=int)
        parser.add_argument('-t', '--time')
        parser.add_argument('-d', '--date')

        options = parser.parse_known_args(argument_list)[0]

        name = argument_list[0]


        image = DrinkImage(
            name=name,
            file_name=file_name,
            priority=options.priority,
            specified_date=options.date,
            drink_day_state=options.drinkDay,
        )

        return image

    def get_drink_images(self):
        return self.drink_image_list


class Ranks(object):

    def __init__(self, path):
        print("init ranks")
        self.ranking = []
        self.path = path
        self.parse()
        self.sort()


    def parse(self):
        self.ranking = []
        for i in Parse(path).get_drink_images():
            self.ranking.append([i.score, i.name, i])

    def sort(self):
        s = sorted(self.ranking, reverse=True, key=itemgetter(0))
        self.ranking = s
        return self.ranking

    def select(self):

        #top_rank = self.ranking[0][0]

        pool = [x[2] for x in self.ranking if x[0] == self.ranking[0][0]] # create selection pool of entries sharing the highest score
        selection = pool[randint(0,len(pool)-1)]
        return selection




if __name__ == "__main__":

    s = Sync()

    while True:

        print("running")
        r = Ranks(path)
        selection = r.select()
        print(selection)
        #pprint(r.ranking)







