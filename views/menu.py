import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager

from .choose_level_difficult import LevelChoose
from .choose_player_model import ModelChoose
from .game import Game


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)

        self.player_model_view = ModelChoose(self)
        self.difficulty_view = LevelChoose(self)

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
        change_person_button = UIFlatButton(text="Выбрать персонажа", width=400, height=80, color=arcade.color.BLUE)
        change_person_button.on_click = self.choose_player_model
        self.box_layout.add(change_person_button)

        choose_level_button = UIFlatButton(text="Выбрать уровень", width=400, height=80, color=arcade.color.BLUE)
        choose_level_button.on_click = self.choose_level
        self.box_layout.add(choose_level_button)

        start_game_buuton = UIFlatButton(text='Начать игру', width=400, height=80, color=arcade.color.BLUE)
        start_game_buuton.on_click = self.start_game
        self.box_layout.add(start_game_buuton)

    def choose_player_model(self, *args):
        self.window.show_view(self.player_model_view)

    def start_game(self, *args):
        game = Game()
        self.window.show_view(game)

    def choose_level(self, *args):
        self.window.show_view(self.difficulty_view)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.Rect(x=self.width // 2, y=self.height // 2,
                                                              width=self.width, height=self.height, bottom=0, left=0,
                                                              right=self.width, top=self.height),
                                 color=arcade.color.WHITE, angle=0.0, blend=True,
                                 alpha=255, pixelated=False, atlas=None)
        self.manager.draw()
