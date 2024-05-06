import pygame


WHITE = (255, 255, 255)


class Target(pygame.sprite.Sprite):
    def __init__(
            self,
            pos_x: int,
            pos_y: int,
            size_x: int,
            size_y: int,
            im_filepath: str,
    ):
        """
        initialize target sprite
        :param pos_x: position x
        :param pos_y: position y
        :param size_x: size in horizontal x distance
        :param size_y: size in vertical y distance
        :param im_filepath: filepath to the asset
        """
        super().__init__()
        self.pos_x = pos_x
        self.pox_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

        self.image = pygame.Surface([self.size_x, self.size_y])
        self.image.fill(WHITE)

        self.img = pygame.image.load(im_filepath)
        self.img = pygame.transform.scale(self.img, (self.size_x, self.size_y))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pox_y
        self.image = self.img
