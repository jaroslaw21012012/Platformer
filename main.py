import pickle
#a = list(range(101))
#print(a)
#with open("level.lvl", "wb") as f:
#    pickle.dump(a, f)




with open("game/levels/level.lvl", "rb") as f:
    level = pickle.load(f)
    print(level)