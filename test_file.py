from backend.class_recommender import Recommender
from backend.support_functions import *
from backend.algo_randomizer import *


# rec = Recommender()
# rec.load_old_data()
# rec.save()
# print(len(rec.games))

# sides = []
# for game in rec.games.values():
#     for round in game.rounds.values():
#         if round.side not in sides:
#             sides.append(round.side)

# print(sides)

# rec = Recommender()
# rec.load_old_data()
# rec = old_input_clean_data(rec)
# rec.save()
# rec.save_to_csv()

# rec = Recommender().load()
# rec.save_to_csv()


# rec = Recommender()
# rec.load_from_csv()
# rec.save()
# rec.save_to_csv()


rec = Recommender().load()
# attack, defense = get_random_operators(rec, formula_weight=100, op_count=5)
# for ema, mihnea in attack:
#     print(f'Attack - Ema: {ema}, Mihnea: {mihnea}')
# for ema, mihnea in defense:
#     print(f'Defense - Ema: {ema}, Mihnea: {mihnea}')





# len_games = []
# for map in rec.maps.values():
#     len_games.append(len(map.games))

# print(sum(len_games))


# check_values = []

# for game in rec.games.values():
#     for round in game.rounds.values():
#         check_values.append(round.site)

# print(set(check_values))
# for item in set(check_values):
#     print(item, type(item))




# rec = Recommender()
# rec.load_old_data()
# print(len(rec.games))

# print(len(rec.rounds))
# print(rec.maps.keys())

# rec = old_input_clean_data(rec)
# rec = old_input_clean_data(rec)

# print(rec.maps.keys())
# print(rec.maps.values())

# rec.save()