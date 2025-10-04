from fastapi import FastAPI, HTTPException
from csv import DictReader
import os

app = FastAPI()

def read_csv_file_by_id(sharkId: int):
    file_path = f"sharksData/{sharkId}.csv"
    res = []
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File for shark {sharkId} not found")

    with open(file_path, "r") as f:
        data = DictReader(f)
        for row in data:
            row.pop("lc", None)
            row["id"] = int(row["id"])
            row["lon"] = float(row["lon"])
            row["lat"] =float(row["lat"])
            res.append(row)

    return res


def read_all_data():
    res = []
    for sharkId in sorted([int(fileName.split(".")[0]) for fileName in os.listdir("sharksData")]):
        res.append(read_csv_file_by_id(sharkId))
    return res


@app.get("/data/all")
def get_all_data():
    data = read_all_data()
    return data


@app.get("/data/{sharkId}")
def get_shark_by_id(sharkId: int):
    data = read_csv_file_by_id(sharkId)
    return data
