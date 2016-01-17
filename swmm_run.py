from swmm_objects import *
from swmm_read import *
from subprocess import call
import sys

def runswmm():
    # Read in the SWMM input (.inp) file
	###(section_names,sections) = read_inp("wingohocking.inp")
	(section_names,sections) = read_inp("Example2_LID_BR_for_RG_PHL.inp")

	# Create an instance of a swmm_model object using the data
	model1 = swmm_model('Model1',section_names,sections)
	###model1.change('[SUBAREAS]','S7','Simp','999')
	###model1.change('[LID_USAGE]',('S1','wakefield_RG'),'RptFile','report.txt')
	#model1.lidChangeArea('S1','wakefield_BR_RG','999')
	#model1.lidChangeNumber('S1','wakefield_BR_RG','1')

    # Write out the model to a new file
	f = open("Ex2_modified.inp",'w')
	model1.output(f)
	f.close()
	# Run the new model file
	call(["swmm5","Ex2_modified.inp", "Ex2_modified.txt", "out.out"])
	# collect the new results:
	(peak,volume,lid_report) = read_report("Ex2_modified.txt")
	#peak = 0.0
	#volume = 0.0
	#lid_report = None
	return (peak,volume,lid_report)

def main():
	acre = 43560.0
	outfile = 'swmm_run_output.txt'
	f = open(outfile,'w')
	(peak,volume,lid_report) = runswmm()
	f.write('peak = %s volume = %s' % (peak,volume) )
	f.write('\n')
	f.close()
	print "peak = %s  volume = %s" % (peak,volume)
	print "LID Report:"
	print lid_report

main()
