import pygame
import os


class screen_display(object):

    def __init__(self, drinkImage, mult=20):
        pygame.init()
        self.X = 32
        self.Y = 16
        self.mult = mult
        self.X *= self.mult
        self.Y *= self.mult
        self.image_location = "./resources/images"
        self.display_surface = pygame.display.set_mode((self.X, self.Y))
        self.image = self.load_image(os.path.join(self.image_location, drinkImage.file_name))
        self.display_surface.blit(self.image, (0, 0))
        # pygame.display.update()
        self.update()

    def update(self):

        self.display_surface.blit(self.image, (0, 0))

        for event in pygame.event.get():
            # print(event)

            if event.type == pygame.QUIT:
                pygame.quit()

                quit()

        pygame.display.update()

    def load_image(self, path):
        self.image = pygame.transform.scale(pygame.image.load(path), (self.X, self.Y))
        self.update()
        return self.image

    def update_image(self, drinkImage):
        self.image = self.load_image(os.path.join(self.image_location, drinkImage.file_name))
        self.update()
