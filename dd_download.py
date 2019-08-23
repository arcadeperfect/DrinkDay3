from ftplib import FTP
import os
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format,
                    level=logging.INFO,
                    datefmt="%H:%M:%S")

address = 'ftp.rojanasakul.com'
account = 'rjnskl@rojanasakul.com'
password = '+1nWVNaIL|D"XS'
downLoadPath = os.path.join(os.path.dirname(__file__),'resources/images')
path = './resources/images'

def download():
    ignore = ['.', '..']
    listing = []
    files = []
    ftp = FTP(address)
    ftp.login(account, password)
    ftp.cwd('drinkDay')
    ftp.retrlines("LIST", listing.append)



    for l in listing:
            filename = l.split(None, 8)[-1].lstrip()
            if not filename in ignore:
                local_filename = os.path.join(downLoadPath, filename)
                lf = open(local_filename, "wb")
                ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
                lf.close()
                files.append(filename)
                logging.info(f"downloaded {l}")
                #print '\ndownloaded: ', l

    return files

def find_downloaded_images(path):
    files = [x for x in os.listdir(path) if x[0] != '.']
    return files
