import os
import sys
import json

sysTabFile = sys.argv[1]

years = ["2016","2017","2018"]
masses = ["300","400","500","600","700","800","900","1000","1100","1200","1300","1400","1500","1600","1700","1800","1900","2000","2100","2200","2300","2400","2500","2600","2700","2800","2900","3000","3500","4000"]

sysTabRootDir = [sysTabFile.split('/')[0].split(y) for y in years if y in sysTabFile.split('/')[0]][0]
sysTabSubDir = sysTabFile.split('/')[1]
sysTabFileName = sysTabFile.split('/')[-1].split('_')[0]


#if "Presel" in sysTabFile:
#    sysTabAllYears = sysTabAllYears.split('.')[0]+"_Presel."+sysTabAllYears.split('.')[-1]

#with open(sysTabAllYears,'w'):
#    pass

# Compare this list to keys in sysDict (in loop below)
sysToInclude = [
    "BTAG",
    "JER",
    "JES",
    "LUMI16Uncorr",
    "LUMI17Uncorr",
    "LUMI18Uncorr",
    "LUMI1718",
    "LUMICorr",
    "MER",
    "MES",
    "MUONHLT",
    "MUONID",
    "MUONISO",
    "MUONRECO",
    "PDF",
    "PREFIRE",
    "PU",
    "SHAPETT",
    "SHAPEVV",
    "SHAPEZ",
    "TOPPT",
    "TTNORM",
    "ZNORM",
    "Total"
]


sysDict = {}
for year in years:
    
    sysDict[year] = {
        "BTAG": {"Signal": [], "Background": []},
        "JER": {"Signal": [], "Background": []},
        "JES": {"Signal": [], "Background": []},
        "LUMI16Uncorr": {"Signal": [], "Background": []},
        "LUMI17Uncorr": {"Signal": [], "Background": []},
        "LUMI18Uncorr": {"Signal": [], "Background": []},
        "LUMI1718": {"Signal": [], "Background": []},
        "LUMICorr": {"Signal": [], "Background": []},
        "MER": {"Signal": [], "Background": []},
        "MES": {"Signal": [], "Background": []},
        "MUONHLT": {"Signal": [], "Background": []},
        "MUONID": {"Signal": [], "Background": []},
        "MUONISO": {"Signal": [], "Background": []},
        "MUONRECO": {"Signal": [], "Background": []},
        "PDF": {"Signal": [], "Background": []},
        "PREFIRE": {"Signal": [], "Background": []},
        "PU": {"Signal": [], "Background": []},
        "SHAPETT": {"Signal": [], "Background": []},
        "SHAPEVV": {"Signal": [], "Background": []},
        "SHAPEZ": {"Signal": [], "Background": []},
        "TOPPT": {"Signal": [], "Background": []},
        "TTNORM": {"Signal": [], "Background": []},
        "ZNORM": {"Signal": [], "Background": []},
        "Total": {"Signal": [], "Background": []}
    }

    sysTabFile = year.join(sysTabRootDir)+'/'+sysTabSubDir+'/'+sysTabFileName+'_'+year+'.tex'
    with open(sysTabFile,'r') as inSysTexFile:
        for line in inSysTexFile:
            if "BTAG" in line: 
                sysDict[year]["BTAG"]["Signal"].append(line.split("&")[1])
                sysDict[year]["BTAG"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "JER" in line: 
                sysDict[year]["JER"]["Signal"].append(line.split("&")[1])
                sysDict[year]["JER"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "JES" in line: 
                sysDict[year]["JES"]["Signal"].append(line.split("&")[1])
                sysDict[year]["JES"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if year == '2016':
                if "LUMI16Uncorr" in line: 
                    sysDict[year]["LUMI16Uncorr"]["Signal"].append(line.split("&")[1])
                    sysDict[year]["LUMI16Uncorr"]["Background"].append(line.split("&")[2].split(r'\\')[0])
                    sysDict[year]["LUMI17Uncorr"]["Signal"].append("n/a")
                    sysDict[year]["LUMI17Uncorr"]["Background"].append("n/a")
                    sysDict[year]["LUMI18Uncorr"]["Signal"].append("n/a")
                    sysDict[year]["LUMI18Uncorr"]["Background"].append("n/a")
                    sysDict[year]["LUMI1718"]["Signal"].append("n/a")
                    sysDict[year]["LUMI1718"]["Background"].append("n/a")
            if year == '2017':
                if "LUMI17Uncorr" in line: 
                    sysDict[year]["LUMI16Uncorr"]["Signal"].append("n/a")
                    sysDict[year]["LUMI16Uncorr"]["Background"].append("n/a")
                    sysDict[year]["LUMI17Uncorr"]["Signal"].append(line.split("&")[1])
                    sysDict[year]["LUMI17Uncorr"]["Background"].append(line.split("&")[2].split(r'\\')[0])
                    sysDict[year]["LUMI18Uncorr"]["Signal"].append("n/a")
                    sysDict[year]["LUMI18Uncorr"]["Background"].append("n/a")
                if "LUMI1718" in line:
                    sysDict[year]["LUMI1718"]["Signal"].append(line.split("&")[1])
                    sysDict[year]["LUMI1718"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if year == '2018':
                if "LUMI18Uncorr" in line: 
                    sysDict[year]["LUMI16Uncorr"]["Signal"].append("n/a")
                    sysDict[year]["LUMI16Uncorr"]["Background"].append("n/a")
                    sysDict[year]["LUMI17Uncorr"]["Signal"].append("n/a")
                    sysDict[year]["LUMI17Uncorr"]["Background"].append("n/a")
                    sysDict[year]["LUMI18Uncorr"]["Signal"].append(line.split("&")[1])
                    sysDict[year]["LUMI18Uncorr"]["Background"].append(line.split("&")[2].split(r'\\')[0])
                if "LUMI1718" in line:
                    sysDict[year]["LUMI1718"]["Signal"].append(line.split("&")[1])
                    sysDict[year]["LUMI1718"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "LUMICorr" in line: 
                sysDict[year]["LUMICorr"]["Signal"].append(line.split("&")[1])
                sysDict[year]["LUMICorr"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "MER" in line: 
                sysDict[year]["MER"]["Signal"].append(line.split("&")[1])
                sysDict[year]["MER"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "MES" in line: 
                sysDict[year]["MES"]["Signal"].append(line.split("&")[1])
                sysDict[year]["MES"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "MUONHLT" in line: 
                sysDict[year]["MUONHLT"]["Signal"].append(line.split("&")[1])
                sysDict[year]["MUONHLT"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "MUONID" in line: 
                sysDict[year]["MUONID"]["Signal"].append(line.split("&")[1])
                sysDict[year]["MUONID"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "MUONISO" in line: 
                sysDict[year]["MUONISO"]["Signal"].append(line.split("&")[1])
                sysDict[year]["MUONISO"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "MUONRECO" in line: 
                sysDict[year]["MUONRECO"]["Signal"].append(line.split("&")[1])
                sysDict[year]["MUONRECO"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "PDF" in line: 
                sysDict[year]["PDF"]["Signal"].append(line.split("&")[1])
                sysDict[year]["PDF"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "PREFIRE" in line:
                if year == "2018":
                    sysDict[year]["PREFIRE"]["Signal"].append("n/a")
                    sysDict[year]["PREFIRE"]["Background"].append("n/a")
                else:
                    sysDict[year]["PREFIRE"]["Signal"].append(line.split("&")[1])
                    sysDict[year]["PREFIRE"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "PU" in line: 
                sysDict[year]["PU"]["Signal"].append(line.split("&")[1])
                sysDict[year]["PU"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "SHAPETT" in line:
                sysDict[year]["SHAPETT"]["Signal"].append("n/a")
                sysDict[year]["SHAPETT"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "SHAPEVV" in line: 
                sysDict[year]["SHAPEVV"]["Signal"].append("n/a")
                sysDict[year]["SHAPEVV"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "SHAPEZ" in line: 
                sysDict[year]["SHAPEZ"]["Signal"].append("n/a")
                sysDict[year]["SHAPEZ"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "TOPPT" in line: 
                sysDict[year]["TOPPT"]["Signal"].append("n/a")
                sysDict[year]["TOPPT"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "TTNORM" in line: 
                sysDict[year]["TTNORM"]["Signal"].append("n/a")
                sysDict[year]["TTNORM"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "ZNORM" in line: 
                sysDict[year]["ZNORM"]["Signal"].append("n/a")
                sysDict[year]["ZNORM"]["Background"].append(line.split("&")[2].split(r'\\')[0])
            if "Total" in line: 
                sysDict[year]["Total"]["Signal"].append(line.split("&")[1])
                sysDict[year]["Total"]["Background"].append(line.split("&")[2].split(r'\\')[0])


#for year in years:
#    tableStrToWrite = ''
#    sysTabFile = year.join(sysTabRootDir)+'/'+sysTabSubDir+'/'+sysTabFileName+'_'+year+'.tex'
#    with open(sysTabFile,'r') as inSysTexFile:
#        for line in inSysTexFile:
#            tableStrToWrite += line
#    with open(sysTabAllYears,'a') as inSysTabAllYears:
#        inSysTabAllYears.write(tableStrToWrite)

sysTabAllYears = "SystematicsAllYears.json"
with open(sysTabAllYears,'w') as inSysTabAllYears:
    json.dump(sysDict,inSysTabAllYears,indent=4)
#

fullTables = ""

for i, mass in enumerate(masses):
    tableStr = "%"+mass+"\n"
    tableStr += r"\b"+"egin{table}[htbp]\n"
    tableStr += "\t"+r"\b"+"egin{center}\n"
    tableStr += "\t\t\caption{Systematic uncertainties and their effects on signal (Sig.) and background (Bkg.) in 2016, 2017, and 2018 for $M_{LQ}="+mass+"$~GeV final selection. All uncertainties are symmetric.}\n"
    tableStr += "\t\t"+r"\b"+"egin{tabular}{lcccccc}\n"
    tableStr += "\t\t\t\hline \hline\n"
    tableStr += "\t\t\t& \multicolumn{2}{c}{2016} & \multicolumn{2}{c}{2017} & \multicolumn{2}{c}{2018} "+r"\\"+"\n"
    tableStr += "\t\t\tSystematic & Sig. (\%) & Bkg. (\%) & Sig. (\%) & Bkg. (\%) & Sig. (\%) & Bkg. (\%) "+r"\\"+" \hline\n"

    for j, sysName in enumerate(sysToInclude):
        sig2016 = sysDict["2016"][sysName]["Signal"][i]
        bkg2016 = sysDict["2016"][sysName]["Background"][i]
        sig2017 = sysDict["2017"][sysName]["Signal"][i]
        bkg2017 = sysDict["2017"][sysName]["Background"][i]
        sig2018 = sysDict["2018"][sysName]["Signal"][i]
        bkg2018 = sysDict["2018"][sysName]["Background"][i]
        if j < len(sysToInclude)-1:
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
#if "Presel" in sysTabFile:
#    sysTabYearComb = sysTabYearComb.split('.')[0]+"_Presel."+sysTabYearComb.split('.')[-1]

with open(sysTabYearComb,"w") as outFile:
    outFile.write(fullTables)