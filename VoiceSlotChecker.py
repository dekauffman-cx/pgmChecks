#!/usr/bin/python3
import sys
import re
import os
import os.path as op
import glob as gb

#sketching out how this will work 

# take the file with list of voice slots read it into a hash with a value of 0
# search the application for .wav files / grab the name 
# match it to the hash with in 
# if it is found increment the hash value by 1 
# else print out an error saying that it wasn't found.
# at the end print out the hash with the values -- likely there will be two -- 1 eng and 10 span

def PrintVoiceHashByValue(vsdict):
    """ prints the voiceslot dictionary in a-z order """
    print("")
    print("   Sorted by Frequency")
    wavListV = vsdict.values()
    uniqueV = list()
    for i in wavListV:
        if i not in uniqueV:
            uniqueV.append(i)
    uniqueV.sort()
    uniqueV.reverse()
    wavListK = vsdict.keys()
    for v in uniqueV:
        for k in sorted(wavListK):
            if vsdict[k] == v:
                print(str(k).ljust(35) + repr(vsdict[k]).rjust(4))
    
def PrintVoiceHashByKey(vsdict):
    """ prints the voiceslot dictionary in a-z order """
    print("")
    print("   Sorted Order ")
    wavList = list()
    wavList = vsdict.keys()
    for k in sorted(wavList):
        print(str(k).ljust(35) + repr(vsdict[k]).rjust(4))

def PrintByOpposite(vsdict, vflist):
    """prints missing voice"""
    print("------------------------------------------------")
    print("                    missing voice")
    wavList = list()
    for i in vflist:
        if i not in vsdict.keys():
            print(i)

def PrintVoiceMissing(vsdict, vflist):
    """prints missing voice"""
    print("------------------------------------------------")
    print("               missing program voice voice slots")
    
    for i in vsdict.keys():
        if i not in vflist:
            print(i)

def OppositeRead(f,vflist):
    """take the files and build a voice list"""
    wavPattern = re.compile(r'^.+\"([a-zA-Z0-9_]+.wav)\"')
    try: 
        f3 = open(f,'r')
        for line in f3:
            if re.search(wavPattern, line) is not None:
                wavname = wavPattern.search(line).group(1)
                if not wavname in vflist:
                    vflist.append(wavname)
        f3.close()
    except IOError:
        print("issue reading file: " + f + ', ' + str(sys.exc_info()))                

def ReadFile(f,vsdict):
    """opens the file, scans through looking for voice slots  
       compares voice slot to the Voice slot Dictionary 
       prints an error if not found 
       else adds one to the dictionary value """
    wavPattern = re.compile(r'^.+\"([a-zA-Z0-9_]+.wav)\"')
    try:
        f2 = open(f,'r')
        for line in f2:
            if re.search(wavPattern, line) is not None:
                wavname = wavPattern.search(line).group(1)
                if wavname in vsdict:
                    vsdict[wavname] += 1
                else:
                    print("Voice Slot Dictionary has no voice slot " + wavname + ': ' + f)
                    #print("Check your spelling on this page: " + f)
        f2.close()
    except IOError:
        print("problem with the file: " + f + " " + str(sys.exc_info()))

def AppRead(vsdict, vflist):
    """Reads through the application directories globbing files """
    if  op.exists("vxml/") and op.isdir("vxml"):
        os.chdir("vxml/")
        listDir = list()
        listSubDir = list()
        listFiles = list()
        listDir = gb.glob("*/")
        listDir.sort()
        for dir in listDir:
            while not op.exists(dir):
                os.chdir("../")
            os.chdir(dir)
            print(dir.rjust(20))
            listSubDir = gb.glob("*/")
            for sd in listSubDir:
                print(sd.rjust(30))
                os.chdir(sd)
                listPrompts = list()
                listSays = list()
                listPrompts.append(gb.glob("prompt_*.json"))
                listSays.append(gb.glob("say_*.json"))
                masterList = listPrompts + listSays
                for arr in masterList:
                    for fileToRead in arr:
                        ReadFile(fileToRead, vsdict)
                        OppositeRead(fileToRead, vflist)
                masterList.clear()
                os.chdir("../")
        listSubDir.clear()

def HashRead(fname, vsdict):
    """Reads the file and creates a dictionary of voiceslots with 0 values. 
       Checks for duplicates and language."""  
    try:
        wavP = re.compile(r'^.+.wav')
        f1 = open(fname, 'r')
        print(f1.name)
        for line in f1:
            pathrm =  re.split(r'\/*\/*\/', line.rstrip())
            #print(pathrm)
            vsName = pathrm[-1]
            if re.search(wavP, line.rstrip()) is None:
                print("directory: " + line)
            else:
                vsName = vsName.rstrip()
                if vsName not in vsdict:
                    vsdict[vsName] = 0
        f1.close()
    except IOError:
        print("problem with the file: " + fname + " " + str(sys.exc_info()))

def main():
    """ sets up the application path to voiceslot.config file """
    if len(sys.argv) == 2:
        pathname = sys.argv[1]
        if op.isabs(pathname) == 1 and op.exists(pathname) == 1:
            os.chdir(pathname)
            fname = "voiceslot.config"
            if op.exists(fname) == 1:
                voiceHash = {}
                listVoice = list()
                HashRead(fname, voiceHash)
                AppRead(voiceHash, listVoice)
                #PrintVoiceHashByKey(voiceHash)
                #PrintVoiceHashByValue(voiceHash)
                PrintByOpposite(voiceHash, listVoice)
                PrintVoiceMissing(voiceHash, listVoice)
            else:
                print("File doesn't exist in the path.")
                print("Please check that file exists and is named voiceslot.config")
        else:
            print(pathname + " is not absolute or doesn't exist")
    else:
        print("Usage: ~dekauffm/bin/VoiceSlotChecker.py /path/to/client/application/")

main()
