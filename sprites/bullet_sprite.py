from pathlib import Path

import arcade

def get_texture(path):
    try:
        return arcade.load_texture(path)
    except Exception:
        return arcade.texture.get_default_texture()

class Bullet(arcade.Sprite):
    def __init__(self, x, y, x_speed, y_speed, angle):
        super().__init__(center_x=x, center_y=y, angle=angle)
        self.texture = get_texture(":resources:images/space_shooter/laserBlue01.png")
        self.change_x = x_speed
        self.change_y = y_speed