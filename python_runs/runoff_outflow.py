import itertools
from swmm_objects_lid import *
from swmm_read_runoff import *
from subprocess import call
import sys

def runswmm(start, end):
	(section_names,sections) = read_inp("wingo_sewers_one_outlet.inp")
	model1 = swmm_model('Model1',section_names,sections)
	model1.change(option,'START_DATE','Value', start)
	model1.change(option,'REPORT_START_DATE','Value', start)
	model1.change(option,'END_DATE','Value', end)
	f = open("wingo_sewers_one_outlet.inp",'w')
	model1.output(f)
	f.close()

def main():
	runoff_data_file = open("runoff_data", "w")
	runoff_data_file.write("Runoff     Total_outflow      CSO_volume     Treated     precipitation     evaporation      infiltration     hours_cso      Date \n")
	#outflow_data_file = open("outflow_data", "w")
	#hours_data_file = open("hour_data","w")
	dates = ['07/01/2008', '08/01/2008','09/01/2008','10/01/2008', '11/01/2008', '12/01/2008', \
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
	#print len(dates)
	months = len(dates)-1
	#print months
	for i in range(months):
		month_variables = []
		out_variables = []
		start = dates[i]
		end = dates[i+1]
		runswmm(start, end)
		call(["./swmm5", "wingo_sewers_one_outlet.inp", "C:/Users/Jonathan/Desktop/python_runs/runoff_rep.rpt"])#, "C:/Users/Jonathan/Desktop/python_runs/out.out"])
		#out_vals=read_cso("outtest.txt")
		#swmm_data_file.write("%s \n" % (out_vals))\
		run_vals=read_runoff("runoff_rep.rpt")
		out_vals=read_out_volume("runoff_rep.rpt")
		precip_vals=read_precipitation("runoff_rep.rpt")
		evap_vals=read_evaporation("runoff_rep.rpt")
		infil_vals=read_infiltration("runoff_rep.rpt")
		times, outflows = read_outflow("runoff_rep.rpt")  #assigns variable to each month's outflow data
		
		out_variables.append(outflows) #convert outflows to string
		month_variables.append(times)
		print start
		# converting units
		#325851
		run_vals = float(run_vals)*325851 #convert from acre-ft to gallons
		out_vals = float(out_vals)*1000000 #convert from gallons*10^6 to gallons
		precip_vals = float(precip_vals)*325851
		evap_vals = float(evap_vals)*325851
		infil_vals  = float(infil_vals)*325851

		#calculating treated and cso volume
		cso_flow = 0
		hours = 0
		tot_flow = 0
		max_treatment = 3122*0.05
		for i in out_variables: #out_variables is list within list (though outer list is just one element)
			tot = len(i)
			for j in i:
				if float(j) > max_treatment:  #ratio method
					tot_flow += float(j)
					cso = float(j) - max_treatment
					cso_flow += cso 
					hours += 1
		tot_volume = tot_flow*900*7.48052 #conver to gallons, and seconds in an hour
		cso_volume = cso_flow*900*7.48052 #for seconds in a hour
			#equiv_rat = cso_volume/tot_volume  #equivalency ratio
		treated_volume = tot_volume - cso_volume
		runoff_data_file.write("%s" % (run_vals))
		runoff_data_file.write(" %s" % (out_vals))
		runoff_data_file.write("  %s" % (cso_volume))
		runoff_data_file.write("  %s" % (treated_volume))
		runoff_data_file.write("  %s" % (precip_vals))
		runoff_data_file.write("  %s" % (evap_vals))
		runoff_data_file.write("  %s" % (infil_vals))
		runoff_data_file.write("  %s" % (hours))
		#runoff_data_file.write("  %s" % (equiv_rat))
		runoff_data_file.write("  %s \n" % (start))


	runoff_data_file.close()



#if(scoop=1)then(removefromprogram)
main()