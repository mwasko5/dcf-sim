import traffic_generation
import csma_top_a
import csma_vcs_top_a

lambdas = [100, 200, 300, 500, 700, 1000]

#total_slots_dcf = []
total_successA_dcf = [[], []]
total_successB_dcf = [[], []]
total_collisions_dcf = [[], []]

for l in range(len(lambdas)):
    trafficA, trafficB = traffic_generation.generate_traffic(lambdas[l])
    total_slots_top_a, successA_top_a, successB_top_a, collisions_top_a = csma_top_a.csma_topology_a(trafficA, trafficB)
    total_slots_vca_top_a, successA_vcs_top_a, successB_vcs_top_a, collisions_vcs_top_a = csma_vcs_top_a.csma_vcs_topology_a(trafficA, trafficB)

    total_successA_dcf[0] += [successA_top_a]
    total_successA_dcf[1] += [successA_vcs_top_a]

    total_successB_dcf[0] += [successB_top_a]
    total_successB_dcf[1] += [successB_vcs_top_a]

    total_collisions_dcf[0] += [collisions_top_a]
    total_collisions_dcf[1] += [collisions_vcs_top_a]
