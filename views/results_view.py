import arcade
from arcade.gui import UIFlatButton, UIBoxLayout, UIAnchorLayout, UIManager
from pyglet.graphics import Batch


class ResultsView(arcade.View):
    def __init__(self, menu, monsters_killed, time_elapsed):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)

        self.menu_view = menu

        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)  # Вертикальный стек

        # Добавим все виджеты в box, потом box в anchor
        self.setup_widgets()  # Функция ниже

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)

        self.batch = Batch()
        self.monsters_killed_text = arcade.Text(f"Монстров убито: {monsters_killed}", self.window.width / 2,
                                     self.window.height / 2 + 200,
                                     arcade.color.BLACK, font_size=40, anchor_x="center", batch=self.batch)
        self.time_elapsed_text = arcade.Text(f"Времени прошло: {time_elapsed:.1f} секунд", self.window.width / 2,
                                     self.window.height / 2 + 100,
                                     arcade.color.BLACK, font_size=40, anchor_x="center", batch=self.batch)

        self.background = arcade.load_texture("images/background.jpg")

    def setup_widgets(self):
        change_person_button = UIFlatButton(text="В меню", width=400, height=80, color=arcade.color.BLUE)
        change_person_button.on_click = self.menu
        self.box_layout.add(change_person_button)

    def menu(self, *args):
        self.window.show_view(self.menu_view)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.Rect(x=self.width // 2, y=self.height // 2,
                                                              width=self.width, height=self.height, bottom=0, left=0,
                                                              right=self.width, top=self.height),
                                 color=arcade.color.WHITE, angle=0.0, blend=True,
                                 alpha=255, pixelated=False, atlas=None)
        self.manager.draw()
        self.batch.draw()

    def on_show_view(self) -> None:
        self.active = True
        self.manager.enable()

    def on_hide_view(self) -> None:
        self.active = False
        self.manager.disable()