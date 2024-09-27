import pandas as pd
import pickle
from backend.class_map import Rmap
from backend.support_functions import *

class Recommender:
    def __init__(self):
        self.maps = {}
        self.game_ids = {}
        self.round_ids = {}

    def last_id(self, data):
        if data:
            return max(data.keys())
        return 0
    
    def add_game(self, game, rounds):
        map_name = game.map_name

        game_id = self.last_id(self.game_ids) + 1
        self.game_ids[game_id] = map_name
        round_ids = []

        game.id = game_id
        for round in rounds:
            round_id = self.last_id(self.round_ids) + 1
            self.round_ids[round_id] = map_name
            round.id = round_id
            round.game_id = game_id
            round_ids.append(round_id)
        
        game.round_ids = round_ids

        if map_name not in self.maps:
            self.maps[map_name] = Rmap(map_name, [])
        self.maps[map_name].update_map(game, rounds)


    def load_old_data(self, csv_name='r6_games.csv', directory='data'):
        path = get_relative_path(csv_name, directory, __file__)
        
        with open(path, 'r', encoding='utf-8') as file:
            next(file)
            for line in file:
                try:
                    input_data = read_old_csv_line(line)
                    clean_input_data = clean_format(input_data)
                    game, rounds = create_game_and_rounds(clean_input_data)
                    self.add_game(game, rounds)
                except Exception as e:
                    print(f'Error: {e}')
                    print(f'Line: {line}')

    def save_to_csv(self, csv_name='csv_games.csv', directory='data'):
        path = get_relative_path(csv_name, directory, __file__)

        temp_df = pd.DataFrame()
        for map in self.maps.values():
            list_dicts = map.to_csv()
            for game_dict in list_dicts:
                temp_df = pd.concat([temp_df, pd.DataFrame([game_dict])], ignore_index=True)

        # Open the file with newline='' to prevent extra empty lines in the CSV
        with open(path, 'w', encoding='utf-8', newline='') as file:
            temp_df.to_csv(file, index=False)

    def load_from_csv(self, csv_name='csv_games.csv', directory='data'):
        path = get_relative_path(csv_name, directory, __file__)

        list_games_and_rounds = load_instances_from_csv(path)
        for game, rounds in list_games_and_rounds:
            self.add_game(game, rounds)

    def save(self, filename='recommender.pkl', directory='data'):
        path = get_relative_path(filename, directory, __file__)

        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filename='recommender.pkl', directory='data'):
        path = get_relative_path(filename, directory, __file__)
        
        with open(path, 'rb') as file:
            return pickle.load(file)
                




