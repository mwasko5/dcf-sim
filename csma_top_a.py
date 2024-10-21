import random

# simulation parameters (in slots)
DIFS = 4
SIFS = 2
ACK = 3
cont_window_0 = 8
cont_window_max = 1024

def get_total_slot_count():
    sim_time = 10 # seconds
    slot_time = 10**-5 # seconds
    return round(sim_time / slot_time)

def get_frame_slot_count():
    bandwidth = 12000000 # bps
    frame_size = 1500 # bytes
    slot_time = 10**-5 # seconds
    frame_time = frame_size * 8 / bandwidth
    return round(frame_time / slot_time)

def generate_backoff(cont_window):
    return random.randrange(cont_window - 1)

def success_transmit(traffic, curr_slot, time, success):
    frame_slot_count = get_frame_slot_count()
    curr_slot = time + frame_slot_count + SIFS + ACK
    traffic.pop(0)
    success += 1
    return curr_slot, success

def collision_transmit(curr_slot, time, collision):
    frame_slot_count = get_frame_slot_count()
    curr_slot = time + frame_slot_count + SIFS + ACK
    collision += 1
    return curr_slot, collision

def csma_topology_a(trafficA, trafficB):
    # get total slot count
    total_slot_count = get_total_slot_count()
    #print("total slots:", total_slot_count)

    # initialize current slot to DIFS duration
    curr_slot = 0
    if len(trafficA) != 0 or len(trafficB) != 0:
        if len(trafficA) == 0:
            curr_slot = trafficB[0]
        elif len(trafficB) == 0:
            curr_slot = trafficA[0]
        else:
            curr_slot = min(trafficA[0], trafficB[0])

    # initialize contention window to initial size
    cont_window = cont_window_0

    # initialize collision flag to false
    collision_flag = False

    # initialize backoff counters
    backoffA = -1
    backoffB = -1

    # initialize performance metric variables
    successA = 0
    successB = 0
    collisions = 0

    # run simulation
    while curr_slot <= total_slot_count and (len(trafficA) != 0 or len(trafficB) != 0):
        #print("TOP")
        #print("    initial traffic:", trafficA, trafficB)
        #print("    curr_slot:", curr_slot)
        if len(trafficA) == 0:
            if trafficB[0] < curr_slot:
                trafficB[0] = curr_slot
            #print("    adjusted traffic:", trafficA, trafficB)
            #print("    SUCCESS: transmit B")
            timeB = trafficB[0] + DIFS + generate_backoff(cont_window)
            curr_slot, successB = success_transmit(trafficB, curr_slot, timeB, successB)
            if collision_flag:
                cont_window = cont_window_0
                collision_flag = False
        elif len(trafficB) == 0:
            if trafficA[0] < curr_slot:
                trafficA[0] = curr_slot
            #print("    adjusted traffic:", trafficA, trafficB)
            #print("    SUCCESS: transmit A")
            timeA = trafficA[0] + DIFS + generate_backoff(cont_window)
            curr_slot, successA = success_transmit(trafficA, curr_slot, timeA, successA)
            if collision_flag:
                cont_window = cont_window_0
                collision_flag = False
        else:
            if trafficA[0] < curr_slot:
                trafficA[0] = curr_slot
            if trafficB[0] < curr_slot:
                trafficB[0] = curr_slot
            #print("    adjusted traffic:", trafficA, trafficB)
            if backoffA == -1:
                timeA = trafficA[0] + DIFS + generate_backoff(cont_window)
            else:
                timeA = trafficA[0] + DIFS + backoffA
                backoffA = -1
            if backoffB == -1:
                timeB = trafficB[0] + DIFS + generate_backoff(cont_window)
            else:
                timeB = trafficB[0] + DIFS + backoffB
                backoffB = -1
            #print("   ", timeA, timeB)
            if timeA == timeB:
                #print("    COLLISION")
                curr_slot, collisions = collision_transmit(curr_slot, timeA, collisions)
                if cont_window < cont_window_max:
                    cont_window *= 2
                collision_flag = True
            elif timeA < timeB:
                if timeA >= trafficB[0] + DIFS:
                    backoffB = timeB - timeA
                    #print("    backoffB:", backoffB)
                #print("    SUCCESS: transmit A")
                curr_slot, successA = success_transmit(trafficA, curr_slot, timeA, successA)
                if collision_flag:
                    cont_window = cont_window_0
                    collision_flag = False
            else:
                if timeB >= trafficA[0] + DIFS:
                    backoffA = timeA - timeB
                    #print("    backoffA:", backoffA)
                #print("    SUCCESS: transmit B")
                curr_slot, successB = success_transmit(trafficB, curr_slot, timeB, successB)
                if collision_flag:
                    cont_window = cont_window_0
                    collision_flag = False

    print("END OF TRANSMISSION")
    print("    initial traffic:", trafficA, trafficB)
    print("    curr_slot:", curr_slot)
    print("    successA:", successA)
    print("    successB:", successB)
    print("    collisions:", collisions)

    return curr_slot, successA, successB, collisions