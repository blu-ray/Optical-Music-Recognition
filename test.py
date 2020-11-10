import numpy as np
import math
def lineLength(array):
    result = np.array([])
    for line in array:
        length2 = ((line[0] - line[2])*(line[0] - line[2]) + (line[1] - line[3])*(line[1] - line[3]))
        #print(line)
        #print(length2)
        #print("Ssssssss")
        result=np.concatenate((result,[length2]))
        print(result)
    return result
'''
a = np.array([[10,10,20,20] , [20,20,25,25] , [30 ,10 ,10 , 30]] )

predicate = lineLength(a)
print(a)
print(predicate)

order = np.argsort(predicate)
print(order)

a_sorted = a[order]
print(a_sorted)

print(min(1,2,3,4,4,-1))
'''
lines = [[[2856.3813 ,3525.3997 , 2173.5703 , 3563.588  ]],
 [[2742.174   ,2074.2588  ,2690.5112  ,1385.6335 ]],
 [[2866.1555  ,3492.9736,  2781.8582,  2501.8765 ]],
 [[ 436.17734  ,455.669    ,202.85472 ,3384.3535 ]]]
lines = [[[ 316.90076,3522.256  , 969.3812 ,3519.7224 ]],
[[2856.3813 ,3525.3997 ,2173.5703 ,3563.588  ]],
[[2866.1555 ,3492.9736 ,2781.8582 ,2501.8765 ]],
[[ 436.17734, 455.669,202.85472,3384.3535 ]]]
for line in lines:
    l1 = [1,3,3,1]
    l1 = line[0]
    l2 = l1
    if (l1[0] - l1[2] != 0):
        k1 = (l1[1] - l1[3]) / (l1[0] - l1[2])
        b1 = l1[1] - k1 * l1[0]
        theta = math.atan(k1)*180/math.pi
    else:
        k1 = 9999
        b1 = l1[0]
        theta = 90
    print(k1)
    print(b1)
    print(theta)
    print("Ssss")
