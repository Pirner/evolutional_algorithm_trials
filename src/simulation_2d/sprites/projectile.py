import pygame
import math
import random

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
            target,
            up_streng_limit: int,
            lo_strength_limit: int,
            up_angle_imit: int,
            lo_angle_limit: int,
            male=None,
            female=None,
    ):
        """
        central class for the projectile which is being shot
        :param velocity_x:
        :param velocity_y:
        :param border_x:
        :param border_y:
        :param im_filepath: filepath to the asset which is being used for the projectile
        :param target: target which the arrow is being shot at
        """
        super().__init__()
        color = (0, 0, 255)
        self.up_streng_limit = up_streng_limit
        self.lo_strength_limit = lo_strength_limit
        self.up_angle_imit = up_angle_imit
        self.lo_angle_limit = lo_angle_limit

        self.height = 20
        self.width = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.border_x = border_x
        self.border_y = border_y
        self.target = target

        self.vel_x = velocity_x
        self.vel_y = velocity_y
        self.rotation_angle = 90

        self.img = pygame.image.load(im_filepath)
        self.img = pygame.transform.scale(self.img, (60, 30))
        # pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()
        self.image = self.img
        self.rect = self.image.get_rect()
        self.bounding_rect = None
        self.shot = False
        self.finished = False

        self.rect.width -= 55
        self.rect.left += 200
        self.rect.x = 0
        self.rect.y = self.border_y - 55

        self.collision_head_x_offset = 40
        self.collision_head = None
        self.create_collision_head()
        self.score = 0.0

        # genetic algorithm parts
        self.learning_rate = 0.005

        if male is None:  # New Bird, no parents
            # easy network
            self.inputWeights = np.random.normal(0, scale=0.1, size=(2, 3))
            self.hiddenWeights = np.random.normal(0, scale=0.1, size=(3, 2))
        elif female is None:  # Only one Parent (self mutate)
            self.inputWeights = male.inputWeights
            self.hiddenWeights = male.hiddenWeights
            self.mutate()
        else:  # Two parents - Breed.
            self.inputWeights = np.random.normal(0, scale=0.1, size=(2, 3))
            self.hiddenWeights = np.random.normal(0, scale=0.1, size=(3, 2))
            self.breed(male, female)

    def reset_arrow(self):
        """
        reset the arrow on the canvas and the position
        :return:
        """
        self.shot = False
        self.finished = False
        self.vel_y = 0
        self.vel_x = 0
        self.rotation_angle = 0
        self.rect.x = 0
        self.rect.y = self.border_y - 55
        self.create_collision_head()

    def create_collision_head(self):
        """
        create collision head for the simulation
        :return:
        """
        self.collision_head = self.rect.copy()
        self.collision_head.x += self.collision_head_x_offset
        self.collision_head.height -= 10
        self.collision_head.top += 5

    def check_collision(self, target) -> bool:
        """
        check whether the arrow has collided yet
        :param target:
        :return:
        """
        if self.collision_head.colliderect(target.ellipse):
            return True
        return False

    def evaluate_score(self) -> float:
        """
        evaluate the score of the shot arrow
        :return:
        """
        assert self.finished
        # check if is collided with the target
        self.score = 0.0
        center_of_target_x = int(self.target.ellipse[0] + 0.5 * self.target.ellipse[2])
        center_of_target_y = int(self.target.ellipse[1] + 0.5 * self.target.ellipse[3])

        coll_head_x = int(self.collision_head[0] + 0.5 * self.collision_head[2])
        coll_head_y = int(self.collision_head[1] + 0.5 * self.collision_head[3])
        distance_x = abs(center_of_target_x - coll_head_x)
        distance_y = abs(center_of_target_y - coll_head_y)
        distance = math.sqrt(math.pow(distance_x, 2) + math.pow(distance_y, 2))
        max_dist = math.sqrt(math.pow(self.target.ellipse[2], 2) + math.pow(self.target.ellipse[3], 2))
        self.score = 1 - distance / max_dist
        self.score = 200 / distance

        if self.check_collision(self.target):
            self.score += 200

        print(self.score)
        return self.score

    @staticmethod
    def relu(x):
        """The relu activation function for the neural network

        INPUT: x - The value to apply the ReLu function on
        OUTPUT: The applied ReLus function value"""

        return np.maximum(x, 0)

    @staticmethod
    def sigmoid(x):
        """The sigmoid activation function for the neural net

        INPUT: x - The value to calculate
        OUTPUT: The calculated result"""

        return 1 / (1 + np.exp(-x))

    def set_weights(self, input_weights, hidden_weights):
        """Overwrites the current weights of the birds brain (neural network).

        INPUT:  inputWeights: The weights for the neural network (input layer)
                hiddenWeights: The weights for the neural network (hidden layer)
        OUTPUT:	None"""
        self.inputWeights = input_weights
        self.hiddenWeights = hidden_weights

    def make_shot_decision(self):
        # get inputs for the algorithm
        center_of_target_x = int(self.target.ellipse[0] + 0.5 * self.target.ellipse[2])
        center_of_target_y = int(self.target.ellipse[1] + 0.5 * self.target.ellipse[3])

        coll_head_x = int(self.collision_head[0] + 0.5 * self.collision_head[2])
        coll_head_y = int(self.collision_head[1] + 0.5 * self.collision_head[3])
        distance_x = abs(center_of_target_x - coll_head_x)
        distance_y = abs(center_of_target_y - coll_head_y)

        x = [distance_x, distance_y]

        hidden_layer_in = np.dot(x, self.inputWeights)
        hidden_layer_out = Projectile.sigmoid(hidden_layer_in)
        output_layer_in = np.dot(hidden_layer_out, self.hiddenWeights)
        prediction = self.sigmoid(output_layer_in)

        # share strength
        strength_value = round(self.lo_strength_limit + (self.up_streng_limit - self.lo_strength_limit) * prediction[0])
        angle_value = round(self.lo_angle_limit + (self.up_angle_imit - self.lo_angle_limit) * prediction[1])
        return strength_value, angle_value

    def update(self):
        """
        update the projectile
        :return:
        """
        if self.finished:
            self.score = self.evaluate_score()
            return

        self.finished = self.check_collision(self.target)

        if not self.shot:
            self.image = pygame.transform.rotate(self.img, self.rotation_angle)
            return

        y_con = self.rect.y - 50 >= self.border_y
        x_con = self.rect.x >= self.border_x
        if (self.rect.y >= self.border_y - self.height - 10) or (self.rect.x >= self.border_x - int(2 * self.width)):
            # print('finished')
            self.vel_x = 0
            self.vel_y = 0
            self.finished = True
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

        self.collision_head.x = self.rect.x + self.collision_head_x_offset
        self.collision_head.y = self.rect.y

        # print('x: {0}, y: {1}'.format(self.rect.y, self.rect.x))

    def mutate(self):
        """mutate (randomly apply the learning rate) the birds brain
            (neural network) randomly changing the individual weights

        INPUT:  None
        OUTPUT:	None"""
        for i in range(len(self.inputWeights)):
            for j in range(len(self.inputWeights[i])):
                self.inputWeights[i][j] = self.get_mutated_gene(self.inputWeights[i][j])
        for i in range(len(self.hiddenWeights)):
            for j in range(len(self.hiddenWeights[i])):
                self.hiddenWeights[i][j] = self.get_mutated_gene(self.hiddenWeights[i][j])

    # genetic algorithm code
    def get_mutated_gene(self, weight):
        """mutate the input by -0.125 to 0.125 or not at all

        INPUT: weight - The weight to mutate
        OUTPUT: mutatedWeight - The mutated weight"""

        multiplier = 0
        learning_rate = random.randint(0, 25) * self.learning_rate
        rand_bool = bool(random.getrandbits(1))  # adapt upwards or downwards?
        rand_bool2 = bool(random.getrandbits(1))  # or not at all?

        if rand_bool and rand_bool2:
            multiplier = 1
        elif not rand_bool and rand_bool2:
            multiplier = -1

        mutated_weight = weight + learning_rate * multiplier

        return mutated_weight

    def breed(self, male, female):
        """Generate a new brain (neural network) from two parent birds
             by averaging their brains and mutating them afterwards

        INPUT:  male - The male bird object (of class bird)
                female - The female bird object (of class bird)
        OUTPUT:	None"""
        for i in range(len(self.inputWeights)):
            self.inputWeights[i] = (male.inputWeights[i] +
                                    female.inputWeights[i]) / 2

        for i in range(len(self.hiddenWeights)):
            self.hiddenWeights[i] = (male.hiddenWeights[i] +
                                     female.hiddenWeights[i]) / 2
