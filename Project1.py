import random

# test

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

#def generate_traffic():
    #TO DO
    #trafficA =
    #trafficB =
    #return (trafficA, trafficB)

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

def dcf_topology_a(total_slot_count, frame_slot_count, trafficA, trafficB):
    # initialize current slot to DIFS duration
    curr_slot = DIFS

    # initialize contention window to initial size
    cont_window = cont_window_0

    # initialize collision flag to false
    collision_flag = False

    # initialize backoff counters to 0
    backoffA = 0
    backoffB = 0

    # initialize performance metric variables
    successA = 0
    successB = 0
    collisions = 0

    # run simulation
    while curr_slot <= total_slot_count:
        print(trafficA, trafficB)
        print("slot:", curr_slot)
        backoff = generate_backoff(cont_window)
        if len(trafficA) == 0 and len(trafficB) == 0:
            # no more frames to transmit
            break
        elif len(trafficA) == 0:
            # only B has frames to transmit
            print("transmission B", backoff)
            if trafficB[0] > curr_slot:
                curr_slot = trafficB[0]
            curr_slot, successB = success_transmit(trafficB, curr_slot, backoff, successB)
        elif len(trafficB) == 0:
            # only A has frames to transmit
            print("transmission A", backoff)
            if trafficA[0] > curr_slot:
                curr_slot = trafficA[0]
            curr_slot, successA = success_transmit(trafficA, curr_slot, backoff, successA)
        elif max(trafficA[0], trafficB[0]) <= curr_slot:
            # contending transmissions
            if backoffA == 0:
                backoffA = generate_backoff(cont_window)
            if backoffB == 0:
                backoffB = generate_backoff(cont_window)

            print("contention", backoffA, backoffB)

            if backoffA == backoffB:
                # collision
                print("collision", backoffA, backoffB)
                curr_slot, collisions = collision_transmit(curr_slot, backoffA, collisions)
                backoffA = 0
                backoffB = 0
                if cont_window < cont_window_max:
                    cont_window *= 2
                collision_flag = True
            elif backoffA < backoffB:
                # A successfully transmits
                print("transmission A", backoffA)
                curr_slot, successA = success_transmit(trafficA, curr_slot, backoffA, successA)
                backoffB -= backoffA
                backoffA = 0
                if collision_flag:
                    cont_window = cont_window_0
                    collision_flag = False
            else: 
                # B successfully transmits
                print("transmission B", backoffB)
                curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                backoffA -= backoffB
                backoffB = 0
                if collision_flag:
                    cont_window = cont_window_0
                    collision_flag = False
        elif min(trafficA[0], trafficB[0]) <= curr_slot:
            # one successful transmission
            if trafficA[0] < trafficB[0]:
                # A successfully transmits
                print("transmission A")
                curr_slot, successA = success_transmit(trafficA, curr_slot, backoff, successA)
            else:
                # B successfully transmits
                print("transmission B")
                curr_slot, successB = success_transmit(trafficB, curr_slot, backoff, successB)
        else:
            # idle channel
            curr_slot = min(trafficA[0], trafficB[0])
    
    total_slots = curr_slot - DIFS
    print(total_slots, successA, successB, collisions)

def main():
    total_slot_count = get_total_slot_count()
    print(total_slot_count)
    frame_slot_count = get_frame_slot_count()
    print(frame_slot_count)
    #trafficA, trafficB = generate_traffic()
    trafficA, trafficB = [10,150,400], [15,250,400]
    dcf_topology_a(total_slot_count, frame_slot_count, trafficA, trafficB)

main()
