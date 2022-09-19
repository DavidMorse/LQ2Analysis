import matplotlib.pyplot as plt
import json
import os
import numpy as np

masses = ['300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2100','2200','2300','2400','2500','2600','2700','2800','2900','3000','3500','4000']

for mass in masses:

    os.system('mkdir '+mass+'/plots')
    copyDataFile = mass+'/data/QuickIntegrals_GEcopies_FinalSel_M'+mass+'.json'

    with open(copyDataFile,'r') as infile:
        copyData = json.load(infile)
    
    sysDataFile = mass+'/data/SystematicResults.json'
    with open(sysDataFile,'r') as infile:
        sysData = json.load(infile)

    x = []
    bkgList = []
    sigList = []

    for icopy in range(51):
        x.append(icopy)
        sigList.append(copyData[str(icopy)]['LQuujj'+mass][0])
        bkg = copyData[str(icopy)]['ZJets'][0]
        bkg += copyData[str(icopy)]['TTBar'][0]
        bkg += copyData[str(icopy)]['SingleTop'][0]
        bkg += copyData[str(icopy)]['WJets'][0]
        bkg += copyData[str(icopy)]['DiBoson'][0]
        bkg += copyData[str(icopy)]['TTV'][0]
        bkgList.append(bkg)

    uncorrected = bkgList[50]

    bkgList = [i/uncorrected for i in bkgList]

    mean = np.mean(bkgList)
    xMeanLine = list(np.full(5000,[i*0.01 for i in range(5000)]))
    yMeanLine = list(np.full(5000,mean))

    yNomLine = list(np.full(5000,1))

    diff = str(round(sysData["Integral"]["Difference"]["Background"],2))
    sys = str(round(sysData["Systematic"]["Background"],2))

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.hist(bkgList[:-1],25)

    #ax.plot(x[:-1],bkgList[:-1],'o',color='b',label="GE copies")
    #ax.plot(xMeanLine,yMeanLine,color='b',label="GE copy mean")
    #ax.plot(xMeanLine,yNomLine,color='r',label="Uncorrected")
    #ax.plot([], [], ' ', label="Systematic = "+sys+"%")

    #ax.set_xlabel("GE scale bias copy")
    #ax.set_ylabel("Relative Events")

    ax.set_xlabel("Relative Events")
    ax.set_ylabel("GE copies")

    #ax.legend()

    ax.set_title(r"2016 Background MC with M$_{LQ}$ = "+mass+" GeV Final Selection")
    fig.savefig(mass+'/plots/validate_Integrals_hist_'+mass+'_plot.pdf')
    plt.close(fig)