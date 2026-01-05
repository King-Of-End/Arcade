import math
from typing import List, Tuple

import arcade
from typing_extensions import Literal

from constants import PLAYER_SPEED, SHOOTING_TIME, BULLET_SPEED, CHARACTER_MAX_HP, INVULNERABILITY_TIME
from sprites.bullet_sprite import Bullet


class V1(arcade.SpriteSolidColor):
    def __init__(self,
                 x: float,
                 y: float,
                 speed: int = PLAYER_SPEED,
                 bullet_list: arcade.SpriteList = None,
                 mouse_placement: List[Tuple[int, int]] = None):
        super().__init__(40, 100, x, y, arcade.types.Color(128, 128, 128))
        self.speed = speed
        self.bullet_list = bullet_list
        self.mouse_placement = mouse_placement
        self.hp = CHARACTER_MAX_HP
        self.invulnerability_timer = 0.0

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.shooting_timer = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        self.shooting_timer += delta_time
        if self.shooting_timer > SHOOTING_TIME:
            self.shooting_timer -= SHOOTING_TIME
            self.shot()

        if self.invulnerability_timer > 0:
            self.invulnerability_timer = max(0.0, self.invulnerability_timer - delta_time)

        self.change_x = 0
        self.change_y = 0

        if self.moving_right:
            self.change_x = self.speed
        if self.moving_left:
            self.change_x -= self.speed
        if self.moving_up:
            self.change_y = self.speed
        if self.moving_down:
            self.change_y -= self.speed

        super().update(delta_time)

    def shot(self):
        """логика выстрела"""
        x, y = self.mouse_placement[0]
        dx = x - self.center_x
        dy = y - self.center_y
        angle = math.atan2(dy, dx)

        bullet = Bullet(self.center_x,
                        self.center_y,
                        BULLET_SPEED * math.cos(angle),
                        BULLET_SPEED * math.sin(angle),
                        -math.degrees(angle))
        self.bullet_list.append(bullet)

    def apply_damage(self, damage: int):
        if self.invulnerability_timer == 0:
            self.hp -= damage
            self.invulnerability_timer += INVULNERABILITY_TIME

    def get_hp(self) -> int:
        return self.hp
