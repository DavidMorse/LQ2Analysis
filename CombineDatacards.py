from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-y", "--year", dest="year", help="option to pick running year (2016,2017,2018,comb)", metavar="YEAR")
options = parser.parse_args()
year = str(options.year)

FinalDatacard = 'Results_'+year+'_Unblinded/Final_selection/FinalCardsFinSelSysLQ_'+year+'.txt'
SysDatacard = 'Results_'+year+'_Unblinded/Enhanced_selection/FinalCardsLQ_'+year+'.txt'

SysLines = {}

with open(SysDatacard, 'r') as sysFile:
    for i,line in enumerate(sysFile):
        if 'LQ_M_' in line and '.txt' in line:
            mass = line.split('.')[0].split('_')[-1]
            SysLines[mass] = []
            print 'Getting sys for LQ mass',mass,'...'
        if 'lnN' in line: 
            SysLines[mass].append(line.strip())

FinLines = {}

with open(FinalDatacard,'r') as finFile:
    for i,line in enumerate(finFile):
        if 'LQ_M_' in line and '.txt' in line:
            mass = line.split('.')[0].split('_')[-1]
            FinLines[mass] = []
            print 'Getting rates and stats for LQ mass',mass,'...'
        if 'lnN' not in line:
            FinLines[mass].append(line.strip())

masses = ['300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000','2100','2200','2300','2400','2500','2600','2700','2800','2900','3000','3500','4000']

with open('Results_'+year+'_Unblinded/Final_selection/FinalCardsLQ_'+year+'.txt','w') as outFile:
    for mass in masses:
        rateLine = 1000000000000
        for i,finLine in enumerate(FinLines[mass]):
            print finLine
            outFile.write(finLine+'\n')
            if 'rate' in finLine:
                rateLine = i
            if i == rateLine+1:
                for sysLine in SysLines[mass]:
                    sysLine = sysLine+' '
                    if 'TOPPT' in sysLine:
                        newSysLine = sysLine.replace('2.0 ','1 ')
                    else:
                        newSysLine = sysLine
                    print newSysLine.strip()
                    outFile.write(newSysLine.strip()+'\n')





