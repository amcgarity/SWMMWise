"""
swmmread.py
Read SWMM input file and create objects for each input category
Also read the resulting output file after SWMM is runcp
2013 Arthur McGarity
Swarthmore College
AEM: Modified 11/2015 to include LID categories in input file
"""
import sys
import numpy as np 
import pandas as pd 

#from swmm_objects import *

def read_inp(swmmInpStr):
# read SWMM inp file fname into a large string
# create a list "section_names" containing the names of the sections found in the file
# create a dictionary "sections" containing the data lines found in each section keyed by section_name
# finally, return "section_names" and "sections"
# NOTE: the calling program is responsible for parsing the data lines in the sections

#    fname = "Example4_bare_PHL.inp"
    data = swmmInpStr
    section_names = []   # we will build this list from section names found in the SWMM .inp file
# remove comment lines and blank lines and identify all section names used in the file
    data1 = []
    for line in data:
        line_ns = line.strip()  # remove whitespace
        if line_ns.startswith('['):
            section_names.append(line_ns)
        elif line_ns.startswith(';;'):  # do not include comment ines
           continue
        elif not line_ns:  # do not include blank lines
           continue
        data1.append(line)  # data1 is a list containing the unstripped lines of the SWMM .inp file 
# now find all data lines in each section, store each data line as an entry in a section_list
# then after reading all the data in a section, store the section_list in
# dictionary sections keyed by the section name
    sections = {}  # dictionary to hold all lines in a section, keyed by section_names
    end = False
    for i in range(len(data1)):
        line = data1[i]
        line_ns = line.strip()  # remove whitespace
        if line_ns in section_names:
            name = line_ns
            section_list = []
            try:
               next_line = data1[i+1]  # look ahead at next line
            except IndexError:
               end = True         # end of input file found
            next_line_ns = next_line.strip()  # remove whitespace
            if (end or (next_line_ns in section_names)):  # we have read the entire section
              sections[name] = section_list              # store the list in the dictionary
        else:
           section_list.append(line)    # store section data in section_list
           try:
               next_line = data1[i+1]  # look ahead at next line
           except IndexError:
               end = True
           next_line_ns = next_line.strip()  # remove whitespace
           if (end or (next_line_ns in section_names)):
              sections[name] = section_list  #populate the sections dictionary
#    for i in section_names:
#        sys.stdout.write("%s\n" % i)
#        for j in sections[i]:
#            sys.stdout.write(j)    
    return((section_names,sections))  # return the section_names LIST and the sections DICTIONARY (keyed by items in the section_names list)

def read_outflow_series(fname):
  infile = open(fname,'r')
  data = infile.readlines()
  node_results = "Node Results"
  found_outfall = False
  hours = []  #empty lists to be appended with data
  outflows = []
  for line in data:
    if node_results in line:    #starting in node results section
      found_outfall = True
    if found_outfall:
      line_list = line.split()
      if len(line_list) > 2:
        time = line_list[0] # get date from list
        if len(time) == 11:  #so that only node results section will be recorded
          hours.append(time)
          out = line_list[2] #get outflow from list
          outflows.append(float(out))
  return (outflows)

def read_runoff(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Runoff Quantity Continuity')
  output_start_index = data.find('Surface ',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
  output_list = output_line.split()
  #print(output_list)
  runoff = output_list[3]
  return float(runoff)

def read_evaporation(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Runoff Quantity Continuity')
  output_start_index = data.find('Evaporation',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
  output_list = output_line.split()
  #print(output_list)
  evaporation = output_list[3]
  return float(evaporation)

def read_infiltration(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Runoff Quantity Continuity')
  output_start_index = data.find('Infiltration',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
  output_list = output_line.split()
  #print(output_list)
  infiltration = output_list[3]
  return float(infiltration)

def read_precipitation(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Runoff Quantity Continuity')
  output_start_index = data.find('Total',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
  output_list = output_line.split()
 # print(output_list)
  precipitation = output_list[3]
  return float(precipitation)

def read_report(fname):
  infile = open(fname,'r')
  data = infile.read()
  # find and parse the External Outflow line
  external_flow_index = data.find('External Outflow')
  if external_flow_index >= 0:  # The External Outflow line is found
    lineList = data[external_flow_index:].split('\n',1)
    wordlist = lineList[0].split()
    volume = float(wordlist[4])
  else:
   volume = None
  # find and parse the LID Performance Summary
  lid_start_index = data.find('LID Performance Summary')
  if lid_start_index >= 0:   # The LID Performance Summary section is in the output file
    lid_subcatchment_heading_index = data.find('Subcatchment',lid_start_index)
    remaining_lines = data[lid_subcatchment_heading_index:].split('\n') 
    #line_after_section = '  '
    i = 2
    lid_performance = []
    while True:
      if remaining_lines[i].strip() == '':   # Blank line found
        break
      lid_performance.append(remaining_lines[i])
      i = i + 1
    lid_dict = {}
    series_dict = {}
    for line in lid_performance:
      this_lid_dict = {}
      labels = ['Total Inflow', 'Evap Loss', 'Infil Loss', 'Surface Outflow', 'Drain Outflow', 
                'Initial Storage', 'Final Storage', 'Continuity Error']
      wordlist = line.split()   
      idx = wordlist[0] + ' ' + wordlist[1]   # string containing subcatchment name and lid name
      values = wordlist[2:]
      i = 0;
      for label in labels:
        this_lid_dict[label] = float(values[i])
        i += 1
      lid_dict[idx] = this_lid_dict  # to be stored in mongo database
      # construct a Pandas dataframe:
      #series_dict[idx] = pd.Series(values, index = labels) 
    #lid_report = pd.DataFrame(series_dict)
  else:
    lid_dict = None
    lid_report = None
  # find and parse the Outfall Loading Summary    
  outfall_start_index = data.find('Outfall Loading Summary')
  output_start_index = data.find('System',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
  output_list = output_line.split()
  peak = float(output_list[3])
  volume = float(output_list[4])
 # peak = None
  runoff = read_runoff(fname)
  evaporation = read_evaporation(fname)
  infiltration = read_infiltration(fname)
  precipitation = read_precipitation(fname)
  outflow_series = read_outflow_series(fname)

  #calculating cso volume
  #cso_volume_list = []
  #for r in  ratio: 
  #outflow_values = []
  #out = read_outflow_series(fname)
  #outflow_values.append(out)
    #cso_flow = 0
    #hours = 0
    #tot_flow = 0
    #max_treatment = 3122*r #max cfs allowed to treatment
    #for i in outflow_values: #out_variables is list within list (though outer list is just one element) (cfs/impervious acres)
    # tot = len(i)
    #3  for j in i: 
    #    if float(j) > max_treatment:  #ratio method--- 
    #      tot_flow += float(j)
    #      cso = float(j) - max_treatment # subtracting treated from total outflow
    #      cso_flow += cso 
    #      hours += 1
    #tot_volume = tot_flow*900*7.48052 #convert to gallons, 900 seconds in 15 minutes
    #cso_volume = cso_flow*900*7.48052 #for seconds in 15 minutes
    #equiv_rat = cso_volume/tot_volume  #equivalency ratio
    #treated_volume = tot_volume - cso_volume
  #cso_volume_list.append(cso_volume)
  return {"peak":peak,"volume":volume,"runoff":runoff,"evap":evaporation,\
  "infil":infiltration, "precip":precipitation,"lid_dict":lid_dict, "outflow_series":outflow_series}
  # peak and volume are strings.  lid_dict is a dictionary of dicts

