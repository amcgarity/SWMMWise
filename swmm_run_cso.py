from swmm_objects import *
from swmm_read_cso_time_series import *
from pymongo import MongoClient
from datetime import datetime
import yaml
from subprocess import call
import sys

def runswmm(runParamList,swmmInitialInpFileStr,runsCollection,tot_area_treated):

    (section_names,sections) = read_inp(swmmInitialInpFileStr)
    # Create an instance of a swmm_model object using the SWMM inp data:
    model1 = swmm_model('Model1',section_names,sections)
    #print sections['[INFILTRATION]']
    for item in runParamList:
        subCat = item['Subcat']
        lid = item['LID']
        newNumber = item['Number']
        newArea = item['Area']
        newWidth = item['Width']
        CapRatioPct = item['CapRatioPct']
        model1.lidChangeNumber(subCat,lid,newNumber)
        model1.lidChangeArea(subCat,lid,newArea,CapRatioPct)
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

    # collect the new results:
    #ratio_list = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009]
    #{"peak":peak,"volume":volume,"cso_list":cso_volume_list,"runoff":runoff,"evap":evaporation,"infil":infiltration, "precip":precipitation,"lid_dict":lid_dict} = read_report("SWMM_modified.rpt", ratio_list)
    x = read_report("SWMM_modified.rpt") # to make list for run dictionary 
    #print x
    run = {"peak": x["peak"], "volume": x["volume"], "runoff": x["runoff"], "evaporation": x["evap"], \
    "infiltration": x["infil"], "precipitation": x["precip"], "lidDict": x["lid_dict"], "outflow_series": x["outflow_series"],\
    "swmmInputFileStr": swmmInputFileStr, "runParamList": runParamList, "swmmStartTime": startTimeStr,"swmmRunTime": elapsedTimeStr, "totalAreaTreated":tot_area_treated }
    doc_id = runsCollection.insert_one(run).inserted_id
    print "volume = %s" % x['volume']
    return (doc_id)
