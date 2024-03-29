from datetime import time, timedelta

from dataclass import Rawdata

def bosDone_test(event: Rawdata):
    pass
def pol_test(event: Rawdata):
    if event.purpose == 'POL' and float(event.fuelAmount) == 0:
        print('Error in {}, no fuel topped up at POL'.format(event.id))
def chronoCheckVehicle_test(event: Rawdata, prev):
    if prev is not None and event.timeStart < prev.timeEnd:
            print('Error in {}, vehicle overlap with {}'.format(
                event.id, prev.id))

def chronoCheckDriver_test(event: Rawdata, prev):
    if prev is not None and event.timeStart < prev.timeEnd:
            print('Error in {}, personel overlap with {}'.format(
                event.id, prev.id))

def meter_test(event: Rawdata, prev):
    if prev is not None:
        if hasattr(event, 'mileageStart'):
            if event.mileageStart != prev.mileageEnd:
                print('Error in {}, mileage at start of {} different from end of {}'.format(
                    event.id, event.purpose, prev.id))
            
        else:
            if int(event.mileageEnd)-int(event.dist) != int(prev.mileageEnd):
                print('Error in {}, mileage at start of {} different from end of {}'.format(
                    event.id, event.purpose, prev.id))

def ipsfBos_test(event: Rawdata, BOS: dict[int, bool], counter: dict[int, list[bool]]):
    if event.purpose == 'BOS' and event.timeStart.time() < time(7, 0):
        if BOS[int(event.vehicle)] is False:
            BOS[int(event.vehicle)] = True
        else:
            print('Error in {}, AM IPSF performed twice for {}'.format(
                event.id, event.vehicle))
        counter[int(event.vehicle)] = [True, counter[int(event.vehicle)][1]]
    return BOS, counter

def ipsfAos_test(event: Rawdata, AOS: dict[int, bool], 
                 BOS: dict[int, bool], counter: dict[int, list[bool]]):   
    if event.purpose == 'AOS' and event.timeStart.time() > time(19, 0):
        if BOS[int(event.vehicle)]:
            if not AOS[int(event.vehicle)]:
                AOS[int(event.vehicle)] = True
            else:
                print('Error in {}, PM IPSF performed twice for {}'.format(
                    event.id, event.vehicle))
        else:
            print('Possible error in {}, AOS performed for {} after 7pm when no AM IPSF BOS done'
                  .format(event.id, event.vehicle))
        counter[int(event.vehicle)] = [counter[int(event.vehicle)][0], True]
    return AOS, counter
    
def matching_test(counter: dict[int, list[bool]], day, prev):
    for veh, outstanding in counter.items():
        match outstanding:
            case [True, False]:
                consider = prev[int(veh)]
                if consider.purpose != 'WPT' and consider.driver != 'Prem':
                    print('Error on {}, AOS not performed for {}'.format(
                        day.isoformat(), veh))
            case [False, True]:
                print('Error on {}, BOS not performed for {}'.format(
                    day.isoformat(), veh))
            

def WPT_test(event: Rawdata):
    flag = False
    if 'WPT' in event.purpose:
        out = "Possible error in {}, ".format(event.id)
        if event.duration != timedelta(minutes=20): 
            out += "WPT is not 20 minutes "
            flag = True
        if int(event.stationary) != 20:
            out += "WPT stationary time is not 20 minutes"
            flag = True
        if flag:
            print(out)

def A5_test(event: Rawdata):
    if int(event.vehicle) == 59087:
        print('Error in {}, A5???'.format(event.id))

def time_test(event: Rawdata):
    if event.purpose == 'BOS' and event.duration != timedelta(minutes=10): 
        print('Error in {}, BOS is not 10 minutes'.format(event.id))
    elif event.purpose == 'AOS' and event.duration != timedelta(minutes=5): 
        print('Error in {}, AOS is not 5 minutes'.format(event.id))     
    elif event.purpose == 'AHS':
        print('Possible error in {}, AHS performed'.format(event.id))
    elif 'JIT' in event.purpose and event.duration < timedelta(minutes=20):
        print('Error in {}, possible JIT less than 20 minutes'.format(event.id))

def beforeAfter_test(event: Rawdata):
    if event.duration <= timedelta(minutes=0):
        print('Error in {}, Time end after time start'.format(event.id))

def tooLong_test(event: Rawdata):
    if (event.timeEnd - event.timeStart) > timedelta(minutes=50):
        print('Possible error in {}, very long activity'.format(event.id))

def MPT_test(event: Rawdata):
    if 'MPT' in event.purpose and int(event.dist) < 1 :
        print("Possible error in {}, MPT less than 1km moved".format(event.id))

#0.0166km/s is 59.67 km/hr
def speed_test(event: Rawdata):
    if event.purpose not in ['BOS','AOS','AHS','POL'] and (int(event.dist)/event.duration.total_seconds()) > 0.0166:
        print("Error in {}, average speed more than 60km/hr".format(event.id))

def early_late_test(event: Rawdata):
    if event.timeStart.time() < time(6, 30):
        print("Error in {}, {} conducted before 6.30am".format(event.id, event.purpose))
    if event.timeEnd.time() > time(19, 30):
        print("Error in {}, {} conducted after 7.30pm".format(event.id, event.purpose))

def BOS_done_test(event: Rawdata, counter: dict[int, list[bool]]):
    if hasattr(event, 'destination') and counter[int(event.vehicle)] != [True, False]:
        print("Error in {}, BOS not performed for {}".format(event.id, event.vehicle))