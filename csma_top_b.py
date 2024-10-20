import random

# simulation parameters (in slots)
DIFS = 4
SIFS = 2
ACK = 3
cont_window_0 = 8
cont_window_max = 1024

trafficB = [1, 100, 200]
trafficA = [2, 101, 201]

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

def success_transmit(traffic, curr_slot, backoff, success):
    print("backoff", backoff)    
    frame_slot_count = get_frame_slot_count()
    curr_slot += backoff + frame_slot_count + SIFS + ACK + DIFS
    traffic.pop(0)
    success += 1
    return curr_slot, success

def collision_transmit(curr_slot, backoff, collisions):
    frame_slot_count = get_frame_slot_count()
    curr_slot += backoff + frame_slot_count + SIFS + ACK + DIFS
    collisions += 1
    return curr_slot, collisions

def csma_topology_b(trafficA, trafficB):
    # get total slot count
    total_slot_count = get_total_slot_count()
    print(total_slot_count)

    # initialize current slot to DIFS duration
    curr_slot = DIFS

    # NEEDS TO BE UPDATED
    # initialize contention window to initial size
    cont_windowA = cont_window_0
    cont_windowB = cont_window_0

    # initialize collision flag to false
    collision_flag = False

    # initialize backoff counters to 0
    backoffA = 0
    backoffB = 0

    # initialize performance metric variables
    successA = 0
    successB = 0
    collisionsA = 0
    collisionsB = 0

    frame_slot_count = get_frame_slot_count()

    # run simulation
    while curr_slot <= total_slot_count and (len(trafficA) != 0 or len(trafficB) != 0):
        print(trafficA, trafficB)
        print("slot:", curr_slot)
        if len(trafficA) == 0:
            # only B has frames to transmit
            if trafficB[0] > curr_slot:
                curr_slot = trafficB[0] + DIFS
            else:
                if backoffB == 0:
                    backoffB = generate_backoff(cont_windowB)
                print("transmission B", backoffB)
                print("curr slot: ", curr_slot)
                curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                backoffB = 0
        elif len(trafficB) == 0:
            # only A has frames to transmit
            if trafficA[0] > curr_slot:
                curr_slot = trafficA[0] + DIFS
            else:
                if backoffA == 0:
                    backoffA = generate_backoff(cont_windowA)
                print("transmission A", backoffA)
                print("curr slot: ", curr_slot)
                curr_slot, successA = success_transmit(trafficA, curr_slot, backoffA, successA)
                backoffA = 0
        elif len(trafficA) and len(trafficB) != 0:
            if (trafficA[0] + DIFS + backoffA + get_frame_slot_count() + SIFS + ACK) < (trafficB[0] + DIFS + backoffB): # successful A
                print("SUCCESSFUL A TRANSMISSION")
                curr_slot, successA = success_transmit(trafficA, curr_slot, backoffA, successA)
                backoffA = 0
                backoffB = 0
                if collision_flag:
                        collision_flag = False
                        cont_windowA = cont_window_0

                generate_backoff(cont_windowA)
            elif (trafficB[0] + DIFS + backoffB + get_frame_slot_count() + SIFS + ACK) < (trafficA[0] + DIFS + backoffA): # successful B
                print("SUCCESSFUL B TRANSMISSION")
                curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                backoffA = 0
                backoffB = 0
                if collision_flag:
                        collision_flag = False
                        cont_windowB = cont_window_0

                generate_backoff(cont_windowB)
            else: # collision
                if (trafficA[0] < trafficB[0]) and ((trafficA[0] + DIFS + backoffA + get_frame_slot_count() + SIFS + ACK) > (trafficB[0] + DIFS + backoffB)): # A is transmitting, B tries to transmit during the A transmission 
                    curr_slot, collisionsB = collision_transmit(curr_slot, backoffB, collisionsB)
                    collision_flag = True
                    print("COLLISION, A TX, B INTERRUPTION")
                    print("curr slot: ", curr_slot)
                    print("contention window B: ", cont_windowB)
                    if cont_windowB < cont_window_max:
                        cont_windowB *= 2
                    
                    backoffB = generate_backoff(cont_windowB)
                elif (trafficB[0] < trafficA[0]) and ((trafficB[0] + DIFS + backoffB + get_frame_slot_count() + SIFS + ACK) > (trafficA[0] + DIFS + backoffA)): # B is transmitting, A tries to transmit during the B transmission
                    curr_slot, collisionsA = collision_transmit(curr_slot, backoffA, collisionsA)
                    collision_flag = True
                    print("COLLISION, B TX, A INTERRUPTION")
                    print("curr slot: ", curr_slot)
                    print("contention window A: ", cont_windowA)
                    if cont_windowA < cont_window_max:
                        cont_windowA *= 2

                    backoffA = generate_backoff(cont_windowA)
        else:
            # idle channel
            curr_slot = min(trafficA[0], trafficB[0]) + DIFS
    
    total_slots = curr_slot - DIFS
    print(total_slots, successA, successB, collisionsA, collisionsB)

    print("collision A: ", collisionsA)
    print("collision B: ", collisionsB)
    
    return total_slots, successA, successB, collisionsA, collisionsB

csma_topology_b(trafficA, trafficB)