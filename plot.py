import matplotlib.pyplot as plt
import main

# parameters
lambda_values = [100, 200, 300, 500, 700, 1000]

# functions 
def plot_csma_top_a():
    # Throughput A vs lambda
    plt.xlabel('λ (frames/second)')
    plt.ylabel('throughput A (Kbps)')

    throughputs = []
    for i in range(len(lambda_values)):
        throughputs += ([(main.total_successA_dcf[0][i] * 12000 / 1000) / 10]) # the divide by 1000 is to get Kbps

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Throughput A (Kbps) vs. λ using CSMA (topology a)')

    plt.plot(lambda_values, throughputs, 'o-') # plt.plot([x], [y])
    plt.show()


plot_csma_top_a()