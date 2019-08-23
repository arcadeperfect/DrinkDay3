from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import os
from dd_util import get_img_path

class display(object):

	def __init__(self, drinkImage, mult):
		self.drinkImage = drinkImage
		self.mult=mult
		self.image_location = get_img_path()
		self.PILImage = self.load_image(os.path.join(self.image_location, drinkImage.file_name))
		print('matrix display')

		options = RGBMatrixOptions()
		options.rows = 32
		options.chain_length = 1
		options.parallel = 1
		options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

		print('creating matrix')
		self.matrix = RGBMatrix(options=options)

	def update(self):
		print("updating display with", self.PILImage)

	def load_image(self, path):
		print("load image")
		self.PILImage = Image.open(path)
		self.show(self.PILImage)

	def update_image(self, drinkImage):
		self.PILImage = Image.open(os.path.join(self.image_location, drinkImage.file_name))
		self.show(self.PILImage)


	def show(self, PILImage):
		PILImage.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)

		#self.matrix.SetImage(PILImage.convert('RGB'))


