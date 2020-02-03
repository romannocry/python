import numpy as np

#person that left the firm
#Sex,Age,Job id
datasetS = [[1,33,3],[1,36,4],[1,34,3],[1,35,4],[1,33,2],[0,38,6]]
datasetL = [[1,25,3],[1,23,4],[1,30,3],[1,26,4],[1,22,2],[0,26,2]]
John = [1,24,3]
Sarah = [0,25,2]
def distance(instance1, instance2):
    # just in case, if the instances are lists or tuples:
    instance1 = np.array(instance1) 
    instance2 = np.array(instance2)
    
    return np.linalg.norm(instance1 - instance2)
#print(distance([3, 5], [1, 1]))

#print(distance(John,datasetL[1]))
#print(distance(John,datasetS[1]))

#print(distance(Sarah,datasetL[5]))
#print(distance(Sarah,datasetS[5]))

print(np.array([1,33,3]))