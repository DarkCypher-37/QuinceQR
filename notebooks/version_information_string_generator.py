fpath = r"./notebooks/scripts/version_information_string.csv"

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
        version, bits = row
        version = int(version)
        mydict[version] = bits

# with open('resources/version_information_string.pickle', 'wb') as file:
#     pickle.dump(mydict, file)

with open('resources/version_information_string.pickle', 'rb') as file:
    version_information_string = pickle.load(file)

# print(mydict)
print(version_information_string)