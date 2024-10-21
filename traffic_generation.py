from numpy import random
import math

def generate_traffic(lambda_value):
    # -------------- parameters --------------
    slot_duration = 0.00001 # 10 microseconds

    # -------------- code --------------
    uniformA = random.uniform(size=lambda_value*10)
    uniformB = random.uniform(size=lambda_value*10)

    station_A_traffic = [0] * len(uniformA)
    station_B_traffic = [0] * len(uniformB)

    for i in range(len(uniformA)):
        station_A_traffic[i] = round(((-1 / lambda_value) * math.log(1 - uniformA[i])) / slot_duration)
        station_A_traffic[i] += station_A_traffic[i - 1]

        station_B_traffic[i] = round(((-1 / lambda_value) * math.log(1 - uniformB[i])) / slot_duration)
        station_B_traffic[i] += station_B_traffic[i - 1]

    #print("A traffic")
    #print(station_A_traffic)

    #print("B traffic")
    #print(station_B_traffic)

    return station_A_traffic, station_B_traffic