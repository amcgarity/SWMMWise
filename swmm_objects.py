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
		if numlist <= numnames:   # one or more optional parameters are NOT used
			for i in range(numlist):
				parlist.append(strlist[i])   # capture the parameter values actually used for this parameter layer for the model
			for i in range(numlist, numnames):  
				parlist.append(' ')   # give value of ' ' for optional values not used for this parameter layer in the swmm file
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
	def output(self):
		outstr = ''
		for i in self.pnames:
			f.write("%s\t" % self.pdict[i])
		f.write("\n")
	def change(self,pname,pvalue):
		self.pdict[pname]=pvalue

class title(swmmobject):
# in the title section, each line contains a line of the title
	heading = '[TITLE]'
	def __init__(self,linelist):
		self.linelist = linelist
	def output(self):
		outstr = ''
		for line in self.linelist:
			outstr = outstr + line + "\n"
		return outstr
class options(swmmobject):
# in an option section, each line identifies a single parameter name and its value
	heading = '[OPTIONS]'
	#pnames = ['Name', 'Value']
	def parse(self,linelist):
		self.numpar = 0
		self.namelist = []   # list to hold parameter names in their original order
		self.pardict = {}
		for line in linelist:
			self.numpar = self.numpar + 1
			wordlist = line.split()  # split the line into words
			parname = wordlist[0]
			self.namelist.append(parname)
			parval = wordlist[1]
			self.pardict[parname] = parval
	def __init__(self,linelist):
		self.parse(linelist)
	def output(self):
		outstr = ''
		for parname in self.namelist:
			parval = self.pardict[parname]
			outstr = outstr + parname + '\t' + parval + '\n'
		return outstr		
class evaporation(swmmobject):
# this section will be treated as a parameter name followed by a string representing the rest of the line
	heading = '[EVAPORATION]'
	def parse(self,linelist):
		self.numpar = 0
		self.namelist = []   # list to hold parameter names in their original order
		self.pardict = {}
		for line in linelist:
			self.numpar = self.numpar + 1
			wordlist = line.split()  # split the line into words
			parname = wordlist[0]
			self.namelist.append(parname)
			n = len(wordlist)
			parval = ''
			for i in range(1,n):
				parval = parval + ' ' + wordlist[i]
			self.pardict[parname] = parval
	def __init__(self,linelist):
		self.parse(linelist)
	def output(self):
		outstr = ''
		for parname in self.namelist:
			parval = self.pardict[parname]
			outstr = outstr + parname + '\t' + parval + '\n'
		return outstr

class category2d:
	def parse(self,linelist):
		self.numpar = 0
		self.namelist = []   # list to hold parameter names in their original order
		self.pardict = {}
		for line in linelist:
			self.numpar = self.numpar + 1
			wordlist = line.split()  # split the line into words
			parname = wordlist[0]
			self.namelist.append(parname)
			n = len(wordlist)
			m = self.npnames
			valnamelist = []
			valdict = {}
			for i in range(1,n):   # assign only those values that exist in the swmm .inp file
				if i <= m-1:
					valnamelist.append(self.pnames[i])
					valdict[self.pnames[i]] = wordlist[i]
				else:
					valdict[self.pnames[m-1]] = valdict[self.pnames[m-1]] + ' ' + wordlist[i]
			self.pardict[parname] = (valnamelist,valdict)  # dictionary contains tuples	
	def __init__(self,linelist,pnames):
		self.pnames = pnames
		self.npnames = len(self.pnames)
		self.parse(linelist)
	def output(self):
		outstr = ''
		for parname in self.namelist:
			outstr = outstr + parname + '\t'
			(valnamelist,valdict) = self.pardict[parname]
			for val in valnamelist:
				outstr = outstr + valdict[val] + ' '
			outstr = outstr + '\n'
		return outstr


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
		for parname in self.namelist:
			outstr = outstr + parname[0] + '\t' + parname[1] + '\t'
			vallist = self.pardict[parname]
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

class lid_usage(category3d):   # multiline category
	heading = '[LID_USAGE]'
	def parse(self):
		for name in self.namelist:
			vallist = self.pardict[name]
			n = len(vallist)
			m = len(self.pnames)
			self.valnamelist = []
			valdict = {}
			for i in range(0,m):   # assign only those values that exist in the swmm .inp file
				if i <= n-1:
					self.valnamelist.append(self.pnames[i])
					valdict[self.pnames[i]] = vallist[i]
				else:
					valdict[self.pnames[i]] = ' '	
			self.liddict[name] = valdict
	def __init__(self,linelist):
		self.liddict = {}
		self.pnames =  ['Number','Area','Width','InitSat','FromImp','ToPerv','RptFile','DrainTo']
		category3d.__init__(self,linelist)
		self.parse()
		self.output()
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

class raingages():
# this section will be treated as a parameter name followed by a string representing the rest of the line
	heading = '[RAINGAGES]'
	def parse(self,linelist):
		self.numpar = 0
		self.namelist = []   # list to hold parameter names in their original order
		self.pardict = {}
		for line in linelist:
			self.numpar = self.numpar + 1
			wordlist = line.split()  # split the line into words
			parname = wordlist[0]
			self.namelist.append(parname)
			n = len(wordlist)
			parval = ''
			for i in range(1,n):
				parval = parval + ' ' + wordlist[i]
			self.pardict[parname] = parval
	def __init__(self,linelist):
		self.parse(linelist)
	def output(self):
		outstr = ''
		for parname in self.namelist:
			parval = self.pardict[parname]
			outstr = outstr + parname + '\t' + parval + '\n'
		return outstr

class subcatchments(category2d):
	heading = '[SUBCATCHMENTS]'
	def __init__(self,linelist):
		pnames = ['Name', 'Rgage', 'OutID', 'Area', 'PctImperv', 'Width', 'Slope', 'Clength', 'Spack']
		category2d.__init__(self,linelist,pnames)

class subareas(category2d):
	heading = '[SUBAREAS]'
	def __init__(self,linelist):
		pnames = ['Subcat', 'Nimp', 'Nperv', 'Simp', 'Sperv', 'PctZero', 'RouteTo', 'PctRted']
		category2d.__init__(self,linelist,pnames)

class infiltration(category2d):
	heading = '[INFILTRATION]'
	def __init__(self,linelist):
		pnames = ['Subcat', 'Parameters']
		category2d.__init__(self,linelist,pnames)

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
'''
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
'''
class swmm_model:
	def __init__(self,name,section_names,sections):
		self.name = name  # name of the model
		# identify the SWMM section categories we currently support in this program:
		self.catclasses = [lid_usage]#[title,options,evaporation,raingages,subcatchments,subareas,infiltration,
		self.catdict = {}
		for swmmcat in self.catclasses:		# populate the "catdict" dictionary with swmm section object names keyed by the section header
			self.catdict[swmmcat.heading]=swmmcat  # pull the heading text string from each swmmobject class for key and use the object for the value
		self.moddict = {}  # dictionary to hold swmm section objects
		for heading in section_names:
			if heading in self.catdict:  # compares headings read in file with headings defined in swmmobject category classes
				objclass = self.catdict[heading]  # retrieve the swmm category class for each section heading found in file
				cat = objclass(sections[heading])
				self.moddict[objclass] = cat  # add this swmmcategory object to the swmm_model's dictionary
	def output(self,f):
		for obj in self.catclasses:
			cat = self.moddict[obj]
			outstr = cat.output()
			f.write(cat.heading+'\n')
			f.write(outstr)
			print cat.heading + '\n',
			print outstr,
	def change(self,catheading,objname,pname,pvalue):
		catclass = self.catdict[catheading]
		self.moddict[catclass].change(objname,pname,pvalue)

				

