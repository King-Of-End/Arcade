import json

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UIFlatButton


class LevelChoose(arcade.View):
    def __init__(self, menu):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        self.menu = menu
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)  # Вертикальный стек

        # Добавим все виджеты в box, потом box в anchor
        self.setup_widgets()  # Функция ниже

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)

        self.background = arcade.load_texture("images/background.jpg")

    def setup_widgets(self):
        to_menu_button = UIFlatButton(text="В меню", width=400, height=80, color=arcade.color.BLUE)
        to_menu_button.on_click = self.to_menu
        self.box_layout.add(to_menu_button)

        level1_button = UIFlatButton(text="Легко", width=400, height=80, color=arcade.color.BLUE)
        level1_button.on_click = self.level1
        self.box_layout.add(level1_button)

        level2_button = UIFlatButton(text="Нормально", width=400, height=80, color=arcade.color.BLUE)
        level2_button.on_click = self.level2
        self.box_layout.add(level2_button)

        level3_button = UIFlatButton(text="Сложно", width=400, height=80, color=arcade.color.BLUE)
        level3_button.on_click = self.level3
        self.box_layout.add(level3_button)

    def to_menu(self, *args):
        if self.active:
            self.window.show_view(self.menu)

    def level1(self, *args):
        self.config(1)

    def level2(self, *args):
        self.config(2)

    def level3(self, *args):
        self.config(3)

    def config(self, level):
        if self.active:
            config = json.loads(open("config.json").read())
            config['difficulty'] = level
            json.dump(config, open("config.json", "w"))

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.Rect(x=self.width // 2, y=self.height // 2,
                                                              width=self.width, height=self.height, bottom=0, left=0,
                                                              right=self.width, top=self.height),
                                 color=arcade.color.WHITE, angle=0.0, blend=True,
                                 alpha=255, pixelated=False, atlas=None)
        self.manager.draw()
        # Рисуем спрайты, сцену...

    def on_show_view(self) -> None:
        self.active = True
        self.manager.enable()

    def on_hide_view(self) -> None:
        self.active = False
        self.manager.disable()

if __name__ == '__main__':
    window = arcade.Window(1000, 800, "")
    menu_view = LevelChoose()
    window.show_view(menu_view)
    arcade.run()
