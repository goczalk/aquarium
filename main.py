import time

since_last_update = 0.0
last_update = time.clock()

print last_update

accumulator = 0.0

#30 actualizations per sec
TIME_STEP = 0.03
#max 1FPS
MAX_ACCUMULATED_TIME = 1.0


i = 0
while ( i != 10):
    since_last_update = time.clock() - last_update
    since_last_update = max(0, since_last_update)
    last_update += since_last_update
    accumulator += since_last_update
    accumulator = min(MAX_ACCUMULATED_TIME, accumulator)

    #grab input
    if (i == 2):
        time.sleep(0.5)
    while( accumulator > TIME_STEP):
        #update
        print 'Klaudia'
        accumulator -= TIME_STEP
    #render
    i+=1