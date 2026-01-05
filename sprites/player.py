import math
from typing import List, Tuple

import arcade
from typing_extensions import Literal

from constants import PLAYER_SPEED, SHOOTING_TIME, BULLET_SPEED, CHARACTER_MAX_HP, INVULNERABILITY_TIME
from sprites.bullet_sprite import Bullet


class V1(arcade.Sprite):
    def __init__(self,
                 x: float,
                 y: float,
                 speed: int = PLAYER_SPEED,
                 bullet_list: arcade.SpriteList = None,
                 mouse_placement: List[Tuple[int, int]] = None, player_model=0):
        super().__init__()
        self.speed = speed
        self.bullet_list = bullet_list
        self.mouse_placement = mouse_placement
        self.hp = CHARACTER_MAX_HP
        self.invulnerability_timer = 0.0

        self.texture_list = []
        self.texture_list.append(arcade.load_texture(f'images/player_{player_model}_1.png'))
        self.texture_list.append(arcade.load_texture(f'images/player_{player_model}_afk.png'))
        self.texture_list.append(arcade.load_texture(f'images/player_{player_model}_2.png'))
        self.texture_list.append(arcade.load_texture(f'images/player_{player_model}_afk.png'))
        self.animation_frame = 0
        self.texture = self.texture_list[0]

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.scale = 0.2
        self.shooting_timer = 0
        self.animation_timer = 0
        self.anim_flag = False

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
            self.scale_x = -0.2
            self.anim_flag = True
        if self.moving_left:
            self.change_x -= self.speed
            self.scale_x = 0.2
            self.anim_flag = True
        if self.moving_up:
            self.change_y = self.speed
            self.anim_flag = True
        if self.moving_down:
            self.change_y -= self.speed
            self.anim_flag = True
        if self.anim_flag:
            self.animation_timer += delta_time
            if self.animation_timer >= 0.2:
                self.animation_timer = 0
                self.animation_frame += 1
            if self.animation_frame > len(self.texture_list) - 1:
                self.animation_frame = 0
            self.texture = self.texture_list[self.animation_frame]
            self.anim_flag = False
        else:
            self.animation_timer = 0
            self.animation_frame += 1
            self.texture = self.texture_list[1]

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
