import os
import sys
import json

sysTabFile = sys.argv[1]

years = ["2016","2017","2018"]
masses = ["300","400","500","600","700","800","900","1000","1100","1200","1300","1400","1500","1600","1700","1800","1900","2000","2100","2200","2300","2400","2500","2600","2700","2800","2900","3000","3500","4000"]

sysTabRootDir = [sysTabFile.split('/')[0].split(y) for y in years if y in sysTabFile.split('/')[0]][0]
sysTabSubDir = sysTabFile.split('/')[1]
sysTabFileName = sysTabFile.split('/')[-1].split('_')[0]

sysTabAllYears = "SysTablesStatAll.json"
if "Presel" in sysTabFile:
    sysTabAllYears = sysTabAllYears.split('.')[0]+"_Presel."+sysTabAllYears.split('.')[-1]
outStatJson = {'2016':{},'2017':{},'2018':{}}

for year in years:
    sysTabFile = year.join(sysTabRootDir)+'/'+sysTabSubDir+'/'+sysTabFileName+'_'+year+'.json'
    with open(sysTabFile,'r') as inStatJson:
        outStatJson[year] = json.load(inStatJson)

with open(sysTabAllYears,'w') as statAllOutFile:
    json.dump(outStatJson,statAllOutFile,indent=4)

