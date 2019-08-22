from sys import platform
import logging
import time
import datetime
from dd_screen_display import screen_display
import dd
import threading
import configparser
from dd_util import get_img_path

if platform == "darwin":
    osx = True
    pi = False

else:
    pi = True
    osx = False

enable_display = False
enable_sync = False
path = get_img_path()
update_interval = 2
sync_interval = 1000

if enable_sync:
    sync = dd.Sync(path)

# TODO: split syncing into own thread
# TODO: why is syncing suddenly slow
# TODO: replace prints with logs


c = 0
while True:

    if c == 0:
        print("\n\n#### init loop ####\n\n")
        rank = dd.Ranks(path)
        selection = rank.select()
        display = screen_display(selection, mult=10)
        today = datetime.date.today()
        lastUpdate = datetime.datetime.now()
    #print(c)

    # if reached sync interval, attempt sync
    if enable_sync:
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
    time.sleep(1)
    c += 1
