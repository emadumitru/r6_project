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