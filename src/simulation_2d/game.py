import pygame

from src.simulation_2d.sprites.car import Car
from src.colors import *


class GameSimulation2D:
    def __init__(self):
        """
        game simulation for a 2D environment
        """
        self.exit = False
        self.height = 840
        self.width = 2048
        self.canvas = pygame.display.set_mode((self.width, self.height))

    def start_mainloop(self):
        """
        start the mainloop of the game
        :return:
        """
        self.exit = False
        all_sprites_list = pygame.sprite.Group()
        player_car = Car((255, 0, 0), 20, 30)
        player_car.rect.x = 200
        player_car.rect.y = 300

        all_sprites_list.add(player_car)

        clock = pygame.time.Clock()

        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # Game Logic
            all_sprites_list.update()

            # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
            all_sprites_list.draw(self.canvas)

            # Draw The Road
            pygame.draw.rect(self.canvas, GREY, [40, 0, 200, 300])
            # Draw Line painting on the road
            pygame.draw.line(self.canvas, WHITE, [140, 0], [140, 300], 5)

            # pygame.display.update()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
