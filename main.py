import csv
from dataclass import Rawdata
from tests import *
from datetime import date

#edit these only
servicingFile = "download-13_24_56.csv"
tripsFile = "download-13_24_49.csv"
start = date(2024, 1, 15)
end = date(2024, 1, 19)

data = []

#read out the servicing file
with open(servicingFile, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        toAdd = Rawdata()
        toAdd.build_servicing(row)
        data.append(toAdd)

#read out the trips file
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
        
#del old data
data = [x for x in data if start <= x.timeStart.date() <= end]

# sort data
data.sort(key=lambda x: x.timeStart)

#split data into days
days = {}
for event in data:
    days.setdefault(event.timeStart.toordinal(), []).append(event)
days = [days.get(day, []) for day in range(min(days), max(days)+1)]
days = [x for x in days if x is not []]

AROS = [59301,59260,59217,59133,59412,59087,59232,59022,59038]
OUV = [34397,34398,34399]

#daily checks
for day in days:
    morn_BOS = {x:False for x in AROS}
    night_AOS = {x:False for x in AROS}
    counter = {x:[False, False] for x in AROS+OUV}
    for event in day:
        if event.purpose == 'BOS':
            counter[int(event.vehicle)] = [True, counter[int(event.vehicle)][1]]
        elif event.purpose == 'AOS':
            counter[int(event.vehicle)] = [counter[int(event.vehicle)][0], True]
            
        time_test(event)
        tooLong_test(event)
        A5_test(event)
        beforeAfter_test(event)
        WPT_test(event)
        MPT_test(event)
        speed_test(event)
        early_late_test(event)
        # for IPSF veh
        if int(event.vehicle) in AROS:
            morn_BOS, counter = ipsfBos_test(event, morn_BOS, counter)
            night_AOS, counter = ipsfAos_test(event, night_AOS, morn_BOS, counter)
            
    matching_test(counter, day[0].timeStart.date())
        
#    chronoCheckVehicle_test(event)
#    chronoCheckDriver_test(event)
#    meter_test(event)