import traffic_generation
import csma_top_a

traffic_generation.generate_traffic()
trafficA, trafficB = [10,150,400, 700], [15,250,400, 700]
csma_top_a.csma_topology_a(trafficA, trafficB)