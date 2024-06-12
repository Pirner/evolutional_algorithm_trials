import random

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
        self.up_strength_cap = 45
        self.lo_strength_cap = 5

        self.target_max_x = 1300
        self.target_min_x = 800
        self.target_max_y = 330

        self.shoot_angle = 0
        self.up_angle = 90
        self.lo_angle = 0

        self.target = None
        self.all_sprites_list = None
        self.best_arrow = None
        self.best_score = 0.0

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

    def all_arrows_finished(self) -> bool:
        """
        check if all arrows are finished
        :return:
        """
        ret = True
        for arr in self.arrows:
            ret = ret and arr.finished
        return ret

    def generate_new_gen_of_arrows(self):
        """
        takes all the arrows and creates the next generation
        :return:
        """
        for arrow in self.arrows:
            arrow.evaluate_score()
        self.arrows.sort(key=lambda x: x.score, reverse=True)
        scores = [x.score for x in self.arrows]
        print(scores)
        n_arrows = len(scores)
        current_best_gen_arrow = self.arrows[0]
        new_gen_arrows = []
        for arrow in self.arrows:
            self.all_sprites_list.remove(arrow)

        # take most fit bird and mutate it
        for _ in range(n_arrows // 3):
            arrow = Projectile(
                velocity_x=15,
                velocity_y=-20,
                border_x=self.width,
                border_y=self.height,
                im_filepath='assets/arrow.png',
                target=self.target,
                up_streng_limit=self.up_strength_cap,
                lo_strength_limit=self.lo_strength_cap,
                up_angle_imit=self.up_angle,
                lo_angle_limit=self.lo_angle,
                male=self.arrows[0],
                female=None,
            )
            new_gen_arrows.append(arrow)
        for _ in range(n_arrows // 3):
            arrow = Projectile(
                velocity_x=15,
                velocity_y=-20,
                border_x=self.width,
                border_y=self.height,
                im_filepath='assets/arrow.png',
                target=self.target,
                up_streng_limit=self.up_strength_cap,
                lo_strength_limit=self.lo_strength_cap,
                up_angle_imit=self.up_angle,
                lo_angle_limit=self.lo_angle,
                male=self.arrows[1],
                female=None,
            )
            new_gen_arrows.append(arrow)
        for _ in range(n_arrows // 3):
            arrow = Projectile(
                velocity_x=15,
                velocity_y=-20,
                border_x=self.width,
                border_y=self.height,
                im_filepath='assets/arrow.png',
                target=self.target,
                up_streng_limit=self.up_strength_cap,
                lo_strength_limit=self.lo_strength_cap,
                up_angle_imit=self.up_angle,
                lo_angle_limit=self.lo_angle,
                male=self.arrows[0],
                female=self.arrows[1],
            )
            new_gen_arrows.append(arrow)
        self.arrows = new_gen_arrows
        for arrow in self.arrows:
            self.all_sprites_list.add(arrow)
        # handle the current best gen arrow
        tmp_arrow = arrow = Projectile(
                velocity_x=15,
                velocity_y=-20,
                border_x=self.width,
                border_y=self.height,
                im_filepath='assets/arrow.png',
                target=self.target,
                up_streng_limit=self.up_strength_cap,
                lo_strength_limit=self.lo_strength_cap,
                up_angle_imit=self.up_angle,
                lo_angle_limit=self.lo_angle,
                # male=self.arrows[0],
                # female=self.arrows[1],
            )
        tmp_arrow.inputWeights = current_best_gen_arrow.inputWeights.copy()
        tmp_arrow.hiddenWeights = current_best_gen_arrow.hiddenWeights.copy()

        self.arrows.append(tmp_arrow)
        self.all_sprites_list.add(tmp_arrow)

    def create_target(self):
        """
        create new target
        :return:
        """
        self.all_sprites_list.remove(self.target)
        target_x = random.randint(self.target_min_x, self.target_max_x)
        self.target = Target(
            pos_x=target_x,
            pos_y=self.target_max_y,
            size_x=225,
            size_y=225,
            im_filepath='assets/target.png'
        )
        self.all_sprites_list.add(self.target)

    def start_mainloop(self):
        """
        start the mainloop of the game
        :return:
        """
        use_ai = True
        n_arrows = 50
        n_rounds = 200

        self.exit = False
        self.all_sprites_list = pygame.sprite.Group()

        target = Target(
            pos_x=self.target_max_x,
            pos_y=self.target_max_y,
            size_x=225,
            size_y=225,
            im_filepath='assets/target.png'
        )
        self.target = target
        for _ in range(n_arrows):
            arrow = Projectile(
                velocity_x=15,
                velocity_y=-20,
                border_x=self.width,
                border_y=self.height,
                im_filepath='assets/arrow.png',
                target=target,
                up_streng_limit=self.up_strength_cap,
                lo_strength_limit=self.lo_strength_cap,
                up_angle_imit=self.up_angle,
                lo_angle_limit=self.lo_angle,
            )
            self.arrows.append(arrow)
            arrow.rotation_angle = self.shoot_angle
            self.all_sprites_list.add(arrow)
        # arrow.rect.x = 0
        # arrow.rect.y = self.height - arrow.height * 2
        self.all_sprites_list.add(target)

        clock = pygame.time.Clock()

        while not self.exit:
            if use_ai:
                # perform actions if genetic search is enabled
                for arrow in self.arrows:
                    if not arrow.shot:
                        streng_val, angle_val = arrow.make_shot_decision()
                        # fire arrow
                        arrow.shot = True
                        # set strength values from rotation and shoot angle
                        vel_x, vel_y = Arrow2DMathematics.get_velocity_x_velocity_y(streng_val, angle_val)
                        arrow.vel_x = vel_x
                        arrow.vel_y = vel_y
                if self.all_arrows_finished():
                    print('finished all arrows')
                    # move target
                    self.create_target()
                    self.generate_new_gen_of_arrows()

            else:
                self.update_values()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                            self.exit = False

                keys = pygame.key.get_pressed()

                # manual key inputs
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

                # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)

                self.canvas.blit(self.strength_text, (0, 0))
                self.canvas.blit(self.shoot_angle_text, (100, 0))

                # check for finished arrows
                if keys[pygame.K_r]:
                    self.reset_arrows()

            # Game Logic
            self.all_sprites_list.update()
            # self.canvas.fill(GREEN)
            self.canvas.blit(self.back_ground_img, (0, 0))
            self.canvas.blit(self.ballista_img, (0, self.height - 64))

            self.all_sprites_list.draw(self.canvas)
            pygame.display.flip()
            clock.tick(40)
        pygame.quit()
