from swmm_objects import *
from swmm_read_cso_time_series import *
from datetime import datetime
import yaml
from subprocess import call
import sys

def runswmm(runParamList,swmmInitialInpList,runsCollection):
    (section_names,sections) = read_inp(swmmInitialInpList)
    # Create an instance of a swmm_model object using the SWMM inp data:
    model1 = swmm_model('Model1',section_names,sections)
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
    # Write out the model to a new file because SWMM must have a properly formatted file
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
    elapsedTimeStr = "Elapsed Time = %s min, %0.2f sec" % minAndSec
    print elapsedTimeStr

    # collect the new results:
    #ratio_list = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009]
    #{"peak":peak,"volume":volume,"cso_list":cso_volume_list,"runoff":runoff,"evap":evaporation,"infil":infiltration, "precip":precipitation,"lid_dict":lid_dict} = read_report("SWMM_modified.rpt", ratio_list)
    x = read_report("SWMM_modified.rpt") # to make list for run dictionary 
    #print x
    run = {"peak": x["peak"], "volume": x["volume"], "runoff": x["runoff"], "evaporation": x["evap"], \
    "infiltration": x["infil"], "precipitation": x["precip"], "lidDict": x["lid_dict"], "outflow_series": x["outflow_series"],\
    "swmmInputFileStr": swmmInputFileStr, "runParamList": runParamList, "swmmStartTime": startTimeStr,"swmmRunTime": elapsedTimeStr}
    doc_id = runsCollection.insert_one(run).inserted_id
##    print "peak = %s, volume = %s, cso_volume = %s, runoff = %s" % (peak,volume,cso_volume,runoff)
##    print "volume = %s" % x['volume']
    return (doc_id)

def zero_lid_runswmm(db,collection,swmmInpFile,lidZeroFile):
    thisRunCollection = db[collection]    # use or create the collection
    infile = open(swmmInpFile,'r')
    swmmInpStr = infile.readlines()
    infile.close()
    f = open(lidZeroFile,'r')   # Read the no LID changable parameters from file
    zeroLidList = yaml.load(f)  # list of dicts, one for each line in [LID_USAGE]
    f.close()
    zeroLidDocId = runswmm(zeroLidList,swmmInpStr,thisRunCollection)  # run SWMM on the no LID model for baseline
    return(zeroLidDocId)

def calculate_cso(imperv_acres, outflow_cfs, wet_weather_treatment_ratio, time_step_min):
    # imperv_acres = watershed impervious acres
    # outflow_cfs = SWMM calculated outflow in cfs from timeseries output
    # wet_weather_treatment_ratio = cfs per impervious acre that can be handled by the sewage treatment plant
    #          so that all flow above imperv_acres * wet_weather_treatment_ratio is CSO flow
    cso_flow = 0.0
    hours = 0
    tot_flow = 0.0
    max_treatment = imperv_acres*wet_weather_treatment_ratio #max cfs allowed to treatment
    #print max_treatment
    tot = len(outflow_cfs)
    for this_flow in outflow_cfs: #out_variables is list within list (though outer list is just one element) (cfs/impervious acres)
        tot_flow += this_flow
        if this_flow > max_treatment:  #ratio method--- 
            this_cso = this_flow - max_treatment # subtracting treated from total outflow
            cso_flow += this_cso 
            hours += 1
    time_step_sec = time_step_min * 60  # convert time step to seconds
    tot_volume = tot_flow*time_step_sec*7.48052 #convert to total gallons
    cso_volume = cso_flow*time_step_sec*7.48052 #convert to total gallons
    return {"cso_volume":cso_volume, "tot_volume":tot_volume}



'''
from mongo_credentials import *
from copy import deepcopy
from mongodb_tools import mongo_doc_id_from_string

import io
def main():
    database = "ewri2017"
    db = mongo_credentials_aws2_AEM(database)
    collection = 'cso_experiments_1'
    thisRunCollection = db[collection]
    zeroLidDocIdString = "583b5f25c10157149703b480"
    zeroLidDocId = mongo_doc_id_from_string(zeroLidDocIdString)
    cursor = thisRunCollection.find_one({'_id':zeroLidDocId})
    zeroLidList = cursor["runParamList"]
#    print yaml.dump(zeroLidList)
#    print zeroLidList[0]['LID']
    swmmInpFileStr = cursor["swmmInputFileStr"]
    buf = io.StringIO(swmmInpFileStr)
    swmmInpList = buf.readlines()

    for numberForAllLid in range(8,10):
        newRunList=deepcopy(zeroLidList)  # copy the zeroLidList into a new list
        for lid in newRunList:
            lid['Number'] = numberForAllLid  # the same number of LIDs will be in every subcatchment
        newRunDocId = runswmm(newRunList,swmmInpList,thisRunCollection)
        cursor = thisRunCollection.find_one({'_id':newRunDocId})
        newVolume = cursor['volume']
        print "Number of Wakefield LID in each selected subcatchment %s" % numberForAllLid
        print "Stored record %s for volume = %s" % (newRunDocId,newVolume)
    print "FINISHED ALL RUNS"

main()
'''