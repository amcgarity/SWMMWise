from borg import *

# AEM 12/1/15 separate the evaluation function into a defined function instead of a lambda function
def efunct(*v):
    o = []
    x = v[0]
    y = v[1]
    obj1 = x**2 + y**2
    obj2 = (x-2)**2 + y**2
    o.append(obj1)
    o.append(obj2)
    return o  # borg wants a list containing the values of the objective functions

borg = Borg(2, 2, 0, efunct,
        bounds=[[-50, 50], [-50, 50]],
        epsilons=[0.01, 0.01])
#result = borg.solve({"maxEvaluations":10000})
#result.display()
solutionNumber = 1
solutionDict = {}
for solution in borg.solve({'maxEvaluations':10000}):
        #solution.display()
        #print solution.getVariables()
        solutionVariableList = solution.getVariables()
        solutionObjectiveList = solution.getObjectives()
        thisSolutionList = [solutionVariableList,solutionObjectiveList]
        solutionDict[solutionNumber] = thisSolutionList
        solutionNumber += 1
print solutionDict