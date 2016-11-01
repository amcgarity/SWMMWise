import itertools
from swmm_objects_lid import *
from swmm_read_cso_runoff import *
from subprocess import call
import sys

def runswmm(start, end):
	(section_names,sections) = read_inp("wingo_sewers.inp")
	model1 = swmm_model('Model1',section_names,sections)
	model1.change(option,'START_DATE','Value', start)
	model1.change(option,'REPORT_START_DATE','Value', start)
	model1.change(option,'END_DATE','Value', end)
	f = open("wingo_sewers.inp",'w')
	model1.output(f)
	f.close()

def main():
	swmm_data_file = open("cso_runoff_data", "w")
	swmm_data_file.write("runoff  CSO_outflow   Date \n")
	dates = ['07/01/2008', '08/01/2008', '09/01/2008','10/01/2008', '11/01/2008', '12/01/2008', \
	 '01/01/2009', '02/01/2009', '03/01/2009', '04/01/2009', '05/01/2009', '06/01/2009', \
	 '07/01/2009', '08/01/2009', '09/01/2009','10/01/2009', '11/01/2009', '12/01/2009', '01/01/2010', \
	 '02/01/2010', '03/01/2010', '04/01/2010', '05/01/2010', '06/01/2010', '07/01/2010', \
	 '08/01/2010', '09/01/2010','10/01/2010', '11/01/2010', '12/01/2010', '01/01/2011', '02/01/2011', \
	 '03/01/2011', '04/01/2011', '05/01/2011', '06/01/2011', '07/01/2011', '08/01/2011', \
	 '09/01/2011','10/01/2011', '11/01/2011', '12/01/2011', '01/01/2012', '02/01/2012',  \
	 '03/01/2012', '04/01/2012', '05/01/2012', '06/01/2012', '07/01/2012', '08/01/2012', '09/01/2012', \
	 '10/01/2012', '11/01/2012', '12/01/2012', '01/01/2013', '02/01/2013', '03/01/2013', \
	 '04/01/2013', '05/01/2013', '06/01/2013', '07/01/2013', '08/01/2013', '09/01/2013', \
	 '10/01/2013', '11/01/2013', '12/01/2013', '01/01/2014', '02/01/2014', '03/01/2014', \
	 '04/01/2014', '05/01/2014', '06/01/2014']
	#for i in range(1,21,1):
	print len(dates)
	months = len(dates)-1
	print months
	for i in range(months):
		start = dates[i]
		end = dates[i+1]
		runswmm(start, end)
		call(["./swmm5", "wingo_sewers.inp", "C:/Users/Jonathan/Desktop/python_runs/outtest.txt", "C:/Users/Jonathan/Desktop/python_runs/out.out"])
		#out_vals=read_cso("outtest.txt")
		#swmm_data_file.write("%s \n" % (out_vals))\

		run_vals=read_runoff("outtest.txt")
		out_vals=read_outflow("outtest.txt")
		print run_vals
		print out_vals
		print start
		swmm_data_file.write("%s" % (run_vals))
		swmm_data_file.write("  %s" % (out_vals))
		swmm_data_file.write("  %s \n" % (start))
		#print('run#: %s' % (i))
	swmm_data_file.close()	
main()