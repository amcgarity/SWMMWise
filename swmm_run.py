from swmm_objects import *
from swmm_read import *
from subprocess import call
import sys

def runswmm(runParamList):
    # Read in the SWMM input (.inp) file
	###(section_names,sections) = read_inp("wingohocking.inp")
	(section_names,sections) = read_inp("Example2_LID_BR_for_RG_PHL.inp")

	# Create an instance of a swmm_model object using the data
	model1 = swmm_model('Model1',section_names,sections)
	#model1.lidChangeFromImp('S1','wakefield_BR_RG','999')
	###model1.change('[SUBAREAS]','S7','Simp','999')
	###model1.change('[LID_USAGE]',('S1','wakefield_RG'),'RptFile','report.txt')
	#model1.lidChangeArea('S1','wakefield_BR_RG','999')
	###model1.lidChangeNumber('S1','wakefield_BR_RG','1')
	for item in runParamList:
		subCat = item['Subcat']
		lid = item['LID']
		newNumber = item['Number']
		newArea = item['Area']
		newWidth = item['Width']
		newFromImp = item['FromImp']
		model1.lidChangeNumber(subCat,lid,newNumber)
		model1.lidChangeArea(subCat,lid,newArea)
		model1.lidChangeWidth(subCat,lid,newWidth)
		model1.lidChangeFromImp(subCat,lid,newFromImp)
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

from pymongo import MongoClient
from datetime import datetime
import yaml
def main():
	# open the mongodb database:
	client = MongoClient('mongodb://server.mcgarity.info:27017/')
	db = client.swmmwiseDebug
	runsToday = db.y16m01d22
	###outfile = 'swmm_run_output.txt'
	###f = open(outfile,'w')
	f = open('runlist.yaml','r')
	runParamList = yaml.load(f)
	f.close()
	dateTime = datetime.now()
	(peak,volume,lidDict) = runswmm(runParamList)
	###f.write('peak = %s volume = %s' % (peak,volume) )
	###f.write('\n')
	###f.close()
	###print "peak = %s  volume = %s" % (peak,volume)
	###print "LID Report:"
	###print lid_report
	run = { "peak": peak, "volume": volume, "lidDict": lidDict, "runParamList": runParamList,
			"dateTime": dateTime}
	doc_id = runsToday.insert_one(run).inserted_id
	print "Successfully stored %s" % doc_id


#main()
