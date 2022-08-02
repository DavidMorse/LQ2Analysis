from matplotlib import pyplot as plt
import sys
import numpy as np
plt.rcParams['text.usetex'] = True


inFile = sys.argv[1]

year = ''
if '2016' in inFile:year = '2016'
if '2017' in inFile:year = '2017'
if '2018' in inFile:year = '2018'
    
dataDict = {}

mass = []
sig = []
zjets = []
ttbar = []
ttv = []
diboson = []
wjets = []
singletop = []
background = []
data = []


with open(inFile) as cleanTable:
    for i,line in enumerate(cleanTable):
        if i == 0: continue
        row = [l.strip() for l in line.split('&')]
        print row
        mass.append(int(row[0].split('$')[0].strip("\\")))
        #sig.append(float(row[1].split('$')[0].strip("\\")))
        zjets.append(float(row[2].split('$')[0].strip("\\")))
        ttbar.append(float(row[3].split('$')[0].strip("\\")))
        ttv.append(float(row[4].split('$')[0].strip("\\")))
        diboson.append(float(row[5].split('$')[0].strip("\\")))
        wjets.append(float(row[6].split('$')[0].strip("\\")))
        singletop.append(float(row[7].split('$')[0].strip("\\")))
        #background.append(float(row[8].split('$')[0].strip("\\")))
        #data.append(float(row[9].split('$')[0].strip("\\")))

bkgs = [
    wjets,
    ttv,
    diboson,
    singletop,
    ttbar,
    zjets 
]

labels = [
    "W+Jets",
    r"$t\overline{t}$V",
    "VV",
    "Single Top",
    r"$t\overline{t}$",
    "Z+Jets"
]

colors = [
    "yellow",
    "lime",
    "magenta",
    "cyan",
    "blue",
    "red"
]



def PlotBarChartYear(year,masses,bkgs,barWidth,labels,colors,xaxismax,ymin,yaxismax):
    print "Plotting bar chart of "+year+" backgrounds..."

    binning = np.arange(50,6050,100)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    y_offset = np.zeros(len(masses))
    for i in range(len(bkgs)):
        print colors[i]
        #relSys = [s*s/t if t > 0 else 0 for s,t in zip(sysDataDict[year][sys][mcType],sysDataDict[year]["Total"][mcType])]
        ax.bar(masses, bkgs[i], width=barWidth, bottom=y_offset, align="center", color=colors[i], label=labels[i])
        y_offset += bkgs[i]

    # Plotting options
    ax.set_ylabel("Events", fontsize=14)
    ax.set_xlabel("LQ Mass [GeV]", fontsize=14)

    ax.tick_params(which='major',direction='in', length=10)
    ax.tick_params(which='minor',direction='in', length=5)

    setLog = True
    if setLog:
        ax.set_ylim([ymin, yaxismax])
        ax.set_yscale('log')
    else:
        ax.set_xlim([0, xaxismax])
        ax.set_ylim([0, yaxismax])

    plt.legend(ncol=1, title=year+" MC")

    # Save plot as a pdf
    print "Saving as BkgCompositonPlot_"+year+".pdf"
    plt.savefig("BkgCompositionPlot_"+year+".pdf")

PlotBarChartYear(year,mass,bkgs,100,labels,colors,6000,0.001,100)