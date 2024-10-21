import traffic_generation
import csma_top_a
import csma_vcs_top_a
import csma_top_b
import csma_vcs_top_b
import plot

lambdas = [100, 200, 300, 500, 700, 1000]

#total_slots_dcf = []
total_successA_dcf = [[], [], [], []]
total_successB_dcf = [[], [], [], []]
total_collisionA_dcf = [[], [], [], []]
total_collisionB_dcf = [[], [], [], []]

for l in range(len(lambdas)):
    trafficA_a, trafficB_a = traffic_generation.generate_traffic(lambdas[l])
    trafficA_vcs_a, trafficB_vcs_a = trafficA_a.copy(), trafficB_a.copy()
    #trafficA_b, trafficB_b = trafficA_a.copy(), trafficB_a.copy()
    trafficA_vcs_b, trafficB_vcs_b = trafficA_a.copy(), trafficB_a.copy()

    total_slots_top_a, successA_top_a, successB_top_a, collisions_top_a = csma_top_a.csma_topology_a(trafficA_a, trafficB_a)

    total_slots_vca_top_a, successA_vcs_top_a, successB_vcs_top_a, collisions_vcs_top_a = csma_vcs_top_a.csma_vcs_topology_a(trafficA_vcs_a, trafficB_vcs_a)

    #total_slots_top_b, successA_top_b, successB_top_b, collisionA_top_b, collisionB_top_b = csma_top_b.csma_topology_b(trafficA_b, trafficB_b)

    total_slots_vca_top_b, successA_vcs_top_b, successB_vcs_top_b, collisionA_vcs_top_b, collisionB_vcs_top_b = csma_vcs_top_b.csma_vcs_topology_b(trafficA_vcs_b, trafficB_vcs_b)

    total_successA_dcf[0] += [successA_top_a]
    total_successA_dcf[1] += [successA_vcs_top_a]
    #total_successA_dcf[2] += [successA_top_b]
    total_successA_dcf[3] += [successA_vcs_top_b]

    total_successB_dcf[0] += [successB_top_a]
    total_successB_dcf[1] += [successB_vcs_top_a]
    #total_successB_dcf[2] += [successB_top_b]
    total_successB_dcf[3] += [successB_vcs_top_b]

    total_collisionA_dcf[0] += [collisions_top_a]
    total_collisionA_dcf[1] += [collisions_vcs_top_a]
    #total_collisionA_dcf[2] += [collisionA_top_b]
    total_collisionA_dcf[3] += [collisionA_vcs_top_b]

    total_collisionB_dcf[0] += [collisions_top_a]
    total_collisionB_dcf[1] += [collisions_vcs_top_a]
    #total_collisionB_dcf[2] += [collisionB_top_b]
    total_collisionB_dcf[3] += [collisionB_vcs_top_b]

plot.plot_throughput_A(lambdas, total_successA_dcf)