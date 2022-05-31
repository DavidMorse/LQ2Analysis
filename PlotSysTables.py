from matplotlib import pyplot as plt
from matplotlib.ticker import *
import numpy as np
import json
plt.rcParams['text.usetex'] = True

############################################################################################################################################################
############################################################## Get statistical uncertainties ###############################################################
############################################################################################################################################################

# 2016

# Background
statLowBkg2016 = [0.63,1.1,0.52,0.45,0.356,0.206,0.211,0.044,0.041,0.07,0.033,0.016,0.023,0.034,0.016,0.034,0.01,0.011,0.022,0.0191,0.044,0.0096,0.0119,0.69,0.011,0.068,0.01,0.0067,0.0034,0.0028]
statHighBkg2016 = [0.63,1.1,0.52,0.45,0.356,0.206,0.211,0.194,0.193,0.201,0.192,0.189,0.19,0.192,0.19,0.192,0.189,0.189,0.19,0.1898,0.194,0.1891,0.1892,0.69,0.189,0.201,0.189,0.1889,0.1889,0.1889]
eventsBkg2016 = [2.54,8.29,3.53,3.23,1.432,0.826,1.22,0.733,0.596,0.67,0.409,0.202,0.29,0.379,0.223,0.345,0.091,0.104,0.11,0.0405,0.102,0.0726,0.0845,3.05,0.057,0.168,0.054,0.031,0.0075,0.0075]

statLowBkg2016 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsBkg2016,statLowBkg2016)]
statHighBkg2016 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsBkg2016,statHighBkg2016)]

# Signal
statLowSig2016 = [410,140,44,17,6.6,2.8,1.4,0.91,0.32,0.16,0.08,0.042,0.023,0.012,0.0068,0.0,0.002,0.001,0.001,0.0,0.0002,0.0001,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
statHighSig2016 = [410,140,44,17,6.6,2.8,1.4,0.91,0.32,0.16,0.08,0.042,0.023,0.012,0.0068,0.0,0.002,0.001,0.001,0.0,0.0002,0.0001,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
eventsSig2016 = [29130,15640,5754,2363,959.4,450.2,231.1,100.94,53.07,27.29,14.088,7.501,4.031,2.169,1.1964,0.65,0.349,0.196,0.109,0.059,0.0325,0.018,0.01,0.0056,0.0,0.0,0.0,0.0,0.0,0.0]

statLowSig2016 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsSig2016,statLowSig2016)]
statHighSig2016 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsSig2016,statHighSig2016)]

# 2017

# Background
statLowBkg2017 = [0.63,1.1,0.52,0.45,0.356,0.206,0.211,0.044,0.041,0.07,0.033,0.016,0.023,0.034,0.016,0.034,0.01,0.011,0.022,0.0191,0.044,0.0096,0.0119,0.69,0.011,0.068,0.01,0.0067,0.0034,0.0028]
statHighBkg2017 = [0.63,1.1,0.52,0.45,0.356,0.206,0.211,0.194,0.193,0.201,0.192,0.189,0.19,0.192,0.19,0.192,0.189,0.189,0.19,0.1898,0.194,0.1891,0.1892,0.69,0.189,0.201,0.189,0.1889,0.1889,0.1889]
eventsBkg2017 = [2.54,8.29,3.53,3.23,1.432,0.826,1.22,0.733,0.596,0.67,0.409,0.202,0.29,0.379,0.223,0.345,0.091,0.104,0.11,0.0405,0.102,0.0726,0.0845,3.05,0.057,0.168,0.054,0.031,0.0075,0.0075]

statLowBkg2017 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsBkg2017,statLowBkg2017)]
statHighBkg2017 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsBkg2017,statHighBkg2017)]

# Signal
statLowSig2017 = [410,140,44,17,6.6,2.8,1.4,0.91,0.32,0.16,0.08,0.042,0.023,0.012,0.0068,0.0,0.002,0.001,0.001,0.0,0.0002,0.0001,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
statHighSig2017 = [410,140,44,17,6.6,2.8,1.4,0.91,0.32,0.16,0.08,0.042,0.023,0.012,0.0068,0.0,0.002,0.001,0.001,0.0,0.0002,0.0001,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
eventsSig2017 = [29130,15640,5754,2363,959.4,450.2,231.1,100.94,53.07,27.29,14.088,7.501,4.031,2.169,1.1964,0.65,0.349,0.196,0.109,0.059,0.0325,0.018,0.01,0.0056,0.0,0.0,0.0,0.0,0.0,0.0]

statLowSig2017 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsSig2017,statLowSig2017)]
statHighSig2017 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsSig2017,statHighSig2017)]

# 2018

# Background
statLowBkg2018 = [0.63,1.1,0.52,0.45,0.356,0.206,0.211,0.044,0.041,0.07,0.033,0.016,0.023,0.034,0.016,0.034,0.01,0.011,0.022,0.0191,0.044,0.0096,0.0119,0.69,0.011,0.068,0.01,0.0067,0.0034,0.0028]
statHighBkg2018 = [0.63,1.1,0.52,0.45,0.356,0.206,0.211,0.194,0.193,0.201,0.192,0.189,0.19,0.192,0.19,0.192,0.189,0.189,0.19,0.1898,0.194,0.1891,0.1892,0.69,0.189,0.201,0.189,0.1889,0.1889,0.1889]
eventsBkg2018 = [2.54,8.29,3.53,3.23,1.432,0.826,1.22,0.733,0.596,0.67,0.409,0.202,0.29,0.379,0.223,0.345,0.091,0.104,0.11,0.0405,0.102,0.0726,0.0845,3.05,0.057,0.168,0.054,0.031,0.0075,0.0075]

statLowBkg2018 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsBkg2018,statLowBkg2018)]
statHighBkg2018 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsBkg2018,statHighBkg2018)]

# Signal
statLowSig2018 = [410,140,44,17,6.6,2.8,1.4,0.91,0.32,0.16,0.08,0.042,0.023,0.012,0.0068,0.0,0.002,0.001,0.001,0.0,0.0002,0.0001,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
statHighSig2018 = [410,140,44,17,6.6,2.8,1.4,0.91,0.32,0.16,0.08,0.042,0.023,0.012,0.0068,0.0,0.002,0.001,0.001,0.0,0.0002,0.0001,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
eventsSig2018 = [29130,15640,5754,2363,959.4,450.2,231.1,100.94,53.07,27.29,14.088,7.501,4.031,2.169,1.1964,0.65,0.349,0.196,0.109,0.059,0.0325,0.018,0.01,0.0056,0.0,0.0,0.0,0.0,0.0,0.0]

statLowSig2018 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsSig2018,statLowSig2018)]
statHighSig2018 = [100.0*s/n if n > 0 else 0 for n,s in zip(eventsSig2018,statHighSig2018)]

############################################################################################################################################################
########################################################################## Setup ###########################################################################
############################################################################################################################################################

# Set lists for years, masses, systematic variations, etc.
years = ["2016","2017","2018"]
masses = ["300","400","500","600","700","800","900","1000","1100","1200","1300","1400","1500","1600","1700","1800","1900","2000","2100","2200","2300","2400","2500","2600","2700","2800","2900","3000","3500","4000"]
plotMasses = masses
massValues = [int(m) for m in plotMasses]

# Systematic variations
sysVars = ["BTAG","JER","JES","LUMI","MER","MES","MUONHLT","MUONID","MUONISO","MUONRECO","PDF","PU","TT Normalization","TT Shape","VV Shape","Z Normalization","Z Shape","Total"]
# listed in order as plotted from base to top of bar chart
sysVarsToPlot = ["Other","MUONRECO","PU","Z Shape"]
sysVarsToPlot += ["Stat High", "Stat Low"]
# When plotting, these systematic variations are grouped in one category. Makes plot cleaner.
otherSys = [sys for sys in sysVars if sys not in sysVarsToPlot and sys != "Total"]

# Define plot colors here
nColors = len(sysVars)-len(otherSys) # all variations (18) - other variations (14) - "Total" (1) + "Other" (1) = 4
colors_2016 = plt.cm.BuPu(np.linspace(0.25, 1, nColors))
colors_2017 = plt.cm.OrRd(np.linspace(0.25, 1, nColors))
colors_2018 = plt.cm.YlGn(np.linspace(0.25, 1, nColors))
colors_stat = ["red","cyan"]

colorsHist = {"2016":"blue", "2017": "red", "2018": "limegreen"}

# Establish nicknames for legends, file names, etc.
mcTypeAbr = {"signal":"sig","background":"bkg"}
sysVarAbr = {   "BTAG": "btag",
                "JER": "jer",
                "JES": "jes",
                "LUMI": "lumi",
                "MER": "mer",
                "MES": "mes",
                "MUONHLT": "muonHlt",
                "MUONID": "muonId",
                "MUONISO": "muonIso",
                "MUONRECO": "muonReco",
                "PDF": "pdf",
                "PU": "pu",
                "TT Normalization": "normTT",
                "TT Shape": "shapeTT",
                "VV Shape": "shapeVV",
                "Z Normalization": "normZ",
                "Z Shape": "shapeZ",
                "Total": "tot",
                "Other": "other"
}
sysVarLabel = { "BTAG": "b Tagging",
                "JER": "JER",
                "JES": "JES",
                "LUMI": "Lumi",
                "MER": "MER",
                "MES": "MES",
                "MUONHLT": "Muon HLT",
                "MUONID": "Muon ID",
                "MUONISO": "Muon Iso",
                "MUONRECO": "Muon Reco",
                "PDF": "PDF",
                "PU": "Pileup",
                "TT Normalization": r"$t\overline{t}$ Norm",
                "TT Shape": r"$t\overline{t}$ Shape",
                "VV Shape": "DiBoson Shape",
                "Z Normalization": "Z Norm",
                "Z Shape": "Z Shape",
                "Total": "Total",
                "Other": "Other"
}


# This dictionary will store the systematics. Format is {key=year: value = { key=sys varitation: value = { key=mass: value={ key=sig/bkg: value=systematic uncertainty } } } }
sysDict = {year:{mass:{sysVar:{} for sysVar in sysVars} for mass in masses} for year in years}

############################################################################################################################################################
################################################################### Read and ParseTables ###################################################################
############################################################################################################################################################

# Just run once. Parses tex file for systematics and loads into a JSON
# Can turn off after first run as JSON file will be loaded when needed for plotting

if False:

    # Open tex file with tables of systematics and store each line as list entry. Makes it easier to parse
    systematics = []
    with open("SysTables.tex","r") as fsystables:
        for line in fsystables:
            systematics.append(line)

    # Parse the systematics tables line by line and extract the data. Put in sysDict
    for i, line in enumerate(systematics):
        if "%" in line: 
            year = line.split("%")[1].strip()
            mass = line.split("%")[-2].strip()

        sysVar = [s for s in sysVars if s in line]

        if sysVar:
            sysVar = sysVar[0]
            sig = line.split("&")[1].strip()
            bkg = line.split("&")[2].split(r"\\")[0].strip()

            if "-" in sig:
                sig = 0.0
            else:
                sig = float(sig)

            if "-" in bkg:
                bkg = 0.0
            else:
                bkg = float(bkg)

            sysDict[year][mass][sysVar]["signal"] = sig
            sysDict[year][mass][sysVar]["background"] = bkg


    for i,mass in enumerate(masses):

        sysDict["2016"][mass]["Stat Low"] = {"signal": statLowSig2016[i], "background": statLowBkg2016[i]}
        sysDict["2017"][mass]["Stat Low"] = {"signal": statLowSig2017[i], "background": statLowBkg2017[i]}
        sysDict["2018"][mass]["Stat Low"] = {"signal": statLowSig2018[i], "background": statLowBkg2018[i]}

        sysDict["2016"][mass]["Stat High"] = {"signal": statHighSig2016[i], "background": statHighBkg2016[i]}
        sysDict["2017"][mass]["Stat High"] = {"signal": statHighSig2017[i], "background": statHighBkg2017[i]}
        sysDict["2018"][mass]["Stat High"] = {"signal": statHighSig2018[i], "background": statHighBkg2018[i]}

    with open("sysTables.json",'w') as sysJson:
        json.dump(sysDict, sysJson, indent=4)

############################################################################################################################################################
################################################################## Fill Data Dictionaries ##################################################################
############################################################################################################################################################

# Fill new dict with different structure (values in a list, for plotting)--filled to ensure list is filled in order of increasing mass
# Also add an "other" category that is the sum of a subset of systematics (smaller contributions defined in otherSys list)

with open("sysTables.json",'r') as sysJson:
    sysDict = json.load(sysJson)

sysDataDict = {}

for year in sysDict:
    sysDataDict[year] = {}
    sysDataDict[year]["Other"] = {"signal":[],"background":[]}
    for mass in massValues:
        otherSig = np.sqrt(sum( [sysDict[year][str(mass)][sys]["signal"]*sysDict[year][str(mass)][sys]["signal"] for sys in otherSys] ))
        otherBkg = np.sqrt(sum( [sysDict[year][str(mass)][sys]["background"]*sysDict[year][str(mass)][sys]["background"] for sys in otherSys] ))
    
        sysDataDict[year]["Other"]["signal"].append(otherSig)
        sysDataDict[year]["Other"]["background"].append(otherBkg)

    for sysVar in sysDict[year][plotMasses[0]]: #arbitrary mass--works as long as each mass has same set of systematics
        sysDataDict[year][sysVar] = {"signal":[],"background":[]}

        for mass in massValues:
            sysDataDict[year][sysVar]["signal"].append(sysDict[year][str(mass)][sysVar]["signal"])
            sysDataDict[year][sysVar]["background"].append(sysDict[year][str(mass)][sysVar]["background"])

############################################################################################################################################################
################################################################# Define Plotting Functions ################################################################
############################################################################################################################################################

# Plots relative uncertainty of each source for a specified year and mc type (sig/bkg) accross the LQ mass range
def PlotBarChartYear(year,mcType,sysVars,barWidth,colors,colorsStat,xaxismax,yaxismax):
    print "Plotting bar chart of "+year+" "+mcType+" systematics..."

    binning = np.arange(50,6050,100)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    y_offset = np.zeros(len(massValues))
    for i,sys in enumerate(sysVars):
        if "Stat" not in sys:
            relSys = [s*s/t if t > 0 else 0 for s,t in zip(sysDataDict[year][sys][mcType],sysDataDict[year]["Total"][mcType])]
            ax.bar(massValues, relSys, width=barWidth, bottom=y_offset, align="center", color=colors[i], label=sysVarLabel[sys])
            y_offset += relSys
    
    for sys in sysVars:
        if "Stat" in sys:
            sign = "+"
            color = "red"
            if "Low" in sys:
                sign = r"$-$"
                color = "cyan"
            stat = sysDataDict[year][sys][mcType]
            ax.hist(massValues, bins=binning, weights=stat, color=color, histtype="step", label=sign+"stat", ls="--")


    # Plotting options
    ax.set_ylabel(r"$\sigma^2/\sigma_{\rm total}$", fontsize=14)
    ax.set_xlabel("LQ Mass [GeV]", fontsize=14)

    #ax.xaxis.set_major_locator(MultipleLocator(500))
    #ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    #ax.xaxis.set_minor_locator(MultipleLocator(100))
    #
    #
    #if yaxismax < 1: ticklabstrform = '%.1f'
    #else: ticklabstrform = '%d'
    #ax.yaxis.set_major_locator(MultipleLocator(yaxismax*0.2))
    #ax.yaxis.set_major_formatter(FormatStrFormatter(ticklabstrform))
    #ax.yaxis.set_minor_locator(MultipleLocator(yaxismax*0.05))

    ax.tick_params(which='major',direction='in', length=10)
    ax.tick_params(which='minor',direction='in', length=5)

    setLog = False
    if setLog:
        ax.set_ylim([1, 1000])
        ax.set_yscale('log')
    else:
        ax.set_xlim([0, xaxismax])
        ax.set_ylim([0, yaxismax])

    plt.legend(ncol=1, title=year)

    # Save plot as a pdf
    print "Saving as SysTablesPlot_"+year+"_"+mcTypeAbr[mcType]+".pdf"
    plt.savefig("SysTablesPlot_"+year+"_"+mcTypeAbr[mcType]+".pdf")


# Plots relative uncertainty of each year for a specified systematic source and mc type (sig/bkg) accross the LQ mass range
def PlotHistVar(sysVar,mcType,colors,xaxismax,yaxismax):
    print "Plotting histogram of "+sysVar+" "+mcType+" systematics..."

    binning = np.arange(50,6050,100)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for i,year in enumerate(years):
        relSys = [s*s/t if t >0 else 0 for s,t in zip(sysDataDict[year][sysVar][mcType],sysDataDict[year]["Total"][mcType])]
        #ax.hist(massValues, bins=binning, weights=relSys, color=colors[year], histtype="step", label=year+" sys")
        ax.hist(massValues, bins=binning, weights=relSys, color=colors[year], histtype="step", label=year+" stat", ls="--")

    # Plotting options
    ax.set_ylabel(r"$\sigma^2/\sigma_{\rm total}$", fontsize=14)
    ax.set_xlabel("LQ Mass [GeV]", fontsize=14)

    ax.xaxis.set_major_locator(MultipleLocator(500))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(MultipleLocator(100))
    
    if yaxismax < 1: ticklabstrform = '%.1f'
    else: ticklabstrform = '%d'
    ax.yaxis.set_major_locator(MultipleLocator(yaxismax*0.2))
    ax.yaxis.set_major_formatter(FormatStrFormatter(ticklabstrform))
    ax.yaxis.set_minor_locator(MultipleLocator(yaxismax*0.05))

    ax.tick_params(which='major',direction='in', length=10)
    ax.tick_params(which='minor',direction='in', length=5)

    setLog = False
    if setLog:
        ax.set_ylim([1, 1000])
        ax.set_yscale('log')
    else:
        ax.set_xlim([0, xaxismax])
        ax.set_ylim([0, yaxismax])

    plt.legend(ncol=1, title=sysVarLabel[sysVar])

    # Save plot as a pdf
    print "Saving as SysTablesPlot_"+sysVarAbr[sysVar]+"_"+mcTypeAbr[mcType]+".pdf"
    plt.savefig("SysTablesPlot_"+sysVarAbr[sysVar]+"_"+mcTypeAbr[mcType]+".pdf")
    
############################################################################################################################################################
####################################################################### Plotting here ######################################################################
############################################################################################################################################################

PlotBarChartYear("2016","background",sysVarsToPlot,90,colors_2016,colors_stat,6000,1000)
#PlotBarChartYear("2017","background",sysVarsToPlot,90,colors_2017,6000,25)
#PlotBarChartYear("2018","background",sysVarsToPlot,90,colors_2018,6000,40)

#PlotHistVar("MUONRECO","background",colorsHist,6000,20)
#PlotHistVar("PU","background",colorsHist,6000,30)
#PlotHistVar("Z Shape","background",colorsHist,6000,30)
