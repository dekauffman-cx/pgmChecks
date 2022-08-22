#!/usr/bin/python 

from Varname import Varname
import os as o
import os.path as op
import sys
import string as strn
import re
import glob as gb



def ProcessWicStdVars(vobj):
    """ process the WicStd variables into the varDict """ 
    ProcessWicStdVars2(vobj)
    try:
        fn = "/wic/sys/php5/extensions/wicstdvxml/wicstd.vxml.php"
        fd = open(fn, 'r')
        wicPattern = re.compile(r'^\$WicStdVariables\[\]\=\"(\w+)\"')
        for line in fd: 
            if re.search(wicPattern, line) is not None:
                wicn = wicPattern.search(line).group(1)
                vobj.setVarDict(wicn)
                vobj.setVarList(wicn)
        fd.close
    except IOError:
        print "problem with the file: wicstd.vxml.php " + str(sys.exc_info())
        sys.exit()

def ProcessWicStdVars2(vobj):
    """ process the Other WicStd variables into the varDict """ 
    try:
        fn = "/wic/home/dekauffm/bin/varname.txt"
        fd = open(fn, 'r')
        for wicn in fd:
            #print wicn.rstrip() + " added"
            vobj.setVarDict(wicn.rstrip())
            vobj.setVarList(wicn.rstrip())
        fd.close()
    except IOError:
        print "problem with the file: varname.txt " + str(sys.exc_info())
        sys.exit()

def PrintFileDict(dir, vobj):
    """Prints the dictionary for each directory and file
        each file and directory has it's own dictionary which were stored in the 
        class instance of vobj.filedict - pretty complex """
    try:
        fn = GetDir(dir)
        fileName = "/wic/home/dekauffm/" + fn +  "rpt.txt" 
        keylistdir = []
        keylistfiles = []
        fw = open(fileName, 'a')
        print >> fw, ""
        print >> fw, "Variables and specific files"
        fd = vobj.getFileDict() # get a copy of the filedict from vobj
        keylistdir = fd.keys()  #gets the keys 
        keylistdir.sort()
        while len(keylistdir):  # loops through the keylist of directories.
            k = keylistdir.pop(0) # pops off the top.
            td = {}               # Creates an empty dictionary for the file level dictionary
            td = fd[k]            # assings the file level dictionary
            print >> fw, "             " + k #prints the directory.
            keylistfiles = td.keys() #gets file level keys
            keylistfiles.sort()
            while len(keylistfiles): #loops through keylistfiles
                j = keylistfiles.pop(0)
                ttd = {}                #creates an empty dict for the variables inside that file
                ttd = td[j]             #assigns to that dict 
                print >>fw, "    " + j  # prints the extracted file name
                for i in ttd.keys():    # loops through the keys in the variable level dictionary
                    print >> fw, str(i).ljust(35) + repr(ttd[i]).rjust(4) #prints the name and freq
        fw.close()
    except IOError:
        print "problem with the file: " + fileName + " " + str(sys.exc_info())

def PrintVarDict(dir, vobj):
    """Prints the Global variable dictionary for the application"""
    try:
        fn = GetDir(dir)
        fileName = "/wic/home/dekauffm/" + fn +  "rpt.txt" 
        fw = open(fileName, 'w')
        noDefList = vobj.getNoDefList()
        print >>fw, "Vars not defined in root"
        for v in noDefList:
            print >>fw, v

        print >>fw, "    Variable Name          Occurances"
        d = vobj.getVarDict()
        keylist = d.keys()
        keylist.sort()
        tmpVlist = d.values()
        valList = list()
        for v in tmpVlist:
            if v not in valList:
                valList.append(v)
        valList.sort()
        valList.reverse()
        for v in valList:
            for k in keylist:
                if d[k] == v: # printing the global vars in descending order of value 
                    print >>fw, str(k).ljust(35) + " :" + repr(d[k]).rjust(4)
        fw.close()
    except IOError:
        print "problem with the file: " + fileName + " " + str(sys.exc_info())

def CheckForVar(line, vobj):
    """ check with regexs for variable creation and assignments  
        puts the variables into vobj global dictionary 
        also returns them for inclusion in the file level dictionary
        checks to see if they've been defined by var before they've been assigned (crude)
        Most of this is kind of inside wic stuff """
    try:
		varPattern = re.compile(r'^.*<var')
		if re.search(varPattern, line) is not None:
			varName = re.compile(r'^.*<var\s+name\s*=\s*.*"(\w+)\\*".+expr\s*=.+')
			vn = varName.search(line).group(1) 
			vobj.setVarDict(vn)
			if vobj.varInVarList(vn):
                            print vn + " already exists in the list of variables"
			else:
                            vobj.setVarList(vn)
			return vn
		asPattern = re.compile(r'^.*<assign')
		if re.search(asPattern, line) is not None:
			asPattern=re.compile(r'^\s*echo\s+')
			if re.search(asPattern, line) is None:
				asName = re.compile(r'^.*<assign\s+name\s*=\s*.*[\"|\'](\w+)\\*[\"|\']\s+.+')
				asn = asName.search(line).group(1)
				if vobj.varInVarDict(asn):
                                    vobj.setVarDict(asn)
				else:
                                    vobj.varNotDefined(asn)
                                    vobj.setVarDict(asn)
                                return asn
		sessPattern = re.compile(r'^\s*\$_\w+\[\'\w+\'\]\s*=\s+.+')
		if re.search(sessPattern, line) is not None:
			sessName = re.compile(r'^\s*\$_\w+\[\'(\w+)\'\]\s*=\s+.+')
			sessn = sessName.search(line).group(1)
			if vobj.varInVarDict(sessn):
				vobj.setVarDict(sessn)
			else:
				#print sessn + ": does not exist before assignment"
				vobj.setVarDict(sessn)
			return sessn
		dataPattern = re.compile(r'^\s*\$data\[\'\w+\'\]\s*=\s+.+')
		if re.search(dataPattern, line) is not None:
			dataName = re.compile(r'^\s*\$data\[\'(\w+)\'\]\s*=\s+.+')
			datan = dataName.search(line).group(1)
			#print datan + " : testing start data"
			if vobj.varInVarDict(datan):
                            vobj.setVarDict(datan)
			else:
                            vobj.varNotDefined(datan)
                            vobj.setVarDict(datan)
			return datan
		fieldPattern = re.compile(r'^\s*<field')
		if re.search(fieldPattern, line) is not None:
			fieldName = re.compile(r'^\s*<field\s+name\s*=\s*.(\w+).\s+.+')
			fieldn = fieldName.search(line).group(1)
			if vobj.varInVarDict(fieldn):
                            vobj.setVarDict(fieldn)
			else:
                            print fieldn + ": does not exist before assignment"
                            vobj.setVarDict(fieldn)
			if vobj.varInVarList(fieldn):
                            print fieldn + " already exists in the list of variables"
			else:
                            vobj.setVarList(fieldn)
			return fieldn
		ffnPattern = re.compile(r'setFormFieldName')
		if re.search(ffnPattern, line) is not None:
			ffName = re.compile(r'^.+\(\"(\w+)\"\).*$')
			ffn = ffName.search(line).group(1)
			vobj.setVarDict(ffn)
			if vobj.varInVarList(ffn):
                            print ffn + " already exists in the list of variables"
			else:
                            vobj.setVarList(ffn)
			return ffn
    except AttributeError:
	print line  
		
def ProcessFile(f, vobj): 
    """ open reads and closes the vxml.php file. Creates the file level var dictionary """
    tmpdict = {}
    try:
        lineCtr = 0
        fi = open(f, 'r') 
        print fi.name + ": " + fi.mode
        for line in fi:
            lineCtr += 1
            #print str(lineCtr) + " ",
            x = CheckForVar(line, vobj)
            if x is not None: #checks for v
                if tmpdict.has_key(x): #if it's in the dict
                    tmpdict[x] += 1   #incements the count for that var
                else:
                    tmpdict[x] = 1   # inserts it with a count of 1
        fi.close()
    except IOError:
       print "problem with the file: " + f + " " + str(sys.exc_info())
    return tmpdict # returns the file level dictionary

def GetDir(d):
    """ returns the top level (application) directory for compare 
        (ie if given /wic/web/vxml/client/app will return app.)
        it's for a safeguard against going too far down the tree. """
    s = str(d)
    ld = s.split('/')
    if ld[-1] == '': # found that the split will make an empty list member if there is a / at the end of the dir string .. not what I wanted
        return ld[-2] 
    else:
        return ld[-1]

def GlobDev(d, vobj):
    """ iterates through the directories and files.  """
    tmpDict = {}
    t = {} 
    f = re.compile(r'^(\w+)\.vxml\.php$') # regex that is used to get the filename with out the extension 
    listdir = list()
    listfiles = list()
    listdir.extend(gb.glob('*/')) # gloh gets a list of directories for use in the second loop
    listdir.sort() 
    listfiles.extend(gb.glob('*.vxml.php')) # python glob like perl glob - gets a list of files
    root = 'root.vxml.php'
    t = ProcessFile(root, vobj) #Get global vars from the root document and returns a dict
    tmpDict['root'] = t # the file level distionary gets added to the tmpdict as root
    listfiles.remove('root.vxml.php') #don't need root any more so it is removed from the listfiles
    while len(listfiles): #runs through files remaining in the dev/ directory.
        t = {}
        file = listfiles.pop(0) #pops the topmost (zeroeth) file name off the top of the array.
        n = f.search(file).group(1) #uses regex to get the filename with out the vxml.php extension
        t = ProcessFile(file, vobj) #processes the file and and returns a variable dictionary of the file
        tmpDict[n] = t              #puts the variable dictionary in to another dictional assviated with the extracted filename
    vobj.setFileDict('dev', tmpDict) #puts the tpmdict hash into the object hash associated with the directory name

    #print fdict['dev']
    for dir in listdir: #iterates through the directories in dev
        tmpDict = {} 
        if not op.exists(dir): # looks for the directory 
            while op.exists(dir) != 1: #while it isn't finding  the directory --  == 0 would work too.
                o.chdir("../")  #changes to the parent
                fd = o.getcwd() # get the path of the parent
                if GetDir(fd) == GetDir(d): #compares the toplevel of the parent to the application
                    sys.exit() #if they're equal we exit because we don't want to go down the tree any further.
        o.chdir(dir) #if the dorectory check drops out we know that the directory exists so we change to that dir
        print dir
        listfiles.extend(gb.glob('*.vxml.php')) # get the list of files with the extension.
        listfiles.sort() 
        while len(listfiles): # when the length is zero it translates to false 
            file = listfiles.pop(0) #pops the topmost (zeroeth) file name off the top of the array
            n = f.search(file).group(1)  #uses regex to get the filename with out the vxml.php extension
            tmpDict[n] = ProcessFile(file, vobj) #processes the file and and returns a variable dictionary of the file
        vobj.setFileDict(dir, tmpDict) #puts the tpmdict hash into the object hash associated with the directory name
        

def main():
    """ Starts the process and checks for valid vxml directory. """
    if len(sys.argv) == 2:
       d = sys.argv[1]
       if op.isabs(d)== 1 and op.exists(d) == 1:
           o.chdir(d)
           if op.exists('dev/') == 1:
               o.chdir('dev/')
               v = Varname() # creates an instance of Varname class
               ProcessWicStdVars(v) # process the standard globals 
               print "we got here 1"
               GlobDev(d, v) # prepares files and directories for proceesing
               print "we got here 2"
               PrintVarDict(d, v)
               PrintFileDict(d, v)
           else:
               print "attempt to change to dev/ not successful" 
       else:
           print d + " is not a valid absolute directory \n"
    else:
       print sys.argv[1]
       print "usage is: tVarNameRpt.py /wic/web/vxml/client/application/"

main()

