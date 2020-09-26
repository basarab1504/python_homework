import csv

def get_data(file_path):
    data = [row for row in csv.reader(
        open(file_path, newline='', encoding="utf8"), delimiter=";")]
    del data[0]
    return data