import json


def read_from_json(filename: str) -> dict:
    with open(filename, "r") as file_data:
        return json.load(file_data)


def write_to_json(filename: str, data: dict) -> None:
    with open(filename, "w") as file_data:
        json.dump(data, file_data, indent=2)
