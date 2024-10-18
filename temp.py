import random

# DIFS AND BACKOFF CAN HAPPEN FOR B AFTER DIFS FOR A IF DONE BEFORE TRANSMIT

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
            print("no more transmissions from A")
            break
        elif len(trafficB) == 0:
            print("no more transmissions from B")
            break
        elif min(trafficA[0], trafficB[0]) < curr_slot:
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
                    elif curr_slot + backoffA > trafficB[0] + DIFS + backoffB:
                        # SUCCESS: transmit B, nonzero backoffA
                        print("transmit B, nonzero backoffA")
                        curr_slot = trafficB[0] + DIFS
                        curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                        backoffA -= backoffB
                        backoffB = 0
                    else:
                        # COLLISION: transmit A and B
                        print("collision, zero backoffs")
                        curr_slot, collisions = collision_transmit(curr_slot, backoffA, collisions)
                        backoffA = 0
                        backoffB = 0
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
                    elif curr_slot + backoffB > trafficA[0] + DIFS + backoffA:
                        # SUCCESS: transmit A, nonzero backoffB
                        print("transmit A, nonzero backoffB")
                        curr_slot = trafficA[0] + DIFS
                        curr_slot, successA = success_transmit(trafficA, curr_slot, backoffA, successA)
                        backoffB -= backoffA
                        backoffA = 0
                    else:
                        # COLLISION: transmit A and B
                        print("collision, zero backoffs")
                        curr_slot, collisions = collision_transmit(curr_slot, backoffA, collisions)
                        backoffA = 0
                        backoffB = 0
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
                elif backoffA > backoffB:
                    # SUCCESS: transmit B, nonzero backoffA
                    print("transmit B, nonzero backoffA")
                    curr_slot, successB = success_transmit(trafficB, curr_slot, backoffB, successB)
                    backoffA -= backoffB
                    backoffB = 0
                else:
                    # COLLISION: transmit A and B
                    print("collision, zero backoffs")
                    curr_slot, collisions = collision_transmit(curr_slot, backoffA, collisions)
                    backoffA = 0
                    backoffB = 0
        else:
            # IDLE: neither A nor B are transmitting yet
            curr_slot = min(trafficA[0], trafficB[0]) + DIFS

csma_topology_a([10, 200, 400, 500, 700], [13, 250, 400, 700])