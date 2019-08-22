from sys import platform
import logging
import time
import datetime
from dd_screen_display import screen_display
import dd
import threading

if platform == "darwin":
    osx = True
    pi = False
else:
    pi = True
    osx = False

display_live = False
sync_live = True
path = './resources/images'
update_interval = 5
sync_interval = 10

if sync_live:

    sync = dd.Sync(path)
rank = dd.Ranks(path)
selection = rank.select()
display = screen_display(selection, mult=10)
today = datetime.date.today()
lastUpdate = datetime.datetime.now()


# TODO: split syncing into own thread
# TODO: why is syncing suddenly slow
# TODO: replace prints with logs


c = 0
while True:

    if c == 0:
        print("\n\n#### begin loop ####\n\n")
    print(c)



    # if reached sync interval, attempt sync
    if sync_live:
        # time since last SYNC attempt
        time_since_check = (datetime.datetime.now() - sync.lastSync).total_seconds()

        if time_since_check >= sync_interval:
            print("check")
            sync.sync_files()

    # if reached selection interval, update image
    if rank.selection_time_delta() >= update_interval:
        print("interval update")
        display.update_image(rank.select())  # update the image with new selection

    # if day changes force an update
    if not datetime.date.today() == today:
        print("day change")
        display.update_image(rank.select())  # update the image with new selection

    display.update()  # update the display loop (needed for pygame eventloop to enable quitting)
    today = datetime.date.today()
    time.sleep(0.1)
    c += 1
