from datetime import timedelta
from dataclass import Rawdata

def time_test(event: Rawdata):
    if event.duration <= timedelta(minutes=0):
        print('Error in {}, Time end after time start'.format(event.id))
    elif event.purpose == 'BOS' and event.duration != timedelta(minutes=10): 
        print('Error in {}, BOS is not 10 minutes'.format(event.id))
    elif event.purpose == 'AOS' and event.duration != timedelta(minutes=5): 
        print('Error in {}, AOS is not 5 minutes'.format(event.id))     
    elif event.purpose == 'AHS':
        print('Possible error in {}, AHS performed'.format(event.id))
    elif 'JIT' in event.purpose and event.duration < timedelta(minutes=20):
        print('Error in {}, possible JIT less than 20 minutes'.format(event.id))
        

def overlap_test(event: Rawdata):
    pass

def tooLong_test(event: Rawdata):
    if (event.timeEnd - event.timeStart) > timedelta(minutes=50):
        print('Possible error in {}, very long activity'.format(event.id))

def chronoCheckVehicle_test(event: Rawdata):
    pass

def chronoCheckDriver_test(event: Rawdata):
    pass

def WPT_check(event: Rawdata):
    pass

def MPT_check(event: Rawdata):
    pass

def meter_check(event: Rawdata):
    pass

def ipsfBos_check(event: Rawdata):
    pass

def matching_check(event: Rawdata):
    pass

