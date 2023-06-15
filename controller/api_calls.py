# calls to virtual-1
# calls to virtual-bands
# calls to virtual-dmx


"""
Bands calls are to last for ~20 seconds, then go to pattern to match dancefloor and current palette
virtual-1 calls to start straight away
virtual-dmx calls to start straight away

four different configs needed for fx
bands - flash
bands - current song
stick - current song
dmx   - current song

complementary patterns needed for bands and stick in particular

"""

import time

from concurrent.futures import ThreadPoolExecutor

def call_1():
    print("Call 1")
    time.sleep(5)
    print("Call 1 part 2")

def call_2():
    print("Call 2")

# test async call
def api_blocking_call():
    print("Calling 1 and 2...")
    
    executor = ThreadPoolExecutor(max_workers=3)
    executor.submit(call_1)
    executor.submit(call_2)
    
    

