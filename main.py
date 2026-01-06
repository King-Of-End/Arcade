import arcade

from views import ScreenSaverView

if __name__ == '__main__':
    window = arcade.Window(1000, 800, "")
    menu_view = ScreenSaverView()
    window.show_view(menu_view)
    arcade.run()