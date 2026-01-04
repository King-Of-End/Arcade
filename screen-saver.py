import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UIFlatButton

from pyglet.graphics import Batch


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
        self.background = arcade.load_texture("background.jpg")

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


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)  # Вертикальный стек

        # Добавим все виджеты в box, потом box в anchor
        self.setup_widgets()  # Функция ниже

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)
        
        self.background = arcade.load_texture("background.jpg")

    def setup_widgets(self):
        change_person_button = UIFlatButton(text="Выбрать персонажа", width=400, height=80, color=arcade.color.BLUE)
        change_person_button.on_click = self.on_button_click
        self.box_layout.add(change_person_button)

        choose_level_button = UIFlatButton(text="Выбрать уровень", width=400, height=80, color=arcade.color.BLUE)
        choose_level_button.on_click = self.on_button_click
        self.box_layout.add(choose_level_button)

    def on_button_click(self, *args):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.Rect(x=self.width // 2, y=self.height // 2,
                                                              width=self.width, height=self.height, bottom=0, left=0,
                                                              right=self.width, top=self.height),
                                 color=arcade.color.WHITE, angle=0.0, blend=True,
                                 alpha=255, pixelated=False, atlas=None)
        self.manager.draw()
        # Рисуем спрайты, сцену...

    def on_update(self, delta_time):
        ...


window = arcade.Window(1000, 800, "")
menu_view = ScreenSaverView()
window.show_view(menu_view)
arcade.run()
