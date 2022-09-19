import os
import sys

sysRangeTabFile = sys.argv[1]

years = ["2016","2017","2018"]
masses = ["300","400","500","600","700","800","900","1000","1100","1200","1300","1400","1500","1600","1700","1800","1900","2000","2100","2200","2300","2400","2500","2600","2700","2800","2900","3000","3500","4000"]

sysRangeTabRootDir = [sysRangeTabFile.split('/')[0].split(y) for y in years if y in sysRangeTabFile.split('/')[0]][0]
sysRangeTabSubDir = sysRangeTabFile.split('/')[1]
sysRangeTabFileName = sysRangeTabFile.split('/')[-1].split('_')[0]

sysRangeTabAllYears = "SysRangesTablesYearSeparated.tex"
if "Presel" in sysRangeTabFile:
    sysRangeTabAllYears = sysRangeTabAllYears.split('.')[0]+"_Presel."+sysRangeTabAllYears.split('.')[-1]
if "EnhancedPresel" in sysRangeTabFile:
    sysRangeTabAllYears = sysRangeTabAllYears.split('.')[0]+"_EnhancedPresel."+sysRangeTabAllYears.split('.')[-1]

with open(sysRangeTabAllYears,'w'):
    pass

for year in years:
    strToWrite = '%'+year+'\n'
    sysRangeTabFile = year.join(sysRangeTabRootDir)+'/'+sysRangeTabSubDir+'/'+sysRangeTabFileName+'_'+year+'.tex'
    with open(sysRangeTabFile,'r') as inSysTexFile:
        for line in inSysTexFile:
            strToWrite += line
    with open(sysRangeTabAllYears,'a') as inSysRangeTabAllYears:
        inSysRangeTabAllYears.write(strToWrite)

BTAG=[]
JER=[]
JES=[]
LUMI=[]
MER=[]
MES=[]
MUONHLT=[]
MUONID=[]
MUONISO=[]
MUONRECO=[]
PDF=[]
PREFIRE=[]
PU=[]
BTAG=[]
TOPPT=[]
TTNORM=[]
TTSHAPE=[]
VVSHAPE=[]
ZNORM=[]
ZSHAPE=[]

with open(sysRangeTabAllYears,'r') as inSysRangeTabAllYears:
    for i, line in enumerate(inSysRangeTabAllYears):
        if 'b-jet tagging' in line:
            BTAG.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Jet energy resolution' in line:
            JER.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Jet energy scale' in line:
            JES.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Luminosity' in line:
            LUMI.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Muon energy resolution' in line:
            MER.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Muon energy scale' in line:
            MES.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Muon trigger' in line:
            MUONHLT.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Muon identification' in line:
            MUONID.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Muon isolation' in line:
            MUONISO.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Muon reconstruction' in line:
            MUONRECO.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'PDF' in line:
            PDF.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Prefire weighting' in line:
            PREFIRE.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Pileup' in line:
            PU.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Top $p_T$ reweighting' in line:
            TOPPT.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'TT normalization' in line:
            TTNORM.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'TT shape' in line:
            TTSHAPE.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Diboson shape' in line:
            VVSHAPE.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Z normalization' in line:
            ZNORM.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        if 'Z shape' in line:
            ZSHAPE.append(line.split('&')[1].strip()+' & '+line.split('&')[2].split(r'\\')[0].strip())
        
fullSysRangeTable = ""
fullSysRangeTable += r'\begin{table}[htbp]' + '\n'
fullSysRangeTable += '\t' + r'\begin{center}' + '\n'
fullSysRangeTable += '\t\t' + r'\caption{Range of systematic uncertainties on signal (Sig.) and background (Bkg.) in 2016.}' + '\n'
fullSysRangeTable += '\t\t' + r'\begin{tabular}{lcccccc}' + '\n'
fullSysRangeTable += '\t\t\t' + r'\hline\hline' + '\n'
fullSysRangeTable += '\t\t\t' + r' & \multicolumn{2}{c}{2016 (min - max) [\%]} & \multicolumn{2}{c}{2017 (min - max) [\%]} & \multicolumn{2}{c}{2018 (min - max) [\%]}' + '\n'
fullSysRangeTable += '\t\t\t' + r'Systematic & Sig. &  Bkg. & Sig. &  Bkg. & Sig. &  Bkg.  \\ \hline' + '\n'

fullSysRangeTable += '\t\t\tb-jet tagging & ' + BTAG[0] + ' & ' + BTAG[1] + ' & ' + BTAG[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tJet energy resolution & ' + JER[0] + ' & ' + JER[1] + ' & ' + JER[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tJet energy scale & ' + JES[0] + ' & ' + JES[1] + ' & ' + JES[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tLuminosity & ' + LUMI[0] + ' & ' + LUMI[1] + ' & ' + LUMI[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tMuon energy resolution & ' + MER[0] + ' & ' + MER[1] + ' & ' + MER[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tMuon energy scale & ' + MES[0] + ' & ' + MES[1] + ' & ' + MES[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tMuon trigger & ' + MUONHLT[0] + ' & ' + MUONHLT[1] + ' & ' + MUONHLT[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tMuon identification & ' + MUONID[0] + ' & ' + MUONID[1] + ' & ' + MUONID[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tMuon isolation & ' + MUONISO[0] + ' & ' + MUONISO[1] + ' & ' + MUONISO[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tMuon reconstruction & ' + MUONRECO[0] + ' & ' + MUONRECO[1] + ' & ' + MUONRECO[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tPDF & ' + PDF[0] + ' & ' + PDF[1] + ' & ' + PDF[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tPrefire reweighting & ' + PREFIRE[0] + ' & ' + PREFIRE[1] + ' & ' + PREFIRE[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tPileup & ' + PU[0] + ' & ' + PU[1] + ' & ' + PU[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tTop pT reweighting & ' + TOPPT[0] + ' & ' + TOPPT[1] + ' & ' + TOPPT[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tTT normalization & ' + TTNORM[0] + ' & ' + TTNORM[1] + ' & ' + TTNORM[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tTT shape & ' + TTSHAPE[0] + ' & ' + TTSHAPE[1] + ' & ' + TTSHAPE[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tDiboson shape & ' + VVSHAPE[0] + ' & ' + VVSHAPE[1] + ' & ' + VVSHAPE[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tZ normalization & ' + ZNORM[0] + ' & ' + ZNORM[1] + ' & ' + ZNORM[2] + r' \\' + '\n'
fullSysRangeTable += '\t\t\tZ shape & ' + ZSHAPE[0] + ' & ' + ZSHAPE[1] + ' & ' + ZSHAPE[2] + r' \\ \hline \hline' + '\n'

fullSysRangeTable += '\t\t' + r'\end{tabular}' + '\n'
fullSysRangeTable += '\t\t' + r'\label{tab:SysRangesAll}' + '\n'
fullSysRangeTable += '\t' + r'\end{center}' + '\n'
fullSysRangeTable += r'\end{table}' + '\n'

print fullSysRangeTable


sysTabYearComb = "SysRangesYearCombined.tex"

with open(sysTabYearComb,"w") as outFile:
    outFile.write(fullSysRangeTable)