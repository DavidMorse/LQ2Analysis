from ROOT import *
import numpy as np
import os, sys, math, random, platform, time, re
from glob import glob
from array import array

gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")
gROOT.SetStyle('Plain')
gStyle.SetOptTitle(0)
sys.argv.append( '-b' )
TTreeFormula.SetMaxima(100000,1000,1000000)

gStyle.SetPadTopMargin(0.1)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.12)
#gStyle.SetPadRightMargin(0.12)
gStyle.SetPadRightMargin(0.1)

NormalDirectory2016 = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2016/gmadigan/NTupleAnalyzer_nanoAOD_RunFull2016_BDT_FullSys_PDF_stockNano_2022_05_19_19_13_13/DaveSummaryFiles'
NormalDirectory2017 = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/dmorseSkim/2017/NTupleAnalyzer_nanoAOD_RunFull2017_BDT_fullSys_2022_05_20_23_30_36/SummaryFiles'
NormalDirectory2018 = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2018/gmadigan/NTupleAnalyzer_nanoAOD_RunFull2018_BDT_FullSys_PDF_stockNano_2022_05_24_19_50_25/SummaryFiles'

TreeName = "PhysicalVariables"

lumi2016 = 36310. # 1/pb
lumiInvfb2016 = '36.3' # 1/fb

lumi2017 = 41480. # 1/pb
lumiInvfb2017 = '41.5' # 1/fb

lumi2018 = 59830. # 1/pb
lumiInvfb2018 = '59.8' # 1/fb

doubleMuIdSF = '*mu1idSF*mu2idSF'
doubleMuIsoSF = '*mu1isoSF*mu2isoSF'
doubleMuRecoSF = '*mu1recoSF*mu2recoSF'
doublemuHLT = '*(1.0-((1.0-mu1hltSF)*(1.0-mu2hltSF)))'

deepJetWPmedium2016 = '0.3093'
deepJetWPmedium2017 = '0.3033'
deepJetWPmedium2018 = '0.2770'

bTagSFmedium2016 = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium2016+')*bTagSF_jet1)*(1-(DeepJet_jet2>'+deepJetWPmedium2016+')*bTagSF_jet2))'
bTagSFmedium2016Up = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium2016+')*bTagSF_jet1Up)*(1-(DeepJet_jet2>'+deepJetWPmedium2016+')*bTagSF_jet2Up))'
bTagSFmedium2016Down = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium2016+')*bTagSF_jet1Down)*(1-(DeepJet_jet2>'+deepJetWPmedium2016+')*bTagSF_jet2Down))'
bTagselmedium2016 = '*(((DeepJet_jet1>'+deepJetWPmedium2016+')+(DeepJet_jet2>'+deepJetWPmedium2016+'))>0)'

bTagSFmedium2017 = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium2017+')*bTagSF_jet1)*(1-(DeepJet_jet2>'+deepJetWPmedium2017+')*bTagSF_jet2))'
bTagSFmedium2017Up = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium2017+')*bTagSF_jet1Up)*(1-(DeepJet_jet2>'+deepJetWPmedium2017+')*bTagSF_jet2Up))'
bTagSFmedium2017Down = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium2017+')*bTagSF_jet1Down)*(1-(DeepJet_jet2>'+deepJetWPmedium2017+')*bTagSF_jet2Down))'
bTagselmedium2017 = '*(((DeepJet_jet1>'+deepJetWPmedium2017+')+(DeepJet_jet2>'+deepJetWPmedium2017+'))>0)'

bTagSFmedium2018 = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium2018+')*bTagSF_jet1)*(1-(DeepJet_jet2>'+deepJetWPmedium2018+')*bTagSF_jet2))'
bTagSFmedium2018Up = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium2018+')*bTagSF_jet1Up)*(1-(DeepJet_jet2>'+deepJetWPmedium2018+')*bTagSF_jet2Up))'
bTagSFmedium2018Down = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium2018+')*bTagSF_jet1Down)*(1-(DeepJet_jet2>'+deepJetWPmedium2018+')*bTagSF_jet2Down))'
bTagselmedium2018 = '*(((DeepJet_jet1>'+deepJetWPmedium2018+')+(DeepJet_jet2>'+deepJetWPmedium2018+'))>0)'

bTagselmedium = "*((Flag_dataYear2016"+bTagselmedium2016+")+(Flag_dataYear2017"+bTagselmedium2017+")+(Flag_dataYear2018"+bTagselmedium2018+"))"

dataHLT2016 = '(Flag_dataYear2016*((pass_HLTMu50+pass_HLTTkMu50)>0))'
dataHLT2017 = '(Flag_dataYear2017*((pass_HLTMu50+pass_HLTOldMu100+pass_HLTTkMu100)>0))'
dataHLT2018 = '(Flag_dataYear2018*((pass_HLTMu50+pass_HLTOldMu100+pass_HLTTkMu100)>0))'
dataHLT = '*('+dataHLT2016+'+'+dataHLT2017+'+'+dataHLT2018+')'

NormalWeight2016 = "(Flag_dataYear2016*("+str(lumi2016)+"*weight_topPt*prefireWeight"+bTagSFmedium2016+"))"
NormalWeight2017 = "(Flag_dataYear2017*("+str(lumi2017)+"*weight_topPt*prefireWeight"+bTagSFmedium2017+"))"
NormalWeight2018 = "(Flag_dataYear2018*("+str(lumi2018)+"*weight_topPt"+bTagSFmedium2018+"))"

NormalWeightMuMu =	 "("+NormalWeight2016+"+"+NormalWeight2017+"+"+NormalWeight2018+")"+doubleMuRecoSF+doubleMuIsoSF+doubleMuIdSF+doublemuHLT

passfilter =  '*(Flag_goodVertices*(GoodVertexCount>=1))'
passfilter += '*(Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter)'
passfilter += '*(Flag_eeBadScFilter*Flag_EcalDeadCellTriggerPrimitiveFilter)'
passfilter += '*(Flag_globalSuperTightHalo2016Filter)'
passfilter += '*(Flag_BadPFMuonFilter)'

preselectionmumu = '((Pt_muon1>53)*(Pt_muon2>53)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3)*((MuonCount+ElectronCount)<3)'+bTagselmedium+')'

preselectionmumu += passfilter

def ConvertBinning(binning):
	binset=[]
	if len(binning)==3:
		for x in range(binning[0]+1):
			binset.append(((binning[2]-binning[1])/(1.0*binning[0]))*x*1.0+binning[1])
	else:
		binset=binning
	return binset

def blind(h,name,num,tag,chan):
	#print name
	#name = h.GetName()
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
		if name == 'LQToBMu_pair_uubj_BDT_discrim_M300':
			blindstart= -0.8
		elif name == 'LQToBMu_pair_uubj_BDT_discrim_M400':
			blindstart= -0.4
		else:
			blindstart=-0.0001
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
	#h.SetMarkerSize(0.0)
	#h.SetLineWidth(0)

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
	hout.GetXaxis().SetLabelOffset(0.007)
	hout.GetYaxis().SetLabelOffset(0.007)
	hout.GetXaxis().SetLabelSize(0.06)
	hout.GetYaxis().SetLabelSize(0.06)

	hout.GetXaxis().SetTitleOffset(0.92)
	hout.GetYaxis().SetTitleOffset(0.92)
	hout.GetXaxis().SetTitleSize(0.06)
	hout.GetYaxis().SetTitleSize(0.06)
	#hout.GetXaxis().CenterTitle(1)
	#hout.GetYaxis().CenterTitle(1)

	return hout

def BeautifyHisto(histo,style,label):
	histo.SetFillStyle(style[0])
	histo.SetMarkerStyle(style[1])
	histo.SetMarkerSize(style[2])
	histo.SetLineWidth(style[3])
	histo.SetMarkerColor(style[4])
	histo.SetLineColor(style[4])
	histo.SetFillColor(style[4])
	histo.SetFillColor(style[4])
	histo.GetXaxis().SetTitle(label[0])
	histo.GetYaxis().SetTitle(label[1])
	histo.GetXaxis().SetTitleFont(42)
	histo.GetYaxis().SetTitleFont(42)
	histo.GetXaxis().SetLabelFont(42)
	histo.GetYaxis().SetLabelFont(42)

	histo.GetXaxis().SetLabelOffset(0.007)
	histo.GetYaxis().SetLabelOffset(0.007)
	histo.GetXaxis().SetLabelSize(0.0505)
	histo.GetYaxis().SetLabelSize(0.0505)
	histo.GetXaxis().SetTitleOffset(0.925)
	histo.GetYaxis().SetTitleOffset(0.9)
	histo.GetXaxis().SetTitleSize(0.07)
	histo.GetYaxis().SetTitleSize(0.07)
	return histo

zscale2016 = 1.02
zscale2017 = 1.371
zscale2018 = 1.302
ttscale2016 = 0.961
ttscale2017 = 1.061
ttscale2018 = 0.981

def MakePlot(variable, xlabel, binning, selection, weight):

	print '\n\n'
	print 'Using...\n'
	print selection+'*'+weight
	print '\n\n'

	# Style options: [FillStyle, MarkerStyle, MarkerSize, LineWidth, Color]

	# 2016 color: Red (2)
	# 2017 color: Blue (4)
	# 2018 color: Green (3)

	DataStyle2016 = [0,20,1,1,2]
	DataStyle2017 = [0,20,1,1,4]
	DataStyle2018 = [0,20,1,1,3]

	MCstyle2016 = [0,20,.00001,2,2]
	MCstyle2017 = [0,20,.00001,2,4]
	MCstyle2018 = [0,20,.00001,2,3]

	Label = [xlabel,"Relative Events / bin"]

	# Normalization factors

	dataNorm2016 = '0.00005397236' #1./18528.0
	dataNorm2017 = '0.0000421088' #1./23748.0
	dataNorm2018 = '0.00002898886' #1./34496.0

	bkgNorm2016 = '0.00005429676' #1./18417.303226
	bkgNorm2017 = '0.00004258704' #1./23481.3196345
	bkgNorm2018 = '0.00002940938' #1./34002.7562659

	# Create histograms here

	# 2016
	h_Data_2016 = CreateHisto('h_Data_2016', '2016 Data', t_SingleMuData_2016, variable, binning, selection+dataHLT2016+'*'+dataNorm2016, DataStyle2016, Label)
	h_ZJets_2016 = CreateHisto('h_ZJets_2016', '2016 Z+Jets', t_ZJets_2016, variable, binning, selection+'*('+str(zscale2016)+')*'+weight+'*'+bkgNorm2016, MCstyle2016, Label)
	h_TTBar_2016 = CreateHisto('h_TTBar_2016', '2016 t#bar{t}', t_TTBar_2016, variable, binning, selection+'*('+str(ttscale2016)+')*'+weight+'*'+bkgNorm2016, MCstyle2016, Label)
	h_SingleTop_2016 = CreateHisto('h_SingleTop_2016', '2016 SingleTop', t_SingleTop_2016, variable, binning, selection+'*'+weight+'*'+bkgNorm2016, MCstyle2016, Label)
	h_WJets_2016 = CreateHisto('h_WJets_2016', '2016 W+Jets', t_WJets_2016, variable, binning, selection+'*'+weight+'*'+bkgNorm2016, MCstyle2016, Label)
	h_TTV_2016 = CreateHisto('h_TTV_2016', '2016 t#bar{t}V', t_TTV_2016, variable, binning, selection+'*'+weight+'*'+bkgNorm2016, MCstyle2016, Label)
	h_DiBoson_2016 = CreateHisto('h_DiBoson_2016', '2016 DiBoson', t_DiBoson_2016, variable, binning, selection+'*'+weight+'*'+bkgNorm2016, MCstyle2016, Label)

	#2017

	h_Data_2017 = CreateHisto('h_Data_2017', '2017 Data', t_SingleMuData_2017, variable, binning, selection+dataHLT2017+'*'+dataNorm2017, DataStyle2017, Label)
	h_ZJets_2017 = CreateHisto('h_ZJets_2017', '2017 Background', t_ZJets_2017, variable, binning, selection+'*('+str(zscale2017)+')*'+weight+'*'+bkgNorm2017, MCstyle2017, Label)
	h_TTBar_2017 = CreateHisto('h_TTBar_2017', '2017 Background', t_TTBar_2017, variable, binning, selection+'*('+str(ttscale2017)+')*'+weight+'*'+bkgNorm2017, MCstyle2017, Label)
	h_SingleTop_2017 = CreateHisto('h_SingleTop_2017', '2017 Background', t_SingleTop_2017, variable, binning, selection+'*'+weight+'*'+bkgNorm2017, MCstyle2017, Label)
	h_WJets_2017 = CreateHisto('h_WJets_2017', '2017 Background', t_WJets_2017, variable, binning, selection+'*'+weight+'*'+bkgNorm2017, MCstyle2017, Label)
	h_TTV_2017 = CreateHisto('h_TTV_2017', '2017 Background', t_TTV_2017, variable, binning, selection+'*'+weight+'*'+bkgNorm2017, MCstyle2017, Label)
	h_DiBoson_2017 = CreateHisto('h_DiBoson_2017', '2017 Background', t_DiBoson_2017, variable, binning, selection+'*'+weight+'*'+bkgNorm2017, MCstyle2017, Label)
	
	#2018
	h_Data_2018 = CreateHisto('h_Data_2018', '2018 Data', t_SingleMuData_2018, variable, binning, selection+dataHLT2018+'*'+dataNorm2018, DataStyle2018, Label)
	h_ZJets_2018 = CreateHisto('h_ZJets_2018', '2018 Background', t_ZJets_2018, variable, binning, selection+'*('+str(zscale2018)+')*'+weight+'*'+bkgNorm2018, MCstyle2018, Label)
	h_TTBar_2018 = CreateHisto('h_TTBar_2018', '2018 Background', t_TTBar_2018, variable, binning, selection+'*('+str(ttscale2018)+')*'+weight+'*'+bkgNorm2018, MCstyle2018, Label)
	h_SingleTop_2018 = CreateHisto('h_SingleTop_2018', '2018 Background', t_SingleTop_2018, variable, binning, selection+'*'+weight+'*'+bkgNorm2018, MCstyle2018, Label)
	h_WJets_2018 = CreateHisto('h_WJets_2018', '2018 Background', t_WJets_2018, variable, binning, selection+'*'+weight+'*'+bkgNorm2018, MCstyle2018, Label)
	h_TTV_2018 = CreateHisto('h_TTV_2018', '2018 Background', t_TTV_2018, variable, binning, selection+'*'+weight+'*'+bkgNorm2018, MCstyle2018, Label)
	h_DiBoson_2018 = CreateHisto('h_DiBoson_2018', '2018 Background', t_DiBoson_2018, variable, binning, selection+'*'+weight+'*'+bkgNorm2018, MCstyle2018, Label)


	# Merge background histograms into one histogram per year (named ZJets)

	h_ZJets_2016.Add(h_TTBar_2016)
	h_ZJets_2016.Add(h_SingleTop_2016)
	h_ZJets_2016.Add(h_WJets_2016)
	h_ZJets_2016.Add(h_TTV_2016)
	h_ZJets_2016.Add(h_DiBoson_2016)
	h_ZJets_2016.SetTitle("2016 background")

	h_ZJets_2017.Add(h_TTBar_2017)
	h_ZJets_2017.Add(h_SingleTop_2017)
	h_ZJets_2017.Add(h_WJets_2017)
	h_ZJets_2017.Add(h_TTV_2017)
	h_ZJets_2017.Add(h_DiBoson_2017)
	h_ZJets_2017.SetTitle("2017 background")

	h_ZJets_2018.Add(h_TTBar_2018)
	h_ZJets_2018.Add(h_SingleTop_2018)
	h_ZJets_2018.Add(h_WJets_2018)
	h_ZJets_2018.Add(h_TTV_2018)
	h_ZJets_2018.Add(h_DiBoson_2018)
	h_ZJets_2018.SetTitle("2018 background")

	# Create canvas and pad

	c1 = TCanvas("c1","",800,800)

	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.3, 1.0, 1.0)
	pad2 = TPad( 'pad2', 'pad2', 0.0, 0.0, 1.0, 0.3)

	pad1.Draw()
	pad2.Draw()
	
	pad1.SetBottomMargin(0.0)
	pad2.SetTopMargin(0.0)
	pad2.SetBottomMargin(0.43)

	gStyle.SetOptStat(0)

	pad1.cd()
	c1.cd(1)
	c1.cd(1).SetLogy()

	# Draw background

	h_ZJets_2016.Draw("HIST")
	h_ZJets_2017.Draw("HISTSAME")
	h_ZJets_2018.Draw("HISTSAME")

	BeautifyHisto(h_ZJets_2016,MCstyle2016,Label)
	BeautifyHisto(h_ZJets_2017,MCstyle2017,Label)
	BeautifyHisto(h_ZJets_2018,MCstyle2018,Label)

	blind(h_Data_2016,variable,1,'standard','uujj')
	blind(h_Data_2017,variable,1,'standard','uujj')
	blind(h_Data_2018,variable,1,'standard','uujj')

	# Draw data

	h_Data_2016.Draw("ZE0PSAME")
	h_Data_2017.Draw("ZE0PSAME")
	h_Data_2018.Draw("ZE0PSAME")

	# Legend

	leg1 = TLegend(0.43,0.53,0.89,0.89,"","brNDC")
	leg1.SetTextFont(42)
	leg1.SetFillColor(0)
	leg1.SetFillStyle(0)
	leg1.SetBorderSize(0)
	leg1.SetTextSize(.05)
	leg1.AddEntry(h_Data_2016,"2016 Data, "+lumiInvfb2016+" fb^{-1}","lpe")
	leg1.AddEntry(h_Data_2017,"2017 Data, "+lumiInvfb2017+" fb^{-1}","lpe")
	leg1.AddEntry(h_Data_2018,"2018 Data, "+lumiInvfb2018+" fb^{-1}","lpe")
	leg1.AddEntry(h_ZJets_2016,"2016 Background MC","l")
	leg1.AddEntry(h_ZJets_2017,"2017 Background MC","l")
	leg1.AddEntry(h_ZJets_2018,"2018 Background MC","l")
	leg1.Draw()


	sqrts = "#sqrt{s} = 13 TeV"
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
	
	l1.DrawLatex(0.12,0.94,"#it{Preliminary}                                           (13 TeV)")
	l2.DrawLatex(0.15,0.84,"CMS")

	# Set y-axis max and min

	gPad.Update()
	gPad.RedrawAxis()

	yaxismin = .0000013333
	h_ZJets_2016.SetMinimum(yaxismin)
	h_ZJets_2016.SetMaximum(100*h_ZJets_2018.GetMaximum())

	#if 'control' in tagname:
	#	h_ZJets_2018.SetMaximum(100000*h_Data_2018.GetMaximum())
	#if 'St' in recovariable or 'GoodVertex' in recovariable:
	#	h_ZJets_2018.SetMaximum(250*h_Data_2018.GetMaximum())
	#if 'GoodVertex' in recovariable and 'linscale' in tagname:
	#	h_ZJets_2018.SetMaximum(2.0*h_Data_2018.GetMaximum())
	#if 'St' in recovariable and 'final' in tagname:
	#	h_ZJets_2018.SetMaximum(50*hs_rec_Signal.GetMaximum())
	#if 'DPhi' in recovariable or ('MT' in recovariable and 'control' in tagname):
	#	h_ZJets_2018.SetMaximum(2.0*h_Data_2018.GetMaximum())

	#gPad.Update()

	pad2.cd()
	pad2.SetGrid()

	RatHistDen2016 =CreateHisto('RatHisDen2016','RatHistDen2016',t_SingleMuData_2016,variable,binning,'0',DataStyle2016,Label)
	RatHistDen2016.Sumw2()
	RatHistNum2016 =CreateHisto('RatHisNum2016','RatHistNum2016',t_SingleMuData_2016,variable,binning,'0',DataStyle2016,Label)
	RatHistNum2016.Sumw2()
	RatHistDen2016.Add(h_ZJets_2016)
	RatHistNum2016.Add(h_Data_2016)
	RatHistNum2016.Divide(RatHistDen2016)

	RatHistNum2016.SetMaximum(1.599)#fixme was 1.499
	RatHistNum2016.SetMinimum(0.401)#fixme was 0.501
	RatHistNum2016.GetXaxis().SetTitle(xlabel)
	RatHistNum2016.GetYaxis().SetTitleFont(42)
	RatHistNum2016.GetYaxis().SetTitle('Data/MC')
	RatHistNum2016.GetYaxis().SetNdivisions(308,True)
	RatHistNum2016.GetXaxis().SetTitleSize(0.14)
	RatHistNum2016.GetYaxis().SetTitleSize(.12)	
	RatHistNum2016.GetXaxis().SetTitleOffset(0.)
	RatHistNum2016.GetYaxis().SetTitleOffset(.45)
	RatHistNum2016.GetYaxis().SetLabelSize(.1)
	RatHistNum2016.GetXaxis().SetLabelSize(.09)
	
	#unity=TLine(RatHistNum2016.GetXaxis().GetXmin(), 1.0 , RatHistNum2016.GetXaxis().GetXmax(),1.0)
	#unity.Draw()

	blind(RatHistNum2016,variable,2,'standard','uujj')#fixme
	RatHistNum2016.Draw("PE0")

	RatHistDen2016.SetMarkerSize(0)
	RatHistDen2016.SetFillColor(17)
	RatHistDen2016.SetFillStyle(3105)
	for bin in range(RatHistDen2016.GetNbinsX()+1) :
		if bin==0: continue
		x = RatHistDen2016.GetBinContent(bin)
		err = RatHistDen2016.GetBinError(bin)
		if x==0: err=0
		else: err = err/x
		RatHistDen2016.SetBinError(bin,err)
		RatHistDen2016.SetBinContent(bin,1)
	RatHistNum2016.Draw("PE0SAMES")



	RatHistDen2017 =CreateHisto('RatHisDen2017','RatHistDen2017',t_SingleMuData_2017,variable,binning,'0',DataStyle2017,Label)
	RatHistDen2017.Sumw2()
	RatHistNum2017 =CreateHisto('RatHisNum2017','RatHistNum2017',t_SingleMuData_2017,variable,binning,'0',DataStyle2017,Label)
	RatHistNum2017.Sumw2()
	RatHistDen2017.Add(h_ZJets_2017)
	RatHistNum2017.Add(h_Data_2017)
	RatHistNum2017.Divide(RatHistDen2017)

	RatHistNum2017.SetMaximum(1.599)#fixme was 1.499
	RatHistNum2017.SetMinimum(0.401)#fixme was 0.501
	RatHistNum2017.GetXaxis().SetTitle(xlabel)
	RatHistNum2017.GetYaxis().SetTitleFont(42)
	RatHistNum2017.GetYaxis().SetTitle('Data/MC')
	RatHistNum2017.GetYaxis().SetNdivisions(308,True)
	RatHistNum2017.GetXaxis().SetTitleSize(0.14)
	RatHistNum2017.GetYaxis().SetTitleSize(.12)	
	RatHistNum2017.GetXaxis().SetTitleOffset(0.)
	RatHistNum2017.GetYaxis().SetTitleOffset(.45)
	RatHistNum2017.GetYaxis().SetLabelSize(.1)
	RatHistNum2017.GetXaxis().SetLabelSize(.09)
	

	blind(RatHistNum2017,variable,2,'standard','uujj')#fixme
	RatHistNum2017.Draw("PE0SAMES")

	RatHistDen2017.SetMarkerSize(0)
	RatHistDen2017.SetFillColor(17)
	RatHistDen2017.SetFillStyle(3105)
	for bin in range(RatHistDen2017.GetNbinsX()+1) :
		if bin==0: continue
		x = RatHistDen2017.GetBinContent(bin)
		err = RatHistDen2017.GetBinError(bin)
		if x==0: err=0
		else: err = err/x
		RatHistDen2017.SetBinError(bin,err)
		RatHistDen2017.SetBinContent(bin,1)
	RatHistNum2017.Draw("PE0SAMES")


	RatHistDen2018 =CreateHisto('RatHisDen2018','RatHistDen2018',t_SingleMuData_2018,variable,binning,'0',DataStyle2018,Label)
	RatHistDen2018.Sumw2()
	RatHistNum2018 =CreateHisto('RatHisNum2018','RatHistNum2018',t_SingleMuData_2018,variable,binning,'0',DataStyle2018,Label)
	RatHistNum2018.Sumw2()
	RatHistDen2018.Add(h_ZJets_2018)
	RatHistNum2018.Add(h_Data_2018)
	RatHistNum2018.Divide(RatHistDen2018)

	RatHistNum2018.SetMaximum(1.599)#fixme was 1.499
	RatHistNum2018.SetMinimum(0.401)#fixme was 0.501
	RatHistNum2018.GetXaxis().SetTitle(xlabel)
	RatHistNum2018.GetYaxis().SetTitleFont(42)
	RatHistNum2018.GetYaxis().SetTitle('Data/MC')
	RatHistNum2018.GetYaxis().SetNdivisions(308,True)
	RatHistNum2018.GetXaxis().SetTitleSize(0.14)
	RatHistNum2018.GetYaxis().SetTitleSize(.12)	
	RatHistNum2018.GetXaxis().SetTitleOffset(0.)
	RatHistNum2018.GetYaxis().SetTitleOffset(.45)
	RatHistNum2018.GetYaxis().SetLabelSize(.1)
	RatHistNum2018.GetXaxis().SetLabelSize(.09)
	

	blind(RatHistNum2018,variable,2,'standard','uujj')#fixme
	RatHistNum2018.Draw("PE0SAMES")

	RatHistDen2018.SetMarkerSize(0)
	RatHistDen2018.SetFillColor(17)
	RatHistDen2018.SetFillStyle(3105)
	for bin in range(RatHistDen2018.GetNbinsX()+1) :
		if bin==0: continue
		x = RatHistDen2018.GetBinContent(bin)
		err = RatHistDen2018.GetBinError(bin)
		if x==0: err=0
		else: err = err/x
		RatHistDen2018.SetBinError(bin,err)
		RatHistDen2018.SetBinContent(bin,1)
	RatHistNum2018.Draw("PE0SAMES")

	gPad.Update()

	# Save plot as a pdf and png

	c1.Print('AllYearsOverlay_'+variable+'.pdf')
	c1.Print('AllYearsOverlay_'+variable+'.png')
	print 'AllYearsOverlay_'+variable+'.pdf'

"""
	c2 = TCanvas("c2","",800,800)
	pad2 = TPad( 'pad2', 'pad2', 0.0, 0.0, 1.0, 1.0)
	pad2.Draw()
	pad2.SetBottomMargin(0.0)
	pad2.SetBottomMargin(0.0)
	gStyle.SetOptStat(0)
	pad2.cd()
	c2.cd(1)
	c2.cd(1).SetLogy()

	# Blind data

	blinded = True
	if blinded: 
		blind(h_Data_2016,variable,1,'standard','uujj')
		blind(h_Data_2017,variable,1,'standard','uujj')
		blind(h_Data_2018,variable,1,'standard','uujj')

	# Draw data

	h_Data_2016.Draw("ZE0P")
	h_Data_2017.Draw("ZE0PSAME")
	h_Data_2018.Draw("ZE0PSAME")

	leg2 = TLegend(0.43,0.53,0.89,0.89,"","brNDC")
	leg2.SetTextFont(42)
	leg2.SetFillColor(0)
	leg2.SetFillStyle(0)
	leg2.SetBorderSize(0)
	leg2.SetTextSize(.05)
	leg2.AddEntry(h_Data_2016,"2016 Data","lpe")
	leg2.AddEntry(h_Data_2017,"2017 Data","lpe")
	leg2.AddEntry(h_Data_2018,"2018 Data","lpe")
	leg2.Draw()

	gPad.Update()
	gPad.RedrawAxis()

	yaxismin = .13333
	h_Data_2016.SetMinimum(yaxismin)
	h_Data_2016.SetMaximum(1000*h_Data_2016.GetMaximum())


	c2.Print('AllYearsOverlayData_'+variable+'.pdf')
	c2.Print('AllYearsOverlayData_'+variable+'.png')
	print 'AllYearsOverlayData_'+variable+'.pdf'
"""
# Get trees
NormalFiles2016 = [ff.replace('\n','') for ff in os.popen('ls '+NormalDirectory2016+"| grep \".root\"").readlines()]
NormalFiles2017 = [ff.replace('\n','') for ff in os.popen('ls '+NormalDirectory2017+"| grep \".root\"").readlines()]
NormalFiles2018 = [ff.replace('\n','') for ff in os.popen('ls '+NormalDirectory2018+"| grep \".root\"").readlines()]

for f in NormalFiles2016:
	_tree = 't_'+f.split('/')[-1].replace(".root","")+"_2016"
	_treeTmp = _tree+"_tmp"
	_prefix = ''
	print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory2016+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory2016+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

for f in NormalFiles2017:
	_tree = 't_'+f.split('/')[-1].replace(".root","")+"_2017"
	_treeTmp = _tree+"_tmp"
	_prefix = ''
	print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory2017+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory2017+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

for f in NormalFiles2018:
	_tree = 't_'+f.split('/')[-1].replace(".root","")+"_2018"
	_treeTmp = _tree+"_tmp"
	_prefix = ''
	print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory2018+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory2018+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

# binning

stbinning = [280 ,300]
for x in range(29):#was 22 then 27
	stbinning.append(stbinning[-1]+10+stbinning[-1]-stbinning[-2])
stbinning = stbinning[1:]

# Plot variables

MakePlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu)
