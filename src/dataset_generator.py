import os
import sys
import datetime as dt

import polars as pl


class DatasetGenerator:

    def __init__(self):
        date = dt.datetime.now().strftime("%Y-%m-%d")
        self.file_path = f"datasets/{date}.parquet"
        self.dataset = pl.DataFrame()

# Fixtures