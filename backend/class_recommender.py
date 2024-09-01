import pandas as pd
import pickle
from support_functions import get_relative_path

class Recommender:
    def __init__(self):
        self.games = {}
        self.rounds = {}
        self.maps = {}
        self.lid_game = self.last_id(self.games)
        self.lid_round = self.last_id(self.rounds)

    def last_id(self, data):
        if data:
            return max(data.keys())
        return 0
    
    def load_old_data(self, csv_name='r6_games.csv', directory='data'):
        path = get_relative_path(csv_name, directory, __file__)

        print(path)
        with open(path, 'r', encoding='utf-8') as file:
            # print first line
            print(file.readline())

            next(file)
            for line in file:
                continue
            ##TODO: transform data and add to class variables

    def save_to_csv(self, csv_name='csv_games.csv', directory='data'):
        path = get_relative_path(csv_name, directory, __file__)

        temp_df = pd.DataFrame()
        for game in self.games.values():
            temp_df = pd.concat([temp_df, pd.DataFrame([game.csv_line])], ignore_index=True)
        with open(path, 'w', encoding='utf-8') as file:
            temp_df.to_csv(file, index=False)

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
    rec = Recommender()
    rec.load_old_data()
