from swmm_objects import *
from swmm_read import *
from subprocess import call
import sys

def runswmm():
    # Read in the SWMM input (.inp) file
	(section_names,sections) = read_inp("wingohocking.inp")
	# Create an instance of a swmm_model object using the data
	model1 = swmm_model('Model1',section_names,sections)
    # Write out the model to a new file
	f = open("Ex4_modified.inp",'w')
	model1.output(f)
	f.close()
	# Run the new model file
	call(["./swmm5","wingohocking_modified.inp", "wingohocking_modified.txt", "out.out"])
	(peak,volume) = read_report("wingohocking_modified.txt")
	return (peak,volume)

def main():
	acre = 43560.0
	outfile = 'swmm_run_output.txt'
	f = open(outfile,'w')
	(peak,volume) = runswmm()
	f.write('peak = %s volume = %s' % (peak,volume) )
	f.write('\n')
	f.close()

main()
