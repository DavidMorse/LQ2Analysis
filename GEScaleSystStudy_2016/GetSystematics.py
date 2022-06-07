import os, math, sys, random
import subprocess
import json
import numpy as np
from array import array
from ROOT import *

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

######################################
###  Background normalization SFs  ###
######################################

bkgSFs = {
		"R_tt_err": 0.013859999999999604, 
		"R_z": 1.015770098706867, 
		"R_tt": 0.9538052042826998, 
		"R_z_err": 0.016999999999999477
	} 

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
bkgTypes = [    "ZJets",
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

if False:
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

def QuickIntegral(tree,selection,scalefac):

	# print selection+'*'+str(scalefac)
	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection+'*'+str(scalefac))
	I = h.GetBinContent(1)
	E = h.GetBinError(1)
	return [I,E]

def GetGEScaleSysPresel(selection,weight,bkgnormsf,json_name):

	if json_name is '':
		print 'Using selection:'
		print selection + '*' + weight
		print ''
		print 'Doing QuickIntegrals...'
		data = {}
		for icopy in loop:
			R_z = bkgnormsf['R_z']
			R_tt = bkgnormsf['R_tt']
			data[str(icopy)] = {}
			for sample in fileTypes:
				print 'Getting Integral for GE copy ',str(icopy),' of ',sample,'...\n'
				if 'ZJets' in sample:exec("data['"+str(icopy)+"']['"+sample+"'] = QuickIntegral(t_"+sample+"_GEcopy"+str(icopy)+", selection + '*' + weight, "+str(R_z)+")")
				elif 'TTBar' in sample:exec("data['"+str(icopy)+"']['"+sample+"'] = QuickIntegral(t_"+sample+"_GEcopy"+str(icopy)+", selection + '*' + weight, "+str(R_tt)+")")
				else: exec("data['"+str(icopy)+"']['"+sample+"'] = QuickIntegral(t_"+sample+"_GEcopy"+str(icopy)+", selection + '*' + weight, 1.0)")
				print '[Integral, Error] = ',data[str(icopy)][sample],'\n'

		json_name = 'EventCountsPresel.json'

		print 'Saving integrals to json file: ',json_name,'\n'

		with open(json_name, 'w') as outfile:
			json.dump(data, outfile, indent=4)

	print 'Reading json file: ',json_name,'\n'

	with open(json_name, 'r') as infile:
		json_data =	json.load(infile)
		
	print 'Doing calculations...\n'

	outSysPresel = {}

	# background

	for bkg in bkgTypes:
		outSysPresel[bkg] = {}

		bkgNom = 0.0
		bkgGEcopyMean = 0.0

		totBkgNom = 0.0
		totBkgGEcopyMean = 0.0
		totBkgDiff = 0.0
		totBkgSys = 0.0

		Ncopies = 0

		for icopy in loop:
			if icopy is 50:
				bkgNom += json_data[str(icopy)][bkg][0]
			else:
				Ncopies += 1
				bkgGEcopyMean += json_data[str(icopy)][bkg][0]
	
		bkgGEcopyMean *= 0.02
		bkgDiff = bkgNom-bkgGEcopyMean
		bkgSys = 100.0*abs(bkgDiff)/bkgNom

		outSysPresel[bkg] = {"nominal events": bkgNom, "mean events": bkgGEcopyMean, "difference": bkgDiff, "systematic": bkgSys}
		
		totBkgNom += bkgNom
		totBkgGEcopyMean += bkgGEcopyMean
		totBkgDiff += bkgDiff

	totBkgSys = 100.0*abs(totBkgDiff)/totBkgNom
	outSysPresel["Background"] = {"nominal events": totBkgNom, "mean events": totBkgGEcopyMean, "difference": totBkgDiff, "systematic": totBkgSys}

	# signals

	for sig in sigTypes:
		outSysPresel[sig] = {}

		sigNom = 0.0
		sigGEcopyMean = 0.0

		Ncopies = 0

		for icopy in loop:
			if icopy is 50:
				sigNom += json_data[str(icopy)][sig][0]
			else:
				Ncopies += 1
				sigGEcopyMean += json_data[str(icopy)][sig][0]

		sigGEcopyMean *= 0.02
		sigDiff = abs(sigNom-sigGEcopyMean)
		sigSys = 100.0*sigDiff/sigNom

		outSysPresel[sig] = {"nominal events": sigNom, "mean events": sigGEcopyMean, "difference": sigDiff, "systematic": sigSys}

	results_name = 'GEScaleSysPresel.json'

	with open(results_name,'w') as outjson:
		json.dump(outSysPresel,outjson,indent=4)

GetGEScaleSysPresel(preselection,eventWeights,bkgSFs,"EventCountsPresel.json")