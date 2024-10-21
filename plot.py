import matplotlib.pyplot as plt

# functions 
def plot_throughput_A(lambda_values, total_successA_dcf):
    # Station A throughput vs rate lambda
    plt.xlabel('Rate λ (frames/sec)')
    plt.ylabel('Throughput (Kbps)')

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Figure 1. Station A Throughput (Kbps) vs. Rate λ (frames/sec)')

    frame_size = 1500 * 8
    sim_time = 10
    throughputA_dcf = [[], [], [], []]
    for i in range(len(throughputA_dcf)):
        throughputA_dcf[i] = [((x * frame_size) / 1000) / sim_time for x in total_successA_dcf[i]]

    plt.plot(lambda_values, throughputA_dcf[0], 'o-', label="Topology A")
    plt.plot(lambda_values, throughputA_dcf[1], 'o-', label="Topology A w/ VCS")
    #plt.plot(lambda_values, throughputA_dcf[2], 'o-', label="Topology B")
    plt.plot(lambda_values, throughputA_dcf[3], 'o-', label="Topology B w/ VCS")
    plt.legend()
    plt.show()
    #plt.savefig('throughput_A.png')

def plot_throughput_B(lambda_values, total_successB_dcf):
    # Station B throughput vs rate lambda
    plt.xlabel('Rate λ (frames/sec)')
    plt.ylabel('Throughput (Kbps)')

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Figure 2. Station B Throughput (Kbps) vs. Rate λ (frames/sec)')

    frame_size = 1500 * 8
    sim_time = 10
    throughputB_dcf = [[], [], [], []]
    for i in range(len(throughputB_dcf)):
        throughputB_dcf[i] = [((x * frame_size) / 1000) / sim_time for x in total_successB_dcf[i]]

    plt.plot(lambda_values, throughputB_dcf[0], 'o-', label="Topology A")
    plt.plot(lambda_values, throughputB_dcf[1], 'o-', label="Topology A w/ VCS")
    #plt.plot(lambda_values, throughputB_dcf[2], 'o-', label="Topology B")
    plt.plot(lambda_values, throughputB_dcf[3], 'o-', label="Topology B w/ VCS")
    plt.legend()
    plt.show()
    #plt.savefig('throughput_B.png')

def plot_collision_AP(lambda_values, total_collision_dcf):
    # Collisions at AP vs rate lambda
    plt.xlabel('Rate λ (frames/sec)')
    plt.ylabel('Number of Collisions N')

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Figure 3. Collisions N vs. Rate λ (frames/sec) For Single Domain')

    plt.plot(lambda_values, total_collision_dcf[0], 'o-', label="Topology A")
    plt.plot(lambda_values, total_collision_dcf[1], 'o-', label="Topology A w/ VCS")
    plt.legend()
    plt.savefig('collision_AP.png')
    plt.show()

def plot_collision_A_B(lambda_values, total_collisionA_dcf, total_collisionB_dcf):
    # Collisions perceived by A and B vs rate lambda
    plt.xlabel('Rate λ (frames/sec)')
    plt.ylabel('Number of Collisions N')

    plt.grid()
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    
    plt.title('Figure 4. Collisions N vs. Rate λ (frames/sec) For Hidden Domains')

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
    
    plt.title('Figure 5. Fairness Index vs. Rate λ (frames/sec)')

    fairness_dcf = [[], [], [], []]
    for i in range(len(fairness_dcf)):
        for j in range(len(total_successA_dcf[i])):
            fairness_dcf[i] += [(total_successA_dcf[i][j] + total_collisionA_dcf[i][j]) / (total_successB_dcf[i][j] + total_collisionB_dcf[i][j])]

    plt.plot(lambda_values, fairness_dcf[0], 'o-', label="Topology A")
    plt.plot(lambda_values, fairness_dcf[1], 'o-', label="Topology A w/ VCS")
    #plt.plot(lambda_values, fairness_dcf[2], 'o-', label="Topology B")
    plt.plot(lambda_values, fairness_dcf[3], 'o-', label="Topology B w/ VCS")

    plt.legend()
    plt.show()
    #plt.savefig('collision_A_B.png')