from datetime import timedelta
from dataclass import Rawdata

def time_test(event: Rawdata):
    timings = {'JIT':20, 'BOS':10, 'AHS':5, 'AOS':5}
    type = event.purpose.upper()
    if (event.timeEnd - event.timeStart) < timedelta(minutes=timings[type]): 
        print('Error in {}, {} less than {} minutes'.format(
            event.id, event.purpose, timings[type]))

def overlap_test(event: Rawdata):
    pass

def tooLong_test(event: Rawdata):
    pass

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

