'''#!/usr/bin/python'''
import subprocess
#subprocess.call(["ls","-l"], stdout=None,stderr=None,shell=True)
#subprocess.check_output(['ls','-l'])
output = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE).communicate()[0]