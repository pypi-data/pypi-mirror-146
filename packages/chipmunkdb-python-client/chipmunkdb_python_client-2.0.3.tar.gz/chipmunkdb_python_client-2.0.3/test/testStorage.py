import sys
sys.path.insert(0,'..')
from chipmunkdb.ChipmunkDb import ChipmunkDb
import time
import pandas as pd

import duckdb
import io

db = ChipmunkDb("localhost", 8091)


storages = db.storages()
print("all storages", storages)

entries = [
    {"key": "cmc.rank", "value": 12},
    {"key": "cmc.rank", "value": 12, "tags": ["ETH"]}
]

db.save_keys_to_storage("test_code", entries)

all_data = db.get_storage("test_code")
print("al", all_data)

eth_key = db.filter_storage("test_code", {"key": "cmc.rank", "tags": ["ETH"]})
print("keye", eth_key)

non_eth_key = db.filter_storage("test_code", {"key": "cmc.rank"})
print("keye", non_eth_key)



