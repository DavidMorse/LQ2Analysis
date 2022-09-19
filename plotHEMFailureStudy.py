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

NormalDirectory = "/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2018/gmadigan/NTupleAnalyzer_nanoAOD_RunFull2018_BDT_FullSys_PDF_stockNano_2022_05_24_19_50_25/SummaryFiles/"

ResultsDir = "/afs/cern.ch/work/g/gmadigan/CMS/Analysis/Leptoquarks/MakeTreesStockNanoAODv6_2/LQ2Analysis13TeV/Results_Testing_2018_stockNanoAODv7_Run2CombBDT_FullSys_PDF"

# Open root file (2018 single muon data)
f_data = TFile.Open(NormalDirectory+"SingleMuData.root","READ")

# Open tree where variables are stored
t_data = f_data.Get("PhysicalVariables")

# Define all functions here
def blind(h,name,num,tag,chan):
	blindstart = 9999
	if name == 'M_uu':
		blindstart = 300
	elif 'St' in name and 'uujj' in chan:
		blindstart = 1500
	elif 'uujj2' in name:
		blindstart = 800
	elif ('M_uu' in name and 'uujj2' not in name) or 'Pt_muon1' in name or 'Pt_miss' in name or 'MT_uv' in name:
		blindstart = 800
	elif 'Pt_muon2' in name:
		blindstart=300
	elif 'BDT' in name:
		blindstart=0
	if 'final' in tag:
		blindstart=0
	for bin in range(h.GetNbinsX()):
		if h.GetBinLowEdge(bin+1)>blindstart:
			if num==1:
				h.SetBinContent(bin+1,0.0)
				h.SetBinError(bin+1,0.0)
			if num==2 or num==3:
				h.SetBinContent(bin+1,-50.0)
				h.SetBinError(bin+1,0.0)
			if 'final' in tag:
				h.SetBinContent(bin+1,.0001)
				h.SetBinError(bin+1,0.0)

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

def MakeBasicPlot(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,cutlog,version_name,plotmass):

    # Create canvas and separate into two pads: main plot and ratio sublot
    Label=[xlabel,"Events / bin"]
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
    h_Data_A=CreateHisto("h_Data_A","Data",t_data,recovariable,presentationbinning,selection+dataHLT+HEM1516Failure_A_sel,DataRecoStyle1,Label)

    # Data in region B (after HEM issue)
    h_Data_B=CreateHisto("h_Data_B","Data",t_data,recovariable,presentationbinning,selection+dataHLT+HEM1516Failure_B_sel,DataRecoStyle2,Label)

    # Normalize distributions to 1 for shape comparison
    int_Data_A = h_Data_A.Integral()
    int_Data_B = h_Data_B.Integral()
    h_Data_A.Scale(1.0/int_Data_A)
    h_Data_B.Scale(1.0/int_Data_B)

    # Blind data (where necessary)
    blinded=True
    if blinded:
        blind(h_Data_A,recovariable,1,tagname,channel)
        blind(h_Data_B,recovariable,1,tagname,channel)

    # Add cosmetic changes to plot
    BeautifyHisto(h_Data_A,DataRecoStyle1,Label,"Data")

    # Draw overlay plots
    h_Data_A.Draw("E0")
    h_Data_B.Draw("E0SAME")

    # Set y-axis to log-scale
    c1.cd(1).SetLogy()

    # Create legend
    leg = TLegend(0.33,0.65,0.79,0.89,"","brNDC");
    leg.SetTextFont(42);
    leg.SetFillColor(0);
    leg.SetFillStyle(0);
    leg.SetBorderSize(0);
    leg.SetTextSize(.05)
    leg.AddEntry(h_Data_A,"Data (norm=1), < run 319077","lep");
    leg.AddEntry(h_Data_B,"Data (norm=1), >= run 319077","lep");
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

    l1.DrawLatex(0.12,0.94,"#it{Preliminary}                           "+lumiInvfb+" fb^{-1} (13 TeV)")
    l2.DrawLatex(0.15,0.84,"CMS")
    
    # Update the pad
    gPad.Update()
    gPad.RedrawAxis()
    
    # Set y-axis maximum and minimum values here (distribution-dependent)
    yaxismin = .13333
    #h_Data.SetMinimum(yaxismin)
    h_Data_A.SetMaximum(10*h_Data_A.GetMaximum())
    if 'control' in tagname:
    	h_Data_A.SetMaximum(10*h_Data_A.GetMaximum())
    if 'St' in recovariable or 'GoodVertex' in recovariable:
    	h_Data_A.SetMaximum(250*h_Data_A.GetMaximum())
    if 'GoodVertex' in recovariable and 'linscale' in tagname:
    	h_Data_A.SetMaximum(2.0*h_Data_A.GetMaximum())
    if 'St' in recovariable and 'final' in tagname:
    	h_Data_A.SetMaximum(50*h_Data_A.GetMaximum())
    if 'DPhi' in recovariable or ('MT' in recovariable and 'control' in tagname):
    	h_Data_A.SetMaximum(2.0*h_Data_A.GetMaximum())
    if blinded==True and 'final' in tagname:
    	h_Data_A.SetMaximum(100*h_Data_A.GetMaximum())

    # Create Ratio subplot here
    pad3.cd()
    pad3.SetGrid()

    RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_data,recovariable,presentationbinning,'0',DataRecoStyle2,Label)
    RatHistDen.Sumw2()
    RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_data,recovariable,presentationbinning,'0',DataRecoStyle2,Label)
    RatHistNum.Sumw2()
    RatHistDen.Add(h_Data_A)
    RatHistNum.Add(h_Data_B)
    RatHistNum.Divide(RatHistDen)
    
    # Cosmetics
    RatHistNum.SetMaximum(1.599)#fixme was 1.499
    RatHistNum.SetMinimum(0.401)#fixme was 0.501
    RatHistNum.GetYaxis().SetTitleFont(42);
    RatHistNum.GetXaxis().SetTitle('');
    RatHistNum.GetYaxis().SetTitle('Ratio');
    RatHistNum.GetXaxis().SetTitle(xlabel)
    RatHistNum.GetYaxis().SetTitleFont(42)
    RatHistNum.GetYaxis().SetTitle('Ratio')
    RatHistNum.GetYaxis().SetNdivisions(308,True)
    RatHistNum.GetXaxis().SetTitleSize(0.14);
    RatHistNum.GetYaxis().SetTitleSize(.12);
    #RatHistNum.GetXaxis().CenterTitle();
    RatHistNum.GetYaxis().CenterTitle();		
    RatHistNum.GetXaxis().SetTitleOffset(0.);
    RatHistNum.GetYaxis().SetTitleOffset(.45);
    RatHistNum.GetYaxis().SetLabelSize(.1);
    RatHistNum.GetXaxis().SetLabelSize(.09);
    RatHistDen.SetMarkerSize(0)
    RatHistDen.SetMarkerColor(1)
    RatHistDen.SetFillColor(17)
    RatHistDen.SetFillStyle(3105)

    # Draw ratio sublot
    for bin in range(RatHistDen.GetNbinsX()+1) :
        if bin==0: continue
        x = RatHistDen.GetBinContent(bin)
        err = RatHistDen.GetBinError(bin)
        if x==0: err=0
        else: err = err/x
        RatHistDen.SetBinError(bin,err)
        RatHistDen.SetBinContent(bin,1)
        RatHistNum.Draw("E0SAMES")
        
        unity=TLine(RatHistNum.GetXaxis().GetXmin(), 1.0 , RatHistNum.GetXaxis().GetXmax(),1.0)
        unity.SetLineColor(1)
        unity.Draw("SAME")
        RatHistNum.Draw("E0SAMES")
    
    # Save plot as PDF
    print "Creating file "+ResultsDir+"/Plots/"+version_name+"/Data_BeforeAfterRun319077_LQ_"+channel+"_"+recovariable+"_"+tagname+".pdf..."
    c1.Print(ResultsDir+"/Plots/"+version_name+"/Data_BeforeAfterRun319077_LQ_"+channel+"_"+recovariable+"_"+tagname+".pdf")


# HEM 15+16 region
HEM1516Failure_runNum = '319077'
HEM1516Failure_eta_low = '-3.0'
HEM1516Failure_eta_high = '-1.3'
HEM1516Failure_phi_low = '-1.57'
HEM1516Failure_phi_high = '-0.87'

# At least one jet in HEM 15/16
HEM1516Failure_eta_jet1_sel = '(Eta_jet1>'+HEM1516Failure_eta_low+')*(Eta_jet1<'+HEM1516Failure_eta_high+')'
HEM1516Failure_eta_jet2_sel = '(Eta_jet2>'+HEM1516Failure_eta_low+')*(Eta_jet2<'+HEM1516Failure_eta_high+')'
HEM1516Failure_phi_jet1_sel = '(Phi_jet1>'+HEM1516Failure_phi_low+')*(Phi_jet1<'+HEM1516Failure_phi_high+')'
HEM1516Failure_phi_jet2_sel = '(Phi_jet2>'+HEM1516Failure_phi_low+')*(Phi_jet2<'+HEM1516Failure_phi_high+')'
HEM1516Failure_Jet_sel = '((('+HEM1516Failure_eta_jet1_sel+'*'+HEM1516Failure_phi_jet1_sel+')+('+HEM1516Failure_eta_jet2_sel+'*'+HEM1516Failure_phi_jet2_sel+'))>0)'

# At least one muon in HEM 15/16
HEM1516Failure_eta_muon1_sel = '(Eta_muon1>'+HEM1516Failure_eta_low+')*(Eta_muon1<'+HEM1516Failure_eta_high+')'
HEM1516Failure_eta_muon2_sel = '(Eta_muon2>'+HEM1516Failure_eta_low+')*(Eta_muon2<'+HEM1516Failure_eta_high+')'
HEM1516Failure_phi_muon1_sel = '(Phi_muon1>'+HEM1516Failure_phi_low+')*(Phi_muon1<'+HEM1516Failure_phi_high+')'
HEM1516Failure_phi_muon2_sel = '(Phi_muon2>'+HEM1516Failure_phi_low+')*(Phi_muon2<'+HEM1516Failure_phi_high+')'
HEM1516Failure_Muon_sel = '((('+HEM1516Failure_eta_muon1_sel+'*'+HEM1516Failure_phi_muon1_sel+')+('+HEM1516Failure_eta_muon2_sel+'*'+HEM1516Failure_phi_muon2_sel+'))>0)'

# MET in HEM 15/16
HEM1516Failure_phi_miss_sel = '(Phi_miss>'+HEM1516Failure_phi_low+')*(Phi_miss<'+HEM1516Failure_phi_high+')'
HEM1516Failure_pt_miss_sel = '(Pt_miss>200)'



# Combine selections
HEM1516Failure_sel = HEM1516Failure_Jet_sel+'+'+HEM1516Failure_Muon_sel

# Select period A
HEM1516Failure_A_sel = '*(run_number<'+HEM1516Failure_runNum+')'
# Select period B
HEM1516Failure_B_sel = '*('+HEM1516Failure_runNum+'<=run_number)'

# 2018 Total integrated luminosity
lumi = 59830.
lumiInvfb = '59.8'

# Integrated lumi in A

# Integrated lumi in B

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

# Correction to tracker issue
trackerHIP1 = "*(0.991237*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.994853*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.996413*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.997157*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.997512*(Eta_muon1>-0.9)*(Eta_muon1<-0.6)+0.99756*(Eta_muon1>-0.6)*(Eta_muon1<-0.3)+0.996745*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.996996*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.99772*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998604*(Eta_muon1>0.3)*(Eta_muon1<0.6)+0.998321*(Eta_muon1>0.6)*(Eta_muon1<0.9)+0.997682*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.995252*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.994919*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.987334*(Eta_muon1>2.1)*(Eta_muon1<2.4) )"
trackerHIP2 = "*(0.991237*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.994853*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.996413*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.997157*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.997512*(Eta_muon2>-0.9)*(Eta_muon2<-0.6)+0.99756*(Eta_muon2>-0.6)*(Eta_muon2<-0.3)+0.996745*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.996996*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.99772*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.998604*(Eta_muon2>0.3)*(Eta_muon2<0.6)+0.998321*(Eta_muon2>0.6)*(Eta_muon2<0.9)+0.997682*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.995252*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.994919*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.987334*(Eta_muon2>2.1)*(Eta_muon2<2.4) )"

# Event weight
NormalWeightMuMu = str(lumi)+"*weight_central"+doublemuHLT+doubleMuRecoSF+doubleMuIsoSF+doubleMuIdSF+bTagSFmedium

# Preselection
preselectionmumu = "((Pt_muon1>53)*(Pt_muon2>53)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3)"+bTagselmedium+")"
preselectionmumu += passfilter

# Trigger selection for data
dataHLT = "*((pass_HLTMu50+pass_HLTOldMu100+pass_HLTTkMu100)>0)"

# Plotting parameters

# Cosmetics
DataRecoStyle1=[0,20,1.5,1,1]
DataRecoStyle2=[0,20,1.5,1,2]

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
[[Rz_uuj,Rz_uuj_err],[Rtt_uuj,Rtt_uuj_err]]  =  [[ 1.334,0.016],[1.033,0.009]] #2018 stock NanoAODv7 with 1 btag (uub)
[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]]  =  [[1.336,0.017],[1.033,0.01]] #2018 stock NanoAODv7 with 1 btag (uubj)
[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = [[1.0,0.0],[1.0,0.0]]

version_name = "HEMFailureStudy"
os.system('mkdir '+ResultsDir+'/Plots')
os.system('mkdir '+ResultsDir+'/Plots/'+version_name)

# Add whichever distributions you like here and a PDF will be created
#print preselectionmumu+dataHLT+HEM1516Failure_B_sel
#exit()
# Objects in eta and phi
MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)

MakeBasicPlot("Phi_miss","#phi^{miss} [GeV]",[16,-3.1416,3.1416],preselectionmumu+'*'+HEM1516Failure_pt_miss_sel,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)	
MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[50,0,1000],preselectionmumu+'*'+HEM1516Failure_phi_miss_sel,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)

# BDT Input variables
MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("M_uujj","M_{#mu#mujj} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[50,0,1000],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
#MakeBasicPlot("DeepJet_jet1","Jet1 DeepJet score",bjetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
#MakeBasicPlot("DeepJet_jet2","Jet2 DeepJet score",bjetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("DR_dimuonjet1","#DeltaR(#mu_{1}+#mu_{2},j_{1})",drbinning,preselectionmumu+"*(St_uujj>1000)*(M_uujj>1000)*(M_uu>250)",NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)

# Interesting plots
MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'linscale','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonzoombinning_uujj_Z,preselectionmumu,NormalWeightMuMu,NormalDirectory,'controlzoom_ZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonzoombinning_uujj_TT,preselectionmumu+'*(M_uu>100)*(Pt_miss>=100)',NormalWeightMuMu,NormalDirectory,'controlzoom_TTRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
