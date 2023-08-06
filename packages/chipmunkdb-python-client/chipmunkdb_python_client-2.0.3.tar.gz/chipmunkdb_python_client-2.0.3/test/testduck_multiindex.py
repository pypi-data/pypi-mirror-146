import numpy as np
import pandas as pd

import duckdb
import io

category_idx = pd.Index(['A', 'B'])
date_idx = pd.date_range('2018-01', '2018-02', freq='MS')
idx = pd.MultiIndex.from_product([category_idx, date_idx], names=['category', 'date'])

series = pd.Series(np.random.randn(len(category_idx) * len(date_idx)), index=idx)


df = pd.DataFrame(series)

print(df)
con = duckdb.connect(database='multiindex.duck', read_only=False)

con.register("my_view", df)

con.execute("SELECT * FROM my_view")

print(con.fetchall())