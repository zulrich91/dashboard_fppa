import pandas as pd
import pymongo
from pymongo import MongoClient
import unidecode

def unidecodePlayersName(name):
    players_name = unidecode.unidecode(name)
    return players_name

client = MongoClient("mongodb://20.74.102.112:27017/joueur_saison")
db = client['joueur_saison']
# collection_attaques = db['attaques']
# collection_defense = db['defenses']

db_stats = client["Stats"]


# table_attaque = pd.DataFrame(list(collection_attaques.find()))
# table_defense = pd.DataFrame(list(collection_defense.find()))
stats_df = pd.DataFrame(db_stats['joueurs'].find({}))

# table_attaque.to_csv("../data/attaque.csv", index=False)
# table_defense.to_csv('../data/defense.csv', index=False)
stats_df.to_csv("../data/stats.csv", index=False,mode='w+')
print(stats_df.head())