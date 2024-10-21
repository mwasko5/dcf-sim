import matplotlib.pyplot as plt
#import main

# parameters
lambda_values = [100, 200, 300, 500, 700, 1000]

# functions 
def plot_throughput_A(lambda_values, total_successA_dcf):
    # Throughput A vs lambda
    plt.xlabel('λ (frames/second)')
    plt.ylabel('Throughput A (Kbps)')

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Throughput A (Kbps) vs. λ using CSMA (topology a)')

    plt.plot(lambda_values, total_successA_dcf[0], 'o-', label="Topology A")
    plt.plot(lambda_values, total_successA_dcf[1], 'o-', label="Topology A w/ VCS")
    #plt.plot(lambda_values, total_successA_dcf[2], 'o-', label="Topology B")
    plt.plot(lambda_values, total_successA_dcf[3], 'o-', label="Topology B w/ VCS")
    plt.legend()
    plt.show()
    #plt.savefig('throughput_A.png')

"""
def plot_csma_top_a():
    # Throughput A vs lambda
    plt.xlabel('λ (frames/second)')
    plt.ylabel('Throughput A (Kbps)')

    throughputs = []
    for i in range(len(lambda_values)):
        throughputs += ([(main.total_successA_dcf[0][i] * 12000 / 1000) / 10]) # the divide by 1000 is to get Kbps
        print(main.total_successA_dcf[0][i])

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Throughput A (Kbps) vs. λ using CSMA (topology a)')

    plt.plot(lambda_values, throughputs, 'o-') # plt.plot([x], [y])
    plt.show()

plot_csma_top_a()
"""