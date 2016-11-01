"""
swmmread.py
Read SWMM input file and create objects for each input category
2013 Arthur McGarity
Swarthmore College
"""
import sys
#from swmm_objects import *

def read_inp(fname):
#    fname = "Example4_bare_PHL.inp"
    infile = open(fname,'r')
    data = infile.readlines()
    section_names = []
#    selected_section_names = ["[TITLE]","[OPTIONS]","[EVAPORATION]"]
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
        data1.append(line)
    sections = {}
    end = False
    for i in range(len(data1)):
        line = data1[i]
        line_ns = line.strip()
        if line_ns in section_names:
           name = line_ns
           section_list = []
           try:
               next_line = data1[i+1]
           except IndexError:
               end = True
           next_line_ns = next_line.strip()
           if (end or (next_line_ns in section_names)):
              sections[name] = section_list
        else:
           section_list.append(line)
           try:
               next_line = data1[i+1]
           except IndexError:
               end = True
           next_line_ns = next_line.strip()
           if (end or (next_line_ns in section_names)):
              sections[name] = section_list
#    for i in section_names:
#        sys.stdout.write("%s\n" % i)
#        for j in sections[i]:
#            sys.stdout.write(j)    

    return((section_names,sections))

def read_cso(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Outfall Loading Summary')
  output_start_index = data.find('CSO',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
#  print output_line
  output_list = output_line.split()
  print(output_list)
  print outfall_start_index
  peak = output_list[3]
  volume = output_list[4]
# print (peak,volume)
  return (volume)

def read_treated(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Outfall Loading Summary')
  output_start_index = data.find('outflow',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
#  print output_line
  output_list = output_line.split()
  print(output_list)
  peak = output_list[3]
  volume = output_list[4]
# print (peak,volume)
  return (volume)

def read_runoff(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Runoff Quantity Continuity')
  output_start_index = data.find('Surface ',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
#  print output_line
  output_list = output_line.split()
  print(output_list)
  runoff = output_list[3]
  #print (peak,volume)
  return (runoff)

def read_evaporation(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Runoff Quantity Continuity')
  output_start_index = data.find('Evaporation',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
#  print output_line
  output_list = output_line.split()
  print(output_list)
  evaporation = output_list[3]
  #print (peak,volume)
  return (evaporation)

def read_infiltration(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Runoff Quantity Continuity')
  output_start_index = data.find('Infiltration',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
#  print output_line
  output_list = output_line.split()
  print(output_list)
  infiltration = output_list[3]
  #print (peak,volume)
  return (infiltration)

def read_precipitation(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Runoff Quantity Continuity')
  output_start_index = data.find('Total',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
#  print output_line
  output_list = output_line.split()
  print(output_list)
  precipitation = output_list[3]
  #print (peak,volume)
  return (precipitation)
