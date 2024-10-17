from numpy import random

def generate_traffic(lambda_value):
    # -------------- parameters --------------
    # lambda_value = frames/sec
    slot_duration = 0.00001 # 10 microseconds

    # -------------- code --------------

    a_poisson = random.poisson(lam=lambda_value, size=200)/10000
    b_poisson = random.poisson(lam=lambda_value, size=200)/10000

    a_slots = a_poisson/slot_duration
    a_slots = a_slots.astype(int)

    b_slots = b_poisson/slot_duration
    b_slots = b_slots.astype(int)

    # initialize station A and B
    station_A_traffic = [0] * len(a_slots)
    station_B_traffic = [0] * len(b_slots)

    # station A traffic generation
    i = -1
    while (station_A_traffic[i] < 100000): # 10 second cutoff
        i += 1
        if i > 0:
            station_A_traffic[i] = int(station_A_traffic[i] + station_A_traffic[i-1] + a_slots[i])
        else:
            station_A_traffic[i] = int(station_A_traffic[i] + a_slots[i])
    station_A_traffic = [x for x in station_A_traffic if x > 0] # 10 second cutoff

    print("A traffic")
    print(station_A_traffic)

    # station B traffic generation
    i = -1
    while (station_B_traffic[i] < 100000): # 10 second cutoff
        i += 1
        if i > 0:
            station_B_traffic[i] = int(station_B_traffic[i] + station_B_traffic[i-1] + b_slots[i])
        else:
            station_B_traffic[i] = int(station_B_traffic[i] + b_slots[i])
    station_B_traffic = [x for x in station_B_traffic if x > 0] # 10 second cutoff

    print("B traffic")
    print(station_B_traffic)

    return station_A_traffic, station_B_traffic
