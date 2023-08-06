import sys
sys.path.insert(0,'..')
from chipmunkdb.ChipmunkDb import ChipmunkDb
import time


db = ChipmunkDb("localhost", 8091)

start = time.time()
db.save_document("asd", "window", [{"name": "Thoren", "age": 32}])

document = db.get_document("asd", "window")



print("time", time.time() - start)
