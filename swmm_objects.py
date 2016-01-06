# AEM Modified 11/2015 to include [LID_CONTROLS] and [LID_USAGE] sections

__metaclass__ = type	# new style classes
import sys

class swmmobject:
	def parse(self,str):
		strlist = str.split()
		numlist = len(strlist)
		numnames = len(self.pnames)
		parlist = []
		if numlist <= numnames:
			for i in range(numlist):
				parlist.append(strlist[i])
			for i in range(numlist, numnames):
				parlist.append(' ')
		else:
			for i in range(numnames-1):
				parlist.append(strlist[i])
			remaining_text = ''
			for i in range(numnames-1,numlist):
				remaining_text += ' ' + strlist[i]
			parlist.append(remaining_text)
		return parlist
	def __init__(self,pvals):
		self.pdict = {}
		for i in range(len(pvals)):
			self.pdict[self.pnames[i]] = pvals[i]
	def put(self,f):
		for i in self.pnames:
			f.write("%s\t" % self.pdict[i])
		f.write("\n")
	def change(self,pname,pvalue):
		self.pdict[pname]=pvalue

class title(swmmobject):
	heading = '[TITLE]'
	name = 'Text'
	def parse(self,str):
		return([str])
	def __init__(self,str):
		self.pnames = ['Text']
		swmmobject.__init__(self,self.parse(str))
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
		pvals = self.parse(str)
		self.name = pvals[0]
		swmmobject.__init__(self,pvals)
class raingage(swmmobject):
	heading = '[RAINGAGES]'
	def __init__(self,str):
		self.pnames = ['Name', 'Form', 'Intvl', 'SCF', 'Type']
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
class lid_controls(swmmobject):
    heading = '[LID_CONTROLS]'
    def parse(self,str):
        return(str.split())
    def __init__(self,str):
        self.pnames = ['Name','Parameters']
        plist = self.parse(str)
        self.name = plist[0]
        swmmobject.__init__(self,plist)
class lid_usage(swmmobject):
    heading = '[LID_USAGE]'
    def parse(self,str):
        return(str.split())
    def __init__(self,str):
        self.pnames =  ['Subcatchment','LID_Process','Number','Area','Width','InitSat','FromImp','ToPerv','RptFile','DrainTo']
        plist = self.parse(str)
        self.name = plist[0]
        swmmobject.__init__(self,plist)

objlist = [title,option,evaporation,raingage,subcatchment,subarea,infiltration,
			junction,outfall,conduit,xsection,timeser,report,lid_controls,lid_usage]
objdict = {}
for obj in objlist:
	objdict[obj.heading]=obj

class swmmcategory:
	def __init__(self,objclass):
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
		self.name = name
		self.moddict = {}
		for head in section_names:
			objclass = objdict[head]
			cat = swmmcategory(objclass)
			active_list =[]
			for line in sections[head]:
				obj = objclass(line)
				cat.add(obj)
				active_list.append(obj.name)
			cat.setactive(active_list)
			self.moddict[objclass] = cat
	def output(self,f):
		for obj in objlist:
			cat = self.moddict[obj]
			cat.putitems(f)
	def change(self,objclass,objname,pname,pvalue):
		self.moddict[objclass].change(objname,pname,pvalue)

				

