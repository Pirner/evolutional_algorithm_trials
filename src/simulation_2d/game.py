import pygame

from src.simulation_2d.mathematics import Arrow2DMathematics
from src.simulation_2d.sprites.projectile import Projectile
from src.simulation_2d.sprites.target import Target
from src.colors import *


class GameSimulation2D:
    def __init__(self):
        """
        game simulation for a 2D environment
        """
        self.arrows = []
        self.exit = False
        self.height = 512
        self.width = 1536
        self.canvas = pygame.display.set_mode((self.width, self.height))
        self.strength = 30
        self.up_strength_cap = 50
        self.lo_strength_cap = 10

        self.shoot_angle = 0
        self.up_angle = 90
        self.lo_angle = 0

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Arial', self.strength)
        self.strength_text = self.my_font.render('{0}'.format(self.strength), False, (0, 0, 0))
        self.shoot_angle_text = self.my_font.render('{0}'.format(self.shoot_angle), False, (0, 0, 0))

        # create background
        self.back_ground_img = pygame.image.load('assets/background.jpg')
        self.back_ground_img = pygame.transform.scale(self.back_ground_img, (self.width, self.height))
        self.canvas.blit(self.back_ground_img, (0, 0))

        # create ballista sprite
        self.ballista_img = pygame.image.load('assets/ballista.png')
        self.ballista_img = pygame.transform.scale(self.ballista_img, (64, 64))
        self.ballista_img = pygame.transform.flip(self.ballista_img, True, False)
        self.canvas.blit(self.ballista_img, (0, 0))

    def update_values(self):
        self.my_font = pygame.font.SysFont('Arial', 30)
        self.strength_text = self.my_font.render('{0}'.format(self.strength), False, (0, 0, 0))
        self.shoot_angle_text = self.my_font.render('{0}'.format(self.shoot_angle), False, (0, 0, 0))

    def reset_arrows(self):
        """
        reset arrows in there
        :return:
        """
        for arrow in self.arrows:
            if arrow.rotation_angle:
                arrow.reset_arrow()
            if arrow.finished and False:
                arrow.rotation_angle = self.shoot_angle
                arrow.rect.x = 0
                arrow.rect.y = self.height - 55
                arrow.finished = False
                arrow.shot = False

    def start_mainloop(self):
        """
        start the mainloop of the game
        :return:
        """
        self.exit = False
        all_sprites_list = pygame.sprite.Group()

        target = Target(
            pos_x=1300,
            pos_y=330,
            size_x=225,
            size_y=225,
            im_filepath='assets/target.png'
        )

        arrow = Projectile(
            velocity_x=15,
            velocity_y=-20,
            border_x=self.width,
            border_y=self.height,
            im_filepath='assets/arrow.png',
            target=target,
        )
        self.arrows.append(arrow)
        arrow.rotation_angle = self.shoot_angle
        # arrow.rect.x = 0
        # arrow.rect.y = self.height - arrow.height * 2
        all_sprites_list.add(target)
        all_sprites_list.add(arrow)

        clock = pygame.time.Clock()

        while not self.exit:
            self.update_values()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                        self.exit = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                if self.strength > self.lo_strength_cap:
                    self.strength -= 1
            if keys[pygame.K_RIGHT]:
                if self.strength < self.up_strength_cap:
                    self.strength += 1
            if keys[pygame.K_SPACE]:
                if not arrow.shot:
                    # fire arrow
                    arrow.shot = True
                    # set strength values from rotation and shoot angle
                    vel_x, vel_y = Arrow2DMathematics.get_velocity_x_velocity_y(self.strength, self.shoot_angle)
                    arrow.vel_x = vel_x
                    arrow.vel_y = vel_y
            if keys[pygame.K_UP]:
                if self.shoot_angle < self.up_angle:
                    self.shoot_angle += 1
                    arrow.rotation_angle = self.shoot_angle
            if keys[pygame.K_DOWN]:
                if self.shoot_angle > self.lo_angle:
                    self.shoot_angle -= 1
                    arrow.rotation_angle = self.shoot_angle

            # Game Logic
            all_sprites_list.update()
            # self.canvas.fill(GREEN)
            self.canvas.blit(self.back_ground_img, (0, 0))
            self.canvas.blit(self.ballista_img, (0, self.height - 64))

            # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
            all_sprites_list.draw(self.canvas)
            self.canvas.blit(self.strength_text, (0, 0))
            self.canvas.blit(self.shoot_angle_text, (100, 0))

            # check for finished arrows
            if keys[pygame.K_r]:
                self.reset_arrows()

            # DEBUG STATES
            color = (255, 0, 0)
            # ellipse = pygame.draw.ellipse(self.canvas, color, target.ellipse)
            # bounding_rectangle_projectile = pygame.draw.rect(self.canvas, color, arrow.collision_head)

            # pygame.display.update()
            pygame.display.flip()
            clock.tick(40)
        pygame.quit()
