import sys
sys.path.insert(0,'..')
from chipmunkdb.ChipmunkDb import ChipmunkDb
import time



db = ChipmunkDb("localhost", 8091)

start = time.time()
df = db.collection_as_pandas("5f9414e059463e65cadf356c")
print("time", time.time() - start)
print(df)