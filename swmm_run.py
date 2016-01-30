from swmm_objects import *
from swmm_read import *
from pymongo import MongoClient
from datetime import datetime
import yaml
from subprocess import call
import sys

def runswmm(runParamList,swmmInitialInpFileStr,runsCollection):

	(section_names,sections) = read_inp(swmmInitialInpFileStr)
	# Create an instance of a swmm_model object using the SWMM inp data:
	model1 = swmm_model('Model1',section_names,sections)
	#print sections['[INFILTRATION]']
	for item in runParamList:
		subCat = item['Subcat']
		lid = item['LID']
		newNumber = item['Number']
		newArea = item['Area']
		newWidth = item['Width']
		CapRatioPct = item['CapRatioPct']
		model1.lidChangeNumber(subCat,lid,newNumber)
		model1.lidChangeArea(subCat,lid,newArea,CapRatioPct)
		###model1.lidChangeWidth(subCat,lid,newWidth)
		###model1.lidChangeFromImp(subCat,lid,newFromImp)
    # Write out the model to a new file because SWMM must have a file
	f = open("SWMM_modified.inp",'w')
	swmmInputFileStr=model1.output()
	f.write(swmmInputFileStr)  # write out the swmmInputFileStr for modified problem
	f.close()
	# Run the new model file
	startTime = datetime.now()   # obtain the starting time of the run
	startTimeStr = str(startTime)
	call(["swmm5","SWMM_modified.inp", "SWMM_modified.txt", "out.out"])
	endTime = datetime.now()   # obtain the ending time of the run
	elapsedTime = endTime - startTime
	minAndSec = divmod(elapsedTime.total_seconds(), 60)
	elapsedTimeStr = "%s min, %0.2f sec" % minAndSec
	print elapsedTimeStr
# 2 minutes, 5.74943 seconds
	# collect the new results:
	(peak,volume,lidDict) = read_report("SWMM_modified.txt")
	run = { "peak": peak, "volume": volume, "lidDict": lidDict, "swmmInputFileStr":swmmInputFileStr, "runParamList": runParamList,
		"swmmStartTime": startTimeStr, "swmmRunTime": elapsedTimeStr}
	doc_id = runsCollection.insert_one(run).inserted_id
	print "volume = %s" % volume
	return (doc_id)


def main():
	# open the mongodb database:
	#client = MongoClient('mongodb://server.mcgarity.info:27017/')
	client = MongoClient()  # use local server by default
	db = client['swmmwise_Wingo_Wakefield_Anna']  # use or create the database
	runsToday = db['y16m01d29_testing']   # use or create the collection
	###outfile = 'swmm_run_output.txt'
	###f = open(outfile,'w')
	swmmInpFile = "wingohocking_borg_initial.inp"
	infile = open(swmmInpFile,'r')
	swmmInitialInpFileStr = infile.readlines()
	infile.close()
	f = open('wingo_Anna_list.yaml','r')
	runParamList = yaml.load(f)
	f.close()
	dateTime = datetime.now()
	(doc_id) = runswmm(runParamList,swmmInitialInpFileStr,runsToday)
	###f.write('peak = %s volume = %s' % (peak,volume) )
	###f.write('\n')
	###f.close()
	###print "peak = %s  volume = %s" % (peak,volume)
	###print "LID Report:"
	###print lid_report
	#run = { "peak": peak, "volume": volume, "lidDict": lidDict, "runParamList": runParamList,
	#		"dateTime": dateTime}
	#doc_id = runsToday.insert_one(run).inserted_id
	print "Successfully stored %s" % doc_id


main()
