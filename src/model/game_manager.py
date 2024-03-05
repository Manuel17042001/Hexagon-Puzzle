import pickle

from model.game import Game


class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    _game = None

    def __init__(self):
        pass

    def get_game(self):
        return self._game

    def create_new_game(self, width, height):
        self._game = Game(width, height)

    def save_game(self):
        with open("game.pickle", "wb") as f:
            pickle.dump(self._game, f)

    def load_game(self):
        with open("game.pickle", "rb") as f:
            self._game = pickle.load(f)
