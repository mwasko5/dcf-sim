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

def double_collision_transmit(curr_slot, time, collisionA, collisionB):
    frame_slot_count = get_frame_slot_count()
    curr_slot = time + frame_slot_count + SIFS + ACK
    collisionA += 1
    collisionB += 1
    return curr_slot, collisionA, collisionB

def single_collision_transmit(time, collision):
    frame_slot_count = get_frame_slot_count()
    time += frame_slot_count + SIFS + ACK
    collision += 1
    return time, collision

def csma_topology_b(trafficA, trafficB):
    # get total slot count
    total_slot_count = get_total_slot_count()
    #print("total slots:", total_slot_count)

    # get frame slot count
    frame_slot_count = get_frame_slot_count()

    # initialize current slot to DIFS duration
    curr_slot = 0
    if len(trafficA) != 0 or len(trafficB) != 0:
        if len(trafficA) == 0:
            curr_slot = trafficB[0]
        elif len(trafficB) == 0:
            curr_slot = trafficA[0]
        else:
            curr_slot = min(trafficA[0], trafficB[0])

    # initialize contention windows to initial size
    cont_windowA = cont_window_0
    cont_windowB = cont_window_0

    # initialize collision flags to false
    collision_flagA = False
    collision_flagB = False

    # initialize backoff counters
    backoffA = -1
    backoffB = -1

    # initialize performance metric variables
    successA = 0
    successB = 0
    collisionA = 0
    collisionB = 0

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
            timeB = trafficB[0] + DIFS + generate_backoff(cont_windowB)
            curr_slot, successB = success_transmit(trafficB, curr_slot, timeB, successB)
            if collision_flagB:
                cont_windowB = cont_window_0
                collision_flagB = False
        elif len(trafficB) == 0:
            if trafficA[0] < curr_slot:
                trafficA[0] = curr_slot
            #print("    adjusted traffic:", trafficA, trafficB)
            #print("    SUCCESS: transmit A")
            timeA = trafficA[0] + DIFS + generate_backoff(cont_windowA)
            curr_slot, successA = success_transmit(trafficA, curr_slot, timeA, successA)
            if collision_flagA:
                cont_windowA = cont_window_0
                collision_flagA = False
        else:
            if trafficA[0] < curr_slot:
                trafficA[0] = curr_slot
            if trafficB[0] < curr_slot:
                trafficB[0] = curr_slot
            #print("    adjusted traffic:", trafficA, trafficB)
            if backoffA == -1:
                timeA = trafficA[0] + DIFS + generate_backoff(cont_windowA)
            else:
                timeA = trafficA[0] + DIFS + backoffA
                backoffA = -1
            if backoffB == -1:
                timeB = trafficB[0] + DIFS + generate_backoff(cont_windowB)
            else:
                timeB = trafficB[0] + DIFS + backoffB
                backoffB = -1
            #print("   ", timeA, timeB)
            if timeA == timeB:
                #print("    EXACT COLLISION")
                curr_slot, collisionA, collisionB = double_collision_transmit(curr_slot, timeA, collisionA, collisionB)
                if cont_windowA < cont_window_max:
                    cont_windowA *= 2
                if cont_windowB < cont_window_max:
                    cont_windowB *= 2
                collision_flagA = True
                collision_flagB = True
            elif timeA < timeB and timeA + frame_slot_count + SIFS + ACK > timeB:
                #print("    COLLISION: B transmits while A transmits")
                timeA, collisionA = single_collision_transmit(timeA, collisionA)
                trafficA[0] = timeA
                if cont_windowA < cont_window_max:
                    cont_windowA *= 2
                collision_flagA = True
                timeB, collisionB = single_collision_transmit(timeB, collisionB)
                trafficB[0] = timeB
                if cont_windowB < cont_window_max:
                    cont_windowB *= 2
                collision_flagB = True
                curr_slot = timeA
            elif timeA > timeB and timeA < timeB + frame_slot_count + SIFS + ACK:
                #print("    COLLISION: A transmits while B transmits")
                timeB, collisionB = single_collision_transmit(timeB, collisionB)
                trafficB[0] = timeB
                if cont_windowB < cont_window_max:
                    cont_windowB *= 2
                collision_flagB = True              
                timeA, collisionA = single_collision_transmit(timeA, collisionA)
                trafficA[0] = timeA
                if cont_windowA < cont_window_max:
                    cont_windowA *= 2
                collision_flagA = True
                curr_slot = timeB
            elif timeA < timeB:
                #print("    SUCCESS: transmit A")
                if timeA + frame_slot_count + SIFS + ACK >= trafficB[0] + DIFS:
                    backoffB = timeB - (timeA + frame_slot_count + SIFS + ACK)
                curr_slot, successA = success_transmit(trafficA, curr_slot, timeA, successA)
                if collision_flagA:
                    cont_windowA = cont_window_0
                    collision_flagA = False
                if collision_flagB:
                    cont_windowB = cont_window_0
                    collision_flagB = False
            elif timeA > timeB:
                #print("    SUCCESS: transmit B")
                if timeB + frame_slot_count + SIFS + ACK >= trafficA[0] + DIFS:
                    backoffA = timeA - (timeB + frame_slot_count + SIFS + ACK)
                curr_slot, successB = success_transmit(trafficB, curr_slot, timeB, successB)
                if collision_flagA:
                    cont_windowA = cont_window_0
                    collision_flagA = False
                if collision_flagB:
                    cont_windowB = cont_window_0
                    collision_flagB = False

    print("END OF TRANSMISSION")
    print("    initial traffic:", trafficA, trafficB)
    print("    curr_slot:", curr_slot)
    print("    successA:", successA)
    print("    successB:", successB)
    print("    collisionA:", collisionA)
    print("    collisionB:", collisionB)

    return curr_slot, successA, successB, collisionA, collisionB