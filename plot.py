import matplotlib.pyplot as plt

# functions 
def plot_throughput_A(lambda_values, total_successA_dcf):
    # Station A throughput vs rate lambda
    plt.xlabel('Rate λ (frames/sec)')
    plt.ylabel('Throughput (Kbps)')

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Station A Throughput (Kbps) vs. Rate λ (frames/sec)')

    plt.plot(lambda_values, total_successA_dcf[0], 'o-', label="Topology A")
    plt.plot(lambda_values, total_successA_dcf[1], 'o-', label="Topology A w/ VCS")
    #plt.plot(lambda_values, total_successA_dcf[2], 'o-', label="Topology B")
    plt.plot(lambda_values, total_successA_dcf[3], 'o-', label="Topology B w/ VCS")
    plt.legend()
    plt.show()
    #plt.savefig('throughput_A.png')

def plot_throughput_B(lambda_values, total_successB_dcf):
    # Station B throughput vs rate lambda
    plt.xlabel('Rate λ (frames/sec)')
    plt.ylabel('Throughput (Kbps)')

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Station B Throughput (Kbps) vs. Rate λ (frames/sec)')

    plt.plot(lambda_values, total_successB_dcf[0], 'o-', label="Topology A")
    plt.plot(lambda_values, total_successB_dcf[1], 'o-', label="Topology A w/ VCS")
    #plt.plot(lambda_values, total_successB_dcf[2], 'o-', label="Topology B")
    plt.plot(lambda_values, total_successB_dcf[3], 'o-', label="Topology B w/ VCS")
    plt.legend()
    plt.show()
    #plt.savefig('throughput_B.png')

def plot_collision_AP(lambda_values, total_collision_dcf):
    # Collisions at AP vs rate lambda
    plt.xlabel('Rate λ (frames/sec)')
    plt.ylabel('Number of Collisions')

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Collisions vs. Rate λ (frames/sec) For Single Domain')

    plt.plot(lambda_values, total_collision_dcf[0], 'o-', label="Topology A")
    plt.plot(lambda_values, total_collision_dcf[1], 'o-', label="Topology A w/ VCS")
    plt.legend()
    plt.show()
    #plt.savefig('collision_AP.png')

def plot_collision_A_B(lambda_values, total_collisionA_dcf, total_collisionB_dcf):
    # Collisions perceived by A and B vs rate lambda
    plt.xlabel('Rate λ (frames/sec)')
    plt.ylabel('Number of Collisions')

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Collisions vs. Rate λ (frames/sec) For Hidden Domains')

    #plt.plot(lambda_values, total_collisionA_dcf[2], 'o-', label="Station A topology B")
    plt.plot(lambda_values, total_collisionA_dcf[3], 'o-', label="Station A topology B w/ VCS")
    #plt.plot(lambda_values, total_collisionB_dcf[2], 'o-', label="Station B topology B")
    plt.plot(lambda_values, total_collisionB_dcf[3], 'o-', label="Station B topology B w/ VCS")

    plt.legend()
    plt.show()
    #plt.savefig('collision_A_B.png')

def plot_fairness_index(lambda_values, total_successA_dcf, total_successB_dcf, total_collisionA_dcf, total_collisionB_dcf):
    # Fairness index vs rate lambda
    plt.xlabel('Rate λ (frames/sec)')
    plt.ylabel('Fairness Index')

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Fairness Index vs. Rate λ (frames/sec)')

    fairness_dcf = [0, 0, 0, 0]
    for i in range(4):
        fairness_dcf[i] = (total_successA_dcf[0] + total_collisionA_dcf[0]) / (total_successB_dcf[0] + total_collisionB_dcf[0])

    plt.plot(lambda_values, fairness_dcf[0], 'o-', label="Topology A")
    plt.plot(lambda_values, fairness_dcf[1], 'o-', label="Topology A w/ VCS")
    #plt.plot(lambda_values, fairness_dcf[2], 'o-', label="Topology B")
    plt.plot(lambda_values, fairness_dcf[3], 'o-', label="Topology B w/ VCS")

    plt.legend()
    plt.show()
    #plt.savefig('collision_A_B.png')

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