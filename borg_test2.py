from borg import *
from pymongo import MongoClient

# AEM 12/1/15 separate the evaluation function into a defined function instead of a lambda function
def efunct(*v):
    global runCount
    runCount += 1
    o = []
    x = v[0]
    y = v[1]
    obj1 = x**2 + y**2
    obj2 = (x-2)**2 + y**2
    o.append(obj1)
    o.append(obj2)
    return o  # borg wants a list containing the values of the objective functions

client = MongoClient()  # On local client
dbName = 'borg_rapid_tests'
dbCollection = 'y16m01d28_testing'
db = client[dbName]
runsCollection = db[dbCollection]
runCount = 0
borg = Borg(2, 2, 0, efunct,
        bounds=[[-50, 50], [-50, 50]],
        epsilons=[0.01, 0.01])
#result = borg.solve({"maxEvaluations":10000})
#result.display()
solutionNumber = 1
solutionDict = {}
result = borg.solve({"maxEvaluations":142})
for solution in result:
    #solution.display()
    #print solution.getVariables()
    solutionVariableList = solution.getVariables()
    solutionObjectiveList = solution.getObjectives()
    thisSolutionList = [solutionVariableList,solutionObjectiveList]
    solutionNumberStr = str(solutionNumber)
    solutionDict[solutionNumberStr] = thisSolutionList
    solutionNumber += 1
doc_id = runsCollection.insert_one(solutionDict).inserted_id
outstr = "Stored Pareto Solution as last record,\nID:%s in mongoDB %s in collection %s\nRUN COMPLETE\n" % (doc_id,dbName,dbCollection)
print outstr
print "runCount = %s" % runCount
#print solutionDict