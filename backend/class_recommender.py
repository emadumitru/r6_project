import pandas as pd
import pickle
from backend.class_map import Rmap
from backend.support_functions import *

class Recommender:
    def __init__(self):
        self.games = {}
        self.rounds = {}
        self.maps = {}

    def last_id(self, data):
        if data:
            return max(data.keys())
        return 0
    
    def add_game(self, game):
        game_id = self.last_id(self.games) + 1
        game.id = game_id
        self.games[game_id] = game
        for round in game.rounds.values():
            id_round = self.last_id(self.rounds) + 1
            round.id = id_round
            round.game_id = game_id
            self.rounds[id_round] = round
        map_name = game.map_name
        if map_name not in self.maps:
            self.maps[map_name] = Rmap(map_name, [])
        self.maps[game.map_name].update_map(game)

    def load_old_data(self, csv_name='r6_games.csv', directory='data'):
        path = get_relative_path(csv_name, directory, __file__)

        with open(path, 'r', encoding='utf-8') as file:
            next(file)
            for line in file:
                try:
                    input_data = read_old_csv_line(line)
                    clean_input_data = clean_format(input_data)
                    game = create_game_and_rounds(clean_input_data)
                    self.add_game(game)
                except Exception as e:
                    print(f'Error: {e}')
                    print(f'Line: {line}')

    def save_to_csv(self, csv_name='csv_games.csv', directory='data'):
        path = get_relative_path(csv_name, directory, __file__)

        temp_df = pd.DataFrame()
        for game in self.games.values():
            temp_df = pd.concat([temp_df, pd.DataFrame([game.csv_line()])], ignore_index=True)

        # Open the file with newline='' to prevent extra empty lines in the CSV
        with open(path, 'w', encoding='utf-8', newline='') as file:
            temp_df.to_csv(file, index=False)

    def load_from_csv(self, csv_name='csv_games.csv', directory='data'):
        path = get_relative_path(csv_name, directory, __file__)

        self.games, self.rounds, self.maps = load_instances_from_csv(path)

    def save(self, filename='recommender.pkl', directory='data'):
        path = get_relative_path(filename, directory, __file__)

        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filename='recommender.pkl', directory='data'):
        path = get_relative_path(filename, directory, __file__)
        
        with open(path, 'rb') as file:
            return pickle.load(file)
                


if __name__ == '__main__':

    pass

