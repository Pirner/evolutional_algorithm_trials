from typing import Tuple

import numpy as np


class Arrow2DMathematics:
    @staticmethod
    def get_velocity_x_velocity_y(strength: int, shoot_angle: int) -> Tuple[int, int]:
        """
        get velocity x and velocity y
        :param strength: shoot strength set
        :param shoot_angle: shoot angle set
        :return:
        """
        # b is the streng into y
        # sin angle = b / c
        alpha = np.deg2rad(shoot_angle)

        b = np.sin(alpha) * strength
        # a is the strength into x
        # cos angle = a / c
        a = np.cos(alpha) * strength
        return a, -b
