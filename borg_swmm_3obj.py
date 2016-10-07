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
    expected_vars = 2*ncat
    if expected_vars != nvars:
        errorStr = "mismatch: %d borg variables but %d expected\n" % (nvars,expected_vars)
        print(errorStr,file=sys.stderr)
        sys.exit()
       
    (section_names,sections) = read_inp(swmmInitialInpFileStr)
    model1 = swmm_model('Model1',section_names,sections)
    i = 0
    lid = 'wakefield_BR_RG'  # fix for now
    for subcat in subcatnames:
        model1.lidChangeNumber(subcat,lid,numlid[i])
        area = model1.lidGetArea(subcat,lid)
        model1.lidChangeArea(subcat,lid,area)   # adjust FromImp for new number by resetting area
        i += 1
    lid = 'Anna_TT_infil'
    for subcat in subcatnames:
        model1.lidChangeNumber(subcat,lid,numlid[i])
        area = model1.lidGetArea(subcat,lid)
        model1.lidChangeArea(subcat,lid,area)   # adjust FromImp for new number by resetting area
        i += 1
    f = open("SWMM_modified.inp",'w')
    swmmInputFileStr=model1.output()
    f.write(swmmInputFileStr)  # write out the swmmInputFileStr for modified problem
    f.close()
    call(["swmm5","SWMM_modified.inp", "SWMM_modified.txt", "out.out"])
    (peak,volume,lidDict) = read_report("SWMM_modified.txt")
    startingVolume = 15.972  # MGAL/yr from single SWMM run of unmodified problem
    volReduction = startingVolume - volume  # objective 3
    numLidWakefield = numlid[:6]   # the first 6 lid numbers in the list
    numLidAnna = numlid[-6:]       # the last 6 lid numbers in the list
    numLidTotalWakefield = sum(numLidWakefield)   # objective 1 
    numLidTotalAnna = sum(numLidAnna)             # objective 2
    run = {"runCount":runCount,"numLidTotalWakefield":numLidTotalWakefield,"numLidTotalAnna":numLidTotalAnna,
           "volReduction":volReduction,"peak":peak,"volume":volume,"numlid":numlid,"lidDict":lidDict}
    doc_id = runsCollection.insert_one(run).inserted_id
    runCount += 1
    obj = []
    obj.append(numLidTotalWakefield)   # objective 1
    obj.append(numLidTotalAnna)        # objective 2
    obj.append(volReduction)           # objective 3
    
    outstr = "runCount = " + str(runCount) + '\n'
    outstr += "numlid:\n"
    outstr += str(numlid) + '\n'
    outstr += "numLidTotalWakefield = %s,numLidTotalAnna = %s,volReduction = %s\n" % (numLidTotalWakefield,numLidTotalAnna,volReduction)
    outstr += "Stored this run in Mogodb doc_id %s\n" % doc_id
    print(outstr, file=sys.stderr)
    #sys.exit()
    return obj

client = MongoClient()  # On local client
dbName = 'borg_swmm'
dbCollection = 'y16m01d28_2lid_run_Example2'
db = client[dbName]
runsCollection = db[dbCollection]
runCount = 0
nvars = 12
nobjs = 3
borg = bg.Borg(nvars, nobjs, 0, swmm)
borg.setBounds(*[[0,5]]*nvars)
#borg.setEpsilons(*[0.01]*nobjs) 
epsilon1 = 1  # for total number of Wakefield LIDs
epsilon2 = 1  # for total number of Anna LIDs
epsilon3 = 0.1  # for annual volume reduction Mgal/year
borg.setEpsilons(epsilon1,epsilon2,epsilon3) 
result = borg.solve({"maxEvaluations":100})
solutionDict = {}
solutionNumber = 1
for solution in result:
    solution.display()  # keep this for now just in case
    solutionVariableList = solution.getVariables()
    solutionObjectiveList = solution.getObjectives()
    thisSolutionList = [solutionVariableList,solutionObjectiveList]
    solutionNumberStr = str(solutionNumber)
    solutionDict[solutionNumberStr] = thisSolutionList
    solutionNumber += 1
doc_id = runsCollection.insert_one(solutionDict).inserted_id
print(solutionDict, file=sys.stderr)
outstr = "Stored Pareto Solution as last record, ID:%s in mongoDB %s in collection %s\nRUN COMPLETE\n" % (doc_id,dbName,dbCollection)
print(outstr, file=sys.stderr)
