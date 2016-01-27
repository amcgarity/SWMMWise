from __future__ import print_function
from swmm_objects import *
from swmm_read import *
import borg as bg
from pymongo import MongoClient
from subprocess import call
import sys




# AEM 1/26/16 drive swmm with borg
# variables are number of lid in each subcatchmen
# objectives are min(total number of lid) and max(runoff volume reduction)

def swmm(*variables):  # v is a list of variables
    global runsCollection
    global runCount
    swmmInpFile = "borg_swmm_initial.inp"
    infile = open(swmmInpFile,'r')
    swmmInitialInpFileStr = infile.readlines()
    infile.close()
    nvars = len(variables)
    #sys.exit()
    numlid = []
    for floatvar in variables:
        roundedFloat = round(floatvar)
        numlid.append(int(roundedFloat))
    subcatnames = ['S1','S2','S3','S4','S5','S6'] # correspond to numlid list
    ncat = len(subcatnames)
    if ncat != nvars:
        errorStr = "mismatch: %d borg variables but %d subcatchments\n" % (nvars,ncat)
        print(errorStr,file=sys.stderr)
        sys.exit()
       
    (section_names,sections) = read_inp(swmmInitialInpFileStr)
    model1 = swmm_model('Model1',section_names,sections)
    i = 0
    lid = 'wakefield_BR_RG'  # fix for now
    for subcat in subcatnames:
        model1.lidChangeNumber(subcat,lid,numlid[i])
        i += 1
    f = open("SWMM_modified.inp",'w')
    swmmInputFileStr=model1.output()
    f.write(swmmInputFileStr)  # write out the swmmInputFileStr for modified problem
    f.close()
    call(["swmm5","SWMM_modified.inp", "SWMM_modified.txt", "out.out"])
    (peak,volume,lidDict) = read_report("SWMM_modified.txt")
    startingVolume = 15.972  # MGAL/yr from single SWMM run of unmodified problem
    volReduction = startingVolume - volume  # objective 2
    numLidTotal = sum(numlid)   # objective 1 
    run = {"numLidTotal":numLidTotal, "volReduction":volReduction,"peak":peak,"volume":volume,"numlid":numlid,"lidDict":lidDict}
    doc_id = runsCollection.insert_one(run).inserted_id
    runCount += 1
    obj = []
    #obj1 = -(x**2 + y**2)
    #obj2 = (x-2)**2 + y**2
    obj.append(numLidTotal)   # objective 1
    obj.append(volReduction)  # objective 2
    #print "variables:"
    #print variables
    
    outstr = "runCount = " + str(runCount) + '\n'
    outstr += "numlid:\n"
    outstr += str(numlid) + '\n'
    outstr += "numLidTotal = %s, volReduction = %s\n" % (numLidTotal,volReduction)
    outstr += "Stored results in Mogodb doc_id %s\n" % doc_id
    print(outstr, file=sys.stderr)
    sys.exit()
    return obj

client = MongoClient()
dbName = 'borg_swmm'
dbCollection = 'y16m01d27_test1'
db = client[dbName]
runsCollection = db[dbCollection]
runCount = 0
nvars = 6
nobjs = 2
borg = bg.Borg(nvars, nobjs, 0, swmm)
borg.setBounds(*[[0,5]]*nvars)
#borg.setEpsilons(*[0.01]*nobjs) 
epsilon1 = 2  # for total number of LIDs
epsilon2 = 1.0  # for annual volume reduction Mgal/year
borg.setEpsilons(epsilon1,epsilon2) 
result = borg.solve({"maxEvaluations":1000})
for solution in result:
    solution.display()  # keep this for now just in case
    solutionVariableList = solution.getVariables()
    solutionObjectiveList = solution.getObjectives()
    thisSolutionList = [solutionVariableList,solutionObjectiveList]
    solutionDict[solutionNumber] = thisSolutionList
    solutionNumber += 1
print(solutionDict, file=sys.stder)
doc_id = runsCollection.insert_one(solutionDict).inserted_id
outstr = "Stored Pareto Solution as last record, ID:%s in mongoDB %s in collection %s\nRUN COMPLETE" % (doc_id,dbName,dbCollection)
print(outstr, file=sys.stderr)
