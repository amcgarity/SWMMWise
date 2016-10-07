from __future__ import print_function
from swmm_objects import *
from swmm_read import *
from math import log10
import borg as bg
from pymongo import MongoClient
from subprocess import call
import sys
import yaml

# AEM 2/15/16 drive swmm with borg to solve same problem as in 
# Post_EWRI_StormWISE min_cost.mod and winghohocking.dat AMPL solution
# variables are number of greened acres in each subcatchment on each ownership for each GI technology
# converted to number of LIDs of each GI technology to deploy in each subcatchment for SWMM runs
# objectives are min(total cost per AWRI cost model) and max(runoff volume reduction)
# upper bounds on variables calculated as in AMPL

def swmm(*variables):  # v is a list of variables
    global runsCollection
    global runCount
    global captAreaPct_Wakefield
    global captAreaPct_Anna
    global cost
    global I
    global J
    global K
    global g
    
    # MGAL/yr from single SWMM run of unmodified problem:  
    # MUST CHANGE IF INITIAL SWMM INP MODIFIED!!!
    startingVolume = 319.424  
    initialFileRoot = "wingohocking_borg_initial"     # .imp
    modifiedFileRoot = "wingohocking_borg_modified"   # .inp, .txt
    # Calculate the total cost of this solution:
    totalCost = 0.0
    varNum = 0
    varDict = {}
    for i in sorted(I):
        for j in sorted(J):
            for k in sorted(K):
                varDict[(i,j,k)] = variables[varNum]  # load variable values into varDict
                totalCost += cost[(j,k)]*variables[varNum]
                varNum += 1
    
    # compute the number of LIDs of each type to deploy in each subcatchment
    # for now, we are simply combining the private and public LIDs and rounding
    nVars = len(variables)
    #sys.exit()
    numlid = []
    for i in sorted(I):
        for k in sorted(K):
            jSum = 0.0
            for j in sorted(J):
                jSum += varDict[(i,j,k)]
            roundedFloat = round(jSum/g[k])  # calculate the floating point number of LIDs and round
            numlid.append(int(roundedFloat))  # convert to integer and append to numlid list
#    numlid = []
#    for floatvar in variables:
#        roundedFloat = round(floatvar)
#        numlid.append(int(roundedFloat))
    subcatnames = ['S1','S2','S3','S4','S5','S6','S7'] # correspond to numlid list
    ncat = len(subcatnames)
    expected_vars = 2*ncat   #  Expecting 4*ncat variables !!!!!
    if expected_vars != nVars:
        errorStr = "mismatch: %d borg variables but %d expected\n" % (nVars,expected_vars)
        print(errorStr,file=sys.stderr)
        sys.exit()
        
    # Read and parse initial SWMM input file:
    swmmInpFile = initialFileRoot + ".inp"
    infile = open(swmmInpFile,'r')
    swmmInitialInpFileStr = infile.readlines()
    infile.close()   
    (section_names,sections) = read_inp(swmmInitialInpFileStr)
    model1 = swmm_model('Model1',section_names,sections)
    
    i = 0
    lid = 'wakefield_BR_RG'  # fix for now
    for subcat in subcatnames:
        model1.lidChangeNumber(subcat,lid,numlid[i])
        area = model1.lidGetArea(subcat,lid)
        # adjust FromImp for new number by resetting area:
        model1.lidChangeArea(subcat,lid,area,captAreaPct_Wakefield)   
        i += 1
    lid = 'Anna_TT_infil'
    for subcat in subcatnames:
        model1.lidChangeNumber(subcat,lid,numlid[i])
        area = model1.lidGetArea(subcat,lid)
        # adjust FromImp for new number by resetting area:
        model1.lidChangeArea(subcat,lid,area,captAreaPct_Anna)           
        i += 1
    modifiedInpFile = modifiedFileRoot + ".inp"
    modifiedTxtFile = modifiedFileRoot + ".txt"
    f = open(modifiedInpFile,'w')
    swmmInputFileStr=model1.output()
    f.write(swmmInputFileStr)  # write out the swmmInputFileStr for modified problem
    f.close()
    call(["swmm5",modifiedInpFile, modifiedTxtFile, "out.out"])
    (peak,volume,lidDict) = read_report(modifiedTxtFile)
    
    volReduction = startingVolume - volume  # objective 2
    # construct MongoDB record to store for this solution:
    run = {"runCount":runCount,"totalCost":totalCost,"volReduction":volReduction,
           "volume":volume,"lidDict":lidDict,"variables":variables}
    doc_id = runsCollection.insert_one(run).inserted_id
    runCount += 1
    obj = []
    obj.append(totalCost)              # objective 1 (minimize)
    obj.append(-volReduction)          # objective 3 (maximize)
    
    outstr = "runCount = " + str(runCount) + '\n'
    outstr += "totalCost = %s  volReduction = %s\n" % (totalCost,volReduction)
    i=0
    lid = 'wakefield_BR_RG'  # fix for now
    outstr += lid + "number LIDs:\n"
    for subcat in subcatnames:
        outstr += subcat + ' ' + str(numlid[i]) + ', '
        i += 1
    outstr += '\n'
    lid = 'Anna_TT_infil'  # fix for now
    outstr += lid + "number LIDs:\n"
    for subcat in subcatnames:
        outstr += subcat + ' ' + str(numlid[i]) + ', '
        i += 1    
    outstr += '\n'
    outstr += "Stored this run in Mogodb doc_id %s\n" % doc_id
    print(outstr, file=sys.stderr)
    #sys.exit()
    return obj

client = MongoClient()  # On local client
dbName = 'borg_wingo_regress'
dbCollection = 'y16m05d20_100_2'
maxEvaluations = 100
captAreaPct_Wakefield = 5
captAreaPct_Anna = 5
db = client[dbName]
runsCollection = db[dbCollection]
runCount = 0

f = open('wingo_regress.yaml','r')
doc = yaml.load(f)
I = doc['I']
J = doc['J']
K = doc['K']
T = doc['T']
D = doc['D']
convert = doc['convert']
a = doc['a']
b = doc['b']
g = doc['g']
deploy = doc['deploy']
ownfr = doc['ownfr']
area = doc['area']
impfr = doc['impfr']

nI = len(I)
nJ = len(J)
nK = len(K)
nVars = nI*nJ*nK
nT = len(T)
nObjs = nT + 1  # number of benefits plus cost for Borg

# Calculate Upper Bounds on variables: number of greened acres (same as in AMPL)
u = {}
bounds = []
for i in sorted(I):
    for j in sorted(J):
        for k in sorted(K):
            f = ownfr[i][j]*(deploy[k]['pervious']*(1-impfr[i]) + deploy[k]['impervious']*impfr[i])
            upper = f*area[i]
            u[(i,j,k)] = upper
            bounds.append([0,upper])
print(bounds)
# Calculate Cost Coefficients
cost = {}
for j in sorted(J):
    for k in sorted(K):
        costCoeff = 10**(a[j] - b[j]*log10(g[k]))
        cost[(j,k)] = costCoeff
            
borg = bg.Borg(nVars, nObjs, 0, swmm)
borg.setBounds(*bounds)
#borg.setEpsilons(*[0.01]*nObjs) 
epsilon1 = 1  # for total cost (obj 1)
epsilon2 = 0.1  # for annual volume reduction Mgal/year
borg.setEpsilons(epsilon1,epsilon2) 
result = borg.solve({"maxEvaluations":maxEvaluations})
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
