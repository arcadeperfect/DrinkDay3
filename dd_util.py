import configparser

def get_img_path():
    config = configparser.ConfigParser()
    config.sections()
    config.read('ftp_config.ini')
    return config['main']['image_path']