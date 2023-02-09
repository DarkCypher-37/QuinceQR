import csv
import pickle
from enum import Enum

class ErrorCorrectionLevel(Enum):
    L = 1
    M = 2
    Q = 3
    H = 4

csv_filepath = "notebooks/scripts/error_correction.csv"
pickle_out_filepath = "notebooks/scripts/error_correction_table.pickle"

data = {}
with open(csv_filepath, 'r') as file:
    reader = csv.reader(file, delimiter=";")
    header = next(reader)  # skip the header row
    for row in reader:
        key = row[0]
        version_str, ec_level_name = key.split('-')
        version_num = int(version_str)
        ec_level_attribute = getattr(ErrorCorrectionLevel, ec_level_name)
        # print(f"{version_num=}, {ec_level_attribute=}")
        key = (version_num, ec_level_attribute)
        values = tuple(int(0 if element == '' else element) for element in row[1:])
        data[key] = values

with open(pickle_out_filepath, 'wb') as file:
    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

assert data[(40, ErrorCorrectionLevel.H)] == (1276, 30, 20, 15, 61, 16)