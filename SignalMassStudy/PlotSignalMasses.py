import os, math, sys, random
import subprocess
import json
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

# Set the data year here:
year = '2018'

#################################################
###  Integrated luminosity for normalization  ###
#################################################

# Udated July 13th 2021: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TWikiLUM
lumi = 0
if year == '2016':
	lumi = 36330.0
	lumiInvfb = '36.3'
elif year == '2017':
	lumi = 41480.0
	lumiInvfb = '41.5'
elif year == '2018':
	lumi = 59830.0
	lumiInvfb = '59.8'

####################################################
###  Medium DeepJet working points defined here  ###
####################################################

deepJetWPmedium = '0'
if year == '2016': deepJetWPmedium = '0.3093'
elif year == '2017': deepJetWPmedium = '0.3033'
elif year == '2018': deepJetWPmedium = '0.2770'

################################
###  HLT paths defined here  ###
################################

dataHLT = '*0'
if year == '2016': dataHLT = '*((pass_HLTMu50+pass_HLTTkMu50)>0)'
elif year == '2017' or year == '2018': dataHLT = '*((pass_HLTMu50+pass_HLTOldMu100+pass_HLTTkMu100)>0)'

####################################
###  Event weights defined here  ###
####################################

# Muon trigger efficiency
doublemuHLT = '*(1.0-((1.0-mu1hltSF)*(1.0-mu2hltSF)))'

# Muon High-pT ID efficiency
doubleMuIdSF = '*mu1idSF*mu2idSF'

# Muon relaitve track isolation efficiency
doubleMuIsoSF = '*mu1isoSF*mu2isoSF'

# Muon reconstruction efficiency
doubleMuRecoSF = '*mu1recoSF*mu2recoSF'

# b-Jet identification efficiency
bTagSFmedium = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium+')*bTagSF_jet1)*(1-(DeepJet_jet2>'+deepJetWPmedium+')*bTagSF_jet2))'

# Concatenate all event weights
eventWeights = str(lumi)+'*weight_central*prefireWeight'+doublemuHLT+doubleMuRecoSF+doubleMuIsoSF+doubleMuIdSF+bTagSFmedium

########################################
###  Preselection cuts defined here  ###
########################################

# b-Jet requirement (>=1 b-jet)
bTagselmedium = '*(((DeepJet_jet1>'+deepJetWPmedium+')+(DeepJet_jet2>'+deepJetWPmedium+'))>0)'

# Preselection
preselection = '((Pt_muon1>53)*(Pt_muon2>53)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3)'+bTagselmedium+')'

###########################################
###  Final selection cuts defined here  ###
###########################################

finalSelCut = {}

# Optimized cuts
finalSelCut['300'] = '*(LQToBMu_pair_uubj_BDT_discrim_M300>0.988)*(M_uu>250)'
finalSelCut['400'] = '*(LQToBMu_pair_uubj_BDT_discrim_M400>0.987)*(M_uu>250)'
finalSelCut['500'] = '*(LQToBMu_pair_uubj_BDT_discrim_M500>0.994)*(M_uu>250)'
finalSelCut['600'] = '*(LQToBMu_pair_uubj_BDT_discrim_M600>0.996)*(M_uu>250)'
finalSelCut['700'] = '*(LQToBMu_pair_uubj_BDT_discrim_M700>0.998)*(M_uu>250)'
finalSelCut['800'] = '*(LQToBMu_pair_uubj_BDT_discrim_M800>0.998)*(M_uu>250)'
finalSelCut['900'] = '*(LQToBMu_pair_uubj_BDT_discrim_M900>0.997)*(M_uu>250)'
finalSelCut['1000'] = '*(LQToBMu_pair_uubj_BDT_discrim_M1000>0.999)*(M_uu>250)'
finalSelCut['1100'] = '*(LQToBMu_pair_uubj_BDT_discrim_M1100>0.999)*(M_uu>250)'
finalSelCut['1200'] = '*(LQToBMu_pair_uubj_BDT_discrim_M1200>0.999)*(M_uu>250)'
finalSelCut['1300'] = '*(LQToBMu_pair_uubj_BDT_discrim_M1300>0.999)*(M_uu>250)'
finalSelCut['1400'] = '*(LQToBMu_pair_uubj_BDT_discrim_M1400>0.999)*(M_uu>250)'
finalSelCut['1500'] = '*(LQToBMu_pair_uubj_BDT_discrim_M1500>0.999)*(M_uu>250)'
finalSelCut['1600'] = '*(LQToBMu_pair_uubj_BDT_discrim_M1600>0.999)*(M_uu>250)'
finalSelCut['1700'] = '*(LQToBMu_pair_uubj_BDT_discrim_M1700>0.997)*(M_uu>250)'
finalSelCut['1800'] = '*(LQToBMu_pair_uubj_BDT_discrim_M1800>0.999)*(M_uu>250)'
finalSelCut['1900'] = '*(LQToBMu_pair_uubj_BDT_discrim_M1900>0.999)*(M_uu>250)'
finalSelCut['2000'] = '*(LQToBMu_pair_uubj_BDT_discrim_M2000>0.999)*(M_uu>250)'
finalSelCut['2100'] = '*(LQToBMu_pair_uubj_BDT_discrim_M2100>0.925)*(M_uu>250)'
finalSelCut['2200'] = '*(LQToBMu_pair_uubj_BDT_discrim_M2200>0.999)*(M_uu>250)'
finalSelCut['2300'] = '*(LQToBMu_pair_uubj_BDT_discrim_M2300>0.996)*(M_uu>250)'
finalSelCut['2400'] = '*(LQToBMu_pair_uubj_BDT_discrim_M2400>0.997)*(M_uu>250)'
finalSelCut['2500'] = '*(LQToBMu_pair_uubj_BDT_discrim_M2500>0.998)*(M_uu>250)'
finalSelCut['2600'] = '*(LQToBMu_pair_uubj_BDT_discrim_M2600>0.9)*(M_uu>250)'
finalSelCut['2700'] = '*(LQToBMu_pair_uubj_BDT_discrim_M2700>0.999)*(M_uu>250)'
finalSelCut['2800'] = '*(LQToBMu_pair_uubj_BDT_discrim_M2800>0.999)*(M_uu>250)'
finalSelCut['2900'] = '*(LQToBMu_pair_uubj_BDT_discrim_M2900>0.953)*(M_uu>250)'
finalSelCut['3000'] = '*(LQToBMu_pair_uubj_BDT_discrim_M3000>0.996)*(M_uu>250)'
finalSelCut['3500'] = '*(LQToBMu_pair_uubj_BDT_discrim_M3500>0.997)*(M_uu>250)'
finalSelCut['4000'] = '*(LQToBMu_pair_uubj_BDT_discrim_M4000>0.9)*(M_uu>250)'

##################################
###  MET filters defined here  ###
##################################

passfilter =  '*(Flag_goodVertices*(GoodVertexCount>=1))'
passfilter += '*(Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter)'
passfilter += '*(Flag_eeBadScFilter*Flag_EcalDeadCellTriggerPrimitiveFilter)'
passfilter += '*(Flag_globalSuperTightHalo2016Filter)'
passfilter += '*(Flag_BadPFMuonFilter)'

# Add the filters to preselection
eventWeights += passfilter

# Prepare info for input files

# Store full path of all 51 subdirectories as values in dict, with copy index as key
if year == '2016':
	NormalDirectory = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2016/gmadigan/NTupleAnalyzer_nanoAOD_Full2016updatedMER_SysBDT_stockNano_2021_11_03_08_40_52/SummaryFiles'
elif year == '2017':
	NormalDirectory = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2017/gmadigan/NTupleAnalyzer_nanoAOD_Full2017updatedMER_SysBDT_stockNano_2021_11_06_12_12_51/SummaryFiles'
elif year == '2018':
	NormalDirectory = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2018/gmadigan/NTupleAnalyzer_nanoAOD_Full2018updatedMER_SysBDT_stockNano_2021_11_03_22_52_50/SummaryFiles'

# Read files in subdirectories and get names of files--stored as values 
bkgTypes = [   "ZJets",
				"TTBar",
				"WJets",
				"SingleTop",
				"TTV",
				"DiBoson"
]

sigTypes = [	"LQuujj300",
				"LQuujj400",
				"LQuujj500",
				"LQuujj600",
				"LQuujj700",
				"LQuujj800",
				"LQuujj900",
				"LQuujj1000",
				"LQuujj1100",
				"LQuujj1200",
				"LQuujj1300",
				"LQuujj1400",
				"LQuujj1500",
				"LQuujj1600",
				"LQuujj1700",
				"LQuujj1800",
				"LQuujj1900",
				"LQuujj2000",
				"LQuujj2100",
				"LQuujj2200",
            	"LQuujj2300",
				"LQuujj2400",
				"LQuujj2500",
				"LQuujj2600",
				"LQuujj2700",
				"LQuujj2800",
				"LQuujj2900",
				"LQuujj3000",
				"LQuujj3500",
				"LQuujj4000"
]

fileTypes = sigTypes

lqMasses = ['300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','200','2100','2200','2300','2400','2500','2600','2700','2800','2900','3000','3500','4000']

# Declare trees as 't_' + file name + '_GEcopy' + index of GE copy
# Declare histograms as 'h_' + variable + '_' + file name + '_GEcopy' + index of GE copy 

########################################
###  Define plotting functions here  ###
########################################

def CreateHisto(name,legendname,tree,variable,binning,selection,style,label):

	# Projects histogram of 'variable' (e.g., 'Pt_muon1') from tree (physical variables)
	# onto new histogram 'hout' with custom binning and selection.
	#
	# Returns TH1D object
	#
	# Style is a list that sets the hist's cosmetics:
	# [fill style, marker style, marker size, line width, marker/line/fill color]
	#
	# Other cosmetics that are set include:
	# - x-axis title font, size, and offset
	# - y-axis title font, size, and offset
	# - x-axis labels font, size, and offset
	# - y-axis labels font, size, and offset

	binset=ConvertBinning(binning)
	n = len(binset)-1
	hout= TH1D(name,legendname,n,array('d',binset))
	hout.Sumw2()
	tree.Project(name,variable,selection)

	# Histogram cosmetics
	# fill style
	hout.SetFillStyle(style[0])
	# marker style
	hout.SetMarkerStyle(style[1])
	# marker size
	hout.SetMarkerSize(style[2])
	# line width
	hout.SetLineWidth(style[3])
	# color
	hout.SetMarkerColor(style[4])
	hout.SetLineColor(style[4])
	hout.SetFillColor(style[4])

	# Axis title cosmetics
	# titles
	hout.GetXaxis().SetTitle(label[0])
	hout.GetYaxis().SetTitle(label[1])
	# font
	hout.GetXaxis().SetTitleFont(42)
	hout.GetYaxis().SetTitleFont(42)
	# offset
	hout.GetXaxis().SetTitleOffset(0.92)
	hout.GetYaxis().SetTitleOffset(0.92)
	# size
	hout.GetXaxis().SetTitleSize(0.06)
	hout.GetYaxis().SetTitleSize(0.06)

	# Axis label cosmetics
	# font
	hout.GetXaxis().SetLabelFont(42)
	hout.GetYaxis().SetLabelFont(42)
	# offset
	hout.GetXaxis().SetLabelOffset(0.007)
	hout.GetYaxis().SetLabelOffset(0.007)
	#size
	hout.GetXaxis().SetLabelSize(0.06)
	hout.GetYaxis().SetLabelSize(0.06)

	return hout

def BeautifyHisto(histo,label):
	histo.GetXaxis().SetTitleFont(42)
	histo.GetYaxis().SetTitleFont(42)
	histo.GetXaxis().SetLabelFont(42)
	histo.GetYaxis().SetLabelFont(42)
	histo.GetXaxis().SetTitle(label[0])
	histo.GetYaxis().SetTitle(label[1])
	histo.GetXaxis().SetTitle(label[0])
	histo.GetYaxis().SetTitle(label[1])
	histo.GetXaxis().SetTitleFont(42)
	histo.GetYaxis().SetTitleFont(42)
	histo.GetXaxis().SetLabelFont(42)
	histo.GetYaxis().SetLabelFont(42)
	histo.GetXaxis().SetLabelOffset(0.007)
	histo.GetYaxis().SetLabelOffset(0.007)
	histo.GetXaxis().SetLabelSize(0.03)
	histo.GetYaxis().SetLabelSize(0.038)

	histo.GetXaxis().SetTitleOffset(1.05)
	histo.GetYaxis().SetTitleOffset(1.25)
	histo.GetXaxis().SetTitleSize(0.048)
	histo.GetYaxis().SetTitleSize(0.05)

def ConvertBinning(binning):
	binset=[]
	if len(binning)==3:
		for x in range(binning[0]+1):
			binset.append(((binning[2]-binning[1])/(1.0*binning[0]))*x*1.0+binning[1])
	else:
		binset=binning
	return binset

def QuickEntries(tree,selection,scalefac):

	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection)
	I = h.GetEntries()
	return [1.0*I*scalefac, math.sqrt(1.0*I*scalefac)]

def QuickIntegral(tree,selection,scalefac):

	# print selection+'*'+str(scalefac)
	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection+'*'+str(scalefac))
	I = h.GetBinContent(1)
	E = h.GetBinError(1)
	return [I,E]


def PlotM300toM800(recovariable,xlabel,presentationbinning,selection,weight,outdir):

	############################################################################
	######### Make plots for muon scale copies and average over copies #########
	######### Include the uncorrected distribution for comparison      #########
	######### Signal samples only								   	   #########
	############################################################################

	#############################################################################
	#																			#
	#						Start with histogram creation						#
	#																			#
	#############################################################################

	# x-axis title and y-axis title

	Label=[xlabel,"Events / bin"]

	# Set style options for average and ratio histograms (den style is a placeholder--will be overridden by numerator style)
	# [fill style, marker style, marker size, line width, marker/line/fill color]

	m300Style = [0,20,1,2,2] #[no fill, filled circle, normal size, normal width, red]
	m400Style = [0,20,1,2,3] #[no fill, filled circle, normal size, normal width, green]
	m500Style = [0,20,1,2,4] #[no fill, filled circle, normal size, normal width, blue]
	m600Style = [0,20,1,2,6] #[no fill, filled circle, normal size, normal width, magenta]
	m700Style = [0,20,1,2,7] #[no fill, filled circle, normal size, normal width, cyan]
	m800Style = [0,20,1,2,28] #[no fill, filled circle, normal size, normal width, brown]

	h_LQuujj300 = CreateHisto("h_LQuujj300","LQuujj300",t_LQuujj300,recovariable,presentationbinning,selection+"*"+weight,m300Style,Label)
	h_LQuujj400 = CreateHisto("h_LQuujj400","LQuujj400",t_LQuujj400,recovariable,presentationbinning,selection+"*"+weight,m400Style,Label)
	h_LQuujj500 = CreateHisto("h_LQuujj500","LQuujj500",t_LQuujj500,recovariable,presentationbinning,selection+"*"+weight,m500Style,Label)
	h_LQuujj600 = CreateHisto("h_LQuujj600","LQuujj600",t_LQuujj600,recovariable,presentationbinning,selection+"*"+weight,m600Style,Label)
	h_LQuujj700 = CreateHisto("h_LQuujj700","LQuujj700",t_LQuujj700,recovariable,presentationbinning,selection+"*"+weight,m700Style,Label)
	h_LQuujj800 = CreateHisto("h_LQuujj800","LQuujj800",t_LQuujj800,recovariable,presentationbinning,selection+"*"+weight,m800Style,Label)

	BeautifyHisto(h_LQuujj300,Label)
	BeautifyHisto(h_LQuujj400,Label)
	BeautifyHisto(h_LQuujj500,Label)
	BeautifyHisto(h_LQuujj600,Label)
	BeautifyHisto(h_LQuujj700,Label)
	BeautifyHisto(h_LQuujj800,Label)
	
	#############################################################################
	#																			#
	#						Create objects for each plot						#
	#																			#
	#############################################################################

	############################################################
	######### Initialize canvases, pads, legends, etc. #########
	######### Customize options for each               #########
	############################################################

	# c1 = main canvas

	c1 = TCanvas("c1","",850,800)

	# Create pads for main and ratio plots per canvas

	pad1_main 	= TPad( 'pad1_main', 'pad1_main', 0.0, 0.0, 1.0, 1.0 )

	# Draw pads

	c1.cd()
	pad1_main.Draw()
	gStyle.SetPadLeftMargin(0.14)
  	gROOT.ForceStyle()

	# Set pad upper and lower margins

	#pad1_main.SetBottomMargin(0.43)	

	# Create each legend and customize options

	leg1 = TLegend(0.5,0.6,0.85,0.85,"","brNDC")


	leg1.SetTextFont(42)
	leg1.SetFillColor(0)
	leg1.SetFillStyle(0)
	leg1.SetBorderSize(0)
	leg1.SetTextSize(.035)


	# For each legend, add an entry for the uncorrected distribution and either:
	# a representative entry for the copies, 
	# or the average over all the copies

	leg1.AddEntry(h_LQuujj300,"m_{LQ} = 300 GeV","l")
	leg1.AddEntry(h_LQuujj400,"m_{LQ} = 400 GeV","l")
	leg1.AddEntry(h_LQuujj500,"m_{LQ} = 500 GeV","l")
	leg1.AddEntry(h_LQuujj600,"m_{LQ} = 600 GeV","l")
	leg1.AddEntry(h_LQuujj700,"m_{LQ} = 700 GeV","l")
	leg1.AddEntry(h_LQuujj800,"m_{LQ} = 800 GeV","l")


	# Declare and customize the LaTeX objects that will be drawn to the pad, 
	# e.g., CMS logo, integrated luminosity, and collision energy

	# Drawn above main pad

	l1_header = TLatex()
	l1_header.SetTextAlign(12)
	l1_header.SetTextFont(42)
	l1_header.SetNDC()
	l1_header.SetTextSize(0.045)

	# Drawn inside main pad

	l1_logo = TLatex()
	l1_logo.SetTextAlign(12)
	l1_logo.SetTextFont(62)
	l1_logo.SetNDC()
	l1_logo.SetTextSize(0.06)

	# Initialize lists for y-axis maxima

	maxList1 = []

	# Get rid of stats box, pad title, etc.,

	gStyle.SetOptStat(0)


	#############################################################################
	#																			#
	#						Draw each plot and save as PDF						#
	#																			#
	#############################################################################

	##################################
	######### GE copies plot #########
	##################################

	c1.cd()

	#############################
	######### Main plot #########
	#############################

	# Switch to main pad, set to log scale

	pad1_main.cd()
	pad1_main.SetLogy()

	# Draw each copy histogram on main pad
	# Modify cosmetics of each histogram with BeautifyHisto()
	# Get the maxima of each histogram

	h_LQuujj300.Draw("HIST")
	h_LQuujj400.Draw("HISTSAME")
	h_LQuujj500.Draw("HISTSAME")
	h_LQuujj600.Draw("HISTSAME")
	h_LQuujj700.Draw("HISTSAME")
	h_LQuujj800.Draw("HISTSAME")

	maxList1.append(h_LQuujj300.GetMaximum())
	maxList1.append(h_LQuujj400.GetMaximum())
	maxList1.append(h_LQuujj500.GetMaximum())
	maxList1.append(h_LQuujj600.GetMaximum())
	maxList1.append(h_LQuujj700.GetMaximum())
	maxList1.append(h_LQuujj800.GetMaximum())

	# Set the maximum on the y-axis shown in the plot 
	# as some multiple of the largest hist maximum

	h_LQuujj300.SetMaximum(100*max(maxList1))
	
	# Draw legend and LaTeX strings

	leg1.Draw()
	l1_header.DrawLatex(0.12,0.93,"#it{Simulation}                            "+lumiInvfb+" fb^{-1} (13 TeV)")
	l1_logo.DrawLatex(0.15,0.845,"CMS")

	# Update the pad and redraw axis

	gPad.Update()
	gPad.RedrawAxis()

	# Save PDFs

	c1.Print(outDir+"/Mujbj_M300_to_M800.pdf")

def PlotM900toM1400(recovariable,xlabel,presentationbinning,selection,weight,outdir):

	############################################################################
	######### Make plots for muon scale copies and average over copies #########
	######### Include the uncorrected distribution for comparison      #########
	######### Signal samples only								   	   #########
	############################################################################

	#############################################################################
	#																			#
	#						Start with histogram creation						#
	#																			#
	#############################################################################

	# x-axis title and y-axis title

	Label=[xlabel,"Events / bin"]

	# Set style options for average and ratio histograms (den style is a placeholder--will be overridden by numerator style)
	# [fill style, marker style, marker size, line width, marker/line/fill color]

	m900Style = [0,20,1,2,2] #[no fill, filled circle, normal size, normal width, red]
	m1000Style = [0,20,1,2,3] #[no fill, filled circle, normal size, normal width, green]
	m1100Style = [0,20,1,2,4] #[no fill, filled circle, normal size, normal width, blue]
	m1200Style = [0,20,1,2,6] #[no fill, filled circle, normal size, normal width, magenta]
	m1300Style = [0,20,1,2,7] #[no fill, filled circle, normal size, normal width, cyan]
	m1400Style = [0,20,1,2,28] #[no fill, filled circle, normal size, normal width, brown]

	h_LQuujj900 = CreateHisto("h_LQuujj900","LQuujj900",t_LQuujj900,recovariable,presentationbinning,selection+"*"+weight,m900Style,Label)
	h_LQuujj1000 = CreateHisto("h_LQuujj1000","LQuujj1000",t_LQuujj1000,recovariable,presentationbinning,selection+"*"+weight,m1000Style,Label)
	h_LQuujj1100 = CreateHisto("h_LQuujj1100","LQuujj1100",t_LQuujj1100,recovariable,presentationbinning,selection+"*"+weight,m1100Style,Label)
	h_LQuujj1200 = CreateHisto("h_LQuujj1200","LQuujj1200",t_LQuujj1200,recovariable,presentationbinning,selection+"*"+weight,m1200Style,Label)
	h_LQuujj1300 = CreateHisto("h_LQuujj1300","LQuujj1300",t_LQuujj1300,recovariable,presentationbinning,selection+"*"+weight,m1300Style,Label)
	h_LQuujj1400 = CreateHisto("h_LQuujj1400","LQuujj1400",t_LQuujj1400,recovariable,presentationbinning,selection+"*"+weight,m1400Style,Label)

	BeautifyHisto(h_LQuujj900,Label)
	BeautifyHisto(h_LQuujj1000,Label)
	BeautifyHisto(h_LQuujj1100,Label)
	BeautifyHisto(h_LQuujj1200,Label)
	BeautifyHisto(h_LQuujj1300,Label)
	BeautifyHisto(h_LQuujj1400,Label)
	
	#############################################################################
	#																			#
	#						Create objects for each plot						#
	#																			#
	#############################################################################

	############################################################
	######### Initialize canvases, pads, legends, etc. #########
	######### Customize options for each               #########
	############################################################

	# c1 = main canvas

	c1 = TCanvas("c1","",850,800)

	# Create pads for main and ratio plots per canvas

	pad1_main 	= TPad( 'pad1_main', 'pad1_main', 0.0, 0.0, 1.0, 1.0 )

	# Draw pads

	c1.cd()
	pad1_main.Draw()
	gStyle.SetPadLeftMargin(0.14)
  	gROOT.ForceStyle()

	# Set pad upper and lower margins

	#pad1_main.SetBottomMargin(0.43)	

	# Create each legend and customize options

	leg1 = TLegend(0.5,0.6,0.85,0.85,"","brNDC")


	leg1.SetTextFont(42)
	leg1.SetFillColor(0)
	leg1.SetFillStyle(0)
	leg1.SetBorderSize(0)
	leg1.SetTextSize(.035)


	# For each legend, add an entry for the uncorrected distribution and either:
	# a representative entry for the copies, 
	# or the average over all the copies

	leg1.AddEntry(h_LQuujj900,"m_{LQ} = 900 GeV","l")
	leg1.AddEntry(h_LQuujj1000,"m_{LQ} = 1000 GeV","l")
	leg1.AddEntry(h_LQuujj1100,"m_{LQ} = 1100 GeV","l")
	leg1.AddEntry(h_LQuujj1200,"m_{LQ} = 1200 GeV","l")
	leg1.AddEntry(h_LQuujj1300,"m_{LQ} = 1300 GeV","l")
	leg1.AddEntry(h_LQuujj1400,"m_{LQ} = 1400 GeV","l")


	# Declare and customize the LaTeX objects that will be drawn to the pad, 
	# e.g., CMS logo, integrated luminosity, and collision energy

	# Drawn above main pad

	l1_header = TLatex()
	l1_header.SetTextAlign(12)
	l1_header.SetTextFont(42)
	l1_header.SetNDC()
	l1_header.SetTextSize(0.045)

	# Drawn inside main pad

	l1_logo = TLatex()
	l1_logo.SetTextAlign(12)
	l1_logo.SetTextFont(62)
	l1_logo.SetNDC()
	l1_logo.SetTextSize(0.06)

	# Initialize lists for y-axis maxima

	maxList1 = []

	# Get rid of stats box, pad title, etc.,

	gStyle.SetOptStat(0)


	#############################################################################
	#																			#
	#						Draw each plot and save as PDF						#
	#																			#
	#############################################################################

	##################################
	######### GE copies plot #########
	##################################

	c1.cd()

	#############################
	######### Main plot #########
	#############################

	# Switch to main pad, set to log scale

	pad1_main.cd()
	pad1_main.SetLogy()

	# Draw each copy histogram on main pad
	# Modify cosmetics of each histogram with BeautifyHisto()
	# Get the maxima of each histogram

	h_LQuujj900.Draw("HIST")
	h_LQuujj1000.Draw("HISTSAME")
	h_LQuujj1100.Draw("HISTSAME")
	h_LQuujj1200.Draw("HISTSAME")
	h_LQuujj1300.Draw("HISTSAME")
	h_LQuujj1400.Draw("HISTSAME")

	maxList1.append(h_LQuujj900.GetMaximum())
	maxList1.append(h_LQuujj1000.GetMaximum())
	maxList1.append(h_LQuujj1100.GetMaximum())
	maxList1.append(h_LQuujj1200.GetMaximum())
	maxList1.append(h_LQuujj1300.GetMaximum())
	maxList1.append(h_LQuujj1400.GetMaximum())

	# Set the maximum on the y-axis shown in the plot 
	# as some multiple of the largest hist maximum

	h_LQuujj900.SetMaximum(100*max(maxList1))
	
	# Draw legend and LaTeX strings

	leg1.Draw()
	l1_header.DrawLatex(0.12,0.93,"#it{Simulation}                            "+lumiInvfb+" fb^{-1} (13 TeV)")
	l1_logo.DrawLatex(0.15,0.845,"CMS")

	# Update the pad and redraw axis

	gPad.Update()
	gPad.RedrawAxis()

	# Save PDFs

	c1.Print(outDir+"/Mujbj_M900_to_M1400.pdf")

def PlotM1500toM2000(recovariable,xlabel,presentationbinning,selection,weight,outdir):

	############################################################################
	######### Make plots for muon scale copies and average over copies #########
	######### Include the uncorrected distribution for comparison      #########
	######### Signal samples only								   	   #########
	############################################################################

	#############################################################################
	#																			#
	#						Start with histogram creation						#
	#																			#
	#############################################################################

	# x-axis title and y-axis title

	Label=[xlabel,"Events / bin"]

	# Set style options for average and ratio histograms (den style is a placeholder--will be overridden by numerator style)
	# [fill style, marker style, marker size, line width, marker/line/fill color]

	m1500Style = [0,20,1,2,2] #[no fill, filled circle, normal size, normal width, red]
	m1600Style = [0,20,1,2,3] #[no fill, filled circle, normal size, normal width, green]
	m1700Style = [0,20,1,2,4] #[no fill, filled circle, normal size, normal width, blue]
	m1800Style = [0,20,1,2,6] #[no fill, filled circle, normal size, normal width, magenta]
	m1900Style = [0,20,1,2,7] #[no fill, filled circle, normal size, normal width, cyan]
	m2000Style = [0,20,1,2,28] #[no fill, filled circle, normal size, normal width, brown]

	h_LQuujj1500 = CreateHisto("h_LQuujj1500","LQuujj1500",t_LQuujj1500,recovariable,presentationbinning,selection+"*"+weight,m1500Style,Label)
	h_LQuujj1600 = CreateHisto("h_LQuujj1600","LQuujj1600",t_LQuujj1600,recovariable,presentationbinning,selection+"*"+weight,m1600Style,Label)
	h_LQuujj1700 = CreateHisto("h_LQuujj1700","LQuujj1700",t_LQuujj1700,recovariable,presentationbinning,selection+"*"+weight,m1700Style,Label)
	h_LQuujj1800 = CreateHisto("h_LQuujj1800","LQuujj1800",t_LQuujj1800,recovariable,presentationbinning,selection+"*"+weight,m1800Style,Label)
	h_LQuujj1900 = CreateHisto("h_LQuujj1900","LQuujj1900",t_LQuujj1900,recovariable,presentationbinning,selection+"*"+weight,m1900Style,Label)
	h_LQuujj2000 = CreateHisto("h_LQuujj2000","LQuujj2000",t_LQuujj2000,recovariable,presentationbinning,selection+"*"+weight,m2000Style,Label)

	BeautifyHisto(h_LQuujj1500,Label)
	BeautifyHisto(h_LQuujj1600,Label)
	BeautifyHisto(h_LQuujj1700,Label)
	BeautifyHisto(h_LQuujj1800,Label)
	BeautifyHisto(h_LQuujj1900,Label)
	BeautifyHisto(h_LQuujj2000,Label)
	
	#############################################################################
	#																			#
	#						Create objects for each plot						#
	#																			#
	#############################################################################

	############################################################
	######### Initialize canvases, pads, legends, etc. #########
	######### Customize options for each               #########
	############################################################

	# c1 = main canvas

	c1 = TCanvas("c1","",850,800)

	# Create pads for main and ratio plots per canvas

	pad1_main 	= TPad( 'pad1_main', 'pad1_main', 0.0, 0.0, 1.0, 1.0 )

	# Draw pads

	c1.cd()
	pad1_main.Draw()
	gStyle.SetPadLeftMargin(0.14)
  	gROOT.ForceStyle()

	# Set pad upper and lower margins

	#pad1_main.SetBottomMargin(0.43)	

	# Create each legend and customize options

	leg1 = TLegend(0.5,0.6,0.85,0.85,"","brNDC")


	leg1.SetTextFont(42)
	leg1.SetFillColor(0)
	leg1.SetFillStyle(0)
	leg1.SetBorderSize(0)
	leg1.SetTextSize(.035)


	# For each legend, add an entry for the uncorrected distribution and either:
	# a representative entry for the copies, 
	# or the average over all the copies

	leg1.AddEntry(h_LQuujj1500,"m_{LQ} = 1500 GeV","l")
	leg1.AddEntry(h_LQuujj1600,"m_{LQ} = 1600 GeV","l")
	leg1.AddEntry(h_LQuujj1700,"m_{LQ} = 1700 GeV","l")
	leg1.AddEntry(h_LQuujj1800,"m_{LQ} = 1800 GeV","l")
	leg1.AddEntry(h_LQuujj1900,"m_{LQ} = 1900 GeV","l")
	leg1.AddEntry(h_LQuujj2000,"m_{LQ} = 2000 GeV","l")


	# Declare and customize the LaTeX objects that will be drawn to the pad, 
	# e.g., CMS logo, integrated luminosity, and collision energy

	# Drawn above main pad

	l1_header = TLatex()
	l1_header.SetTextAlign(12)
	l1_header.SetTextFont(42)
	l1_header.SetNDC()
	l1_header.SetTextSize(0.045)

	# Drawn inside main pad

	l1_logo = TLatex()
	l1_logo.SetTextAlign(12)
	l1_logo.SetTextFont(62)
	l1_logo.SetNDC()
	l1_logo.SetTextSize(0.06)

	# Initialize lists for y-axis maxima

	maxList1 = []

	# Get rid of stats box, pad title, etc.,

	gStyle.SetOptStat(0)


	#############################################################################
	#																			#
	#						Draw each plot and save as PDF						#
	#																			#
	#############################################################################

	##################################
	######### GE copies plot #########
	##################################

	c1.cd()

	#############################
	######### Main plot #########
	#############################

	# Switch to main pad, set to log scale

	pad1_main.cd()
	pad1_main.SetLogy()

	# Draw each copy histogram on main pad
	# Modify cosmetics of each histogram with BeautifyHisto()
	# Get the maxima of each histogram

	h_LQuujj1500.Draw("HIST")
	h_LQuujj1600.Draw("HISTSAME")
	h_LQuujj1700.Draw("HISTSAME")
	h_LQuujj1800.Draw("HISTSAME")
	h_LQuujj1900.Draw("HISTSAME")
	h_LQuujj2000.Draw("HISTSAME")

	maxList1.append(h_LQuujj1500.GetMaximum())
	maxList1.append(h_LQuujj1600.GetMaximum())
	maxList1.append(h_LQuujj1700.GetMaximum())
	maxList1.append(h_LQuujj1800.GetMaximum())
	maxList1.append(h_LQuujj1900.GetMaximum())
	maxList1.append(h_LQuujj2000.GetMaximum())

	# Set the maximum on the y-axis shown in the plot 
	# as some multiple of the largest hist maximum

	h_LQuujj1500.SetMaximum(100*max(maxList1))
	
	# Draw legend and LaTeX strings

	leg1.Draw()
	l1_header.DrawLatex(0.12,0.93,"#it{Simulation}                            "+lumiInvfb+" fb^{-1} (13 TeV)")
	l1_logo.DrawLatex(0.15,0.845,"CMS")

	# Update the pad and redraw axis

	gPad.Update()
	gPad.RedrawAxis()

	# Save PDFs

	c1.Print(outDir+"/Mujbj_M1500_to_M2000.pdf")

def PlotM2100toM2600(recovariable,xlabel,presentationbinning,selection,weight,outdir):

	############################################################################
	######### Make plots for muon scale copies and average over copies #########
	######### Include the uncorrected distribution for comparison      #########
	######### Signal samples only								   	   #########
	############################################################################

	#############################################################################
	#																			#
	#						Start with histogram creation						#
	#																			#
	#############################################################################

	# x-axis title and y-axis title

	Label=[xlabel,"Events / bin"]

	# Set style options for average and ratio histograms (den style is a placeholder--will be overridden by numerator style)
	# [fill style, marker style, marker size, line width, marker/line/fill color]

	m2100Style = [0,20,1,2,2] #[no fill, filled circle, normal size, normal width, red]
	m2200Style = [0,20,1,2,3] #[no fill, filled circle, normal size, normal width, green]
	m2300Style = [0,20,1,2,4] #[no fill, filled circle, normal size, normal width, blue]
	m2400Style = [0,20,1,2,6] #[no fill, filled circle, normal size, normal width, magenta]
	m2500Style = [0,20,1,2,7] #[no fill, filled circle, normal size, normal width, cyan]
	m2600Style = [0,20,1,2,28] #[no fill, filled circle, normal size, normal width, brown]

	h_LQuujj2100 = CreateHisto("h_LQuujj2100","LQuujj2100",t_LQuujj2100,recovariable,presentationbinning,selection+"*"+weight,m2100Style,Label)
	h_LQuujj2200 = CreateHisto("h_LQuujj2200","LQuujj2200",t_LQuujj2200,recovariable,presentationbinning,selection+"*"+weight,m2200Style,Label)
	h_LQuujj2300 = CreateHisto("h_LQuujj2300","LQuujj2300",t_LQuujj2300,recovariable,presentationbinning,selection+"*"+weight,m2300Style,Label)
	h_LQuujj2400 = CreateHisto("h_LQuujj2400","LQuujj2400",t_LQuujj2400,recovariable,presentationbinning,selection+"*"+weight,m2400Style,Label)
	h_LQuujj2500 = CreateHisto("h_LQuujj2500","LQuujj2500",t_LQuujj2500,recovariable,presentationbinning,selection+"*"+weight,m2500Style,Label)
	h_LQuujj2600 = CreateHisto("h_LQuujj2600","LQuujj2600",t_LQuujj2600,recovariable,presentationbinning,selection+"*"+weight,m2600Style,Label)

	BeautifyHisto(h_LQuujj2100,Label)
	BeautifyHisto(h_LQuujj2200,Label)
	BeautifyHisto(h_LQuujj2300,Label)
	BeautifyHisto(h_LQuujj2400,Label)
	BeautifyHisto(h_LQuujj2500,Label)
	BeautifyHisto(h_LQuujj2600,Label)
	
	#############################################################################
	#																			#
	#						Create objects for each plot						#
	#																			#
	#############################################################################

	############################################################
	######### Initialize canvases, pads, legends, etc. #########
	######### Customize options for each               #########
	############################################################

	# c1 = main canvas

	c1 = TCanvas("c1","",850,800)

	# Create pads for main and ratio plots per canvas

	pad1_main 	= TPad( 'pad1_main', 'pad1_main', 0.0, 0.0, 1.0, 1.0 )

	# Draw pads

	c1.cd()
	pad1_main.Draw()
	gStyle.SetPadLeftMargin(0.14)
  	gROOT.ForceStyle()

	# Set pad upper and lower margins

	#pad1_main.SetBottomMargin(0.43)	

	# Create each legend and customize options

	leg1 = TLegend(0.5,0.6,0.85,0.85,"","brNDC")


	leg1.SetTextFont(42)
	leg1.SetFillColor(0)
	leg1.SetFillStyle(0)
	leg1.SetBorderSize(0)
	leg1.SetTextSize(.035)


	# For each legend, add an entry for the uncorrected distribution and either:
	# a representative entry for the copies, 
	# or the average over all the copies

	leg1.AddEntry(h_LQuujj2100,"m_{LQ} = 2100 GeV","l")
	leg1.AddEntry(h_LQuujj2200,"m_{LQ} = 2200 GeV","l")
	leg1.AddEntry(h_LQuujj2300,"m_{LQ} = 2300 GeV","l")
	leg1.AddEntry(h_LQuujj2400,"m_{LQ} = 2400 GeV","l")
	leg1.AddEntry(h_LQuujj2500,"m_{LQ} = 2500 GeV","l")
	leg1.AddEntry(h_LQuujj2600,"m_{LQ} = 2600 GeV","l")


	# Declare and customize the LaTeX objects that will be drawn to the pad, 
	# e.g., CMS logo, integrated luminosity, and collision energy

	# Drawn above main pad

	l1_header = TLatex()
	l1_header.SetTextAlign(12)
	l1_header.SetTextFont(42)
	l1_header.SetNDC()
	l1_header.SetTextSize(0.045)

	# Drawn inside main pad

	l1_logo = TLatex()
	l1_logo.SetTextAlign(12)
	l1_logo.SetTextFont(62)
	l1_logo.SetNDC()
	l1_logo.SetTextSize(0.06)

	# Initialize lists for y-axis maxima

	maxList1 = []

	# Get rid of stats box, pad title, etc.,

	gStyle.SetOptStat(0)


	#############################################################################
	#																			#
	#						Draw each plot and save as PDF						#
	#																			#
	#############################################################################

	##################################
	######### GE copies plot #########
	##################################

	c1.cd()

	#############################
	######### Main plot #########
	#############################

	# Switch to main pad, set to log scale

	pad1_main.cd()
	pad1_main.SetLogy()

	# Draw each copy histogram on main pad
	# Modify cosmetics of each histogram with BeautifyHisto()
	# Get the maxima of each histogram

	h_LQuujj2100.Draw("HIST")
	h_LQuujj2200.Draw("HISTSAME")
	h_LQuujj2300.Draw("HISTSAME")
	h_LQuujj2400.Draw("HISTSAME")
	h_LQuujj2500.Draw("HISTSAME")
	h_LQuujj2600.Draw("HISTSAME")

	maxList1.append(h_LQuujj2100.GetMaximum())
	maxList1.append(h_LQuujj2200.GetMaximum())
	maxList1.append(h_LQuujj2300.GetMaximum())
	maxList1.append(h_LQuujj2400.GetMaximum())
	maxList1.append(h_LQuujj2500.GetMaximum())
	maxList1.append(h_LQuujj2600.GetMaximum())

	# Set the maximum on the y-axis shown in the plot 
	# as some multiple of the largest hist maximum

	h_LQuujj2100.SetMaximum(100*max(maxList1))
	
	# Draw legend and LaTeX strings

	leg1.Draw()
	l1_header.DrawLatex(0.12,0.93,"#it{Simulation}                            "+lumiInvfb+" fb^{-1} (13 TeV)")
	l1_logo.DrawLatex(0.15,0.845,"CMS")

	# Update the pad and redraw axis

	gPad.Update()
	gPad.RedrawAxis()

	# Save PDFs

	c1.Print(outDir+"/Mujbj_M2100_to_M2600.pdf")

def PlotM2700toM4000(recovariable,xlabel,presentationbinning,selection,weight,outdir):

	############################################################################
	######### Make plots for muon scale copies and average over copies #########
	######### Include the uncorrected distribution for comparison      #########
	######### Signal samples only								   	   #########
	############################################################################

	#############################################################################
	#																			#
	#						Start with histogram creation						#
	#																			#
	#############################################################################

	# x-axis title and y-axis title

	Label=[xlabel,"Events / bin"]

	# Set style options for average and ratio histograms (den style is a placeholder--will be overridden by numerator style)
	# [fill style, marker style, marker size, line width, marker/line/fill color]

	m2700Style = [0,20,1,2,2] #[no fill, filled circle, normal size, normal width, red]
	m2800Style = [0,20,1,2,3] #[no fill, filled circle, normal size, normal width, green]
	m2900Style = [0,20,1,2,4] #[no fill, filled circle, normal size, normal width, blue]
	m3000Style = [0,20,1,2,6] #[no fill, filled circle, normal size, normal width, magenta]
	m3500Style = [0,20,1,2,7] #[no fill, filled circle, normal size, normal width, cyan]
	m4000Style = [0,20,1,2,28] #[no fill, filled circle, normal size, normal width, brown]

	h_LQuujj2700 = CreateHisto("h_LQuujj2700","LQuujj2700",t_LQuujj2700,recovariable,presentationbinning,selection+"*"+weight,m2700Style,Label)
	h_LQuujj2800 = CreateHisto("h_LQuujj2800","LQuujj2800",t_LQuujj2800,recovariable,presentationbinning,selection+"*"+weight,m2800Style,Label)
	h_LQuujj2900 = CreateHisto("h_LQuujj2900","LQuujj2900",t_LQuujj2900,recovariable,presentationbinning,selection+"*"+weight,m2900Style,Label)
	h_LQuujj3000 = CreateHisto("h_LQuujj3000","LQuujj3000",t_LQuujj3000,recovariable,presentationbinning,selection+"*"+weight,m3000Style,Label)
	h_LQuujj3500 = CreateHisto("h_LQuujj3500","LQuujj3500",t_LQuujj3500,recovariable,presentationbinning,selection+"*"+weight,m3500Style,Label)
	h_LQuujj4000 = CreateHisto("h_LQuujj4000","LQuujj4000",t_LQuujj4000,recovariable,presentationbinning,selection+"*"+weight,m4000Style,Label)

	BeautifyHisto(h_LQuujj2700,Label)
	BeautifyHisto(h_LQuujj2800,Label)
	BeautifyHisto(h_LQuujj2900,Label)
	BeautifyHisto(h_LQuujj3000,Label)
	BeautifyHisto(h_LQuujj3500,Label)
	BeautifyHisto(h_LQuujj4000,Label)
	
	#############################################################################
	#																			#
	#						Create objects for each plot						#
	#																			#
	#############################################################################

	############################################################
	######### Initialize canvases, pads, legends, etc. #########
	######### Customize options for each               #########
	############################################################

	# c1 = main canvas

	c1 = TCanvas("c1","",850,800)

	# Create pads for main and ratio plots per canvas

	pad1_main 	= TPad( 'pad1_main', 'pad1_main', 0.0, 0.0, 1.0, 1.0 )

	# Draw pads

	c1.cd()
	pad1_main.Draw()
	gStyle.SetPadLeftMargin(0.14)
  	gROOT.ForceStyle()

	# Set pad upper and lower margins

	#pad1_main.SetBottomMargin(0.43)	

	# Create each legend and customize options

	leg1 = TLegend(0.5,0.6,0.85,0.85,"","brNDC")


	leg1.SetTextFont(42)
	leg1.SetFillColor(0)
	leg1.SetFillStyle(0)
	leg1.SetBorderSize(0)
	leg1.SetTextSize(.035)


	# For each legend, add an entry for the uncorrected distribution and either:
	# a representative entry for the copies, 
	# or the average over all the copies

	leg1.AddEntry(h_LQuujj2700,"m_{LQ} = 2700 GeV","l")
	leg1.AddEntry(h_LQuujj2800,"m_{LQ} = 2800 GeV","l")
	leg1.AddEntry(h_LQuujj2900,"m_{LQ} = 2900 GeV","l")
	leg1.AddEntry(h_LQuujj3000,"m_{LQ} = 3000 GeV","l")
	leg1.AddEntry(h_LQuujj3500,"m_{LQ} = 3500 GeV","l")
	leg1.AddEntry(h_LQuujj4000,"m_{LQ} = 4000 GeV","l")


	# Declare and customize the LaTeX objects that will be drawn to the pad, 
	# e.g., CMS logo, integrated luminosity, and collision energy

	# Drawn above main pad

	l1_header = TLatex()
	l1_header.SetTextAlign(12)
	l1_header.SetTextFont(42)
	l1_header.SetNDC()
	l1_header.SetTextSize(0.045)

	# Drawn inside main pad

	l1_logo = TLatex()
	l1_logo.SetTextAlign(12)
	l1_logo.SetTextFont(62)
	l1_logo.SetNDC()
	l1_logo.SetTextSize(0.06)

	# Initialize lists for y-axis maxima

	maxList1 = []

	# Get rid of stats box, pad title, etc.,

	gStyle.SetOptStat(0)


	#############################################################################
	#																			#
	#						Draw each plot and save as PDF						#
	#																			#
	#############################################################################

	##################################
	######### GE copies plot #########
	##################################

	c1.cd()

	#############################
	######### Main plot #########
	#############################

	# Switch to main pad, set to log scale

	pad1_main.cd()
	pad1_main.SetLogy()

	# Draw each copy histogram on main pad
	# Modify cosmetics of each histogram with BeautifyHisto()
	# Get the maxima of each histogram

	h_LQuujj2700.Draw("HIST")
	h_LQuujj2800.Draw("HISTSAME")
	h_LQuujj2900.Draw("HISTSAME")
	h_LQuujj3000.Draw("HISTSAME")
	h_LQuujj3500.Draw("HISTSAME")
	h_LQuujj4000.Draw("HISTSAME")

	maxList1.append(h_LQuujj2700.GetMaximum())
	maxList1.append(h_LQuujj2800.GetMaximum())
	maxList1.append(h_LQuujj2900.GetMaximum())
	maxList1.append(h_LQuujj3000.GetMaximum())
	maxList1.append(h_LQuujj3500.GetMaximum())
	maxList1.append(h_LQuujj4000.GetMaximum())

	# Set the maximum on the y-axis shown in the plot 
	# as some multiple of the largest hist maximum

	h_LQuujj2700.SetMaximum(100*max(maxList1))
	
	# Draw legend and LaTeX strings

	leg1.Draw()
	l1_header.DrawLatex(0.12,0.93,"#it{Simulation}                            "+lumiInvfb+" fb^{-1} (13 TeV)")
	l1_logo.DrawLatex(0.15,0.845,"CMS")

	# Update the pad and redraw axis

	gPad.Update()
	gPad.RedrawAxis()

	# Save PDFs

	c1.Print(outDir+"/Mujbj_M2700_to_M4000.pdf")

for ftype in fileTypes:

	# Open all ROOT files for GE copy "copy"
	# Tree names look like, e.g., f_ZJets_GEcopy0
	f = "f_" + ftype
	print 'Opening ', NormalDirectory + '/' + ftype + '.root', ' as ', f
	exec(f + " = TFile.Open(\"" + NormalDirectory + "/" + ftype + ".root\",\"READ\")")

	# Get PhysicalVariables tree from each file of GE copy "copy"
	# Tree names look like, e.g., t_ZJets_GEcopy0
	t = "t_" + ftype
	exec(t + " = " + f + ".Get(\"PhysicalVariables\")")

# Define Binning

lqbinning300 = [-20,0]

for x in range(40):
	lqbinning300.append(lqbinning300[-1]+5+lqbinning300[-1]-lqbinning300[-2])

lqbinning900 = [-20,0]

for x in range(55):
	lqbinning900.append(lqbinning900[-1]+5+lqbinning900[-1]-lqbinning900[-2])

lqbinning1500 = [-20,0]

for x in range(60):
	lqbinning1500.append(lqbinning1500[-1]+5+lqbinning1500[-1]-lqbinning1500[-2])

lqbinning2100 = [-20,0]

for x in range(65):
	lqbinning2100.append(lqbinning2100[-1]+5+lqbinning2100[-1]-lqbinning2100[-2])

lqbinning2700 = [-20,0]

for x in range(70):
	lqbinning2700.append(lqbinning2700[-1]+5+lqbinning2700[-1]-lqbinning2700[-2])

os.system("mkdir "+year)
outDir = year

PlotM300toM800("M_uujj","M_{#mu#mujj} [GeV]",lqbinning300,preselection,eventWeights,outDir)
PlotM900toM1400("M_uujj","M_{#mu#mujj} [GeV]",lqbinning900,preselection,eventWeights,outDir)
PlotM1500toM2000("M_uujj","M_{#mu#mujj} [GeV]",lqbinning1500,preselection,eventWeights,outDir)
PlotM2100toM2600("M_uujj","M_{#mu#mujj} [GeV]",lqbinning2100,preselection,eventWeights,outDir)
PlotM2700toM4000("M_uujj","M_{#mu#mujj} [GeV]",lqbinning2700,preselection,eventWeights,outDir)

