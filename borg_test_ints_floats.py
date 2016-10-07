from borg import *
import sys

# AEM 1/26/16 drive swmm with borg
# variables are number of lid in each subcatchmen
# objectives are min(total number of lid) and max(runoff volume reduction)

def swmm(*variables):  # v is a list of variables
    nvars = len(variables)
    #sys.exit()
    numlid = []
    for floatvar in variables:
        numlid.append(floatvar)
        #numlid.append(round(floatvar))
    x = numlid[0]
    y = numlid[1]
    
    obj = []
    obj1 = -(x**2 + y**2)
    obj2 = (x-2)**2 + y**2
    obj.append(obj1)
    obj.append(obj2)
    return obj

print "x y obj1 obj2"
borg = Borg(2, 2, 0, swmm,
        bounds=[[-5, 5], [-5, 5]],
        epsilons=[0.01, 0.01])
result = borg.solve({"maxEvaluations":10000})
result.display()

#for solution in borg.solve({'maxEvaluations':10000}):
#        solution.display()
  
