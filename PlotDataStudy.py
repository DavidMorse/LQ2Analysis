import os, math, sys
import numpy as np
from array import array
from ROOT import *

# Prevents pop-up windows while saving each plot
gROOT.SetBatch(kTRUE)

gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")
gROOT.SetStyle('Plain')
gStyle.SetOptTitle(0)

gStyle.SetPadTopMargin(0.1)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.12)
gStyle.SetPadRightMargin(0.1)

# Open root file (2018 single muon data)
f_data_2016 = TFile.Open("/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2016/gmadigan/NTupleAnalyzer_nanoAOD_FullRun2DataMC_2016_2023_01_26_18_25_50/SummaryFiles/SingleMuData.root","READ")
f_data_2017 = TFile.Open("/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2017/gmadigan/NTupleAnalyzer_nanoAOD_FullRun2DataMC_2017_2023_01_26/SummaryFiles/SingleMuData.root","READ")
f_data_2018 = TFile.Open("/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2018/gmadigan/NTupleAnalyzer_nanoAOD_FullRun2DataMC_2018_2023_01_30/SummaryFiles/SingleMuData.root","READ")

# Open tree where variables are stored
t_data_2016 = f_data_2016.Get("PhysicalVariables")
t_data_2017 = f_data_2017.Get("PhysicalVariables")
t_data_2018 = f_data_2018.Get("PhysicalVariables")

def CreateHisto(name,legendname,tree,variable,binning,selection,style,label):

    binset=ConvertBinning(binning)
    n = len(binset)-1
    hout= TH1D(name,legendname,n,array("d",binset))
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

    hout.GetXaxis().SetTitle(label[0])
    hout.GetYaxis().SetTitle(label[1])
    hout.GetXaxis().SetTitleFont(42)
    hout.GetYaxis().SetTitleFont(42)
    hout.GetXaxis().SetLabelFont(42)
    hout.GetYaxis().SetLabelFont(42)
    hout.GetXaxis().SetLabelOffset(0.007)
    hout.GetYaxis().SetLabelOffset(0.007)
    hout.GetXaxis().SetLabelSize(0.06)
    hout.GetYaxis().SetLabelSize(0.06)
    
    hout.GetXaxis().SetTitleOffset(0.92)
    hout.GetYaxis().SetTitleOffset(0.92)
    hout.GetXaxis().SetTitleSize(0.06)
    hout.GetYaxis().SetTitleSize(0.06)
    
    return hout

def ConvertBinning(binning):
	binset=[]
	if len(binning)==3:
		for x in range(binning[0]+1):
			binset.append(((binning[2]-binning[1])/(1.0*binning[0]))*x*1.0+binning[1])
	else:
		binset=binning
	return binset

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
    histo.GetXaxis().SetLabelOffset(0.007)
    histo.GetYaxis().SetLabelOffset(0.007)
    histo.GetXaxis().SetLabelSize(0.0505)
    histo.GetYaxis().SetLabelSize(0.0505)

    histo.GetXaxis().SetTitleOffset(0.925)
    histo.GetYaxis().SetTitleOffset(0.9)
    histo.GetXaxis().SetTitleSize(0.07)
    histo.GetYaxis().SetTitleSize(0.07)

    return histo

def MakeBasicPlot(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale, vvscale, cutlog,version_name,plotmass):

    # Create canvas and separate into two pads: main plot and ratio sublot
    Label=[xlabel,"arbitrary units"]
    c1 = TCanvas("c1","",800,800)
    pad1 = TPad( 'pad1', 'pad1', 0.0, 0.3, 1.0, 1.0 )
    pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.3 )
    pad1.Draw()
    pad3.Draw()
    pad1.SetBottomMargin(0.0)		
    pad3.SetTopMargin(0.0)
    pad3.SetBottomMargin(0.43)
    gStyle.SetOptStat(0)

    # First create main plot
    pad1.cd()

    # Create histograms for overlay
    # Normalize distributions to 

    # Data in region A (before HEM issue)
    h_data_2016 = CreateHisto("data_2016", "data_2016", t_data_2016, recovariable, presentationbinning, selection+weight+dataHLT, style2016, Label)
    h_data_2017 = CreateHisto("data_2017", "data_2017", t_data_2017, recovariable, presentationbinning, selection+weight+dataHLT, style2017, Label)
    h_data_2018 = CreateHisto("data_2018", "data_2018", t_data_2018, recovariable, presentationbinning, selection+weight+dataHLT, style2018, Label)

    #h_data_ZCR_2016 = CreateHisto("data_ZCR_2016", "data_ZCR_2016", t_data_2016, recovariable, presentationbinning, selection+weight+dataHLT+'*(M_uu>80)*(M_uu<100)', style2016, Label)
    #h_data_ZCR_2017 = CreateHisto("data_ZCR_2017", "data_ZCR_2017", t_data_2017, recovariable, presentationbinning, selection+weight+dataHLT+'*(M_uu>80)*(M_uu<100)', style2017, Label)
    #h_data_ZCR_2018 = CreateHisto("data_ZCR_2018", "data_ZCR_2018", t_data_2018, recovariable, presentationbinning, selection+weight+dataHLT+'*(M_uu>80)*(M_uu<100)', style2018, Label)
    #
    #h_data_ttCR_2016 = CreateHisto("data_ttCR_2016", "data_ttCR_2016", t_data_2016, recovariable, presentationbinning, selection+weight+dataHLT+'*(M_uu>100)*(M_uu<250)', style2016, Label)
    #h_data_ttCR_2017 = CreateHisto("data_ttCR_2017", "data_ttCR_2017", t_data_2017, recovariable, presentationbinning, selection+weight+dataHLT+'*(M_uu>100)*(M_uu<250)', style2017, Label)
    #h_data_ttCR_2018 = CreateHisto("data_ttCR_2018", "data_ttCR_2018", t_data_2018, recovariable, presentationbinning, selection+weight+dataHLT+'*(M_uu>100)*(M_uu<250)', style2018, Label)
    #
    #int_data_ZCR_2016 = h_data_ZCR_2016.Integral(0, -1)
    #int_data_ZCR_2017 = h_data_ZCR_2017.Integral(0, -1)
    #int_data_ZCR_2018 = h_data_ZCR_2018.Integral(0, -1)
    #
    #int_data_ttCR_2016 = h_data_ttCR_2016.Integral(0, -1)
    #int_data_ttCR_2017 = h_data_ttCR_2017.Integral(0, -1)
    #int_data_ttCR_2018 = h_data_ttCR_2018.Integral(0, -1)
    #
    #ratio_ZCR_2017 = int_data_ZCR_2017/int_data_ZCR_2016
    #ratio_ZCR_2018 = int_data_ZCR_2018/int_data_ZCR_2016
    #
    #ratio_ttCR_2017 = int_data_ttCR_2017/int_data_ttCR_2016
    #ratio_ttCR_2018 = int_data_ttCR_2018/int_data_ttCR_2016
    #
    #print "2017/2016 (inside Z CR) = ", ratio_ZCR_2017
    #print "2018/2016 (inside Z CR) = ", ratio_ZCR_2018
    #
    #print "2017/2016 (inside tt-bar CR) = ", ratio_ttCR_2017
    #print "2018/2016 (inside tt-bar CR) = ", ratio_ttCR_2018

    # Add cosmetic changes to plot
    BeautifyHisto(h_data_2016,style2016,Label,"Data")

    # Draw overlay plots
    h_data_2016.Draw("lpe")
    h_data_2017.Draw("lpeSAME")
    h_data_2018.Draw("lpeSAME")

    # Set y-axis to log-scale
    c1.cd(1).SetLogy()

    # Create legend
    leg = TLegend(0.53,0.65,0.95,0.89,"","brNDC")
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(.04)
    #leg.SetHeader("Data normalized to unity","L")
    leg.AddEntry(h_data_2016,"2016 Data / 36.3 fb^{-1}","lpe")
    leg.AddEntry(h_data_2017,"2017 Data / 41.5 fb^{-1}","lpe")
    leg.AddEntry(h_data_2018,"2018 Data / 59.8 fb^{-1}","lpe")
    leg.Draw()

    # "CMS" and "Preliminary," "integrated luminosity,"" and "collision energy" headers"
    l1=TLatex()
    l1.SetTextAlign(12)
    l1.SetTextFont(42)
    l1.SetNDC()
    l1.SetTextSize(0.06)
    l2=TLatex()
    l2.SetTextAlign(12)
    l2.SetTextFont(62)
    l2.SetNDC()
    l2.SetTextSize(0.08)

    l1.DrawLatex(0.12,0.94,"#it{Preliminary}                                          (13 TeV)")
    l2.DrawLatex(0.15,0.84,"CMS")
    
    # Update the pad
    gPad.Update()
    gPad.RedrawAxis()
    
    # Set y-axis maximum and minimum values here (distribution-dependent)
    yaxismin = .13333
    #h_Data.SetMinimum(yaxismin)
    h_data_2016.SetMaximum(100*h_data_2016.GetMaximum())
	#if 'control' in tagname:
	#	h_data_2016.SetMaximum(100*h_data_2016.GetMaximum())
	#if 'St' in recovariable or 'GoodVertex' in recovariable:
	#	h_data_2016.SetMaximum(250*h_data_2016.GetMaximum())


    # Create Ratio subplot here
    pad3.cd()
    pad3.SetGrid()

    RatHistDen2017 =CreateHisto('RatHistDen2017','RatHistDen2017',t_data_2016,recovariable,presentationbinning,'0',style2017,Label)
    RatHistDen2017.Sumw2()
    RatHistNum2017 =CreateHisto('RatHistNum2017','RatHistNum2017',t_data_2017,recovariable,presentationbinning,'0',style2017,Label)
    RatHistNum2017.Sumw2()
    RatHistDen2017.Add(h_data_2016)
    RatHistNum2017.Add(h_data_2017)
    RatHistNum2017.Divide(RatHistDen2017)
    
    # Cosmetics
    RatHistNum2017.SetMaximum(1.599)#fixme was 1.499
    RatHistNum2017.SetMinimum(0.401)#fixme was 0.501
    RatHistNum2017.GetYaxis().SetTitleFont(42)
    RatHistNum2017.GetXaxis().SetTitle('')
    RatHistNum2017.GetYaxis().SetTitle('year / 2016')
    RatHistNum2017.GetXaxis().SetTitle(xlabel)
    RatHistNum2017.GetYaxis().SetTitleFont(42)
    RatHistNum2017.GetYaxis().SetTitle('year / 2016')
    RatHistNum2017.GetYaxis().SetNdivisions(308,True)
    RatHistNum2017.GetXaxis().SetTitleSize(0.14)
    RatHistNum2017.GetYaxis().SetTitleSize(.12)
    #RatHistNum2017.GetXaxis().CenterTitle()
    RatHistNum2017.GetYaxis().CenterTitle();		
    RatHistNum2017.GetXaxis().SetTitleOffset(0.)
    RatHistNum2017.GetYaxis().SetTitleOffset(.45)
    RatHistNum2017.GetYaxis().SetLabelSize(.1)
    RatHistNum2017.GetXaxis().SetLabelSize(.09)
    RatHistDen2017.SetMarkerSize(0)
    RatHistDen2017.SetMarkerColor(1)
    RatHistDen2017.SetFillColor(17)
    RatHistDen2017.SetFillStyle(3105)

    RatHistDen2018 =CreateHisto('RatHistDen2018','RatHistDen2018',t_data_2016,recovariable,presentationbinning,'0',style2018,Label)
    RatHistDen2018.Sumw2()
    RatHistNum2018 =CreateHisto('RatHistNum2018','RatHistNum2018',t_data_2018,recovariable,presentationbinning,'0',style2018,Label)
    RatHistNum2018.Sumw2()
    RatHistDen2018.Add(h_data_2016)
    RatHistNum2018.Add(h_data_2018)
    RatHistNum2018.Divide(RatHistDen2018)
    
    # Cosmetics
    RatHistNum2018.SetMaximum(1.599)#fixme was 1.499
    RatHistNum2018.SetMinimum(0.401)#fixme was 0.501
    RatHistNum2018.GetYaxis().SetTitleFont(42)
    RatHistNum2018.GetXaxis().SetTitle('')
    RatHistNum2018.GetYaxis().SetTitle('year / 2016')
    RatHistNum2018.GetXaxis().SetTitle(xlabel)
    RatHistNum2018.GetYaxis().SetTitleFont(42)
    RatHistNum2018.GetYaxis().SetTitle('year / 2016')
    RatHistNum2018.GetYaxis().SetNdivisions(308,True)
    RatHistNum2018.GetXaxis().SetTitleSize(0.14)
    RatHistNum2018.GetYaxis().SetTitleSize(.12)
    #RatHistNum2018.GetXaxis().CenterTitle()
    RatHistNum2018.GetYaxis().CenterTitle()
    RatHistNum2018.GetXaxis().SetTitleOffset(0.)
    RatHistNum2018.GetYaxis().SetTitleOffset(.45)
    RatHistNum2018.GetYaxis().SetLabelSize(.1)
    RatHistNum2018.GetXaxis().SetLabelSize(.09)
    RatHistDen2018.SetMarkerSize(0)
    RatHistDen2018.SetMarkerColor(1)
    RatHistDen2018.SetFillColor(17)
    RatHistDen2018.SetFillStyle(3105)

    # Draw ratio sublot
    for bin in range(RatHistDen2017.GetNbinsX()+1) :
        if bin==0: continue
        x2017 = RatHistDen2017.GetBinContent(bin)
        err2017 = RatHistDen2017.GetBinError(bin)
        if x2017==0: err2017=0
        else: err2017 = err2017/x2017
        x2018 = RatHistDen2018.GetBinContent(bin)
        err2018 = RatHistDen2018.GetBinError(bin)
        if x2018==0: err2018=0
        else: err2018 = err2018/x2018
        RatHistDen2017.SetBinError(bin,err2017)
        RatHistDen2017.SetBinContent(bin,1)
        RatHistDen2018.SetBinError(bin,err2018)
        RatHistDen2018.SetBinContent(bin,1)
        RatHistNum2017.Draw("lpeSAMES")
        RatHistNum2018.Draw("lpeSAMES")
        
        unity=TLine(RatHistNum2017.GetXaxis().GetXmin(), 1.0 , RatHistNum2017.GetXaxis().GetXmax(),1.0)
        unity.SetLineColor(1)
        unity.Draw("SAME")
        RatHistNum2017.Draw("lpeSAMES")
        RatHistNum2018.Draw("lpeSAMES")
    
    # Save plot as PDF
    print "Creating file "+FileDirectory+"/DataStudy_"+recovariable+"_"+tagname+".pdf..."
    c1.Print(FileDirectory+"/DataStudy_"+recovariable+"_"+tagname+".pdf")


# Filters
passfilter =  "*(Flag_goodVertices*(GoodVertexCount>=1))"
passfilter += "*(Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter)"
passfilter += "*(Flag_eeBadScFilter*Flag_EcalDeadCellTriggerPrimitiveFilter)"
passfilter += "*(Flag_globalSuperTightHalo2016Filter)"
passfilter += "*(Flag_BadPFMuonFilter)"

# Muon efficiency scale factors
doubleMuIdSF = "*mu1idSF*mu2idSF"
doubleMuIsoSF = "*mu1isoSF*mu2isoSF"
doubleMuRecoSF = "*mu1recoSF*mu2recoSF"
doublemuHLT = "*(1.0-((1.0-mu1hltSF)*(1.0-mu2hltSF)))"

# DeppJet b-tag efficiency scale factors
deepJetWPmedium = "0.2770"
bTagSFmedium = "*(1-(1-(DeepJet_jet1>"+deepJetWPmedium+")*bTagSF_jet1)*(1-(DeepJet_jet2>"+deepJetWPmedium+")*bTagSF_jet2))"
bTagSFmediumUp = "*(1-(1-(DeepJet_jet1>"+deepJetWPmedium+")*bTagSF_jet1Up)*(1-(DeepJet_jet2>"+deepJetWPmedium+")*bTagSF_jet2Up))"
bTagSFmediumDown = "*(1-(1-(DeepJet_jet1>"+deepJetWPmedium+")*bTagSF_jet1Down)*(1-(DeepJet_jet2>"+deepJetWPmedium+")*bTagSF_jet2Down))"
bTagselmedium = "*(((DeepJet_jet1>"+deepJetWPmedium+")+(DeepJet_jet2>"+deepJetWPmedium+"))>0)"

# Event weight
NormalWeightMuMu = "*(weight_topPt"+bTagSFmedium+doublemuHLT+doubleMuRecoSF+doubleMuIsoSF+doubleMuIdSF+")"

# Normalize each year to 1
lumi2016 = 36310.0
lumi2017 = 41480.0
lumi2018 = 59830.0

lumiWeight2016 = '(Flag_dataYear2016*'+str(1.0/lumi2016)+')'
lumiWeight2017 = '(Flag_dataYear2017*'+str(1.0/lumi2017)+')'
lumiWeight2018 = '(Flag_dataYear2018*'+str(1.0/lumi2018)+')'
lumiWeight = '*('+lumiWeight2016+'+'+lumiWeight2017+'+'+lumiWeight2018+')'

NormalWeightMuMu += lumiWeight

# Preselection
preselectionmumu = '((Pt_muon1>53)*(Pt_muon2>53)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3)*((MuonCountPt20+ElectronCountPt20)<3)'+bTagselmedium+')'
preselectionmumu += passfilter

# Muon triggers for data
dataHLT2016 = '(Flag_dataYear2016*((pass_HLTMu50+pass_HLTTkMu50)>0))'
dataHLT2017 = '(Flag_dataYear2017*((pass_HLTMu50+pass_HLTOldMu100+pass_HLTTkMu100)>0))'
dataHLT2018 = '(Flag_dataYear2018*((pass_HLTMu50+pass_HLTOldMu100+pass_HLTTkMu100)>0))'
dataHLT = '*('+dataHLT2016+'+'+dataHLT2017+'+'+dataHLT2018+')'

# Plotting parameters

# Cosmetics
style2016=[0,20,1.5,1,1]
style2017=[0,20,1.5,1,2]
style2018=[0,20,1.5,1,4]

# Binning
ptbinning = [53,75,105]
ptbinning2 = [53,75,105]
metbinning2 = [0,5]

stbinning = [200,225]
bosonbinning = [50,60,70,80,90,100,110,120]
bosonzoombinning_uujj_Z = [50,70,120]
bosonzoombinning_uujj_TT = [95,100]
metzoombinning_uujj_TT = [95,100]
metzoombinning_uujj_Z = [0,5,10,15,22,30,40,55,75,100]
	
bosonzoombinning_uvjj = [50,65,115]
bosonslopebinning_uvjj = [40,70,270]
massslopebining_uvjj = [25,100,600]

lqbinning = [50,60]
etabinning = [26,-2.6,2.6]
drbinning = [70,0,7]
phibinning = [26,-3.1416,3.1416]
dphibinning = [64,0,3.2]

for x in range(40):
	if ptbinning[-1] < 2000:
       		ptbinning.append(ptbinning[-1]+(ptbinning[-1] - ptbinning[-2])*1.2)
       	if ptbinning2[-1] < 700:
       		ptbinning2.append(ptbinning2[-1]+(ptbinning2[-1] - ptbinning2[-2])*1.2)
       	if metbinning2[-1] < 900:
       		metbinning2.append(metbinning2[-1]+(metbinning2[-1] - metbinning2[-2])*1.2)		
       	if stbinning[-1] < 3200:
       		stbinning.append(stbinning[-1]+(stbinning[-1] - stbinning[-2])*1.2)
       	if bosonbinning[-1]<1000:
       		bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.2 )
       	if lqbinning[-1]<2000:
       		lqbinning.append(lqbinning[-1]+(lqbinning[-1] - lqbinning[-2])*1.1)
       	if bosonzoombinning_uujj_TT[-1] < 900:
       		bosonzoombinning_uujj_TT.append(bosonzoombinning_uujj_TT[-1] + (bosonzoombinning_uujj_TT[-1] - bosonzoombinning_uujj_TT[-2])*1.25)	       	
	if metzoombinning_uujj_TT[-1] < 900:
	       	metzoombinning_uujj_TT.append(metzoombinning_uujj_TT[-1] + (metzoombinning_uujj_TT[-1] - metzoombinning_uujj_TT[-2])*1.4)
		
vbinning = [50,0,50]
nbinning = [10,0,10]
ptbinning = [round(x) for x in ptbinning]
ptbinning2 = [round(x) for x in ptbinning2]
metbinning2 = [round(x) for x in metbinning2]
stbinning = [round(x) for x in stbinning]
bosonbinning = [round(x) for x in bosonbinning]
lqbinning = [round(x) for x in lqbinning]

bjetbinning = [0,.05]
for x in range(20):
	bjetbinning.append(bjetbinning[-1]+.05)
stbinning = [280 ,300]
lqbinning = [-20,0]
for x in range(29):
	stbinning.append(stbinning[-1]+10+stbinning[-1]-stbinning[-2])
for x in range(28):
	lqbinning.append(lqbinning[-1]+5+lqbinning[-1]-lqbinning[-2])
stbinningTT = stbinning[1:20]
stbinning = stbinning[1:]
lqbinningTT = lqbinning[1:20]
lqbinning = lqbinning[1:]
bjetweightbinning = [10,.8,1.4]
bdtbinning = [40,-1,1]

bosonbinning = [50,60,70,80,90,100,110,120]
for x in range(55):
	if bosonbinning[-1]<1800:
		bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.075 )#was 1.2	       	
bosonbinning = [round(x) for x in bosonbinning]


# Z and tt background normalization scale factors (unused for data-only plots)
[[Rz_uuj,Rz_uuj_err],[Rtt_uuj,Rtt_uuj_err]]  =  [[1.298,0.016],[0.975,0.009]] #2018 stock NanoAODv7 with 1 btag (uub)
[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]]  =  [[1.298,0.017],[0.979,0.01]] #2018 stock NanoAODv7 with 1 btag (uubj) (Rz_uujj = 88% purity, Rtt_uujj = 88% purity)
Rz_uujj = "((1.164*(JetCount==2))+(1.437*(JetCount==3))+(2.023*(JetCount==4))+(2.804*(JetCount>=5)))"
Rz_uujj_err = [0.017, 0.040, 0.113, 0.335]
[Rvv_uujj,Rvv_uujj_err] = [1.366,0.11]
[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = [[1.0,0.0],[1.0,0.0]]

ResultsDir = "DataStudy"
os.system('mkdir '+ResultsDir)


# BDT Input variables
MakeBasicPlot("M_uu","M_{#mu#mu} [GeV]",bosonzoombinning_uujj_Z,preselectionmumu,NormalWeightMuMu,ResultsDir,'controlzoom_ZRegion','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("M_uu","M_{#mu#mu} [GeV]",bosonzoombinning_uujj_TT,preselectionmumu+'*(M_uu>100)*(Pt_miss>=100)',NormalWeightMuMu,ResultsDir,'controlzoom_TTRegion','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[50,0,1000],preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("M_uu","M_{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("M_jj","M_{jj} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)
MakeBasicPlot("M_uujj","M_{#mu#mujj} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,ResultsDir,'standard','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,Rvv_uujj,'','',1000)