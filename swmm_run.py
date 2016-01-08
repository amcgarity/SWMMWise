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
	f = open("wingo_modified.inp",'w')
	model1.output(f)
	f.close()
	# Run the new model file
	###call(["swmm5","Example4_bare_fast_PHL.inp", "Example4_bare_fast_PHL.txt"])
	###(peak,volume) = read_report("Example4_bare_fast_PHL.txt")
	peak = 0.0
	volume = 0.0
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
