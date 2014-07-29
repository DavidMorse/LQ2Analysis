import os, sys, math, random
from glob import glob

##########################################################################
########    GLOBAL VARIABLES NEEDED FOR PLOTS AND ANALYSIS        ########
##########################################################################

# Directory where root files are kept and the tree you want to get root files from
QCDDirectory = 'NTupleAnalyzer_FullJuly24QCDNonIsoQuickTest_2014_07_25_15_39_48/SummaryFiles'
EMuDirectory = 'NTupleAnalyzer_FullJuly24EMuSwitch_2014_07_25_03_54_54/SummaryFiles'
NormalDirectory='NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles'

# The name of the main ttree (ntuple structure)
TreeName = "PhysicalVariables"

# Integrated luminosity for nuormalization
lumi = 19600.0

# Single-mu trigger efficiencies as a functino of muon Eta. 
# This is for the case of one muon
singlemuHLT =  '*( 0.93*(abs(Eta_muon1)<=0.9) + 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) + 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) )'
# This if for the case of two muons (i.e. the above factors, but for the case where the events has two muosn)
doublemuHLT =  '*(1.0-(( 1.0 - 0.93*(abs(Eta_muon1)<=0.9) - 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) - 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) )'
doublemuHLT += '*( 1.0 - 0.93*(abs(Eta_muon2)<=0.9) - 0.83*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2) - 0.80*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1) )))'
# This is for the case of the E-mu sample, where one "muon" is replaced by an exlectron. In that case, we check
# which muon is a real muon (IsMuon_muon1) and apply the trigger efficiency based on the muon
singlemuHLTEMU = '*((IsMuon_muon1*( 0.93*(abs(Eta_muon1)<=0.9) + 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) + 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) ))'
singlemuHLTEMU += '+(IsMuon_muon2*( 0.93*(abs(Eta_muon2)<=0.9) + 0.83*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2) + 0.80*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1) )))'

# This is the rescaling of the EMu data for the ttbar estimate (2 - Eff_trigger)
dataHLTEMUADJ = '*(2.0 - 1.0'+singlemuHLTEMU+')'

# Weights for different MC eselections, including integrated luminosity, event weight, and trigger weight
NormalWeightMuMu = str(lumi)+'*weight_central'+doublemuHLT
NormalWeightMuNu = str(lumi)+'*weight_central'+singlemuHLT
NormalWeightEMu = str(lumi)+'*weight_central'+singlemuHLTEMU
NormalWeightEMuNoHLT = str(lumi)+'*weight_central'

# This is the real data trigger condition
dataHLT = '*(pass_HLTMu40_eta2p1)'

# This is the set of event filters used
passfilter =  '*(passDataCert*passPrimaryVertex)'
passfilter += '*(passBeamScraping*passPhysDeclared*passBeamHalo*passHBHENoiseFilter*passTrackingFailure)'
passfilter += '*(passEcalDeadCellBE*passEcalDeadCellTP*passBadEESuperCrystal*passHcalLaserEvent*passBPTX0)'

# This defines the preselections for the mu-mu, mu-nu, and e-mu samples
preselectionmumu = '((Pt_muon1>45)*(Pt_muon2>45)*(Pt_jet1>125)*(Pt_jet2>45)*(St_uujj>300)*(M_uu>50))*(DR_muon1muon2>0.3)'
preselectionmunu = '((Pt_muon1>45)*(Pt_muon2<45.0)*(Pt_miss>55)*(Pt_jet1>125)*(Pt_jet2>45)*(Pt_ele1<45.0)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5)*(MT_uv>50.0))'
preselectionemu  = '((Pt_muon1>45)*(Pt_muon2>45)*(Pt_jet1>125)*(Pt_jet2>45)*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3))'

# Add the filters to the preselections
preselectionemu += passfilter
preselectionmumu+=passfilter
preselectionmunu+=passfilter


##########################################################################
########    HARD CODED RESULTS USED IN ANALYSIS                   ########
##########################################################################

# These are hard-coded results for the more grueling studies we don't want to repeat every time. 

# First is the ttbar data-driven e-mu scale factor.
emu_id_eff = 0.5716
emu_id_eff_err = 0.00606


# Next are the PDF uncertainties. 
pdf_MASS   =[ 300 , 350 , 400 , 450 , 500 , 550 , 600 , 650 , 700 , 750 , 800 , 850 , 900 , 950 , 1000 , 1050 , 1100 , 1150 , 1200 ]               
# pdf_uujj_TTBar =[ 3.92 , 4.42 , 4.96 , 5.14 , 5.48 , 5.43 , 5.18 , 5.26 , 5.15 , 5.89 , 4.57 , 6.08 , 10.13 , 16.58 , 16.58 , 16.58 , 16.58 , 16.58 , 16.58]
# pdf_uujj_ZJets =[  0.33 , 0.65 , 0.94 , 1.31 , 1.59 , 2.23 , 3.04 , 2.34 , 2.38 , 2.58 , 2.58 , 2.58 , 2.97 , 2.97 , 4.45 , 4.45 , 4.45 , 4.45 , 4.45]
# pdf_uujj_WJets =[  3.86 , 3.67 , 6.01 , 6.01 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94 , 10.94]
# pdf_uujj_sTop =[  7.44 , 8.97 , 11.78 , 13.98 , 18.23 , 20.37 , 20.37 , 20.37 , 20.37 , 20.37 , 21.2 , 21.2 , 47.28 , 47.28 , 47.28 , 47.28 , 47.28 , 47.28 , 47.28]
# pdf_uujj_VV =[  2.9 , 3.2 , 3.43 , 3.88 , 4.27 , 4.27 , 4.34 , 4.34 , 4.86 , 12.8 , 24.32 , 30.4 , 30.4 , 30.4 , 30.4 , 30.4 , 30.4 , 30.4 , 30.4]
# pdf_uujj_Signal = [2.0 for x in pdf_MASS]               

       
# pdf_uvjj_TTBar =[  0.65 , 0.94 , 1.75 , 2.44 , 2.52 , 3.28 , 4.14 , 4.99 , 5.81 , 4.48 , 3.58 , 4.28 , 5.15 , 4.56 , 7.93 , 7.93 , 7.93 , 7.93 , 7.93]
# pdf_uvjj_ZJets =[  0.44 , 0.56 , 0.59 , 0.7 , 0.63 , 0.9 , 1.33 , 1.91 , 2.51 , 3.85 , 3.85 , 3.74 , 8.11 , 8.11 , 8.11 , 8.11 , 8.11 , 8.11 , 8.11]
# pdf_uvjj_WJets =[  1.17 , 1.36 , 1.85 , 2.72 , 3.02 , 4.41 , 7.16 , 10.54 , 15.21 , 19.12 , 16.87 , 40.14 , 40.14 , 40.14 , 40.14 , 40.14 , 40.14 , 40.14 , 40.14]
# pdf_uvjj_sTop =[  9.56 , 12.25 , 8.74 , 9.07 , 9.6 , 11.44 , 8.52 , 12.8 , 12.8 , 12.8 , 12.8 , 12.8 , 12.8 , 12.8 , 12.8 , 12.8 , 12.8 , 12.8 , 12.8]
# pdf_uvjj_VV =[  2.09 , 2 , 2.12 , 2.13 , 2.26 , 2.8 , 2.4 , 2.27 , 2.34 , 2.7 , 3.42 , 3.2 , 4.19 , 4.19 , 4.19 , 4.19 , 4.19 , 4.19 , 4.19]
# pdf_uvjj_Signal = [2.0 for x in pdf_MASS]               


# pdf_uujj_ZJets = [0.241,0.451,0.666,0.936,1.178,1.775,2.52,2.52,2.52,2.52,2.52,2.52,2.52,2.52,3.64,3.64,3.64,3.64,3.64]
# pdf_uujj_TTBar = [3.73,4.249,4.838,5.054,5.492,5.492,5.492,5.492,5.492,5.492,5.492,6.373,11.177,18.24,18.24,18.24,18.24,18.24,18.24]
# pdf_uujj_WJets = [1.984,2.275,3.811,3.811,6.956,6.956,6.956,6.956,6.956,6.956,6.956,6.956,6.956,6.956,6.956,6.956,6.956,6.956,6.956]
# pdf_uujj_VV = [2.288,2.657,2.899,3.243,3.554,3.606,3.606,4.888,6.976,13.459,17.724,20.767,20.767,20.767,20.767,20.767,20.767,20.767,20.767]
# pdf_uujj_sTop = [7.94,9.713,13.337,15.854,20.022,27.444,27.444,27.444,27.444,33.063,45.625,45.625,100.0,100.0,100.0,100.0,100.0,100.0,100.0]
# pdf_uujj_Signal = [0.025,0.041,0.061,0.094,0.116,0.172,0.216,0.226,0.235,0.259,0.291,0.298,0.337,0.389,0.447,0.447,0.447,0.447,0.447]
# pdf_uujj_Signal = [2.0 for x in pdf_MASS]               

# pdf_uvjj_ZJets = [1.363,1.363,1.363,1.544,1.544,1.598,2.375,2.375,2.678,3.443,3.443,3.604,4.443,5.091,5.091,5.091,5.091,5.091,5.091]
# pdf_uvjj_TTBar = [0.91,1.622,2.254,2.953,3.113,4.102,5.037,5.816,6.131,6.131,6.131,6.131,6.131,6.131,10.147,10.147,10.147,10.147,10.147]
# pdf_uvjj_WJets = [0.843,1.089,1.614,2.326,2.7,3.754,7.133,9.918,14.182,18.07,18.07,69.647,69.647,69.647,69.647,69.647,69.647,69.647,69.647]
# pdf_uvjj_VV = [2.191,2.191,2.191,2.236,2.397,3.011,3.011,3.011,3.011,3.011,3.313,3.909,4.674,4.873,4.873,4.873,4.873,4.873,4.873]
# pdf_uvjj_sTop = [5.599,7.664,8.186,9.168,10.064,12.788,15.976,15.976,15.976,15.976,15.976,15.976,15.976,15.976,15.976,15.976,15.976,15.976,15.976]
# pdf_uvjj_Signal = [0.13,0.141,0.461,0.461,0.461,0.496,0.523,0.603,0.637,0.74,0.865,0.901,0.967,1.006,1.136,1.136,1.136,1.136,1.136]
# pdf_uvjj_Signal = [2.0 for x in pdf_MASS]               



# pdf_uujj_Signal = [0.1,0.17,0.18,0.21,0.26,0.26,0.26,0.27,0.29,0.31,0.35,0.36,0.46,0.65,1.06,1.06,1.06,1.06,1.06]
# pdf_uvjj_Signal = [0.35,0.53,0.83,0.83,0.83,0.83,0.83,0.83,0.83,0.84,1.2,1.2,1.62,1.62,2.22,2.35,2.35,2.35,2.35]
# pdf_uujj_Signal = [2.0 for x in pdf_MASS]               
# pdf_uvjj_Signal = [3.0 for x in pdf_MASS]               

# pdf_uujj_TTBar = [4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11,4.11]
# pdf_uujj_WJets = [3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58]
# pdf_uujj_VV = [3.15,3.33,3.63,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15]
# pdf_uujj_ZJets = [0.58,1.35,1.93,2.8,4.07,5.96,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62]
# pdf_uujj_sTop = [8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43]

# pdf_uvjj_TTBar = [2.15,3.48,5.15,6.33,7.33,9.97,14.52,14.52,14.52,14.52,14.52,14.52,14.52,14.52,14.52,14.52,14.52,14.52,14.52]
# pdf_uvjj_WJets = [1.06,1.46,2.3,3.67,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72]
# pdf_uvjj_ZJets = [2.98,3.15,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49]
# pdf_uvjj_VV = [3.34,3.41,3.62,3.73,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03]
# pdf_uvjj_sTop = [8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77,8.77]


pdf_uujj_TTBar = [4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1]
pdf_uujj_WJets = [3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58]
pdf_uujj_VV = [3.15,3.33,3.63,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15]
pdf_uujj_ZJets = [0.58,1.34,1.93,2.8,4.07,5.96,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62]
pdf_uujj_sTop = [8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43]

pdf_uvjj_WJets = [1.06,1.46,2.3,3.67,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72]
pdf_uvjj_sTop = [8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78]
pdf_uvjj_TTBar = [2.18,3.54,5.16,6.33,7.34,10.01,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36]
pdf_uvjj_ZJets = [2.98,3.15,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49]
pdf_uvjj_VV = [3.35,3.41,3.62,3.73,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03]

pdf_uvjj_Signal = [0.35,0.53,0.83,0.83,0.83,0.83,0.83,0.83,0.83,0.84,1.21,1.21,1.62,1.62,2.22,2.35,2.35,2.35,2.35]
pdf_uujj_Signal = [0.1,0.17,0.18,0.21,0.26,0.26,0.26,0.27,0.29,0.31,0.35,0.36,0.46,0.65,1.06,1.06,1.06,1.06,1.06]
pdf_uujj_Signal = [2.0 for x in pdf_MASS]               
pdf_uvjj_Signal = [3.0 for x in pdf_MASS]               



# These are the total background uncertainties. They are used just to make some error bands on plots. 
totunc_uujj = [3.46, 2.55, 2.98, 3.67, 5.44, 5.73, 6.21, 6.47, 9.47, 11.16, 14.79, 19.75, 31.11, 35.41, 8.12, 8.12, 8.12, 8.12, 8.12]
totunc_uvjj = [13.37, 12.37, 13.35, 12.97, 13.62, 15.94, 16.23, 20.67, 23.94, 30.29, 35.3, 52.94, 69.57, 46.09, 42.3, 42.3, 42.3, 42.3, 42.3]


# Muon alignment Uncs, [uujj sig, uujj bg, uvjj sig, [uvjj bg] ] Only uvjj BG significantly varies with mass
alignmentuncs = [0.1,1.0,1.0,[0.027,0.072,0.205,0.672,1.268,2.592,3.632,4.518,6.698,6.355,5.131,9.615,12.364,16.176,16.176,16.176,16.176,16.176,16.176,16.176]]

# Shape systematics (from running ShapeSystematics.py) in percent
shapesys_uujj_zjets = 2.99
shapesys_uujj_ttbar = 6.27
shapesys_uvjj_wjets = 4.13
shapesys_uvjj_ttbar = 4.72

##########################################################################
########    THE MAIN FUNCTION THAT DEFINES WHAT STUDIES TO DO     ########
##########################################################################



def main():

	#######################################################################################
    ######  The output directories, and the files that define final selection cuts  #######
	#######################################################################################

	# Please retain the "scriptflag" comment. Some python scripts are available which search
	# for this, and make use of it. e.g. For systematic variations, we can in batch instead
	# of running serially, which speeds things up.

	version_name = 'Testing_July24' # scriptflag
	os.system('mkdir Results_'+version_name) 

	MuMuOptCutFile = 'Results_'+version_name+'/Opt_uujjCuts_Smoothed_pol2cutoff.txt' # scriptflag
	MuNuOptCutFile = 'Results_'+version_name+'/Opt_uvjjCuts_Smoothed_pol2cutoff.txt' # scriptflag


	############################################################
    #####  The binning (const or variable) used for plots ######
	############################################################


	ptbinning = [40,60]
	ptbinning2 = [40,60]
	metbinning2 = [0,5]

	stbinning = [250,275]
	bosonbinning = [50,60,70,80,90,100,110,120]
	bosonzoombinning_uujj_Z = [30,50,140]
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
		if ptbinning[-1] < 1500:
			ptbinning.append(ptbinning[-1]+(ptbinning[-1] - ptbinning[-2])*1.2)
		if ptbinning2[-1] < 700:
			ptbinning2.append(ptbinning2[-1]+(ptbinning2[-1] - ptbinning2[-2])*1.2)
		if metbinning2[-1] < 700:
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

	vbinning = [60,0,60]
	nbinning = [10,0,10]

	ptbinning = [round(x) for x in ptbinning]
	ptbinning2 = [round(x) for x in ptbinning2]
	metbinning2 = [round(x) for x in metbinning2]
	stbinning = [round(x) for x in stbinning]
	bosonbinning = [round(x) for x in bosonbinning]
	lqbinning = [round(x) for x in lqbinning]


	#################################################################################
    ##############     A FEW STANDARD PLOTTING ROUTINES AND STUDIES   ###############
	#################################################################################

	# ====================================================================================================================================================== #
	# These are PDF uncertainty studies. Ignore these for now!      ### STILL FIXING THIS PORTION
	# ====================================================================================================================================================== #

	if (False):
		PDF4LHCUncStudy(MuMuOptCutFile,MuNuOptCutFile,version_name)
		PDF4LHCPlotsFromResultDict('Results_'+version_name+'/PDFVariationsDictionary.json',version_name)


	# ====================================================================================================================================================== #
	# The ttbar e-mu data-driven study. You only need to do this once, check the validation output, and use the scale-factor as global variable "emu_id_eff"
	# The scale-factor should be near 0.5
	# ====================================================================================================================================================== #
	if (True):
		# TTBar STudy
		[Rtt_uujj,Rtt_uujj_err] = GetEMuScaleFactors( NormalWeightEMu+'*'+preselectionemu, EMuDirectory)
		Rw_uvjj,Rz_uujj = [1.0,1.0]
		# # PreSelection Plots

		# MakeBasicPlotEMu("Pt_miss","E_{T}^{miss} [GeV]",metbinning2,preselectionemu,NormalWeightEMu,EMuDirectory,'emusel','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("St_uujj","S_{T}^{e #mu j j} [GeV]",stbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emusel','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		exit()
		MakeBasicPlotEMu("M_uu","M^{e #mu} [GeV]",bosonbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emusel','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("M_uujj2","M^{e/#mu j}_{2} [GeV]",lqbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emusel','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("DR_muon1muon2","#DeltaR(#mu,e})",drbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emusel','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)

		MakeBasicPlotEMu("Pt_miss","E_{T}^{miss} [GeV]",metbinning2,preselectionemu,NormalWeightEMu,EMuDirectory,'emuselPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("St_uujj","S_{T}^{e #mu j j} [GeV]",stbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuselPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("M_uu","M^{e #mu} [GeV]",bosonbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuselPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("M_uujj2","M^{e/#mu j}_{2} [GeV]",lqbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuselPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("DR_muon1muon2","#DeltaR(#mu,e})",drbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuselPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)



	# ====================================================================================================================================================== #
	# This is the QCD study. It will make a couple plots, and test QCD contamination at final selection. We consider QCD negligible, but is good to test this once!
	# ====================================================================================================================================================== #
	if (False):
		qcdselectionmumu = '((Pt_muon1>45)*(Pt_muon2>45)*(Pt_jet1>125)*(Pt_jet2>45)*(St_uujj>300)*(DR_muon1muon2>0.3))'
		qcdselectionmunu = '((Pt_muon1>45)*(Pt_muon2<45.0)*(Pt_jet1>125)*(Pt_jet2>45)*(Pt_ele1<45.0)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5))'

		QCDStudy(qcdselectionmumu,qcdselectionmunu,MuMuOptCutFile,MuNuOptCutFile,NormalWeightMuMu,NormalWeightMuNu,version_name)


	# ====================================================================================================================================================== #
	# This is a testing plot routine for use with the new RPV susy sample
	# ====================================================================================================================================================== #
	if (False):

		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
		exit()
		# UUJJ plots at preselection, Note that putting 'TTBarDataDriven' in the name turns on the use of data-driven ttbar e-mu sample in place of MC
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[60,0,600],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MH_uujj","M^{#mu j} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj1","M^{#mu j}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj2","M^{#mu j}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon2jet1","#DeltaR(#mu_{2},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon2jet2","#DeltaR(#mu_{2},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_jet1met","#Delta #phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_jet2met","#Delta #phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu_{1},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu_{1},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon2jet1","#Delta #phi(#mu_{2},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon2jet2","#Delta #phi(#mu_{2},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)


	# ====================================================================================================================================================== #
	# This is a basic plotting routine to make Analysis-Note style plots with ratio plots. 
	# ====================================================================================================================================================== #
	if (False):

		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')


		# Optionally, you can make an event-count table for each selection. Useful if testing a new optimiation
		# We will do this later wtih full systematics for our set of stable cuts. 
		if False:
			QuickTableTTDD(MuMuOptCutFile, preselectionmumu+"*(M_uu>100)",NormalWeightMuMu,Rz_uujj, Rw_uvjj,Rtt_uujj,0)
			QuickTable(MuNuOptCutFile, preselectionmunu,NormalWeightMuNu,Rz_uujj, Rw_uvjj,Rtt_uvjj,0)


		# Here are a few plots which are zoomed-in on control regions. 
		MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonzoombinning_uujj_Z,preselectionmumu,NormalWeightMuMu,NormalDirectory,'controlzoom_ZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metzoombinning_uujj_Z,preselectionmumu+'*(M_uu>80)*(M_uu<100)*(Pt_miss<100)',NormalWeightMuMu,NormalDirectory,'controlzoomZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonzoombinning_uujj_TT,preselectionmumu+'*(M_uu>100)*(Pt_miss>=100)',NormalWeightMuMu,NormalDirectory,'controlzoom_TTRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metzoombinning_uujj_TT,preselectionmumu+'*(M_uu>100)*(Pt_miss>=100)',NormalWeightMuMu,NormalDirectory,'controlzoomTTRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)

		MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonslopebinning_uvjj, preselectionmunu,NormalWeightMuNu,NormalDirectory,'controlzoom_SlopeRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",massslopebining_uvjj,preselectionmunu,NormalWeightMuNu,NormalDirectory,'controlzoom_SlopeRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)


		# UUJJ plots at preselection, Note that putting 'TTBarDataDriven' in the name turns on the use of data-driven ttbar e-mu sample in place of MC
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[60,0,600],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MH_uujj","M^{#mu j} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj1","M^{#mu j}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj2","M^{#mu j}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon2jet1","#DeltaR(#mu_{2},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon2jet2","#DeltaR(#mu_{2},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_jet1met","#Delta #phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_jet2met","#Delta #phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu_{1},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu_{1},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon2jet1","#Delta #phi(#mu_{2},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon2jet2","#Delta #phi(#mu_{2},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)

		# UVJJ plots at preselection, 
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Phi_miss","#phi^{miss} [GeV]",[100,-3.1416,3.1416],preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("St_uvjj","S_{T}^{#mu #nu j j} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MT_uvjj","M_{T}^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MH_uvjj","M^{#mu j} (lead jet only) [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("DPhi_jet1met","#Delta #phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("DPhi_jet2met","#Delta #phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu,j_{1})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu,j_{2})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)



		# Full Selection Plots
		for lqmass in [300,500,700,900]:
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)

			# MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uujj2","M^{#mu j}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("St_uvjj","S_{T}^{#mu #nu j j} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uujj2","M^{#mu j}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)


		os.system('echo Combining Figures; convert -density 800 Results_'+version_name+'/*png Results_'+version_name+'/AllPlots.pdf')



	# ====================================================================================================================================================== #
	# This is a plotting routine for PAS-style publication-quality plots
	# ====================================================================================================================================================== #

	if False:


		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')

		# Here are a few plots which are zoomed-in on control regions. 
		MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",[20,80,100],preselectionmumu,NormalWeightMuMu,NormalDirectory,'controlzoomPASTTBarDataDriven_ZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonzoombinning_uujj_Z,preselectionmumu,NormalWeightMuMu,NormalDirectory,'controlzoomPAS_ZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		bosonzoombinning_uvjj = [20,70,110]
		MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)',NormalWeightMuNu,NormalDirectory,'controlzoomPAS_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)',NormalWeightMuNu,NormalDirectory,'controlzoomPAS_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		exit()

		# sys.exit()

		# Preselection plots in the UUJJ channel in the PAS style (no subplot)
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MH_uujj","M^{#mu j} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj1","M^{#mu j}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj2","M_{min}(#mu, jet) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)


		# Preselection plots in the UVJJ channel in the PAS style (no subplot)
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("St_uvjj","S_{T}^{#mu #nu j j} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MT_uvjj","M_{T}^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MH_uvjj","M^{#mu j} (lead jet only) [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		# Full Selection Plots in the PAS style
		for lqmass in [300,400, 500,600,700,800,900,1000,1100]:
			MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDrivenPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDrivenPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uujj2","M_{min}(#mu, jet) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDrivenPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("St_uvjj","S_{T}^{#mu #nu j j} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)



	# ====================================================================================================================================================== #
	# This runs a "FullAnalysis" - i.e. produces tables with full systematis included. 
	# ====================================================================================================================================================== #

	# You can run this to make the full set of tables needed to construct the higgs card. This takes a long time!
	# Alternatively, you can run > python SysBatcher.py --launch to do each table in a separate batch job
	# When done, proceed to the next step to make higgs limit cards
	if (False):
		FullAnalysis(MuMuOptCutFile, preselectionmumu,preselectionmunu,NormalDirectory,NormalWeightMuMu,'TTBarDataDriven')  # scriptflag
		FullAnalysis(MuNuOptCutFile, preselectionmumu,preselectionmunu,NormalDirectory,NormalWeightMuNu,'normal')  # scriptflag

	if (False):
		uujjcardfiles = MuMuOptCutFile.replace('.txt','_systable*.txt')
		uvjjcardfiles = MuNuOptCutFile.replace('.txt','_systable*.txt')

		uujjcards = ParseFinalCards(uujjcardfiles)
		uvjjcards = ParseFinalCards(uvjjcardfiles)
		finalcards = FixFinalCards([uujjcards,uvjjcards])

		print 'Final Cards Available in ',finalcards




	# ====================================================================================================================================================== #
	# These are some plots with the systematic variations turned on. They are just sanity checks and not part of any normal procedure
	# ====================================================================================================================================================== #
	if (False):

		for sample in ['ScaleUp','ScaleDown','MatchUp','MatchDown']:
			preselectionmunu_mod = preselectionmunu
			NormalWeightMuNu_mod = NormalWeightMuNu
			Rz_uujj = 1.0
			[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactorsMod( NormalWeightMuNu_mod+'*'+preselectionmunu_mod, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)',sample)
			MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2}) "+sample,drbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sysmethod in ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','PUup','PUdown']:
			preselectionmunu_mod = ModSelection(preselectionmunu,sysmethod,MuNuOptCutFile)
			NormalWeightMuNu_mod = ModSelection(NormalWeightMuNu,sysmethod,MuNuOptCutFile)

			Rz_uujj = 1.0
			[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu_mod+'*'+preselectionmunu_mod, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
			MakeBasicPlot(ModSelection("M_uvjj",sysmethod,MuNuOptCutFile),"M^{#mu j} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sysmethod,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot(ModSelection("MT_uv",sysmethod,MuNuOptCutFile),"M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sysmethod,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sample in ['ScaleUp','ScaleDown','MatchUp','MatchDown']:
			Rw_uvjj = 1.0
			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactorsMod( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',sample)
			# MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			# MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV] "+sample,ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardTTBarDataDriven_sys'+sample,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV] "+sample,ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardTTBarDataDriven_sys'+sample,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			rescale_string = MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)',NormalWeightMuNu,NormalDirectory,'standard_rescaletest_pre','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sysmethod in ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','PUup','PUdown']:
			preselectionmumu_mod = ModSelection(preselectionmumu,sysmethod,MuMuOptCutFile)
			NormalWeightMuMu_mod = ModSelection(NormalWeightMuMu,sysmethod,MuMuOptCutFile)

			Rw_uvjj = 1.0

			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu_mod+'*'+preselectionmumu_mod, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)')

			MakeBasicPlot(ModSelection("Pt_jet1",sysmethod,MuMuOptCutFile),"p_{T}(jet_{1}) [GeV] "+sysmethod,ptbinning,preselectionmumu_mod,NormalWeightMuMu_mod,NormalDirectory,'standard_sys'+sysmethod,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot(ModSelection("Pt_jet2",sysmethod,MuMuOptCutFile),"p_{T}(jet_{2}) [GeV] "+sysmethod,ptbinning,preselectionmumu_mod,NormalWeightMuMu_mod,NormalDirectory,'standard_sys'+sysmethod,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)




####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################

signal = 'LQToCMu_M_250'

for n in range(len(sys.argv)):
	if sys.argv[n]=='-v' or sys.argv[n]=='--version_name':
		if len(sys.argv)<=n+1:
			print 'No version name specified. Exiting.'
			exit()
		version_name=sys.argv[n+1]
	if sys.argv[n]=='-s' or sys.argv[n]=='--signal':
		if len(sys.argv)<=n+1:
			print 'No signal specified. Exiting.'
			exit()
		signal=sys.argv[n+1]

# os.system('rm -r Results_'+version_name)


##########################################################################
########            All functions and Details Below               ########
##########################################################################

import math
sys.argv.append( '-b' )
from ROOT import *
gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")
TFormula.SetMaxima(100000,1000,1000000)
import numpy
import math
rnd= TRandom3()
person = (os.popen('whoami').readlines()[0]).replace("\n",'')

for f in os.popen('ls '+NormalDirectory+"| grep \".root\"").readlines():
	exec ('t_'+f.replace(".root\n","")+" = TFile.Open(\""+NormalDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	print('t_'+f.replace(".root\n","")+" = TFile.Open(\""+NormalDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")

for f in os.popen('ls '+EMuDirectory+"| grep \".root\"").readlines():
	exec('te_'+f.replace(".root\n","")+" = TFile.Open(\""+EMuDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")

for f in os.popen('ls '+QCDDirectory+"| grep \".root\"").readlines():
	exec('tn_'+f.replace(".root\n","")+" = TFile.Open(\""+QCDDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")



##########################################################################
########              Clean up ROOT  Style                        ########
##########################################################################
gROOT.SetStyle('Plain')
gStyle.SetOptTitle(0)
from array import array
NCont = 50
NRGBs = 5
stops = array("d",[ 0.00, 0.34, 0.61, 0.84, 1.00])
red= array("d",[ 0.00, 0.00, 0.87, 1.00, 0.51 ])
green= array("d",[ 0.00, 0.81, 1.00, 0.20, 0.00 ])
blue= array("d",[ 0.51, 1.00, 0.12, 0.00, 0.00 ])
TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
gStyle.SetNumberContours(NCont)
##########################################################################
##########################################################################



def PDF4LHCUncStudy(MuMuOptCutFile,MuNuOptCutFile,versionname):

	N_cteq = 53
	N_nnpdf = 101
	N_mstw = 41
	# N_cteq = 3
	# N_nnpdf = 0
	# N_mstw = 0
	cteqweights = ['*(factor_cteq_'+str(n+1)+'/factor_cteq_1)' for n in range(N_cteq)]
	nnpdfweights = ['*(factor_nnpdf_'+str(n+1)+'/factor_cteq_1)' for n in range(N_nnpdf)]
	mstwweights = ['*(factor_mstw_'+str(n+1)+'/factor_cteq_1)' for n in range(N_mstw)]

	ResultList = []
	ResultDict = {}
	MuMuSels = []
	MuNuSels = []

	# Get selections
	for line in open(MuMuOptCutFile,'r'):
		if '=' in line:
			MuMuSels.append(line.split('=')[-1].replace('\n','').replace(' ',''))
	for line in open(MuNuOptCutFile,'r'):
		if '=' in line:
			MuNuSels.append(line.split('=')[-1].replace('\n','').replace(' ',''))


	# UUJJ CHANNEL SYSTEMATICS

	# treenames = ['ZJets','Signal']
	treenames = ['ZJets','TTBar','WJets','VV','sTop','Signal']
	uncnames = ['pdf_uujj_'+x for x in treenames]
	# trees  = [[t_ZJetsJBin]]
	trees  = [[t_ZJetsJBin],[t_TTBarDBin],[t_WJetsJBin],[t_DiBoson],[t_SingleTop]]
	trees.append([t_LQuujj300,t_LQuujj350,t_LQuujj400,t_LQuujj450,t_LQuujj500,t_LQuujj550,t_LQuujj600,t_LQuujj650,t_LQuujj700,t_LQuujj750,t_LQuujj800,t_LQuujj850,t_LQuujj900,t_LQuujj950,t_LQuujj1000,t_LQuujj1050,t_LQuujj1100,t_LQuujj1150,t_LQuujj1200])


	# ================================================================================================================
	# Loop over trees to consider
	for ii in range(len(trees)):
		junkfile = TFile.Open('myjunkfileforpdfanalysis.root','RECREATE')

		# Speed up by copying to new preselection tree
		ntree = 0
		systematic = '0.0'
		_t = trees[ii][ntree]
		norm_sel = '(1)'
		print 'Analyzing',  uncnames[ii], 'in the uujj channel. Systematics are:'
		result = uncnames[ii]+' = ['
		ResultDict[uncnames[ii]+'_uujj'] = {}
		ResultDict[uncnames[ii]+'_uujj']['cteq'] = []
		ResultDict[uncnames[ii]+'_uujj']['mstw'] = []
		ResultDict[uncnames[ii]+'_uujj']['nnpdf'] = []		
		if 'ZJets' in uncnames[ii]:
			norm_sel = '(M_uu>80)*(M_uu<100)'
		_tnew = _t.CopyTree(preselectionmumu + '*'+norm_sel)
		# Get the preselection values for all PDF members
		presel_central_value = QuickIntegral(_tnew,NormalWeightMuMu,1.0)[0]
		presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweights]
		presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in nnpdfweights]
		presel_varied_mstw_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in mstwweights]
		# Loop over selections
		for _sel in MuMuSels:
			print '   ... using tree ',trees[ii][ntree]
			if 'Signal' in uncnames[ii]:
				_t = trees[ii][ntree]
				ntree += 1
				_tnew = _t.CopyTree(preselectionmumu + '*'+norm_sel)
				# Get the preselection values for all PDF members
				presel_central_value = QuickIntegral(_tnew,NormalWeightMuMu,1.0)[0]
				presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweights]
				presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in nnpdfweights]
				presel_varied_mstw_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in mstwweights]

			# Copy tree to new final selection tree
			_tnewsel = _t.CopyTree(preselectionmumu+'*'+_sel)
			if _tnewsel.GetEntries()<100 and ResultDict[uncnames[ii]+'_uujj']['cteq'] != []:
				ResultDict[uncnames[ii]+'_uujj']['cteq'].append(  ResultDict[uncnames[ii]+'_uujj']['cteq'][-1] )
				ResultDict[uncnames[ii]+'_uujj']['mstw'].append(  ResultDict[uncnames[ii]+'_uujj']['mstw'][-1] )
				ResultDict[uncnames[ii]+'_uujj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uujj']['nnpdf'][-1] )					
				continue
			# Get the final-selection integrals
			finsel_central_value=QuickIntegral(_tnewsel,NormalWeightMuMu,1.0)[0]
			finsel_varied_cteq_values = [QuickIntegral(_tnewsel,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweights]
			finsel_varied_nnpdf_values = [QuickIntegral(_tnewsel,NormalWeightMuMu+_fact,1.0)[0] for _fact in nnpdfweights]
			finsel_varied_mstw_values = [QuickIntegral(_tnewsel,NormalWeightMuMu+_fact,1.0)[0] for _fact in mstwweights]

			# Normalize Z and Signal at preselection
			if 'ZJet' in uncnames[ii] or 'Signal' in uncnames[ii]:
				finsel_central_value /= presel_central_value
				finsel_varied_cteq_values = [finsel_varied_cteq_values[jj]/presel_varied_cteq_values[jj] for jj in range(len(presel_varied_cteq_values))]
				finsel_varied_mstw_values = [finsel_varied_mstw_values[jj]/presel_varied_mstw_values[jj] for jj in range(len(presel_varied_mstw_values))]
				finsel_varied_nnpdf_values = [finsel_varied_nnpdf_values[jj]/presel_varied_nnpdf_values[jj] for jj in range(len(presel_varied_nnpdf_values))]

			if finsel_central_value >0.0:
				# Get the variations w.r.t the central memeber
				finsel_varied_cteq_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_cteq_values]
				finsel_varied_mstw_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_mstw_values]
				finsel_varied_nnpdf_diffs =[abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_nnpdf_values]

				sfinsel_varied_cteq_diffs = [(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_cteq_values]
				sfinsel_varied_mstw_diffs = [(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_mstw_values]
				sfinsel_varied_nnpdf_diffs =[(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_nnpdf_values]

				# Adjust cteq to 68% CL
				finsel_varied_cteq_diffs = [xx/1.645  for xx in finsel_varied_cteq_diffs]
				ResultDict[uncnames[ii]+'_uujj']['cteq'].append(  [100*jj for jj in sfinsel_varied_cteq_diffs])
				ResultDict[uncnames[ii]+'_uujj']['mstw'].append(  [100*jj for jj in sfinsel_varied_mstw_diffs])
				ResultDict[uncnames[ii]+'_uujj']['nnpdf'].append( [100*jj for jj in sfinsel_varied_nnpdf_diffs])
		

				old_systematic = str(systematic)
				systematic = str(round(100.0*max( finsel_varied_cteq_diffs + finsel_varied_mstw_diffs + finsel_varied_nnpdf_diffs ),3))
				if float(systematic) < float(old_systematic):
					systematic = str(old_systematic)

				if float(systematic) > 100.0:
					systematic = '100.0'
			else:
				ResultDict[uncnames[ii]+'_uujj']['cteq'].append(  ResultDict[uncnames[ii]+'_uujj']['cteq'][-1] )
				ResultDict[uncnames[ii]+'_uujj']['mstw'].append(  ResultDict[uncnames[ii]+'_uujj']['mstw'][-1] )
				ResultDict[uncnames[ii]+'_uujj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uujj']['nnpdf'][-1] )		
			# print ResultDict
			print systematic+'%'
			result += systematic+','
			junkfile.Close()


		result = result[:-1]+']'
		ResultList.append(result)



	# ================================================================================================================
	# UvJJ CHANNEL SYSTEMATICS

	# treenames = ['TTBar','WJets','Signal']
	treenames = ['ZJets','TTBar','WJets','VV','sTop','Signal']
	uncnames = ['pdf_uvjj_'+x for x in treenames]
	# trees  = [[t_TTBarDBin],[t_WJetsJBin]]
	trees  = [[t_ZJetsJBin],[t_TTBarDBin],[t_WJetsJBin],[t_DiBoson],[t_SingleTop]]
	trees.append([t_LQuvjj300,t_LQuvjj350,t_LQuvjj400,t_LQuvjj450,t_LQuvjj500,t_LQuvjj550,t_LQuvjj600,t_LQuvjj650,t_LQuvjj700,t_LQuvjj750,t_LQuvjj800,t_LQuvjj850,t_LQuvjj900,t_LQuvjj950,t_LQuvjj1000,t_LQuvjj1050,t_LQuvjj1100,t_LQuvjj1150,t_LQuvjj1200])


	# Loop over trees to consider
	for ii in range(len(trees)):
		junkfile = TFile.Open('myjunkfileforpdfanalysis.root','RECREATE')

		# Speed up by copying to new preselection tree
		ntree = 0
		systematic = '0.0'
		_t = trees[ii][ntree]
		norm_sel = '(1)'
		print 'Analyzing',  uncnames[ii], 'in the uvjj channel. Systematics are:'
		result = uncnames[ii]+' = ['
		ResultDict[uncnames[ii]+'_uvjj'] = {}
		ResultDict[uncnames[ii]+'_uvjj']['cteq'] = []
		ResultDict[uncnames[ii]+'_uvjj']['mstw'] = []
		ResultDict[uncnames[ii]+'_uvjj']['nnpdf'] = []				
		result = uncnames[ii]+' = ['
		if 'WJets' in uncnames[ii]:
			norm_sel = '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)'
		if 'TTBar' in uncnames[ii]:
			norm_sel = '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)'		
		_tnew = _t.CopyTree(preselectionmunu + '*'+norm_sel)
		# Get the preselection values for all PDF members
		presel_central_value = QuickIntegral(_tnew,NormalWeightMuNu,1.0)[0]
		presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in cteqweights]
		presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in nnpdfweights]
		presel_varied_mstw_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in mstwweights]
		# Loop over selections
		for _sel in MuNuSels:
			print '   ... using tree ',trees[ii][ntree]
			if 'Signal' in uncnames[ii]:
				_t = trees[ii][ntree]
				ntree += 1
				_tnew = _t.CopyTree(preselectionmunu + '*'+norm_sel)
				# Get the preselection values for all PDF members
				presel_central_value = QuickIntegral(_tnew,NormalWeightMuNu,1.0)[0]
				presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in cteqweights]
				presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in nnpdfweights]
				presel_varied_mstw_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in mstwweights]

			# Copy tree to new final selection tree
			_tnewsel = _t.CopyTree(preselectionmunu+'*'+_sel)
			if _tnewsel.GetEntries()<100  and ResultDict[uncnames[ii]+'_uvjj']['cteq'] != []:
				ResultDict[uncnames[ii]+'_uvjj']['cteq'].append(  ResultDict[uncnames[ii]+'_uvjj']['cteq'][-1] )
				ResultDict[uncnames[ii]+'_uvjj']['mstw'].append(  ResultDict[uncnames[ii]+'_uvjj']['mstw'][-1] )
				ResultDict[uncnames[ii]+'_uvjj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uvjj']['nnpdf'][-1] )	
				continue				
			# Get the final-selection integrals
			finsel_central_value=QuickIntegral(_tnewsel,NormalWeightMuNu,1.0)[0]
			finsel_varied_cteq_values = [QuickIntegral(_tnewsel,NormalWeightMuNu+_fact,1.0)[0] for _fact in cteqweights]
			finsel_varied_nnpdf_values = [QuickIntegral(_tnewsel,NormalWeightMuNu+_fact,1.0)[0] for _fact in nnpdfweights]
			finsel_varied_mstw_values = [QuickIntegral(_tnewsel,NormalWeightMuNu+_fact,1.0)[0] for _fact in mstwweights]

			# Normalize W, TTBar, and Z at preselection
			if 'WJet' in uncnames[ii] or 'TTBar' in uncnames[ii] or 'Signal' in uncnames[ii]:
				finsel_central_value /= presel_central_value
				finsel_varied_cteq_values = [finsel_varied_cteq_values[jj]/presel_varied_cteq_values[jj] for jj in range(len(presel_varied_cteq_values))]
				finsel_varied_mstw_values = [finsel_varied_mstw_values[jj]/presel_varied_mstw_values[jj] for jj in range(len(presel_varied_mstw_values))]
				finsel_varied_nnpdf_values = [finsel_varied_nnpdf_values[jj]/presel_varied_nnpdf_values[jj] for jj in range(len(presel_varied_nnpdf_values))]

			if finsel_central_value >0.0:
				# Get the variations w.r.t the central memeber
				finsel_varied_cteq_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_cteq_values]
				finsel_varied_mstw_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_mstw_values]
				finsel_varied_nnpdf_diffs =[abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_nnpdf_values]

				sfinsel_varied_cteq_diffs = [(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_cteq_values]
				sfinsel_varied_mstw_diffs = [(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_mstw_values]
				sfinsel_varied_nnpdf_diffs =[(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_nnpdf_values]

				# Adjust cteq to 68% CL
				finsel_varied_cteq_diffs = [xx/1.645  for xx in finsel_varied_cteq_diffs]
				ResultDict[uncnames[ii]+'_uvjj']['cteq'].append([100*jj for jj in sfinsel_varied_cteq_diffs])
				ResultDict[uncnames[ii]+'_uvjj']['mstw'].append([100*jj for jj in sfinsel_varied_mstw_diffs])
				ResultDict[uncnames[ii]+'_uvjj']['nnpdf'].append([100*jj for jj in sfinsel_varied_nnpdf_diffs])

				old_systematic = str(systematic)
				systematic = str(round(100.0*max( finsel_varied_cteq_diffs + finsel_varied_mstw_diffs + finsel_varied_nnpdf_diffs ),3))
				if float(systematic) < float(old_systematic):
					systematic = str(old_systematic)

				if float(systematic) > 100.0:
					systematic = '100.0'
			else:
				ResultDict[uncnames[ii]+'_uvjj']['cteq'].append(  ResultDict[uncnames[ii]+'_uvjj']['cteq'][-1] )
				ResultDict[uncnames[ii]+'_uvjj']['mstw'].append(  ResultDict[uncnames[ii]+'_uvjj']['mstw'][-1] )
				ResultDict[uncnames[ii]+'_uvjj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uvjj']['nnpdf'][-1] )	
			print systematic+'%'
			result += systematic+','
			junkfile.Close()

		result = result[:-1]+']'
		ResultList.append(result)

	json_name = 'Results_'+versionname+'/PDFVariationsDictionary.json'
	print ' -------- Creating JSON file: ',json_name
	import json
	json.dump(ResultDict, open(json_name, 'wb'))


	# print '\n\n---------- Summary of PDF systematics as percentages --------\n'
	# for result in ResultList:
	# 	print result
	# print '\n\n'



def PDF4LHCPlotsFromResultDict(filename,versionname):
	import json
	dictionary = json.load(open(filename))
	
	mass = [300 + x*50 for x in range(19)]

	resultlist = []

	def rms(X):
		n = 0.0
		rms = 0.0
		for x in X:
			n += 1.0
			rms += x*x
		rms = rms/n
		rms = math.sqrt(rms)
		return rms

	for key in dictionary:
		result = key + ' = ['
		print 'Evaluating PDF bands for',key
		basename = key.split('_')
		chan = '#mu #mu jj'*('uujj' in basename) + '#mu #nu jj'*('uvjj' in basename)
		data = dictionary[key]

		c0 = TCanvas("c1","",1200,900)
		gStyle.SetOptStat(0)
		cl = TH1F('cl','cl',1,275,1225)
		cl.SetLineStyle(2)
		gStyle.SetOptTitle(1)
		cl.GetXaxis().SetTitle("LQ Mass [GeV]")
		cl.GetYaxis().SetTitle("Percent Variation")
		cl.SetTitle(basename[2]+' '+chan) 
		rmax = 1.0
		for pdfset in data:
			vsets = data[pdfset]
			for vset in vsets:
				for v in vset:
					if abs(v) > rmax:
						rmax = abs(v)
		# rmax *=0.6
		if rmax > 200.0:
			rmax = 200.0
		print '    ... Drawing for variations up to ',rmax,'percent.'

		cl.SetMaximum(1.0*rmax)
		cl.SetMinimum(-1.0*(rmax))
		cl.Draw()

		hlist = []
		Crms, Mrms, Nrms, Ms = [],[],[],[]

		cteq,mstw,nnpd = [],[],[]
		old_systematic = 0.0
		systematic = 0.0
		for imass in range(len(mass)):


			old_cteq = list(cteq)
			old_mstw = list(mstw)
			old_nnpd = list(nnpd)

			cteq = data['cteq'][imass]
			mstw = data['mstw'][imass]
			nnpd = data['nnpdf'][imass]

			if cteq == old_cteq or old_cteq == [0]:
				cteq = [0]
			if mstw == old_mstw or old_mstw == [0]:
				mstw = [0]
			if nnpd == old_nnpd or  old_nnpd == [0]:
				nnpd = [0]

			C, M, N = array('d',cteq), array('d',mstw), array('d',nnpd)
			m = mass[imass]
			Cm = array('d',[m for x in C])
			Mm = array('d',[m-7. for x in M])
			Nm = array('d',[m+7. for x in N])

			# print C
			Crms.append(rms(C))
			Mrms.append(rms(M))
			Nrms.append(rms(N))

			old_systematic = systematic
			systematic = max([ Crms[-1],Mrms[-1],Nrms[-1] ])
			if systematic < old_systematic:
				systematic = old_systematic
			result += (str(round(systematic,2))) + ','
			Ms.append(1.0*m)

			hlist.append(TGraph(len(C), Cm, C))
			hlist[-1].SetMarkerStyle(24)
			hlist[-1].SetMarkerColor(6)
			hlist[-1].SetMarkerSize(0.3)

			hlist.append(TGraph(len(M), Mm, M))
			hlist[-1].SetMarkerStyle(24)
			hlist[-1].SetMarkerColor(2)
			hlist[-1].SetMarkerSize(0.3)	

			hlist.append(TGraph(len(N), Nm, N))
			hlist[-1].SetMarkerStyle(24)
			hlist[-1].SetMarkerColor(4)	
			hlist[-1].SetMarkerSize(0.3)


		result = result[:-1]
		result += ']'
		resultlist.append(result)
		print result
		for plot in hlist:
			plot.Draw("P")



		leg = TLegend(0.12,0.77,0.27,0.89,"","brNDC")
		leg.SetTextFont(42)
		leg.SetFillColor(0)
		leg.SetBorderSize(0)
		leg.SetTextSize(.037)


		Crmsclone = list(Crms)
		Nrmsclone = list(Nrms)
		Mrmsclone = list(Mrms)
		Msclone = list(Ms)

		for xx in range(len(Crms)):
			Crms.append(-1.0*Crmsclone[-1-xx])
			Nrms.append(-1.0*Nrmsclone[-1-xx])
			Mrms.append(-1.0*Mrmsclone[-1-xx])
			Ms.append(Msclone[-1-xx])

		Crms.append(Crms[0])
		Mrms.append(Mrms[0])
		Nrms.append(Nrms[0])
		Ms.append(Ms[0])

		Crms = array('d',Crms)
		Nrms = array('d',Nrms)
		Mrms = array('d',Mrms)
		Ms = array('d',Ms)

		cwin = TPolyLine(len(Crms),Ms,Crms,"")
		cwin.SetFillColor(6)
		cwin.SetLineColor(6)
		cwin.SetLineWidth(2)
		cwin.Draw("L")

		mwin = TPolyLine(len(Mrms),Ms,Mrms,"")
		mwin.SetFillColor(2)
		mwin.SetLineColor(2)
		mwin.SetLineWidth(2)
		mwin.Draw("L")

		nwin = TPolyLine(len(Nrms),Ms,Nrms,"")
		nwin.SetFillColor(4)
		nwin.SetLineColor(4)
		nwin.SetLineWidth(2)
		nwin.Draw("L")

		ch=TH1F()
		ch.SetLineColor(6)
		ch.SetMarkerColor(6)
		ch.SetLineWidth(2)

		mh=TH1F()
		mh.SetLineColor(2)
		mh.SetMarkerColor(2)
		mh.SetLineWidth(2)

		nh=TH1F()
		nh.SetLineColor(4)
		nh.SetMarkerColor(4)
		nh.SetLineWidth(2)

		leg.AddEntry(ch,"CT10")
		leg.AddEntry(mh,"MSTW")
		leg.AddEntry(nh,"NNPDF")
		leg.Draw()


		c0.Print('Results_'+versionname+'/PDFValidation_'+key+'.pdf')
		c0.Print('Results_'+versionname+'/PDFValidation_'+key+'.png')

	print '\n\n---------- Summary of PDF systematics as percentages --------\n'
	for result in resultlist:
		print result
	print '\n\n'

	# os.system('convert -density 400 Results_'+versionname+'/PDFValidation*png Results_'+versionname+'/PDFValidation_ValPlots.pdf')
	gStyle.SetOptTitle(0)


def FixDrawLegend(legend):
	legend.SetTextFont(42)
	legend.SetFillColor(0)
	legend.SetBorderSize(0)
	legend.Draw()
	return legend

def ConvertBinning(binning):
	binset=[]
	if len(binning)==3:
		for x in range(binning[0]+1):
			binset.append(((binning[2]-binning[1])/(1.0*binning[0]))*x*1.0+binning[1])
	else:
		binset=binning
	return binset

gStyle.SetPadTopMargin(0.1);
gStyle.SetPadBottomMargin(0.16);
gStyle.SetPadLeftMargin(0.12);
#gStyle.SetPadRightMargin(0.12);
gStyle.SetPadRightMargin(0.1);

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
	hout.GetXaxis().SetLabelSize(0.05)
	hout.GetYaxis().SetLabelSize(0.05)

	hout.GetXaxis().SetTitleOffset(0.92)
	hout.GetYaxis().SetTitleOffset(0.92)
	hout.GetXaxis().SetTitleSize(0.06)
	hout.GetYaxis().SetTitleSize(0.06)
	hout.GetXaxis().CenterTitle(1)
	hout.GetYaxis().CenterTitle(1)

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
	histo.GetXaxis().SetTitle(label[0])
	histo.GetYaxis().SetTitle(label[1])
	histo.GetXaxis().SetTitleFont(42)
	histo.GetYaxis().SetTitleFont(42)
	histo.GetXaxis().SetLabelFont(42)
	histo.GetYaxis().SetLabelFont(42)
	return histo

def BeautifyStack(stack,label):
	stack.GetHistogram().GetXaxis().SetTitleFont(42)
	stack.GetHistogram().GetYaxis().SetTitleFont(42)
	stack.GetHistogram().GetXaxis().SetLabelFont(42)
	stack.GetHistogram().GetYaxis().SetLabelFont(42)
	stack.GetHistogram().GetXaxis().SetTitle(label[0])
	stack.GetHistogram().GetYaxis().SetTitle(label[1])
	stack.GetHistogram().GetXaxis().SetTitle(label[0])
	stack.GetHistogram().GetYaxis().SetTitle(label[1])
	stack.GetHistogram().GetXaxis().SetTitleFont(42)
	stack.GetHistogram().GetYaxis().SetTitleFont(42)
	stack.GetHistogram().GetXaxis().SetLabelFont(42)
	stack.GetHistogram().GetYaxis().SetLabelFont(42)
	stack.GetHistogram().GetXaxis().SetLabelOffset(0.007)
	stack.GetHistogram().GetYaxis().SetLabelOffset(0.007)
	stack.GetHistogram().GetXaxis().SetLabelSize(0.05)
	stack.GetHistogram().GetYaxis().SetLabelSize(0.05)

	stack.GetHistogram().GetXaxis().SetTitleOffset(0.92)
	stack.GetHistogram().GetYaxis().SetTitleOffset(0.92)
	stack.GetHistogram().GetXaxis().SetTitleSize(0.06)
	stack.GetHistogram().GetYaxis().SetTitleSize(0.06)
	stack.GetHistogram().GetXaxis().CenterTitle(1)
	stack.GetHistogram().GetYaxis().CenterTitle(1)
	return stack

def QuickFIntegral(tree,selection,scalefac):

	h = TH1F('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection+'*'+str(scalefac))
	I = h.GetBinContent(1)
	E = h.GetBinError(1)
	return [I,E]

def QuickIntegral(tree,selection,scalefac):

	# print selection+'*'+str(scalefac)
	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection+'*'+str(scalefac))
	I = h.GetBinContent(1)
	E = h.GetBinError(1)
	return [I,E]

def QuickSysIntegral(tree,selection,scalefac,globalscalefac):

	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection+'*'+str(globalscalefac*scalefac))
	I = h.Integral()
	E = h.GetEntries()
	return str([I,int(E)])

def QuickMultiIntegral(trees,selection,scalefacs):

	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
 	nn = -1
 	for _ib in trees:
 		nn += 1
 		exec('_bb'+str(n)+' = TH1D(\''+'_bb'+str(n)+'\',\'_bb'+str(n)+'\',1,-1,3)')
 		exec('_bb'+str(n)+'.Sumw2()')
		_ib.Project('_bb'+str(n),'1.0',selection+'*'+str(scalefacs[nn]))
 		exec('h.Add(_bb'+str(n)+')')
	I = h.GetBinContent(1)
	E = h.GetBinError(1)
	return [I,E]

def QuickEntries(tree,selection,scalefac):

	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection)
	I = h.GetEntries()
	return [1.0*I*scalefac, math.sqrt(1.0*I*scalefac)]

def QuickSysEntries(tree,selection,scalefac):

	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection)
	I = h.GetEntries()
	return str([int(1.0*I*scalefac),int(1.0*I*scalefac)]) 

def QCDStudy(sel_mumu,sel_munu,cutlogmumu,cutlogmunu,weight_mumu,weight_munu,version_name):


	#################################
	######## DIMUON CHANNEL #########
	#################################	
	print '\n------ DIMUON CHANNEL -------\n\n'
	Q_ss = QuickIntegral(tn_QCDMu,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)	
	Q_os = QuickIntegral(tn_QCDMu,sel_mumu + '*(Charge_muon1*Charge_muon2 < 0)*'+weight_mumu,1.0)

	print Q_ss
	print Q_os
	# sys.exit()
	studyvals = []
	for x in range(1000):
		same = RR(Q_ss)
		opp = RR(Q_os)	
		studyvals.append( (same + opp) /same )
	sameoppscale =  GetStats(studyvals)
	print "\n\nIn QCD MC, the conversion factor between same-sign muon events and all events is:", texentry4(sameoppscale)

	Q_ssiso = QuickIntegral(tn_QCDMu,sel_mumu+'*(TrkIso_muon1<0.1)*'+weight_mumu,1.0)
	studyvals = []
	for x in range(1000):
		same = RR(Q_ss)
		isosame  = RR(Q_ssiso)	
		studyvals.append( isosame/same )
	singleisoscale =  GetStats(studyvals)
	print "In QCD MC, the single-muon isolation acceptance is:", texentry4(singleisoscale)

	isoscale = [singleisoscale[0]**2, 2*singleisoscale[0]*singleisoscale[1]]
	print "In QCD MC, the conversion factor between non-isolated di-muon events and isolated dimuon events is:", texentry4(isoscale)

	SSNonIsoDataRescale = [isoscale[0]*sameoppscale[0], isoscale[0]*sameoppscale[0]*(math.sqrt( (isoscale[1]/isoscale[0])**2 + (sameoppscale[1]/sameoppscale[0])**2) )    ]
	print "Thus, in Same-Sign non-iso data, a factor of :", texentry4(SSNonIsoDataRescale), 'will give the QCD estiamte.'

	sel_mumu_ss = sel_mumu#+'*(Charge_muon1*Charge_muon2 > 0)'
	MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,2.0,5.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_noniso','uujj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,2.0,5.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_noniso','uujj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,1.5,2.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisoPAS','uujj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,1.5,2.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisoPAS','uujj',1.0,1.0,1.0,version_name,1.0)


	print '\nFor final selections, this gives estimates:\n'


	for plotmass in [300,350,400,450,500,550,600,650,700,750,800]:
		channel='uujj'
		fsel = ((os.popen('cat '+cutlogmumu+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+sel_mumu+fsel+')'

		Nss_noniso_data = QuickEntries(tn_SingleMuData,selection + '*(Charge_muon1*Charge_muon2 > 0)',1.0)
		Nss_noniso_mc = QuickMultiIntegral([tn_DiBoson,tn_TTBarDBin,tn_WJetsJBin,tn_ZJetsJBin,tn_SingleTop],selection+'*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,[1.0,1.0,1.0,1.0,1.0])		
		Nss_noniso_qcdest = [Nss_noniso_data[0] - Nss_noniso_mc[0] ,  math.sqrt(Nss_noniso_data[1]**2 + Nss_noniso_mc[1]**2)]
		N_iso_qcdest = [ Nss_noniso_qcdest[0]*SSNonIsoDataRescale[0], (math.sqrt((Nss_noniso_qcdest[1]/Nss_noniso_qcdest[0])**2 + (SSNonIsoDataRescale[1]/SSNonIsoDataRescale[0])**2))*Nss_noniso_qcdest[0]*SSNonIsoDataRescale[0] ]

		print plotmass ,'&',texentry4(N_iso_qcdest),'\\\\'

	print '\n'

	#################################
	######## 1 MUON CHANNEL #########
	#################################	
	print '\n------ MUON+MET CHANNEL -------\n\n'

	sel_low_munu = sel_munu + '*(Pt_miss<10)'

	# print sel_low_munu

	D_noniso = QuickEntries(tn_SingleMuData,sel_low_munu,1.0)	
	D_iso = QuickEntries(tn_SingleMuData,sel_low_munu + '*(TrkIso_muon1<0.1)',1.0)	

	Q_noniso = QuickIntegral(tn_QCDMu,sel_low_munu+'*'+weight_munu,1.0)	
	Q_iso = QuickIntegral(tn_QCDMu,sel_low_munu + '*(TrkIso_muon1<0.1)*'+weight_munu,1.0)	

	B_noniso = QuickMultiIntegral([tn_DiBoson,tn_TTBarDBin,tn_WJetsJBin,tn_ZJetsJBin,tn_SingleTop],sel_low_munu+'*'+weight_munu,[1.0,1.0,1.0,1.0,1.0])
	B_iso = QuickMultiIntegral([tn_DiBoson,tn_TTBarDBin,tn_WJetsJBin,tn_ZJetsJBin,tn_SingleTop],sel_low_munu+'*(TrkIso_muon1<0.1)*'+weight_munu,[1.0,1.0,1.0,1.0,1.0])

	# print '  Data (noniso):',D_noniso
	# print ' SM BG (noniso):',B_noniso
	# print 'QCD MC (noniso):',Q_noniso

	# print '  Data (iso):',D_iso
	# print ' SM BG (iso):',B_niso
	# print 'QCD MC (iso):',Q_iso

	ScaleFactor_QCD = (D_noniso[0] - B_noniso[0])/Q_noniso[0]
	ScaleFactor_QCD_Err  = (math.sqrt((math.sqrt(D_noniso[1]**2 + B_noniso[1]**2)/(D_noniso[0] - B_noniso[0]))**2 + (Q_noniso[1]/Q_noniso[0])**2))*ScaleFactor_QCD


	FakeRate = (D_iso[0] - B_iso[0])/(D_noniso[0]-B_noniso[0])
	FakeRate_err = (math.sqrt(( math.sqrt(D_iso[1]**2 + B_iso[1]**2) / (D_iso[0] - B_iso[0]) )**2 + ( math.sqrt(D_noniso[1]**2 + B_noniso[1]**2) / (D_noniso[0] - B_noniso[0]) )**2))*FakeRate

	MCFakeRate = Q_iso[0]/Q_noniso[0]
	MCFakeRate_err = (math.sqrt((Q_iso[1]/Q_iso[0])**2  + (Q_noniso[1]/Q_noniso[0])**2))*MCFakeRate


	print "\nIn the non_isolated low-MET region, the global QCD rescaling is:", texentry4([ScaleFactor_QCD,ScaleFactor_QCD_Err])
	print "\nThe data-driven fake-rate is:", texentry4([FakeRate,FakeRate_err])
	print "\nThe MC-driven fake-rate is:", texentry4([MCFakeRate,MCFakeRate_err])

	MakeBasicPlotQCD("Pt_miss","MET [GeV] (muon non-isolated)",[50,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_mumu,NormalDirectory,'qcd_noniso_unweighted','uvjj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("Pt_miss","MET [GeV] (muon non-isolated, qcd reweighted)",[50,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_mumu,NormalDirectory,'qcd_noniso_weighted','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD)
	MakeBasicPlotQCD("Pt_miss","MET [GeV] (muon non-isolated)",[50,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_mumu,NormalDirectory,'qcd_noniso_unweightedPAS','uvjj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("Pt_miss","MET [GeV] (muon non-isolated, qcd reweighted)",[50,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_mumu,NormalDirectory,'qcd_noniso_weightedPAS','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD)


	sel__munu = sel_munu + '*(MT_uv>50)*(Pt_miss>55)'

	print '\nFor final selections, this gives estimates:\n'

	for plotmass in [300,350,400,450,500,550,600,650,700,750,800]:
		channel='uvjj'
		fsel = ((os.popen('cat '+cutlogmunu+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+sel_munu+fsel+')'
		[Nest,Nest_err] = QuickIntegral(tn_QCDMu,selection+'*'+weight_munu,ScaleFactor_QCD*FakeRate)
		Nest_toterr = math.sqrt(((math.sqrt((FakeRate_err/FakeRate)**2 + (ScaleFactor_QCD_Err/ScaleFactor_QCD)**2))*Nest)**2 + Nest_err **2 ) 
		print plotmass ,'&',texentry4([Nest,Nest_toterr]),'\\\\'

	print '\n'

def texentry4(measurement):
	return '$ '+str(round(measurement[0],4))+' \\pm '+str(round(measurement[1],4))+' $'

def texentry(measurement):
	return '$ '+str(round(measurement[0],2))+' \\pm '+str(round(measurement[1],2))+' $'

def csventry(measurement):
	return str(round(measurement[0],2))+' +- '+str(round(measurement[1],2))

def QuickTableLine(treestruc,selection,scalefacs,ftex,fcsv):
	[_stree,_btrees,_dtree] = treestruc
	print 'SELECTION',selection
	_s = QuickIntegral(_stree,selection,scalefacs[0])
	_bs = [QuickIntegral(_btrees[b],selection,scalefacs[1][b]) for b in range(len(_btrees))]
	_bt = QuickMultiIntegral(_btrees,selection,scalefacs[1])
	# dselection = selection.split('*(fact')[0]
	parseselection = selection.replace('*',' ').replace(')',' ').replace('(',' ')
	parseselection = parseselection.split()
	dselection = str(selection)
	for segment in parseselection:
		if 'factor' in segment:
			dselection = dselection.replace(segment,'1')
	print 'DSELECTION',dselection
	_d = QuickEntries (_dtree,dselection+dataHLT,scalefacs[2])

	texline = ''
	for x in _bs:
		texline += ' '+texentry(x)+' &'
	texline += texentry(_bt)+' & '
	texline += texentry(_d)+' & '
	texline += texentry(_s)+' \\\\ '
	
	csvline = ''
	for x in _bs:
		csvline += ' '+csventry(x)+' ,'
	csvline += csventry(_bt)+' , '
	csvline += csventry(_d)+' , '
	csvline += csventry(_s)+'  '

	# print selection
	# print texline 

	f = open(ftex,'a')
	f.write(texline+'\n')
	f.close()

	f = open(fcsv,'a')
	f.write(csvline+'\n')
	f.close()


def QuickTableLineTTDD(treestruc,selections,scalefacs,ftex,fcsv):
	[_stree,_demutree,_mcemutrees,_btrees,_dtree] = treestruc
	[emudataselection,emumcselection,basicselection] = selections
	[signalscale,emudatascale,emumcscales,normalscales,datascale] = scalefacs

	_s = QuickIntegral(_stree,basicselection,signalscale)

	__emudat = QuickIntegral(_demutree,emudataselection,emudatascale)
	__emuBGsubtract = QuickMultiIntegral(_mcemutrees,emumcselection,emumcscales)

	# print __emudat
	# print __emuBGsubtract

	_b_ttbar = [emu_id_eff*(__emudat[0] + __emuBGsubtract[0]), emu_id_eff*(math.sqrt(__emudat[1]**2 + __emuBGsubtract[1]**2))]

	_b_other = [QuickIntegral(_btrees[b],basicselection,normalscales[b]) for b in range(len(_btrees))]

	_bs = []
	_bs.append(_b_ttbar)
	for x in _b_other:
		_bs.append(x)


	_b_tot = 0.0
	_b_tot_err = 0.0

	for b in _bs:
		_b_tot += b[0]
		_b_tot_err += b[1]**2
	_b_tot_err = math.sqrt(_b_tot_err)

	_bt = [_b_tot, _b_tot_err]

	_d = QuickEntries (_dtree,basicselection+dataHLT,datascale)



	texline = ''
	for x in _bs:
		texline += ' '+texentry(x)+' &'
	texline += texentry(_bt)+' & '
	texline += texentry(_d)+' & '
	texline += texentry(_s)+' \\\\ '
	
	csvline = ''
	for x in _bs:
		csvline += ' '+csventry(x)+' ,'
	csvline += csventry(_bt)+' , '
	csvline += csventry(_d)+' , '
	csvline += csventry(_s)+'  '

	# print selection
	print texline 

	f = open(ftex,'a')
	f.write(texline+'\n')
	f.close()

	f = open(fcsv,'a')
	f.write(csvline+'\n')
	f.close()


def QuickTable(optimlog, selection, weight,rz,rw,rt,num):
	selection = weight+'*'+selection
	texfile = optimlog.replace('.txt','_table'+str(num)+'.tex')
	csvfile = optimlog.replace('.txt','_table'+str(num)+'.csv')

	headers = ['TTBar','Z+Jets','W+Jets','sTop','VV','Tot BG','Data','Signal']


	f = open(texfile,'w')
	header = '  '
	for h in headers:
		header += h + '&'
	header = header[:-1]
	header += '\\\\'
	f.write(header+'\n')
	f.close()

	f = open(csvfile,'w')
	header = ' '
	for h in headers:
		header += h + ','
	header = header[:-1]	
	f.write(header+'\n')
	f.close()

	nline = 0
	for line in open(optimlog,'r'):

		if nline==0:

			print '  ..processing table line for optimization:  ', line
			fsel = line.replace('\n','')
			masschan = fsel.split('=')[0]
			masschan = masschan.replace('\n','')
			masschan = masschan.replace(' ','')
			mass = masschan.split('jj')[-1]
			chan = 't_'+masschan.split('_')[-1]
			fsel = (fsel.split("="))[-1]
			fsel = '*'+fsel.replace(" ","")
			this_sel = '('+selection+')'

			exec('treefeed = ['+chan+']')
			treefeed.append([t_TTBarDBin,t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
			treefeed.append(t_SingleMuData)
			scalefacs = [1,[rt,rz,rw,1,1],1]
			QuickTableLine(treefeed,this_sel,scalefacs,texfile,csvfile)

		print '  ..processing table line for optimization:  ', line
		fsel = line.replace('\n','')
		masschan = fsel.split('=')[0]
		masschan = masschan.replace('\n','')
		masschan = masschan.replace(' ','')
		mass = masschan.split('jj')[-1]
		chan = 't_'+masschan.split('_')[-1]
		fsel = (fsel.split("="))[-1]
		fsel = fsel.replace(" ","")
		this_sel = fsel+'*'+selection

		exec('treefeed = ['+chan+']')
		treefeed.append([t_TTBarDBin,t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		treefeed.append(t_SingleMuData)
		scalefacs = [1,[rt,rz,rw,1,1],1]
		QuickTableLine(treefeed,this_sel,scalefacs,texfile,csvfile)

		nline += 1


def QuickTableTTDD(optimlog, selection, weight,rz,rw,rt,num):
	# selection = selection+'*'+weight
	texfile = optimlog.replace('.txt','_table'+str(num)+'.tex')
	csvfile = optimlog.replace('.txt','_table'+str(num)+'.csv')

	headers = ['TTBar','Z+Jets','W+Jets','sTop','VV','Tot BG','Data','Signal']


	f = open(texfile,'w')
	header = '  '
	for h in headers:
		header += h + '&'
	header = header[:-1]
	header += '\\\\'
	f.write(header+'\n')
	f.close()

	f = open(csvfile,'w')
	header = ' '
	for h in headers:
		header += h + ','
	header = header[:-1]	
	f.write(header+'\n')
	f.close()

	nline = 0
	for line in open(optimlog,'r'):

		if nline==0:

			print '  ..processing table line for optimization:  ', line
			fsel = line.replace('\n','')
			masschan = fsel.split('=')[0]
			masschan = masschan.replace('\n','')
			masschan = masschan.replace(' ','')
			mass = masschan.split('jj')[-1]
			chan = 't_'+masschan.split('_')[-1]
			fsel = (fsel.split("="))[-1]
			fsel = '*'+fsel.replace(" ","")
			this_sel = '('+selection+')'

			exec('treefeed = ['+chan+']')
			treefeed.append(te_SingleMuData)
			treefeed.append([te_ZJetsJBin,te_WJetsJBin,te_SingleTop,te_DiBoson])
			treefeed.append([t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
			treefeed.append(t_SingleMuData)
			scalefacs = [1,1,[-1.0*rz,-1.0*rw,-1.0,-1.0],[rz,rw,1,1],1]
			selections = [ this_sel +dataHLT+dataHLTEMUADJ, this_sel+'*'+NormalWeightEMuNoHLT, this_sel+'*'+NormalWeightMuMu ]
			QuickTableLineTTDD(treefeed,selections,scalefacs,texfile,csvfile)

		print '  ..processing table line for optimization:  ', line
		fsel = line.replace('\n','')
		masschan = fsel.split('=')[0]
		masschan = masschan.replace('\n','')
		masschan = masschan.replace(' ','')
		mass = masschan.split('jj')[-1]
		chan = 't_'+masschan.split('_')[-1]
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		this_sel = '('+selection+fsel+')'

		exec('treefeed = ['+chan+']')
		treefeed.append(te_SingleMuData)
		treefeed.append([te_ZJetsJBin,te_WJetsJBin,te_SingleTop,te_DiBoson])
		treefeed.append([t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		treefeed.append(t_SingleMuData)

		scalefacs = [1,1,[-1.0*rz,-1.0*rw,-1.0,-1.0],[rz,rw,1,1],1]
		selections = [ this_sel +dataHLT+dataHLTEMUADJ, this_sel+'*'+NormalWeightEMuNoHLT, this_sel+'*'+NormalWeightMuMu ]		
	
		QuickTableLineTTDD(treefeed,selections,scalefacs,texfile,csvfile)

		nline += 1

def QuickSysTableLine(treestruc,selection,scalefacs,fsys,chan,rglobals,rglobalb):
	[_stree,_dtree,_btrees] = treestruc
	_s = QuickSysIntegral(_stree,selection,scalefacs[0],rglobals)
	_bs = [QuickSysIntegral(_btrees[b],selection,scalefacs[1][b],rglobalb) for b in range(len(_btrees))]
	_d = QuickSysEntries (_dtree,selection+dataHLT,scalefacs[2])

	sysline = 'L_'+chan + ' = ['
	sysline += (_s)+' , '
	sysline += (_d)+' , '
	for x in _bs:
		sysline += ' '+(x)
		sysline += ' , '
	sysline = sysline[0:-2]+' ]'

	print selection.replace('\n','')
	print ' '

	f = open(fsys,'a')
	f.write(sysline+'\n')
	f.close()


def QuickSysTableLineTTDD(treestruc,selections,scalefacs,fsys,chan,rglobals,rglobalb):
	[_stree,_demutree,_mcemutrees,_btrees,_dtree] = treestruc
	[emudataselection,emumcselection,basicselection] = selections
	[signalscale,emudatascale,emumcscales,normalscales,datascale] = scalefacs

	print 'EMU Data:', emudataselection
	print 'EMU MC:' , emumcselection
	print 'basicselection:', basicselection
	_s = QuickSysIntegral(_stree,basicselection,signalscale,rglobals)


	__emudat = QuickIntegral(_demutree,emudataselection,1.0)
	__emudat_str = QuickSysIntegral(_demutree,emudataselection,1.0,1.0)
	__emuBGsubtract = QuickMultiIntegral(_mcemutrees,emumcselection,emumcscales)

	exec('emuinfo='+__emudat_str)
	_b_ttbar = str([emudatascale*(__emudat[0] + __emuBGsubtract[0]),emuinfo[1] ])
	
	_b_other = [QuickSysIntegral(_btrees[b],basicselection,normalscales[b],rglobalb) for b in range(len(_btrees))]

	_bs = []
	_bs.append(_b_ttbar)
	for x in _b_other:
		_bs.append(x)

	# _b_tot = 0.0
	# _b_tot_err = 0.0

	# for b in _bs:
	# 	_b_tot += b[0]
	# 	_b_tot_err += b[1]**2
	# _b_tot_err = math.sqrt(_b_tot_err)

	# _bt = [_b_tot, _b_tot_err]

	_d = QuickSysEntries (_dtree,basicselection+dataHLT,datascale)

	sysline = 'L_'+chan + ' = ['
	sysline += (_s)+' , '
	sysline += (_d)+' , '
	for x in _bs:
		sysline += ' '+(x)
		sysline += ' , '
	sysline = sysline[0:-2]+' ]'


	f = open(fsys,'a')
	f.write(sysline+'\n')
	f.close()






def ModSelection(selection,sysmethod,channel_log):
	_kinematicvariables = ['Pt_muon1','Pt_muon2','Pt_ele1','Pt_ele2','Pt_jet1','Pt_jet2','Pt_miss']
	_kinematicvariables += ['Eta_muon1','Eta_muon2','Eta_ele1','Eta_ele2','Eta_jet1','Eta_jet2','Eta_miss']
	_kinematicvariables += ['Phi_muon1','Phi_muon2','Phi_ele1','Phi_ele2','Phi_jet1','Phi_jet2','Phi_miss']
	_kinematicvariables += ['St_uujj','St_uvjj']
	_kinematicvariables += ['St_eejj','St_evjj']
	_kinematicvariables += ['M_uujj1','M_uujj2','M_uujjavg','MT_uvjj1','MT_uvjj2','M_uvjj','MT_uvjj']
	_kinematicvariables += ['M_uu','MT_uv']
	_kinematicvariables += ['DR_muon1muon2','DPhi_muon1met','DPhi_jet1met']
	# _kinematicvariables += ['M_eejj1','M_eejj2','MT_evjj1','MT_evjj2','M_evjj','MT_evjj']
	# _kinematicvariables += ['JetCount','MuonCount','ElectronCount','GenJetCount']
	_weights = ['weight_nopu','weight_central', 'weight_pu_up', 'weight_pu_down']
	_variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER']	
	selsplit = []
	selchars = ''
	alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
	for s in selection:
		if s not in alphabet:
			selsplit.append(selchars)
			selchars = s
			selsplit.append(selchars)
			selchars = ''
		else:
			selchars += s
	selsplit.append(selchars)
	outsel = ''
	for v in _variations:
		if sysmethod == v:
			for sobj in selsplit:
				for k in _kinematicvariables:
					if sobj == k:
						sobj = k+sysmethod
				outsel += sobj
	if outsel != '':
		selection=outsel



	if 'weight' in selection:

		if sysmethod == 'LUMIup':
			selection = '(1.044)*'+selection
		if sysmethod == 'LUMIdown':
			selection = '(0.956)*'+selection

		if sysmethod == 'MUONIDISO':
			if 'uujj' in channel_log: 
				selection = '(1.04)*'+selection
			if 'uvjj' in channel_log: 
				selection = '(1.02)*'+selection

		if sysmethod == 'MUONHLT':
			if 'uvjj' in channel_log: 
				selection = '(1.01)*'+selection

		if sysmethod == 'PUup':
			selection = selection.replace('weight_central','weight_pu_up')
		if sysmethod == 'PUdown':
			selection = selection.replace('weight_central','weight_pu_down')

	return selection


def SysTable(optimlog, selection_uujj,selection_uvjj,NormalDirectory, weight,sysmethod):
	selection_uujj = selection_uujj+'*'+weight
	selection_uvjj = selection_uvjj+'*'+weight
	selection_uujj = ModSelection(selection_uujj,sysmethod,optimlog)
	selection_uvjj = ModSelection(selection_uvjj,sysmethod,optimlog)

	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( selection_uujj, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)')
	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( selection_uvjj, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')

	Rz_uujj_print = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
	Rtt_uujj_print = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
	Rw_uvjj_print = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
	Rtt_uvjj_print = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))	
	print sysmethod+' & ' + Rz_uujj_print+' & '+Rtt_uujj_print+' & '+Rw_uvjj_print+' & '+Rtt_uvjj_print+' \\\\'

	if 'uujj' in optimlog:
		[rz,rw,rt] = [Rz_uujj,Rw_uvjj,Rtt_uujj]
		[_e_rz,_e_rw,_e_rt] = [Rz_uujj_err,Rw_uvjj_err,Rtt_uujj_err]

		selection = selection_uujj
		alignmentcorrs = [alignmentuncs[0],alignmentuncs[1]]

	if 'uvjj' in optimlog:
		[rz,rw,rt] = [Rz_uujj,Rw_uvjj,Rtt_uvjj]
		[_e_rz,_e_rw,_e_rt] = [Rz_uujj_err,Rw_uvjj_err,Rtt_uvjj_err]	
		selection = selection_uvjj
		alignmentcorrs = [alignmentuncs[2],alignmentuncs[3]]

	rglobals = 1.0
	rglobalb = 1.0


	if sysmethod == 'ZNORMup':     rz += _e_rz 
	if sysmethod == 'ZNORMdown':   rz += -_e_rz 
	if sysmethod == 'WNORMup': 	   rw += _e_rw
	if sysmethod == 'WNORMdown':   rw += -_e_rw 
	if sysmethod == 'TTNORMup':    rt += _e_rt
	if sysmethod == 'TTNORMdown':  rt += -_e_rt 	

	if sysmethod == 'SHAPETT' : 
		if 'uujj' in optimlog: 
			rt = (1.+.01*shapesys_uujj_ttbar )*rt
		if 'uvjj' in optimlog: 
			rt = (1.+.01*shapesys_uvjj_ttbar )*rt

	if sysmethod == 'SHAPEZ'  : rz = (1.+.01*shapesys_uujj_zjets)*rz
	if sysmethod == 'SHAPEW'  : rw = (1.+.01*shapesys_uvjj_wjets)*rw


	sysfile = optimlog.replace('.txt','_systable_'+sysmethod+'.txt')

	headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV']


	f = open(sysfile,'w')
	header = 'headers = '+str(headers)
	f.write(header+'\n')
	f.close()


	nalign = -1
	for line in open(optimlog,'r'):
		nalign += 1
		line = line.replace('\n','')
		print 'processing table line for optimization:  ', line

		if sysmethod == 'ALIGN':
			if 'uujj' in optimlog:
				rglobals = 1.0 + alignmentcorrs[0]*.01
				rglobalb = 1.0 + alignmentcorrs[1]*.01
			if 'uvjj' in optimlog:
				rglobals = 1.0 + alignmentcorrs[0]*.01
				rglobalb = 1.0 + alignmentcorrs[1][nalign] *.01


		fsel = line.replace('\n','')
		fsel = ModSelection(fsel,sysmethod,optimlog)
		masschan = fsel.split('=')[0]
		masschan = masschan.replace('\n','')
		masschan = masschan.replace(' ','')
		mass = masschan.split('jj')[-1]
		chan = 't_'+masschan.split('_')[-1]
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		this_sel = '('+selection+fsel+')'

		rstop = 1
		rdiboson = 1
		rsig = 1
		_rt = rt
		_rw = rw
		_rz = rz

		if 'PDF'  in sysmethod:
			if 'uujj' in optimlog:
				_rt *= (1.0+pdf_uujj_TTBar[nalign]*0.01)
				_rw *= (1.0+pdf_uujj_WJets[nalign]*0.01)
				_rz *= (1.0+pdf_uujj_ZJets[nalign]*0.01)
				rstop *= (1.0+pdf_uujj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uujj_VV[nalign]*0.01)
				rsig *= (1.0+pdf_uujj_Signal[nalign]*0.01)

			if 'uvjj' in optimlog:
				_rt *= (1.0+pdf_uvjj_TTBar[nalign]*0.01)
				_rw *= (1.0+pdf_uvjj_WJets[nalign]*0.01)
				_rz *= (1.0+pdf_uvjj_ZJets[nalign]*0.01)
				rstop *= (1.0+pdf_uvjj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uvjj_VV[nalign]*0.01)
				rsig *= (1.0+pdf_uvjj_Signal[nalign]*0.01)

		exec('treefeed = ['+chan+']')
		treefeed.append(t_SingleMuData)
		treefeed.append([t_TTBarDBin,t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		scalefacs = [rsig,[_rt,_rz,_rw,rstop,rdiboson],1]
		QuickSysTableLine(treefeed,this_sel,scalefacs,sysfile,chan,rglobals,rglobalb)
		# break



def SysTableTTDD(optimlog, selection_uujj,selection_uvjj,NormalDirectory, weight,sysmethod):
	selection_uujj = selection_uujj
	selection_uvjj = selection_uvjj

	selection_uujj_unmod = ModSelection(selection_uujj,"",optimlog)
	selection_uvjj_unmod = ModSelection(selection_uvjj,"",optimlog)

	selection_uujj = ModSelection(selection_uujj,sysmethod,optimlog)
	selection_uvjj = ModSelection(selection_uvjj,sysmethod,optimlog)

	weightmod = '*'+ModSelection(weight,sysmethod,optimlog)

	weightmod_uvjj = '*'+ModSelection(NormalWeightMuNu,sysmethod,optimlog)

	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( selection_uujj+weightmod, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)')
	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( selection_uvjj+weightmod_uvjj, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')

	[Rtt_uujj, Rtt_uujj_err] = [emu_id_eff, emu_id_eff_err]

	Rz_uujj_print = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
	Rtt_uujj_print = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
	Rw_uvjj_print = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
	Rtt_uvjj_print = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))	
	print sysmethod+' & ' + Rz_uujj_print+' & '+Rtt_uujj_print+' & '+Rw_uvjj_print+' & '+Rtt_uvjj_print+' \\\\'

	if 'uujj' in optimlog:
		[rz,rw,rt] = [Rz_uujj,Rw_uvjj,Rtt_uujj]
		[_e_rz,_e_rw,_e_rt] = [Rz_uujj_err,Rw_uvjj_err,Rtt_uujj_err]

		selection = selection_uujj
		selection_unmod = selection_uujj_unmod
		alignmentcorrs = [alignmentuncs[0],alignmentuncs[1]]

	if 'uvjj' in optimlog:
		[rz,rw,rt] = [Rz_uujj,Rw_uvjj,Rtt_uvjj]
		[_e_rz,_e_rw,_e_rt] = [Rz_uujj_err,Rw_uvjj_err,Rtt_uvjj_err]	
		selection = selection_uvjj
		selection_unmod = selection_uvjj_unmod
		alignmentcorrs = [alignmentuncs[2],alignmentuncs[3]]

	rglobals = 1.0
	rglobalb = 1.0


	if sysmethod == 'ZNORMup':     rz += _e_rz 
	if sysmethod == 'ZNORMdown':   rz += -_e_rz 
	if sysmethod == 'WNORMup': 	   rw += _e_rw
	if sysmethod == 'WNORMdown':   rw += -_e_rw 
	if sysmethod == 'TTNORMup':    rt += _e_rt
	if sysmethod == 'TTNORMdown':  rt += -_e_rt 	

	# if sysmethod == 'SHAPETT' : 
	# 	if 'uujj' in optimlog: 
	# 		rt = 1.077*rt
	# 	if 'uvjj' in optimlog: 
	# 		rt = 1.199*rt

	if sysmethod == 'SHAPEZ'  : rz = (1.+.01*shapesys_uujj_zjets)*rz
	if sysmethod == 'SHAPEW'  : rw = (1.+.01*shapesys_uvjj_wjets)*rw

	sysfile = optimlog.replace('.txt','_systable_'+sysmethod+'.txt')

	headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV']


	f = open(sysfile,'w')
	header = 'headers = '+str(headers)
	f.write(header+'\n')
	f.close()


	nalign = -1
	for line in open(optimlog,'r'):
		nalign += 1
		line = line.replace('\n','')
		print 'processing table line for optimization:  ', line

		if sysmethod == 'ALIGN':
			if 'uujj' in optimlog:
				rglobals = 1.0 + alignmentcorrs[0]*.01
				rglobalb = 1.0 + alignmentcorrs[1]*.01
			if 'uvjj' in optimlog:
				rglobals = 1.0 + alignmentcorrs[0]*.01
				rglobalb = 1.0 + alignmentcorrs[1][nalign] *.01


		fsel = line.replace('\n','')
		fsel_unmod = ModSelection(fsel,"",optimlog)

		fsel = ModSelection(fsel,sysmethod,optimlog)

		masschan = fsel.split('=')[0]
		masschan = masschan.replace('\n','')
		masschan = masschan.replace(' ','')
		mass = masschan.split('jj')[-1]
		chan = 't_'+masschan.split('_')[-1]
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		this_sel = '('+selection+fsel+')'

		fsel_unmod = (fsel_unmod.split("="))[-1]
		fsel_unmod = '*'+fsel_unmod.replace(" ","")
		this_sel_unmod = '('+selection_unmod+fsel_unmod+')'

		rstop = 1
		rdiboson = 1
		rsig = 1
		_rt = rt
		_rw = rw
		_rz = rz

		if 'PDF'  in sysmethod:
			if 'uujj' in optimlog:
				# _rt *= (1.0+pdf_uujj_TTBar[nalign]*0.01)
				_rw *= (1.0+pdf_uujj_WJets[nalign]*0.01)
				_rz *= (1.0+pdf_uujj_ZJets[nalign]*0.01)
				rstop *= (1.0+pdf_uujj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uujj_VV[nalign]*0.01)
				rsig *= (1.0+pdf_uujj_Signal[nalign]*0.01)

			if 'uvjj' in optimlog:
				_rt *= (1.0+pdf_uvjj_TTBar[nalign]*0.01)
				_rw *= (1.0+pdf_uvjj_WJets[nalign]*0.01)
				_rz *= (1.0+pdf_uvjj_ZJets[nalign]*0.01)
				rstop *= (1.0+pdf_uvjj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uvjj_VV[nalign]*0.01)
				rsig *= (1.0+pdf_uvjj_Signal[nalign]*0.01)


		exec('treefeed = ['+chan+']')
		treefeed.append(te_SingleMuData)
		treefeed.append([te_ZJetsJBin,te_WJetsJBin,te_SingleTop,te_DiBoson])
		treefeed.append([t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		treefeed.append(t_SingleMuData)

		scalefacs = [rsig,_rt,[-1.0*_rz,-1.0*_rw,-1.0*rstop,-1.0*rdiboson],[_rz,_rw,rstop,rdiboson],1]
		selections = [ this_sel_unmod +dataHLT+dataHLTEMUADJ, this_sel_unmod+'*'+NormalWeightEMuNoHLT, this_sel+weightmod ]		

		QuickSysTableLineTTDD(treefeed,selections,scalefacs,sysfile,chan,rglobals,rglobalb)
		# break

def FullAnalysis(optimlog,selection_uujj,selection_uvjj,NormalDirectory,weight,usedd):
	TTDD = False
	if usedd=='TTBarDataDriven':
		TTDD=True
	_Variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','WNORMup','WNORMdown','TTNORMup','TTNORMdown','SHAPETT','SHAPEZ','SHAPEW','MUONIDISO','MUONHLT','ALIGN','PDF']	
	for v in _Variations:
		print ' -'*50
		print 'Processing table for variation: ',v
		if (optimlog.replace('.txt','_systable_'+v+'.txt')) in str(os.popen('ls '+optimlog.replace('.txt','_systable_'+v+'.txt')).readlines()):
			print 'Already present ... skipping. '
			continue
		if TTDD:
			SysTableTTDD(optimlog, selection_uujj, selection_uvjj,NormalDirectory, weight,v)
		else:
			SysTable(optimlog, selection_uujj, selection_uvjj,NormalDirectory, weight,v)




def GetScaleFactors(n1,n2,a1,a2,b1,b2,o1,o2):
	Ra = 1.0
	Rb = 1.0
	for x in range(10):
		Ra = (n1 - Rb*b1 - o1)/(a1)
		Rb = (n2 - Ra*a2 - o2)/(b2) 
	return [Ra, Rb]

def GetSimpleScaleFactors(n1,n2,a1,a2,b1,b2,o1,o2):
	Ra = 1.0
	Rb = 1.0
	for x in range(10):
		# Ra = (n1 - 1.0*b1 - o1)/(a1)
		Rb = (n2 - 1.0*a2 - o2)/(b2) 
	return [Ra, Rb]

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

def binmeanstdv(X,Y,Yrange):
	x = []
	for j in range(len(X)):
		if Y[j] > Yrange[0] and Y[j] < Yrange[1]:
			x.append(X[j])

	n, mean, std = len(x), 0, 0 

	for a in x: 
		mean = mean + a 
	if n >= 1:
		mean = mean / float(n) 
	else:
		mean = 0
	for a in x: 
		std = std + (a - mean)**2 
	if n>=1:	
		std = math.sqrt(std / float(n)) 
	elif n == 1:
		std = mean
	else:
		std = 99999999.
	print Yrange,len(x),mean,std
	return [mean, std]

def GetProfile(X,Y,binning):
	X= [1.0*xx for xx in X]
	Y= [1.0*yy for yy in Y]
	binset = ConvertBinning(binning)
	bins = []
	for b in range(len(binset)-1):
		bmin = binset[b]
		bmax = binset[b+1]
		bins.append([bmin,bmax])
	Ymeans = []
	Yerrs = []
	Xmeans = []
	Xerrs = []
	for B in bins:
		stats = binmeanstdv(X,Y,B)
		Ymeans.append(stats[0])
		Yerrs.append(stats[1])
		Xmeans.append((B[1] + B[0])/2.0)
		Xerrs.append(abs(B[1] - B[0])/2.0)
	return [Xmeans,Xerrs,Ymeans,Yerrs]



def RR(List):
	return random.gauss(List[0],List[1])

def PrintRuns():
	tmpfile = TFile("tmp.root","RECREATE")
	t_SingleMuData2 = t_SingleMuData.CopyTree(preselectionmunu)
	allruns = []
	NN = t_SingleMuData2.GetEntries()
	for n in range(NN):
		if n%1000 ==0:
			print n,'of',NN
		t_SingleMuData2.GetEntry(n)
		ev = t_SingleMuData2.run_number
		if ev not in allruns:
			allruns.append(ev)

	allruns.sort()
	for a in allruns:
		print a

def GetMuMuScaleFactors( selection, FileDirectory, controlregion_1, controlregion_2):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_SingleMuData,selection + '*' + controlregion_1,1.0)
	# print QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	# sys.exit()
	selection_data = selection.split('*(fact')[0]
	N1 = QuickEntries(t_SingleMuData,selection_data + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_SingleMuData,selection_data + '*' + controlregion_2+dataHLT,1.0)

	Z1 = QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBarDBin,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(t_WJetsJBin,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)

	Z2 = QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBarDBin,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(t_WJetsJBin,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)



	Other1 = [ s1[0]+w1[0]+v1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+w2[0]+v2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] ) ]
	zvals = []
	tvals = []

	for x in range(10000):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(Z1),RR(Z2),RR(T1),RR(T2),Other1[0],Other2[0]))
		zvals.append(variation[0])
		tvals.append(variation[1])

	zout =  GetStats(zvals)
	tout = GetStats(tvals)

	# ttbar force unity
	tout = [1.0,0.067,'1.000 +- 0.067']

	print 'MuMu: RZ  = ', zout[-1]
	print 'MuMu: Rtt = ', tout[-1]
	return [ [ zout[0], zout[1] ] , [ tout[0],tout[1] ] ]

def GetMuMuScaleFactorsMod( selection, FileDirectory, controlregion_1, controlregion_2,samp):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_SingleMuData,selection + '*' + controlregion_1,1.0)
	# print QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	# sys.exit()

	if 'ScaleUp' in samp:
		t_Z = t_ZJetsScaleUp
		t_T = t_TTJetsScaleDown

	elif 'ScaleDown' in samp:
		t_Z = t_ZJetsScaleDown
		t_T = t_TTJetsScaleDown

	elif 'MatchUp' in samp:
		t_Z = t_ZJetsMatchUp
		t_T = t_TTJetsMatchDown

	elif 'MatchDown' in samp:
		t_Z = t_ZJetsMatchDown
		t_T = t_TTJetsMatchDown	

	else:
		t_Z = t_ZJetsJBin
		t_T = t_TTBarDBin		

	N1 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

	Z1 = QuickIntegral(t_Z,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBarDBin,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(t_WJetsJBin,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)

	Z2 = QuickIntegral(t_Z,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBarDBin,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(t_WJetsJBin,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)



	Other1 = [ s1[0]+w1[0]+v1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+w2[0]+v2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] ) ]
	zvals = []
	tvals = []

	for x in range(10000):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(Z1),RR(Z2),RR(T1),RR(T2),Other1[0],Other2[0]))
		zvals.append(variation[0])
		tvals.append(variation[1])

	zout =  GetStats(zvals)
	tout = GetStats(tvals)

	# ttbar force unity
	tout = [1.0,0.067,'1.000 +- 0.067']

	print 'MuMu: RZ  = ', zout[-1]
	print 'MuMu: Rtt = ', tout[-1]
	return [ [ zout[0], zout[1] ] , [ tout[0],tout[1] ] ]



def GetEMuScaleFactors( selection, FileDirectory):

	print 'Checking TTBar E-Mu sample against E_Mu MC with selection:'
	print selection 
	N1 = QuickEntries(te_SingleMuData,selection  + dataHLT,1.0)

	Z1 = QuickIntegral(te_ZJetsJBin,selection ,1.0)
	T1 = QuickIntegral(te_TTBarDBin,selection ,1.0)
	s1 = QuickIntegral(te_SingleTop,selection ,1.0)
	w1 = QuickIntegral(te_WJetsJBin,selection ,1.0)
	v1 = QuickIntegral(te_DiBoson,selection ,1.0)


	print 'This is the information for the NOTE table 6:'
	print ' Data:',N1[0]
	print '   TT:',T1[0]
	print '    Z:',Z1[0]
	print ' Stop:',s1 [0]
	print '    W:',w1[0]
	print '   VV:',v1[0]

	SF=[1.0,0.0]

	SF[0] = (N1[0] - Z1[0] - s1[0] -v1[0] - w1[0])/T1[0]

	relerror_num  = math.sqrt(N1[1]**2. + Z1[1]**2. + s1[1]**2. + v1[1]**2. + w1[1]**2.)/(N1[0] - Z1[0] - s1[0] -v1[0] - w1[0])
	relerror_denom = T1[1]/T1[0]
	SF[1] = SF[0]*math.sqrt(relerror_num**2.0 + relerror_denom**2.)

	print 'MuMu: Rtt = ', SF


	print 'Now calculating R_mumu,emu, the ratio of mumu to e,mu events in ttbar MC. '
	print 'Should be near 0.5'
	T2 = QuickIntegral(t_TTBarDBin,selection.replace(singlemuHLTEMU,singlemuHLT) ,1.0)

	Ruueu = T2[0]/T1[0]
	dRuueu =  Ruueu*(math.sqrt((T1[1]/T1[0])**2.0 + (T2[1]/T2[0])**2.0))

	print 'R_uu,eu = ',Ruueu,' +- ',dRuueu

	return SF

def GetMuNuScaleFactorsMod( selection, FileDirectory, controlregion_1, controlregion_2,samp):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")

	if 'ScaleUp' in samp:
		t_W = t_WJetsScaleUp
		t_T = t_TTJetsScaleDown

	elif 'ScaleDown' in samp:
		t_W = t_WJetsScaleDown
		t_T = t_TTJetsScaleDown

	elif 'MatchUp' in samp:
		t_W = t_WJetsMatchUp
		t_T = t_TTJetsMatchDown

	elif 'MatchDown' in samp:
		t_W = t_WJetsMatchDown
		t_T = t_TTJetsMatchDown	

	else:
		t_W = t_WJetsJBin
		t_T = t_TTBarDBin		

	N1 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

	W1 = QuickIntegral(t_W,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_T,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	z1 = QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)

	W2 = QuickIntegral(t_W,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_T,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	z2 = QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)

	Other1 = [ s1[0]+z1[0]+v1[0], math.sqrt( s1[1]*s1[1] + z1[1]*z1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+z2[0]+v2[0], math.sqrt( s2[1]*s2[1] + z2[1]*z2[1] + v2[1]*v2[1] ) ]

	# print N1,N2
	# print T1,T2
	# print W1,W2
	# print Other1,Other2

	wvals = []
	tvals = []



	for x in range(10000):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(W1),RR(W2),RR(T1),RR(T2),Other1[0],Other2[0]))
		wvals.append(variation[0])
		tvals.append(variation[1])

	wout =  GetStats(wvals)
	tout = GetStats(tvals)

	print 'MuNu: RW  = ', wout[-1]
	print 'MuNu: Rtt = ', tout[-1]
	return [ [ wout[0], wout[1] ] , [ tout[0],tout[1] ] ]


def GetMuNuScaleFactors( selection, FileDirectory, controlregion_1, controlregion_2):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	selection_data = selection.split('*(fact')[0]

	N1 = QuickEntries(t_SingleMuData,selection_data + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_SingleMuData,selection_data + '*' + controlregion_2+dataHLT,1.0)

	W1 = QuickIntegral(t_WJetsJBin,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBarDBin,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	z1 = QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)

	W2 = QuickIntegral(t_WJetsJBin,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBarDBin,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	z2 = QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)

	Other1 = [ s1[0]+z1[0]+v1[0], math.sqrt( s1[1]*s1[1] + z1[1]*z1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+z2[0]+v2[0], math.sqrt( s2[1]*s2[1] + z2[1]*z2[1] + v2[1]*v2[1] ) ]
	wvals = []
	tvals = []

	for x in range(10000):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(W1),RR(W2),RR(T1),RR(T2),Other1[0],Other2[0]))
		wvals.append(variation[0])
		tvals.append(variation[1])

	print 'Here $(N_1,N_2) = (  ',
	print round(N1[0],1),',',round(N2[0],1),
	print ')$, $(N_{1,\\ttbar},N_{2,\\ttbar}) = ( ',
	print round(T1[0],1),'\\pm',round(T1[1],1),',',round(T2[0],1),'\\pm',round(T2[1],1),
	print ')$,  $(N_{1,W},N_{2,W}) = ( ',
	print round(W1[0],1),'\\pm',round(W1[1],1),',',round(W2[0],1),'\\pm',round(W2[1],1),
	print '$, and $(N_{1,0},N_{2,0}) = ( ',
	print round(Other1[0],1),'\\pm',round(Other1[1],1),',',round(Other2[0],1),'\\pm',round(Other2[1],1),
	print ')$.' ,


	wout =  GetStats(wvals)
	tout = GetStats(tvals)

	print 'MuNu: RW  = ', wout[-1]
	print 'MuNu: Rtt = ', tout[-1]
	return [ [ wout[0], wout[1] ] , [ tout[0],tout[1] ] ]






def MakeBasicPlot(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,cutlog,version_name,plotmass):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	# Create Canvas
	yaxismin = .13333
	perc = 0.0
	if channel == 'uujj':
		syslist = totunc_uujj	
	if channel == 'uvjj':
		syslist = totunc_uvjj

	if channel == 'susy':
		plotmass = 500
		print "SUSY TESTS: Using only mass of ",plotmass

	if 'PAS' not in tagname:
		c1 = TCanvas("c1","",800,800)
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.4, 1.0, 1.0 )#divide canvas into pads
		pad2 = TPad( 'pad2', 'pad2', 0.0, 0.26, 1.0, 0.4 )
		pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.26 )
		pad1.Draw()
		pad2.Draw()
		pad3.Draw()
		pad1.SetBottomMargin(0.0)		
		pad2.SetTopMargin(0.0)
		pad3.SetTopMargin(0.0)
		pad2.SetBottomMargin(0.0)
		pad3.SetBottomMargin(0.43)
	else:
		# if 'final' not in tagname:
		c1 = TCanvas("c1","",800,550)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		perc = 5.0
		for m in range(len(pdf_MASS)):
			if str(pdf_MASS[m]) in str(plotmass):
				perc = syslist[m]


		# else:
		# 	c1 = TCanvas("c1","",800,650)					
		# 	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.35, 1.0, 1.0 )#divide canvas into pads
		# 	pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.35 )
		# 	pad1.Draw()
		# 	pad3.Draw()
		# 	pad1.SetBottomMargin(0.0)		
		# 	pad3.SetTopMargin(0.0)
		# 	pad3.SetBottomMargin(0.43)	
		# 	perc = 30.0

	print 'Defining systematic band with percent uncertainty:',perc,'%'

	gStyle.SetOptStat(0)


	pad1.cd()
	# pad1.SetGrid()
	# These are the style parameters for certain plots - [FillStyle,MarkerStyle,MarkerSize,LineWidth,Color]
	MCRecoStyle=[0,20,.00001,1,4]
	DataRecoStyle=[0,20,.7,1,1]
	# X and Y axis labels for plot
	Label=[xlabel,"Events/Bin"]

	WStackStyle=[3007,20,.00001,2,6]
	TTStackStyle=[3005,20,.00001,2,4]
	ZStackStyle=[3004,20,.00001,2,2]
	DiBosonStackStyle=[3006,20,.00001,2,3]
	StopStackStyle=[3008,20,.00001,2,7]
	QCDStackStyle=[3013,20,.00001,2,15]

	SignalStyle=[0,22,0.7,3,28]
	SignalStyle2=[0,22,0.7,3,38]

	bgbandstyle=[3002,20,.00001,0,14]


	print 'Getting Final sel '
	if 'final' in tagname:
		print 'cat '+cutlog+' | grep '+channel+str(plotmass)
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		print 'found'
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+selection+fsel+')'
		print 'parsed'
		# print selection

	##############################################################################
	#######      Top Left Plot - Normal Stacked Distributions              #######
	##############################################################################
	c1.cd(1)
	# print 'Projecting trees...  ',

	tt_sel_weight = selection+'*('+str(ttscale)+')*'+weight

	print 'Choosing sample...',
	if 'ScaleUp' in tagname:
		print 'ScaleUp'
		t_W = t_WJetsScaleUp
		t_T = t_TTJetsScaleDown
		t_Z = t_ZJetsScaleUp

	elif 'ScaleDown' in tagname:
		print 'ScaleDown'
		t_W = t_WJetsScaleDown
		t_T = t_TTJetsScaleDown
		t_Z = t_ZJetsScaleDown

	elif 'MatchUp' in tagname:
		print 'MatchUp'
		t_W = t_WJetsMatchUp
		t_T = t_TTJetsMatchUp
		t_Z = t_ZJetsMatchUp

	elif 'MatchDown' in tagname:
		print "MatchDown"
		t_W = t_WJetsMatchDown
		t_T = t_TTJetsMatchDown	
		t_Z = t_ZJetsMatchDown

	else:
		print "Regular"
		t_W = t_WJetsJBin
		t_Z = t_ZJetsJBin
		print 'USING STANDARD W'
		if 'TTBarDataDriven' not in tagname:
			t_T = t_TTBarDBin
			print 'Using Decay-binned ttbar MC.'
		else:
			t_T = te_SingleMuData
			tt_sel_weight = selection +dataHLT+dataHLTEMUADJ
			print 'Using emu data for ttbar est.'

		# t_T = t_TTPowheg

	print 'Doing Projections'
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',t_W,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',t_SingleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',t_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',t_Z,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	print 'Doing ttbar:'
	print selection+'*('+str(ttscale)+')*'+weight
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',t_T,recovariable,presentationbinning,tt_sel_weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',t_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)

	if 'TTBarDataDriven' in tagname:

		hs_emu_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',te_WJetsJBin,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+NormalWeightEMuNoHLT,WStackStyle,Label)
		hs_emu_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,DiBosonStackStyle,Label)
		hs_emu_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',te_ZJetsJBin,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+NormalWeightEMuNoHLT,ZStackStyle,Label)
		hs_emu_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',te_SingleTop,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,StopStackStyle,Label)
		hs_emu_rec_WJets.Scale(-1.0)
		hs_emu_rec_DiBoson.Scale(-1.0)
		hs_emu_rec_ZJets.Scale(-1.0)
		hs_emu_rec_SingleTop.Scale(-1.0)
		hs_rec_TTBar.Add(hs_emu_rec_WJets)
		hs_rec_TTBar.Add(hs_emu_rec_DiBoson)
		hs_rec_TTBar.Add(hs_emu_rec_ZJets)
		hs_rec_TTBar.Add(hs_emu_rec_SingleTop)
		hs_rec_TTBar.Scale(emu_id_eff)



	sig1name = ''
	sig2name = ''

	if channel == 'uujj':
		sig1name = 'LQ, M = 500 GeV'
		sig2name = 'LQ, M = 900 GeV'
		if 'final' not in tagname:
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_LQuujj500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_LQuujj900,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
		if 'final' in tagname:
			exec ("_stree = t_LQ"+channel+str(plotmass))
			hs_rec_Signal=CreateHisto('hs_rec_Signal','LQ, M = '+str(plotmass)+' GeV',_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)

		hs_rec_DiBoson.SetTitle("Other Backgrounds")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets]

	if channel == 'susy':
		sig1name = 'LQ, M = 500 GeV'
		sig2name = 'RPV Susy, M = 500 GeV'
		if 'final' not in tagname:
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_LQuujj500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_Susy500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
		if 'final' in tagname:
			exec ("_stree = t_LQ"+channel+str(plotmass))
			hs_rec_Signal=CreateHisto('hs_rec_Signal','LQ, M = '+str(plotmass)+' GeV',_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)

		hs_rec_DiBoson.SetTitle("Other Backgrounds")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets]

	if channel == 'uvjj':
		if 'final' not in tagname:	
			sig1name = 'LQ, M = 400 GeV'
			sig2name = 'LQ, M = 750 GeV'
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_LQuvjj400,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_LQuvjj750,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
		if 'final' in tagname:
			exec ("_stree = t_LQ"+channel+str(plotmass))
			hs_rec_Signal=CreateHisto('hs_rec_Signal','LQ, M = '+str(plotmass)+' GeV',_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
	
		hs_rec_DiBoson.SetTitle("Other Backgrounds")
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)		
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_WJets]
	
	bgcont = []
	dcont = []
	bgconterr = []

	hs_bgband=CreateHisto('hs_bgband','bgband',t_SingleTop,recovariable,presentationbinning,'(0)',bgbandstyle,Label)
	for x in SM:
		hs_bgband.Add(x)


	# print presentationbinning
	for nn in range(SM[0].GetNbinsX()):
		n = nn + 1
		lhs = SM[0].GetBinCenter(n) - 0.5*SM[0].GetBinWidth(n)
		rhs = SM[0].GetBinCenter(n) + 0.5*SM[0].GetBinWidth(n)
		cont = 0.0
		conterr = 0.0
		for ss in SM:
			cont += ss.GetBinContent(n)
			conterr += ss.GetBinError(n)*ss.GetBinError(n)
		conterr = math.sqrt(conterr)
		# print lhs, rhs, cont
		bgcont.append(cont)
		bgconterr.append(conterr)
		dcont.append(hs_rec_Data.GetBinContent(n))


	# sysbandX = []
	# sysbandY = []
	# sysbandYaddon = []
	# sysbandXaddon = []

	# sysratbandX = []
	# sysratbandY = []
	# sysratbandYaddon = []
	# sysratbandXaddon = []


	# for c in range(len(bgcont)):
	# 	_err = math.sqrt(((perc*0.01)*bgcont[c])**2 + bgconterr[c]**2)

		# sysbandX.append(presentationbinning[c])
		# sysbandX.append(presentationbinning[c+1])
		# sysbandXaddon.append(presentationbinning[c])
		# sysbandXaddon.append(presentationbinning[c+1])

		# sysbandY.append(bgcont[c]+_err)
		# sysbandY.append(bgcont[c]+_err)
		# sysbandYaddon.append(bgcont[c]-_err)
		# sysbandYaddon.append(bgcont[c]-_err)

		# sysratbandX.append(presentationbinning[c])
		# sysratbandX.append(presentationbinning[c+1])
		# sysratbandXaddon.append(presentationbinning[c])
		# sysratbandXaddon.append(presentationbinning[c+1])

		# rat = 1.0
		# invrat = 1.0
		# if bgcont[c] > 0.0:
		# 	rat = (bgcont[c] + _err)/bgcont[c]
		# 	invrat = (bgcont[c] - _err)/bgcont[c]
		# sysratbandY.append(rat)
		# sysratbandY.append(rat)
		# sysratbandYaddon.append(invrat)
		# sysratbandYaddon.append(invrat)

	for c in range(hs_bgband.GetNbinsX()+1):
		_err = math.sqrt( (hs_bgband.GetBinError(c))**2 + (perc*0.01*hs_bgband.GetBinContent(c))**2 )
		hs_bgband.SetBinError(c,_err)
		if hs_bgband.GetBinContent(c) < 0.0001:
			hs_bgband.SetBinContent(c,0.0)
			hs_bgband.SetBinError(c,0.0)

	# print sysbandY

	# for y in range(len(sysbandY)):
	# 	if sysbandY[y] < yaxismin:
	# 		sysbandY[y] = yaxismin

	# print sysbandY


	# sysbandYaddon.reverse()
	# sysbandYaddon.reverse()
	# sysratbandYaddon.reverse()
	# sysratbandYaddon.reverse()

	# for x in sysbandYaddon:
	# 	sysbandY.append(x)

	# for x in sysbandXaddon:
	# 	sysbandX.append(x)

	# for x in sysratbandYaddon:
	# 	sysratbandY.append(x)

	# for x in sysratbandXaddon:
	# 	sysratbandX.append(x)


	# sysbandX = array("d",sysbandX)
	# sysbandY = array("d",sysbandY)
	# sysratbandX = array("d",sysratbandX)
	# sysratbandY = array("d",sysratbandY)


	# sysTop =  TPolyLine(len(sysbandY),sysbandX,sysbandY,"")
	# sysTop.SetLineColor(14)
	# sysTop.SetFillColor(14)
	# sysTop.SetFillStyle(3002)

	# sysBot =  TPolyLine(len(sysratbandY),sysratbandX,sysratbandY,"")
	# sysBot.SetLineColor(14)
	# sysBot.SetFillColor(14)
	# sysBot.SetFillStyle(3002)


	# mcdatascalepres = (1.0*(hs_rec_Data.GetEntries()))/(sum(k.Integral() for k in SM))

	MCStack = THStack ("MCStack","")
	SMIntegral = sum(k.Integral() for k in SM)
	# print SMIntegral
	# print hs_rec_Data.Integral(), hs_rec_Data.GetEntries()
	# MCStack.SetMaximum(SMIntegral*100)
	
	print 'Stacking...  ',	
	for x in SM:
		# x.Scale(mcdatascalepres)
		MCStack.Add(x)
		x.SetMaximum(10*hs_rec_Data.GetMaximum())


	MCStack.Draw("HIST")
	c1.cd(1).SetLogy()

 	# sysTop->Draw("L");


	MCStack=BeautifyStack(MCStack,Label)
	hs_rec_Signal.Draw("HISTSAME")
	if 'final' not in tagname:
		hs_rec_Signal2.Draw("HISTSAME")
 	if 'PAS' in tagname and 'final' in tagname:
		# sysTop.Draw("F")
		hs_bgband.Draw("E2SAME")
	hs_rec_Data.Draw("EPSAME")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	leg = TLegend(0.53,0.52,0.89,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(.05)
	leg.AddEntry(hs_rec_Data,"Data");
	if channel=='uujj':
		leg.AddEntry(hs_rec_ZJets,'Z/#gamma^{*} + jets')
	if channel=='uvjj':
		leg.AddEntry(hs_rec_WJets,'W + jets')
	leg.AddEntry(hs_rec_TTBar,'t #bar{t} + jets' + (' (e #mu est)')*('TTBarDataDrivena' in tagname))

	leg.AddEntry(hs_rec_DiBoson,'Other Background')
	if 'final' not in tagname:
		leg.AddEntry(hs_rec_Signal,sig1name)
		leg.AddEntry(hs_rec_Signal2,sig2name)
	else:
		if 'PAS' in tagname:
			leg.AddEntry(hs_bgband,'Unc. (stat + syst)')
		leg.AddEntry(hs_rec_Signal,'LQ, M = '+str(plotmass)+' GeV')
	leg.Draw()

	sqrts = "#sqrt{s} = 8 TeV";
	l1=TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.06)
 
	l1.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.6 fb^{-1}")
	# l1.DrawLatex(0.13,0.76,sqrts)

	# l2=TLatex()
	# l2.SetTextAlign(12)
	# l2.SetTextFont(42)
	# l2.SetNDC()
	# l2.SetTextSize(0.06)
	# # l2.SetTextAngle(45);	
	# l2.DrawLatex(0.15,0.83,"PRELIMINARY")

	gPad.RedrawAxis()

	MCStack.SetMinimum(yaxismin)
	MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())
	if 'control' in tagname:
		MCStack.SetMaximum(100000*hs_rec_Data.GetMaximum())
		
	resstring = ''
	if 'PAS' not in tagname:

		pad2.cd()
		# pad2.SetLogy()
		pad2.SetGrid()

		RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)

		RatHistDen.Sumw2()
		RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
		RatHistNum.Sumw2()
		for hmc in SM:
			RatHistDen.Add(hmc)

		RatHistNum.Add(hs_rec_Data)
		RatHistNum.Divide(RatHistDen)
		# for x in RatHistNum.GetNbinsX():
		# 	print RatHistNum.GetBinCenter(x), RatHistNum.GetBinContent(x)

		RatHistNum.SetMaximum(1.499)
		RatHistNum.SetMinimum(0.501)


		RatHistNum.GetYaxis().SetTitleFont(42);
		RatHistNum.GetXaxis().SetTitle('');
		RatHistNum.GetYaxis().SetTitle('Data/MC');
		RatHistNum.GetXaxis().SetTitle(xlabel)

		RatHistNum.GetXaxis().SetTitleFont(42)
		RatHistNum.GetYaxis().SetTitleFont(42)
		RatHistNum.GetXaxis().SetLabelFont(42)
		RatHistNum.GetYaxis().SetLabelFont(42)
		RatHistNum.GetXaxis().SetLabelOffset(0.007)
		RatHistNum.GetYaxis().SetLabelOffset(0.007)
		RatHistNum.GetXaxis().SetLabelSize(0.15)
		RatHistNum.GetYaxis().SetLabelSize(0.15)

		RatHistNum.GetXaxis().SetTitleOffset(0.92)
		RatHistNum.GetYaxis().SetTitleOffset(0.28)
		RatHistNum.GetXaxis().SetTitleSize(0.18)
		RatHistNum.GetYaxis().SetTitleSize(0.18)
		RatHistNum.GetXaxis().CenterTitle(1)
		RatHistNum.GetYaxis().CenterTitle(1)


		RatHistNum.Draw()

		unity=TLine(RatHistNum.GetXaxis().GetXmin(), 1.0 , RatHistNum.GetXaxis().GetXmax(),1.0)
		unity.Draw("SAME")	



		pad3.cd()
		# pad2.SetLogy()
		pad3.SetGrid()

		chiplot =CreateHisto('chiplot','chiplot',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
		chiplot.Sumw2()

		resstring = '( 0.0 '

		for n in range(chiplot.GetNbinsX()+1):
			lhs = chiplot.GetBinCenter(n) - 0.5*chiplot.GetBinWidth(n)
			rhs = chiplot.GetBinCenter(n) + 0.5*chiplot.GetBinWidth(n)
			lhs = str(round(lhs,3))
			rhs = str(round(rhs,3))

			bg = 0
			bgerr = 0
			dat = hs_rec_Data.GetBinContent(n)
			daterr = math.sqrt(1.0*dat)
			for hmc in SM:
				bg += hmc.GetBinContent(n)
				bgerr += hmc.GetBinError(n)*hmc.GetBinError(n)
			bgerr = math.sqrt(bgerr)
			total_err = math.sqrt(bgerr*bgerr+daterr*daterr)
			
			resfac = '1.0'

			if total_err>0: 
				chi = (dat - bg)/total_err
				chiplot.SetBinContent(n,chi)
				chiplot.SetBinError(n,0.0)
			if bg > 0 and dat > 0:
				resfac = str(round(dat/bg,3))
			if n != 0:
				resstring += ' + '+resfac+'*('+recovariable +'>'+lhs+')'+'*('+recovariable +'<='+rhs+')'

		resstring += ')'
		if recovariable =='Phi_miss':
			print resstring

		chiplot.SetMaximum(5.99)
		chiplot.SetMinimum(-5.99)


		chiplot.GetYaxis().SetTitleFont(42);
		chiplot.GetYaxis().SetTitle('#chi (Data,MC)');
		chiplot.GetXaxis().SetTitle(xlabel)

		chiplot.GetXaxis().SetTitleFont(42)
		chiplot.GetYaxis().SetTitleFont(42)
		chiplot.GetXaxis().SetLabelFont(42)
		chiplot.GetYaxis().SetLabelFont(42)
		chiplot.GetXaxis().SetLabelOffset(0.007)
		chiplot.GetYaxis().SetLabelOffset(0.007)
		chiplot.GetXaxis().SetLabelSize(0.12)
		chiplot.GetYaxis().SetLabelSize(0.1)

		chiplot.GetXaxis().SetTitleOffset(0.96)
		chiplot.GetYaxis().SetTitleOffset(0.48)
		chiplot.GetXaxis().SetTitleSize(0.15)
		chiplot.GetYaxis().SetTitleSize(0.1)
		chiplot.GetXaxis().CenterTitle(1)
		chiplot.GetYaxis().CenterTitle(1)


		chiplot.Draw('EP')
		zero=TLine(RatHistNum.GetXaxis().GetXmin(), 0.0 , RatHistNum.GetXaxis().GetXmax(),0.0)
		plus2=TLine(RatHistNum.GetXaxis().GetXmin(), 2.0 , RatHistNum.GetXaxis().GetXmax(),2.0)
		minus2=TLine(RatHistNum.GetXaxis().GetXmin(), -2.0 , RatHistNum.GetXaxis().GetXmax(),-2.0)
		plus2.SetLineColor(2)
		minus2.SetLineColor(2)

		plus2.Draw("SAME")
		minus2.Draw("SAME")
		zero.Draw("SAME")	



	if 'PAS' in tagname and 'final' in tagname and False:

		pad3.cd()
		pad3.SetLogy()
		pad3.SetGrid()

		RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)

		RatHistDen.Sumw2()
		RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
		RatHistNum.Sumw2()
		for hmc in SM:
			RatHistDen.Add(hmc)

		RatHistNum.Add(hs_rec_Data)
		RatHistNum.Divide(RatHistDen)
		ratmax = 1.999
		for x in (range(RatHistNum.GetNbinsX())):
			_top = RatHistNum.GetBinContent(x+1) + RatHistNum.GetBinError(x+1)
			if _top > ratmax:
				ratmax = _top
				ratmax = 1.05*ratmax

		RatHistNum.SetMaximum(ratmax)
		RatHistNum.SetMinimum(0.1)


		RatHistNum.GetYaxis().SetTitleFont(42);
		RatHistNum.GetXaxis().SetTitle('');
		RatHistNum.GetYaxis().SetTitle('Data/MC');
		RatHistNum.GetXaxis().SetTitle(xlabel)

		RatHistNum.GetXaxis().SetTitleFont(42)
		RatHistNum.GetYaxis().SetTitleFont(42)
		RatHistNum.GetXaxis().SetLabelFont(42)
		RatHistNum.GetYaxis().SetLabelFont(42)
		RatHistNum.GetXaxis().SetLabelOffset(0.007)
		RatHistNum.GetYaxis().SetLabelOffset(0.007)
		RatHistNum.GetXaxis().SetLabelSize(0.08)
		RatHistNum.GetYaxis().SetLabelSize(0.08)

		RatHistNum.GetXaxis().SetTitleOffset(0.92)
		RatHistNum.GetYaxis().SetTitleOffset(0.52)
		RatHistNum.GetXaxis().SetTitleSize(0.12)
		RatHistNum.GetYaxis().SetTitleSize(0.10)
		RatHistNum.GetXaxis().CenterTitle(1)
		RatHistNum.GetYaxis().CenterTitle(1)

		RatHistNum.Draw("")
		# sysBot.Draw("F")		
		RatHistNum.Draw("SAME")

		unity=TLine(RatHistNum.GetXaxis().GetXmin(), 1.0 , RatHistNum.GetXaxis().GetXmax(),1.0)
		unity.Draw("SAME")	


	recovariable = recovariable.replace('/','_DIV_')
	print 'Saving...  ',
	if 'final' not in tagname:
		c1.Print('Results_'+version_name+'/Basic_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
		c1.Print('Results_'+version_name+'/Basic_'+channel+'_'+recovariable+'_'+tagname+'.png')
	else:
		c1.Print('Results_'+version_name+'/Basic_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf')
		c1.Print('Results_'+version_name+'/Basic_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.png')		
	print 'Done.'

	return resstring



def MakeBasicPlotQCD(recovariable,xlabel,presentationbinning,selection,qcdselection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,version_name,qcdrescale):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	# Create Canvas
	# c1 = TCanvas("c1","",800,800)
	# gStyle.SetOptStat(0)

	# pad1 = TPad( 'pad1', 'pad1', 0.0, 0.47, 1.0, 1.0 )#divide canvas into pads
	# pad2 = TPad( 'pad2', 'pad2', 0.0, 0.25, 1.0, 0.44 )
	# pad3 = TPad( 'pad3', 'pad3', 0.0, 0.03, 1.0, 0.22 )
	# if tagname == 'uujj':
	# 	pad1.SetLogx()
	# 	pad2.SetLogx()
	# 	pad3.SetLogx()

	# pad1.Draw()
	# pad2.Draw()
	# pad3.Draw()

	if 'PAS' not in tagname:
		c1 = TCanvas("c1","",800,800)
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.4, 1.0, 1.0 )#divide canvas into pads
		pad2 = TPad( 'pad2', 'pad2', 0.0, 0.26, 1.0, 0.4 )
		pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.26 )
		pad1.Draw()
		pad2.Draw()
		pad3.Draw()
		pad1.SetBottomMargin(0.0)		
		pad2.SetTopMargin(0.0)
		pad3.SetTopMargin(0.0)
		pad2.SetBottomMargin(0.0)
		pad3.SetBottomMargin(0.43)
	else:
		# if 'final' not in tagname:
		c1 = TCanvas("c1","",800,550)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		perc = 5.0


	pad1.cd()
	# pad1.SetGrid()
	# These are the style parameters for certain plots - [FillStyle,MarkerStyle,MarkerSize,LineWidth,Color]
	MCRecoStyle=[0,20,.00001,1,4]
	DataRecoStyle=[0,20,.7,1,1]
	# X and Y axis labels for plot
	Label=[xlabel,"Events/Bin"]

	WStackStyle=[3007,20,.00001,2,6]
	TTStackStyle=[3005,20,.00001,2,4]
	ZStackStyle=[3004,20,.00001,2,2]
	DiBosonStackStyle=[3006,20,.00001,2,3]
	StopStackStyle=[3008,20,.00001,2,7]
	QCDStackStyle=[3013,20,.00001,2,15]

	SignalStyle=[0,22,0.7,3,28]
	SignalStyle2=[0,22,0.7,3,38]

	print 'Getting Final sel '
	if tagname == 'final':
		print 'cat '+cutlog+' | grep '+channel+str(plotmass)
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		print 'found'
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+selection+fsel+')'
		print 'parsed'
		# print selection

	##############################################################################
	#######      Top Left Plot - Normal Stacked Distributions              #######
	##############################################################################
	c1.cd(1)

	print 'Doing Projections'
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',tn_WJetsJBin,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',tn_SingleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',tn_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',tn_ZJetsJBin,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',tn_TTBarDBin,recovariable,presentationbinning,selection+'*('+str(ttscale)+')*'+weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',tn_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)

	if channel=='uujj':
		if 'weight' in qcdselection:
			hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched',tn_QCDMu,recovariable,presentationbinning,qcdselection,QCDStackStyle,Label)
		if 'weight' not in qcdselection:
			hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched',tn_SingleMuData,recovariable,presentationbinning,qcdselection,QCDStackStyle,Label)

	if channel=='uvjj':
		hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched',tn_QCDMu,recovariable,presentationbinning,qcdselection+'*('+str(qcdrescale)+')',QCDStackStyle,Label)


	if channel == 'uujj':

		hs_rec_DiBoson.SetTitle("Other Backgrounds")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets,hs_rec_QCDMu]

	if channel == 'uvjj':
	
		hs_rec_DiBoson.SetTitle("Other Backgrounds")
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)		
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_WJets,hs_rec_QCDMu]
		


	MCStack = THStack ("MCStack","")
	SMIntegral = sum(k.Integral() for k in SM)
	print SMIntegral
	print hs_rec_Data.Integral(), hs_rec_Data.GetEntries()
	
	print 'Stacking...  ',	
	for x in SM:
		# x.Scale(mcdatascalepres)
		MCStack.Add(x)
		x.SetMaximum(10*hs_rec_Data.GetMaximum())

	MCStack.Draw("HIST")
	c1.cd(1).SetLogy()

	MCStack=BeautifyStack(MCStack,Label)

	hs_rec_Data.Draw("EPSAME")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	leg = TLegend(0.63,0.62,0.89,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(.04)
	leg.AddEntry(hs_rec_Data,"Data");
	if channel=='uujj':
		leg.AddEntry(hs_rec_ZJets,'Z/#gamma^{*} + jets')
	if channel=='uvjj':
		leg.AddEntry(hs_rec_WJets,'W + jets')
	leg.AddEntry(hs_rec_TTBar,'t #bar{t} + jets')
	leg.AddEntry(hs_rec_DiBoson,'Other Backgrounds')
	leg.AddEntry(hs_rec_QCDMu,'QCD')
	leg.Draw()

	sqrts = "#sqrt{s} = 8 TeV";
	l1=TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.06)
 
	# l1.DrawLatex(0.37,0.94,"CMS 2012  "+sqrts+", 19.6 fb^{-1}")
	# l1.DrawLatex(0.13,0.76,sqrts)

	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(42)
	l2.SetNDC()
	l2.SetTextSize(0.06)
	# l2.SetTextAngle(45);	
	# l2.DrawLatex(0.15,0.83,"CMS #it{Preliminary}")
	l2.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.6 fb^{-1}")

	gPad.RedrawAxis()

	MCStack.SetMinimum(1.)
	MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())

	if 'PAS' in tagname:
		print 'Saving...  ',
		c1.Print('Results_'+version_name+'/BasicQCD_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
		c1.Print('Results_'+version_name+'/BasicQCD_'+channel+'_'+recovariable+'_'+tagname+'.png')		
		print 'Done.'
		return



	pad2.cd()
	# pad2.SetLogy()
	pad2.SetGrid()

	RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)



	RatHistDen.Sumw2()
	RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
	RatHistNum.Sumw2()
	for hmc in SM:
		RatHistDen.Add(hmc)

	RatHistNum.Add(hs_rec_Data)
	RatHistNum.Divide(RatHistDen)
	# for x in RatHistNum.GetNbinsX():
	# 	print RatHistNum.GetBinCenter(x), RatHistNum.GetBinContent(x)

	RatHistNum.SetMaximum(1.5)
	RatHistNum.SetMinimum(0.5)


	RatHistNum.GetYaxis().SetTitleFont(42);
	RatHistNum.GetXaxis().SetTitle('');
	RatHistNum.GetYaxis().SetTitle('Data/MC');


	RatHistNum.GetXaxis().SetTitleSize(.13);
	RatHistNum.GetYaxis().SetTitleSize(.13);
	RatHistNum.GetXaxis().CenterTitle();
	RatHistNum.GetYaxis().CenterTitle();		
	RatHistNum.GetXaxis().SetTitleOffset(.28);
	RatHistNum.GetYaxis().SetTitleOffset(.28);
	RatHistNum.GetYaxis().SetLabelSize(.09);
	RatHistNum.GetXaxis().SetLabelSize(.09);


	RatHistNum.Draw()
	unity=TLine(RatHistNum.GetXaxis().GetXmin(), 1.0 , RatHistNum.GetXaxis().GetXmax(),1.0)
	unity.Draw("SAME")	


	pad3.cd()
	# pad2.SetLogy()
	pad3.SetGrid()

	chiplot =CreateHisto('chiplot','chiplot',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
	chiplot.Sumw2()

	resstring = '( 0.0 '

	for n in range(chiplot.GetNbinsX()+1):
		lhs = chiplot.GetBinCenter(n) - 0.5*chiplot.GetBinWidth(n)
		rhs = chiplot.GetBinCenter(n) + 0.5*chiplot.GetBinWidth(n)
		lhs = str(round(lhs,3))
		rhs = str(round(rhs,3))

		bg = 0
		bgerr = 0
		dat = hs_rec_Data.GetBinContent(n)
		daterr = math.sqrt(1.0*dat)
		for hmc in SM:
			bg += hmc.GetBinContent(n)
			bgerr += hmc.GetBinError(n)*hmc.GetBinError(n)
		bgerr = math.sqrt(bgerr)
		total_err = math.sqrt(bgerr*bgerr+daterr*daterr)
		
		resfac = '1.0'

		if total_err>0: 
			chi = (dat - bg)/total_err
			chiplot.SetBinContent(n,chi)
			chiplot.SetBinError(n,0.0)
		if bg > 0 and dat > 0:
			resfac = str(round(dat/bg,3))
		if n != 0:
			resstring += ' + '+resfac+'*('+recovariable +'>'+lhs+')'+'*('+recovariable +'<='+rhs+')'

	resstring += ')'
	if recovariable =='Phi_miss':
		print resstring

	chiplot.SetMaximum(6)
	chiplot.SetMinimum(-6)


	chiplot.GetYaxis().SetTitleFont(42);
	chiplot.GetXaxis().SetTitle('');
	chiplot.GetYaxis().SetTitle('#chi (Data,MC)');


	chiplot.GetXaxis().SetTitleSize(.13);
	chiplot.GetYaxis().SetTitleSize(.13);
	chiplot.GetXaxis().CenterTitle();
	chiplot.GetYaxis().CenterTitle();		
	chiplot.GetXaxis().SetTitleOffset(.28);
	chiplot.GetYaxis().SetTitleOffset(.28);
	chiplot.GetYaxis().SetLabelSize(.09);
	chiplot.GetXaxis().SetLabelSize(.09);


	chiplot.Draw('EP')
	zero=TLine(RatHistNum.GetXaxis().GetXmin(), 0.0 , RatHistNum.GetXaxis().GetXmax(),0.0)
	plus2=TLine(RatHistNum.GetXaxis().GetXmin(), 2.0 , RatHistNum.GetXaxis().GetXmax(),2.0)
	minus2=TLine(RatHistNum.GetXaxis().GetXmin(), -2.0 , RatHistNum.GetXaxis().GetXmax(),-2.0)
	plus2.SetLineColor(2)
	minus2.SetLineColor(2)

	plus2.Draw("SAME")
	minus2.Draw("SAME")
	zero.Draw("SAME")	


	print 'Saving...  ',
	c1.Print('Results_'+version_name+'/BasicQCD_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
	c1.Print('Results_'+version_name+'/BasicQCD_'+channel+'_'+recovariable+'_'+tagname+'.png')		
	print 'Done.'



def MakeBasicPlotEMu(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,cutlog,version_name,plotmass):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "te_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('te_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	# Create Canvas
	c1 = TCanvas("c1","",800,800)
	gStyle.SetOptStat(0)

	if 'PAS' not in tagname:
		c1 = TCanvas("c1","",800,800)
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.4, 1.0, 1.0 )#divide canvas into pads
		pad2 = TPad( 'pad2', 'pad2', 0.0, 0.26, 1.0, 0.4 )
		pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.26 )
		pad1.Draw()
		pad2.Draw()
		pad3.Draw()
		pad1.SetBottomMargin(0.0)		
		pad2.SetTopMargin(0.0)
		pad3.SetTopMargin(0.0)
		pad2.SetBottomMargin(0.0)
		pad3.SetBottomMargin(0.43)
	else:
		# if 'final' not in tagname:
		c1 = TCanvas("c1","",800,550)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		perc = 5.0


	pad1.cd()
	# pad1.SetGrid()
	# These are the style parameters for certain plots - [FillStyle,MarkerStyle,MarkerSize,LineWidth,Color]
	MCRecoStyle=[0,20,.00001,1,4]
	DataRecoStyle=[0,20,.7,1,1]
	# X and Y axis labels for plot
	Label=[xlabel,"Events/Bin"]

	WStackStyle=[3007,20,.00001,2,6]
	TTStackStyle=[3005,20,.00001,2,4]
	ZStackStyle=[3004,20,.00001,2,2]
	DiBosonStackStyle=[3006,20,.00001,2,3]
	StopStackStyle=[3008,20,.00001,2,7]
	QCDStackStyle=[3013,20,.00001,2,15]

	SignalStyle=[0,22,0.7,3,28]
	SignalStyle2=[0,22,0.7,3,38]

	if tagname == 'final':
		# print 'cat '+cutlog+' | grep '+channel+str(plotmass)
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+selection+fsel+')'
		# print selection

	##############################################################################
	#######      Top Left Plot - Normal Stacked Distributions              #######
	##############################################################################
	c1.cd(1)
	print 'Projecting trees...  ',
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',te_WJetsJBin,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',te_SingleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',te_ZJetsJBin,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',te_TTBarDBin,recovariable,presentationbinning,selection+'*('+str(ttscale)+')*'+weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',te_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)

	print "THIS NUMBER -->",hs_rec_TTBar.Integral(), hs_rec_TTBar.GetEntries()

	# hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched [Pythia]',te_QCDMu,recovariable,presentationbinning,selection+'*'+weight,QCDStackStyle,Label)

	sig1name = ''
	sig2name = ''

	if channel == 'uujj':
		hs_rec_DiBoson.SetTitle("Other Backgrounds")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_DiBoson,hs_rec_ZJets,hs_rec_TTBar]

	if channel == 'uvjj':
		hs_rec_DiBoson.SetTitle("Other Backgrounds")
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)		
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_WJets]
		

	# mcdatascalepres = (1.0*(hs_rec_Data.GetEntries()))/(sum(k.Integral() for k in SM))

	MCStack = THStack ("MCStack","")
	SMIntegral = sum(k.Integral() for k in SM)
	print SMIntegral
	print hs_rec_Data.Integral(), hs_rec_Data.GetEntries()
	# MCStack.SetMaximum(SMIntegral*100)
	
	print 'Stacking...  ',	
	for x in SM:
		# x.Scale(mcdatascalepres)
		MCStack.Add(x)
		x.SetMaximum(10*hs_rec_Data.GetMaximum())

	MCStack.Draw("HIST")
	c1.cd(1).SetLogy()

	MCStack=BeautifyStack(MCStack,Label)

	hs_rec_Data.Draw("EPSAME")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	leg = TLegend(0.63,0.62,0.89,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(.04)
	leg.AddEntry(hs_rec_Data,"Data");
	if channel=='uujj':
		leg.AddEntry(hs_rec_ZJets,'Z/#gamma^{*} + jets')
	if channel=='uujj':
		leg.AddEntry(hs_rec_WJets,'W + jets')
	leg.AddEntry(hs_rec_TTBar,'t #bar{t} + jets')
	leg.AddEntry(hs_rec_DiBoson,'Other Backgrounds')
	leg.Draw()

	sqrts = "#sqrt{s} = 8 TeV";
	l1=TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.06)
 
	# l1.DrawLatex(0.37,0.94,"CMS 2012  "+sqrts+", 19.6 fb^{-1}")
	# l1.DrawLatex(0.13,0.76,sqrts)

	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(42)
	l2.SetNDC()
	l2.SetTextSize(0.06)
	# l2.SetTextAngle(45);	
	# l2.DrawLatex(0.15,0.83,"CMS #it{Preliminary} ")
	l2.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.6 fb^{-1}")

	gPad.RedrawAxis()

	MCStack.SetMinimum(.03333)
	MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())

	if 'PAS' in tagname:

		print 'Saving...  ',
		if 'final' not in tagname:
			c1.Print('Results_'+version_name+'/Basic_NoRatio_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
			c1.Print('Results_'+version_name+'/Basic_NoRatio_'+channel+'_'+recovariable+'_'+tagname+'.png')
		else:
			c1.Print('Results_'+version_name+'/Basic_NoRatio_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf')
			c1.Print('Results_'+version_name+'/Basic_NoRatio_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.png')		
		print 'Done.'

		return

	pad2.cd()
	# pad2.SetLogy()
	pad2.SetGrid()

	RatHistDen =CreateHisto('RatHisDen','RatHistDen',te_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)



	RatHistDen.Sumw2()
	RatHistNum =CreateHisto('RatHisNum','RatHistNum',te_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
	RatHistNum.Sumw2()
	for hmc in SM:
		RatHistDen.Add(hmc)

	RatHistNum.Add(hs_rec_Data)
	RatHistNum.Divide(RatHistDen)
	# for x in RatHistNum.GetNbinsX():
	# 	print RatHistNum.GetBinCenter(x), RatHistNum.GetBinContent(x)

	RatHistNum.SetMaximum(1.5)
	RatHistNum.SetMinimum(0.5)


	RatHistNum.GetYaxis().SetTitleFont(42);
	RatHistNum.GetXaxis().SetTitle('');
	RatHistNum.GetYaxis().SetTitle('Data/MC');


	RatHistNum.GetXaxis().SetTitleSize(.13);
	RatHistNum.GetYaxis().SetTitleSize(.13);
	RatHistNum.GetXaxis().CenterTitle();
	RatHistNum.GetYaxis().CenterTitle();		
	RatHistNum.GetXaxis().SetTitleOffset(.28);
	RatHistNum.GetYaxis().SetTitleOffset(.28);
	RatHistNum.GetYaxis().SetLabelSize(.09);
	RatHistNum.GetXaxis().SetLabelSize(.09);


	RatHistNum.Draw()
	unity=TLine(RatHistNum.GetXaxis().GetXmin(), 1.0 , RatHistNum.GetXaxis().GetXmax(),1.0)
	unity.Draw("SAME")	


	pad3.cd()
	# pad2.SetLogy()
	pad3.SetGrid()

	chiplot =CreateHisto('chiplot','chiplot',te_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
	chiplot.Sumw2()

	resstring = '( 0.0 '

	for n in range(chiplot.GetNbinsX()+1):
		lhs = chiplot.GetBinCenter(n) - 0.5*chiplot.GetBinWidth(n)
		rhs = chiplot.GetBinCenter(n) + 0.5*chiplot.GetBinWidth(n)
		lhs = str(round(lhs,3))
		rhs = str(round(rhs,3))

		bg = 0
		bgerr = 0
		dat = hs_rec_Data.GetBinContent(n)
		daterr = math.sqrt(1.0*dat)
		for hmc in SM:
			bg += hmc.GetBinContent(n)
			bgerr += hmc.GetBinError(n)*hmc.GetBinError(n)
		bgerr = math.sqrt(bgerr)
		total_err = math.sqrt(bgerr*bgerr+daterr*daterr)
		
		resfac = '1.0'

		if total_err>0: 
			chi = (dat - bg)/total_err
			chiplot.SetBinContent(n,chi)
			chiplot.SetBinError(n,0.0)
		if bg > 0 and dat > 0:
			resfac = str(round(dat/bg,3))
		if n != 0:
			resstring += ' + '+resfac+'*('+recovariable +'>'+lhs+')'+'*('+recovariable +'<='+rhs+')'

	resstring += ')'
	if recovariable =='Phi_miss':
		print resstring

	chiplot.SetMaximum(6)
	chiplot.SetMinimum(-6)


	chiplot.GetYaxis().SetTitleFont(42);
	chiplot.GetXaxis().SetTitle('');
	chiplot.GetYaxis().SetTitle('#chi (Data,MC)');


	chiplot.GetXaxis().SetTitleSize(.13);
	chiplot.GetYaxis().SetTitleSize(.13);
	chiplot.GetXaxis().CenterTitle();
	chiplot.GetYaxis().CenterTitle();		
	chiplot.GetXaxis().SetTitleOffset(.28);
	chiplot.GetYaxis().SetTitleOffset(.28);
	chiplot.GetYaxis().SetLabelSize(.09);
	chiplot.GetXaxis().SetLabelSize(.09);


	chiplot.Draw('EP')
	zero=TLine(RatHistNum.GetXaxis().GetXmin(), 0.0 , RatHistNum.GetXaxis().GetXmax(),0.0)
	plus2=TLine(RatHistNum.GetXaxis().GetXmin(), 2.0 , RatHistNum.GetXaxis().GetXmax(),2.0)
	minus2=TLine(RatHistNum.GetXaxis().GetXmin(), -2.0 , RatHistNum.GetXaxis().GetXmax(),-2.0)
	plus2.SetLineColor(2)
	minus2.SetLineColor(2)

	plus2.Draw("SAME")
	minus2.Draw("SAME")
	zero.Draw("SAME")	


	print 'Saving...  ',
	if 'final' not in tagname:
		c1.Print('Results_'+version_name+'/Basic_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
		c1.Print('Results_'+version_name+'/Basic_'+channel+'_'+recovariable+'_'+tagname+'.png')
	else:
		c1.Print('Results_'+version_name+'/Basic_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf')
		c1.Print('Results_'+version_name+'/Basic_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.png')		
	print 'Done.'

def round_to(n, precission):
    correction = 0.5 if n >= 0 else -0.5
    return int(n/precission+correction)*precission

def TH2toCutRes(th2,thname, addon):
	res = []

	# print th2.Integral()
	nx = th2.GetNbinsX()+1
	ny = th2.GetNbinsY()+1
	for x in range(nx):
		for y in range(ny):
			if x == 0 : continue
			if y == 0 : continue
			res.append([thname,[addon, th2.GetXaxis().GetBinCenter(x) - 0.5*th2.GetXaxis().GetBinWidth(x), th2.GetYaxis().GetBinCenter(y) - 0.5*th2.GetYaxis().GetBinWidth(y)],th2.Integral(x,nx,y,ny)])

	return res


def GetRatesFromTH2(sigs,baks,_presel,_weight,_hvars,addon,scalefac):
	b1 = ConvertBinning(_hvars[0][1])
	b2 = ConvertBinning(_hvars[1][1])
	v1 = (_hvars[0][0])
	v2 = (_hvars[1][0])
	allinfo = []
	for t in sigs+baks:
		print 'Checking: ',t
		h = 'h_'+t
		# print( h + ' = TH2D("'+h+'","'+h+'",len(b1)-1,array(\'d\',b1),len(b2)-1,array(\'d\',b2))')
		exec( h + ' = TH2D("'+h+'","'+h+'",len(b1)-1,array(\'d\',b1),len(b2)-1,array(\'d\',b2))')
		exec( t+'.Project("'+h+'","'+v2+':'+v1+'","'+_presel+'*('+_weight+'*'+scalefac+')")')
		exec( 'allinfo += TH2toCutRes ('+h+',"'+h+'",'+str(addon)+')')
		# break
	return allinfo


def OptimizeCuts3D(variablespace,presel,weight,tag,scalefacs,cutfile,channel):
	outfile = 'Results_'+tag+'/'+channel+'Cuts.txt'
	ftmpname = channel+'_opttmp.root'
	ftmp = TFile.Open(ftmpname,'RECREATE')
	optvars = []
	binnings = []
	for v in variablespace:
		v = v.split(':')
		var = v[0]
		v0 = float(v[1])
		v1 = float(v[3])
		vb = float(v[2])
		bins = [int(round((v1-v0)/vb)),v0,v1]
		optvars.append([var,bins]) 

	minvar = ['',[9999999,0,0]]
	for v in range(len(optvars)):
		if optvars[v][1][0] < minvar[1][0]:
			minvar = optvars[v]
	hvars = []
	for v in range(len(optvars)):
		if optvars[v] != minvar:
			hvars.append(optvars[v])

	minvarcuts = ['('+minvar[0]+'>'+str(x)+')' for x in ConvertBinning(minvar[1])] 

	signals =  [ 't_'+x.replace('.root\n','') for x in  os.popen('ls '+NormalDirectory+'| grep root | grep LQ'+channel+' ').readlines()]
	backgrounds =  [ 't_'+x.replace('\n','') for x in  ['DiBoson','WJetsJBin','TTBarDBin','ZJetsJBin','SingleTop']]

	[_r_z,_r_tt,_r_w] = scalefacs

	if cutfile=='':
		cutinfo = []
		logfile = 'Results_'+tag+'/Log_'+channel+'Cuts.txt'
		l = open(logfile,'w')
		for h in signals+backgrounds:
			l.write('h_'+h+' = [] \n')
		for x in range(len(minvarcuts)):
			print 'Analyzing for case ',minvarcuts[x]
			scalefac = '1.0'
			if 'ZJets' in h:
				scalefac = str(_r_z)
			if 'WJets' in h:
				scalefac = str(_r_w)
			if 'TTBar' in h:
				scalefac = str(_r_tt)
		 	moreinfo = GetRatesFromTH2(signals,backgrounds,presel+'*'+minvarcuts[x],weight,hvars,(ConvertBinning(minvar[1]))[x],scalefac)
		 	for m in  moreinfo:
				l.write(m[0]+'.append(['+str(m[2])+','+str(m[1])+'])\n')
		l.close()

		os.system('rm '+ftmpname)
		cutfile = logfile
	
	print 'Getting log ... '
	# flog = open('loglog.txt','w')

	nf = os.popen('cat '+cutfile+' | wc -l').readlines()[0]
	nf = int(nf)
	nd = 0
	for c in open(cutfile):
		nd += 1
		if nd%100000==0:
			print str(round( (1.0*nd)/(1.0*nf),2 )), '% complete'
		# print '** ',c
		# flog.write('** '+c)
		exec(c)

	# flog.close()
	
	SIGS = []
	BAKS = []

	for h in signals:
		exec('SIGS.append(h_'+h+')')
	for h in backgrounds:
		exec('BAKS.append(h_'+h+')')

	optimlog = open('Results_'+tag+'/Opt_'+channel+'Cuts.txt','w')

	valuetable = []

	for S in range(len(SIGS)):
		_ssbmax = -99999
		_bestcut = 0
		for icut in range(len(SIGS[S])):
			_s = SIGS[S][icut][0]
			_b = 0.0
			for B in BAKS:
				_b += B[icut][0]
			if _s + _b < 0.0001:
				continue
			_ssb = _s/math.sqrt(_s+_b)
			if _ssb > _ssbmax:
				_ssbmax = _ssb
				_bestcut = icut
		opt = 'opt_'+signals[S].replace('t_','')+ ' = (('+minvar[0] +'>' + str(SIGS[S][_bestcut][1][0])+')*('+hvars[0][0]+'>'+str(SIGS[S][_bestcut][1][1])+')*('+hvars[1][0]+'>'+str(SIGS[S][_bestcut][1][2])+'))\n'  
		print opt
		thismass = float(((signals[S].replace('t_','')).split('jj'))[-1])
		valueline = [thismass, (SIGS[S][_bestcut][1][0]), (SIGS[S][_bestcut][1][1]), (SIGS[S][_bestcut][1][2])]
		valuetable.append(valueline)
		optimlog.write(opt)

	optimlog.close()

	print 'Performing fits ...'
	cuts = MakeSmoothCuts(valuetable,[minvar[0],hvars[0][0], hvars[1][0]],tag,channel,'lin')
	cuts = MakeSmoothCuts(valuetable,[minvar[0],hvars[0][0], hvars[1][0]],tag,channel,'lintanh')
	cuts = MakeSmoothCuts(valuetable,[minvar[0],hvars[0][0], hvars[1][0]],tag,channel,'pol2')
	cuts = MakeSmoothCuts(valuetable,[minvar[0],hvars[0][0], hvars[1][0]],tag,channel,'pol2cutoff')
	cuts = MakeSmoothCuts(valuetable,[minvar[0],hvars[0][0], hvars[1][0]],tag,channel,'lincutoff')

	return cuts

def ReDoOptFits(OptFile):
	tag = OptFile.split('/')[0]
	tag = tag.replace('Results_','')
	valuetable = []
	for line in open(OptFile):
		valueline = []
		channel = line.split('jj')[0]
		channel = channel.split('LQ')[1]
		channel += 'jj'
		mass = float(line.split('jj')[1].split('=')[0].replace(' ',''))

		varnames = line.split('=')[-1]
		varnames = varnames.replace(')','')
		varnames = varnames.replace('(','')
		varnames = varnames.split('*')
		varwords = []
		varvals = []
		for v in varnames:
			v = v.split('>')
			varwords.append(v[0].replace(' ',''))
			varvals.append(float(v[1]))
		valueline = [mass]
		for v in varvals:
			valueline.append(v)
		valuetable.append(valueline)
	# print tag,channel, varwords
	# for v in valuetable:
	# 	print v

	# cuts = MakeSmoothCuts(valuetable,varwords,tag,channel,'lin')
	# cuts = MakeSmoothCuts(valuetable,varwords,tag,channel,'lintanh')
	# cuts = MakeSmoothCuts(valuetable,varwords,tag,channel,'pol2')
	cuts = MakeSmoothCuts(valuetable,varwords,tag,channel,'pol2cutoff')
	# cuts = MakeSmoothCuts(valuetable,varwords,tag,channel,'lincutoff')		

def MakeSmoothCuts(vals,vnames,versionname,chan,rawmethod):

	xnames = []
	for x in vnames:
		a = x
		if "Pt_jet1" in a :  x = "p_{T}(jet_{1})"
		if "Pt_jet2" in a :  x = "p_{T}(jet_{2})"
		if "Pt_muon1" in a :  x = "p_{T}(#mu_{1})"
		if "Pt_muon2" in a :  x = "p_{T}(#mu_{2})"
		if "St_uujj" in a :  x = "S_{T}^{#mu #mu j j}"
		if "M_uu" in a :  x = "M^{#mu #mu}"
		if "M_uujj1" in a :  x = "M^{#mu j}_{1}"
		if "M_uujj2" in a :  x = "M^{#mu j}_{2}"
		if "GoodVertexCount" in a :  x = "N_{Vertices}"
		if "Pt_jet1" in a :  x = "p_{T}(jet_{1})"
		if "Pt_jet2" in a :  x = "p_{T}(jet_{2})"
		if "Pt_muon1" in a :  x = "p_{T}(#mu_{1})"
		if "Pt_miss" in a :  x = "E_{T}^{miss}"
		if "St_uvjj" in a :  x = "S_{T}^{#mu #nu j j}"
		if "MT_uv in" in a :  x = "M_{T}^{#mu #nu}"
		if "MT_uvjj" in a :  x = "M_{T}^{#mu j}"
		if "M_uvjj" in a :  x = "M^{#mu j}"
		xnames.append(x)

	_allvals = sorted(vals,key=lambda vals: vals[0])


	if 'cutoff' in rawmethod:
		_vals = []
		for v in _allvals:
			if v[0] <= 1000:
				_vals.append(v)
	else:
		_vals=_allvals

	for v in _vals:
		print v

	yinds = []
	masses = []

	for v in range(len(_vals[0])):
		if v == 0: 
			for v in _vals:
				masses.append(v[0])
			continue
		yinds.append(v)

	allmasses = []

	for v in range(len(_allvals[0])):
		if v == 0: 
			for v in _allvals:
				allmasses.append(v[0])	

	n = len(masses)

	method = rawmethod.replace('cutoff','')
	optim_res=[masses]
	for y in yinds:

		Y = []
		for v in _vals:
			Y.append(v[y])
		print Y		
		X = array("d", masses)
		Y = array("d", Y)

		c1 = TCanvas("c1","",700,500)
		c1.cd(1).SetGrid()

		print X
		print Y
		hout = TGraph(n,X,Y)
		hout.GetYaxis().SetTitle(xnames[y-1]+' Threshold [GeV]')
		hout.GetXaxis().SetTitle('LQ Mass [GeV]')
		hout.SetTitle('')
		hout.SetMarkerStyle(21)
		hout.SetMarkerSize(1)
		hout.SetLineWidth(2)
		hout.SetLineColor(1)
		hout.GetXaxis().SetTitleFont(42)
		hout.GetYaxis().SetTitleFont(42)
		hout.GetXaxis().SetLabelFont(42)
		hout.GetYaxis().SetLabelFont(42)
		hout.GetYaxis().SetTitleFont(42);
		hout.GetXaxis().SetTitleSize(.06);
		hout.GetYaxis().SetTitleSize(.06);
		hout.GetXaxis().CenterTitle();
		hout.GetYaxis().CenterTitle();
		hout.GetXaxis().SetTitleOffset(0.8);
		hout.GetYaxis().SetTitleOffset(0.8);
		hout.GetYaxis().SetLabelSize(.05);
		hout.GetXaxis().SetLabelSize(.05);
		hout.Draw("AP")
		
		if method == 'lin':
			ft = TF1("ft","[1]*x + [0]", 250,1250 )  # linear
		if method == 'lintanh':
			ft = TF1("ft","[0] + [1]*[1]*tanh(x+[2]) + [3]*[3]*x",250,1250) 		#linear+tanh monotonic
		if method == 'pol2':
			ft = TF1("ft","[0] + [1]*x + [2]*(x*x)", 250, 1250); # second degree pol
		hout.Fit('ft')

		betterfits = []
		for m in allmasses:
			orig_val = ft.Eval(m)
			new_val = round_to(orig_val,5)
			betterfits.append(new_val)
		optim_res.append(betterfits)
		c1.Print('Results_'+versionname+'/Optimization_'+chan+'_'+vnames[y-1]+'_'+rawmethod+'.pdf')
		c1.Print('Results_'+versionname+'/Optimization_'+chan+'_'+vnames[y-1]+'_'+rawmethod+'.png')

	optimlog = open('Results_'+versionname+'/Opt_'+chan+'Cuts_Smoothed_'+rawmethod+'.txt','w')	

	for x in range(len(optim_res[0])):
		cutstr = ''
		for y in range(len(vnames)):
			cutstr += '('+vnames[y]+ '>'+str(optim_res[y+1][x])+ ')*'
		optline =  'opt_LQ'+chan+str(int(optim_res[0][x]))+ ' = ('+cutstr[:-1]+')'
		print optline
		optimlog.write(optline+'\n')
	optimlog.close()
	return 'Results_'+versionname+'/Opt_'+chan+'Cuts_Smoothed.txt'

def CompareMeanSys(m,s1,s2):
	_m = []
	_s1 = []
	_s2 = []
	for x in range(len(m)):
		if x == 1:
			continue
		_m.append(m[x][0])
		_s1.append(s1[x][0])
		_s2.append(s2[x][0])

	systematics = []

	for x in range(len(_m)):
		syst = 1
		mavg = _m[x]
		sv1 = _s1[x]
		sv2 = _s2[x]
		d1 = abs(sv1-mavg)
		d2 = abs(sv2-mavg)
		diff = max([d1,d2])
		if diff > 0 and mavg > 0:
			syst = 1 + diff/mavg
		systematics.append(syst)
	outline = ' '
	for s in systematics:
		outline += str(s) + ' '
	return outline


def ParseFinalCards(cardcoll):
	chan = '' + 'uujj'*('uujj' in cardcoll)+ 'uvjj'*('uvjj' in cardcoll) 
	tables = glob(cardcoll)
	systypes = []
	for t in tables:
		_sys = (t.split('_')[-1]).replace('.txt','')
		systypes.append(_sys)
	variations = []
	for s in systypes:
		s = s.replace('up','')
		s = s.replace('down','')
		if s not in variations:
			variations.append(s)
	# for v in variations:
	# 	print v
	T = ''
	for n in range(len(systypes)):
		if systypes[n]=='':
			T = tables[n]
	print T
	cardnames = []
	for line in open(T,'r'):
		if 'L_' in line:
			cardname = line.split(' = ')[0]
			cardname = cardname.split('_')[-1] 
			cardnames.append(cardname)
		print ' * ',line
		exec(line)

	configlines = ['','imax 1','jmax '+str(len(headers)-2),'kmax '+str(len(headers)-1+len(variations)-1),'','bin 1','']

	nc = 0
	standardweights = []

	finalcards = cardcoll.replace('*','_ALL_')
	finalcards = finalcards.replace('systable','finalcards')
	fout = open(finalcards,'w')


	for card in cardnames:
		allcards = [line.replace('\n','') for line in os.popen('grep '+card+' '+cardcoll).readlines()]
		nc += 1
		mcard = ''
		scards = []
		for a in allcards:
			if T in a:
				mcard = a
			else:
				scards.append(a)
			
		statlines = []

		# print headers
		# print mcard
		exec ('minfo = '+mcard.split('=')[-1])
		# print minfo
		# print ' \n '
		weights = []
		nums = []
		rates = []
		for entry in minfo:
			if entry[1] > 0.001:
				weights.append((1.0*entry[0])/(1.0*entry[1]))
			else:
				weights.append(0)
			nums.append(int(entry[1]))
			rates.append(entry[0])
		if nc ==1:
			standardweights = weights
		statlines = []
		spacers = -1
		rateline = 'rate '
		for h in range(len(headers)):
			head = headers[h]
			if 'Data' in head:
				continue
			spacers += 1
			nmc = nums[h]
			w = weights[h]
			if w <0.0000000001:
				w = standardweights[h]
			nmc = str(int(nmc))
			w = str(w)
			r = str(rates[h])
			statline = 'stat_'+head+' gmN '+nmc + (' - ')*spacers +' ' + w +' '+(' - ')*(len(headers) -2 - spacers)
			if nmc > 0:
				statlines.append(statline)
			rateline += ' '+r


		obsline = 'observation '+str(minfo[1][1])
		binline = 'bin '+(' 1 ')*(len(headers)-1)
		procline1 = 'process  '+card
		for hh in headers:
			if 'Sig' in hh or 'Data' in hh:
				continue
			procline1 += ' '+hh
		procline2 = 'process  0 '+(' 1 ')*(len(headers)-2)

		syslines = []
		for v in variations:
			if v == '':
				continue
			sysline = v + '  lnN  '
			this_sysset = []
			for ss in scards:
				if v in ss:
					this_sysset.append(ss)
			if len(this_sysset) == 1:
				this_sysset.append(this_sysset[0])
			exec ('sys1 = '+this_sysset[0].split('=')[-1])
			exec ('sys2 = '+this_sysset[1].split('=')[-1])
			sysline += CompareMeanSys(minfo,sys1,sys2)
			syslines.append(sysline)


		fout.write( card + '.txt\n\n')
		for configline in configlines:
			fout.write( configline+'\n')
		fout.write( obsline+'\n')
		fout.write( ' '+'\n')
		fout.write( binline+'\n')
		fout.write( procline1+'\n')
		fout.write( procline2+'\n')
		fout.write( ' '+'\n')
		fout.write( rateline+'\n')
		fout.write( ' '+'\n')
		for sysline in syslines:
			fout.write( sysline+'\n')
		fout.write( ' '+'\n')
		for statline in statlines:
			fout.write( statline+'\n')
		fout.write( '\n'*3)

	fout.close()
	return finalcards

def FixFinalCards(cardsets):
	f = cardsets[0].split('/')[0]+'/FinalCards.txt'
	fout = open(f,'w')
	for c in cardsets:
		for line in open(c,'r'):
			line = line.replace('uujj','_M_')
			line = line.replace('uvjj','_BetaHalf_M_')
			fout.write(line)
	fout.close()
	return f


main()
