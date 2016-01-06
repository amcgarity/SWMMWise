from swmm_objects import *
from swmm_read import *
from subprocess import call
from random import choice
import sys

BMP_subcatchments = ["S_FS_1","S_FS_2","S_FS_3","S_FS_4","S_IT_1","S_IT_2","S_IT_3","S_IT_4"]
FS_subcatchments = ["S_FS_1","S_FS_2","S_FS_3","S_FS_4"]
IT_subcatchments = ["S_IT_1","S_IT_2","S_IT_3","S_IT_4"]
FS_widths = {"S_FS_1":"410", "S_FS_2":"463", "S_FS_3":"267", "S_FS_4":"894"}
IT_lengths = {"S_IT_1":"450", "S_IT_2":"474", "S_IT_3":"450", "S_IT_4":"470"}
FS_widths = {"S_FS_1":"410", "S_FS_2":"463", "S_FS_3":"267", "S_FS_4":"894"}
FS_length_orig = 4.0  #feet
IT_lengths = {"S_IT_1":"450", "S_IT_2":"474", "S_IT_3":"450", "S_IT_4":"470"}
IT_width_orig = 3.0  #feet

def runswmm(BMP_length, BMP_width, BMP_area ,BMP_imperv):
	(section_names,sections) = read_inp("Example4_bare_fast_PHL.inp")
	model1 = swmm_model('Model1',section_names,sections)

	for bmp in BMP_subcatchments:
		length = BMP_length[bmp]
		model1.change(subcatchment,bmp,'Length',length)
		width = BMP_width[bmp]
		model1.change(subcatchment,bmp,'Width',width)
		area = BMP_area[bmp]
		model1.change(subcatchment,bmp,'Area',area)
		imperv = BMP_imperv[bmp]
		model1.change(subcatchment,bmp,'PctImperv',imperv)
	f = open("Ex4_modified.inp",'w')
	model1.output(f)
	f.close()
	call(["./swmm5","Ex4_modified.inp", "Ex4_modified.txt", "out.out"])
	(peak,volume) = read_report("Ex4_modified.txt")
	return (peak,volume)

def main():
	acre = 43560.0
	outfile = 'Ex4_run_random.txt'

	BMP_length = {}
	BMP_width = {}
	BMP_area = {}	
	BMP_imperv = {}
	nruns = 1
	f = open(outfile,'w')
	f.close()

	byterange = range(0,255)
	max_mult = 4
	multiple_range = range(1,max_mult+1)
	for run in range(1,nruns+1):
		byte = choice(byterange)
		byte += 2**8
		print "\nRun Number %i" % run
		f = open(outfile,'a')
		bit_pattern = bin(byte)
		run_pattern = bit_pattern[3:]
		bit = 0
		sys.stdout.write('imperv: ')
		for bmp in BMP_subcatchments:
			imperv = int(run_pattern[bit])*100
			f.write('%s ' % run_pattern[bit])
			BMP_imperv[bmp] = imperv
			sys.stdout.write('%i ' % imperv)
			bit += 1
		sys.stdout.write('\n')
		sys.stdout.write('areas: ')
		for bmp in FS_subcatchments:
			mult = choice(multiple_range)
			f.write('%i ' % mult)
			length = FS_length_orig * mult
			width = float(FS_widths[bmp])
			area = length*width/acre
			sys.stdout.write('%f ' % area)
			BMP_length[bmp] = str(length)
			BMP_width[bmp] = str(width)
			BMP_area[bmp] = str(area)
		for bmp in IT_subcatchments:
			mult = choice(multiple_range)
			f.write('%i ' % mult)
			width = IT_width_orig * mult
			length = float(IT_lengths[bmp])
			area = length*width/acre
			sys.stdout.write('%f ' % area)
			BMP_length[bmp] = str(length)
			BMP_width[bmp] = str(width)
			BMP_area[bmp] = str(area)
		sys.stdout.write('\n')
#		for bmp in BMP_subcatchments:
#			f.write('%s %s %s: ' % (BMP_length[bmp],BMP_width[bmp],BMP_area[bmp]))
		(peak,volume) = runswmm(BMP_length, BMP_width, BMP_area ,BMP_imperv)
		f.write('%s %s' % (peak,volume) )
		f.write('\n')
	f.close()

main()
