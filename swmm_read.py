"""
swmmread.py
Read SWMM input file and create objects for each input category
2013 Arthur McGarity
Swarthmore College
AEM: Modified 11/2015 to include LID categories in input file
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
        line_ns = line.strip()  # remove whitespace
        if line_ns in section_names:
           name = line_ns
           section_list = []
           try:
               next_line = data1[i+1]  # look ahead at next line
           except IndexError:
               end = True
           next_line_ns = next_line.strip()  # remove whitespace
           if (end or (next_line_ns in section_names)):
              sections[name] = section_list
        else:
           section_list.append(line)
           try:
               next_line = data1[i+1]  # look ahead at next line
           except IndexError:
               end = True
           next_line_ns = next_line.strip()  # remove whitespace
           if (end or (next_line_ns in section_names)):
              sections[name] = section_list
#    for i in section_names:
#        sys.stdout.write("%s\n" % i)
#        for j in sections[i]:
#            sys.stdout.write(j)    

    return((section_names,sections))

def read_report(fname):
  infile = open(fname,'r')
  data = infile.read()
  outfall_start_index = data.find('Outfall Loading Summary')
  output_start_index = data.find('System',outfall_start_index)
  split = data[output_start_index:].split('\n',1)
  output_line = split[0]
#  print output_line
  output_list = output_line.split()
  peak = output_list[3]
  volume = output_list[4]
#  print (peak,volume)
  return (peak,volume)


