from pymongo import MongoClient as mc

client = mc()
db = client.ITjuzi
tobe = db.ToBeCaptured
for i in range(1, 1246):
    tobe.insert_one({"pageid": i, "done": 0})