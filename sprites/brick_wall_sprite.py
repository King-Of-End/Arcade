import arcade

ANIMATION_SPEED = 0.3


class BrickWall(arcade.Sprite):
    # Загружаем текстуру один раз на уровне класса
    _texture = None

    def __init__(self, x, y):
        super().__init__()

        # Ленивая загрузка текстуры (первый раз загружаем, потом переиспользуем)
        if BrickWall._texture is None:
            BrickWall._texture = arcade.load_texture("images/brick_wall.png")

        self.texture = BrickWall._texture
        self.center_x = x
        self.center_y = y
        self.scale = 0.07


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.slug_list = arcade.SpriteList()
        self.emitters = []
        self.player_x = 700
        self.player_y = 500

    def setup(self):
        slug1 = BrickWall(100, 100)
        self.slug_list.append(slug1)

        slug2 = BrickWall(300, 200)
        self.slug_list.append(slug2)

    def on_draw(self):
        self.clear()

        for emitter in self.emitters:
            emitter.draw()
        arcade.draw_rect_filled(arcade.Rect(x=self.player_x, y=self.player_y, width=10, height=10, bottom=0, left=0, right=0, top=0), arcade.color.RED)

        self.slug_list.draw()

    def on_update(self, delta_time):
        pass


    def on_key_press(self, key, modifiers):
        # Управление игроком (не червяком!)
        if key == arcade.key.LEFT:
            self.player_x -= 100
        elif key == arcade.key.RIGHT:
            self.player_x += 100
        elif key == arcade.key.UP:
            self.player_y += 100
        elif key == arcade.key.DOWN:
            self.player_y -= 100


def main():
    game = MyGame(1000, 600, "тест червяка")
    game.setup()
    arcade.run()


if __name__ == '__main__':
    main()
