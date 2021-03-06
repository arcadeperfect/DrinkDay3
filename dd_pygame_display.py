import os



import pygame


class display(object):

    def __init__(self, drinkImage, mult=20, enable_display = True):
        self.enable_display = enable_display
        if self.enable_display:
            pygame.init()
            self.X = 32
            self.Y = 16
            self.mult = mult
            self.X *= self.mult
            self.Y *= self.mult
            self.image_location = "./resources/images"
            self.display_surface = pygame.display.set_mode((self.X, self.Y))
            self.pyGameImage = self.load_image(os.path.join(self.image_location, drinkImage.file_name))
            self.display_surface.blit(self.pyGameImage, (0, 0))
            # pygame.display.update()
            self.update()

    def update(self):

        self.display_surface.blit(self.pyGameImage, (0, 0))

        for event in pygame.event.get():
            # print(event)

            if event.type == pygame.QUIT:
                pygame.quit()

                quit()

        pygame.display.update()

    def load_image(self, path):
        self.pyGameImage = pygame.transform.scale(pygame.image.load(path), (self.X, self.Y))
        self.update()
        return self.pyGameImage

    def update_image(self, drinkImage):
        self.pyGameImage = self.load_image(os.path.join(self.image_location, drinkImage.file_name))
        self.update()
