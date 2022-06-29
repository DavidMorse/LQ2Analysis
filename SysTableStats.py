import sys, os 
import re
import json

cleantablefile = sys.argv[1]

years = ['2016','2017','2018']
year = [s for s in cleantablefile.split('/')[0].split('_') if s in years][0]
outPath = '/'.join(cleantablefile.split('/')[:-1])
outJson = outPath+'/CleanTableStats_'+year+'.json'

allStats = {}

with open(cleantablefile,'r') as infile:
    for i,line in enumerate(infile):
        if i == 0: continue
        splitline = line.split('&')
        mass = splitline[0].strip()
        sigStr = splitline[1]
        bkgStr = splitline[8]

        allStats[mass] = {'signal':{},'background':{}}

        if r'$\pm$' in sigStr:
            sigStat = sigStr.split(r'$\pm$')[-1].strip()
            sigStatHigh = sigStat
            sigStatLow = sigStat
        else:
            sigStat = sigStr.split("$")[1].strip()
            sigStatVals = re.findall(r'[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?', sigStat)
            sigStatHigh = str([abs(float(n)) for n in sigStatVals if '+' in n][0])
            sigStatLow = str([abs(float(n)) for n in sigStatVals if '-' in n][0])

        if bkgStr.count(r'$\pm$') == 2:
            bkgStat = bkgStr.split(r'$\pm$')[1].strip()
            bkgStatHigh = bkgStat
            bkgStatLow = bkgStat
        elif bkgStr.count(r'$\pm$') == 1:
            bkgStat = bkgStr.split("$")[1].strip()
            bkgStatVals = re.findall(r'[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?', bkgStat)
            bkgStatHigh = str([abs(float(n)) for n in bkgStatVals if '+' in n][0])
            bkgStatLow = str([abs(float(n)) for n in bkgStatVals if '-' in n][0])
        
        allStats[mass]['signal']['high'] = sigStatHigh
        allStats[mass]['signal']['low'] = sigStatLow
        allStats[mass]['background']['high'] = bkgStatHigh
        allStats[mass]['background']['low'] = bkgStatLow

with open(outJson,'w') as outf:
    json.dump(allStats,outf,indent=4)




