import sys
sys.path.insert(0,'..')
from chipmunkdb.ChipmunkDb import ChipmunkDb
import time


db = ChipmunkDb("localhost", 8091)

start = time.time()
document = db.collection_as_pandas_additional("dev_602be966a7a840a2e232d6eb", ["dev_602be966a7a840a2e232d6eb_6060b1c1375dcc2a5f90bb08"])

print("doc", document)


print("time", time.time() - start)
