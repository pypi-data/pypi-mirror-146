from pathlib import Path
import pandas as pd

def get_setting_file():
    return Path('tst.txt').absolute()

def generate_file():
    data = {"names": ["go", "map", "filter"]}
    df = pd.DataFrame(data)
    df.to_csv("output" + "/" + "result", index=False)
