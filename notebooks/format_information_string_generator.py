fpath = r"./notebooks/scripts/format_information_string.csv"

import csv
import pickle
from enum import Enum

mydict = {}

class ErrorCorrectionLevel(Enum):
    L = 1
    M = 2
    Q = 3
    H = 4 

# Open the CSV file
with open(fpath, newline='') as csvfile:

    # Create a CSV reader object
    reader = csv.reader(csvfile)

    # Loop over the rows in the CSV file and print them
    for row in reader:
        ecl, mask_pattern, bits = row
        ecl = ErrorCorrectionLevel.__members__[ecl]
        mask_pattern = int(mask_pattern)
        mydict[(ecl, mask_pattern)] = bits
        print(ecl, mask_pattern)

# with open('resources/format_information_string.pickle', 'wb') as file:
#     pickle.dump(mydict, file)

with open('resources/format_information_string.pickle', 'rb') as file:
    format_information_string = pickle.load(file)

print(format_information_string)