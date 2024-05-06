import pandas as pd
import os
from collections import Counter

def kappa(data:pd.DataFrame):
    for i, row in data.iterrows():
        for annotations in zip(row.iloc[1:]):
            print([type(item) for item in [l for l in annotations]])
            flattened = [annotation["value"] for annotation in [item["result"] for item in [l for l in annotations]]]
            print(flattened[0])
            # tag_counts=Counter(flattened)
            # print(tag_counts)


def complied_data(data:pd.DataFrame):
    for root, dirs, files in os.walk(annotations_folder):
        for i, f in enumerate(files):
            df = pd.read_json(os.path.join(root, f))
            df["data"] = [r["text"] for r in df["data"]]
            if not data["data"].equals(df["data"]):
                data["data"] = df["data"]
            df = df.rename(columns={"annotations": f"annotations_{i}"})
            data = pd.merge(data, df[[f"annotations_{i}", f"data"]], on="data")
    return data


if __name__ == "__main__":
    annotations_folder = "../annotations"
    data = pd.DataFrame(columns=["data"])
    data = complied_data(data)
    kappa(data)
