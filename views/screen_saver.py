import arcade

from pyglet.graphics import Batch

from .menu import MenuView


class ScreenSaverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.GRAY

        self.batch = Batch()
        self.main_text = arcade.Text(f"Главное Меню игры Buckshot Blitz", self.window.width / 2,
                                     self.window.height / 2 + 200,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.autor_text = arcade.Text("Авторы: Рудаков Никита, Карафизи Марк", self.window.width / 2,
                                     self.window.height / 2 + 50,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы начать!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.background = arcade.load_texture("images/background.jpg")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.Rect(x=self.width // 2, y=self.height // 2,
                                                              width=self.width, height=self.height, bottom=0, left=0,
                                                              right=self.width, top=self.height),
                                 color=arcade.color.WHITE, angle=0.0, blend=True,
                                 alpha=255, pixelated=False, atlas=None)
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = MenuView()  # это должен быть класс основнй игры
            self.window.show_view(game_view)


if __name__ == '__main__':
    window = arcade.Window(1000, 800, "")
    menu_view = ScreenSaverView()
    window.show_view(menu_view)
    arcade.run()
