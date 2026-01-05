from typing import Tuple, List

import arcade
from arcade import SpriteList
from pyglet.event import EVENT_HANDLE_STATE

from sprites.player import V1
from constants import PLAYER_SPEED


class Game(arcade.Window):
    def __init__(self, speed):
        super().__init__(800, 600, 'free Ultrakill clone')
        self.bullet_list: SpriteList = arcade.SpriteList()
        self.mouse_placement: List[Tuple[int, int]] = [(0, 0)]

        self.player: V1 = V1(
            self.center_x,
            self.center_y,
            PLAYER_SPEED,
            self.bullet_list,
            self.mouse_placement
        )
        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.player_list.append(self.player)


    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.bullet_list.draw()

    def on_update(self, delta_time: float) -> bool | None:
        self.player_list.update(delta_time)
        self.bullet_list.update(delta_time)

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

def main():
    game = Game(200)
    arcade.run()

if __name__ == "__main__":
    main()