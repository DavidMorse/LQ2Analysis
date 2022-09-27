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


# Define copies to iterate here:
loop = []
for i in range(50):
	loop.append(i)
loop.append(50)

# Set the data year here:
year = '2016'

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
eventWeights = str(lumi)+'*weight_central'+doublemuHLT+doubleMuRecoSF+doubleMuIsoSF+doubleMuIdSF+bTagSFmedium
if year == '2016' or year == '2017': eventWeights+='*prefireWeight'

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

# Path to subdirectories
inputPath = "/eos/user/g/gmadigan/MES_Syst_Study"

# Generic name for subdirectory (same for all GE copies)
dirPrefix = "NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy"

# Subdirectory time stamp (same for all GE copies)
timeStamp = "_2022_02_23_22_53_17"
summaryDir = "SummaryFiles"

# Store full path of all 51 subdirectories as values in dict, with copy index as key
directories = {str(copy):inputPath+'/'+dirPrefix+str(copy)+timeStamp+'/'+summaryDir for copy in range(51)}

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

fileTypes = bkgTypes+sigTypes

lqMasses = ['300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2100','2200','2300','2400','2500','2600','2700','2800','2900','3000','3500','4000']


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
	histo.GetXaxis().SetLabelSize(0.0505)
	histo.GetYaxis().SetLabelSize(0.0505)

	histo.GetXaxis().SetTitleOffset(0.925)
	histo.GetYaxis().SetTitleOffset(0.9)
	histo.GetXaxis().SetTitleSize(0.07)
	histo.GetYaxis().SetTitleSize(0.07)

def BeautifyRatio(num,den,xlabel,style):
	num.SetMaximum(1.999)#fixme was 1.499
	num.SetMinimum(0.001)#fixme was 0.501
	num.GetYaxis().SetTitleFont(42)
	num.GetXaxis().SetTitle('')
	num.GetYaxis().SetTitle('variation')
	num.GetXaxis().SetTitle(xlabel)
	num.GetYaxis().SetTitleFont(42)
	num.GetYaxis().SetTitle('variation')
	num.GetYaxis().SetNdivisions(306,True)
	num.GetXaxis().SetTitleSize(0.14)
	num.GetYaxis().SetTitleSize(.12)

	num.GetYaxis().CenterTitle()		
	num.GetXaxis().SetTitleOffset(0.)
	num.GetYaxis().SetTitleOffset(.45)
	num.GetYaxis().SetLabelSize(.1)
	num.GetXaxis().SetLabelSize(.09)
	num.SetMarkerSize(style[2])
	num.SetMarkerColor(style[4])
	num.SetFillColor(style[4])
	num.SetFillStyle(style[0])
	num.SetMarkerStyle(style[1])
	den.SetMarkerSize(style[2])
	den.SetMarkerColor(style[4])
	den.SetFillColor(style[4])
	den.SetFillStyle(style[0])
	den.SetMarkerStyle(style[1])

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

def GetScaleFactors(n1,n2,a1,a2,b1,b2,o1,o2):
	Ra = 1.0
	Rb = 1.0
	for x in range(10):
		Ra = (n1 - Rb*b1 - o1)/(a1)
		Rb = (n2 - Ra*a2 - o2)/(b2) 
	return [Ra, Rb]

def RR(List):
	return random.gauss(List[0],List[1])

def GetStats(List):
	av = 0.0
	n = 1.0*len(List)
	for x in List:
		av += x
	av = av/n
	dev = 0.0
	while True:
		N=0
		dev += 0.00001
		for x in List:
			if abs(x-av)<dev:
				N+= 1
		if N>.68*len(List):
			break
	return [av,dev, str(round(av,3)) +' +- '+str(round(dev,3))]


def GetMuMuScaleFactors( selection, controlregion_1, controlregion_2, isQuick, icopy):

	selection_data = selection.split('*(fact')[0]
	selection_data = selection.split('*scaleWeight')[0]

	N1 = QuickEntries(t_SingleMuData,selection_data + '*' + controlregion_1+dataHLT,1.0)
	print selection_data + '*' + controlregion_1+dataHLT
	N2 = QuickEntries(t_SingleMuData,selection_data + '*' + controlregion_2+dataHLT,1.0)

	exec("Z1 = QuickIntegral(t_ZJets_GEcopy"+str(icopy)+",selection + '*' + controlregion_1,1.0)")
	exec("T1 = QuickIntegral(t_TTBar_GEcopy"+str(icopy)+",selection + '*' + controlregion_1,1.0)")
	exec("s1 = QuickIntegral(t_SingleTop_GEcopy"+str(icopy)+",selection + '*' + controlregion_1,1.0)")
	exec("w1 = QuickIntegral(t_WJets_GEcopy"+str(icopy)+",selection + '*' + controlregion_1,1.0)")
	exec("v1 = QuickIntegral(t_DiBoson_GEcopy"+str(icopy)+",selection + '*' + controlregion_1,1.0)")
	exec("ttv1 = QuickIntegral(t_TTV_GEcopy"+str(icopy)+",selection + '*' + controlregion_1,1.0)")

	exec("Z2 = QuickIntegral(t_ZJets_GEcopy"+str(icopy)+",selection + '*' + controlregion_2,1.0)")
	exec("T2 = QuickIntegral(t_TTBar_GEcopy"+str(icopy)+",selection + '*' + controlregion_2,1.0)")
	exec("s2 = QuickIntegral(t_SingleTop_GEcopy"+str(icopy)+",selection + '*' + controlregion_2,1.0)")
	exec("w2 = QuickIntegral(t_WJets_GEcopy"+str(icopy)+",selection + '*' + controlregion_2,1.0)")
	exec("v2 = QuickIntegral(t_DiBoson_GEcopy"+str(icopy)+",selection + '*' + controlregion_2,1.0)")
	exec("ttv2 = QuickIntegral(t_TTV_GEcopy"+str(icopy)+",selection + '*' + controlregion_2,1.0)")

	Other1 = [ s1[0]+w1[0]+v1[0]+ttv1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] + ttv1[1]*ttv1[1]) ]
	Other2 = [ s2[0]+w2[0]+v2[0]+ttv2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] + ttv2[1]*ttv2[1]) ]
	zvals = []
	tvals = []

	if isQuick: loops=50
	else: loops=10000
	for x in range(loops):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(Z1),RR(Z2),RR(T1),RR(T2),Other1[0],Other2[0]))
		#print x,": R_Z:",variation[0]
		#print x,": R_tt:",variation[1]
		zvals.append(variation[0])
		tvals.append(variation[1])

	zout =  GetStats(zvals)
	tout = GetStats(tvals)


	print 'MuMu scale factor integrals:'
	print 'Data:',N1,N2
	print 'Z:',Z1,Z2
	print 'TT:',T1,T2
	print 'ST:',s1,s2
	print 'W:',w1,w2
	print 'VV:',v1,v2
	print 'TTV:',ttv1,ttv2
	print 'Other:',Other1,Other2


	print 'MuMu: RZ  = ', zout[-1]
	print 'MuMu: Rtt = ', tout[-1]
	return [ [ zout[0], zout[1] ] , [ tout[0],tout[1] ] ]


def GetGEScaleSystematic(mass,selection,weight,bkgnormsf_name,json_name):
	
	mass_dir = str(mass)
	os.system('mkdir '+mass_dir)
	data_dir = mass_dir+'/data'
	os.system('mkdir '+data_dir)

	bkgList = ['ZJets','TTBar','SingleTop','WJets','DiBoson','TTV']
	signalList = ['LQuujj'+mass]
	sampleList = bkgList+signalList

	if json_name is '':
		print 'Using selection:'
		print selection + finalSelCut[str(mass)] + '*' + weight
		print ''
		print 'Doing QuickIntegrals...'
		data = {}
		for icopy in loop:
			with open(bkgnormsf_name,'r') as infile: 
				bkgnormsf = json.load(infile)
			R_z = bkgnormsf['50']['R_z']
			R_tt = bkgnormsf['50']['R_tt']
			print 'R_z of GE copy ',str(icopy),' is ',R_z
			print 'R_tt of GE copy ',str(icopy),' is ',R_tt
			data[str(icopy)] = {}
			for sample in sampleList:
				print 'Getting Integral for GE copy ',str(icopy),' of ',sample,'...\n'
				if 'ZJets' in sample:exec("data['"+str(icopy)+"']['"+sample+"'] = QuickIntegral(t_"+sample+"_GEcopy"+str(icopy)+", selection + finalSelCut['"+str(mass)+"'] + '*' + weight, "+str(R_z)+")")
				elif 'TTBar' in sample:exec("data['"+str(icopy)+"']['"+sample+"'] = QuickIntegral(t_"+sample+"_GEcopy"+str(icopy)+", selection + finalSelCut['"+str(mass)+"'] + '*' + weight, "+str(R_tt)+")")
				else: exec("data['"+str(icopy)+"']['"+sample+"'] = QuickIntegral(t_"+sample+"_GEcopy"+str(icopy)+", selection + finalSelCut['"+str(mass)+"'] + '*' + weight, 1.0)")
				print '[Integral, Error] = ',data[str(icopy)][sample],'\n'

		json_name = 'QuickIntegrals_GEcopies_FinalSel_M'+mass+'.json'

		print 'Saving integrals to json file: ',data_dir+'/'+json_name,'\n'

		with open(data_dir+'/'+json_name, 'w') as outfile:
			json.dump(data, outfile, indent=4)

	print 'Reading json file: ',data_dir+'/'+json_name,'\n'

	with open(data_dir+'/'+json_name, 'r') as infile:
		json_data =	json.load(infile)

	bkgNom = 0.0
	sigNom = 0.0
	bkgGEcopyMean = 0.0
	sigGEcopyMean = 0.0
	Ncopies = 0

	print 'Doing calculations...\n'
	for icopy in loop:
		for sample in sampleList:
			if icopy is 50:
				if sample in bkgList:
					bkgNom += json_data[str(icopy)][sample][0]
				elif sample in signalList:
					sigNom += json_data[str(icopy)][sample][0]
			else:
				Ncopies += 1
				if sample in bkgList:
					bkgGEcopyMean += json_data[str(icopy)][sample][0]
				elif sample in signalList:
					sigGEcopyMean += json_data[str(icopy)][sample][0]
	
	bkgGEcopyMean *= 0.02
	sigGEcopyMean *= 0.02

	bkgDiff = abs(bkgNom-bkgGEcopyMean)
	sigDiff = abs(sigNom-sigGEcopyMean)

	bkgSyst = 100.0*bkgDiff/bkgNom
	sigSyst = 100.0*sigDiff/sigNom

	results_name = mass_dir+'/SystematicResults.txt'

	print 'Writing results to txt file: ',results_name
	with open(results_name,'w') as outfile:
		outfile.write('Final selection cut: '+finalSelCut[str(mass)]+'\n')
		outfile.write('Total area of background (nominal): '+str(bkgNom)+'\n')
		outfile.write('Total area of background (GE copy average): '+str(bkgGEcopyMean)+'\n')
		outfile.write('Total area of signal (nominal): '+str(sigNom)+'\n')
		outfile.write('Total area of signal (GE copy average): '+str(sigGEcopyMean)+'\n')
		outfile.write('Difference in background area: '+str(bkgDiff)+'\n')
		outfile.write('Difference in signal area: '+str(sigDiff)+'\n')
		outfile.write('Systematic on background (percent): '+str(bkgSyst)+'\n')
		outfile.write('Systematic on signal (percent): '+str(sigSyst)+'\n')

	print ''
	print 'Results of Muon Energy Scale systematic study using GE method:'
	print ''
	print 'Final selection cut: ',finalSelCut[str(mass)]
	print ''
	print 'Normalization Scale Factors [[R_z, R_z_err],[R_tt, R_tt_err]] = ',
	print ''
	print 'Total area of background (nominal): ',bkgNom
	print 'Total area of background (GE copy average): ',bkgGEcopyMean
	print 'Total area of signal (nominal): ',sigNom
	print 'Total area of signal (GE copy average): ',sigGEcopyMean
	print ''
	print 'Difference in background area: ',bkgDiff
	print 'Difference in signal area: ',sigDiff
	print ''
	print 'Systematic on background: ',round(bkgSyst,2),'%'
	print 'Systematic on signal: ',round(sigSyst,2),'%'
	print ''
	print 'Saved output to ',results_name
	print ''
	print 'Done.'

def MakeBackgroundPlots(recovariable,xlabel,presentationbinning,selection,weight,bkgnormsf,outdir):

	############################################################################
	######### Make plots for muon scale copies and average over copies #########
	######### Include the uncorrected distribution for comparison      #########
	######### Background samples only							       #########
	############################################################################

	#############################################################################
	#																			#
	#						Start with histogram creation						#
	#																			#
	#############################################################################

	# Get selection type (final or pre), if final, get signal mass

	cutMass = ""
	if "LQToBMu_pair_uubj_BDT_discrim_M" in selection: 
		cutMass = selection.split("LQToBMu_pair_uubj_BDT_discrim_M")[-1].split(">")[0].strip()
		selectionType = "finalSel"+"_M"+cutMass
	else: selectionType = "preSel"

	print ""
	print "Creating plot: GEScaleSystStudyPlot_2016_Background_Copies_"+selectionType+"_"+recovariable+".pdf"
	print "Creating plot: GEScaleSystStudyPlot_2016_Background_Average_"+selectionType+"_"+recovariable+".pdf"
	print ""
	# x-axis title and y-axis title

	Label=[xlabel,"Events / bin"]

	# Weight for calculating average over GE copies

	nCopies = len(loop)-1
	averageWeight = 1.0/float(nCopies)

	# Set style options for average and ratio histograms (den style is a placeholder--will be overridden by numerator style)
	# [fill style, marker style, marker size, line width, marker/line/fill color]

	averageStyle = [0,20,1,1,2] #[no fill, filled circle, normal size, normal width, red]
	ratioDenStyle = [0,20,1,1,1] #[no fill, filled circle, normal size, normal width, black]

	# Create empty histograms for denominators of each copy for ratio subplots (uncorrected MC)
	# Create empty histograms for average over GE copies
	# Create empty histograms for denominators of average ofer copies for ratio subplots (uncorrected MC)

	h_ratioDen = CreateHisto("h_ratioDen","ratioDen",t_SingleMuData,recovariable,presentationbinning,"0",ratioDenStyle,Label)
	h_average = CreateHisto("h_average","average",t_SingleMuData,recovariable,presentationbinning,"0",averageStyle,Label)
	h_averageRatioDen = CreateHisto("h_averageRatioDen","averageRatioDen",t_SingleMuData,recovariable,presentationbinning,"0",ratioDenStyle,Label)

	##############################################
	######### Loop over each GE copy     #########
	######### Create histograms for each #########
	##############################################

	for icopy in loop:

		##############################
		######### Main plots #########
		##############################

		# Marker colors for copies and uncorrected MC

		if icopy%5 == 0: copyColor = 2 # Red
		elif icopy%5 == 1: copyColor = 3 # Blue
		elif icopy%5 == 2: copyColor = 4 # Green
		elif icopy%5 == 3: copyColor = 6 # Magenta
		elif icopy%5 == 4: copyColor = 7 # Cyan
		if icopy == 50: copyColor = 1 # Black (uncorrected MC)

		# [fill style, marker style, marker size, line width, marker/line/fill color]	

		copyStyle = [0,20,1,1,copyColor] #[no fill, filled circle, normal size, normal width, color will vary]

		# Background normalization scale factors

		zscale = bkgnormsf["R_z"]
		ttscale = bkgnormsf["R_tt"]
		
		# Create hist for each background sample (Z+Jets, TTBar, SingleTop, W+Jets, DiBoson, and TTV)
		# Creates an empty TH1D and projects recovariable from tree with selection and weights onto TH1D (defined in CreateHisto)

		for ftype in bkgTypes:

			# Get the name of the background tree to project and name the histogram

			name = ftype + "_GEcopy" + str(icopy)
			tname = "t_" + name
			hname = "h_" + name

			sys.stdout.write("\x1b[1K\rCreating: "+hname)
			sys.stdout.flush()

			# Z+Jets and TTBar have different selection (bkg norm SFs) so need conditional

			if 'ZJets' in name: exec(hname + " = CreateHisto(\"" + hname + "\",\"" + name + "\"," + tname + ",recovariable,presentationbinning,selection + \"*(\" + str(zscale) + \")*\" + weight,copyStyle,Label)")
			elif 'TTBar' in name: exec(hname + " = CreateHisto(\"" + hname + "\",\"" + name + "\"," + tname + ",recovariable,presentationbinning,selection + \"*(\" + str(ttscale) + \")*\" + weight,copyStyle,Label)")
			else: exec(hname + " = CreateHisto(\"" + hname + "\",\"" + name + "\"," + tname + ",recovariable,presentationbinning,selection + \"*\" + weight,copyStyle,Label)")
		
		# Combine all background histograms (store in Z+Jets)

		exec("h_ZJets_GEcopy"+str(icopy)+".Add(h_TTBar_GEcopy"+str(icopy)+")")
		exec("h_ZJets_GEcopy"+str(icopy)+".Add(h_SingleTop_GEcopy"+str(icopy)+")")
		exec("h_ZJets_GEcopy"+str(icopy)+".Add(h_WJets_GEcopy"+str(icopy)+")")
		exec("h_ZJets_GEcopy"+str(icopy)+".Add(h_TTV_GEcopy"+str(icopy)+")")
		exec("h_ZJets_GEcopy"+str(icopy)+".Add(h_DiBoson_GEcopy"+str(icopy)+")")

		#######################################
		######### Average over copies #########
		#######################################

		if icopy != 50: 

			exec("h_average.Add(h_ZJets_GEcopy"+str(icopy)+","+str(averageWeight)+")")

	##################################
	######### Ratio subplots #########
	##################################

	# Fill empty ratio denominator histograms with the uncorrected MC

	h_ratioDen.Add(h_ZJets_GEcopy50)
	h_averageRatioDen.Add(h_ZJets_GEcopy50)

	##############################################
	######### Loop over each GE copy     #########
	######### Create histograms for each #########
	##############################################

	for icopy in loop:

		##############################
		######### Main plots #########
		##############################

		# Marker colors for copies and uncorrected MC

		if icopy%5 == 0: copyColor = 2 # Red
		elif icopy%5 == 1: copyColor = 3 # Blue
		elif icopy%5 == 2: copyColor = 4 # Green
		elif icopy%5 == 3: copyColor = 6 # Magenta
		elif icopy%5 == 4: copyColor = 7 # Cyan
		if icopy == 50: copyColor = 1 # Black (uncorrected MC)

		# [fill style, marker style, marker size, line width, marker/line/fill color]	

		copyStyle = [0,20,1,1,copyColor] #[no fill, filled circle, normal size, normal width, color will vary]

		# Create an empty numerator histogram for each GE copy
		# Add the GE copy histogram to the empty numerator histogram
		# Divide the numerator by the deniminator
		# Modify the histogram cosmetics with BeautifyRatio()

		sys.stdout.write("\x1b[1K\rCreating: h_ratioNum_GEcopy"+str(icopy))
		sys.stdout.flush()

		exec("h_ratioNum_GEcopy"+str(icopy)+" = CreateHisto(\"h_ratioNum_GEcopy"+str(icopy)+"\",\"ratioNum_GEcopy"+str(icopy)+"\",t_SingleMuData,recovariable,presentationbinning,\"0\",copyStyle,Label)")
		exec("h_ratioNum_GEcopy"+str(icopy)+".Sumw2()")
		exec("h_ratioNum_GEcopy"+str(icopy)+".Add(h_ZJets_GEcopy"+str(icopy)+")")
		exec("h_ratioNum_GEcopy"+str(icopy)+".Divide(h_ratioDen)") 

	sys.stdout.write("\x1b[1K\r")
	sys.stdout.flush()

	#############################################
	######### Ratio average over copies #########
	#############################################

	# Create an empty numerator histogram for average
	# Add the GE copy average histogram to the empty numerator histogram
	# Divide the numerator by the deniminator
	# Modify the histogram cosmetics with BeautifyRatio()

	h_averageRatioNum = CreateHisto("h_averageRatioNum","averageRatioNum",t_SingleMuData,recovariable,presentationbinning,"0",averageStyle,Label)
	h_averageRatioNum.Sumw2()
	h_averageRatioNum.Add(h_average)
	h_averageRatioNum.Divide(h_averageRatioDen)

	#############################################################################
	#																			#
	#						Create objects for each plot						#
	#																			#
	#############################################################################

	############################################################
	######### Initialize canvases, pads, legends, etc. #########
	######### Customize options for each               #########
	############################################################

	# c1 = GE copies
	# c2 = Average over GE copies

	c1 = TCanvas("c1","",800,800)
	c2 = TCanvas("c2","",800,800)

	# Create pads for main and ratio plots per canvas

	pad1_main 	= TPad( 'pad1_main', 'pad1_main', 0.0, 0.3, 1.0, 1.0 )
	pad1_ratio 	= TPad( 'pad1_ratio', 'pad1_ratio', 0.0, 0.0, 1.0, 0.3 )
	pad2_main 	= TPad( 'pad2_main', 'pad2_main', 0.0, 0.3, 1.0, 1.0 )
	pad2_ratio 	= TPad( 'pad2_ratio', 'pad2_ratio', 0.0, 0.0, 1.0, 0.3 )

	# Draw pads

	c1.cd()
	pad1_main.Draw()
	pad1_ratio.Draw()

	c2.cd()
	pad2_main.Draw()
	pad2_ratio.Draw()

	# Set pad upper and lower margins

	pad1_main.SetBottomMargin(0.0)		
	pad1_ratio.SetTopMargin(0.0)
	pad1_ratio.SetBottomMargin(0.43)
	pad2_main.SetBottomMargin(0.0)		
	pad2_ratio.SetTopMargin(0.0)
	pad2_ratio.SetBottomMargin(0.43)

	# Create each legend and customize options

	leg1 = TLegend(0.3,0.7,0.75,0.85,"","brNDC")
	leg2 = TLegend(0.3,0.7,0.75,0.85,"","brNDC")

	leg1.SetTextFont(42)
	leg1.SetFillColor(0)
	leg1.SetFillStyle(0)
	leg1.SetBorderSize(0)
	leg1.SetTextSize(.04)

	leg2.SetTextFont(42)
	leg2.SetFillColor(0)
	leg2.SetFillStyle(0)
	leg2.SetBorderSize(0)
	leg2.SetTextSize(.04)

	# For each legend, add an entry for the uncorrected distribution and either:
	# a representative entry for the copies, 
	# or the average over all the copies

	leg1.AddEntry(h_ZJets_GEcopy50,"uncorrected","lep")
	leg1.AddEntry(h_ZJets_GEcopy0,"copies: gauss(#kappa_{b}, #sigma), sign constraint","lep")

	leg2.AddEntry(h_ZJets_GEcopy50,"uncorrected","lep")
	leg2.AddEntry(h_average,"Average: gauss(#kappa_{b}, #sigma), sign constraint","lep")

	# Declare and customize the LaTeX objects that will be drawn to the pad, 
	# e.g., CMS logo, integrated luminosity, and collision energy

	# Drawn above main pad

	l1_header = TLatex()
	l1_header.SetTextAlign(12)
	l1_header.SetTextFont(42)
	l1_header.SetNDC()
	l1_header.SetTextSize(0.06)

	l2_header = TLatex()
	l2_header.SetTextAlign(12)
	l2_header.SetTextFont(42)
	l2_header.SetNDC()
	l2_header.SetTextSize(0.06)

	# Drawn inside main pad

	l1_logo = TLatex()
	l1_logo.SetTextAlign(12)
	l1_logo.SetTextFont(62)
	l1_logo.SetNDC()
	l1_logo.SetTextSize(0.08)

	l2_logo = TLatex()
	l2_logo.SetTextAlign(12)
	l2_logo.SetTextFont(62)
	l2_logo.SetNDC()
	l2_logo.SetTextSize(0.08)

	# Initialize lists for y-axis maxima

	maxList1 = []
	maxList2 = []

	# Get rid of stats box, pad title, etc.,

	gStyle.SetOptStat(0)

	#############################################################################
	#																			#
	#						Draw each plot and save as PDF						#
	#																			#
	#############################################################################

	##########################################
	######### Background copies plot #########
	##########################################

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

	for icopy in loop:
		if icopy == 0: exec("h_ZJets_GEcopy"+str(icopy)+".Draw(\"LEP\")")
		else: exec("h_ZJets_GEcopy"+str(icopy)+".Draw(\"LEPSAME\")")
		exec("BeautifyHisto(h_ZJets_GEcopy"+str(icopy)+",Label)")
		exec("maxList1.append(h_ZJets_GEcopy"+str(icopy)+".GetMaximum())")

	# Set the maximum on the y-axis shown in the plot 
	# as some multiple of the largest hist maximum

	h_ZJets_GEcopy0.SetMaximum(100*max(maxList1))
	
	# Draw legend and LaTeX strings

	leg1.Draw()
	l1_header.DrawLatex(0.12,0.94,"#it{Simulation}                            "+lumiInvfb+" fb^{-1} (13 TeV)")
	l1_logo.DrawLatex(0.15,0.84,"CMS")

	# Update the pad and redraw axis

	gPad.Update()
	gPad.RedrawAxis()

	#################################
	######### Ratio subplot #########
	#################################

	# Switch to secondary pad for ratio subplot
	# Add a grid to the pad

	pad1_ratio.cd()
	pad1_ratio.SetGrid()

	# Draw each copy histogram on secondary pad for ratio subplot
	# Modify cosmetics of each histogram with BeautifyRatio()

	for icopy in loop:

		# Marker colors for copies and uncorrected MC

		if icopy%5 == 0: copyColor = 2 # Red
		elif icopy%5 == 1: copyColor = 3 # Blue
		elif icopy%5 == 2: copyColor = 4 # Green
		elif icopy%5 == 3: copyColor = 6 # Magenta
		elif icopy%5 == 4: copyColor = 7 # Cyan
		if icopy == 50: copyColor = 1 # Black (uncorrected MC)

		# [fill style, marker style, marker size, line width, marker/line/fill color]	

		copyStyle = [0,20,1,1,copyColor] #[no fill, filled circle, normal size, normal width, color will vary]

		if icopy == 50: continue
		elif icopy == 0: exec("h_ratioNum_GEcopy"+str(icopy)+".Draw(\"LEP\")")
		elif icopy < 50: exec("h_ratioNum_GEcopy"+str(icopy)+".Draw(\"LEPSAME\")")
		exec("BeautifyRatio(h_ratioNum_GEcopy"+str(icopy)+",h_ratioDen,xlabel,copyStyle)")

	# Update the pad and redraw axis

	gPad.Update()

	#######################################################
	######### Background average over copies plot #########
	#######################################################

	c2.cd()

	#############################
	######### Main plot #########
	#############################

	# Switch to main pad, set to log scale

	pad2_main.cd()
	pad2_main.SetLogy()

	# Draw the average and uncorrected histograma on main pad

	h_average.Draw("LEP")
	h_ZJets_GEcopy50.Draw("LEPSAME")

	# Modify cosmetics of the histograms with BeautifyHisto()
	# Get the maxima of each histogram

	BeautifyHisto(h_average,Label)
	BeautifyHisto(h_ZJets_GEcopy50,Label)
	maxList2.extend([h_average.GetMaximum(),h_ZJets_GEcopy50.GetMaximum()])

	# Set the maximum on the y-axis shown in the plot 
	# as some multiple of the largest hist maximum

	h_average.SetMaximum(100*max(maxList2))
	
	# Draw legend and LaTeX strings

	leg2.Draw()
	l2_header.DrawLatex(0.12,0.94,"#it{Simulation}                            "+lumiInvfb+" fb^{-1} (13 TeV)")
	l2_logo.DrawLatex(0.15,0.84,"CMS")

	# Update the pad and redraw axis

	gPad.Update()
	gPad.RedrawAxis()

	#################################
	######### Ratio subplot #########
	#################################

	# Switch to secondary pad for ratio subplot
	# Add a grid to the pad

	pad2_ratio.cd()
	pad2_ratio.SetGrid()

	# Draw each copy histogram on secondary pad for ratio subplot
	# Modify cosmetics of each histogram with BeautifyRatio()

	h_averageRatioNum.Draw("LEP")
	BeautifyRatio(h_averageRatioNum,h_averageRatioDen,xlabel,averageStyle)

	# Update the pad and redraw axis

	gPad.Update()

	###########################################
	######### Save each plot as a PDF #########
	###########################################

	# Create subdirectories

	os.system("mkdir "+outdir+"/Background")
	os.system("mkdir "+outdir+"/Background/Copies")
	os.system("mkdir "+outdir+"/Background/Copies/"+selectionType)
	os.system("mkdir "+outdir+"/Background/Averages")
	os.system("mkdir "+outdir+"/Background/Averages/"+selectionType)

	# Save PDFs

	c1.Print(outdir+"/Background/Copies/"+selectionType+"/GEScaleSystStudyPlot_2016_Background_Copies_"+selectionType+"_"+recovariable+".pdf")
	c2.Print(outdir+"/Background/Averages/"+selectionType+"/GEScaleSystStudyPlot_2016_Background_Average_"+selectionType+"_"+recovariable+".pdf")
	print ""

def MakeSignalPlots(recovariable,xlabel,presentationbinning,selection,weight,bkgnormsf,outdir,mass):

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

		# Get selection type (final or pre), if final, get signal mass

	cutMass = ""
	if "LQToBMu_pair_uubj_BDT_discrim_M" in selection: 
		cutMass = selection.split("LQToBMu_pair_uubj_BDT_discrim_M")[-1].split(">")[0].strip()
		selectionType = "finalSel"+"_M"+cutMass
	else: selectionType = "preSel"

	print ""
	print "Creating plot: GEScaleSystStudyPlot_"+year+"_SignalM"+mass+"_Copies_"+selectionType+"_"+recovariable+".pdf"
	print "Creating plot: GEScaleSystStudyPlot_"+year+"_SignalM"+mass+"_Average_"+selectionType+"_"+recovariable+".pdf"
	print ""

	# Get the signal mass name

	signalName = "LQuujj"+mass

	# x-axis title and y-axis title

	Label=[xlabel,"Events / bin"]

	# Weight for calculating average over GE copies

	nCopies = len(loop)-1
	averageWeight = 1.0/float(nCopies)

	# Set style options for average and ratio histograms (den style is a placeholder--will be overridden by numerator style)
	# [fill style, marker style, marker size, line width, marker/line/fill color]

	averageStyle = [0,20,1,1,2] #[no fill, filled circle, normal size, normal width, red]
	ratioDenStyle = [0,20,1,1,1] #[no fill, filled circle, normal size, normal width, black]

	# Create empty histograms for denominators of each copy for ratio subplots (uncorrected MC)
	# Create empty histograms for average over GE copies
	# Create empty histograms for denominators of average ofer copies for ratio subplots (uncorrected MC)

	h_ratioDen = CreateHisto("h_ratioDen","ratioDen",t_SingleMuData,recovariable,presentationbinning,"0",ratioDenStyle,Label)
	h_average = CreateHisto("h_average","average",t_SingleMuData,recovariable,presentationbinning,"0",averageStyle,Label)
	h_averageRatioDen = CreateHisto("h_averageRatioDen","averageRatioDen",t_SingleMuData,recovariable,presentationbinning,"0",ratioDenStyle,Label)


	##############################################
	######### Loop over each GE copy     #########
	######### Create histograms for each #########
	##############################################

	for icopy in loop:

		##############################
		######### Main plots #########
		##############################

		# Marker colors for copies and uncorrected MC

		if icopy%5 == 0: copyColor = 2 # Red
		elif icopy%5 == 1: copyColor = 3 # Blue
		elif icopy%5 == 2: copyColor = 4 # Green
		elif icopy%5 == 3: copyColor = 6 # Magenta
		elif icopy%5 == 4: copyColor = 7 # Cyan
		if icopy == 50: copyColor = 1 # Black (uncorrected MC)

		# [fill style, marker style, marker size, line width, marker/line/fill color]	

		copyStyle = [0,20,1,1,copyColor] #[no fill, filled circle, normal size, normal width, color will vary]

		# Create hist for the signal sample corresponding to the mass variable
		# Creates an empty TH1D and projects recovariable from tree with selection and weights onto TH1D (defined in CreateHisto)

		# Get the name of the signal tree to project and name the histogram

		name = "signal_GEcopy" + str(icopy)
		tname = "t_" + signalName + "_GEcopy" + str(icopy)
		hname = "h_" + name

		sys.stdout.write("\x1b[1K\rCreating: "+hname)
		sys.stdout.flush()

		exec(hname+" = CreateHisto(\"" + hname + "\",\"" + name + "\"," + tname + ",recovariable,presentationbinning,selection + \"*\" + weight,copyStyle,Label)")

		#######################################
		######### Average over copies #########
		#######################################

		if icopy != 50:

			exec("h_average.Add("+hname+","+str(averageWeight)+")")

	##################################
	######### Ratio subplots #########
	##################################

	# Fill empty ratio denominator histograms with the uncorrected MC

	h_ratioDen.Add(h_signal_GEcopy50)
	h_averageRatioDen.Add(h_signal_GEcopy50)

	##############################################
	######### Loop over each GE copy     #########
	######### Create histograms for each #########
	##############################################

	for icopy in loop:

		################################
		######### Ratio copies #########
		################################

		# Marker colors for copies and uncorrected MC

		if icopy%5 == 0: copyColor = 2 # Red
		elif icopy%5 == 1: copyColor = 3 # Blue
		elif icopy%5 == 2: copyColor = 4 # Green
		elif icopy%5 == 3: copyColor = 6 # Magenta
		elif icopy%5 == 4: copyColor = 7 # Cyan
		if icopy == 50: copyColor = 1 # Black (uncorrected MC)

		# [fill style, marker style, marker size, line width, marker/line/fill color]	

		copyStyle = [0,20,1,1,copyColor] #[no fill, filled circle, normal size, normal width, color will vary]

		# Create an empty numerator histogram for each GE copy
		# Add the GE copy histogram to the empty numerator histogram
		# Divide the numerator by the deniminator

		sys.stdout.write("\x1b[1K\rCreating: h_ratioNum_GEcopy"+str(icopy))
		sys.stdout.flush()

		exec("h_ratioNum_GEcopy"+str(icopy)+" = CreateHisto(\"h_ratioNum_GEcopy"+str(icopy)+"\",\"ratioNum_GEcopy"+str(icopy)+"\",t_SingleMuData,recovariable,	presentationbinning,\"0\",copyStyle,Label)")
		exec("h_ratioNum_GEcopy"+str(icopy)+".Sumw2()")
		exec("h_ratioNum_GEcopy"+str(icopy)+".Add(h_signal_GEcopy"+str(icopy)+")")
		exec("h_ratioNum_GEcopy"+str(icopy)+".Divide(h_ratioDen)") 

	sys.stdout.write("\x1b[1K\r")
	sys.stdout.flush()

	#############################################
	######### Ratio average over copies #########
	#############################################

	# Create an empty numerator histogram for average
	# Add the average histogram to the empty numerator histogram
	# Divide the numerator by the deniminator

	h_averageRatioNum = CreateHisto("h_averageRatioNum","averageRatioNum",t_SingleMuData,recovariable,presentationbinning,"0",averageStyle,Label)
	h_averageRatioNum.Sumw2()
	h_averageRatioNum.Add(h_average)
	h_averageRatioNum.Divide(h_averageRatioDen)

	#############################################################################
	#																			#
	#						Create objects for each plot						#
	#																			#
	#############################################################################

	############################################################
	######### Initialize canvases, pads, legends, etc. #########
	######### Customize options for each               #########
	############################################################

	# c1 = GE copies
	# c2 = Average over GE copies

	c1 = TCanvas("c1","",800,800)
	c2 = TCanvas("c2","",800,800)

	# Create pads for main and ratio plots per canvas

	pad1_main 	= TPad( 'pad1_main', 'pad1_main', 0.0, 0.3, 1.0, 1.0 )
	pad1_ratio 	= TPad( 'pad1_ratio', 'pad1_ratio', 0.0, 0.0, 1.0, 0.3 )
	pad2_main 	= TPad( 'pad2_main', 'pad2_main', 0.0, 0.3, 1.0, 1.0 )
	pad2_ratio 	= TPad( 'pad2_ratio', 'pad2_ratio', 0.0, 0.0, 1.0, 0.3 )

	# Draw pads

	c1.cd()
	pad1_main.Draw()
	pad1_ratio.Draw()

	c2.cd()
	pad2_main.Draw()
	pad2_ratio.Draw()

	# Set pad upper and lower margins

	pad1_main.SetBottomMargin(0.0)		
	pad1_ratio.SetTopMargin(0.0)
	pad1_ratio.SetBottomMargin(0.43)
	pad2_main.SetBottomMargin(0.0)		
	pad2_ratio.SetTopMargin(0.0)
	pad2_ratio.SetBottomMargin(0.43)

	# Create each legend and customize options

	leg1 = TLegend(0.3,0.7,0.75,0.85,"","brNDC")
	leg2 = TLegend(0.3,0.7,0.75,0.85,"","brNDC")

	leg1.SetTextFont(42)
	leg1.SetFillColor(0)
	leg1.SetFillStyle(0)
	leg1.SetBorderSize(0)
	leg1.SetTextSize(.04)

	leg2.SetTextFont(42)
	leg2.SetFillColor(0)
	leg2.SetFillStyle(0)
	leg2.SetBorderSize(0)
	leg2.SetTextSize(.04)

	# For each legend, add an entry for the uncorrected distribution and either:
	# a representative entry for the copies, 
	# or the average over all the copies

	leg1.AddEntry(h_signal_GEcopy50,"uncorrected","lep")
	leg1.AddEntry(h_signal_GEcopy0,"copies: gauss(#kappa_{b}, #sigma), sign constraint","lep")

	leg2.AddEntry(h_signal_GEcopy50,"uncorrected","lep")
	leg2.AddEntry(h_average,"Average: gauss(#kappa_{b}, #sigma), sign constraint","lep")

	# Declare and customize the LaTeX objects that will be drawn to the pad, 
	# e.g., CMS logo, integrated luminosity, and collision energy

	# Drawn above main pad

	l1_header = TLatex()
	l1_header.SetTextAlign(12)
	l1_header.SetTextFont(42)
	l1_header.SetNDC()
	l1_header.SetTextSize(0.06)

	l2_header = TLatex()
	l2_header.SetTextAlign(12)
	l2_header.SetTextFont(42)
	l2_header.SetNDC()
	l2_header.SetTextSize(0.06)

	# Drawn inside main pad

	l1_logo = TLatex()
	l1_logo.SetTextAlign(12)
	l1_logo.SetTextFont(62)
	l1_logo.SetNDC()
	l1_logo.SetTextSize(0.08)

	l2_logo = TLatex()
	l2_logo.SetTextAlign(12)
	l2_logo.SetTextFont(62)
	l2_logo.SetNDC()
	l2_logo.SetTextSize(0.08)

	# Initialize lists for y-axis maxima

	maxList1 = []
	maxList2 = []

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

	for icopy in loop:
		if icopy == 0: exec("h_signal_GEcopy"+str(icopy)+".Draw(\"LEP\")")
		else: exec("h_signal_GEcopy"+str(icopy)+".Draw(\"LEPSAME\")")
		exec("BeautifyHisto(h_signal_GEcopy"+str(icopy)+",Label)")
		exec("maxList1.append(h_signal_GEcopy"+str(icopy)+".GetMaximum())")

	# Set the maximum on the y-axis shown in the plot 
	# as some multiple of the largest hist maximum

	h_signal_GEcopy0.SetMaximum(100*max(maxList1))
	
	# Draw legend and LaTeX strings

	leg1.Draw()
	l1_header.DrawLatex(0.12,0.94,"#it{Simulation}                            "+lumiInvfb+" fb^{-1} (13 TeV)")
	l1_logo.DrawLatex(0.15,0.84,"CMS")

	# Update the pad and redraw axis

	gPad.Update()
	gPad.RedrawAxis()

	#################################
	######### Ratio subplot #########
	#################################

	# Switch to secondary pad for ratio subplot
	# Add a grid to the pad

	pad1_ratio.cd()
	pad1_ratio.SetGrid()

	# Draw each copy histogram on secondary pad for ratio subplot
	# Modify cosmetics of each histogram with BeautifyRatio()

	for icopy in loop:

		# Marker colors for copies and uncorrected MC

		if icopy%5 == 0: copyColor = 2 # Red
		elif icopy%5 == 1: copyColor = 3 # Blue
		elif icopy%5 == 2: copyColor = 4 # Green
		elif icopy%5 == 3: copyColor = 6 # Magenta
		elif icopy%5 == 4: copyColor = 7 # Cyan
		if icopy == 50: copyColor = 1 # Black (uncorrected MC)

		# [fill style, marker style, marker size, line width, marker/line/fill color]	

		copyStyle = [0,20,1,1,copyColor] #[no fill, filled circle, normal size, normal width, color will vary]

		if icopy == 50: continue
		elif icopy == 0: exec("h_ratioNum_GEcopy"+str(icopy)+".Draw(\"LEP\")")
		elif icopy < 50: exec("h_ratioNum_GEcopy"+str(icopy)+".Draw(\"LEPSAME\")")
		exec("BeautifyRatio(h_ratioNum_GEcopy"+str(icopy)+",h_ratioDen,xlabel,copyStyle)")

	# Update the pad and redraw axis

	gPad.Update()

	###############################################
	######### Average over GE copies plot #########
	###############################################

	c2.cd()

	#############################
	######### Main plot #########
	#############################

	# Switch to main pad, set to log scale

	pad2_main.cd()
	pad2_main.SetLogy()

	# Draw the average and uncorrected histograma on main pad

	h_average.Draw("LEP")
	h_signal_GEcopy50.Draw("LEPSAME")

	# Modify cosmetics of the histograms with BeautifyHisto()
	# Get the maxima of each histogram

	BeautifyHisto(h_average,Label)
	BeautifyHisto(h_signal_GEcopy50,Label)
	maxList2.extend([h_average.GetMaximum(),h_signal_GEcopy50.GetMaximum()])

	# Set the maximum on the y-axis shown in the plot 
	# as some multiple of the largest hist maximum

	h_average.SetMaximum(100*max(maxList2))
	
	# Draw legend and LaTeX strings

	leg2.Draw()
	l2_header.DrawLatex(0.12,0.94,"#it{Simulation}                            "+lumiInvfb+" fb^{-1} (13 TeV)")
	l2_logo.DrawLatex(0.15,0.84,"CMS")

	# Update the pad and redraw axis

	gPad.Update()
	gPad.RedrawAxis()

	#################################
	######### Ratio subplot #########
	#################################

	# Switch to secondary pad for ratio subplot
	# Add a grid to the pad

	pad2_ratio.cd()
	pad2_ratio.SetGrid()

	# Draw each copy histogram on secondary pad for ratio subplot
	# Modify cosmetics of each histogram with BeautifyRatio()


	h_averageRatioNum.Draw("LEP")
	BeautifyRatio(h_averageRatioNum,h_averageRatioDen,xlabel,averageStyle)

	# Update the pad and redraw axis

	gPad.Update()

	###########################################
	######### Save each plot as a PDF #########
	###########################################

	# Create subdirectories

	os.system("mkdir "+outdir+"/SignalM"+mass)
	os.system("mkdir "+outdir+"/SignalM"+mass+"/Copies")
	os.system("mkdir "+outdir+"/SignalM"+mass+"/Copies/"+selectionType)
	os.system("mkdir "+outdir+"/SignalM"+mass+"/Averages")
	os.system("mkdir "+outdir+"/SignalM"+mass+"/Averages/"+selectionType)

	# Save PDFs

	c1.Print(outdir+"/SignalM"+mass+"/Copies/"+selectionType+"/GEScaleSystStudyPlot_"+year+"_SignalM"+mass+"_Copies_"+selectionType+"_"+recovariable+".pdf")
	c2.Print(outdir+"/SignalM"+mass+"/Averages/"+selectionType+"/GEScaleSystStudyPlot_"+year+"_SignalM"+mass+"_Average_"+selectionType+"_"+recovariable+".pdf")
	print ""

def MakeSFJSON(json_name):
	print 'Opening file ',json_name
	with open(json_name,'w') as outfile:
		emptyDict = {}
		'Writing empty dictionary to ',json_name
		json.dump(emptyDict, outfile, indent=4)

	for icopy in loop:
		print 'Getting background scale factors for GE copy ',str(icopy),':'

		print 'Reading file ',json_name
		with open(json_name,'r') as infile:
			'Loading json from ',json_name
			SFs = json.load(infile)

		[[R_z,R_z_err],[R_tt,R_tt_err]] =  GetMuMuScaleFactors( eventWeights+'*'+preselection, '(M_uu>80)*(M_uu<100)', '(M_uu>100)*(M_uu<250)',0,icopy) 
		SFs[str(icopy)] = {
			'R_z':R_z,
			'R_z_err':R_z_err,
			'R_tt':R_tt,
			'R_tt_err':R_tt_err
		}
		print 'Opening file ',json_name
		with open(json_name,'w') as outfile:
			print 'Writing SFs to file ',json_name
			print ''
			json.dump(SFs, outfile, indent=4)


def ReformatResultsToJSON():
	print 'Reformating results...'
	for lqmass in lqMasses:
		print 'Mass: ',lqmass,' GeV'
		mass_dir = str(lqmass)
		dataJSON = {
			"Cut":"",
			"Integral":{
				"Nominal":{
					"Signal":0,
					"Background":0
				},
				"Average":{
					"Signal":0,
					"Background":0
				},
				"Difference":{
					"Signal":0,
					"Background":0
				}
			},
			"Systematic":{
				"Signal":0,
				"Background":0
			}
		}
		with open(mass_dir+'/SystematicResults.txt','r') as infile:
			for line in infile.readlines():
				key = line.split(':')[0].strip()
				value = line.split(':')[1].strip()
				if 'Final selection cut' in key:
					dataJSON["Cut"] = value
				elif 'signal' in key:
					if 'nominal' in key:
						dataJSON["Integral"]["Nominal"]["Signal"] = float(value)
					elif 'average' in key:
						dataJSON["Integral"]["Average"]["Signal"] = float(value)
					elif 'Difference' in key:
						dataJSON["Integral"]["Difference"]["Signal"] = float(value)
					elif 'Systematic' in key:
						dataJSON["Systematic"]["Signal"] = float(value)
				elif 'background' in key:
					if 'nominal' in key:
						dataJSON["Integral"]["Nominal"]["Background"] = float(value)
					elif 'average' in key:
						dataJSON["Integral"]["Average"]["Background"] = float(value)
					elif 'Difference' in key:
						dataJSON["Integral"]["Difference"]["Background"] = float(value)
					elif 'Systematic' in key:
						dataJSON["Systematic"]["Background"] = float(value)

		with open(mass_dir+'/SystematicResults.json','w') as outJSON:
			json.dump(dataJSON, outJSON, indent=4)

		os.system('mv '+mass_dir+'/SystematicResults.txt '+mass_dir+'/data/SystematicResults.txt')
		os.system('mv '+mass_dir+'/SystematicResults.json '+mass_dir+'/data/SystematicResults.json')



def CombineJSONs():
	print 'Combining results...'
	allMasses = {}
	for lqmass in lqMasses:
		print 'Mass: ',lqmass,' GeV'
		mass_dir = str(lqmass)
		with open(mass_dir+'/data/SystematicResults.json','r') as inJSON:
			jsonForMass = json.load(inJSON)
		allMasses[str(lqmass)] = jsonForMass
	
	with open('AllSystematics.json','w') as outJSON:
		json.dump(allMasses, outJSON, indent=4)
		


OpenTrees = False
DoValidationPlots = False
CompileResults = False

if OpenTrees:
	for icopy in loop:
		for ftype in fileTypes:
			name = ftype + "_GEcopy" + str(icopy)

			# Open all ROOT files for GE copy "copy"
			# Tree names look like, e.g., f_ZJets_GEcopy0
			f = "f_" + name
			print 'Opening ', directories[str(icopy)] + '/' + ftype + '.root', ' as ', f
			exec(f + " = TFile.Open(\"" + directories[str(icopy)] + "/" + ftype + ".root\",\"READ\")")

			# Get PhysicalVariables tree from each file of GE copy "copy"
			# Tree names look like, e.g., t_ZJets_GEcopy0
			t = "t_" + name
			exec(t + " = " + f + ".Get(\"PhysicalVariables\")")

	# Data just used as empty histograms
	f_SingleMuData = TFile.Open("/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2016/gmadigan/NTupleAnalyzer_nanoAOD_Full2016updatedMER_SysBDT_stockNano_2021_11_03_08_40_52/SummaryFiles/SingleMuData.root","READ")
	t_SingleMuData = f_SingleMuData.Get("PhysicalVariables")

if DoValidationPlots:

	# Define Binning
	bdtbinning = [40,-1,1]
	ptbinning = [53,75,105]
	ptbinning2 = [53,75,105]
	metbinning2 = [0,5]
	stbinning = [200,225]
	bosonbinning = [50,60,70,80,90,100,110,120]
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

	bdtbinningFS = [100,0.9,1]

	# Output directories
	plot_dir = 'StudyPlots_'+year
	os.system('mkdir '+plot_dir)

	# Hardcoded 2016 Z+Jets and tt-bar background normalization scale factors (for all distributions)
	BkgNormSF = {
	    "R_tt_err": 0.013859999999999604, 
	    "R_z": 1.015770098706867, 
	    "R_tt": 0.9538052042826998, 
	    "R_z_err": 0.016999999999999477
	}

	# Selection = preselection

	# Variable = pT

	# Samples = background

	#MakeBackgroundPlots("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection,eventWeights,BkgNormSF,plot_dir)
	#MakeBackgroundPlots("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning,preselection,eventWeights,BkgNormSF,plot_dir)

	#for mass in lqMasses:
	#
	#	# Samples = signals
	#
	#	MakeSignalPlots("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection,eventWeights,BkgNormSF,plot_dir,mass)
	#	MakeSignalPlots("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning,preselection,eventWeights,BkgNormSF,plot_dir,mass)
	#
	#
	# Variable = BDT scores
	#
	#for mass in lqMasses:
	#	
	#	mass_str = "LQToBMu_pair_uubj_BDT_discrim_M"+mass
	#	title_str = "BDT score (M_{LQ} = "+mass+" GeV)"
	#
	#	# Samples = background
	#
	#	MakeBackgroundPlots(mass_str,title_str,bdtbinning,preselection,eventWeights,BkgNormSF,plot_dir)
	#
	#	# Samples = signals
	#
	#	MakeSignalPlots(mass_str,title_str,bdtbinning,preselection,eventWeights,BkgNormSF,plot_dir,mass)

	
	# Selection = final selection

	for mass in lqMasses:

		# Variable = pT
	
		# Samples = background
	
		MakeBackgroundPlots("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection+"*"+finalSelCut[mass],eventWeights,BkgNormSF,plot_dir)
		MakeBackgroundPlots("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning,preselection+"*"+finalSelCut[mass],eventWeights,BkgNormSF,plot_dir)
	
		# Samples = signals
	
		MakeSignalPlots("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection+"*"+finalSelCut[mass],eventWeights,BkgNormSF,plot_dir,mass)
		MakeSignalPlots("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning,preselection+"*"+finalSelCut[mass],eventWeights,BkgNormSF,plot_dir,mass)
	
	
		# Variable = BDT scores
		
		mass_str = "LQToBMu_pair_uubj_BDT_discrim_M"+mass
		title_str = "BDT score (M_{LQ} = "+mass+" GeV)"
	
		# Samples = background
	
		MakeBackgroundPlots(mass_str,title_str,bdtbinningFS,preselection+"*"+finalSelCut[mass],eventWeights,BkgNormSF,plot_dir)
	
		# Samples = signals
	
		MakeSignalPlots(mass_str,title_str,bdtbinningFS,preselection+"*"+finalSelCut[mass],eventWeights,BkgNormSF,plot_dir,mass)


if CompileResults:
	ReformatResultsToJSON()
	CombineJSONs()
