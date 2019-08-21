from sys import platform
import logging
import time
import datetime
from dd_screen_display import screen_display
import dd

if platform == "darwin":
    osx = True
    pi = False
else:
    pi = True
    osx = False

display_live = True
path = './resources/images'
interval = 5
sync_interval = 60
drink = dd.DrinkOrNotDrink(invert=True)

sync = dd.Sync(path)
rank = dd.Ranks(path)
selection = rank.select()
display = screen_display(selection, mult=30)

#TODO: handle case when no images
#TODO: why doesn't closing window quit any more
#TODO: handle when no internet connection
#TODO: split syncing into own thread
#TODO: why is syncing suddenly slow
#TODO: current day is drinkday? class

c = 0

while True:

    if c == 0:
        print("being loop")
    #print(c)
    drink.update()
    print("drinkday is", drink.drink)

    time_since_check = (datetime.datetime.now()-sync.lastSync).total_seconds()

    if time_since_check >= sync_interval:
        print("check")
        sync.sync_files()

    time_since_selection = (datetime.datetime.now()-selection.time).total_seconds()

    if time_since_selection >= interval:

        selection = rank.select()
        display.update_image(selection)

    #rank.update()


    display.update()
    time.sleep(0.5)
    c += 1
