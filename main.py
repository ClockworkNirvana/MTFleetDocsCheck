import csv
from dataclass import Rawdata
from tests import *

servicingFile = "download-13_24_56.csv"
tripsFile = "download-13_24_49.csv"

data = []

with open(servicingFile, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        toAdd = Rawdata()
        toAdd.build_servicing(row)
        data.append(toAdd)

with open(tripsFile, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        #Canceled trip
        if row[6] == "N/A":
            continue
        toAdd = Rawdata()
        toAdd.build_trip(row)
        data.append(toAdd)

for event in data:
    time_test(event)
    tooLong_test(event)
    A5_test(event)
    beforeAfter_test(event)
    WPT_test(event)
    MPT_test(event)
    speed_test(event)