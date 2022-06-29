import os
import json

f = '/afs/cern.ch/work/g/gmadigan/CMS/Analysis/Leptoquarks/MyAnalysisNotes/AN-19-233/systematics.tex'

lqMasses = ['300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000','2100','2200','2300','2400','2500','2600','2700','2800','2900','3000','3500','4000']

i = 0
iyear = 0
years = ['2016','2017','2018']

sysDict = { '2016': {}, 
            '2017': {}, 
            '2018': {}
}

with open(f,'r') as infile:
    for line in infile:
        if 'Total' in line:

            print 'i:',i
            imass = i%30 
            print 'imass:',imass
            mass = lqMasses[imass]
            i+=1

            print 'mass',mass

            if imass==0:
                year = years[iyear]
                iyear += 1
            
            print 'year:',year

            sigTot = float(line.split('&')[1].strip())
            bkgTot = float(line.split('&')[-1].split('\\')[0].strip())

            print 'sigTot:',sigTot
            print 'bkgTot:',bkgTot

            sysDict[year][mass] = {
                'signal': sigTot,
                'background': bkgTot
            }

with open('totalSystematics.json','w') as jsonFile:
    json.dump(sysDict, jsonFile, indent=4)
            
