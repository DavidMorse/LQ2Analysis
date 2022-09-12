import os
import sys

sysTabFile = sys.argv[1]

years = ["2016","2017","2018"]
masses = ["300","400","500","600","700","800","900","1000","1100","1200","1300","1400","1500","1600","1700","1800","1900","2000","2100","2200","2300","2400","2500","2600","2700","2800","2900","3000","3500","4000"]

sysTabRootDir = [sysTabFile.split('/')[0].split(y) for y in years if y in sysTabFile.split('/')[0]][0]
sysTabSubDir = sysTabFile.split('/')[1]
sysTabFileName = sysTabFile.split('/')[-1].split('_')[0]

sysTabAllYears = "SysTablesYearSeparated.tex"
if "Presel" in sysTabFile:
    sysTabAllYears = sysTabAllYears.split('.')[0]+"_Presel."+sysTabAllYears.split('.')[-1]

with open(sysTabAllYears,'w'):
    pass

for year in years:
    tableStrToWrite = ''
    sysTabFile = year.join(sysTabRootDir)+'/'+sysTabSubDir+'/'+sysTabFileName+'_'+year+'.tex'
    with open(sysTabFile,'r') as inSysTexFile:
        for line in inSysTexFile:
            if 'LUMI16' in line or 'LUMI17' in line or 'LUMI18' in line or 'LUMI1718' in line:
                continue
            else:
                tableStrToWrite += line
    with open(sysTabAllYears,'a') as inSysTabAllYears:
        inSysTabAllYears.write(tableStrToWrite)

fullTables = ""

for mass in masses:
    tableStr = "%"+mass+"\n"
    tableStr += r"\b"+"egin{table}[htbp]\n"
    tableStr += "\t"+r"\b"+"egin{center}\n"
    tableStr += "\t\t\caption{Systematic uncertainties and their effects on signal (Sig.) and background (Bkg.) in 2016, 2017, and 2018 for $M_{LQ}="+mass+"$~GeV final selection. All uncertainties are symmetric.}\n"
    tableStr += "\t\t"+r"\b"+"egin{tabular}{lcccccc}\n"
    tableStr += "\t\t\t\hline \hline\n"
    tableStr += "\t\t\t& \multicolumn{2}{c}{2016} & \multicolumn{2}{c}{2017} & \multicolumn{2}{c}{2018} "+r"\\"+"\n"
    tableStr += "\t\t\tSystematic & Sig. (\%) & Bkg. (\%) & Sig. (\%) & Bkg. (\%) & Sig. (\%) & Bkg. (\%) "+r"\\"+" \hline\n"
    with open(sysTabAllYears,"r") as systables:
        lines = []
        for i, line in enumerate(systables):
            if "%2016% %"+mass+"%" in line:
                start2016 = i+7
            if "%2017% %"+mass+"%" in line:
                start2017 = i+7
            if "%2018% %"+mass+"%" in line:
                start2018 = i+7
            lines.append(line)
        for sys in range(19):
            sysName = lines[start2016+sys].split("&")[0].strip().replace('16','').replace('17','').replace('18','')

            sig2016 = lines[start2016+sys].split("&")[1].strip()
            bkg2016 = lines[start2016+sys].split("&")[2].split(r"\\")[0].strip()

            sig2017 = lines[start2017+sys].split("&")[1].strip()
            bkg2017 = lines[start2017+sys].split("&")[2].split(r"\\")[0].strip()

            sig2018 = lines[start2018+sys].split("&")[1].strip()
            bkg2018 = lines[start2018+sys].split("&")[2].split(r"\\")[0].strip()
            if sys != 18:
                tableStr += "\t\t\t"+sysName+" & "+sig2016+" & "+bkg2016+" & "+sig2017+" & "+bkg2017+" & "+sig2018+" & "+bkg2018+r" \\"+"\n"
            else:
                tableStr += "\t\t\t"+sysName+" & "+sig2016+" & "+bkg2016+" & "+sig2017+" & "+bkg2017+" & "+sig2018+" & "+bkg2018+r" \\"+" \hline \hline\n"
    tableStr += "\t\t\end{tabular}\n"
    tableStr += "\t\t\label{tab:SysUncertainties_"+mass+"}\n"
    tableStr += "\t\end{center}\n"
    tableStr += "\end{table}\n"
    tableStr += "\n"

    print tableStr

    fullTables += tableStr

sysTabYearComb = "SysTablesYearCombined.tex"
if "Presel" in sysTabFile:
    sysTabYearComb = sysTabYearComb.split('.')[0]+"_Presel."+sysTabYearComb.split('.')[-1]

with open(sysTabYearComb,"w") as outFile:
    outFile.write(fullTables)