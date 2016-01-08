# AEM Modified 11/2015 to include [LID_CONTROLS] and [LID_USAGE] sections

__metaclass__ = type	# new style classes
import sys

# NOTE: each SWMM .inp file major category section will have one or more swmmobjects created for it:
class swmmobject:
	# NOTE: the portion of the SWMM .inp file associated with a swmmobject depends on the SWMM section.
	# pnames = swmm parameter layer names assigned in each object subclass below
	# pvals = swmm defined parameter values for this layer (one or more for parameter values for each parameter layer name)

	# NOTE: this is the default parse which works for swmm categories for which an object is associated with a single line
	def parse(self,str):  
		strlist = str.split()  # return a list of the words in "str"
		numlist = len(strlist) # the total number of words found in "str"
		numnames = len(self.pnames)  # the number of defined values (numeric or string) for parameters in this category section
		parlist = []
		if numlist <= numnames:
			for i in range(numlist):
				parlist.append(strlist[i])   # capture the parameter values actually used for this parameter layer for the model
			for i in range(numlist, numnames):  
				parlist.append(' ')   # give value of ' ' for values not used for this parameter layer in the swmm file
		else:   # the number of parameter values found in the swmm file for this layer is greater than the number of parameter names
			for i in range(numnames-1):   
				parlist.append(strlist[i]) # for all but the last name, assign found values one-to-one with names
			remaining_text = ''
			for i in range(numnames-1,numlist):
				# join all of the remaining values separated by ' ' and assign to the last name:
				remaining_text += ' ' + strlist[i] 
			parlist.append(remaining_text)  # treat the remaining text as a single value for the last name
		return parlist
	def __init__(self,pvals):
		self.pdict = {}   # the parameter dictionary for this swmm object
		# NOTE: swmm parameter layers have at least one parameter value and frequently several parameter values
		for i in range(len(pvals)):
			self.pdict[self.pnames[i]] = pvals[i]  # parameter values (in the required order) keyed by the parameter name
	def put(self,f):
		for i in self.pnames:
			f.write("%s\t" % self.pdict[i])
		f.write("\n")
	def change(self,pname,pvalue):
		self.pdict[pname]=pvalue

class title(swmmobject):
	heading = '[TITLE]'
	#name = 'Text'
	##def parse(self,linelist):   # overrides the swmmobject parse()
		# in a title section, each line identifies a single parameter name and its value

	##	return([str])
	def __init__(self,linelist):
		self.numpar = 0
		self.pardict = {}
		for line in linelist:
			self.numpar = self.numpar + 1
			parname = line[0]
			parval = line[1]
			self.pardict[parname] = parval
		###self.pnames = ['Text']
		###swmmobject.__init__(self,self.parse(str))
	def output(self):
		outstr = ''
		for parname in self.paramdict:
			parval = self.pardict[parname]
			outstr = outstr + parname + parval + "\n"
			return outstr
class option(swmmobject):
	heading = '[OPTIONS]'
	def parse(self,str):
		return(str.split())
	def __init__(self,str):
		self.pnames = ['Name', 'Value']
		plist = self.parse(str)
		self.name = plist[0]
		swmmobject.__init__(self,plist)
class evaporation(swmmobject):
	heading = '[EVAPORATION]'
	def __init__(self,str):
		self.pnames = ['Type','Values']
		pvals = self.parse(str)    # using the swmmobject parse()
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class raingage(swmmobject):
	heading = '[RAINGAGES]'
	def __init__(self,str):
		self.pnames = ['Name', 'Form', 'Intvl', 'SCF', 'Type']  # 'Name' = parameter layer name
		pvals = self.parse(str)
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class subcatchment(swmmobject):
	heading = '[SUBCATCHMENTS]'
	def __init__(self,str):
		self.pnames = ['Name', 'Rgage', 'OutID', 'Area', 'PctImperv', 'Width', 'Slope', 'Clength', 'Spack']
		pvals = self.parse(str)
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class subarea(swmmobject):
	heading = '[SUBAREAS]'
	def __init__(self,str):
		self.pnames = ['Subcat', 'Nimp', 'Nperv', 'Simp', 'Sperv', 'PctZero', 'RouteTo', 'PctRted']
		pvals = self.parse(str)
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class infiltration(swmmobject):
	heading = '[INFILTRATION]'
	def __init__(self,str):
		self.pnames = ['Subcat', 'Parameters']
		pvals = self.parse(str)
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class junction(swmmobject):
	heading = '[JUNCTIONS]'
	def __init__(self,str):
		self.pnames = ['Name', 'Elev', 'Ymax', 'Y0', 'Ysur', 'Apond']
		pvals = self.parse(str)
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class outfall(swmmobject):
	heading = '[OUTFALLS]'
	def __init__(self,str):
		self.pnames = ['Name', 'Elev', 'Type', 'Parameters']
		pvals = self.parse(str)
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class conduit(swmmobject):
	heading = '[CONDUITS]'
	def __init__(self,str):
		self.pnames = ['Name', 'Node1', 'Node2', 'Length', 'N', 'Z1', 'Z2', 'Q0', 'Qmax']
		pvals = self.parse(str)
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class xsection(swmmobject):
	heading = '[XSECTIONS]'
	def __init__(self,str):
		self.pnames = ['Link', 'Parameters']
		pvals = self.parse(str)
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class timeser(swmmobject):
	heading = '[TIMESERIES]'
	def __init__(self,str):
		self.pnames = ['Name', 'Parameters']
		pvals = self.parse(str)
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class report(swmmobject):
	heading = '[REPORT]'
	def parse(self,str):
		return(str.split())
	def __init__(self,str):
		self.pnames = ['Name', 'Value']
		plist = self.parse(str)
		self.name = plist[0]
		swmmobject.__init__(self,plist)
class lid_controls(swmmobject):   # multiline category
    heading = '[LID_CONTROLS]'
    def parse(self,str):
        return(str.split())
    def __init__(self,str):
        self.pnames = ['Name','Parameters']
        plist = self.parse(str)
        self.name = plist[0]
        swmmobject.__init__(self,plist)
class lid_usage(swmmobject):   # multiline category
    heading = '[LID_USAGE]'
    def parse(self,str):
        return(str.split())
    def __init__(self,str):
        self.pnames =  ['Subcatchment','LID_Process','Number','Area','Width','InitSat','FromImp','ToPerv','RptFile','DrainTo']
        plist = self.parse(str)
        self.name = plist[0]
        swmmobject.__init__(self,plist)

# GLOBAL VARIABLE SECTION:
# Here is the list of swmm section objects that will be saved or manipulated for the current project:


# NOTE: a swmmcategory object is instantiated for each SWMM file category section.
#       and each swmmcategory object contains one or more swmmobjects
class swmmcategory:
	def __init__(self,objclass,linelist):
		self.heading = objclass.heading
		self.odict = {}

	def add(self,obj):
		oname = obj.name
		self.odict[oname] = obj
	def setactive(self,actlist):
		self.active_list = actlist
	def putitems(self,f):
		f.write(self.heading+'\n')
		for item in self.active_list:
			self.odict[item].put(f)
	def change(self,oname,pname,pvalue):
		self.odict[oname].change(pname,pvalue)

class swmm_model:
	def __init__(self,name,section_names,sections):
		# section_names = a list of all the section heading names found in the SWMM .inp file
		# sections = a dictionary, keyed by section_names containing a list of strings, one for each line in each category section
		self.name = name  # name of the model
		# identify the SWMM section categories we currently support in this program:
		self.catclasses = [title]#[title,option,evaporation,raingage,subcatchment,subarea,infiltration,
					#junction,outfall,conduit,xsection,timeser,report,lid_controls,lid_usage]  # list of classes defined above
		###self.multiline_objects = [lid_controls,lid_usage]  # identify those objects that have parameter values on multiple lines
		self.catdict = {}
		for swmmcat in self.catclasses:		# populate the "catdict" dictionary with swmm section object names keyed by the section header
			self.catdict[swmmcat.heading]=swmmcat  # pull the heading text string from each swmmobject class for key and use the object for the value
			###objclass = self.catdict[head]  # retrieve the object class name created above for each section name (heading)
			###heading = swmmcat.heading
			###cat = swmmcategory(swmmcat,sections[heading]) # create a swmmcategory object for the swmm section category
		self.moddict = {}  # dictionary to hold swmm section objects
		for heading in section_names:
			if heading in self.catdict:  # compares headings read in file with headings defined in swmmobject category classes
				objclass = self.catdict[heading]  # retrieve the swmm category class for each section heading found in file
				cat = objclass(sections[heading])
				##cat = swmmcategory(objclass,sections[heading]) # instantiate a swmmcategory object for the swmm section category
			###active_list =[]
			''' MOVE TO PARSE FUNCTIONS FOR EACH CATEGORY SECTION
			for line in sections[head]:	# for each line in the data file for this section
				obj = self.objclass(line)    # instantiate the swmmobject corresponding to this line with the data in the line 
				cat.add(obj)			# add this swmmobject to its swmmcategory (major SWMM .inp file section)
				active_list.append(obj.name)  # build the list of active swmmobject names for this swmmcategory
			'''
			###cat.setactive(active_list)  # transfer the built active_list to the swmmcategory object
			self.moddict[objclass] = cat  # add this swmmcategory object to the swmm_model's dictionary
	def output(self,f):
		for obj in self.catclasses:
			###cat = self.moddict[obj]
			outstr = obj.output()
			f.write(obj.heading+'\n')
			f.write(outstr)
	def change(self,objclass,objname,pname,pvalue):
		self.moddict[objclass].change(objname,pname,pvalue)

				

