import traffic_generation
import csma_top_a
import csma_vcs_top_a

traffic_generation.generate_traffic()
trafficA, trafficB = [10,150,400,700], [15,250,400,700]
total_slots_top_a, successA_top_a, successB_top_a, collisions_top_a = csma_top_a.csma_topology_a(trafficA, trafficB)
total_slots_vca_top_a, successA_vcs_top_a, successB_vcs_top_a, collisions_vcs_top_a = csma_vcs_top_a.csma_vcs_topology_a(trafficA, trafficB)