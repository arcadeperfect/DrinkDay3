import pygame
import os


class screen_display(object):

    def __init__(self, drinkImage, mult = 20):
        pygame.init()
        self.X = 32
        self.Y = 16
        self.mult = mult
        self.X *= self.mult
        self.Y *= self.mult
        image_location = "./resources/images"
        #self.image = self.load_image(os.path.join(image_location, drinkImage.file_name))

        self.image = self.load_image("dd.png")

        self.display_surface = pygame.display.set_mode((self.X, self.Y))
        pygame.display.set_caption('Image')
        self.display_surface.blit(self.image, (0, 0))
        pygame.display.update()


    def cycle(self):

        self.display_surface.blit(self.image, (0, 0))

        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()

                quit()

        pygame.display.update()

    def load_image(self, path):
        self.image = pygame.transform.scale(pygame.image.load("dd.png"), (self.X, self.Y))
        return self.image