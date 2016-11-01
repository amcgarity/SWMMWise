import itertools
from swmm_objects_lid import *
from swmm_read import *
from subprocess import call
import sys

def runswmm(diam):
	(section_names,sections) = read_inp("wingo_sewers.inp")
	model1 = swmm_model('Model1',section_names,sections)
	model1.change(xsection,'Or1','Geom1',diam)
	f = open("wingo_sewers.inp",'w')
	model1.output(f)
	f.close()

def main():
	swmm_data_file = open("outflow_data.txt", "w")
	for i in range(1,21,1):
		runswmm(i)
		call(["./swmm5", "wingo_sewers.inp", "C:/Users/Jonathan/Desktop/orifice_runs/outtest.txt", "C:/Users/Jonathan/Desktop/orifice_runs/out.out"])
		#out_vals=read_report("outtest.txt")
		#swmm_data_file.write("%s \n" % (out_vals))
		#print('run#: %s' % (i))
	swmm_data_file.close()	
main()