class ScreenData(object):
    def __init__(self, window):
        self.__window = window
        self.__screen_index = 0
        self.__background_color = (20, 20, 31)
        self.__hexagon_side_length = window.get_width() / 50

    def get_screen_index(self):
        return self.__screen_index

    def set_screen_index(self, screen_index):
        self.__screen_index = screen_index

    def get_window(self):
        return self.__window

    def get_background_color(self):
        return self.__background_color

    def get_hexagon_side_length(self):
        return self.__hexagon_side_length
