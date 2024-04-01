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
        self.width = 1024
        self.canvas = pygame.display.set_mode((self.width, self.height))

    def start_mainloop(self):
        """
        start the mainloop of the game
        :return:
        """
        self.exit = False
        all_sprites_list = pygame.sprite.Group()
        player_car = Car((255, 0, 0), 20, 30)
        player_car.rect.x = 0
        player_car.rect.y = 0
        all_sprites_list.add(player_car)

        bullet = Projectile(velocity_x=10, velocity_y=-10, border_x=self.width, border_y=self.height)
        bullet.rect.x = 0
        bullet.rect.y = self.height - bullet.height * 2
        all_sprites_list.add(bullet)

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
            # Draw The Road
            pygame.draw.rect(self.canvas, GREY, [40, 0, 200, 300])
            # Draw Line painting on the road
            pygame.draw.line(self.canvas, WHITE, [140, 0], [140, 300], 5)

            # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
            all_sprites_list.draw(self.canvas)

            # pygame.display.update()
            pygame.display.flip()
            clock.tick(10)
        pygame.quit()
