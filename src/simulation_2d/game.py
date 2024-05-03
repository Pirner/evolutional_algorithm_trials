import pygame

from src.simulation_2d.sprites.car import Car
from src.simulation_2d.sprites.projectile import Projectile
from src.colors import *


class GameSimulation2D:
    def __init__(self):
        """
        game simulation for a 2D environment
        """
        self.exit = False
        self.height = 512
        self.width = 1536
        self.canvas = pygame.display.set_mode((self.width, self.height))
        self.strength = 30

        pygame.font.init()
        my_font = pygame.font.SysFont('Arial', self.strength)
        self.strength_value = 30
        self.strength_text = my_font.render('{0}'.format(self.strength_value), False, (0, 0, 0))

    def start_mainloop(self):
        """
        start the mainloop of the game
        :return:
        """
        self.exit = False
        all_sprites_list = pygame.sprite.Group()

        arrow = Projectile(
            velocity_x=15,
            velocity_y=-20,
            border_x=self.width,
            border_y=self.height,
            im_filepath='assets/arrow.png'
        )
        arrow.rect.x = 0
        arrow.rect.y = self.height - arrow.height * 2
        all_sprites_list.add(arrow)

        clock = pygame.time.Clock()

        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                        self.exit = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_car.move_left(5)
            if keys[pygame.K_RIGHT]:
                player_car.move_right(5)

            # Game Logic
            all_sprites_list.update()
            self.canvas.fill(GREEN)

            # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
            all_sprites_list.draw(self.canvas)
            self.canvas.blit(self.strength_text, (0, 0))

            # pygame.display.update()
            pygame.display.flip()
            clock.tick(40)
        pygame.quit()
