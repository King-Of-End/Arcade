import arcade


class Bullet(arcade.Sprite):
    def __init__(self, x, y, x_speed, y_speed):
        super().__init__(center_x=x, center_y=y)
        self.change_x = x_speed
        self.change_y = y_speed