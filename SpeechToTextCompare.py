import speech_recognition as sr
from openpyxl import load_workbook
from pathlib import Path
import os.path as op
import SpeechObject
import os
import logging, sys
import glob as gb 
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
import json
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# sketching out how this script will work 
# open prompt list with openpyxl
# Pick up the list of voice slots from the voice directory (stored locally)
# match each individual voice slot to a line in the prompt list 
#   1.  if it exists  read tte voice file intu the  recognizer and print out the speech to text 
#       compare the speech to text to the text in the prompt list to ensure accuracy 
#           (figured out how to do fuzzy matching score so we don't need an exact match -- fuzzy wuzzy will work --- low score == low match)
#   2.  if it doesn't exist in the prompt list Or the prompt list has a voice slot that is unaccounted for in the voice file directory 
#       mark it as an error and proceed to the next voice slot 
# future work on object hold strings and print out results at end..

def Compare(textOfVoice, textFromFile): 
    try:
        ratio = fuzz.ratio(textOfVoice, textFromFile)
        part_ratio = fuzz.partial_ratio(textOfVoice, textFromFile)
        return ratio, part_ratio
    except:
        print("fuzzy didn't work: " + sys.exc_info())
        
def GetRecognition(path, wav, textFromFile, so):
    try:
        d = {}
        s = sr.Recognizer()
        if wav.isFile():
            with sr.AudioFile(wav) as source:
                audio_data = s.record(source)
                textOfAudio = s.recognize_google(audio_data)
            (ratio, pr) = Compare(textOfAudio, textFromFile)

            if so.exists(path):
                d =  {wav: {"TextOfAudio": textOfAudio, "TextFromFile": textFromFile, "ratio": ratio, "partial_ratio": pr }}
                so.innerDict(path, d)
            else:
                d = {path: path}
                so.insertOuter(d)
                d = {wav: {"TextOfAudio": textOfAudio, "TextFromFile": textFromFile, "ratio": ratio, "partial_ratio": pr }}
                so.innerDict(path, d)
        else:
            raise(Exception(wav + ": not found in voice directory" + path))
    except: 
        print("Speech Recognition issue: " + sys.exc_info())

def LoadExcel(ef, so):
    try:
        dirArr = gb.glob("*/")
        wb = load_workbook(filename = ef, read_only = True)
        sheet_obj = wb.active
        numRows = sheet_obj.max_row
        rowPath = sheet_obj.cell(3, 1)        
        os.chdir(rowPath)
        for i in range(3,numRows):
            k = dirArr.index(rowPath)
            logging.debug(rowPath, dirArr[k])
            test = dirArr[k]
            if rowPath == test:               
                rVoice = sheet_obj.cell(i, 2)
                wavFile = rVoice.lstrip().rstrip() + '.wav'
                rowText = sheet_obj.cell(i, 3)
                logging.debug(rowPath, wavFile, rowText) 
                GetRecognition(rowPath ,wavFile, rowText, so)
            else:
                os.chdir("..")
                k = dirArr.index(rowPath)
                test = dirArr[k]
                os.chdir(test)
                rVoice = sheet_obj.cell(i, 2)
                wavFile = rVoice.lstrip().rstrip() + '.wav'
                rowText = sheet_obj.cell(i, 3)
                logging.debug(rowPath, wavFile, rowText) 
                GetRecognition(rowPath ,wavFile, rowText, so)
    except: 
        print("Not able to load " + ef + ': ' + sys.exc_info())
        sys.exit(1)

def do_CheckPaths(vp, ef):
    """checking paths to make sure they exist """
    if vp.isdir and ef.isfile:
        op.chdir(vp)
    else:
        sys.throw("File or voice path incorrect")             
        sys.exit(1)
def main():
    """ do checks on voice file path and xlsx file """ 
    if sys.argv == 4:
        voiceFilePath = sys.argv[1] 
        excelFile = sys.argv[2]
        do_CheckPaths(voiceFilePath, excelFile)
        so = SpeechObject.SpeechObject()
        LoadExcel(excelFile,so)
           
    else:
        print("required number of args has to be two")
        print("must have voice file path and excel file name plus directory in that order")
        sys.exit(0)
    
     