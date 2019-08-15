from sys import platform
import logging


from dd_screen_display import screen_display
from dd_download import download, find_downloaded_images

if platform == "darwin":
    osx = True
    pi = False
else:
    pi = True
    osx = False

if osx:
    p = screen_display('d.png', mult = 30)


c = 0

while True:
    print(c)
    download()
    if osx:
        p.cycle()

        if c == 5:
            p.load_image("dd.png")

    #time.sleep(1)
    c += 1