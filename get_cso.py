
def calculate_cso(outflow_values, ratio):
    cso_flow = 0
    hours = 0
    tot_flow = 0
    max_treatment = 3122*ratio #max cfs allowed to treatment  ALERT: WINGOHOCKING ONLY FOR NOW !!!
    #print max_treatment
    tot = len(outflow_values)
    for i in outflow_values: #out_variables is list within list (though outer list is just one element) (cfs/impervious acres)
        tot_flow += i
        if i > max_treatment:  #ratio method--- 
            cso = i - max_treatment # subtracting treated from total outflow
            cso_flow += cso 
            hours += 1
    tot_volume = tot_flow*900*7.48052 #convert to gallons, 900 seconds in 15 minutes
    cso_volume = cso_flow*900*7.48052 #for seconds in 15 minutes
    #equiv_rat = cso_volume/tot_volume  #equivalency ratio
    treated_volume = tot_volume - cso_volume
    #print tot_volume
    return {"cso_volume":cso_volume, "tot_volume":tot_volume}

def cso_reduction(collectionName, ratio, numSubs, results): 
    # ALERT:  numSubs is never used !!!
    # ALERT:  collectionName is never used !!!
    from process_collection import *
    # generates plot of cso reduction
    cso_list = []
    tot_vol_list = []
    cso_reduction_list = []
    numSims = results["numSims"] 
    for i in range(0,numSims):
        cso = calculate_cso(results["outflow_series"][i],ratio)
        cso_list.append(cso["cso_volume"])
        tot_vol_list.append(cso["tot_volume"])
        #reduction = cso["tot_volume"] - cso["cso_volume"]
        #reduction_list.append(reduction)
    original_cso_volume = cso_list[0]  #cso from run with no lids
    for i in range(0,numSims):       
        cso_reduction = original_cso_volume - cso_list[i]  
        cso_reduction_list.append(cso_reduction)
    #print cso_reduction_list
    return {"csoReduction": cso_reduction_list, "cso": cso_list, "totalVol": tot_vol_list}
