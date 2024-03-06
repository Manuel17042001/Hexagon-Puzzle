import os
import pickle

from model.game import Game
from model.screen_data import ScreenData
from utils import resource_holder


class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    _game = None

    __save_game_file = "game.pickle"

    def get_game(self):
        return self._game

    def create_new_game(self, width, height):
        self._game = Game(width, height)
        resource_holder.update_screen_data(ScreenData(), (width, height))

    def save_game(self):
        with open(self.__save_game_file, "wb") as f:
            pickle.dump(self._game, f)

    def load_game(self):
        with open(self.__save_game_file, "rb") as f:
            self._game = pickle.load(f)
            resource_holder.update_screen_data(ScreenData(), self.get_game().get_map().get_grid_size())

    def exists_saved_game(self) -> bool:
        return os.path.exists(self.__save_game_file)
