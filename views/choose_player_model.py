import json

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIFlatButton

player_model_number = 0 # это номер модельки игрока, пригодится при анимации игрока по формуле
                        # f"player_{i}_1.png" и другие

class ModelChoose(arcade.View):
    def __init__(self, menu):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        self.menu = menu

        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.manager.add(self.anchor_layout)
        self.background = arcade.load_texture("images/background.jpg")
        self.setup_widgets()

    def setup_widgets(self):
        button_width = 300
        button_height = 60
        left_margin = 150

        to_menu_button = UIFlatButton(
            text="В меню",
            width=button_width,
            height=button_height
        )
        to_menu_button.on_click = self.to_menu
        self.anchor_layout.add(
            to_menu_button,
            anchor_x="left",
            anchor_y="bottom",
            align_x=left_margin,
            align_y=640
        )

        # Кнопка «Легко»
        level1_button = UIFlatButton(
            text="Легко",
            width=button_width,
            height=button_height
        )
        level1_button.on_click = self.model0
        self.anchor_layout.add(
            level1_button,
            anchor_x="left",
            anchor_y="bottom",
            align_x=left_margin,
            align_y=480
        )

        # Кнопка «Нормально»
        level2_button = UIFlatButton(
            text="Нормально",
            width=button_width,
            height=button_height
        )
        level2_button.on_click = self.model1
        self.anchor_layout.add(
            level2_button,
            anchor_x="left",
            anchor_y="bottom",
            align_x=left_margin,
            align_y=320
        )

        # Кнопка «Сложно»
        level3_button = UIFlatButton(
            text="Сложно",
            width=button_width,
            height=button_height
        )
        level3_button.on_click = self.model2
        self.anchor_layout.add(
            level3_button,
            anchor_x="left",
            anchor_y="bottom",
            align_x=left_margin,
            align_y=160
        )

    def to_menu(self, event):
        if self.active:
            self.window.show_view(self.menu)

    def model0(self, event):
        print(0)
        self.config(0)

    def model1(self, event):
        print(1)
        self.config(1)

    def model2(self, event):
        print(2)
        self.config(2)

    def config(self, level):
        if self.active:
            config = json.loads(open("config.json").read())
            config['player_model'] = level
            json.dump(config, open("config.json", "w"))

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.Rect(x=self.width // 2, y=self.height // 2,
                                                              width=self.width, height=self.height, bottom=0, left=0,
                                                              right=self.width, top=self.height),
                                 color=arcade.color.WHITE, angle=0.0, blend=True,
                                 alpha=255, pixelated=False, atlas=None)
        arcade.draw_texture_rect(arcade.load_texture("images/player_0_afk.png"),
                                 arcade.Rect(x=600, y=525,
                                             width=120, height=120, bottom=0, left=0,
                                             right=self.width, top=self.height),
                                 color=arcade.color.WHITE, angle=0.0, blend=True,
                                 alpha=255, pixelated=False, atlas=None)
        arcade.draw_texture_rect(arcade.load_texture("images/player_1_afk.png"),
                                 arcade.Rect(x=600, y=365,
                                             width=120, height=120, bottom=0, left=0,
                                             right=self.width, top=self.height),
                                 color=arcade.color.WHITE, angle=0.0, blend=True,
                                 alpha=255, pixelated=False, atlas=None)
        arcade.draw_texture_rect(arcade.load_texture("images/player_2_afk.png"),
                                 arcade.Rect(x=600, y=205,
                                             width=120, height=120, bottom=0, left=0,
                                             right=self.width, top=self.height),
                                 color=arcade.color.WHITE, angle=0.0, blend=True,
                                 alpha=255, pixelated=False, atlas=None)
        global player_model_number
        if player_model_number == 0:
            arcade.draw_rect_filled(arcade.Rect(x=800, y=525,
                                             width=120, height=120, bottom=0, left=0,
                                             right=self.width, top=self.height), arcade.color.GREEN,)
        if player_model_number == 1:
            arcade.draw_rect_filled(arcade.Rect(x=800, y=365,
                                             width=120, height=120, bottom=0, left=0,
                                             right=self.width, top=self.height), arcade.color.GREEN,)
        if player_model_number == 2:
            arcade.draw_rect_filled(arcade.Rect(x=800, y=205,
                                             width=120, height=120, bottom=0, left=0,
                                             right=self.width, top=self.height), arcade.color.GREEN,)
        self.manager.draw()

    def on_show_view(self) -> None:
        self.active = True
        self.manager.enable()

    def on_hide_view(self) -> None:
        self.active = False
        self.manager.disable()


if __name__ == '__main__':
    window = arcade.Window(1000, 800, "Выбор уровня")
    menu_view = ModelChoose()
    window.show_view(menu_view)
    arcade.run()
