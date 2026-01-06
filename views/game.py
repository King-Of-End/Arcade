import json
import sys
from typing import Tuple, List

import arcade
from arcade import SpriteList, Camera2D
from pyglet.event import EVENT_HANDLE_STATE

from sprites import V1, Slug, Worm
from constants import PLAYER_SPEED
from views.results_view import ResultsView


class Game(arcade.View):
    def __init__(self, menu_view: arcade.View):
        super().__init__()
        self.menu_view = menu_view
        self.kills = 0
        self.timer = 0

        self.bullet_list: SpriteList = arcade.SpriteList()
        self.mouse_placement: List[Tuple[int, int]] = [(0, 0)]

        self.difficulty, player_model = self.get_config()

        self.player: V1 = V1(
            self.center_x,
            self.center_y,
            PLAYER_SPEED,
            self.bullet_list,
            self.mouse_placement,
            player_model=player_model # это значение мы получим из окна выбора персонажа
        )
        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.player_list.append(self.player)

        self.enemies_list: arcade.SpriteList = arcade.SpriteList()

        self.setup()
        self.world_camera = Camera2D()

    def get_config(self):
        with open('config.json') as file:
            config = json.load(file)
        return config['difficulty'], config['player_model']

    def setup(self) -> None:
        self.add_enemies()


    def add_enemies(self):
        self.enemies_list.append(Slug(500, 500))
        self.enemies_list.append(Worm(300, 300))
        ... # Добавдение врагов в self.enemies_list

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemies_list.draw()

    def on_update(self, delta_time: float) -> bool | None:
        """Обновляем все спрайты, врагам передаём позицию игрока"""
        self.timer += delta_time

        self.player_list.update(delta_time)
        self.bullet_list.update(delta_time)
        self.enemies_list.update(delta_time, self.get_player_coords())

        contacting_player = arcade.check_for_collision_with_list(self.player, self.enemies_list)
        for enemy in contacting_player:
            self.player.apply_damage(12)

        if self.player.get_hp() < 0:
            self.end_game()

        for enemy in self.enemies_list:
            touching_bulet = arcade.check_for_collision_with_list(enemy, self.bullet_list)
            if touching_bulet:
                enemy.remove_from_sprite_lists()
                self.kills += 1
        #
        # self.world_camera.position = self.get_player_coords()


    def get_player_coords(self):
        return self.player.center_x, self.player.center_y

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.D:
            self.player.moving_right = True
        if symbol == arcade.key.A:
            self.player.moving_left = True
        if symbol == arcade.key.W:
            self.player.moving_up = True
        if symbol == arcade.key.S:
            self.player.moving_down = True

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.D:
            self.player.moving_right = False
        if symbol == arcade.key.A:
            self.player.moving_left = False
        if symbol == arcade.key.W:
            self.player.moving_up = False
        if symbol == arcade.key.S:
            self.player.moving_down = False

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> EVENT_HANDLE_STATE:
        self.mouse_placement.pop()
        self.mouse_placement.append((x, y))

    def end_game(self):
        """логика при проигрыше"""
        self.window.show_view(ResultsView(self.menu_view, self.kills, self.timer))
