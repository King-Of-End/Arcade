import arcade


class Bullet(arcade.Sprite):
    def __init__(self, x, y, x_speed, y_speed, angle):
        super().__init__(center_x=x, center_y=y, angle=angle)
        print(self.angle)
        self.texture = arcade.load_texture(":resources:images/space_shooter/laserBlue01.png")
        self.change_x = x_speed
        self.change_y = y_speed