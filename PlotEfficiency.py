import json
from ROOT import *
import math
import os 

# Step 1. Read preselection+ "clean tables" with event counts and statistical uncertainties for each year
# Step 2. Read final selection "clean tables" with event counts and statistical uncertainties for each year
# Step 3. Read preselection+ "sys tables" with systematic uncertainties for each year
# Step 4. Compute efficiencies and efficiency error
# Step 5. Plot efficiencies

#### Step 1. ####

# Here we hardcode the names of the TeX files
# To get the clean tables, run CleanTableParse.py
# To get the sys tables, SysTableParse.py
# Check the date (MM/DD/YY) below to make sure the tables are up-to-date
# Last accessed: 08/11/22

# 2016

cleanTabPresel2016 = "Results_Testing_2016_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization_Presel/CleanTable_2016.tex" # Initial events and stat error on initial events(evaluated at preselection)
cleanTabFinal2016 = "Results_Testing_2016_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization/CleanTable_2016.tex" # Final events and stat error on final events (evaluated at final selection)
sysTabPresel2016 = "Results_Testing_2016_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization_Presel/SysTables_2016.tex" # Sys error on initial events (evaluated at preselection)
sysTabEnhancedPresel2016 = "Results_Testing_2016_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization_EnhancedPresel/SysTables_2016.tex" # Sys error on final events (evaluated at enhanced selection)

# 2017

cleanTabPresel2017 = "Results_Testing_2017_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization_Presel/CleanTable_2017.tex" # Initial events and stat error on initial events (evaluated at preselection)
cleanTabFinal2017 = "Results_Testing_2017_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization/CleanTable_2017.tex" # Final events and stat error on final events (evaluated at final selection)
sysTabPresel2016 = "Results_Testing_2017_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization_Presel/SysTables_2017.tex" # Sys error on initial events (evaluated at preselection)
sysTabEnhancedPresel2017 = "Results_Testing_2017_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization_EnhancedPresel/SysTables_2017.tex" # Sys error on final events (evaluated at enhanced selection)

# 2018

cleanTabPresel2018 = "Results_Testing_2018_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization_Presel/CleanTable_2018.tex" # Initial events and stat error on initial events (evaluated at preselection)
cleanTabFinal2018 = "Results_Testing_2018_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization/CleanTable_2018.tex" # Final events and stat error on final events (evaluated at final selection)
sysTabPresel2016 = "Results_Testing_2018_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization_Presel/SysTables_2018.tex" # Sys error on initial events (evaluated at preselection)
sysTabEnhancedPresel2018 = "Results_Testing_2018_stockNanoAODv7_Run2CombBDT_FullSys_PDF/Optimization_EnhancedPresel/SysTables_2018.tex" # Sys error on final events (evaluated at enhanced selection)

# Set LQ masses, here

LQmasses = ['300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000','2100','2200','2300','2400','2500']#,'2600','2700','2800','2900','3000','3500','4000']

# Here we define functions to get events, sys errors, and stat errors
# Each function takes the filename and data type (signal or background)
# Returns a list with the values with each entry corresponding to a mass point
# For stat errors, entries are length 2 lists of the form ['up','down'] for upper and lower bounds

def GetSysFromSysTable(tableStr,dataType):
    sys = []
    if "signal" in dataType: k = 1
    if "background" in dataType: k = 2
    with open(tableStr,'r') as inTable:
        for i, line in enumerate(inTable):
            if 'Total' in line and "&" in line and "\hline" in line:
                tabEntries = line.split('&')
                for j, entry in enumerate(tabEntries):
                    if j == k: # if k == 1 gets "Signal" events, if k == 2 gets "Background" events
                        sys.append(0.01*float(entry.split('\\')[0].strip())) # Relative error
                    else: continue
    return sys

def GetEventsFromCleanTable(tableStr,dataType):
    events = []
    if "signal" in dataType: k = 1
    if "background" in dataType: k = 8
    #print 'doing',dataType
    with open(tableStr,'r') as inTable:
        for i, line in enumerate(inTable):
            if i==0: continue # Skip table header
            tabEntries = [ent.strip(r'\\') for ent in line.split('&')] # split line into each column entry
            for j, entry in enumerate(tabEntries):
                if j == k: # if k == 1 gets "Signal" events, if k == 8 gets "All BG" events
                    events.append(float(ParseSingleTableEntry(entry)[0])) # Total events
                else: continue
    return events

def GetStatsFromCleanTable(tableStr,dataType):
    stats = []
    if "signal" in dataType: k = 1
    if "background" in dataType: k = 8
    with open(tableStr,'r') as inTable:
        for i, line in enumerate(inTable):
            if i==0: continue # Skip table header
            tabEntries = [ent.strip(r'\\') for ent in line.split('&')] # split line into each column entry
            ##print tabEntries
            for j, entry in enumerate(tabEntries):
                if j == k: # if k == 1 gets "Signal" events, if k == 8 gets "All BG" events
                    events = float(ParseSingleTableEntry(entry)[0])
                    statUp = float(ParseSingleTableEntry(entry)[1].strip('-+')) # Absolute error (not relative)
                    statDown = float(ParseSingleTableEntry(entry)[2].strip('-+')) # Absolute error (not relative)
                    stats.append([statUp,statDown])
                else: continue
    return stats

def ParseSingleTableEntry(entry):

    # This function deconstructs a single LaTeX "clean table" entry, i.e., a single string between two '&' characters
    # Returns the central value (i.e., events)
    # Returns the upper and lower bounds on statistical uncertainties 
    # Returns the upper and lower bounds on systematic uncertainties

    central = entry.strip()
    statUp = '0.0'
    statDown = '0.0'
    sysUp = '0.0'
    sysDown = '0.0'
    if '$' in entry:
        splitEntry = entry.split('$') 
        central = splitEntry[0].strip()
        if len(splitEntry) == 3:
            if 'pm' in entry:
                sysUp = splitEntry[-1].strip()
                sysDown = splitEntry[-1].strip()
            elif '_' in entry and '^' in entry:
                sysUp = splitEntry[1].split('^')[-1].split('{')[1].split('}')[0].strip()
                sysDown = splitEntry[1].split('_')[-1].split('{')[1].split('}')[0].strip()
        if len(splitEntry) == 5:
            if '\pm' in entry and '_' not in entry and '^' not in entry:
                statUp = splitEntry[2].strip()
                statDown = splitEntry[2].strip()
                sysUp = splitEntry[-1].strip()
                sysDown = splitEntry[-1].strip()
            elif '\pm' in entry and '_' in entry and '^' in entry:
                if '\pm' in splitEntry[1] :
                    statUp = splitEntry[2].strip()
                    statDown = splitEntry[2].strip()
                    sysUp = splitEntry[3].split('^')[-1].split('{')[1].split('}')[0].strip()
                    sysDown = splitEntry[3].split('_')[-1].split('{')[1].split('}')[0].strip()
                elif '_' in splitEntry[1] and '^' in splitEntry[1]:
                    statUp = splitEntry[1].split('^')[-1].split('{')[1].split('}')[0].strip()
                    statDown = splitEntry[1].split('_')[-1].split('{')[1].split('}')[0].strip()
                    sysUp = splitEntry[-1].strip()
                    sysDown = splitEntry[-1].strip()
            elif '_' in entry and '^' in entry and '\pm' not in entry:
                    statUp = splitEntry[1].split('^')[-1].split('{')[1].split('}')[0].strip()
                    statDown = splitEntry[1].split('_')[-1].split('{')[1].split('}')[0].strip()
                    sysUp = splitEntry[3].split('^')[-1].split('{')[1].split('}')[0].strip()
                    sysDown = splitEntry[3].split('_')[-1].split('{')[1].split('}')[0].strip()

    return [central,statUp,statDown,sysUp,sysDown]

# This is a function to compute the efficiency
def GetEfficiency(Norig,statNorig,sysNorig,N,statN,sysN):

    if Norig > 0:
        eff = N/Norig
        statRelNorigUp = statNorig[0]/Norig
        statRelNorigDown = statNorig[1]/Norig
    else:
        eff = 0.0
        statRelNorigUp = 0.0
        statRelNorigDown = 0.0
        
    if N > 0:
        statRelNup = statN[0]/N
        statRelNdown = statN[1]/N
    else:
        statRelNup = 0.0
        statRelNdown = 0.0

    effErrUp = eff * ( 1 + math.sqrt( (sysN**2) + (sysNorig**2) + (statRelNup**2) + (statRelNorigUp**2) ) )
    effErrDown = eff * ( 1 - math.sqrt( (sysN**2) + (sysNorig**2) + (statRelNdown**2) + (statRelNorigDown**2) ) )

    return [eff,effErrUp,effErrDown]


# Here is the plotting function 
def PlotEfficiencies(efficiency2016,efficiency2017,efficiency2018):

    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt

    x = map(int, LQmasses)

    ySig2016 = []
    ySig2017 = []
    ySig2018 = []
    yBkg2016 = []
    yBkg2017 = []
    yBkg2018 = []

    effErrSig2016_up = []
    effErrSig2017_up = []
    effErrSig2018_up = []
    effErrSig2016_down = []
    effErrSig2017_down = []
    effErrSig2018_down = []
    effErrBkg2016_up = []
    effErrBkg2017_up = []
    effErrBkg2018_up = []
    effErrBkg2016_down = []
    effErrBkg2017_down = []
    effErrBkg2018_down = []

    for mass in LQmasses:
        ySig2016.append(efficiency2016[mass]["Signal"]["Eff"])
        ySig2017.append(efficiency2017[mass]["Signal"]["Eff"])
        ySig2018.append(efficiency2018[mass]["Signal"]["Eff"])
        yBkg2016.append(efficiency2016[mass]["Background"]["Eff"])
        yBkg2017.append(efficiency2017[mass]["Background"]["Eff"])
        yBkg2018.append(efficiency2018[mass]["Background"]["Eff"])

        effErrSig2016_up.append(efficiency2016[mass]["Signal"]["EffErrUp"])
        effErrSig2017_up.append(efficiency2017[mass]["Signal"]["EffErrUp"])
        effErrSig2018_up.append(efficiency2018[mass]["Signal"]["EffErrUp"])
        effErrSig2016_down.append(efficiency2016[mass]["Signal"]["EffErrDown"])
        effErrSig2017_down.append(efficiency2017[mass]["Signal"]["EffErrDown"])
        effErrSig2018_down.append(efficiency2018[mass]["Signal"]["EffErrDown"])
        effErrBkg2016_up.append(efficiency2016[mass]["Background"]["EffErrUp"])
        effErrBkg2017_up.append(efficiency2017[mass]["Background"]["EffErrUp"])
        effErrBkg2018_up.append(efficiency2018[mass]["Background"]["EffErrUp"])
        effErrBkg2016_down.append(efficiency2016[mass]["Background"]["EffErrDown"])
        effErrBkg2017_down.append(efficiency2017[mass]["Background"]["EffErrDown"])
        effErrBkg2018_down.append(efficiency2018[mass]["Background"]["EffErrDown"])
        
        
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    sig2016 = ax1.plot(x,ySig2016,'-',linewidth=1, label="2016 Signal",color='tab:red')
    sigSysUp2016 = ax1.plot(x,effErrSig2016_up,'--',linewidth=1, label="2016 Signal",color='tab:red')
    sigSysDown2016 = ax1.plot(x,effErrSig2016_down,'--',linewidth=1, label="2016 Signal",color='tab:red')

    sig2017 = ax1.plot(x,ySig2017,'-',linewidth=1, label="2017 Signal",color='tab:orange')
    sigSysUp2017 = ax1.plot(x,effErrSig2017_up,'--',linewidth=1, label="2017 Signal",color='tab:orange')
    sigSysDown2017 = ax1.plot(x,effErrSig2017_down,'--',linewidth=1, label="2017 Signal",color='tab:orange')

    sig2018 = ax1.plot(x,ySig2018,'-',linewidth=1, label="2018 Signal",color='tab:pink')
    sigSysUp2018 = ax1.plot(x,effErrSig2018_up,'--',linewidth=1, label="2018 Signal",color='tab:pink')
    sigSysDown2018 = ax1.plot(x,effErrSig2018_down,'--',linewidth=1, label="2018 Signal",color='tab:pink')


    ax2 = ax1.twinx()
    bkg2016 = ax2.plot(x,yBkg2016,'-',linewidth=1, label="2016 Background",color='tab:blue')
    bkgSysUp2016 = ax2.plot(x,effErrBkg2016_up,'--',linewidth=1, label="2016 Background",color='tab:blue')
    bkgSysDown2016 = ax2.plot(x,effErrBkg2016_down,'--',linewidth=1, label="2016 Background",color='tab:blue')

    bkg2017 = ax2.plot(x,yBkg2017,'-',linewidth=1, label="2017 Background",color='tab:green')
    bkgSysUp2017 = ax2.plot(x,effErrBkg2017_up,'--',linewidth=1, label="2017 Background",color='tab:green')
    bkgSysDown2017 = ax2.plot(x,effErrBkg2017_down,'--',linewidth=1, label="2017 Background",color='tab:green')

    bkg2018 = ax2.plot(x,yBkg2018,'-',linewidth=1, label="2018 Background",color='tab:cyan')
    bkgSysUp2018 = ax2.plot(x,effErrBkg2018_up,'--',linewidth=1, label="2018 Background",color='tab:cyan')
    bkgSysDown2018 = ax2.plot(x,effErrBkg2018_down,'--',linewidth=1, label="2018 Background",color='tab:cyan')


    ax1.set_ylabel("Signal Efficiency",fontsize=16)
    ax2.set_ylabel("Background Efficiency",fontsize=16)
    ax1.set_xlabel(r"$M_{LQ}$ [GeV]",fontsize=16)

    ax2.xaxis.major.formatter._useMathText = True
    ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    sigbkg = sig2016+bkg2016+sig2017+bkg2017+sig2018+bkg2018
    labels = [x.get_label() for x in sigbkg]
    ax1.legend(sigbkg, labels, loc=7)

    #plt.yscale(value="log")
    fig.tight_layout()
    fig.savefig("finalSelectionEfficiencies.pdf")
    plt.close(fig)

# Here we open the TeX files containing the tables, 
# extract the numbers we need, 
# and store the values in dictionaries for easier management

initSigEvents2016 = GetEventsFromCleanTable(cleanTabPresel2016,'signal')
initSigEvents2017 = GetEventsFromCleanTable(cleanTabPresel2017,'signal')
initSigEvents2018 = GetEventsFromCleanTable(cleanTabPresel2018,'signal')

initBkgEvents2016 = GetEventsFromCleanTable(cleanTabPresel2016,'background')
initBkgEvents2017 = GetEventsFromCleanTable(cleanTabPresel2017,'background')
initBkgEvents2018 = GetEventsFromCleanTable(cleanTabPresel2018,'background')

initSigStats2016 = GetStatsFromCleanTable(cleanTabPresel2016,'signal')
initSigStats2017 = GetStatsFromCleanTable(cleanTabPresel2017,'signal')
initSigStats2018 = GetStatsFromCleanTable(cleanTabPresel2018,'signal')

initBkgStats2016 = GetStatsFromCleanTable(cleanTabPresel2016,'background')
initBkgStats2017 = GetStatsFromCleanTable(cleanTabPresel2017,'background')
initBkgStats2018 = GetStatsFromCleanTable(cleanTabPresel2018,'background')

initSigSys2016 = GetSysFromSysTable(sysTabPresel2016,'signal')
initSigSys2017 = GetSysFromSysTable(sysTabPresel2017,'signal')
initSigSys2018 = GetSysFromSysTable(sysTabPresel2018,'signal')

initBkgSys2016 = GetSysFromSysTable(sysTabPresel2016,'background')
initBkgSys2017 = GetSysFromSysTable(sysTabPresel2017,'background')
initBkgSys2018 = GetSysFromSysTable(sysTabPresel2018,'background')

finalSigEvents2016 = GetEventsFromCleanTable(cleanTabFinal2016,'signal')
finalSigEvents2017 = GetEventsFromCleanTable(cleanTabFinal2017,'signal')
finalSigEvents2018 = GetEventsFromCleanTable(cleanTabFinal2018,'signal')

finalBkgEvents2016 = GetEventsFromCleanTable(cleanTabFinal2016,'background')
finalBkgEvents2017 = GetEventsFromCleanTable(cleanTabFinal2017,'background')
finalBkgEvents2018 = GetEventsFromCleanTable(cleanTabFinal2018,'background')

finalSigStats2016 = GetStatsFromCleanTable(cleanTabFinal2016,'signal')
finalSigStats2017 = GetStatsFromCleanTable(cleanTabFinal2017,'signal')
finalSigStats2018 = GetStatsFromCleanTable(cleanTabFinal2018,'signal')

finalBkgStats2016 = GetStatsFromCleanTable(cleanTabFinal2016,'background')
finalBkgStats2017 = GetStatsFromCleanTable(cleanTabFinal2017,'background')
finalBkgStats2018 = GetStatsFromCleanTable(cleanTabFinal2018,'background')

finalSigSys2016 = GetSysFromSysTable(sysTabEnhancedPresel2016,'signal')
finalSigSys2017 = GetSysFromSysTable(sysTabEnhancedPresel2017,'signal')
finalSigSys2018 = GetSysFromSysTable(sysTabEnhancedPresel2018,'signal')

finalBkgSys2016 = GetSysFromSysTable(sysTabEnhancedPresel2016,'background')
finalBkgSys2017 = GetSysFromSysTable(sysTabEnhancedPresel2017,'background')
finalBkgSys2018 = GetSysFromSysTable(sysTabEnhancedPresel2018,'background')

rawData2016 = {}
rawData2017 = {}
rawData2018 = {}

efficiency2016 = {}
efficiency2017 = {}
efficiency2018 = {}

for i, mass in enumerate(LQmasses):

    rawData2016[mass] = {"Signal": {}, "Background":{}}
    rawData2017[mass] = {"Signal": {}, "Background":{}}
    rawData2018[mass] = {"Signal": {}, "Background":{}}

    rawData2016[mass]["Signal"]["Intial Events"] = initSigEvents2016[i]
    rawData2016[mass]["Signal"]["Initial Stat Error Up"] = initSigStats2016[i][0]
    rawData2016[mass]["Signal"]["Initial Stat Error Down"] = initSigStats2016[i][1]
    rawData2016[mass]["Signal"]["Initial Sys Error"] = initSigSys2016[i]
    rawData2016[mass]["Signal"]["Final Events"] = finalSigEvents2016[i]
    rawData2016[mass]["Signal"]["Final Stat Error Up"] = finalSigStats2016[i][0]
    rawData2016[mass]["Signal"]["Final Stat Error Down"] = finalSigStats2016[i][1]
    rawData2016[mass]["Signal"]["Final Sys Error"] = finalSigSys2016[i]

    rawData2016[mass]["Background"]["Intial Events"] = initBkgEvents2016[i]
    rawData2016[mass]["Background"]["Initial Stat Error Up"] = initBkgStats2016[i][0]
    rawData2016[mass]["Background"]["Initial Stat Error Down"] = initBkgStats2016[i][1]
    rawData2016[mass]["Background"]["Initial Sys Error"] = initBkgSys2016[i]
    rawData2016[mass]["Background"]["Final Events"] = finalBkgEvents2016[i]
    rawData2016[mass]["Background"]["Final Stat Error Up"] = finalBkgStats2016[i][0]
    rawData2016[mass]["Background"]["Final Stat Error Down"] = finalBkgStats2016[i][1]
    rawData2016[mass]["Background"]["Final Sys Error"] = finalBkgSys2016[i]

    rawData2017[mass]["Signal"]["Intial Events"] = initSigEvents2017[i]
    rawData2017[mass]["Signal"]["Initial Stat Error Up"] = initSigStats2017[i][0]
    rawData2017[mass]["Signal"]["Initial Stat Error Down"] = initSigStats2017[i][1]
    rawData2017[mass]["Signal"]["Initial Sys Error"] = initSigSys2017[i]
    rawData2017[mass]["Signal"]["Final Events"] = finalSigEvents2017[i]
    rawData2017[mass]["Signal"]["Final Stat Error Up"] = finalSigStats2017[i][0]
    rawData2017[mass]["Signal"]["Final Stat Error Down"] = finalSigStats2017[i][1]
    rawData2017[mass]["Signal"]["Final Sys Error"] = finalSigSys2017[i]

    rawData2017[mass]["Background"]["Intial Events"] = initBkgEvents2017[i]
    rawData2017[mass]["Background"]["Initial Stat Error Up"] = initBkgStats2017[i][0]
    rawData2017[mass]["Background"]["Initial Stat Error Down"] = initBkgStats2017[i][1]
    rawData2017[mass]["Background"]["Initial Sys Error"] = initBkgSys2017[i]
    rawData2017[mass]["Background"]["Final Events"] = finalBkgEvents2017[i]
    rawData2017[mass]["Background"]["Final Stat Error Up"] = finalBkgStats2017[i][0]
    rawData2017[mass]["Background"]["Final Stat Error Down"] = finalBkgStats2017[i][1]
    rawData2017[mass]["Background"]["Final Sys Error"] = finalBkgSys2017[i]

    rawData2018[mass]["Signal"]["Intial Events"] = initSigEvents2018[i]
    rawData2018[mass]["Signal"]["Initial Stat Error Up"] = initSigStats2018[i][0]
    rawData2018[mass]["Signal"]["Initial Stat Error Down"] = initSigStats2018[i][1]
    rawData2018[mass]["Signal"]["Initial Sys Error"] = initSigSys2018[i]
    rawData2018[mass]["Signal"]["Final Events"] = finalSigEvents2018[i]
    rawData2018[mass]["Signal"]["Final Stat Error Up"] = finalSigStats2018[i][0]
    rawData2018[mass]["Signal"]["Final Stat Error Down"] = finalSigStats2018[i][1]
    rawData2018[mass]["Signal"]["Final Sys Error"] = finalSigSys2018[i]

    rawData2018[mass]["Background"]["Intial Events"] = initBkgEvents2018[i]
    rawData2018[mass]["Background"]["Initial Stat Error Up"] = initBkgStats2018[i][0]
    rawData2018[mass]["Background"]["Initial Stat Error Down"] = initBkgStats2018[i][1]
    rawData2018[mass]["Background"]["Initial Sys Error"] = initBkgSys2018[i]
    rawData2018[mass]["Background"]["Final Events"] = finalBkgEvents2018[i]
    rawData2018[mass]["Background"]["Final Stat Error Up"] = finalBkgStats2018[i][0]
    rawData2018[mass]["Background"]["Final Stat Error Down"] = finalBkgStats2018[i][1]
    rawData2018[mass]["Background"]["Final Sys Error"] = finalBkgSys2018[i]

    with open('eventsAndErr2016.json','w') as out2016json:
        json.dump(rawData2016,out2016json,indent=4)
    with open('eventsAndErr2017.json','w') as out2017json:
        json.dump(rawData2017,out2017json,indent=4)
    with open('eventsAndErr2018.json','w') as out2018json:
        json.dump(rawData2018,out2018json,indent=4)

    effSig2016 = GetEfficiency(initSigEvents2016[i],initSigStats2016[i],initSigSys2016[i],finalSigEvents2016[i],finalSigStats2016[i],finalSigSys2016[i])
    effSig2017 = GetEfficiency(initSigEvents2017[i],initSigStats2017[i],initSigSys2017[i],finalSigEvents2017[i],finalSigStats2017[i],finalSigSys2017[i])
    effSig2018 = GetEfficiency(initSigEvents2018[i],initSigStats2018[i],initSigSys2018[i],finalSigEvents2018[i],finalSigStats2018[i],finalSigSys2018[i])

    effBkg2017 = GetEfficiency(initBkgEvents2017[i],initBkgStats2016[i],initBkgSys2016[i],finalBkgEvents2017[i],finalBkgStats2017[i],finalBkgSys2017[i])
    effBkg2016 = GetEfficiency(initBkgEvents2016[i],initBkgStats2017[i],initBkgSys2017[i],finalBkgEvents2016[i],finalBkgStats2016[i],finalBkgSys2016[i])
    effBkg2018 = GetEfficiency(initBkgEvents2018[i],initBkgStats2018[i],initBkgSys2018[i],finalBkgEvents2018[i],finalBkgStats2018[i],finalBkgSys2018[i])

    efficiency2016[mass] = {"Signal": {}, "Background":{}}
    efficiency2017[mass] = {"Signal": {}, "Background":{}}
    efficiency2018[mass] = {"Signal": {}, "Background":{}}

    efficiency2016[mass]["Signal"]["Eff"] = effSig2016[0]
    efficiency2017[mass]["Signal"]["Eff"] = effSig2017[0]
    efficiency2018[mass]["Signal"]["Eff"] = effSig2018[0]

    efficiency2016[mass]["Signal"]["EffErrUp"] = effSig2016[1]
    efficiency2017[mass]["Signal"]["EffErrUp"] = effSig2017[1]
    efficiency2018[mass]["Signal"]["EffErrUp"] = effSig2018[1]

    efficiency2016[mass]["Signal"]["EffErrDown"] = effSig2016[2]
    efficiency2017[mass]["Signal"]["EffErrDown"] = effSig2017[2]
    efficiency2018[mass]["Signal"]["EffErrDown"] = effSig2018[2]

    efficiency2016[mass]["Background"]["Eff"] = effBkg2016[0]
    efficiency2017[mass]["Background"]["Eff"] = effBkg2017[0]
    efficiency2018[mass]["Background"]["Eff"] = effBkg2018[0]

    efficiency2016[mass]["Background"]["EffErrUp"] = effBkg2016[1]
    efficiency2017[mass]["Background"]["EffErrUp"] = effBkg2017[1]
    efficiency2018[mass]["Background"]["EffErrUp"] = effBkg2018[1]

    efficiency2016[mass]["Background"]["EffErrDown"] = effBkg2016[2]
    efficiency2017[mass]["Background"]["EffErrDown"] = effBkg2017[2]
    efficiency2018[mass]["Background"]["EffErrDown"] = effBkg2018[2]

    with open('efficiencies2016.json','w') as out2016json:
        json.dump(efficiency2016,out2016json,indent=4)
    with open('efficiencies2017.json','w') as out2017json:
        json.dump(efficiency2017,out2017json,indent=4)
    with open('efficiencies2018.json','w') as out2018json:
        json.dump(efficiency2018,out2018json,indent=4)


PlotEfficiencies(efficiency2016,efficiency2017,efficiency2018)


