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

def success_transmit(traffic, curr_slot, backoff, success):
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

def csma_topology_a(trafficA, trafficB):
    # get total slot count
    total_slot_count = get_total_slot_count()
    print("total slots:", total_slot_count)

    # initialize current slot to DIFS duration
    curr_slot = 0
    if len(trafficA) != 0 or len(trafficB) != 0:
        if len(trafficA) == 0:
            curr_slot = trafficB[0] + DIFS
        elif len(trafficB) == 0:
            curr_slot = trafficA[0] + DIFS
        else:
            curr_slot = min(trafficA[0], trafficB[0]) + DIFS

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
    while curr_slot <= total_slot_count and (len(trafficA) != 0 or len(trafficB) != 0):
        
        print(trafficA, trafficB)
        print("current slot:", curr_slot)

        if len(trafficA) == 0:
            # only B has frames to transmit
            if trafficB[0] > curr_slot:
                curr_slot = trafficB[0] + DIFS
            else:
                if backoffB == 0:
                    backoffB = generate_backoff(cont_window)
                print("transmission B", backoffB)
                curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                backoffB = 0
                if collision_flag:
                    collision_flag = False
                    cont_window = cont_window_0
        elif len(trafficB) == 0:
            # only A has frames to transmit
            if trafficA[0] > curr_slot:
                curr_slot = trafficA[0] + DIFS
            else:
                if backoffA == 0:
                    backoffA = generate_backoff(cont_window)
                print("transmission A", backoffA)
                curr_slot, successA = success_transmit(trafficA, curr_slot, backoffA, successA)
                backoffA = 0
                if collision_flag:
                    collision_flag = False
                    cont_window = cont_window_0
        elif max(trafficA[0], trafficB[0]) <= curr_slot:
            if backoffA == 0:
                backoffA = generate_backoff(cont_window)
            print("backoffA:", backoffA)
            if backoffB == 0:
                backoffB = generate_backoff(cont_window)
            print("backoffB:", backoffB)
            if backoffA < backoffB:
                # SUCCESS: transmit A, nonzero backoffB
                print("transmit A, nonzero backoffB")
                curr_slot, successA = success_transmit(trafficA, curr_slot, backoffA, successA)
                backoffB -= backoffA
                backoffA = 0
                if collision_flag:
                    collision_flag = False
                    cont_window = cont_window_0
            elif backoffA > backoffB:
                # SUCCESS: transmit B, nonzero backoffA
                print("transmit B, nonzero backoffA")
                curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                backoffA -= backoffB
                backoffB = 0
                if collision_flag:
                    collision_flag = False
                    cont_window = cont_window_0
            else:
                # COLLISION: transmit A and B
                print("collision, zero backoffs")
                curr_slot, collisions = collision_transmit(curr_slot, backoffA, collisions)
                backoffA = 0
                backoffB = 0
                collision_flag = True
                if cont_window < cont_window_max:
                    cont_window *= 2
        elif min(trafficA[0], trafficB[0]) <= curr_slot:
            if trafficA[0] < trafficB[0]:
                if backoffA == 0:
                    backoffA = generate_backoff(cont_window)
                print("backoffA:", backoffA)
                print("comparisonFirst:", curr_slot + backoffA, trafficB[0] + DIFS)
                if curr_slot + backoffA < trafficB[0] + DIFS:
                    # SUCCESS: transmit A
                    print("transmit A, zero backoffs")
                    curr_slot, successA = success_transmit(trafficA, curr_slot, backoffA, successA)
                    backoffA = 0
                    backoffB = 0
                    if collision_flag:
                        collision_flag = False
                        cont_window = cont_window_0
                else:
                    if backoffB == 0:
                        backoffB = generate_backoff(cont_window)
                    print("backoffB:", backoffB)
                    print("comparisonSecond:", curr_slot + backoffA, trafficB[0] + DIFS + backoffB)
                    if curr_slot + backoffA < trafficB[0] + DIFS + backoffB:
                        # SUCCESS: transmit A, nonzero backoffB
                        print("transmit A, nonzero backoffB")
                        curr_slot, successA = success_transmit(trafficA, curr_slot, backoffA, successA)
                        backoffB -= backoffA
                        backoffA = 0
                        if collision_flag:
                            collision_flag = False
                            cont_window = cont_window_0
                    elif curr_slot + backoffA > trafficB[0] + DIFS + backoffB:
                        # SUCCESS: transmit B, nonzero backoffA
                        print("transmit B, nonzero backoffA")
                        curr_slot = trafficB[0] + DIFS
                        curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                        backoffA -= backoffB
                        backoffB = 0
                        if collision_flag:
                            collision_flag = False
                            cont_window = cont_window_0
                    else:
                        # COLLISION: transmit A and B
                        print("collision, zero backoffs")
                        curr_slot, collisions = collision_transmit(curr_slot, backoffA, collisions)
                        backoffA = 0
                        backoffB = 0
                        collision_flag = True
                        if cont_window < cont_window_max:
                            cont_window *= 2
            elif trafficA[0] > trafficB[0]:
                if backoffB == 0:
                    backoffB = generate_backoff(cont_window)
                print("backoffB:", backoffB)
                print("comparisonFirst:", curr_slot + backoffB, trafficA[0] + DIFS)
                if curr_slot + backoffB < trafficA[0] + DIFS:
                    # SUCCESS: transmit B
                    print("transmit B, zero backoffs")
                    curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                    backoffA = 0
                    backoffB = 0
                    if collision_flag:
                        collision_flag = False
                        cont_window = cont_window_0
                else:
                    if backoffA == 0:
                        backoffA = generate_backoff(cont_window)
                    print("backoffA:", backoffA)
                    print("comparisonSecond:", curr_slot + backoffB, trafficA[0] + DIFS + backoffA)
                    if curr_slot + backoffB < trafficA[0] + DIFS + backoffA:
                        # SUCCESS: transmit B, nonzero backoffA
                        print("transmit B, nonzero backoffA")
                        curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                        backoffA -= backoffB
                        backoffB = 0
                        if collision_flag:
                            collision_flag = False
                            cont_window = cont_window_0
                    elif curr_slot + backoffB > trafficA[0] + DIFS + backoffA:
                        # SUCCESS: transmit A, nonzero backoffB
                        print("transmit A, nonzero backoffB")
                        curr_slot = trafficA[0] + DIFS
                        curr_slot, successA = success_transmit(trafficA, curr_slot, backoffA, successA)
                        backoffB -= backoffA
                        backoffA = 0
                        if collision_flag:
                            collision_flag = False
                            cont_window = cont_window_0
                    else:
                        # COLLISION: transmit A and B
                        print("collision, zero backoffs")
                        curr_slot, collisions = collision_transmit(curr_slot, backoffA, collisions)
                        backoffA = 0
                        backoffB = 0
                        collision_flag = True
                        if cont_window < cont_window_max:
                            cont_window *= 2
            else:
                if backoffA == 0:
                    backoffA = generate_backoff(cont_window)
                print("backoffA:", backoffA)
                if backoffB == 0:
                    backoffB = generate_backoff(cont_window)
                print("backoffB:", backoffB)
                if backoffA < backoffB:
                    # SUCCESS: transmit A, nonzero backoffB
                    print("transmit A, nonzero backoffB")
                    curr_slot, successA = success_transmit(trafficA, curr_slot, backoffA, successA)
                    backoffB -= backoffA
                    backoffA = 0
                    if collision_flag:
                        collision_flag = False
                        cont_window = cont_window_0
                elif backoffA > backoffB:
                    # SUCCESS: transmit B, nonzero backoffA
                    print("transmit B, nonzero backoffA")
                    curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                    backoffA -= backoffB
                    backoffB = 0
                    if collision_flag:
                        collision_flag = False
                        cont_window = cont_window_0
                else:
                    # COLLISION: transmit A and B
                    print("collision, zero backoffs")
                    curr_slot, collisions = collision_transmit(curr_slot, backoffA, collisions)
                    backoffA = 0
                    backoffB = 0
                    collision_flag = True
                    if cont_window < cont_window_max:
                        cont_window *= 2
        else:
            # IDLE: neither A nor B are transmitting yet
            curr_slot = min(trafficA[0], trafficB[0]) + DIFS

    total_slots = curr_slot - DIFS
    print(total_slots, successA, successB, collisions)

    return total_slots, successA, successB, collisions