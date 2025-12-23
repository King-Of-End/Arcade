import arcade
from typing_extensions import Literal

SPEED: int = 200

class V1(arcade.SpriteSolidColor):
    def __init__(self, x, y):
        super().__init__(40, 100, x, y, arcade.types.Color(128, 128, 128))
        self.y = y
        self.speed = SPEED
        self.jump: bool = False
        self.in_air: bool = False
        self.slam: bool = False
        self.moving_left = False
        self.moving_right = False
        self.change_x = 0
        self.center_x = x
        self.sliding = False
        self.sliding_direction: Literal['left', 'right'] | None = None

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        if self.jump:
            self.jump = False
            self.change_y = 500
            self.in_air = True

        if self.slam:
            self.change_y = -1000
            self.change_x = 0

        if self.in_air:
            self.change_y -= 10
            if self.center_y < self.y:
                self.change_y = 0
                self.in_air = False
                self.slam = False
                self.center_y = self.y

        self.change_x = 0
        if self.sliding:
            self.change_x = self.speed if self.sliding_direction == 'right' else -self.speed
            self.change_x *= 5
        elif self.moving_left and self.moving_right:
            ...
        elif self.moving_left and not self.slam:
            self.change_x = -self.speed
        elif self.moving_right and not self.slam:
            self.change_x = self.speed



        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

class Game(arcade.Window):
    def __init__(self, speed):
        super().__init__(800, 600, 'free Ultrakill clone')
        self.v1: V1 = V1(self.center_x, self.center_y)
        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.player_list.append(self.v1)

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time: float) -> bool | None:
        self.player_list.update()

    def on_key_press(self, symbol, modifiers):
        print('key pressed')
        if symbol == arcade.key.SPACE:
            self.v1.jump = True if self.v1.in_air is False else False
        if symbol == arcade.key.D:
            self.v1.moving_right = True
        if symbol == arcade.key.A:
            self.v1.moving_left = True
        if symbol == arcade.key.LCTRL:
            if self.v1.in_air:
                self.v1.slam = True
            else:
                self.v1.sliding = True

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.D:
            self.v1.moving_right = False
            if not self.v1.sliding:
                self.v1.sliding_direction = 'right'
        if symbol == arcade.key.A:
            self.v1.moving_left = False
            if not self.v1.sliding:
                self.v1.sliding_direction = 'left'
        if symbol == arcade.key.LCTRL:
            if self.v1.sliding:
                self.v1.sliding = False

def main():
    game = Game(200)
    arcade.run()

if __name__ == '__main__':
    main()