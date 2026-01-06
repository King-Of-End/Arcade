import json
import math
import random
import sys
from typing import Tuple, List

import arcade
from arcade import SpriteList, Camera2D
from arcade.particles import Emitter, EmitMaintainCount, FadeParticle
from pyglet.event import EVENT_HANDLE_STATE

from sprites import V1, Slug, Worm, BrickWall, Bird
from constants import PLAYER_SPEED
from views.results_view import ResultsView

SPARK_TEX = [
    arcade.make_soft_circle_texture(8, arcade.color.PASTEL_YELLOW),
    arcade.make_soft_circle_texture(8, arcade.color.PEACH),
    arcade.make_soft_circle_texture(8, arcade.color.BABY_BLUE),
    arcade.make_soft_circle_texture(8, arcade.color.ELECTRIC_CRIMSON),
]


def make_trail(attached_sprite, maintain=40):
    emit = Emitter(
        center_xy=(attached_sprite.center_x, attached_sprite.center_y),
        emit_controller=EmitMaintainCount(maintain),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEX),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 1.6),
            lifetime=random.uniform(0.35, 0.6),
            start_alpha=220,
            end_alpha=0,
            scale=random.uniform(0.25, 0.4),
        ),
    )
    emit._attached = attached_sprite
    return emit

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
            player_model=player_model  # это значение мы получим из окна выбора персонажа
        )
        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.player_list.append(self.player)

        self.enemies_list: arcade.SpriteList = arcade.SpriteList()

        self.walls_list: SpriteList = arcade.SpriteList()
        self.setup()
        self.engine = arcade.PhysicsEngineSimple(
            self.player,
            self.walls_list
        )

        self.enemy_types = [Bird, Slug, Worm]

        self.world_camera = Camera2D()
        self.emitters = []

    def get_config(self):
        with open('config.json') as file:
            config = json.load(file)
        return config['difficulty'], config['player_model']

    def setup(self) -> None:
        for _ in range(random.randint(1000, 2000)):
            x, y = random.randint(-9000, 9000), random.randint(-9000, 9000)
            wall = BrickWall(x, y)
            self.walls_list.append(wall)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemies_list.draw()
        self.walls_list.draw()
        for emitter in self.emitters:
            emitter.draw()

    def on_update(self, delta_time: float) -> bool | None:
        """Обновляем все спрайты, врагам передаём позицию игрока"""
        self.timer += delta_time

        self.player_list.update(delta_time)
        self.bullet_list.update(delta_time)
        self.enemies_list.update(delta_time, self.get_player_coords())
        self.engine.update()

        if abs(self.player.center_x) > 10000:
            self.player.center_x *= -1
        if abs(self.player.center_y) > 10000:
            self.player.center_x *= -1

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

        self.world_camera.position = self.get_player_coords()
        emitters_copy = self.emitters.copy()
        for emitter in emitters_copy:
            emitter.update(delta_time)
            if emitter.can_reap():
                self.emitters.remove(emitter)

        if len(self.enemies_list) < 5:
            enemy_coords = self.get_random_points_on_circle(self.get_player_coords()[0], self.get_player_coords()[1], 1000)
            for i in enemy_coords:
                enemy = random.choice(self.enemy_types)(*i)
                self.enemies_list.append(enemy)
                self.emitters.append(enemy.trail_emitter)

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
        world_x, world_y = self.world_camera.unproject((x, y))[:2]
        self.mouse_placement[0] = (world_x, world_y)

    def end_game(self):
        """логика при проигрыше"""
        self.world_camera.position = -100000, -1000
        self.player.position = 500, 400
        self.window.show_view(ResultsView(self.menu_view, self.kills, self.timer))

    def get_random_points_on_circle(self, center_x: float, center_y: float, radius: float) -> list[tuple[float, float]]:
        points = []
        used_angles = set()

        with open('config.json', 'r') as file:
            data = json.load(file)

        counter = data['difficulty']

        while len(points) < int(counter) * 2:
            angle = random.uniform(0, 2 * math.pi)

            angle_deg = round(math.degrees(angle))

            if angle_deg in used_angles:
                continue

            used_angles.add(angle_deg)

            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            points.append((x, y))

        return points
