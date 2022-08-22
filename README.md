# pgmChecks
these are some python filee I have wwrittien over the years. 
tVarNameRpt.py and Varname.py 
Variable checking code that worhed on NativeVXML NOTE: these haven't been transitioned to Nerve!! 
These were written in python 2.7 so need to be upgraded to python 3

VoiceSlotChecker.py 
checkes for missing voice bascally
It uses a voice slot list created by grepping through the voiceslots
grep */*/*.wav > voiceslt.config
put that in the app drectory (ie: iva-vxml-publish-custcare)
and then:
./VoiceSlotChecker.py /path/to/app > test.wnatever.


This is transitioned to python3  
