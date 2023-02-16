# pgmChecks
these are some python files I have written over the years. 

# tVarNameRpt.py and Varname.py 
Variable checking code that worked on NativeVXML NOTE: these haven't been transitioned to Nerve!! 
These were written in python 2.7 and need to be upgraded to python 3

# VoiceSlotChecker.py 
checks for missing voice
It uses a voice slot list created by grepping through the voiceslots
grep '*/*/*.wav' > voiceslot.config
put that in the app directory (ie: iva-vxml-publish-custcare)
and then:
./VoiceSlotChecker.py /path/to/app > test.whatever.

This is transitioned to python3  
Recommend that you add voiceslot.config to .gitIgnore

# SpeechToTextCompare.py Written 01/23 -- 02/23
Does an audio file transcription using google speech recognition 
Then does  a fuzzy match compare with the promptlist giving both a ratio and a partial ratio
Prints out a spreadsheet of the Text in the file, the transcript, ratio, and partial ratio.

## Python3 Modules required:
speech_recognition -- used to transcribe Voice files
openpyxl -- used to read a prompt list
SpeechObject -- (written by dekauffman -- not necessary at this point but I'll work on it )
xlsxwriter -- used to write an excel xlsx file - I think I could use openpyxl to do this but this works
python-Levenshtein -- algorithm necessary for fuzzywuzzy to work 
fuzzywuzzy -- fuzzy matches the transcription to the text in the prompt list
