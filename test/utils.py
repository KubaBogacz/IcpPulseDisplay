import polars as pl
import pandas as pd


class Utils:

    @staticmethod
    def read_data(file_path, *data_names):
        lazy_df = pl.scan_csv(file_path).select(data_names)
        df = lazy_df.collect()
        data = {}
        for name in data_names:
            if name in df.columns:
                data[name] = df.get_column(name).to_numpy()
        return data
