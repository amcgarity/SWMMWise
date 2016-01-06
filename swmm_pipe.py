#!/usr/bin/python
from swmm_objects import *
from swmm_read import *
import os
import subprocess
from random import choice
import sys


BMP_subcatchments = ["S_FS_1","S_FS_2","S_FS_3","S_FS_4","S_IT_1","S_IT_2","S_IT_3","S_IT_4"]
FS_subcatchments = ["S_FS_1","S_FS_2","S_FS_3","S_FS_4"]
IT_subcatchments = ["S_IT_1","S_IT_2","S_IT_3","S_IT_4"]
FS_widths = {"S_FS_1":"410", "S_FS_2":"463", "S_FS_3":"267", "S_FS_4":"894"}
IT_lengths = {"S_IT_1":"450", "S_IT_2":"474", "S_IT_3":"450", "S_IT_4":"470"}
FS_length_orig = 4.0  #feet
IT_width_orig = 3.0  #feet
FS_cost = 80  # $K/acre of installed practice (not impervious area served)
IT_cost = 40  # $K/acre of installed practice (not impervious area served)
base_volume = 18.713   # annual volume before BMPs  (Million Gallons)

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
#    sys.stderr.write('In runswmm\n')
    output = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE).communicate()[0]
    output = subprocess.Popen(["./swmm5","Ex4_modified.inp", "Ex4_modified.txt", "out.out"], stdout=subprocess.PIPE).communicate()[0]
#    subprocess.call("ls -l", stdout=None,shell=False)
 #   os.system('./swmm5 Ex4_modified.in Ex4_modified.txt out.out > /dev/null')
    (peak,volume) = read_report("Ex4_modified.txt")
    return (peak,volume)

def main():
    acre = 43560.0    # square feet
    outfile = 'Ex4_pipe_outfile.txt'

    BMP_length = {}
    BMP_width = {}
    BMP_area = {}	
    BMP_imperv = {}
    BMP_cost = {}
    f = open(outfile,'w')
    f.close()
    (section_names,sections) = read_inp("Example4_bare_fast_PHL.inp")
    model1 = swmm_model('Model1',section_names,sections)

    run = 0
    while True:
        line=sys.stdin.readline()
        if not line: break
        run = run + 1
        sys.stderr.write("\nRun Number %i\n" % run)
        f = open(outfile,'a')
        #f.write("In child received the line: %s" % line)
        vars = []
        objs = []
        for t in line.split():
            vars.append(float(t))
#            sys.stderr.write('%f ' % float(t))
#        sys.stderr.write('\n')
        i = 0
        for bmp in BMP_subcatchments:
            imperv = vars[i]
            f.write('%s ' % imperv)
            BMP_imperv[bmp] = imperv
            i += 1
        for bmp in FS_subcatchments:
            mult = vars[i]
            f.write('%i ' % mult)
            length = FS_length_orig * mult
            width = float(FS_widths[bmp])
            area = length*width/acre
            cost = area * FS_cost * (100.0-BMP_imperv[bmp])/100.0
            BMP_length[bmp] = str(length)
            BMP_width[bmp] = str(width)
            BMP_area[bmp] = str(area)
            BMP_cost[bmp] = cost
            i += 1
        for bmp in IT_subcatchments:
            mult = vars[i]
            f.write('%i ' % mult)
            width = IT_width_orig * mult
            length = float(IT_lengths[bmp])
            area = length*width/acre
            cost = area * IT_cost * (100.0-BMP_imperv[bmp])/100.0
            BMP_length[bmp] = str(length)
            BMP_width[bmp] = str(width)
            BMP_area[bmp] = str(area)
            BMP_cost[bmp] = cost
            i += 1
#        sys.stderr.write('Hey Ho:\n')
#        for bmp in BMP_subcatchments:
#            sys.stderr.write('%s %s %s: ' % (BMP_length[bmp],BMP_width[bmp],BMP_area[bmp]))
        (peak,volume) = runswmm(BMP_length, BMP_width, BMP_area ,BMP_imperv)
        volume_reduction = base_volume - float(volume)
        f.write('%s %s ' % (peak,volume) ) # Units:  (cfs,Mgal)
        total_cost = 0.0
#        sys.stderr.write('In swmm_pipe: volume_reduction = %f ' % volume_reduction)
        for bmp in BMP_subcatchments:
            total_cost += BMP_cost[bmp]
        f.write('%f %f' % (total_cost,volume_reduction) )
        f.write('\n')
#        sys.stderr.write('total_cost = %f\n' % total_cost)
        objs.append(total_cost)
        objs.append(-volume_reduction)
        line_out = ''
        for z in objs:
            line_out = line_out+str(z)+' '
        line_out = line_out+'\n'
        sys.stdout.write(line_out)
        sys.stdout.flush()
    f.close()
    exit(0)

main()
