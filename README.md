# graph-based-service-placement

A very simple form of the service placement heuristic is shared here. First all paths are identified between a given node (video service instance in the paper) to the end node (control node in the paper). Once all paths are identified between two nodes, both node capacity (resource capacity of the node) and the link capacity are checked before placing linear service graph on the infrastructure graph. 

 We first give as input, 1) the selected vehicular cluster which is the strongest detected community, 2) service template: the linear type graph to be placed and 3) the upper (UL) and lower limit (LL) for the number of TIs of each type to be placed. The LL for all the tasks is 1 as we want to make sure at least one TI of each type is placed. The UL for each TI is equal to the number of video sources or Type 1 TIs, ensuring each stream gets one processing TI, in case the available processing capacity at individual nodes is very low. 

Instead of placing TIs on the shortest path, we consider the joint CCP of the path from a source TI (of Type 1) to the CN. We then place TIs along the path with the highest joint CCP. As we intend to place a long chain of TIs along this path, choosing a longer chain increases the possibility of placing most TIs on the path to the CN. The heuristic may also randomly choose the shortest path, in terms of hop count, if the combined CCP of the path is the highest. 

If the upper limit is not reached, all the paths are explored from Type_i to CN of the cluster. All the paths are sorted based on the path weight, which in our case is the total CCP of the path. All the paths are iterated over, and the bandwidth capacity requirement is checked for the path. If the bandwidth requirement is met and the resource capacity requirement for the node is met, then Type_(i+1) is placed on the node v. If there are no more available nodes on the path to the CN, a failed placement is registered. Thus, this approach aims to send the collected data to the CN and tries to place processing TIs in-network when possible. 



