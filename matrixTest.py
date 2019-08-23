from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image


# image_file = "./resources/images/drink.png -z=1"
# image = Image.open(image_file)
#
# options = RGBMatrixOptions()
# options.rows = 32
# options.chain_length = 1
# options.parallel = 1
# options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
#
# matrix = RGBMatrix(options = options)
#
# # Make image fit our screen.
# image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
#
# matrix.SetImage(image.convert('RGB'))


class matrix(object):

    def __init__(self):
        self.image_file = "./resources/images/drink.png -z=1"
        self.image = Image.open(self.image_file)

        options = RGBMatrixOptions()
        options.rows = 32
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

        self.matrix = RGBMatrix(options=options)

    def show(self):
        self.image.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        self.matrix.SetImage(self.image.convert('RGB'))


m = matrix()
m.show()