# AEM Modified 11/2015 to include [LID_CONTROLS] and [LID_USAGE] sections

__metaclass__ = type	# new style classes
import sys

class title():
# in the title section, each line contains a line of the title
	heading = '[TITLE]'
	def __init__(self,linelist):
		self.linelist = linelist
	def output(self):
		outstr = ''
		for line in self.linelist:
			outstr = outstr + line
		return outstr

class category1d:
	def parse(self,linelist):
		self.namelist = []   # list to hold parameter names in their original order
		self.pardict = {}
		for line in linelist:
			wordlist = line.split()  # split the line into words
			parname = wordlist[0]
			self.namelist.append(parname)
			nwords = len(wordlist)
			parstring = ''
			for i in range(1,nwords):
				parstring = parstring + wordlist[i] + ' '  # make one string out of all remaining words
			self.pardict[parname] = parstring	
	def __init__(self,linelist):
		self.parse(linelist)
	def output(self):
		outstr = ''
		for parname in self.namelist:
			parstring = self.pardict[parname]
			outstr = outstr + parname + '\t' + parstring + '\n'
		return outstr
	def change(self,objname,pname,pvalue):
		self.pardict[pname] = pvalue

class options(category1d):
# in an option section, each line identifies a single parameter name and its value
	heading = '[OPTIONS]'
	#pnames = ['Name', 'Value']
	def __init__(self,linelist):
		category1d.__init__(self,linelist)

class evaporation(category1d):
# this section will be treated as a parameter name followed by a string representing the rest of the line
	heading = '[EVAPORATION]'
	def __init__(self,linelist):
		category1d.__init__(self,linelist)

class temperature(category1d):
	heading = '[TEMPERATURE]'
	def __init__(self,linelist):
		category1d.__init__(self,linelist)

class raingages(category1d):
# this section will be treated as a parameter name followed by a string representing the rest of the line
	heading = '[RAINGAGES]'
	def __init__(self,linelist):
		category1d.__init__(self,linelist)

class infiltration(category1d):
	heading = '[INFILTRATION]'
	def __init__(self,linelist):
		category1d.__init__(self,linelist)

class xsections(category1d):
	heading = '[XSECTIONS]'
	def __init__(self,linelist):
		category1d.__init__(self,linelist)

class timeseries(category1d):
	heading = '[TIMESERIES]'
	def __init__(self,linelist):
		category1d.__init__(self,linelist)

class report(category1d):
	heading = '[REPORT]'
	def __init__(self,linelist):
		category1d.__init__(self,linelist)

class category2d:
	def parse(self,linelist):
		self.namelist = []   # list to hold parameter names in their original order
		self.pardict = {}
		for line in linelist:
			wordlist = line.split()  # split the line into words
			objname = wordlist[0]
			self.namelist.append(objname)  # object names found in swmm input file
			n = len(wordlist)
			m = self.npnames   # number of parameter names defined in SWMM users guide
			valnamelist = []   # will contain entries from the self.pnames list
			valdict = {}      # for each line parsed, will contain values found indexed by a name from pnames
			for i in range(0,m):   # assign ALL values defined in the SWMM manual
				if i <= n-2:   # input file has provided a value for this pname
					valnamelist.append(self.pnames[i])
					valdict[self.pnames[i]] = wordlist[i+1]
				else:     # input file has no value for this optional pname so assign empty string
					valdict[self.pnames[i]] = ''	
			if (n-1) > m:   # there must be a multiword parameter at the end of the line
				# tack on the extra words found in the dat file to the last named parameter:
				extraWords = valdict[self.pnames[m-1]]
				for i in range(m,n):  # iterate over the extra words found at the end of the line
					extraWords += (' '+wordlist[i])  # tack on a space followed by the next extra word
				valdict[self.pnames[m-1]] = extraWords
			self.pardict[objname] = (valnamelist,valdict)  # dictionary contains tuples	
	def __init__(self,linelist,pnames):
		self.pnames = pnames
		self.npnames = len(self.pnames)
		self.parse(linelist)
	def output(self):
		outstr = ''
		for objname in self.namelist:
			outstr = outstr + objname + '\t'
			(valnamelist,valdict) = self.pardict[objname]
			for val in valnamelist:
				outstr = outstr + valdict[val] + ' '
			outstr = outstr + '\n'
		#print outstr
		return outstr
	def change(self,objname,pname,newval):
		(valnamelist,valdict) = self.pardict[objname]
		valdict[pname] = newval
		self.pardict[objname] = (valnamelist,valdict)
	def get(self,objname,pname):
		(valnamelist,valdict) = self.pardict[objname]
		return valdict[pname]

class subcatchments(category2d):
	heading = '[SUBCATCHMENTS]'
	def __init__(self,linelist):
		pnames = ['Rgage', 'OutID', 'Area', 'PctImperv', 'Width', 'Slope', 'Clength', 'Spack']
		category2d.__init__(self,linelist,pnames)

class subareas(category2d):
	heading = '[SUBAREAS]'
	def __init__(self,linelist):
		pnames = ['Nimp', 'Nperv', 'Simp', 'Sperv', 'PctZero', 'RouteTo', 'PctRted']
		category2d.__init__(self,linelist,pnames)

class junctions(category2d):
	heading = '[JUNCTIONS]'
	def __init__(self,linelist):
		pnames = ['Elev', 'Ymax', 'Y0', 'Ysur', 'Apond']
		category2d.__init__(self,linelist,pnames)

class outfalls(category2d):
	heading = '[OUTFALLS]'
	def __init__(self,linelist):
		pnames = ['Elev', 'Type', 'Parameters']
		category2d.__init__(self,linelist,pnames)

class conduits(category2d):
	heading = '[CONDUITS]'
	def __init__(self,linelist):
		pnames = ['Node1', 'Node2', 'Length', 'N', 'Z1', 'Z2', 'Q0', 'Qmax']
		category2d.__init__(self,linelist,pnames)

class category3d:
	def parse3d(self,linelist):
		self.namelist = []   # list to hold layer names in their original order
		self.pardict = {}
		for line in linelist:
			wordlist = line.split()  # split the line into words
			name = (wordlist[0],wordlist[1])   # now a tuple
			self.namelist.append(name)
			n = len(wordlist)
			#m = self.npnames
			#valnamelist = []
			vallist = []
			for i in range(2,n):   # assign only those values that exist in the swmm .inp file
				vallist.append(wordlist[i])
			self.pardict[name] = vallist  # dictionary keyed by tuple (wordlist[0],wordlist[1])	
	def __init__(self,linelist):
		#self.pdict = pdict
		#self.types = types
		#for 
		#self.npnames = len(self.pnames)
		self.parse3d(linelist)

	def output(self):  # This is the default output function that can be used with subclasses that do not have a change function
		outstr = ''
		for objname in self.namelist:
			outstr = outstr + objname[0] + '\t' + objname[1] + '\t'
			vallist = self.pardict[objname]
			for val in vallist:
				outstr = outstr + val + ' '
			outstr = outstr + '\n'
		return outstr

class lid:
	types = ['BC','RG','GR','IT','PP','RB','RD','VS']
	layers = ['SURFACE','SOIL','PAVEMENT','STORAGE','DRAIN','DRAINMAT']
	# pdict is a dictionary keyed by the LID layer
	pdict = {'SURFACE':['StorHt','VegFrac','Rough','Slope','XSlope'],
			'SOIL':['Thick','Por','FC','WP','Ksat','Kcoeff','Suct'],
			'PAVEMENT':['Thick','Vratio','FracImp','Perm','Vclog'],
			'STORAGE':['Height','Vratio','Seepage','Vclog'],
			'DRAIN':['Coeff','Expon','Offset','Delay'],
			'DRAINMAT':['Thick','Vratio','Rough']}
	def __init__(self,lid_name,lid_type):
		self.name = lid_name
		self.type = lid_type
		self.layerlist = []
		self.valdict = {}
	def addlayer(self,parlayer,vallist):
		self.layerlist.append(parlayer)
		pnames = lid.pdict[parlayer]
		i = 0
		for par in pnames:
			self.valdict[(parlayer,par)] = vallist[i]
			i = i+1
			# print self.name + ' ' + parlayer + ' ' + par + ' ' + self.valdict[(parlayer,par)]
	def output(self):
		outstr = ''
		outstr = outstr + self.name + '\t' + self.type + '\n'
		for lay in self.layerlist:
			outstr = outstr + self.name + '\t' + lay + ' '
			for par in lid.pdict[lay]:
				val = self.valdict[(lay,par)]
				outstr = outstr + val + ' '
			outstr = outstr + '\n'
		return outstr
	def change(self,layer,param,newval):
		parname = (layer,param)   # a tuple
		self.valdict[parname] = newval
	def get(self,layer,param):
		parname = (layer,param)
		return self.valdict[parname]
		
class lid_controls(category3d):
	heading = '[LID_CONTROLS]'
	def parse(self):	
		for parname in self.namelist:
			vallist = self.pardict[parname]
			if not vallist:  # empty vallist means LID type is being defined
				lidname = parname[0]
				lidtype = parname[1]
				self.lidlist.append(lidname)
				if lidtype in lid.types:
					newlid = lid(lidname,lidtype)
					self.liddict[lidname] = newlid
				else:
					print "ERROR: SWMM Input File uses unknown LID Type"
			else:  # this parname contains parameters
				lidname = parname[0]
				parlayer = parname[1]
				thislid = self.liddict[lidname]
				thislid.addlayer(parlayer,vallist)
	def __init__(self,linelist):
		self.lidlist = []
		self.liddict = {}
		category3d.__init__(self,linelist)
		self.parse()
	def output(self):
		outstr = ''
		for ld in self.lidlist:
			#print ld
			lidobj = self.liddict[ld]
			#print lidobj.output()
			outstr = outstr + lidobj.output()
		return outstr
	def change3d(self,name,layer,param,newval):
		ld = self.liddict[name]
		ld.change(layer,param,newval)
	def change(self,name,pname,pvalue):
		self.change3d(name,pname[0],pname[1],pvalue)
	def get(self,name,layer,pname):
		ld = self.liddict[name]
		return ld.get(layer,pname)

class lid_usage(category3d):   # multiline category
	heading = '[LID_USAGE]'
	def parse(self):
		for name in self.namelist:
			vallist = self.pardict[name]
			n = len(vallist)
			m = len(self.pnames)  # number of parameter names defined in SWMM manual
			self.valnamelist = []
			valdict = {}
			for i in range(0,m):   # assign ALL values defined in the SWMM manual
				if i <= n-1:   # input file has provided a value for this pname
					self.valnamelist.append(self.pnames[i])
					valdict[self.pnames[i]] = vallist[i]
				else:     # input file has no value for this optional pname so assign empty string
					valdict[self.pnames[i]] = ''	
			if (n-1) > m:   # there must be a multiword parameter at the end of the line
				# tack on the extra words found in the dat file to the last named parameter:
				extraWords = valdict[self.pnames[m-1]]
				for i in range(m,n):  # iterate over the extra words found at the end of the line
					extraWords += (' '+vallist[i])  # tack on a space followed by the next extra word
				valdict[self.pnames[m-1]] = extraWords
			self.liddict[name] = valdict
	def __init__(self,linelist):
		self.liddict = {}
		self.pnames =  ['Number','Area','Width','InitSat','FromImp','ToPerv','RptFile','DrainTo']
		category3d.__init__(self,linelist)
		self.parse()
		#self.output()
	def output(self):
		outstr = ''
		for name in self.namelist:
			outstr = outstr + name[0] + '\t' + name[1] + '\t'
			valdict = self.liddict[name]
			for pname in self.pnames:
				val = valdict[pname]
				outstr = outstr + val + ' '
			outstr = outstr + '\n'
		return outstr
	def change(self,name,pname,newval):
		valdict = self.liddict[name]  # retrieve the current valdict for name
		valdict[pname] = newval   # change the specified value
		self.liddict[name] = valdict  # replace the current value with the new value
	def get(self,name,pname):
		valdict = self.liddict[name]
		return valdict[pname]

class swmm_model:
	def __init__(self,name,section_names,sections):
		self.name = name  # name of the model
		self.section_names = section_names
		self.sections = sections
		# identify the SWMM section categories we currently support in this program:
		self.catclasses = [title,options,evaporation,temperature,raingages,subcatchments,subareas,infiltration,
							lid_controls,lid_usage,
							junctions,outfalls,conduits,xsections,timeseries,report]
		self.catdict = {}
		for swmmcat in self.catclasses:		# populate the "catdict" dictionary with swmm section object names keyed by the section header
			# pull the heading text string from each swmmobject class for key and use the object for the value
			self.catdict[swmmcat.heading]=swmmcat  
		self.moddict = {}  # dictionary to hold swmm section objects
		for heading in section_names:
			if heading in self.catdict:  # compares headings read in file with headings defined in swmmobject category classes
				objclass = self.catdict[heading]  # retrieve the swmm category class for each section heading found in file
				cat = objclass(sections[heading])  # instantiate the category object
				self.moddict[objclass] = cat  # add this swmmcategory object to the swmm_model's dictionary
	def output(self):  #,f):
		swmmInputFileStr = ''
		for obj in self.catclasses:
			heading = self.catdict.keys()[self.catdict.values().index(obj)]  # return key associated with dict value
			if heading in self.section_names:      # only work with the sections found in input file
				cat = self.moddict[obj]
				outstr = cat.output()
				swmmInputFileStr += cat.heading+'\n'
				swmmInputFileStr += outstr
				#print cat.heading+'\n'
				#print outstr
		return swmmInputFileStr
				
	def change(self,catheading,objname,pname,pvalue):
		catclass = self.catdict[catheading]
		self.moddict[catclass].change(objname,pname,pvalue)

	def lidChangeArea(self,subcatchment,lidname,newarea,capRatioPct):
		# This is a change in the category [LID_USAGE]
		# AND to the PctImperv parameter of the subcatchment where the lids are placed
		# But the new PctImperv parameter must be CALCULATED first!!
		acre = 43560.0
		new_lid_acre = newarea/acre
		newarea_str = str(newarea)
		lid_usage_class = self.moddict[lid_usage]
		# Find out what LID type we are changing the area of:
		lid_controls_class = self.moddict[lid_controls]
		lid = lid_controls_class.liddict[lidname]
		lid_type = lid.type
		old_lid_area_str = lid_usage_class.get((subcatchment,lidname),'Area')  # LID area in SQUARE FEET
		old_lid_area = float(old_lid_area_str)
		old_lid_acre = old_lid_area/acre
		lid_number_str = lid_usage_class.get((subcatchment,lidname),'Number')
		lid_number = int(lid_number_str)
		
		subcatchments_class = self.moddict[subcatchments]
		subcat_area_str = subcatchments_class.get(subcatchment,'Area')
		subcat_area = float(subcat_area_str)  # Subcatchment area in acre
		subcat_PctImperv_old_str = subcatchments_class.get(subcatchment,'PctImperv')
		subcat_PctImperv_old = float(subcat_PctImperv_old_str)
		# old impervious area in acre:
		imperv_area_old = (subcat_PctImperv_old/100.0)*subcat_area   
		# original imperv area before any LID deployment:
		  
		lidOnPervList = ['GR','IT','PP','RB','RD']
		if lid_type in lidOnPervList:  # LID displaces some of the subcatchment's imperv. area
			# so we must adjust the % Impervious parameter in the subcatchment:
			imperv_area_original = imperv_area_old + lid_number*old_lid_acre			
			# new imperv area after "newnumber" of LID:
			imperv_area_new = imperv_area_original - lid_number*new_lid_acre 
			if imperv_area_new < 0.0: 
				imperv_area_new = 0.0
			subcat_PctImperv_new = 100*imperv_area_new/subcat_area
			subcat_PctImperv_new_str = "%.3f" % subcat_PctImperv_new
			subcatchments_class.change(subcatchment,'PctImperv',subcat_PctImperv_new_str)
			imperv_area = imperv_area_new
		else:
			# OTHERWISE, the impervious area & percentage remains the same as before:
			imperv_area = imperv_area_old
				
		# NOW: make the changes:
		lid_usage_class.change((subcatchment,lidname),'Area',newarea_str)  # change the number
		# adjust the FromImp parameter - the % of subcat area treated by each LID:
		#print "imperv_area = %s" % imperv_area
		capRatio = capRatioPct/100.0
		imperv_area_treated = lid_number*new_lid_acre/capRatio
		if imperv_area <= 0.0:
			lidFromImp = 0.0;
		else:
			lidFromImp_new = 100.0*imperv_area_treated/imperv_area
			if lidFromImp_new > 100.0:
				lidFromImp_new = 100.0    # don't let the impervious area served be more than 100%
		self.lidChangeFromImp(subcatchment,lidname,lidFromImp_new)

	def lidChangeNumber(self,subcatchment,lidname,newnumber):
		# This requires changes to both [LID_USAGE] (straightforward)
		# AND to the PctImperv parameter of the subcatchment where the lids are placed
		# But the new PctImperv parameter must be CALCULATED first!!
		acre = 43560.0
		newnumber_str = str(newnumber)
		lid_usage_class = self.moddict[lid_usage]
		lid_area_str = lid_usage_class.get((subcatchment,lidname),'Area')  # LID area in SQUARE FEET
		lid_area = float(lid_area_str)
		lid_acre = lid_area/acre
		lid_number_old_str = lid_usage_class.get((subcatchment,lidname),'Number')
		lid_number_old = int(lid_number_old_str)
		# Find out what LID type we are changing the area of:
		lid_controls_class = self.moddict[lid_controls]
		lid = lid_controls_class.liddict[lidname]
		lid_type = lid.type		
		lidOnPervList = ['GR','IT','PP','RB','RD']
		if lid_type in lidOnPervList:  # LID displaces some of the subcatchment's imperv. area
			# so we must adjust the % Impervious parameter in the subcatchment:
			subcatchments_class = self.moddict[subcatchments]
			subcat_area_str = subcatchments_class.get(subcatchment,'Area')
			subcat_area = float(subcat_area_str)  # Subcatchment area in acre
			subcat_PctImperv_old_str = subcatchments_class.get(subcatchment,'PctImperv')
			subcat_PctImperv_old = float(subcat_PctImperv_old_str)
			imperv_area_old = (subcat_PctImperv_old/100.0)*subcat_area   # old impervious area in acre
			lid_number_new = int(newnumber_str)
			# original imperv area before any LID deployment
			imperv_area_original = imperv_area_old + lid_number_old*lid_acre  
			# new imperv area after "newnumber" of LID
			imperv_area_new = imperv_area_original - lid_number_new*lid_acre 
			if imperv_area_new < 0.0:
				imperv_area_new = 0.0
			subcat_PctImperv_new = 100*imperv_area_new/subcat_area
			subcat_PctImperv_new_str = "%.3f" % subcat_PctImperv_new
			# change the pct. imperv
			subcatchments_class.change(subcatchment,'PctImperv',subcat_PctImperv_new_str)  
		# NOW make the changes to the number of LIDs:
		lid_usage_class.change((subcatchment,lidname),'Number',newnumber_str)  # change the number

		

	def lidChangeFromImp(self,subcatchment,lidname,newnumber):
		# Note: there appear to be no interlinked calculations required
		# So just change the number:
		newnumber_str = "%0.3f" % newnumber
		lid_usage_class = self.moddict[lid_usage]
		lid_usage_class.change((subcatchment,lidname),'FromImp',newnumber_str)  # change the number

	def lidChangeWidth(self,subcatchment,lidname,newnumber):
		# Note: there appear to be no interlinked calculations required
		# So just change the number:
		newnumber_str = "%0.3f" % newnumber
		lid_usage_class = self.moddict[lid_usage]
		lid_usage_class.change((subcatchment,lidname),'Width',newnumber_str)  # change the number
	def lidGetArea(self,subcatchment,lidname):
		lid_usage_class = self.moddict[lid_usage]
		lid_area_str = lid_usage_class.get((subcatchment,lidname),'Area')  # LID area in SQUARE FEET
		lid_area = float(lid_area_str)	
		return lid_area		