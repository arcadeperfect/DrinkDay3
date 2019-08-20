from sys import platform
import logging
import time

from dd_screen_display import screen_display
# from dd_download import download, list_downloaded_images
import dd

if platform == "darwin":
    osx = True
    pi = False
else:
    pi = True
    osx = False

# if osx:
#     p = screen_display('d.png', mult = 30)


display = True
path = './resources/images'
s = dd.Sync(path)
r = dd.Ranks(path)

c = 0


while True:
    print(c)

    if c % 50 == 0:         # check for new files every n loops
        print('check')
        s.sync_files()

    s=r.select()


    if display:             # update display
        if c == 0:
            if osx:
                p = screen_display(s, mult=30)
            if pi:
                print("do pi things")
        p.cycle()
        if c == 5:
            p.load_image("dd.png")

    time.sleep(0.1)
    c += 1
