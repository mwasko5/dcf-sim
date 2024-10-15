from numpy import random

# -------------- parameters --------------
lambda_value = 100 # frames/sec
slot_duration = 0.00001 # 10 microseconds

# -------------- code --------------

a_poisson = random.poisson(lam=lambda_value, size=200)/10000
b_poisson = random.poisson(lam=lambda_value, size=200)/10000

a_slots = a_poisson/slot_duration
a_slots = a_slots.astype(int)

b_slots = b_poisson/slot_duration
b_slots = b_slots.astype(int)

# initialize station A and B
station_A = [0] * len(a_slots)
station_B = [0] * len(b_slots)

# station A traffic generation
i = -1
while (station_A[i] < 100000): # 10 second cutoff
    i += 1
    if i > 0:
        station_A[i] = int(station_A[i] + station_A[i-1] + a_slots[i])
    else:
        station_A[i] = int(station_A[i] + a_slots[i])
station_A = [x for x in station_A if x > 0] # 10 second cutoff

print("A traffic")
print(a_slots)
print(station_A)

# station B traffic generation
i = -1
while (station_B[i] < 100000): # 10 second cutoff
    i += 1
    if i > 0:
        station_B[i] = int(station_B[i] + station_B[i-1] + b_slots[i])
    else:
        station_B[i] = int(station_B[i] + b_slots[i])
station_B = [x for x in station_B if x > 0] # 10 second cutoff

print("B traffic")
print(b_slots)
print(station_B)
