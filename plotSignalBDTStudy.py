import os, math, sys
import numpy as np
from array import array
from ROOT import *
sys.argv.append( '-b' )
gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")
gROOT.SetStyle('Plain')
gStyle.SetOptTitle(0)

gStyle.SetPadTopMargin(0.1)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.12)
gStyle.SetPadRightMargin(0.1)

Directory = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2016/gmadigan/NTupleAnalyzer_nanoAOD_RunFull2016_BDT_FullSys_PDF_stockNano_2022_05_19_19_13_13/DaveSummaryFiles'

TreeName = "PhysicalVariables"
pairLQ = {}
singleLQ = {}
Files = [ff.replace('\n','') for ff in os.popen('ls '+Directory+"| grep \".root\"").readlines()]
Masses = []
for f in Files:
    _tree = 't_'+f.split('/')[-1].replace(".root","")
    isPair = 'uujj' in _tree
    _mass = ''.join([i for i in _tree if i.isdigit()])
    _treeTmp = _tree+"_tmp"
    _prefix = ''
    #print(_tree+" = TFile.Open(\""+_prefix+Directory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
    exec (_treeTmp+" = TFile.Open(\""+_prefix+Directory+"/"+f.replace("\n","")+"\",\"READ\")")
    exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")
    if isPair:
        exec ("pairLQ[\""+_mass+"\"] = "+_treeTmp+".Get(\""+TreeName+"\")")
        Masses.append(_mass)
        #print 'mass = ',_mass
    elif not isPair:
        exec ("singleLQ[\""+_mass+"\"] = "+_treeTmp+".Get(\""+TreeName+"\")")

#print pairLQ
#print singleLQ
colorDict = {
    'kWhite':0,
    'kBlack':1,
    'kGray':920,
    'kRed':632,
    'kGreen':416,
    'kBlue':600,
    'kYellow':400,
    'kMagenta':616,
    'kCyan':432,
    'kOrange':800,
    'kSpring':820,
    'kTeal':840,
    'kAzure':860,
    'kViolet':880,
    'kPink':900
}

#colorDict = {
#    'kRed':gROOT.GetColor(kRed),
#    'kBlue':gROOT.GetColor(kBlue),
#    'kGreen':gROOT.GetColor(kGreen),
#    'kMagenta':gROOT.GetColor(kMagenta),
#    'kCyan':gROOT.GetColor(kCyan),
#    'kYellow':gROOT.GetColor(kYellow),
#    'kRed+2':gROOT.GetColor(kRed+2),
#    'kBlue+2':gROOT.GetColor(kBlue+2),
#    'kGreen+2':gROOT.GetColor(kGreen+2),
#    'kMagenta+2':gROOT.GetColor(kMagenta+2),
#    'kCyan+2':gROOT.GetColor(kCyan+2),
#    'kYellow+2':gROOT.GetColor(kYellow+2),
#    'kRed-7':gROOT.GetColor(kRed-7),
#    'kBlue-7':gROOT.GetColor(kBlue-7),
#    'kGreen-7':gROOT.GetColor(kGreen-7),
#    'kMagenta-7':gROOT.GetColor(kMagenta-7),
#    'kCyan-7':gROOT.GetColor(kCyan-7),
#    'kYellow-7':gROOT.GetColor(kYellow-7),
#    'kRed-10':gROOT.GetColor(kRed-10),
#    'kBlue-10':gROOT.GetColor(kBlue-10),
#    'kGreen-10':gROOT.GetColor(kGreen-10),
#    'kMagenta-10':gROOT.GetColor(kMagenta-10),
#    'kCyan-10':gROOT.GetColor(kCyan-10),
#    'kYellow-10':gROOT.GetColor(kYellow-10),
#    'kAzure':gROOT.GetColor(kAzure),
#    'kSpring':gROOT.GetColor(kSpring),
#    'kPink':gROOT.GetColor(kPink),
#    'kTeal':gROOT.GetColor(kTeal),
#    'kOrange':gROOT.GetColor(kOrange),
#    'kViolet':gROOT.GetColor(kViolet),
#}


def CreateHisto(name,legendname,tree,variable,binning,selection,style,label):
	binset=ConvertBinning(binning)
	n = len(binset)-1
	hout= TH1D(name,legendname,n,array('d',binset))
	hout.Sumw2()
	tree.Project(name,variable,selection)
	hout.SetFillStyle(style[0])
	hout.SetMarkerStyle(style[1])
	hout.SetMarkerSize(style[2])
	hout.SetLineWidth(style[3])
	hout.SetMarkerColor(style[4])
	hout.SetLineColor(style[4])
	hout.SetFillColor(style[4])
	hout.SetFillColor(style[4])

	# hout.SetMaximum(2.0*hout.GetMaximum())
	hout.GetXaxis().SetTitle(label[0])
	hout.GetYaxis().SetTitle(label[1])
	hout.GetXaxis().SetTitleFont(42)
	hout.GetYaxis().SetTitleFont(42)
	hout.GetXaxis().SetLabelFont(42)
	hout.GetYaxis().SetLabelFont(42)
	hout.GetXaxis().SetLabelOffset(.0015)
	hout.GetYaxis().SetLabelOffset(.64)
	hout.GetXaxis().SetLabelSize(.027)
	hout.GetYaxis().SetLabelSize(.03)

	hout.GetXaxis().SetTitleOffset(.0015)
	hout.GetYaxis().SetTitleOffset(0.92)
	hout.GetXaxis().SetTitleSize(0.036)
	hout.GetYaxis().SetTitleSize(0.036)
	#hout.GetXaxis().CenterTitle(1)
	#hout.GetYaxis().CenterTitle(1)

	return hout

def BeautifyHisto(histo,style,label,newname):
    histo.SetTitle(newname)	
    histo.SetFillStyle(style[0])
    histo.SetMarkerStyle(style[1])
    histo.SetMarkerSize(style[2])
    histo.SetLineWidth(style[3])
    histo.SetMarkerColor(style[4])
    histo.SetLineColor(style[4])
    histo.SetFillColor(style[4])
    histo.SetFillColor(style[4])
    histo.GetXaxis().SetTitleFont(42)
    histo.GetYaxis().SetTitleFont(42)
    histo.GetXaxis().SetLabelFont(42)
    histo.GetYaxis().SetLabelFont(42)
    histo.GetXaxis().SetTitle(label[0])
    histo.GetYaxis().SetTitle(label[1])
    histo.GetXaxis().SetTitle(label[0])
    histo.GetYaxis().SetTitle(label[1])
    histo.GetXaxis().SetLabelOffset(.002)
    histo.GetYaxis().SetLabelOffset(.008)
    histo.GetXaxis().SetLabelSize(.027)
    histo.GetYaxis().SetLabelSize(.035)

    histo.GetXaxis().SetTitleOffset(.975)
    histo.GetYaxis().SetTitleOffset(1.275)
    histo.GetXaxis().SetTitleSize(0.042)
    histo.GetYaxis().SetTitleSize(0.049)
    #histo.GetXaxis().CenterTitle(1)
    #histo.GetYaxis().CenterTitle(1)
    return histo

def ConvertBinning(binning):
	binset=[]
	if len(binning)==3:
		for x in range(binning[0]+1):
			binset.append(((binning[2]-binning[1])/(1.0*binning[0]))*x*1.0+binning[1])
	else:
		binset=binning
	return binset

#def MakeBasicPlot(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,cutlog,version_name,plotmass):
def MakeBasicPlot(recovariable,xlabel,binning,selection,weight,channel,lqmass):
    c1 = TCanvas("c1","",800,800)
    pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0)
    pad1.Draw()
    pad1.SetBottomMargin(0.129) #0.43 x 0.3
    pad1.SetTopMargin(0.07) #margin (0.1) x 0.7
    pad1.cd()
    gStyle.SetOptStat(0)
    #hout.SetFillStyle(style[0])
	#hout.SetMarkerStyle(style[1])
	#hout.SetMarkerSize(style[2])
	#hout.SetLineWidth(style[3])
	#hout.SetMarkerColor(style[4])
	#hout.SetLineColor(style[4])
	#hout.SetFillColor(style[4])
	#hout.SetFillColor(style[4])
    colorList = []
    histos = []
    Label=[xlabel,"Events / bin"]
    lumifb = '41.5'
    sqrts = "#sqrt{s} = 13 TeV"
    
    #plot single LQ samples
    i=0
    #color = [2,3,4,6,7,803,800-3,861]
    #color0 = [colorDict['kRed'],colorDict['kBlue'],colorDict['kGreen'],colorDict['kMagenta'],colorDict['kCyan'],colorDict['kOrange']]
    #color2 = [c+2 for c in color0]
    #color7 = [c-7 for c in color0]
    #color10 = [c-10 for c in color0]
    #coloralt = [colorDict['kAzure'],colorDict['kSpring'],colorDict['kPink'],colorDict['kTeal'],colorDict['kOrange'],colorDict['kViolet']]
    #color = color0+coloralt+color10+color2+color7
    color = [colorDict['kRed'],colorDict['kBlue'],colorDict['kGreen'],colorDict['kMagenta'],colorDict['kCyan'],colorDict['kOrange'],colorDict['kOrange']+3,colorDict['kAzure']+1]
    #masses = ['500','1000','1500','2000','2500','3000','3500','4000']
    masses = ['300','600','1000','1500','2000','3000','4000']
    if lqmass not in masses:
        masses.append(lqmass)
    #['300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000','2100','2200','2300','2400','2500','2600','2700','2800','2900','3000','3500','4000']#['300','600','1000','1500','2000']
    
    for mass in masses:
        print "Using color ",color[i]
        LQstyle=[1,20,0.0001,2,color[i]]
        if channel == 'uujj':
            tree = pairLQ[mass]
        elif channel == 'uuj':
            tree = singleLQ[mass]
        #hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',t_W,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
        histos.append(CreateHisto('hs_LQ'+channel+mass,mass,tree,recovariable,binning,selection,LQstyle,Label))
        histos[i].SetMaximum(histos[i].GetMaximum()*2)
        BeautifyHisto(histos[i],LQstyle,Label,mass)
        if i==0:histos[0].Draw("HIST")
        else:histos[i].Draw("HISTSAME")
        i+=1
    
    c1.cd(1)

    l1=TLatex()
    l1.SetTextAlign(12)
    l1.SetTextFont(42)
    l1.SetNDC()
    l1.SetTextSize(0.042)#.06
    l2=TLatex()
    l2.SetTextAlign(12)
    l2.SetTextFont(62)
    l2.SetNDC()
    l2.SetTextSize(0.056)#.08
    #l1.DrawLatex(0.12,.958,"#it{Preliminary}                           "+lumifb+" fb^{-1} (13 TeV)")
    #l2.DrawLatex(0.15,0.888,"CMS")

    #c1.cd(1).SetLogy()
    gPad.Update()
    gPad.RedrawAxis()

    leg = TLegend(0.2,0.4,0.6,0.89,"","brNDC")
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(.018)
    if channel == 'uujj':legchan = 'pair LQ'
    elif channel == 'uuj':legchan = 'single LQ'
    for i in range(len(masses)):
        leg.AddEntry(histos[i],'LQ, M = '+masses[i]+' GeV', "f")
    leg.Draw()

    c1.Print(ResultsDir+'/Plots/SignalBDTStudy/LQ_'+channel+'_'+recovariable+'.pdf')

def main():

    ResultsDir = "/afs/cern.ch/work/g/gmadigan/CMS/Analysis/Leptoquarks/MakeTreesStockNanoAODv6_2/LQ2Analysis13TeV/Results_Testing_2016_stockNanoAODv7_Run2CombBDT_FullSys_PDF"

    os.system('mkdir '+ResultsDir+'/Plots')
    os.system('mkdir '+ResultsDir+'/Plots/SignalBDTStudy')

    #lqbinning = [-20,0]
    #for x in range(36):#was 22 then 28
        #lqbinning.append(lqbinning[-1]+5+lqbinning[-1]-lqbinning[-2])
    lqbinning = []
    for x in range(41):
        lqbinning.append(-1+(x*0.05))
    print "binning:",lqbinning
    selection = ''
    weight = ''

    #MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,selection,weight,'uujj',Masses)
    masses = ['300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000','2100','2200','2300','2400','2500','2600','2700','2800','2900','3000','3500','4000']
    for lqmass in masses:
        MakeBasicPlot("LQToBMu_pair_uubj_BDT_discrim_M"+lqmass,"BDT score (M_{LQ} = "+lqmass+" GeV)",lqbinning,selection,weight,'uujj',lqmass)

    #MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,selection,weight,'uujj',Masses)
    #MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,selection,weight,'uuj',Masses)

main()