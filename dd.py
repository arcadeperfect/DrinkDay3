# from datetime import datetime
import argparse
import configparser
import datetime
import logging
import os
import shlex
from ftplib import FTP
from operator import itemgetter
from os import listdir
from random import randint

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format,
                    level=logging.INFO,
                    datefmt="%H:%M:%S")


class Sync(object):
    # sync local image files with remote ftp

    def __init__(self, path):
        print("init sync")
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read('ftp_config.ini')
        self.path = self.config['main']['path']

        self.absolute_download_path = os.path.join(os.path.dirname(__file__), self.path)
        self.sync_files()
        self.lastSync = datetime.datetime.now()

    def sync_files(self):
        try:
            print("syncing")
            address = self.config['main']['ftp_address']
            account = self.config['main']['ftp_account']
            password = self.config['main']['ftp_password']
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
            self.lastSync = datetime.datetime.now()
        except Exception as e:
            print("sync failed:")
            print(e)

        self.lastSync = datetime.datetime.now()

    def list_downloaded_images(self, path):
        files = [x for x in os.listdir(path) if x[0] != '.']
        return files


class Parse(object):

    # class to find images and parse the arguments into DrinkImage objects

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

        # convert date string from argument into datetime object
        try:
            date_object = datetime.date(int(options.date[0:2]) + 2000, int(options.date[2:4]), int(options.date[4:7]))

        except:
            date_object = None

        image = DrinkImage(  # crate new DrinkImage object
            name=name,
            file_name=file_name,
            priority=options.priority,
            specified_date=date_object,
            drink_day_state=options.drinkDay,
        )

        return image

    def get_drink_images(self):

        return self.drink_image_list


class DrinkImage(object):

    # class to hold the image and associated meta data, also calculates score

    def __init__(self, name, file_name, priority=0, specified_date=None, drink_day_state=None, score=0):
        self.name = name
        self.file_name = file_name
        self.priority = priority
        self.specified_date = specified_date
        self.drink_day_state = drink_day_state
        self.time = None
        self.score = 0


class Ranks(object):

    def __init__(self, path):
        print("init ranks")
        self.drinkOrNotDrink = DrinkOrNotDrink()  # boolean to invert current drinkDay state
        self.drink = self.drinkOrNotDrink.get()  # determine if today is a drinkDay
        self.path = path  # set location of image files
        self.parse()  # create DrinkImage objects from files, create init score
        self.lastSelectionTime = None
        self.pool = None

    def parse(self):

        self.pool = []
        for i in Parse(self.path).get_drink_images():
            self.pool.append(i)
        if len(self.pool) == 0:
            print("no images!")
            exit()

    def select(self):  # select an image based on scoring and chaning conditions
        self.parse()
        self.drink = self.drinkOrNotDrink.get()
        ranks = []
        for i in self.pool:
            # if i.drink_day_state == self.drink:
            self.score_image(i)
            ranks.append([i.score, i])
        ranks = sorted(ranks, reverse=True, key=itemgetter(0))
        pool = [x[1] for x in ranks if x[0] == ranks[0][0]]
        selection = pool[randint(0, len(pool) - 1)]
        self.lastSelectionTime = datetime.datetime.now()
        print('selected', selection.name)
        return selection

    def score_image(self, drinkImage):  # logic to determine score
        this_score = 0

        if self.drink == drinkImage.drink_day_state:
            drinkImage.score += 3
            this_score += 3

        if drinkImage.specified_date == datetime.date.today():
            drinkImage.score += 5
            this_score += 5
        return this_score

    def selection_time_delta(self):
        return (datetime.datetime.now() - self.lastSelectionTime).total_seconds()


class DrinkOrNotDrink(object):

    def __init__(self):
        print('init drinkOrNotDrink')
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read('drink_config.ini')
        self.invert = self.config['main']['invert']

        if 'false' in self.invert.lower():
            self.invert = False
        elif 'true' in self.invert.lower():
            self.invert = True

        self.day = None
        self.dayOfYear = None
        self.update()

    def update(self):

        self.day = datetime.date.today()
        self.dayOfYear = datetime.datetime.now().timetuple().tm_yday

        if self.invert:
            divide = 0
        else:
            divide = 1

        if self.dayOfYear % 2 == divide:
            self.drink = True
        else:
            self.drink = False
        print('drinkday is', self.drink, '\n')
        return self.drink

    def get(self):
        self.update()
        return self.drink
