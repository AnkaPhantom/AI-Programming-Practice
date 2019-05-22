from copy import deepcopy
import heapq
import time

with open('input4.txt','r') as f:
    l = f.readline()
    data = l.split(' ')
    LGT = [0 for x in xrange(3)]
    for a in xrange(3):
        LGT[a] = int(data[a])
    plane_num = int(f.readline())
    Plane = [[0 for x in xrange(6)] for y in xrange(plane_num)]
    i = 0
    for i in xrange(plane_num):
        c =  f.readline()
        content = c.split(' ')
        j = 0
        for j in xrange(5):
            Plane[i][j] = int(content[j])
        Plane[i][5] = i

def if_empty(arr):
    for row in xrange(plane_num):
        for col in xrange(5):
            if(arr[row][col]==' '):
                return True
    return False

def sorting(arr):
    n = len(arr)
    for i in xrange(n):
        for j in xrange(0, n-i-1):
            if arr[j][0]+arr[j][1] > arr[j+1][0]+arr[j+1][1]:
                for x in xrange( len(arr[0]) ):
                    arr[j][x], arr[j+1][x] = arr[j+1][x], arr[j][x]

def landing_overlap_safe(plane, schedule, Land, landing_time):
    if len(Land) < LGT[0]:
        return True
    else:
        return False

def gate_overlap_safe(plane, schedule, Gate):
    if len(Gate) < LGT[1]:
        return True
    else:
        return False

def taking_off_overlap_safe(plane, schedule, Takeoff, takingoff_time):
    if len(Takeoff) < LGT[2]:
        return True
    else:
        return False

def plane_schedule(plane, schedule, num, Land, Gate, Takeoff):
    #num += 1
    if( not if_empty(schedule) ):
        return True

    for landing_time in xrange( 0, (plane[num][0] + 1) ):
        if len(Land) == 0 or landing_time >= Land[0]:
            if len(Land) != 0:
                heapq.heappop(Land)
        if len(Gate) == 0 or landing_time+plane[num][1] >= Gate[0]:
            if len(Gate) != 0:
                heapq.heappop(Gate)

        if( landing_overlap_safe(plane, schedule, Land, landing_time) and gate_overlap_safe(plane, schedule, Gate) ):
            heapq.heappush( Land, (landing_time + plane[num][1]) )
            #if num == 0:
            #    heapq.heappush( Gate, 0 )
            #elif num > 0:
            #    heapq.heappush( Gate, 0 )
            schedule[num][0] = landing_time                      # landing time
            schedule[num][1] = schedule[num][0] + plane[num][1]  # arriving gate time

            for leaving_gate_time in xrange( (schedule[num][1] + plane[num][2]), (schedule[num][1] + plane[num][4]+1) ):
                if len(Takeoff) == 0 or leaving_gate_time >= Takeoff[0]:
                    if len(Takeoff) != 0:
                        heapq.heappop(Takeoff)

                if( taking_off_overlap_safe(plane, schedule, Takeoff, leaving_gate_time) ):
                    #heapq.heappop(Gate)
                    heapq.heappush( Gate, leaving_gate_time)
                    heapq.heappush( Takeoff, (leaving_gate_time + plane[num][3]) )
                    schedule[num][2] = leaving_gate_time                 # leaving gate time
                    schedule[num][3] = schedule[num][2] + plane[num][3]  # taking-off time
                    schedule[num][4] = plane[num][5]                     # actual order of plane

                    if( plane_schedule(plane, schedule, num+1, Land, Gate, Takeoff) ):
                        return True

                    schedule[num][0] = ' '
                    schedule[num][1] = ' '
                    schedule[num][2] = ' '
                    schedule[num][3] = ' '
                    schedule[num][4] = ' '
            #return False
    return False

if __name__ == '__main__':

    time_schedule = [[0 for x in xrange(5)] for y in xrange(plane_num)]
    for a in xrange(plane_num):
        for b in xrange(5):
            time_schedule[a][b] = ' '

    Land , Gate, Takeoff = [], [], []
    Plane_landing_order = deepcopy(Plane)
    sorting(Plane_landing_order)
    plane_schedule(Plane_landing_order, time_schedule, 0, Land, Gate, Takeoff)

    print LGT
    print plane_num
    print Plane
    print Plane_landing_order
    print time_schedule
    time_schedule.sort(key=lambda x:x[-1])
    print time_schedule

    c = 0
    f = open("output.txt", "w")
    for c in xrange(plane_num):
        f.write( str(time_schedule[c][0]) )
        f.write(' ')
        f.write( str(time_schedule[c][2]) )
        f.write('\n')