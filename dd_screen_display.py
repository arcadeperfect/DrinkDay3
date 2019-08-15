import pygame

class screen_display(object):

    def __init__(self, path, mult = 20):
        pygame.init()
        self.X = 32
        self.Y = 16
        self.mult = mult
        self.X *= self.mult
        self.Y *= self.mult

        self.image = self.load_image(path)

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
        self.image = pygame.transform.scale(pygame.image.load(path), (self.X, self.Y))
        return self.image