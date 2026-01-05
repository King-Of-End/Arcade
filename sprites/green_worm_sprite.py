import arcade
import random
from arcade.particles import FadeParticle, Emitter, EmitMaintainCount

ANIMATION_SPEED = 0.3

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

class Slug(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # сюда можно запихнуть наши текстуры
        self.textures = []
        texture = arcade.load_texture("images/green_worm1.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/green_worm2.png")
        self.textures.append(texture)

        self.texture = self.textures[0]
        self.center_x = x
        self.center_y = y
        self.scale = 0.6

        self.animation_frame = 0
        self.animation_timer = 0

        self.trail_emitter = make_trail(self, maintain=40)

    def update(self, delta_time, player_x):
        self.animation_timer += delta_time
        if self.animation_timer >= ANIMATION_SPEED:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.textures)
        self.texture = self.textures[self.animation_frame]
        if player_x > self.center_x:
            self.scale_x = -0.6
        else:
            self.scale_x = 0.6
        # self.center_x = random.randint(50, 150) - этой строчкой можно посмотреть что след реально остается за ними

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.slug_list = arcade.SpriteList()
        self.emitters = []

    def setup(self):
        slug1 = Slug(100, 100)
        self.slug_list.append(slug1)

        slug2 = Slug(300, 200)
        self.slug_list.append(slug2)

        self.emitters.append(slug1.trail_emitter)
        self.emitters.append(slug2.trail_emitter)

    def on_draw(self):
        self.clear()

        for emitter in self.emitters:
            emitter.draw()

        self.slug_list.draw()

    def on_update(self, delta_time):
        lst_coords = self.get_coords()
        player_x, player_y = lst_coords[0], lst_coords[1]  # позиция «игрока» для определения направления

        for slug in self.slug_list:
            slug.update(delta_time, player_x)

        for slug in self.slug_list:
            slug.trail_emitter.center_x = slug.center_x
            slug.trail_emitter.center_y = slug.center_y - 35

        emitters_copy = self.emitters.copy()
        for emitter in emitters_copy:
            emitter.update(delta_time)
            if emitter.can_reap():
                self.emitters.remove(emitter)

    def on_key_press(self, key, modifiers):
        # этот кусочек кода позволяет
        # управлять одним из червяков
        # и смотреть за его состоянием

        if len(self.slug_list) > 0:
            slug = self.slug_list[0]
            if key == arcade.key.LEFT:
                slug.center_x -= 5
            elif key == arcade.key.RIGHT:
                slug.center_x += 5
            elif key == arcade.key.UP:
                slug.center_y += 5
            elif key == arcade.key.DOWN:
                slug.center_y -= 5

    def get_coords(self):
        return [200, 200]
        pass
        # тут надо реализовать в основном коде получение координат игрока


def main():
    game = MyGame(1000, 600, "Цветущие лилии")
    game.setup()
    arcade.run()


if __name__ == '__main__':
    main()
