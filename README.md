# pgmChecks
these are some python files I have written over the years. 
tVarNameRpt.py and Varname.py 
Variable checking code that worked on NativeVXML NOTE: these haven't been transitioned to Nerve!! 
These were written in python 2.7 so need to be upgraded to python 3

VoiceSlotChecker.py 
checks for missing voice basically
It uses a voice slot list created by grepping through the voiceslots
grep '*/*/*.wav' > voiceslot.config
put that in the app directory (ie: iva-vxml-publish-custcare)
and then:
./VoiceSlotChecker.py /path/to/app > test.whatever.

This is transitioned to python3  
