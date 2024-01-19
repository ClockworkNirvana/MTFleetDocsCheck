from datetime import timedelta
from dataclass import Rawdata
    
def chronoCheckVehicle_test(event: Rawdata):
    pass

def chronoCheckDriver_test(event: Rawdata):
    pass

def meter_test(event: Rawdata):
    pass

def ipsfBos_test(event: Rawdata):
    pass

def ipsfAos_test(event: Rawdata):
    pass
    
def matching_test(event: Rawdata):
    pass

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