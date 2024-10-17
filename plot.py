import matplotlib.pyplot as plt

import main

# parameters
lambda_values = [100, 200, 300, 500, 700, 1000]

# functions 
def plot_csma_top_a():
    # Throughput A vs lambda
    plt.xlabel('lambda')
    plt.ylabel('throughput A (bps)')

    throughputs = []
    for i in range(len(lambda_values)):
        throughputs += [(main.total_successA_dcf[0][i] * 12000) / 10]

    plt.plot(lambda_values, throughputs) # plt.plot([x], [y])
    plt.show()


plot_csma_top_a()