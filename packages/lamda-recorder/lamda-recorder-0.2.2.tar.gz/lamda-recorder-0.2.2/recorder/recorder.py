import os
from collections import defaultdict

import numpy as np
import pandas as pd
from prettytable import PrettyTable, from_csv

"""
    For record your machine learning process and export it as a table.
"""


class ItemRecorder:
    """
        For record an item, for example , a column(row) of a table  
    """

    def __init__(self, item_name: str = ""):
        self.item_name = item_name
        self.record_dict = defaultdict(list)

    def record(self, key, val):
        assert isinstance(val, float) or isinstance(val, int), "val should be a number!"
        self.record_dict[key].append(val)

    def __repr__(self):
        res = f"recorder:{self.item_name}\n"
        ret = self.process()
        for key in ret:
            res += f"{key}:{ret[key]}\n"
        return res

    def process(self, process_type: [str, dict] = "mean") -> dict:
        if isinstance(process_type, str):
            # Set default value of process_type when input is only a string.
            s = process_type
            process_type = defaultdict(lambda: s)
        elif isinstance(process_type, dict):
            assert set(process_type.keys()) == set(self.record_dict.keys())
        operator = {"mean": np.mean, "std": np.std, "max": np.max, "min": np.min, "median": np.median}
        result = defaultdict(float)
        for key in self.record_dict:
            result[key] = operator[process_type[key]](self.record_dict[key])
        return result


class defaultdictByKey(dict):
    def __init__(self, factory=None, **kwargs):
        super(defaultdictByKey, self).__init__(**kwargs)
        self._factory = factory

    def __missing__(self, key):
        if self._factory != None:
            self[key] = value = self._factory(key)
            return value
        else:
            raise KeyError(key)


class Recorder:
    """
        Recorder a table 
    """

    def __init__(self, table_name: str = ''):
        self.table_name = table_name
        self.Item_dict = defaultdictByKey(ItemRecorder)
        self.table = PrettyTable()

    def record(self, item_name, key, val):
        self.Item_dict[item_name].record(key, val)

    def __repr__(self):
        return str(self.table)

    def process(self, process_type: [str, dict] = 'mean') -> None:
        result = defaultdict(dict)
        self.table = PrettyTable()
        assert len(self.Item_dict) >= 1, "no data, process nothing!"
        keyset = set()
        for item in self.Item_dict:
            result[item] = self.Item_dict[item].process(process_type)
            keyset = set.union(keyset, set(result[item].keys()))
        for item in self.Item_dict:
            for key in keyset:
                if key not in result[item].keys():
                    result[item][key] = "Null"

        self.table.add_column(self.table_name, list(result[item].keys()))
        for col in result:
            self.table.add_column(col, list(result[col].values()))
        if len(self.Item_dict) >= 5:
            self.store_csv('tmp.csv')
            frame = pd.read_csv('tmp.csv', index_col=self.table_name)
            frame = frame.transpose()
            frame.to_csv('tmp.csv')
            with open('tmp.csv', 'r+') as f:
                self.table = from_csv(f)
            os.remove('tmp.csv')

    def store_csv(self, file_path='recorder.csv') -> None:
        with open(file_path, 'w+') as f:
            s = self.table.get_csv_string()
            f.write(s)


if __name__ == '__main__':
    print("hhh")
