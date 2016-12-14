# IMPORTANT:  RUN THIS BLOCK FIRST
# ONLY for loop tests for which all subcats have the same number of a single LID:
from pymongo import MongoClient
from process_collection import *
def volume_reduction_and_runoff_volume_vs_lid_number(collectionName,numSubs, db):
    from pymongo import MongoClient
    from datetime import datetime
    import matplotlib.pyplot as plt
    mGal = 133680.5  # 1 Million gallon in cubic feet
    runs = db[collectionName]
    cursor = runs.find() 
    print cursor
    numLists = []
    for n in range(0,numSubs):
        numLists.append([])

    volReductionList = []
    totalSurfaceOutflowList = []
    csoVolList=[]
    noLidRun = cursor[0]
    noLidVolume = noLidRun['volume']
    outflow_series_list = []
    for run in cursor:
        for i in range(0,numSubs):
            runParamsZero = run['runParamList'][i] 
            numInitial = runParamsZero['Number']
            numLists[i].append(numInitial)
        volume = run['volume']
        volReduction = noLidVolume-volume
        volReductionList.append(volReduction)
        outflow_series=run['outflow_series']
        #outflow_series_list.append
        series = run['outflow_series']
        #print series
        outflow_series_list.append(series)
        if run['lidDict'] == None:
            #numList.append(number)
            totalSurfaceOutflowList.append(None)
            continue
        else:
            totalSurfaceOutflow = 0.0
            runParamList = run['runParamList']
            lidDict = run['lidDict']
            for lidUsage in runParamList: #was lidUsage in runParamList 
                lid = lidUsage['LID']
                subcat = lidUsage['Subcat']
                lidNumber = lidUsage['Number']
                lidArea = lidUsage['Area']  # in square feet
                #lidKey = subcat+' '+lid
                #surfaceOutflowInches = lidDict[lidKey]['Surface Outflow']
                #surfaceOutflow = surfaceOutflowInches*lidNumber*lidArea/12.0  # cubic feet
                #totalSurfaceOutflow += surfaceOutflow/mGal  # convert to million Gal/year
            #totalSurfaceOutflowList.append(totalSurfaceOutflow)
    numSims = len(volReductionList)
    return{"numLists": numLists, "outflow_series": outflow_series_list, "volReductionList": volReductionList, \
           "surface_outflow":totalSurfaceOutflowList,"numSims": numSims}