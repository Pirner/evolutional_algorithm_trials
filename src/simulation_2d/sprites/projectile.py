import pygame
import numpy as np

from src.simulation_2d import constants

WHITE = (255, 255, 255)


class Projectile(pygame.sprite.Sprite):
    def __init__(
            self,
            velocity_x,
            velocity_y,
            border_x: int,
            border_y: int,
            im_filepath: str,
    ):
        """
        central class for the projectile which is being shot
        :param velocity_x:
        :param velocity_y:
        :param border_x:
        :param border_y:
        :param im_filepath: filepath to the asset which is being used for the projectile
        """
        super().__init__()
        color = (0, 0, 255)
        self.height = 20
        self.width = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.border_x = border_x
        self.border_y = border_y

        self.vel_x = velocity_x
        self.vel_y = velocity_y

        self.img = pygame.image.load(im_filepath)
        self.img = pygame.transform.scale(self.img, (40, 20))
        # pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()
        self.image = self.img

    def update(self):
        """
        update the projectile
        :return:
        """
        y_con = self.rect.y >= self.border_y
        x_con = self.rect.x >= self.border_x
        if (self.rect.y >= self.border_y - self.height) or (self.rect.x >= self.border_x - self.width):
            print('finished')
            self.vel_x = 0
            self.vel_y = 0
            return

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.vel_x += constants.HOR_SLOWDOWN
        self.vel_y -= constants.GRAVITY
        alpha = np.arctan(self.vel_x / (self.vel_y + 0.0001))
        alpha = np.rad2deg(alpha) + 90
        if self.vel_y >= 0:
            alpha += 180
        self.image = pygame.transform.rotate(self.img, alpha)

        print('x: {0}, y: {1}'.format(self.rect.y, self.rect.x))
