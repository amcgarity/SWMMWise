from swmm_objects import *
from swmm_read_cso_time_series import *
from pymongo import MongoClient
from datetime import datetime
import yaml
from subprocess import call
import sys

def runswmm(runParamList,swmmInitialInpFileStr,runsCollection,perm):
    # NOTE:  perm is passed only to store in database document for this run
    #  all LID run specifications are passed in runParamList

    (section_names,sections) = read_inp(swmmInitialInpFileStr)
    # Create an instance of a swmm_model object using the SWMM inp data:
    model1 = swmm_model('Model1',section_names,sections)
    #print sections['[INFILTRATION]']
    for item in runParamList:
        subcat = item['Subcat']
        lid = item['LID']
        newNumber = item['Number']
        area = model1.getLidArea(subcat,lid)
        ContribImpervArea = item['ContribImpervArea']   # square feet
        contribImpervAreaAcre = ContribImpervArea/43560.0
        #newWidth = item['Width']
        #CapRatioPct = item['CapRatioPct']
        model1.lidChangeNumber(subcat,lid,newNumber)
        model1.lidChangeArea(subcat,lid,area,contribImpervAreaAcre)  # must call to properly set FromImp parameter !!
        ###model1.lidChangeWidth(subCat,lid,newWidth)
        ###model1.lidChangeFromImp(subCat,lid,newFromImp)
    # Write out the model to a new file because SWMM must have a file
    f = open("SWMM_modified.inp",'w')
    swmmInputFileStr=model1.output()
    f.write(swmmInputFileStr)  # write out the swmmInputFileStr for modified problem
    f.close()
    # Run the new model file
    startTime = datetime.now()   # obtain the starting time of the run
    startTimeStr = str(startTime)
    call(["swmm5.exe", "SWMM_modified.inp", "SWMM_modified.rpt"])
    endTime = datetime.now()   # obtain the ending time of the run
    elapsedTime = endTime - startTime
    minAndSec = divmod(elapsedTime.total_seconds(), 60)
    elapsedTimeStr = "%s min, %0.2f sec" % minAndSec
    print elapsedTimeStr

    x = read_report("SWMM_modified.rpt") # to make list for run dictionary 
    if x == "failed":
        return 0
    else:
        run = {"peak": x["peak"], "volume": x["volume"], "runoff": x["runoff"], "evaporation": x["evap"], \
        "infiltration": x["infil"], "precipitation": x["precip"], "lidDict": x["lid_dict"], "outflow_series": x["outflow_series"],\
        "swmmInputFileStr": swmmInputFileStr, "runParamList": runParamList, "swmmStartTime": startTimeStr,"swmmRunTime": elapsedTimeStr, "perm":perm }
        doc_id = runsCollection.insert_one(run).inserted_id
        print "volume = %s" % x['volume']
        return (doc_id)
