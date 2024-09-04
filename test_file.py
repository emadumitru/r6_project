from backend.class_recommender import Recommender

rec = Recommender()
rec.load_old_data()
rec.save()
print(len(rec.games))

# sides = []
# for game in rec.games.values():
#     for round in game.rounds.values():
#         if round.side not in sides:
#             sides.append(round.side)

# print(sides)




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