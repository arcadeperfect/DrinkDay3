from ftplib import FTP
import os
import logging
from os import listdir
import datetime
#from datetime import datetime
import argparse
import shlex
from operator import itemgetter
from random import randint
from pprint import pprint

path = "./resources/images"
current_day_drinkDay_state = 0
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format,
                    level=logging.INFO,
                    datefmt="%H:%M:%S")

class Sync(object):
    # sync local image files with remote ftp

    def __init__(self, path):
        print("init sync")
        self.path = path
        self.absolute_download_path = os.path.join(os.path.dirname(__file__), 'resources/images')
        self.sync_files()
        self.lastSync = datetime.datetime.now()

    def sync_files(self):
        try:
            d = g
            print("syncing")
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
            self.lastSync = datetime.datetime.now()
        except:
            print("syncing failed")

        self.lastSync = datetime.datetime.now()

    def list_downloaded_images(self, path):
        files = [x for x in os.listdir(path) if x[0] != '.']
        return files



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

        # convert date string from argument into datetime object
        try:
            date_object = datetime.date(int(options.date[0:2]) + 2000, int(options.date[2:4]), int(options.date[4:7]))

        except:
            date_object = None

        image = DrinkImage(
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
        self.score = None


class Ranks(object):

    def __init__(self, path):
        print("init ranks")
        #self.ranking = [] # don't think i need this
        self.drinkObject = DrinkOrNotDrink(invert=False)     # boolean to invert current drinkDay state
        self.drink = self.drinkObject.get()                 # determine if today is a drinkDay
        self.path = path                                    # set location of image files
        self.parse()                                        # create DrinkImage objects from files, create init score
        self.sort()                                         # sort the ran by score

    def parse(self):
        self.ranking = []
        for i in Parse(path).get_drink_images():
            score = self.score_image(i)
            self.ranking.append([score, i.name, i])

    def update_scores(self):

        for i in self.ranking:
            self.drinkObject.update()
            thisScore = self.score_image(i[2])              # run on drinkImage, which is 3rd element in list
            i[0] = thisScore                                # set first list element as score for sorting #TODO: refactor this into oblivion
            i[2].score = thisScore                          # set drinkImage object's own score variable

    def score_image(self,drinkImage):                       # logic to determine score
        thisScore = 0
        # print("scoring")
        # print("self.drink = ", self.drink)
        # print("drinkImage.drink_day_state = ", drinkImage.drink_day_state)
        if self.drink == drinkImage.drink_day_state:
            #drinkImage.score += 3
            thisScore += 3

        if drinkImage.specified_date == datetime.date.today():
            #drinkImage.score += 5
            thisScore += 5
        return thisScore

    def sort(self):
        s = sorted(self.ranking, reverse=True, key=itemgetter(0))
        self.ranking = s
        return self.ranking

    def select(self):

        pool = [x[2] for x in self.ranking if x[0] == self.ranking[0][0]] # create selection pool of entries sharing the highest score
        self.drinkObject.update()
        self.update_scores()
        selection = pool[randint(0,len(pool)-1)]
        self.lastSelectionTime = datetime.datetime.now()
        return selection

    def selection_time_delta(self):
        return (datetime.datetime.now()-self.lastSelectionTime).total_seconds()


class DrinkOrNotDrink(object):

    def __init__(self, invert=True):
        print('init drinkOrNotDrink')

        self.invert = invert


        self.update()

    def update(self):

        self.day = datetime.date.today()
        self.dayOfYear = datetime.datetime.now().timetuple().tm_yday
        #print('day of year is', self.dayOfYear)
        print('invert is', self.invert)

        if self.invert:
            #print('inverting')
            divide = 0
        else:
            #print('not inverting')
            divide = 1
        #print('divide is', divide)

        if self.dayOfYear%2 == divide:
            self.drink = True
        else:
            self.drink = False
        print('drinkday is', self.drink, '\n')
        return self.drink

    def get(self):
        return self.drink



if __name__ == "__main__":

    s = Sync()

    while True:

        print("running")
        r = Ranks(path)
        selection = r.select()
        print(selection)
        #pprint(r.ranking)








