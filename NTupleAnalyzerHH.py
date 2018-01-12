#!/usr/bin/python
from datetime import datetime
import sys
sys.argv.append( '-b True' )
from ROOT import *
import array
import math
from argparse import ArgumentParser
tRand = TRandom3()
from random import randint

##########################################################################################
#################      SETUP OPTIONS - File, Normalization, etc    #######################
##########################################################################################

# Input Options - file, cross-section, number of events
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help="input root file", metavar="FILE")
parser.add_argument("-b", "--batch", dest="dobatch", help="run in batch mode", metavar="BATCH")
parser.add_argument("-s", "--sigma", dest="crosssection", help="specify the process cross-section", metavar="SIGMA")
parser.add_argument("-n", "--ntotal", dest="ntotal", help="total number of MC events for the sample", metavar="NTOTAL")
parser.add_argument("-l", "--lumi", dest="lumi", help="integrated luminosity for data taking", metavar="LUMI")
parser.add_argument("-j", "--json", dest="json", help="json file for certified run:lumis", metavar="JSON")
parser.add_argument("-d", "--dir", dest="dir", help="output directory", metavar="DIR")
parser.add_argument("-p", "--pdf", dest="pdf", help="option to produce pdf uncertainties", metavar="PDF")


options = parser.parse_args()
dopdf = int(options.pdf)==1

# Here we get the file name, and adjust it accordingly for EOS, castor, or local directory
name = options.filename
amcNLOname = options.filename

if '/store' in name:
	name = 'root://eoscms//eos/cms'+name
if '/castor/cern.ch' in name:
	name = 'rfio://'+name

# These are switches based on the tag name. 
# First is whether to change out a muon with an electron ( for e-mu ttbar samples)
emuswitch=False
if "EMuSwitch" in options.dir:
	emuswitch=True
# Turn of the isolation condition for QCD studies
nonisoswitch=False
if "NonIso" in options.dir:
	nonisoswitch = True
# Quick test means no systematics
quicktestswitch = False
if "QuickTest" in options.dir:
	quicktestswitch = True
# Modifications of muon pT due to muon aligment mismodelling.
alignementcorrswitch = False
if "AlignmentCorr" in options.dir:
	alignementcorrswitch = True

print 'EMu Switch = ', emuswitch
print 'NonIso Switch = ', nonisoswitch
print 'Quick Switch (No Sys) = ', quicktestswitch
print 'AlignmentCorr Switch = ', alignementcorrswitch

# Get the file, tree, and number of entries
print name
#newntupleswitch = True#'V00-03-18' in name
#if newntupleswitch == True:
#	print 'Detected V00-03-18 ntuple - making small tweaks to handle this!'

fin = TFile.Open(name,"READ")

hev = fin.Get('LJFilter/EventCount/EventCounter')
NORIG = hev.GetBinContent(1)
SumOfTopPtReweights = hev.GetBinContent(4)
if 'SingleMuon' in name or 'SingleElectron' in name or 'DoubleMuon' in name or 'DoubleEG' in name:
	_TopPtFactor = 1.0
else:
	_TopPtFactor = float(NORIG)/float(SumOfTopPtReweights)

# Typical event weight, sigma*lumi/Ngenerated
startingweight = _TopPtFactor*float(options.crosssection)*float(options.lumi)/float(options.ntotal)

to = fin.Get("rootTupleTree/tree")
No = to.GetEntries()

# Here we are going to pre-skim the file to reduce running time.
indicator = ((name.split('/'))[-1]).replace('.root','')
#print indicator
#junkfile1 = str(randint(100000000,1000000000))+indicator+'junk.root'

# At least one 44 GeV Muon - offline cut is 50
#fj1 = TFile.Open(junkfile1,'RECREATE')
#t1 = to.CopyTree('MuonPt[]>12')#fixme was MuonPt[]>44
# t1 = to.CopyTree('(1)')
#Nm1 = t1.GetEntries()

junkfile2 = str(randint(100000000,1000000000))+indicator+'junk.root'

# At least one 44 GeV jet - offline cut is 50
fj2 = TFile.Open(junkfile2,'RECREATE')
t = to.CopyTree('PFJetPtAK4CHS[]>18')#fixme was 44
N = t.GetEntries()

# Print the reduction status
print 'Original events:          ',No
#print 'After demand 1 pT16 muon or electron: ',Nm1
print 'After demand 1 pT18 jet:  ',N

##########################################################################################
#################      PREPARE THE VARIABLES FOR THE OUTPUT TREE   #######################
##########################################################################################

# Branches will be created as follows: One branch for each kinematic variable for each 
# systematic variation determined in _variations. One branch for each weight and flag.
# So branch names will include weight_central, run_number, Pt_muon1, Pt_muon1MESUP, etc.

_kinematicvariables = ['Pt_muon1','Pt_muon2','Pt_ele1','Pt_ele2','Pt_lep1','Pt_lep2','Pt_jet1','Pt_jet2','Pt_miss']
_kinematicvariables += ['Pt_jet3','Pt_jet4']
_kinematicvariables += ['Eta_muon1','Eta_muon2','Eta_ele1','Eta_ele2','Eta_lep1','Eta_lep2','Eta_jet1','Eta_jet2','Eta_miss']
_kinematicvariables += ['Phi_muon1','Phi_muon2','Phi_ele1','Phi_ele2','Phi_lep1','Phi_lep2','Phi_jet1','Phi_jet2','Phi_miss']
_kinematicvariables += ['Phi_Hjet1','Phi_Hjet2','Phi_Zjet1','Phi_Zjet2']
_kinematicvariables += ['Eta_Hjet1','Eta_Hjet2','Eta_Zjet1','Eta_Zjet2']
_kinematicvariables += ['Pt_muon1_gen','Pt_muon2_gen']
_kinematicvariables += ['Pt_Hjet1_gen','Pt_Hjet2_gen','Pt_Zjet1_gen','Pt_Zjet2_gen']
_kinematicvariables += ['Pt_muon1_genMatched','Pt_muon2_genMatched']
_kinematicvariables += ['Pt_Hjet1_genMatched','Pt_Hjet2_genMatched','Pt_Zjet1_genMatched','Pt_Zjet2_genMatched']
_kinematicvariables += ['Phi_Hjet1_gen','Phi_Hjet2_gen','Phi_Zjet1_gen','Phi_Zjet2_gen']
_kinematicvariables += ['Eta_Hjet1_gen','Eta_Hjet2_gen','Eta_Zjet1_gen','Eta_Zjet2_gen']
_kinematicvariables += ['X_miss','Y_miss']
_kinematicvariables += ['TrkIso_muon1','TrkIso_muon2','TrkIso_ele1','TrkIso_ele2','TrkIso_lep1','TrkIso_lep2']
_kinematicvariables += ['Chi2_muon1','Chi2_muon2']
_kinematicvariables += ['PFID_muon1','PFID_muon2']
_kinematicvariables += ['TrkMeasLayers_muon1','TrkMeasLayers_muon2']
_kinematicvariables += ['Charge_muon1','Charge_muon2','Charge_ele1','Charge_ele2','Charge_lep1','Charge_lep2']
_kinematicvariables += ['TrkGlbDpt_muon1','TrkGlbDpt_muon2']
_kinematicvariables += ['NHEF_jet1','NHEF_jet2','NEMEF_jet1','NEMEF_jet2']
_kinematicvariables += ['St_uujj','St_eejj','St_lljj']
_kinematicvariables += ['St_uu4j','St_ee4j','St_ll4j']
_kinematicvariables += ['M_uu','M_ee','M_ll']
_kinematicvariables += ['M_jj']
_kinematicvariables += ['DR_muon1muon2','DPhi_muon1met','DPhi_jet1met','DPhi_jet2met']
_kinematicvariables += ['DR_ele1ele2','DPhi_ele1met']
_kinematicvariables += ['DR_muon1jet1','DR_muon1jet2','DR_muon2jet1','DR_muon2jet2']
_kinematicvariables += ['DR_ele1jet1','DR_ele1jet2','DR_ele2jet1','DR_ele2jet2']
_kinematicvariables += ['DR_lep1jet1','DR_lep1jet2','DR_lep2jet1','DR_lep2jet2']
_kinematicvariables += ['DR_jet1jet2','DPhi_jet1jet2']
_kinematicvariables += ['DPhi_muon1jet1','DPhi_muon1jet2','DPhi_muon2jet1','DPhi_muon2jet2']
_kinematicvariables += ['DPhi_ele1jet1','DPhi_ele1jet2','DPhi_ele2jet1','DPhi_ele2jet2']
_kinematicvariables += ['DPhi_lep1jet1','DPhi_lep1jet2','DPhi_lep2jet1','DPhi_lep2jet2']
_kinematicvariables += ['M_uujj','M_eejj','M_ll4j']
_kinematicvariables += ['M_uu4j','M_ee4j','M_ll4j']
_kinematicvariables += ['Mbb_H','Mjj_Z','Mjj_Z_3jet']
_kinematicvariables += ['Mbb_H_gen','Mjj_Z_gen']
_kinematicvariables += ['Mbb_H_genMatched','Mjj_Z_genMatched']
_kinematicvariables += ['Mbb_H_noReg','Muu4j_noReg']
_kinematicvariables += ['cosThetaStarMu','cosThetaStarEle','cosThetaStarLep']
_kinematicvariables += ['cosThetaStarMu_gen','cosThetaStarEle_gen']
_kinematicvariables += ['cosThetaStar_gen','cosTheta_hbb_gen','cosTheta_zjj_hzz_gen','cosTheta_zuu_hzz_gen','cosTheta_zj1_hzz_gen','cosTheta_zu1_hzz_gen']
_kinematicvariables += ['phi0_gen','phi1_gen']
_kinematicvariables += ['cosThetaStarZuu_CS_gen','cosTheta_Zuu_gen']
_kinematicvariables += ['phi0_zz_gen','phi1_zuu_gen','phi1_zjj_gen']
_kinematicvariables += ['cosThetaStar','cosTheta_hbb','cosTheta_zjj_hzz','cosTheta_zuu_hzz','cosTheta_zj1_hzz','cosTheta_zu1_hzz']
_kinematicvariables += ['phi0','phi1']
_kinematicvariables += ['cosThetaStarZuu_CS','cosTheta_Zuu']
_kinematicvariables += ['phi0_zz','phi1_zuu','phi1_zjj']
_kinematicvariables += ['Pt_Hjet1_noReg','Pt_Hjet2_noReg']
_kinematicvariables += ['Pt_Hjet1','Pt_Hjet2','Pt_Zjet1','Pt_Zjet2']
_kinematicvariables += ['Pt_Hjets','Pt_Zjets','Pt_uu','Pt_ee','Pt_ll']
_kinematicvariables += ['DR_jj_Z','DR_bb_H']
_kinematicvariables += ['DR_u1Hj1','DR_u1Hj2','DR_u2Hj1','DR_u2Hj2']
_kinematicvariables += ['DR_u1Zj1','DR_u1Zj2','DR_u2Zj1','DR_u2Zj2']
_kinematicvariables += ['DR_u1Hj1_gen','DR_u1Hj2_gen','DR_u2Hj1_gen','DR_u2Hj2_gen']
_kinematicvariables += ['DR_u1Zj1_gen','DR_u1Zj2_gen','DR_u2Zj1_gen','DR_u2Zj2_gen']
_kinematicvariables += ['DR_u1Hj1_genMatched','DR_u1Hj2_genMatched','DR_u2Hj1_genMatched','DR_u2Hj2_genMatched']
_kinematicvariables += ['DR_u1Zj1_genMatched','DR_u1Zj2_genMatched','DR_u2Zj1_genMatched','DR_u2Zj2_genMatched']
_kinematicvariables += ['DR_uu_bb_H','DR_uu_jj_Z','DPhi_uu_bb_H','DPhi_uu_jj_Z']
_kinematicvariables += ['DR_ee_bb_H','DR_ee_jj_Z','DPhi_ee_bb_H','DPhi_ee_jj_Z']
_kinematicvariables += ['DR_ll_bb_H','DR_ll_jj_Z','DPhi_ll_bb_H','DPhi_ll_jj_Z']
_kinematicvariables += ['DPhi_jj_Z','DPhi_bb_H']
_kinematicvariables += ['minDR_muonjet','minDR_electronjet']
_kinematicvariables += ['M_uu4j_gen','M_uu4j_genMatched']
_kinematicvariables += ['M_ee4j_gen','M_ee4j_genMatched']
_kinematicvariables += ['M_ll4j_gen','M_ll4j_genMatched']
_kinematicvariables += ['jetCntPreFilter','JetCount','MuonCount','ElectronCount','GenJetCount']
_kinematicvariables += ['IsMuon_muon1','IsMuon_muon2']
_kinematicvariables += ['muonIndex1','muonIndex2']
_kinematicvariables += ['jetIndex1','jetIndex2']
_kinematicvariables += ['ptHat']
_kinematicvariables += ['CISV_jet1','CISV_jet2']
_kinematicvariables += ['CISV_bjet1','CISV_bjet2']
_kinematicvariables += ['CMVA_jet1','CMVA_jet2']
_kinematicvariables += ['CMVA_bjet1','CMVA_bjet2']
_kinematicvariables += ['isMuonEvent','isElectronEvent']
_kinematicvariables += ['Hj1Matched','Hj2Matched','Zj1Matched','Zj2Matched']
_kinematicvariables += ['Hj1Present','Hj2Present','Zj1Present','Zj2Present']
_kinematicvariables += ['NGenMuonsZ', 'NGenElecsZ']
_kinematicvariables += ['M_uujj_gen', 'M_uujj_genMatched']
_kinematicvariables += ['M_eejj_gen', 'M_eejj_genMatched']
_kinematicvariables += ['M_lljj_gen', 'M_lljj_genMatched']
_kinematicvariables += ['M_uu_gen', 'M_uu_genMatched']
_kinematicvariables += ['bscoreMVA1_genMatched', 'bscoreMVA2_genMatched']
_kinematicvariables += ['CorHj1j2Avail','CorZj1j2Avail']
_kinematicvariables += ['passWptCut','passZptCut','WorZSystemPt']
_kinematicvariables += ['bdt_discrim_M260','bdt_discrim_M270','bdt_discrim_M300','bdt_discrim_M350','bdt_discrim_M400']
_kinematicvariables += ['bdt_discrim_M450','bdt_discrim_M500','bdt_discrim_M550','bdt_discrim_M600','bdt_discrim_M650']
_kinematicvariables += ['bdt_discrim_M750','bdt_discrim_M800','bdt_discrim_M900','bdt_discrim_M1000']
_kinematicvariables += ['bdt_discrims2_M300','bdt_discrims2_M550']
_kinematicvariables += ['bdt_discrims3_low','bdt_discrims3_hig']

_weights = ['scaleWeight_Up','scaleWeight_Down','scaleWeight_R1_F1','scaleWeight_R1_F2','scaleWeight_R1_F0p5','scaleWeight_R2_F1','scaleWeight_R2_F2','scaleWeight_R2_F0p5','scaleWeight_R0p5_F1','scaleWeight_R0p5_F2','scaleWeight_R0p5_F0p5','scaleWeight_R2_F2','weight_amcNLO','weight_nopu','weight_central', 'weight_pu_up', 'weight_pu_down','weight_topPt']
_flagDoubles = ['run_number','event_number','lumi_number']
_flags = ['pass_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ','pass_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ','pass_HLT_Mu17_Mu8','GoodVertexCount']
_flags += ['passPrimaryVertex','passHBHENoiseFilter','passHBHENoiseIsoFilter','passBeamHalo','passTriggerObjectMatching','passDataCert']
_flags += ['passBadEESuperCrystal','passEcalDeadCellTP','passBeamHalo2016','passBadEcalSC','passBadMuon','passBadChargedHadron','badMuonsFlag','duplicateMuonsFlag','noBadMuonsFlag']
#_variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER']
_variations = ['','JESup','JESdown','JER','MESup','MESdown','MER','EESup','EESdown','EER']
if nonisoswitch==True or emuswitch==True or quicktestswitch==True:
	print 'NOT performing systematics...'
	_variations = ['']  # For quicker tests
# _variations = ['']  # For quicker tests



##########################################################################################
#################     Everything needed for Pileup reweighting     #######################
##########################################################################################



def GetPURescalingFactors(puversion):
	# Purpose: To get the pileup reweight factors from the PU_Central.root, PU_Up.root, and PU_Down.root files.
	#         The MC Truth distribution is taken from https://twiki.cern.ch/twiki/bin/view/CMS/PileupMCReweightingUtilities

	#MCDistSummer12 = [2.560E-06, 5.239E-06, 1.420E-05, 5.005E-05, 1.001E-04, 2.705E-04, 1.999E-03, 6.097E-03, 1.046E-02, 1.383E-02, 
        #              1.685E-02, 2.055E-02, 2.572E-02, 3.262E-02, 4.121E-02, 4.977E-02, 5.539E-02, 5.725E-02, 5.607E-02, 5.312E-02, 5.008E-02, 4.763E-02, 
        #              4.558E-02, 4.363E-02, 4.159E-02, 3.933E-02, 3.681E-02, 3.406E-02, 3.116E-02, 2.818E-02, 2.519E-02, 2.226E-02, 1.946E-02, 1.682E-02, 
        #              1.437E-02, 1.215E-02, 1.016E-02, 8.400E-03, 6.873E-03, 5.564E-03, 4.457E-03, 3.533E-03, 2.772E-03, 2.154E-03, 1.656E-03, 1.261E-03, 
        #              9.513E-04, 7.107E-04, 5.259E-04, 3.856E-04, 2.801E-04, 2.017E-04, 1.439E-04, 1.017E-04, 7.126E-05, 4.948E-05, 3.405E-05, 2.322E-05, 
        #              1.570E-05, 5.005E-06]

	#MCDistStartup15 = [4.8551E-07,1.74806E-06,3.30868E-06,1.62972E-05,4.95667E-05,0.000606966,0.003307249,0.010340741,0.022852296,0.041948781,0.058609363,0.067475755,0.072817826,0.075931405,0.076782504,0.076202319,0.074502547,0.072355135,0.069642102,0.064920999,0.05725576,0.047289348,0.036528446,0.026376131,0.017806872,0.011249422,0.006643385,0.003662904,0.001899681,0.00095614,0.00050028,0.000297353,0.000208717,0.000165856,0.000139974,0.000120481,0.000103826,8.88868E-05,7.53323E-05,6.30863E-05,5.21356E-05,4.24754E-05,3.40876E-05,2.69282E-05,2.09267E-05,1.5989E-05,4.8551E-06,2.42755E-06,4.8551E-07,2.42755E-07,1.21378E-07,4.8551E-08]#fixme todo updated to 2015, from https://github.com/cms-sw/cmssw/blob/CMSSW_7_6_X/SimGeneral/MixingModule/python/mix_2015_25ns_Startup_PoissonOOTPU_cfi.py and https://twiki.cern.ch/twiki/bin/view/CMS/PdmVPileUpDescription#Run_2_and_Upgrades

	#MCDistStartup16 = [0.000829312873542,0.00124276120498,0.00339329181587,0.00408224735376,0.00383036590008,0.00659159288946,0.00816022734493,0.00943640833116,0.0137777376066,0.017059392038,0.0213193035468,0.0247343174676,0.0280848773878,0.0323308476564,0.0370394341409,0.0456917721191,0.0558762890594,0.0576956187107,0.0625325287017,0.0591603758776,0.0656650815128,0.0678329011676,0.0625142146389,0.0548068448797,0.0503893295063,0.040209818868,0.0374446988111,0.0299661572042,0.0272024759921,0.0219328403791,0.0179586571619,0.0142926728247,0.00839941654725,0.00522366397213,0.00224457976761,0.000779274977993,0.000197066585944,7.16031761328e-05,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]#Updated to 2016, from https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/SimGeneral/MixingModule/python/mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi.py and https://twiki.cern.ch/twiki/bin/view/CMS/PdmVPileUpDescription#Run_2_and_Upgrades

	MCDistSummer16 = [1.78653e-05 ,2.56602e-05 ,5.27857e-05 ,8.88954e-05 ,0.000109362 ,0.000140973 ,0.000240998 ,0.00071209 ,0.00130121 ,0.00245255 ,0.00502589 ,0.00919534 ,0.0146697 ,0.0204126 ,0.0267586 ,0.0337697 ,0.0401478 ,0.0450159 ,0.0490577 ,0.0524855 ,0.0548159 ,0.0559937 ,0.0554468 ,0.0537687 ,0.0512055 ,0.0476713 ,0.0435312 ,0.0393107 ,0.0349812 ,0.0307413 ,0.0272425 ,0.0237115 ,0.0208329 ,0.0182459 ,0.0160712 ,0.0142498 ,0.012804 ,0.011571 ,0.010547 ,0.00959489 ,0.00891718 ,0.00829292 ,0.0076195 ,0.0069806 ,0.0062025 ,0.00546581 ,0.00484127 ,0.00407168 ,0.00337681 ,0.00269893 ,0.00212473 ,0.00160208 ,0.00117884 ,0.000859662 ,0.000569085 ,0.000365431 ,0.000243565 ,0.00015688 ,9.88128e-05 ,6.53783e-05 ,3.73924e-05 ,2.61382e-05 ,2.0307e-05 ,1.73032e-05 ,1.435e-05 ,1.36486e-05 ,1.35555e-05 ,1.37491e-05 ,1.34255e-05 ,1.33987e-05 ,1.34061e-05 ,1.34211e-05 ,1.34177e-05 ,1.32959e-05 ,1.33287e-05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]# from https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2016Analysis and https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/SimGeneral/MixingModule/python/mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi.py


    # This is the standard (all of 2012) pileup scenario
	if puversion =='Basic':
		f_pu_up = TFile("PU_Up.root","read")
		h_pu_up = f_pu_up.Get('pileup')
		f_pu_down = TFile("PU_Down.root","read")
		h_pu_down = f_pu_down.Get('pileup')
		f_pu_central = TFile("PU_Central.root","read")
		h_pu_central = f_pu_central.Get('pileup')
		#h_pu_up = TFile.Open("PU_Up.root",'read').Get('pileup')
		#h_pu_down = TFile.Open("PU_Down.root",'read').Get('pileup')
		#h_pu_central = TFile("PU_Central.root",'read').Get('pileup')

	# This is just for 2012D. It was used for some studies. Not that important.
	#if puversion =='2012D':
	#	f_pu_up = TFile("PU_Up_2012D.root","read")
	#	h_pu_up = f_pu_up.Get('pileup')
	#	f_pu_down = TFile("PU_Down_2012D.root","read")
	#	h_pu_down = f_pu_down.Get('pileup')
	#	f_pu_central = TFile("PU_Central_2012D.root","read")
	#	h_pu_central = f_pu_central.Get('pileup')
	#	#h_pu_up = TFile.Open("PU_Up_2012D.root").Get('pileup')
	#	#h_pu_down = TFile.Open("PU_Down_2012D.root",'read').Get('pileup')
	#	#h_pu_central = TFile.Open("PU_Central_2012D.root",'read').Get('pileup')

	# Arrays for the central and up/down variation weights.
	bins_pu_central = []
	bins_pu_up = []
	bins_pu_down = []

	# Loop over bins and put content in arrays
	for x in range(h_pu_up.GetNbinsX()):
		bin = x +1
		bins_pu_central.append(h_pu_central.GetBinContent(bin))
		bins_pu_up.append(h_pu_up.GetBinContent(bin))
		bins_pu_down.append(h_pu_down.GetBinContent(bin))

	# Sum bins for proper normalizations
	total_pu_central = sum(bins_pu_central)
	total_pu_up = sum(bins_pu_up)
	total_pu_down = sum(bins_pu_down)
	total_mc = sum(MCDistSummer16)

	# Get normalized bins
	bins_pu_central_norm = [x/total_pu_central for x in bins_pu_central]
	bins_pu_up_norm = [x/total_pu_up for x in bins_pu_up]
	bins_pu_down_norm = [x/total_pu_down for x in bins_pu_down]
	bins_mc_norm  = [x/total_mc for x in MCDistSummer16]

	# Arrays for scale factors (central and systematic varied)
	scale_pu_central = []
	scale_pu_up = []
	scale_pu_down = []

	# Fill arrays of scale factors
	for x in range(len(bins_mc_norm)):
		if bins_mc_norm[x]>0:
			scale_pu_central.append(bins_pu_central_norm[x]/bins_mc_norm[x])
			scale_pu_up.append(bins_pu_up_norm[x]/bins_mc_norm[x])
			scale_pu_down.append(bins_pu_down_norm[x]/bins_mc_norm[x])
		else:
			scale_pu_central.append(1.)
			scale_pu_up.append(1.)
			scale_pu_down.append(1.)

	# Return arrays of scale factors
	return [scale_pu_central, scale_pu_up, scale_pu_down]

# Use the above function to get the pu weights
[CentralWeights,UpperWeights,LowerWeights] =GetPURescalingFactors('Basic')
#[CentralWeights_2012D,UpperWeights_2012D,LowerWeights_2012D] =GetPURescalingFactors('2012D')


##########################################################################################
#################     Everything needed for PDF Weight variation   #######################
##########################################################################################


def GetPDFWeightVars(T):
	# Purpose: Determine all the branch names needed to store the PDFWeights 
	#         for CTEQ, MMTH, and NNPDF in flat (non vector) form. 
	if T.isData:
		return []
	else:
		T.GetEntry(1)
		pdfweights=[]
		#for x in range(len(T.PDFCTEQWeights)):
		#	#if(T.PDFCTEQWeights[x]>-10 and T.PDFCTEQWeights[x]<10): pdfweights.append('factor_cteq_'+str(x+1-53))
		#	if(T.PDFCTEQWeights[x]>-10 and T.PDFCTEQWeights[x]<10): pdfweights.append('factor_cteq_'+str(x+1))
		#for x in range(len(T.PDFMMTHWeights)):
		#	#if(T.PDFMMTHWeights[x]>-10 and T.PDFMMTHWeights[x]<10): pdfweights.append('factor_mmth_'+str(x+1-51))
		#	if(T.PDFMMTHWeights[x]>-10 and T.PDFMMTHWeights[x]<10): pdfweights.append('factor_mmth_'+str(x+1))
		
		for x in range(101):
			pdfweights.append('factor_nnpdf_'+str(x+1))
		#if 'amcatnlo' in amcNLOname :
		#	for x in range(len(T.PDFAmcNLOWeights)):
		#		pdfweights.append('factor_nnpdf_'+str(x+1))
		#else:
		#	for x in range(len(T.PDFNNPDFWeights)):
		#	        #if(T.PDFNNPDFWeights[x]>-10 and T.PDFNNPDFWeights[x]<10): pdfweights.append('factor_nnpdf_'+str(x+1-101))
		#	        #if(T.PDFNNPDFWeights[x]>-10 and T.PDFNNPDFWeights[x]<10): pdfweights.append('factor_nnpdf_'+str(x+1))
		#		if(T.PDFNNPDFWeights[x]>-10 and T.PDFNNPDFWeights[x]<10): pdfweights.append('factor_nnpdf_'+str(x+1))
		return pdfweights


# Get the appropriate numbers of PDF weights from the tree
_pdfweightsnames = GetPDFWeightVars(t)

##########################################################################################
#################         Prepare the Output Tree                  #######################
##########################################################################################

# First create the output file. 
tmpfout = str(randint(100000000,1000000000))+indicator+'.root'
if '/store' in name:
	finalfout = options.dir+'/'+(name.split('/')[-5]+'__'+name.split('/')[-1].replace('.root','_tree.root'))#changed -2 to -5 to get dataset name instead of 0000
else:
	finalfout = options.dir+'/'+name.replace('.root','_tree.root')

# Create the output file and tree "PhysicalVariables"
fout = TFile.Open(tmpfout,"RECREATE")
tout=TTree("PhysicalVariables","PhysicalVariables")


# Below all the branches are created, everything is a double except for flags
# for b in _kinematicvariables:
# 	for v in _variations:
# 		exec(b+v+' = array.array("f",[0])')
# 		exec('tout.Branch("'+b+v+'",'+b+v+',"'+b+v+'/F")' )
# for b in _weights:
# 	exec(b+' = array.array("f",[0])')
# 	exec('tout.Branch("'+b+'",'+b+',"'+b+'/F")' )
# if dopdf:
# 	for b in _pdfweights:
# 		exec(b+' = array.array("f",[0])')
# 		print (b+' = array.array("f",[0])')
# 		exec('tout.Branch("'+b+'",'+b+',"'+b+'/F")' )
# for b in _flags:
# 	exec(b+' = array.array("L",[0])')
# 	exec('tout.Branch("'+b+'",'+b+',"'+b+'/i")' )

Branches = {}
for b in _kinematicvariables:
	for v in _variations:
		Branches[b+v] = array.array("f",[0])
		tout.Branch(b+v,Branches[b+v],b+v+"/F")
for b in _weights:
	Branches[b] = array.array("f",[0])
	tout.Branch(b,Branches[b],b+"/F")
if dopdf:
	for b in _pdfweightsnames:
		Branches[b] = array.array("f",[0])
		tout.Branch(b,Branches[b],b+"/F")
for b in _flagDoubles:
	Branches[b] = array.array("f",[0])
	tout.Branch(b,Branches[b],b+"/F")

for b in _flags:
	Branches[b] = array.array("L",[0])
	tout.Branch(b,Branches[b],b+"/i")

##########################################################################################
#################      Setup BDT discrimator calculation           #######################
##########################################################################################
TMVA.Tools.Instance()
SignalM = ['260','270','300','350','400', '450', '500', '550', '600','650', '750', '800', '900', '1000']

# TMVA.Reader
reader_12vars_set1 = TMVA.Reader("!Color")

# the order of the variables matters, need to be the same as when training
_bdtvars = ['abs(cosThetaStarMu)','Mbb_H','abs(phi0)','Pt_muon1','Pt_muon2','CMVA_bjet1','DR_bb_H','DR_jj_Z','DR_muon1muon2','M_uu4j','M_uu','Mjj_Z']
_bdtvarnames = {}
for vth in _bdtvars:
	_bdtvarnames[vth] = array.array('f',[0])
	reader_12vars_set1.AddVariable(vth, _bdtvarnames[vth])

# TMVA.Reader booked with BDT_classifier, input is .weights.xml file
for ith in range(len(SignalM)):
	reader_12vars_set1.BookMVA(str("BDT_classifier_12vars_set1_M" + SignalM[ith]), str("weights_classification/weights_file_12vars_set1/TMVAClassification_BDT_M" + SignalM[ith] + ".weights.xml"))


# 2nd set of BDTs
reader_13vars_set2 = TMVA.Reader("!Color")
_bdtvars_s2 = ['abs(cosThetaStarMu)','Mbb_H','abs(phi0)','Pt_muon1','Pt_muon2','CMVA_bjet1','DR_jj_Z','DR_muon1muon2','M_uu','Mjj_Z','abs(cosTheta_hbb)','abs(cosTheta_zuu_hzz)','CMVA_bjet2']
_bdtvarnames_s2 = {}
for vth in _bdtvars_s2:
	_bdtvarnames_s2[vth] = array.array('f',[0])
	reader_13vars_set2.AddVariable(vth, _bdtvarnames_s2[vth])

reader_13vars_set2.BookMVA(str("BDT_classifier_13vars_set2_M300"), str("weights_classification/weights_file_13vars_set2/TMVAClassification_BDT_M300.weights.xml"))
reader_13vars_set2.BookMVA(str("BDT_classifier_13vars_set2_M550"), str("weights_classification/weights_file_13vars_set2/TMVAClassification_BDT_M550.weights.xml"))


# 3rd set of BDTs
reader_15vars_set3 = TMVA.Reader("!Color")
_bdtvars_s3 = ['abs(cosThetaStarMu)','Mbb_H','abs(phi0)','Pt_muon1','Pt_muon2','CMVA_bjet1','DR_bb_H','DR_jj_Z','DR_muon1muon2','M_uu','Mjj_Z','abs(cosTheta_hbb)','abs(cosTheta_zuu_hzz)','CMVA_bjet2','DR_uu_bb_H']
_bdtvarnames_s3 = {}
for vth in _bdtvars_s3:
	_bdtvarnames_s3[vth] = array.array('f',[0])
	reader_15vars_set3.AddVariable(vth, _bdtvarnames_s3[vth])

reader_15vars_set3.BookMVA(str("BDT_classifier_15vars_set3_Mlow"), str("weights_classification/weights_file_15vars_set3/TMVAClassification_BDT_Mlow.weights.xml"))
reader_15vars_set3.BookMVA(str("BDT_classifier_15vars_set3_Mhig"), str("weights_classification/weights_file_15vars_set3/TMVAClassification_BDT_Mhig.weights.xml"))

##########################################################################################
#################      Setup bjets energy regression calculation   #######################
##########################################################################################
RegressionReaderBJet1 = TMVA.Reader("!Color")
RegressionReaderBJet2 = TMVA.Reader("!Color")
_regrvars = ['Jet_pt','Jet_corr','Jet_eta','Jet_mt','Jet_leadTrackPt','Jet_leptonPtRel','Jet_leptonPt','Jet_leptonDeltaR','Jet_totHEF','Jet_neEmEF','Jet_vtxPt','Jet_vtxMass','Jet_vtx3dL','Jet_vtxNtrk','Jet_vtx3deL','nPVs','Jet_PFMET','Jet_METDPhi']
_regrvarsnamesBjet1 = {}
_regrvarsnamesBjet2 = {}
for vth in _regrvars:
	_regrvarsnamesBjet1[vth] = array.array('f',[0])
	_regrvarsnamesBjet2[vth] = array.array('f',[0])
	RegressionReaderBJet1.AddVariable(vth, _regrvarsnamesBjet1[vth])
	RegressionReaderBJet2.AddVariable(vth, _regrvarsnamesBjet2[vth])
RegressionReaderBJet1.BookMVA("BDTG method", "weights_classification/BDTG_16plus2_jetGenJet_nu_7_6.weights.xml")
RegressionReaderBJet2.BookMVA("BDTG method", "weights_classification/BDTG_16plus2_jetGenJet_nu_7_6.weights.xml")

##########################################################################################
#################           SPECIAL FUNCTIONS FOR ANALYSIS         #######################
##########################################################################################

def PrintBranchesAndExit(T):
	# Purpose: Just list the branches on the input file and bail out. 
	#         For coding and debugging
	x = T.GetListOfBranches()
	for n in x:
		print n
	sys.exit()

# PrintBranchesAndExit(t)

#def parseRLElist(triples):
#	parsedTriples = []
#	tempTrips = []
#	_runs = []
#	_le = []
#	i = 0
#	for trip in triples :
#		[_r,_l,_e] = [trip[0],trip[1],trip[2]]
#		print [_r,_l,_e]
#		_runs.append[_r]
#		if triples[i+1][0] not in _runs :
#			_le.append([_l,_e])
#			parsedTriples.append([r,_le])
#			_le = []		
#		else :
#			_le.append([_l,_e])
#		i = i+1
#	print parsedTriples
#	return parsedTriples
#	
def GetRunLumiEventListNew(fileName):
	#n=0
	#Purpose: parse a met filter event list to get a BAD list of run:lumi:event.  For real data only
	mfile = open(fileName,'r')
	run=''
	lumi=''
	event=''
	triples=[]
	for lines in mfile :
		triple=[]
		line=lines.replace('\n','')
		line=line.split(':')
		exec('run = '+line[0])
		exec('lumi = '+line[1])
		exec('event = '+line[2])
		triple.append(run)
		triple.append(lumi)
		triple.append(event)
		triples.append(triple)
		#print triple
		#print n
		#n=n+1
	parsedTriples = []
	tempTrips = []
	_runs = []
	_le = []
	i = 0
	N = len(triples)
	for trip in triples :
		[_r,_l,_e] = [trip[0],trip[1],trip[2]]
		if _r not in _runs:
			_runs.append(_r)
		if i<N-2 :
			if triples[i+1][0] not in _runs :
				_le.append([_l,_e])
				parsedTriples.append([_r,_le])
				#print _r,_le
				_le = []
				i = i+1		
			else :
				_le.append([_l,_e])
				i = i+1
				#if i%10000 == 0 :
					#print i
			if i==N-2 :
				_le.append([_l,_e])
				parsedTriples.append([_r,_le])
	#print 'DONE',parsedTriples
	return parsedTriples

def GetRunLumiEventList(fileName):
	#n=0
	#Purpose: parse a met filter event list to get a BAD list of run:lumi:event.  For real data only
	global options
	mfile = open(fileName,'r')
	run=''
	lumi=''
	event=''
	triples=[]
	for line in mfile :
		#print line
		triple=[]
		line=line.split(':')
		exec('run = '+line[0])
		exec('lumi = '+line[1])
		exec('event = '+line[2])
		triple.append(run)
		triple.append(lumi)
		triple.append(event)
		triples.append(triple)
		#print triple
		#print n
		#n=n+1
	return triples

#BadMuonRunLumiEventsNew = GetRunLumiEventListNew('muonBadTrack.txt')

def CheckBadRunLumiEventNew(badEvents,r,l,e,isData):
	#Purpose: Use the BadBeamHaloRunLumiEvents list, to check and see if a given event
	#         is flagged as beam halo
	#for _rle in BadBeamHaloRunLumiEvents :
	if isData == True:
		#print 'before looping'
		for _rle in badEvents :
		#print _rle[0],_rle[1],_rle[2]
			#print 'before run'
			#print _rle[0]
			#print name,r,_rle[0]
			if _rle[0]==r :
				#print 'before lumi'
				for _le in _rle[1] :
					#print r,l,e
					#print '  ',_rle[0],_le[0],_le[1]
					if _le[0]==l :
					#print 'before event'
						if _le[1]==e :
							return False
		return True
	else :
		return True

def CheckBadRunLumiEvent(badEvents,r,l,e,isData):
	#Purpose: Use the BadBeamHaloRunLumiEvents list, to check and see if a given event
	#         is flagged as beam halo
	#for _rle in BadBeamHaloRunLumiEvents :
	if isData == True:
		for _rle in badEvents :
		#print _rle[0],_rle[1],_rle[2]
			#print 'before run'
			if _rle[0]==r :
				#print 'before lumi'
				if _rle[1]==l :
					#print 'before event'
					if _rle[2]==e :
						return False
		return True
	else :
		return True

def GetRunLumiList():
	# Purpose: Parse the json file to get a list of good runs and lumis 
	#          to call on later. For real data only.
	jfile = open(options.json,'r')	
	flatjson = ''
	for line in jfile:
		flatjson+=line.replace('\n','')
	flatjson = flatjson.replace("}","")
	flatjson = flatjson.replace("{","")
	flatjson = flatjson.replace(":","")
	flatjson = flatjson.replace(" ","")
	flatjson = flatjson.replace("\t","")

	jinfo = flatjson.split('"')
	strjson = ''
	for j in jinfo:
		strjson += j
	strjson = strjson.replace('\n[',' [')
	strjson = strjson.replace(']],',']]\n')
	strjson = strjson.replace('[[',' [[')

	pairs = []
	for line in strjson.split('\n'):
		pair = []
		line = line.split(' ')
		exec('arun = '+line[0])
		exec('alumis = '+line[1])
		verboselumis = []
		for r in alumis:
			verboselumis +=  range(r[0],r[1]+1)

		pair.append(arun)
		pair.append(verboselumis)
		pairs.append(pair)
	return pairs

GoodRunLumis = GetRunLumiList()

def CheckRunLumiCert(r,l):
	# Purpose: Use the GoodRunLumis list, to check and see if a given
	#          run and lumi (r and l) are in the list. 
	for _rl in GoodRunLumis:
		if _rl[0]==r:
			for _l in _rl[1]:
				if _l == l:
					return True
	return False
def TransMass(p1,p2):
	# Purpose: Simple calculation of transverse mass between two TLorentzVectors
	return math.sqrt( 2*p1.Pt()*p2.Pt()*(1-math.cos(p1.DeltaPhi(p2))) )

def InvMass(particles):
	# Purpose: Simple calculation of invariant mass between two TLorentzVectors	
	output=particles
	return (p1+p2).M()

def ST(particles):
	# Purpose: Calculation of the scalar sum of PT of a set of TLorentzVectors	
	st = 0.0
	for p in particles:
		st += p.Pt()
	return st

def PassTrigger(T,trigger_identifiers,prescale_threshold):
	# Purpose: Return a flag (1 or 0) to indicate whether the event passes any trigger
	#         which is syntactically matched to a set of strings trigger_identifiers,
	#         considering only triggers with a prescale <= the prescale threshold.	
	for n in range(len(T.HLTInsideDatasetTriggerNames)):
		name = T.HLTInsideDatasetTriggerNames[n]
		consider_trigger=True
		for ident in trigger_identifiers:
			if ident not in name:
				consider_trigger=False
		if (consider_trigger==False) : continue

		prescale = T.HLTInsideDatasetTriggerPrescales[n]

		if prescale > prescale_threshold:
			consider_trigger=False
		if (consider_trigger==False) : continue

		decision = bool(T.HLTInsideDatasetTriggerDecisions[n])
		if decision==True:
			return 1
	return 0	

def CountVertices(T):
	vertices = 0
	for v in range(len(T.VertexZ)):
		if ( T.VertexIsFake[v] == True ) :  continue
		if ( T.VertexNDF[v] <= 4.0 ) :  continue
		if ( abs(T.VertexZ[v]) > 24.0 ) :  continue
		if ( abs(T.VertexRho[v]) >= 2.0 ) :  continue
		vertices += 1
	return vertices	

def GetPUWeight(T,version,puversion):
	# Purpose: Get the pileup weight for an event. Version can indicate the central
	#         weight, or the Upper or Lower systematics. Needs to be updated for
	#         input PU histograms given only the generated disribution........	

	# Only necessary for MC
	if T.isData:
		return 1.0

	# Getting number of PU interactions, start with zero.	
	N_pu = 0

	# Set N_pu to number of true PU interactions in the central bunch
	for n in range(len(T.PileUpInteractionsTrue)):
		if abs(T.PileUpOriginBX[n]==0):
			N_pu = int(1.0*(T.PileUpInteractionsTrue[n]))

	puweight = 0

	# Assign the list of possible PU weights according to what is being done
	# Central systematics Up, or systematic down
	if puversion=='Basic':
		puweights = CentralWeights
		if version=='SysUp':
			puweights=UpperWeights
		if version=='SysDown':
			puweights=LowerWeights

	# Also possible to do just for 2012D, for cross-checks. 
	#if puversion=='2012D':
	#	puweights = CentralWeights_2012D
	#	if version=='SysUp':
	#		puweights=UpperWeights_2012D
	#	if version=='SysDown':
	#		puweights=LowerWeights_2012D


	# Make sure there exists a weight for the number of interactions given, 
	# and set the puweight to the appropriate value.
	NRange = range(len(puweights))
	if N_pu in NRange:
		puweight=puweights[N_pu]
	# print puweight
	return puweight



def GetPDFWeights(T):
	# Purpose: Gather the pdf weights into a single list. 	
	_allweights = []
	#for x in range(len(T.PDFCTEQWeights)):
	#	if(T.PDFCTEQWeights[x]>-10 and T.PDFCTEQWeights[x]<10): _allweights.append(T.PDFCTEQWeights[x])
	#for x in range(len(T.PDFMMTHWeights)):
	#	if(T.PDFMMTHWeights[x]>-10 and T.PDFMMTHWeights[x]<10): _allweights.append(T.PDFMMTHWeights[x])
	extras=0
	if 'amcatnlo' in amcNLOname :
		for x in range(len(T.PDFNNPDFWeightsAMCNLO)):
			_allweights.append(T.PDFNNPDFWeightsAMCNLO[x]/T.PDFNNPDFWeightsAMCNLO[0])
		extras = 101-len(T.PDFNNPDFWeightsAMCNLO)
	else:
		for x in range(len(T.PDFNNPDFWeights)):
		        #if(T.PDFNNPDFWeights[x]>-10 and T.PDFNNPDFWeights[x]<10): _allweights.append(T.PDFNNPDFWeights[x])
			_allweights.append(T.PDFNNPDFWeights[x])
		extras = 101-len(T.PDFNNPDFWeights)
	for x in range(extras):
		_allweights.append(1.0)
	return _allweights


def MuonsFromLQ(T):
	# Purpose: Testing. Get the muons from LQ decays and find the matching reco muons. 
	#         Return TLorentzVectors of the gen and reco muons, and the indices for
	#         the recomuons as well.
	muons = []
	genmuons=[]
	recomuoninds = []
	for n in range(len(T.MuonPt)):	
		m = TLorentzVector()
		m.SetPtEtaPhiM(T.MuonPt[n],T.MuonEta[n],T.MuonPhi[n],0)
		muons.append(m)
	for n in range(len(T.GenParticlePdgId)):
		pdg = T.GenParticlePdgId[n]
		if pdg not in [13,-13]:
			continue
		motherIndex = T.GenParticleMotherIndex[n]
		
		motherid = 0
		if motherIndex>-1:
			motherid = T.GenParticlePdgId[motherIndex]
			#print 'pdgId:',pdg,'index:',T.GenParticleMotherIndex[n],'mother pdgId:',T.GenParticlePdgId[motherIndex]
		if motherid not in [42,-42]:
			continue	
		m = TLorentzVector()
		m.SetPtEtaPhiM(T.GenParticlePt[n],T.GenParticleEta[n],T.GenParticlePhi[n],0.0)
		genmuons.append(m)
	
	matchedrecomuons=[]
	emptyvector = TLorentzVector()
	emptyvector.SetPtEtaPhiM(0,0,0,0)
	#print 'number of genmuons:',len(genmuons)
	for g in genmuons:
		bestrecomuonind=-1
		mindr = 99999
		ind=-1
		for m in muons:
			ind+=1
			dr = abs(m.DeltaR(g))
			if dr<mindr:
				mindr =dr
				bestrecomuonind=ind
		if mindr<0.4:
			matchedrecomuons.append(muons[bestrecomuonind])
			recomuoninds.append(bestrecomuonind)
		else:
			matchedrecomuons.append(emptyvector)
			recomuoninds.append(-99)
		#print mindr, muons[bestrecomuonind].Pt(), g.Pt()
	while len(recomuoninds)<2 :
		recomuoninds.append(-99)
	return([genmuons,matchedrecomuons,recomuoninds])
	#return(recomuoninds)

def JetsFromLQ(T):
	# Purpose: Testing. Get the quarks from LQ decays and find the matching reco pfJets. 
	#         Return TLorentzVectors of the gen and reco jets, and the indices for
	#         the recojets as well.
	jets = []
	genjets=[]
	recojetinds = []
	for n in range(len(T.PFJetPtAK4CHS)):	
		if  T.PFJetPassLooseIDAK4CHS[n]==1 and T.PFJetPtAK4CHS[n]>30 and abs(T.PFJetEtaAK4CHS[n])<2.4 : #morse only use jets that pass id
			m = TLorentzVector()
			m.SetPtEtaPhiM(T.PFJetPtAK4CHS[n],T.PFJetEtaAK4CHS[n],T.PFJetPhiAK4CHS[n],0)
			jets.append(m)
	for n in range(len(T.GenParticlePdgId)):
		pdg = T.GenParticlePdgId[n]
		if pdg not in [4,-4]: #Get charm quarks
			continue
		motherIndex = T.GenParticleMotherIndex[n]
		motherid = 0
		if motherIndex>-1:
			motherid = T.GenParticlePdgId[motherIndex]
		if motherid not in [42,-42]:
			continue	
		m = TLorentzVector()
		m.SetPtEtaPhiM(T.GenParticlePt[n],T.GenParticleEta[n],T.GenParticlePhi[n],0.0)
		genjets.append(m)
	
	matchedrecojets=[]
	emptyvector = TLorentzVector()
	emptyvector.SetPtEtaPhiM(0,0,0,0)
	for g in genjets:
		bestrecojetind=-1
		mindr = 99999
		ind=-1
		for m in jets:
			ind+=1
			dr = abs(m.DeltaR(g))
			if dr<mindr:
				mindr =dr
				bestrecojetind=ind
		if mindr<0.6:
			matchedrecojets.append(jets[bestrecojetind])
			recojetinds.append(bestrecojetind)
		else:
			matchedrecojets.append(emptyvector)
			recojetinds.append(-99)
		#print mindr, jets[bestrecojetind].Pt(), g.Pt()
	while len(recojetinds)<2 :
		recojetinds.append(-99)
	return([genjets,matchedrecojets,recojetinds])
	#return(recojetinds)

def LeptonsAndJetsFromHH(T):
	# Purpose: Testing. HH. Get the muons from Z decays (on and off shell) and find the matching reco muons. 
	#         Return TLorentzVectors of the gen and reco muons, and the indices for
	#         the recomuons as well.
	muons = []
	genmuons=[]
	recomuoninds = []
	electrons = []
	genelectrons=[]
	recoelectroninds = []
	onShellZMu=False
	onShellZEle=False
	for n in range(len(T.MuonPt)):
		m = TLorentzVector()
		m.SetPtEtaPhiM(T.MuonPt[n],T.MuonEta[n],T.MuonPhi[n],0)
		muons.append(m)
	for n in range(len(T.GenParticlePdgId)):
		pdg = T.GenParticlePdgId[n]
		if pdg not in [13,-13]:
			continue
		motherIndex = T.GenParticleMotherIndex[n]
		
		motherid = 0
		if motherIndex>-1:
			motherid = T.GenParticlePdgId[motherIndex]
		#if v=='': print 'pdgId:',pdg,'mother index:',T.GenParticleMotherIndex[n],'muStatus:',T.GenParticleStatus[n],'mother pdgId:',T.GenParticlePdgId[motherIndex], 'mu pt', T.GenParticlePt[n]
		if motherid not in [23,-23,25,-25]:
			continue
		if motherid in [23,-23]: onShellZMu=True
		#elif v=='': print 'Muon not from Z???  muStatus:',T.GenParticleStatus[n],'  Muparent:',motherid

		# AH: here we keep also gmuon status 23 and status 1, of which mother 25. But we do not keep muon status 1 of which mother is 13, -13
		m = TLorentzVector()
		m.SetPtEtaPhiM(T.GenParticlePt[n],T.GenParticleEta[n],T.GenParticlePhi[n],0.0)
		genmuons.append(m)
		#if v=='': print ' gen muon pt ', m.Pt(), 'eta', m.Eta()
	
	matchedrecomuons=[]
	matchedrecoelectrons=[]
	emptyvector = TLorentzVector()
	emptyvector.SetPtEtaPhiM(0,0,0,0)
	#print 'number of genmuons:',len(genmuons)
	for g in genmuons:
		bestrecomuonind=-1
		mindr = 99999
		ind=-1
		for m in muons:
			ind+=1
			dr = abs(m.DeltaR(g))
			if dr<mindr:
				mindr =dr
				bestrecomuonind=ind
		if mindr<0.4:
			matchedrecomuons.append(muons[bestrecomuonind])
			recomuoninds.append(bestrecomuonind)
		else:
			matchedrecomuons.append(emptyvector)
			recomuoninds.append(-99)
		#print 'dr', mindr, 'pt', muons[bestrecomuonind].Pt(), g.Pt(), 'eta', muons[bestrecomuonind].Eta(), g.Eta(), 'phi', muons[bestrecomuonind].Phi(), g.Phi()
	while len(recomuoninds)<2 :
		recomuoninds.append(-99)
	#return([genmuons,matchedrecomuons,recomuoninds])
	#return(recomuoninds)

	for n in range(len(T.ElectronPt)):	
		m = TLorentzVector()
		m.SetPtEtaPhiM(T.ElectronPt[n],T.ElectronEta[n],T.ElectronPhi[n],0)
		electrons.append(m)
	for n in range(len(T.GenParticlePdgId)):
		pdg = T.GenParticlePdgId[n]
		if pdg not in [11,-11]:
			continue
		motherIndex = T.GenParticleMotherIndex[n]
		
		motherid = 0
		if motherIndex>-1:
			motherid = T.GenParticlePdgId[motherIndex]
			#print 'pdgId:',pdg,'index:',T.GenParticleMotherIndex[n],'mother pdgId:',T.GenParticlePdgId[motherIndex]
		if motherid not in [23,-23,25,-25]:
			continue
		if motherid in [23,-23]: onShellZEle=True
		#elif v=='': print 'Electron not from Z???  Eleparent:',motherid
		m = TLorentzVector()
		m.SetPtEtaPhiM(T.GenParticlePt[n],T.GenParticleEta[n],T.GenParticlePhi[n],0.0)
		genelectrons.append(m)
	
	#if v=='':print 'onShellZMu:',onShellZMu,'onShellZEle:',onShellZEle
	#if v == '':print 'number of genmuons:',len(genmuons),'number of genelectrons:',len(genelectrons)

	matchedrecoelectrons=[]
	emptyvector = TLorentzVector()
	emptyvector.SetPtEtaPhiM(0,0,0,0)
	#if v == '': print 'number of genelectrons:',len(genelectrons)
	for g in genelectrons:
		bestrecoelectronind=-1
		mindr = 99999
		ind=-1
		for m in electrons:
			ind+=1
			dr = abs(m.DeltaR(g))
			if dr<mindr:
				mindr =dr
				bestrecoelectronind=ind
		if mindr<0.4:
			matchedrecoelectrons.append(electrons[bestrecoelectronind])
			recoelectroninds.append(bestrecoelectronind)
		else:
			matchedrecoelectrons.append(emptyvector)
			recoelectroninds.append(-99)
		#print mindr, electrons[bestrecoelectronind].Pt(), g.Pt()
	while len(recoelectroninds)<2 :
		recoelectroninds.append(-99)
	# Purpose: Testing. HH. Get the quarks from H and Z decays (on and off shell) and find the matching reco pfJets. 
	#         Return TLorentzVectors of the gen and reco jets, and the indices for
	#         the recojets as well.
	jetsZ = []
	genjetsZ=[]
	recojetindsZ = []
	recojetOriIndsZ = []
	jetsH = []
	genjetsH=[]
	recojetindsH = []
	recojetOriIndsH = []
	genjetsZH = []
	if onShellZMu or onShellZEle: 
		#parentParticles = [25,-25]
		daughterJets = [1,2,3,4,5,-5,-4,-3,-2,-1] #Get charm quarks
	if not (onShellZMu or onShellZEle)  : 
		#parentParticles = [23,-23]
		daughterJets = [1,2,3,4,5,-5,-4,-3,-2,-1] #Get all quark flavors
	for n in range(len(T.PFJetPtAK4CHS)):
		#if v == '': print 'reco jet pt', T.PFJetPtAK4CHS[n],'eta',T.PFJetEtaAK4CHS[n],'btagScore',T.PFJetCombinedInclusiveSecondaryVertexBTagAK4CHS[n],'index', n
		#if  T.PFJetPassLooseIDAK4CHS[n]==1 and T.PFJetPtAK4CHS[n]>15 and abs(T.PFJetEtaAK4CHS[n])<2.4 : #morse only use jets that pass id #fixme loosening to study HH
		#if  T.PFJetPassLooseIDAK4CHS[n]==1 and T.PFJetPtAK4CHS[n]>20 and abs(T.PFJetEtaAK4CHS[n])<2.4 :
		if True :
			m = TLorentzVector()
			m.SetPtEtaPhiM(T.PFJetPtAK4CHS[n],T.PFJetEtaAK4CHS[n],T.PFJetPhiAK4CHS[n],0)
			jetsZ.append(m)
			jetsH.append(m)
			recojetOriIndsZ.append(n)
			recojetOriIndsH.append(n)
	for n in range(len(T.GenParticlePdgId)):
		pdg = T.GenParticlePdgId[n]
		if pdg not in daughterJets:
			continue
		motherIndex = T.GenParticleMotherIndex[n]
		[motherid,motherStatus,grandMotherid] = [0,0,0]
		if motherIndex>-1:
			motherid = T.GenParticlePdgId[motherIndex]
			motherStatus = T.GenParticleStatus[motherIndex]
			grandMotherid = T.GenParticlePdgId[T.GenParticleMotherIndex[motherIndex]]
			#if parent=='Z' : print 'daughter:',pdg,'  mother:',motherid, '  grandMother:',grandMotherid
			#if v=='' : print 'daughter:',pdg,'  Status:',T.GenParticleStatus[n],'  mother:',motherid,'  grandMother:',grandMotherid

		if motherid not in [23,-23,25,-25] :#parentParticles:
			continue	
		m = TLorentzVector()
		m.SetPtEtaPhiM(T.GenParticlePt[n],T.GenParticleEta[n],T.GenParticlePhi[n],0.0)
		#if v == '':print 'Qaurk jet:',pdg,'  mother:',motherid, ' onShellZLep ', (onShellZMu or onShellZEle), '  status:',T.GenParticleStatus[n],'pt',m.Pt(),'eta',m.Eta(),'phi',m.Phi()
		if not (onShellZMu or onShellZEle) :
			#if v == '':print ' Not onShellZ','jet:',pdg,'  mother:',motherid,'  status:',T.GenParticleStatus[n],'pt',m.Pt(),'eta',m.Eta()
			if motherid in [23,-23] : genjetsZ.append(m)
			if motherid in [25,-25] : genjetsH.append(m)
		if onShellZMu or onShellZEle :
			#if v == '':print ' onShellZ','jet:',pdg,'  mother:',motherid,'  status:',T.GenParticleStatus[n],'pt',m.Pt(),'eta',m.Eta()
			genjetsZH.append(m)
		
	if onShellZMu or onShellZEle or len(genjetsH)>=4:
		genjetsZnew,genjetsHnew = [],[]

		if len(genjetsZH)>=4:
			mass1 = abs(125.-(genjetsZH[0]+genjetsZH[1]).M())
			mass2 = abs(125.-(genjetsZH[0]+genjetsZH[2]).M())
			mass3 = abs(125.-(genjetsZH[0]+genjetsZH[3]).M())
			mass4 = abs(125.-(genjetsZH[1]+genjetsZH[2]).M())
			mass5 = abs(125.-(genjetsZH[1]+genjetsZH[3]).M())
			mass6 = abs(125.-(genjetsZH[2]+genjetsZH[3]).M())
			minMass = min(mass1,mass2,mass3,mass4,mass5,mass6)
			if mass1 == minMass: [h1,h2,z1,z2]=[0,1,2,3]
			if mass2 == minMass: [h1,h2,z1,z2]=[0,2,1,3]
			if mass3 == minMass: [h1,h2,z1,z2]=[0,3,1,2]
			if mass4 == minMass: [h1,h2,z1,z2]=[1,2,0,3]
			if mass5 == minMass: [h1,h2,z1,z2]=[1,3,0,2]
			if mass6 == minMass: [h1,h2,z1,z2]=[2,3,0,1]
			genjetsHnew.append(genjetsZH[h1])
			genjetsHnew.append(genjetsZH[h2])
			genjetsZnew.append(genjetsZH[z1])
			genjetsZnew.append(genjetsZH[z2])
		elif len(genjetsH)>=4:
			genjetsZH=genjetsH
			mass1 = abs(125.-(genjetsZH[0]+genjetsZH[1]).M())
			mass2 = abs(125.-(genjetsZH[0]+genjetsZH[2]).M())
			mass3 = abs(125.-(genjetsZH[0]+genjetsZH[3]).M())
			mass4 = abs(125.-(genjetsZH[1]+genjetsZH[2]).M())
			mass5 = abs(125.-(genjetsZH[1]+genjetsZH[3]).M())
			mass6 = abs(125.-(genjetsZH[2]+genjetsZH[3]).M())
			minMass = min(mass1,mass2,mass3,mass4,mass5,mass6)
			if mass1 == minMass: [h1,h2,z1,z2]=[0,1,2,3]
			if mass2 == minMass: [h1,h2,z1,z2]=[0,2,1,3]
			if mass3 == minMass: [h1,h2,z1,z2]=[0,3,1,2]
			if mass4 == minMass: [h1,h2,z1,z2]=[1,2,0,3]
			if mass5 == minMass: [h1,h2,z1,z2]=[1,3,0,2]
			if mass6 == minMass: [h1,h2,z1,z2]=[2,3,0,1]
			genjetsHnew.append(genjetsZH[h1])
			genjetsHnew.append(genjetsZH[h2])
			genjetsZnew.append(genjetsZH[z1])
			genjetsZnew.append(genjetsZH[z2])

		genjetsZ,genjetsH = genjetsZnew,genjetsHnew
					
	matchedrecojetsZ=[]
	matchedrecojetsH=[]
	emptyvector = TLorentzVector()
	emptyvector.SetPtEtaPhiM(0,0,0,0)
	#if not (onShellZMu or onShellZEle) :
	if True :
		usedHjetsInd = []
		for g in genjetsH:
			bestrecojetind=-1
			mindr = 99999
			ind=-1
			for m in jetsH:
				ind+=1
				if abs(T.PFJetPartonFlavourAK4CHS[recojetOriIndsH[ind]]) != 5 : continue
				#if v == '': print 'ind in jetsH', ind ,'reco idex', recojetOriIndsH[ind], 'flavor', T.PFJetPartonFlavourAK4CHS[recojetOriIndsH[ind]]
				skip = False
				for indc in range(len(usedHjetsInd)):
					if ind == usedHjetsInd[indc]:
						skip = True
						#if v == '':print ' >> skip ind in jetsH', ind
						continue
				if skip: continue
				dr = abs(m.DeltaR(g))
				#if v == '':print 'ind in jetsH', ind ,'DeltaR:',dr, ' >> gen pt eta', g.Pt(),g.Eta(),' >> reco pt eta', m.Pt(),m.Eta(), 'dr', dr
				if dr<mindr:
					mindr =dr
					bestrecojetind=ind
			if mindr<0.5: # was 0.6
				matchedrecojetsH.append(jetsH[bestrecojetind])
				recojetindsH.append(recojetOriIndsH[bestrecojetind])
				usedHjetsInd.append(bestrecojetind)
				#recojetindsH.append(bestrecojetind)
			else:
				matchedrecojetsH.append(emptyvector)
				recojetindsH.append(-99)
			#if v == '':print 'Done this genjetsH with bestrecojetind', bestrecojetind , 'mindr:',mindr, 'len(usedHjetsInd)', len(usedHjetsInd)
		while len(recojetindsH)<2 :
			recojetindsH.append(-99)

		usedZjetsInd = []
		for g in genjetsZ:
			bestrecojetind=-1
			mindr = 99999
			ind=-1
			for m in jetsZ:
				ind+=1
				skip = False
				for indc in range(len(usedZjetsInd)):
					#if v == '':print 'indc', indc, 'jetind stored in usedZjetsInd', usedZjetsInd[indc]
					if ind == usedZjetsInd[indc]:
						skip = True
						#if v == '':print ' >> skip ind in jetsZ', ind
						continue
				for indc in range(len(usedHjetsInd)):
					if ind == usedHjetsInd[indc]:
						skip = True
						continue
				if skip: continue
				dr = abs(m.DeltaR(g))
				#if v == '':print 'ind in jetsZ', ind ,'DeltaR:',dr, ' >> gen pt eta', g.Pt(),g.Eta(),' >> reco pt eta', m.Pt(),m.Eta(), 'dr', dr
				if dr<mindr:
					mindr =dr
					bestrecojetind=ind
			if mindr<0.6:
				matchedrecojetsZ.append(jetsZ[bestrecojetind])
				recojetindsZ.append(recojetOriIndsZ[bestrecojetind])
				usedZjetsInd.append(bestrecojetind)
				#recojetindsZ.append(bestrecojetind)
			else:
				matchedrecojetsZ.append(emptyvector)
				recojetindsZ.append(-99)
			#if v == '':print 'Done this genjetsZ with bestrecojetind', bestrecojetind , 'mindr:',mindr, 'len(usedZjetsInd)', len(usedZjetsInd)
		while len(recojetindsZ)<2 :
			recojetindsZ.append(-99)

	# the following are not futher used, I still do not know what is it doing but will look into it.
	hjet1,hjet2,zjet1,zjet2 = -1,-1,-1,-1
	for hJet in matchedrecojetsH :
		for n in range(len(T.PFJetPtAK4CHS)) :
			if abs(hJet.Pt()-T.PFJetPtAK4CHS[n])<0.01 and  abs(hJet.Eta()-T.PFJetEtaAK4CHS[n])<0.01 :
				if hjet1 < 0 : hjet1 = n
				else : hjet2 = n
	for zJet in matchedrecojetsZ :
		for n in range(len(T.PFJetPtAK4CHS)) :
			if abs(zJet.Pt()-T.PFJetPtAK4CHS[n])<0.01 and  abs(zJet.Eta()-T.PFJetEtaAK4CHS[n])<0.01 :
				if zjet1 < 0 : zjet1 = n
	"""			else : zjet2 = n
	if v=='':
		h1,h2,z1,z2 = TLorentzVector(),TLorentzVector(),TLorentzVector(),TLorentzVector()
		h1.SetPtEtaPhiM(T.PFJetPtAK4CHS[hjet1],T.PFJetEtaAK4CHS[hjet1],T.PFJetPhiAK4CHS[hjet1],0)
		h2.SetPtEtaPhiM(T.PFJetPtAK4CHS[hjet2],T.PFJetEtaAK4CHS[hjet2],T.PFJetPhiAK4CHS[hjet2],0)
		z1.SetPtEtaPhiM(T.PFJetPtAK4CHS[zjet1],T.PFJetEtaAK4CHS[zjet1],T.PFJetPhiAK4CHS[zjet1],0)
		z2.SetPtEtaPhiM(T.PFJetPtAK4CHS[zjet2],T.PFJetEtaAK4CHS[zjet2],T.PFJetPhiAK4CHS[zjet2],0)
		print 'jet indices (h1, h2, z1, z2):',hjet1,hjet2,zjet1,zjet2
		print 'masses                (h, z):',(h1+h2).M(),(z1+z2).M()
		print 'pt          (h1, h2, z1, z2):',T.PFJetPtAK4CHS[hjet1],T.PFJetPtAK4CHS[hjet2],T.PFJetPtAK4CHS[zjet1],T.PFJetPtAK4CHS[zjet2]
		print 'btags       (h1, h2, z1, z2):',T.PFJetCombinedInclusiveSecondaryVertexBTagAK4CHS[hjet1],T.PFJetCombinedInclusiveSecondaryVertexBTagAK4CHS[hjet2],T.PFJetCombinedInclusiveSecondaryVertexBTagAK4CHS[zjet1],T.PFJetCombinedInclusiveSecondaryVertexBTagAK4CHS[zjet2]
		print ''
	"""

	"""
	if v == '':
		for i in range(len(genjetsH)) :
			print 'H: genpt',genjetsH[i].Pt(),'geneta',genjetsH[i].Eta(),'recopt',matchedrecojetsH[i].Pt(),'recoeta',matchedrecojetsH[i].Eta(),'index',recojetindsH[i]
		for i in range(len(genjetsZ)) :
			print 'Z: genpt',genjetsZ[i].Pt(),'geneta',genjetsZ[i].Eta(),'recopt',matchedrecojetsZ[i].Pt(),'recoeta',matchedrecojetsZ[i].Eta(),'index',recojetindsZ[i]
	"""
	while len(genmuons)<2:
		genmuons.append(emptyvector)
	while len(genelectrons)<2:
		genelectrons.append(emptyvector)
	while len(genjetsH)<2:
		genjetsH.append(emptyvector)
	while len(genjetsZ)<2:
		genjetsZ.append(emptyvector)
	while len(matchedrecomuons)<2:
		matchedrecomuons.append(emptyvector)
	while len(matchedrecoelectrons)<2:
		matchedrecoelectrons.append(emptyvector)
	while len(matchedrecojetsH)<2:
		matchedrecojetsH.append(emptyvector)
	while len(matchedrecojetsZ)<2:
		matchedrecojetsZ.append(emptyvector)

	return([genmuons,matchedrecomuons,recomuoninds,genelectrons,matchedrecoelectrons,recoelectroninds,genjetsH,matchedrecojetsH,recojetindsH,genjetsZ,matchedrecojetsZ,recojetindsZ,onShellZMu,onShellZEle])
	#return(recojetinds)


def PropagatePTChangeToMET(met,original_object,varied_object):
	# Purpose: This takes an input TLorentzVector met representing the missing ET
	#         (no eta component), and an original object (arg 2), which has been
	#         kinmatically modified for a systematic (arg 3), and modifies the 
	#         met to compensate for the change in the object.
	return  met + varied_object - original_object

def MediumIDMuons(T,_met,variation,isdata):
	# Purpose: Gets the collection of muons passing medium muon ID. 
	#         Returns muons as TLorentzVectors, and indices corrresponding
	#         to the surviving muons of the muon collection. 
	#         Also returns modified MET for systematic variations.
	muons = []
	muoninds = []
	if variation=='MESup':	
		#_MuonPt = [(pt + pt*(0.05*pt/1000.0)) for pt in T.MuonPt]#original
		_MuonPt = [(pt + pt*(0.10*pt/1000.0)) for pt in T.MuonPt]#updated to Zprime 13TeV study number
	elif variation=='MESdown':	
		#_MuonPt = [(pt - pt*(0.05*pt/1000.0)) for pt in T.MuonPt]
		_MuonPt = [(pt - pt*(0.10*pt/1000.0)) for pt in T.MuonPt]
	elif variation=='MER':	
		_MuonPt = [pt+pt*tRand.Gaus(0.0,  0.01*(pt<=200.0) + (0.04)*(pt>200.0) ) for pt in T.MuonPt]
	else:	
		_MuonPt = [pt for pt in T.MuonPt]	

	if (isdata):
		_MuonPt = [pt for pt in T.MuonPt]	

	trk_isos = []
	charges = []
	deltainvpts = []

	chi2 = []
	pfid = []
	layers = []

	nequiv = []
	for n in range(len(T.MuonPt)):
		#if T.MuonIsGlobal[n] or newntupleswitch==True: #not necessary anymore - global muon requirement encompassed later
		nequiv.append(n)

	# Loop over muons using the pT array from above
	for n in range(len(_MuonPt)):

		# Some muon alignment studies use the inverse diff of the high pT and Trk pT values
		deltainvpt = -1.0	
		if ( T.MuonTrkPt[nequiv[n]] > 0.0 ) and (_MuonPt[n]>0.0):
			deltainvpt = ( 1.0/T.MuonTrkPt[nequiv[n]] - 1.0/_MuonPt[n])
	
		# For alignment correction studies in MC, the pT is modified according to
		# parameterizations of the position
		if alignementcorrswitch == True and isdata==False:
			if abs(deltainvpt) > 0.0000001:
				__Pt_mu = _MuonPt[n]
				__Eta_mu = T.MuonEta[n]
				__Phi_mu = T.MuonPhi[n]
				__Charge_mu = T.MuonCharge[nequiv[n]]
				if (__Pt_mu >200)*(abs(__Eta_mu) < 0.9)      : 
					_MuonPt[n] =  ( (1.0) / ( -5e-05*__Charge_mu*sin(-1.4514813+__Phi_mu ) + 1.0/__Pt_mu ) ) 
				deltainvpt = ( 1.0/T.MuonTrkPt[nequiv[n]] - 1.0/_MuonPt[n])


		# For the ID, begin by assuming it passes. Veto if it fails any condition
		# High PT conditions from https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonIdRun2#Short_Term_Medium_Muon_Definitio
		# NTuple definitions in https://raw.githubusercontent.com/CMSLQ/RootTupleMakerV2/master/src/RootTupleMakerV2_Muons.cc
		Pass = True
                #There is an or of requirements, do this by making 2 bools and OR'ing them later
	        Pass1, Pass2 =  True, True

                # Require Loose muon flag
	        Pass *= T.MuonIsLooseMuon[n] > 0

	        #fixme these two are equivalent to IsLooseMuon
		#Pass *= T.MuonIsPF[n]
	        #Pass *= (T.MuonIsGlobal[n] or T.MuonIsTracker[n])

	        # Require valid fraction of hits
	        Pass *= T.MuonTrkValidFractionOfHits[n] > 0.49

		# A preliminary pT cut.
		Pass *= (_MuonPt[n] > 8)#fixme offline cuts are 20(10)

		# Eta requirement 
		Pass *= abs(T.MuonEta[n])<2.4

	        # Require Global Muon
                Pass1 *= T.MuonIsGlobal[n]

		# Global Track chi2
                Pass1 *= T.MuonGlobalChi2[n] < 3

		# combined Quality chi2LocalPosition
		Pass1 *= T.MuonCombinedQualityChi2LocalPosition[n] < 12

		# combined Quality Track Kink
		Pass1 *= T.MuonCombinedQualityTrkKink[n] < 20

		# segment Compatibility
		Pass1 *= T.MuonSegmentCompatibility[n] > 0.303

		# segment Compatibility
		Pass2 *= T.MuonSegmentCompatibility[n] > 0.451

		Pass *= (Pass1 or Pass2)

		# Isolation condition using combined PF relative isolation - 0.25 for loose (98% efficiency), 0.15 for tight (95% efficiency)
		if nonisoswitch != True:
			correctedIso = T.MuonPFIsoR04ChargedHadron[n] + max(0.,T.MuonPFIsoR04NeutralHadron[n]+T.MuonPFIsoR04Photon[n]-0.5*T.MuonPFIsoR04PU[n])
			Pass *= correctedIso/_MuonPt[n] < 0.25

		# Propagate MET changes if undergoing systematic variation
		if (Pass):
			NewMu = TLorentzVector()
			OldMu = TLorentzVector()
			NewMu.SetPtEtaPhiM(_MuonPt[n],T.MuonEta[n],T.MuonPhi[n],0)
			#NewMu.SetPtEtaPhiM(_MuonPt[n],T.MuonEta[n],T.MuonPhi[n],0)
			OldMu.SetPtEtaPhiM(T.MuonPt[n],T.MuonEta[n],T.MuonPhi[n],0)
			#OldMu.SetPtEtaPhiM(T.MuonPt[n],T.MuonEta[n],T.MuonPhi[n],0)
			_met = PropagatePTChangeToMET(_met,OldMu,NewMu)

			# Append items to retun if the muon is good

			muons.append(NewMu)
			trk_isos.append((T.MuonTrackerIsoSumPT[nequiv[n]]/_MuonPt[n]))
			chi2.append(T.MuonGlobalChi2[nequiv[n]])
			pfid.append(T.MuonIsPF[nequiv[n]])
			layers.append(T.MuonTrackLayersWithMeasurement[nequiv[n]])
			charges.append(T.MuonCharge[n])
			muoninds.append(n)
			deltainvpts.append(deltainvpt)

	return [muons,muoninds,_met,trk_isos,charges,deltainvpts,chi2,pfid,layers]


def TightHighPtIDMuons(T,_met,variation,isdata):
	# Purpose: Gets the collection of muons passing tight muon ID. 
	#         Returns muons as TLorentzVectors, and indices corrresponding
	#         to the surviving muons of the muon collection. 
	#         Also returns modified MET for systematic variations.
	muons = []
	muoninds = []
	if variation=='MESup':	
		#_MuonCocktailPt = [(pt + pt*(0.05*pt/1000.0)) for pt in T.MuonCocktailPt]#original
		_MuonCocktailPt = [(pt + pt*(0.10*pt/1000.0)) for pt in T.MuonCocktailPt]#updated to Zprime 13TeV study number
	elif variation=='MESdown':	
		#_MuonCocktailPt = [(pt - pt*(0.05*pt/1000.0)) for pt in T.MuonCocktailPt]
		_MuonCocktailPt = [(pt - pt*(0.10*pt/1000.0)) for pt in T.MuonCocktailPt]
	elif variation=='MER':	
		_MuonCocktailPt = [pt+pt*tRand.Gaus(0.0,  0.01*(pt<=200.0) + (0.04)*(pt>200.0) ) for pt in T.MuonCocktailPt]
	else:	
		_MuonCocktailPt = [pt for pt in T.MuonCocktailPt]	

	if (isdata):
		_MuonCocktailPt = [pt for pt in T.MuonCocktailPt]	

	trk_isos = []
	charges = []
	deltainvpts = []

	chi2 = []
	pfid = []
	layers = []

	nequiv = []
	for n in range(len(T.MuonPt)):
		#if T.MuonIsGlobal[n] or newntupleswitch==True: #not necessary anymore - global muon requirement encompassed later
		nequiv.append(n)

	# Loop over muons using the pT array from above
	for n in range(len(_MuonCocktailPt)):

		# Some muon alignment studies use the inverse diff of the high pT and Trk pT values
		deltainvpt = -1.0	
		if ( T.MuonTrkPt[nequiv[n]] > 0.0 ) and (_MuonCocktailPt[n]>0.0):
			deltainvpt = ( 1.0/T.MuonTrkPt[nequiv[n]] - 1.0/_MuonCocktailPt[n])
	
		# For alignment correction studies in MC, the pT is modified according to
		# parameterizations of the position
		if alignementcorrswitch == True and isdata==False:
			if abs(deltainvpt) > 0.0000001:
				__Pt_mu = _MuonCocktailPt[n]
				__Eta_mu = T.MuonCocktailEta[n]
				__Phi_mu = T.MuonCocktailPhi[n]
				__Charge_mu = T.MuonCharge[nequiv[n]]
				if (__Pt_mu >200)*(abs(__Eta_mu) < 0.9)      : 
					_MuonCocktailPt[n] =  ( (1.0) / ( -5e-05*__Charge_mu*sin(-1.4514813+__Phi_mu ) + 1.0/__Pt_mu ) ) 
				deltainvpt = ( 1.0/T.MuonTrkPt[nequiv[n]] - 1.0/_MuonCocktailPt[n])


		# For the ID, begin by assuming it passes. Veto if it fails any condition
		# High PT conditions from https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId
		# NTuple definitions in https://raw.githubusercontent.com/CMSLQ/RootTupleMakerV2/master/src/RootTupleMakerV2_Muons.cc
		Pass = True
		# A preliminary pT cut. This also encompasses the GlobalMuon conditions, since
		# all non-global muons have cocktail pT of -1 in the ntuples.
		Pass *= (_MuonCocktailPt[n] > 10)#fixme todo was 35 - changed to 10 for HH testing      
		# Eta requirement matches trigger.
		Pass *= abs(T.MuonCocktailEta[n])<2.1    

		# Number of valid hits
		Pass *= T.MuonGlobalTrkValidHits[nequiv[n]]>=1

		# Number of station matches
		Pass *= T.MuonStationMatches[nequiv[n]]>1 

		# Impact parameters
		# Pass *= abs(T.MuonCocktailTrkVtxDXY[n]) < 0.2     
		# Pass *= abs(T.MuonCocktailTrkVtxDZ[n]) < 0.5      
		Pass *= abs(T.MuonBestTrackVtxDistXY[nequiv[n]]) < 0.2     # Fixed
		Pass *= abs(T.MuonBestTrackVtxDistZ[nequiv[n]]) < 0.5      #Fixed 
		# Pixel hits
		Pass *= T.MuonTrkPixelHits[nequiv[n]]>=1  

		# Layers with measurement (high PT ID cut is 5, used to be tight id cut at 8)
		Pass *= T.MuonTrackLayersWithMeasurement[nequiv[n]] > 5 
		Pass *= T.MuonCocktailPtError[n]/T.MuonCocktailPt[n]  < 0.3

		# Isolation condition using tracker-only isolation
		if nonisoswitch != True:
			Pass *= (T.MuonTrackerIsoSumPT[nequiv[n]]/_MuonCocktailPt[n])<0.1

		# Propagate MET changes if undergoing systematic variation
		if (Pass):
			NewMu = TLorentzVector()
			OldMu = TLorentzVector()
			NewMu.SetPtEtaPhiM(_MuonCocktailPt[n],T.MuonCocktailEta[n],T.MuonCocktailPhi[n],0)
			#NewMu.SetPtEtaPhiM(_MuonCocktailPt[n],T.MuonEta[n],T.MuonPhi[n],0)
			OldMu.SetPtEtaPhiM(T.MuonCocktailPt[n],T.MuonCocktailEta[n],T.MuonCocktailPhi[n],0)
			#OldMu.SetPtEtaPhiM(T.MuonPt[n],T.MuonEta[n],T.MuonPhi[n],0)
			_met = PropagatePTChangeToMET(_met,OldMu,NewMu)

			# Append items to retun if the muon is good

			muons.append(NewMu)
			trk_isos.append((T.MuonTrackerIsoSumPT[nequiv[n]]/_MuonCocktailPt[n]))
			chi2.append(T.MuonGlobalChi2[nequiv[n]])
			pfid.append(T.MuonIsPF[nequiv[n]])
			layers.append(T.MuonTrackLayersWithMeasurement[nequiv[n]])
			charges.append(T.MuonCocktailCharge[n])
			muoninds.append(n)
			deltainvpts.append(deltainvpt)

	return [muons,muoninds,_met,trk_isos,charges,deltainvpts,chi2,pfid,layers]


def HEEPElectrons(T,_met,variation):
	# Purpose: Gets the collection of electrons passing HEEP ID. 
	#         Returns electrons as TLorentzVectors, and indices corrresponding
	#         to the surviving electrons of the electron collection. 
	#         Also returns modified MET for systematic variations.	
	electrons = []
	electroninds = []
	if variation=='EESup':	
		_ElectronPt = [pt*1.01 for pt in T.ElectronPtHeep]
	elif variation=='EESdown':	
		_ElectronPt = [pt*0.99 for pt in T.ElectronPtHeep]
	elif variation=='EER':	
		_ElectronPt = [pt+pt*tRand.Gaus(0.0,0.04) for pt in T.ElectronPtHeep]
	else:	
		_ElectronPt = [pt for pt in T.ElectronPtHeep]	

	for n in range(len(_ElectronPt)):
		Pass = True
		Pass *= (_ElectronPt[n] > 35)
		Pass *= abs(T.ElectronEta[n])<2.4

		barrel = (abs(T.ElectronSCEta[n]))<1.442
		endcap = (abs(T.ElectronSCEta[n]))>1.566
		Pass *= (barrel+endcap)

		if barrel:
			Pass *= bool(T.ElectronIsEcalDriven[n])
			Pass *= T.ElectronDeltaEtaTrkSeedSC[n] < 0.004
			Pass *= T.ElectronDeltaPhiTrkSC[n] < 0.06
			Pass *= T.ElectronHoE[n] < 0.05 + 1./T.ElectronSCEnergy[n]
			Pass *= ((T.ElectronFull5x5E2x5OverE5x5[n] > 0.94) or (T.ElectronFull5x5E1x5OverE5x5[n] > 0.83) )
	                if nonisoswitch != True:
				Pass *= (T.ElectronHcalIsoD1DR03[n] + T.ElectronEcalIsoDR03[n]) <  (2.0 + 0.03*_ElectronPt[n] + 0.28*T.ElectronRhoIsoHEEP[n])
			        Pass *= T.ElectronHeep70TrkIso[n] < 5.0
			Pass *= T.ElectronMissingHits[n] <=1
			Pass *= T.ElectronLeadVtxDistXY[n]<0.02

		if endcap:
			Pass *= bool(T.ElectronIsEcalDriven[n])
			Pass *= T.ElectronDeltaEtaTrkSeedSC[n] < 0.006
			Pass *= T.ElectronDeltaPhiTrkSC[n] < 0.06
			Pass *= T.ElectronHoE[n] < 0.05 + 5./T.ElectronSCEnergy[n]
			Pass *= T.ElectronFull5x5SigmaIEtaIEta[n] < 0.03
	                if nonisoswitch != True:
				if _ElectronPt[n]<50:
					Pass *= ((T.ElectronHcalIsoD1DR03[n] + T.ElectronEcalIsoDR03[n]) < (2.5 + 0.28*T.ElectronRhoIsoHEEP[n]))
				else:
					Pass *= ((T.ElectronHcalIsoD1DR03[n] + T.ElectronEcalIsoDR03[n]) < (2.5 + 0.03*(_ElectronPt[n]-50.0) + 0.28*T.ElectronRhoIsoHEEP[n]))
				Pass *= T.ElectronHeep70TrkIso[n] < 5.0
			Pass *= T.ElectronMissingHits[n] <=1
			Pass *= T.ElectronLeadVtxDistXY[n]<0.05

		if (Pass):
			NewEl = TLorentzVector()
			OldEl = TLorentzVector()
			NewEl.SetPtEtaPhiM(_ElectronPt[n],T.ElectronEta[n],T.ElectronPhi[n],0)
			OldEl.SetPtEtaPhiM(T.ElectronPtHeep[n],T.ElectronEta[n],T.ElectronPhi[n],0)
			met = PropagatePTChangeToMET(_met,OldEl,NewEl)

		Pass *= (_ElectronPt[n] > 35)
		if (Pass):
			electrons.append(NewEl)
			electroninds.append(n)
	return [electrons,electroninds,_met]


def TightElectrons(T,_met,variation,isdata):
	# Purpose: Gets the collection of electrons passing Tight Electron ID. 
	#         Returns electrons as TLorentzVectors, and indices corrresponding
	#         to the surviving electrons of the electron collection. 
	#         Also returns modified MET for systematic variations.	
	#         https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Recommended_Working_points_for_2
	electrons = []
	electroninds = []
	if variation=='EESup':	
		_ElectronPt = [pt*1.01 for pt in T.ElectronPt]
	elif variation=='EESdown':	
		_ElectronPt = [pt*0.99 for pt in T.ElectronPt]
	elif variation=='EER':	
		_ElectronPt = [pt+pt*tRand.Gaus(0.0,0.04) for pt in T.ElectronPt]
	else:	
		_ElectronPt = [pt for pt in T.ElectronPt]	

	trk_isos = []
	charges = []
	deltainvpts = []
	chi2 = []
	pfid = []
	layers = []

	for n in range(len(_ElectronPt)):
		Pass = True
		Pass *= (T.ElectronPt[n] > 12)
		Pass *= abs(T.ElectronEta[n])<2.5

		barrel = (abs(T.ElectronSCEta[n]))<1.442
		endcap = (abs(T.ElectronSCEta[n]))>1.56 
		Pass *= (barrel+endcap)

	        Pass *= T.ElectronPassEGammaIDTight[n]>0

		if (Pass):
			NewEl = TLorentzVector()
			OldEl = TLorentzVector()
			NewEl.SetPtEtaPhiM(_ElectronPt[n],T.ElectronEta[n],T.ElectronPhi[n],0)
			OldEl.SetPtEtaPhiM(T.ElectronPt[n],T.ElectronEta[n],T.ElectronPhi[n],0)
			met = PropagatePTChangeToMET(_met,OldEl,NewEl)

		if (Pass):
			electrons.append(NewEl)
			electroninds.append(n)
			trk_isos.append(T.ElectronTrkIsoDR03[n])
			charges.append(T.ElectronCharge[n])
			deltainvpts.append(0.)
			chi2.append(0.)
			pfid.append(0.)
			layers.append(0.)

	return [electrons,electroninds,_met,trk_isos,charges]



def JERModifiedPt(pt,eta,phi,T,modtype):
	# Pupose: Modify reco jets based on genjets. Input is pt/eta/phi of a jet. 
	#         The jet will be matched to a gen jet, and the difference
	#         between reco and gen will be modified according to appropriate
	#         pt/eta dependent scale factors. 
	#         The modified jet PT is returned.
	#         https://hypernews.cern.ch/HyperNews/CMS/get/JetMET/1336.html
	#         https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution

	if T.isData:
		return pt
	
	bestn = -1
	bestdpt = 0.
	bestdR = 9999999.9
	jet = TLorentzVector()
	jet.SetPtEtaPhiM(pt,eta,phi,0.0)
	for n in range(len(T.GenJetPtAK4)):
		gjet = TLorentzVector()
		gjet.SetPtEtaPhiM(T.GenJetPtAK4[n],T.GenJetEtaAK4[n],T.GenJetPhiAK4[n],0.0)
		dR = abs(jet.DeltaR(gjet))
		if dR<bestdR and dR<0.3 :
			bestdR = dR
			bestn = n
			bestdpt = pt-gjet.Pt()

	if bestdR>0.5:
		return pt

	abseta = abs(eta)

	#13 TeV 80X (2016, BCD+GH PromtReco) DATA/MC SFs
	if abseta >= 0   : jfacs = [  0.109 , 0.117 , 0.101  ] 
	if abseta >= 0.5 : jfacs = [  0.138 , 0.151 , 0.125  ] 
	if abseta >= 0.8 : jfacs = [  0.114 , 0.127 , 0.101  ] 
	if abseta >= 1.1 : jfacs = [  0.123 , 0.147 , 0.099  ] 
	if abseta >= 1.3 : jfacs = [  0.084 , 0.095 , 0.073  ] 
	if abseta >= 1.7 : jfacs = [  0.082 , 0.117 , 0.047  ] 
	if abseta >= 1.9 : jfacs = [  0.140 , 0.187 , 0.093  ] 
	if abseta >= 2.1 : jfacs = [  0.067 , 0.120 , 0.014  ]  
	if abseta >= 2.3 : jfacs = [  0.177 , 0.218 , 0.136  ] 
	if abseta >= 2.5 : jfacs = [  0.364 , 0.403 , 0.325  ] 
	if abseta >= 2.8 : jfacs = [  0.857 , 0.928 , 0.786  ] 
	if abseta >= 3.0 : jfacs = [  0.328 , 0.350 , 0.306  ]  
	if abseta >= 3.2 : jfacs = [  0.160 , 0.189 , 0.131  ]  

	if modtype == '':
		adjustmentfactor = jfacs[0]
	if modtype == 'up':
		adjustmentfactor = jfacs[1]
	if modtype == 'down':
		adjustmentfactor = jfacs[2]

	ptadjustment = adjustmentfactor*bestdpt
	pt += ptadjustment
	return max(0.,pt)


def LooseIDJets(T,met,variation,isdata):
	# Pupose: Gets the collection of jets passing loose PFJet ID. 
	#         Returns jets as TLorentzVectors, and indices corrresponding
	#         to the surviving jetss of the jet collection. 
	#         Also returns modified MET for systematic variations.	

	if variation!='JERup' and variation!='JERdown':
		# _PFJetPt = [JERModifiedPt(T.PFJetPt[n],T.PFJetEta[n],T.PFJetPhi[n],T,'') for n in range(len(T.PFJetPt))] 	
		 _PFJetPt = [pt for pt in T.PFJetPtAK4CHS]				
	if variation=='JERup':	
		_PFJetPt = [JERModifiedPt(T.PFJetPtAK4CHS[n],T.PFJetEtaAK4CHS[n],T.PFJetPhiAK4CHS[n],T,'up') for n in range(len(T.PFJetPtAK4CHS))] 
	if variation=='JERdown':	
		_PFJetPt = [JERModifiedPt(T.PFJetPtAK4CHS[n],T.PFJetEtaAK4CHS[n],T.PFJetPhiAK4CHS[n],T,'down') for n in range(len(T.PFJetPtAK4CHS))] 		

	if variation=='JESup':	
		_PFJetPt = [ _PFJetPt[n]*(1.0+T.PFJetJECUncAK4CHS[n]) for n in range(len(_PFJetPt))]
	if variation=='JESdown':	
		_PFJetPt = [ _PFJetPt[n]*(1.0-T.PFJetJECUncAK4CHS[n]) for n in range(len(_PFJetPt))]

	if (isdata):
		_PFJetPt = [pt for pt in T.PFJetPtAK4CHS]	
		#_PFJetPt = [T.PFJetPtAK4CHS[n]*T.PFJetL2L3ResJECAK4CHS[n] for n in range(len(T.PFJetPtAK4CHS))]	

	# print met.Pt(),


	JetFailThreshold=0.0

	jets = []
	jetinds = []
	NHFs = []
	NEMFs = []
	CSVscores,bMVAscores = [],[]
	for n in range(len(_PFJetPt)):
		looseJetID = False
		eta = T.PFJetEtaAK4CHS[n]
		NHF = T.PFJetNeutralHadronEnergyFractionAK4CHS[n]
		NEMF = T.PFJetNeutralEmEnergyFractionAK4CHS[n]
		CEMF = T.PFJetChargedEmEnergyFractionAK4CHS[n]
		CHF = T.PFJetChargedHadronEnergyFractionAK4CHS[n]
		MUF = T.PFJetMuonEnergyFractionAK4CHS[n]
		NumConst = T.PFJetChargedMultiplicityAK4CHS[n]+T.PFJetNeutralMultiplicityAK4CHS[n]
		NumNeutralParticle = T.PFJetNeutralMultiplicityAK4CHS[n]
		CHM = T.PFJetChargedMultiplicityAK4CHS[n]
		if abs(eta)<=2.7:
			looseJetID = (NHF<0.99 and NEMF<0.99 and NumConst>1) and ((abs(eta)<=2.4 and CHF>0 and CHM>0 and CEMF<0.99) or abs(eta)>2.4) and abs(eta)<=2.7
		elif abs(eta)<=3.0:
			looseJetID = (NHF< 0.98 and NEMF>0.01 and NumNeutralParticle>2 and abs(eta)>2.7 and abs(eta)<=3.0 )
		else:
			looseJetID = (NEMF<0.90 and NumNeutralParticle>10 and abs(eta)>3.0 and abs(eta)<5.0 )
		if _PFJetPt[n]>18 :#fixme todo was pt>30, reduced for HH
			if looseJetID:
				j = TLorentzVector()
				j.SetPtEtaPhiM(_PFJetPt[n],T.PFJetEtaAK4CHS[n],T.PFJetPhiAK4CHS[n],0)
				oldjet = TLorentzVector()
				oldjet.SetPtEtaPhiM(T.PFJetPtAK4CHS[n],T.PFJetEtaAK4CHS[n],T.PFJetPhiAK4CHS[n],0)				
				met = PropagatePTChangeToMET(met,oldjet,j)
				jets.append(j)
				jetinds.append(n)
				NHFs.append(NHF)
				NEMFs.append(NEMF)
				CSVscores.append(T.PFJetCombinedInclusiveSecondaryVertexBTagAK4CHS[n])
				bMVAscores.append(T.PFJetCombinedMVABTagAK4CHS[n])
			else:
				if _PFJetPt[n] > JetFailThreshold:
					JetFailThreshold = _PFJetPt[n]

	# print met.Pt()

	return [jets,jetinds,met,JetFailThreshold,NHFs,NEMFs,CSVscores,bMVAscores]

def GetHHJetsOld(jets,btagScoresCSV,btagScoresMVA,muon1,muon2,jetinds, T):
	#Purpose: select which jets to use for HH analysis, separating bJets from light jets. Note that jets have already been cleaned from muons and electrons in cone of 0.3.
	
	EmptyLorentz = TLorentzVector()
	EmptyLorentz.SetPtEtaPhiM(0,0,0,0)
	[bjet1,bjet2,jet1,jet2,jet3]=[EmptyLorentz,EmptyLorentz,EmptyLorentz,EmptyLorentz,EmptyLorentz]
	#if v == '' : print len(jets)
	highBtagCSV,highBtag = -20.0,-20.0
	secondBtagCSV,secondBtag = -20.0,-20.0
	highBtagCounter = -1
	secondBtagCounter = -1
	indRecoBJet1 = -1
	indRecoBJet2 = -1
	indRecoJet1 = -1
	indRecoJet2 = -1
	indRecoJet3 = -1
	
	for i in range(len(btagScoresMVA)) :
		#if v == '' : print 'jet i', i, 'flavour',T.PFJetPartonFlavourAK4CHS[jetinds[i]]
		#if T.PFJetPartonFlavourAK4CHS[jetinds[i]] == 21 : continue  # for testing the effect of gluon jets
		if btagScoresMVA[i]>highBtag:
			highBtag = btagScoresMVA[i]
			highBtagCSV = btagScoresCSV[i]
			highBtagCounter = i
	for i in range(len(btagScoresMVA)) :
		#if T.PFJetPartonFlavourAK4CHS[jetinds[i]] == 21 : continue  # for testing the effect of gluon jets
		#if  btagScoresMVA[i]>secondBtag and btagScoresMVA[i]<highBtag:
		if i==highBtagCounter: continue
		if btagScoresMVA[i]>secondBtag :
			secondBtag = btagScoresMVA[i]
			secondBtagCSV = btagScoresCSV[i]
			secondBtagCounter = i
	#[bjet1,bjet2] = [jets[highBtagCounter],jets[secondBtagCounter]]
	[bjet1,bjet2,indRecoBJet1,indRecoBJet2] = [jets[highBtagCounter],jets[secondBtagCounter],jetinds[highBtagCounter],jetinds[secondBtagCounter]]
	#if v == '' : print 'bjet counters',highBtagCounter,secondBtagCounter
	#if v == '' : print 'bjet reco ind',indRecoBJet1,indRecoBJet2,'jets ind',highBtagCounter,secondBtagCounter,(bjet1+bjet2).M()

	## --- Next looking for Z_jj
	jet1index, jet2index, closestZ = -1,-1,2200.
	gotJet1,gotJet2=False,False
	[jet1Btag,jet2Btag]=[-20.0,-20.0]

	for i in range(len(jets)-1) :
		if i==highBtagCounter or i==secondBtagCounter: continue
		for j in range(i+1,len(jets)) :
			if j==highBtagCounter or j==secondBtagCounter: continue
			if i>=j: continue
			#if v == '': print 'i:',i,'j:',j,'M_H_mumujj',(muon1+muon2+jets[i]+jets[j]).M()
			if abs((muon1+muon2+jets[i]+jets[j]).M()-125) < closestZ and (muon1+muon2+jets[i]+jets[j]).M() > 0:
				closestZ = abs((muon1+muon2+jets[i]+jets[j]).M()-125)
				jet1index,jet2index = i,j
				jet1, jet2 = jets[i], jets[j]
				indRecoJet1, indRecoJet2 = jetinds[i], jetinds[j]
				gotJet1=True
				gotJet2=True
	#if v == '': print 'Zjet reco ind',indRecoJet1,indRecoJet2,'jets ind',jet1index,jet2index,'M_H_mumujj',(muon1+muon2+jets[jet1index]+jets[jet2index]).M()

	for i in range(len(jets)):
		if i==highBtagCounter or i==secondBtagCounter:
			continue
		if not gotJet1:
			jet1=jets[i]
			indRecoJet1=jetinds[i]
			gotJet1=True
			jet1Btag = btagScoresMVA[i]
			continue
		if not gotJet2:
			jet2=jets[i]
			indRecoJet2=jetinds[i]
			gotJet2=True
			jet2Btag = btagScoresMVA[i]
			continue
		jet3=jets[i]
		indRecoJet3=jetinds[i]
		break
	#if v == '': print 'Zjet reco ind',indRecoJet1,indRecoJet2,'jets ind',jet1index,jet2index,'M_H_mumujj',(muon1+muon2+jet1+jet2).M()
	#if v == '' :
	#	print 'pts:',bjet1.Pt(),bjet2.Pt(),jet1.Pt(),jet2.Pt()
	#	print 'btag scores:', highBtag,secondBtag,jet1Btag,jet2Btag
	return [bjet1,highBtagCSV,highBtag,bjet2,secondBtagCSV,secondBtag,jet1,jet2,jet3,indRecoBJet1,indRecoBJet2,indRecoJet1,indRecoJet2,indRecoJet3]

def GetHHJetsNew(jets,btagScoresCSV,btagScoresMVA,muon1,muon2,jetinds, T, met):
	#Purpose: select which jets to use for HH analysis, separating bJets from light jets. Note that jets have already been cleaned from muons and electrons in cone of 0.3.

	EmptyLorentz = TLorentzVector()
	EmptyLorentz.SetPtEtaPhiM(0,0,0,0)
	[bjet1,bjet2,jet1,jet2,jet3]=[EmptyLorentz,EmptyLorentz,EmptyLorentz,EmptyLorentz,EmptyLorentz]
	#if v == '' : print len(jets)
	highBtagCSV,highBtag = -20.0,-20.0
	secondBtagCSV,secondBtag = -20.0,-20.0
	highBtagCounter = -1
	secondBtagCounter = -1
	jet1index,jet2index = -1,-1
	indRecoBJet1 = -1
	indRecoBJet2 = -1
	indRecoJet1 = -1
	indRecoJet2 = -1
	indRecoJet3 = -1
	closestH = 2200. #999.
	closestZ = 2200. #175.
	gotBs = False
	gotZjs = False
	
	if not gotBs :
		highBtagCSV,highBtag = -20.0,-20.0
		secondBtagCSV,secondBtag = -20.0,-20.0
		highBtagCounter = -1
		secondBtagCounter = -1
		indRecoBJet1 = -1
		indRecoBJet2 = -1

		for i in range(len(btagScoresMVA)) :
			#if T.PFJetPartonFlavourAK4CHS[jetinds[i]] == 21 : continue  # for testing the effect of gluon jets
			if btagScoresCSV[i] < 0.57 : continue
			if btagScoresMVA[i] < -0.7 : continue
			if i==jet1index or i==jet2index: continue
			if btagScoresMVA[i]>highBtag:
				highBtag = btagScoresMVA[i]
				highBtagCSV = btagScoresCSV[i]
				highBtagCounter = i
		for i in range(len(btagScoresMVA)) :
			#if T.PFJetPartonFlavourAK4CHS[jetinds[i]] == 21 : continue  # for testing the effect of gluon jets
			if btagScoresCSV[i] < 0.57 : continue
			if btagScoresMVA[i] < -0.7 : continue
			if i==jet1index or i==jet2index: continue
			if i==highBtagCounter: continue
			if btagScoresMVA[i]>secondBtag :
				secondBtag = btagScoresMVA[i]
				secondBtagCSV = btagScoresCSV[i]
				secondBtagCounter = i
		if highBtagCounter >= 0 :
			bjet1,indRecoBJet1 = jets[highBtagCounter],jetinds[highBtagCounter]
			highBtag,highBtagCSV  = btagScoresMVA[highBtagCounter],btagScoresCSV[highBtagCounter]
			if secondBtagCounter >= 0 :
				bjet2,indRecoBJet2 = jets[secondBtagCounter],jetinds[secondBtagCounter]
				secondBtag,secondBtagCSV = btagScoresMVA[secondBtagCounter],btagScoresCSV[secondBtagCounter]
				gotBs = True
			else:
				for j in range(len(btagScoresMVA)) :
					#if T.PFJetPartonFlavourAK4CHS[jetinds[j]] == 21 : continue  # for testing the effect of gluon jets
					#if btagScoresCSV[j] < 0.06  and abs(-0.853212237358 - btagScoresMVA[j]) < 0.000000000002 : continue # if I want to include this condition I have to put somthing tighter, because there are bjets with this condition as well
					if j==jet1index or j==jet2index: continue
					if j==highBtagCounter: continue
					#if v == '' : print ' debug 1 high bscore : index i', jetinds[highBtagCounter], 'index j', jetinds[j],'m_bb',(jets[highBtagCounter]+jets[j]).M(), ' diff', abs((jets[highBtagCounter]+jets[j]).M()-125), 'dR', abs(jets[highBtagCounter].DeltaR(jets[j]))
					if abs((jets[highBtagCounter]+jets[j]).M()-125) < closestH and (jets[highBtagCounter]+jets[j]).M() > 0 :
						closestH = abs((jets[highBtagCounter]+jets[j]).M()-125)
						secondBtagCounter = j
						bjet2 = jets[j]
						indRecoBJet2 = jetinds[j]
						secondBtag = btagScoresMVA[j]
						secondBtagCSV = btagScoresCSV[j]
						gotBs = True

	if not gotBs :
		highBtagCSV,highBtag = -20.0,-20.0
		secondBtagCSV,secondBtag = -20.0,-20.0
		highBtagCounter = -1
		secondBtagCounter = -1
		indRecoBJet1 = -1
		indRecoBJet2 = -1

		closestH = 2200 #2200. #50.
		for i in range(len(jets)-1) :
			#if T.PFJetPartonFlavourAK4CHS[jetinds[i]] == 21 : continue  # for testing the effect of gluon jets
			if btagScoresCSV[i] < 0.06  and abs(-0.853212237358 - btagScoresMVA[i]) < 0.000000000002 : continue
			if not T.PFJetPileupMVApassesMediumAK4CHS[jetinds[i]] : continue
			if i==jet1index or i==jet2index: continue
			for j in range(i+1,len(jets)) :
				#if T.PFJetPartonFlavourAK4CHS[jetinds[j]] == 21 : continue  # for testing the effect of gluon jets
				if btagScoresCSV[j] < 0.06  and abs(-0.853212237358 - btagScoresMVA[j]) < 0.000000000002 : continue
				if not T.PFJetPileupMVApassesMediumAK4CHS[jetinds[j]] : continue
				if j==jet1index or j==jet2index: continue
				if i>=j: continue
				#if v == '' : print ' debug : index i', jetinds[i], 'index j', jetinds[j],'m_bb',(jets[i]+jets[j]).M(), ' diff', abs((jets[i]+jets[j]).M()-125), 'dR', abs(jets[i].DeltaR(jets[j]))
				if abs((jets[i]+jets[j]).M()-125) < closestH and (jets[i]+jets[j]).M() > 0 :
					closestH = abs((jets[i]+jets[j]).M()-125)
					if btagScoresMVA[i] > btagScoresMVA[j]:
						highBtagCounter,secondBtagCounter = i,j
						bjet1, bjet2 = jets[i], jets[j]
						indRecoBJet1, indRecoBJet2 = jetinds[i], jetinds[j]
						highBtag, secondBtag = btagScoresMVA[i],btagScoresMVA[j]
						highBtagCSV, secondBtagCSV = btagScoresCSV[i],btagScoresCSV[j]
					else:
						highBtagCounter,secondBtagCounter = j,i
						bjet1, bjet2 = jets[j], jets[i]
						indRecoBJet1, indRecoBJet2 = jetinds[j], jetinds[i]
						highBtag, secondBtag = btagScoresMVA[j],btagScoresMVA[i]
						highBtagCSV, secondBtagCSV = btagScoresCSV[j],btagScoresCSV[i]
					gotBs = True

	if not gotBs :
		highBtagCSV,highBtag = -20.0,-20.0
		secondBtagCSV,secondBtag = -20.0,-20.0
		highBtagCounter = -1
		secondBtagCounter = -1
		indRecoBJet1 = -1
		indRecoBJet2 = -1

		for i in range(len(btagScoresMVA)) :
			#if T.PFJetPartonFlavourAK4CHS[jetinds[i]] == 21 : continue  # for testing the effect of gluon jets
			if i==jet1index or i==jet2index: continue
			if btagScoresMVA[i]>highBtag:
				highBtag = btagScoresMVA[i]
				highBtagCSV = btagScoresCSV[i]
				highBtagCounter = i
		for i in range(len(btagScoresMVA)) :
			#if T.PFJetPartonFlavourAK4CHS[jetinds[i]] == 21 : continue  # for testing the effect of gluon jets
			if i==jet1index or i==jet2index: continue
			if i==highBtagCounter: continue
			if btagScoresMVA[i]>secondBtag :
				secondBtag = btagScoresMVA[i]
				secondBtagCSV = btagScoresCSV[i]
				secondBtagCounter = i
		if highBtagCounter >= 0 :
			bjet1,indRecoBJet1 = jets[highBtagCounter],jetinds[highBtagCounter]
			highBtag,highBtagCSV  = btagScoresMVA[highBtagCounter],btagScoresCSV[highBtagCounter]
		if secondBtagCounter >= 0 :
			bjet2,indRecoBJet2 = jets[secondBtagCounter],jetinds[secondBtagCounter]
			secondBtag,secondBtagCSV = btagScoresMVA[secondBtagCounter],btagScoresCSV[secondBtagCounter]
		gotBs = True #  if cannot really find Hjets, just return EmptyVector

	if not gotZjs :
		## --- Next looking for Z_jj
		closestZ = 2200.
		for i in range(len(jets)-1) :
			if i==highBtagCounter or i==secondBtagCounter: continue
			for j in range(i+1,len(jets)) :
				if j==highBtagCounter or j==secondBtagCounter: continue
				if i>=j: continue
				#if v == '': print 'i:',i,'j:',j,'M_H_mumujj',(muon1+muon2+jets[i]+jets[j]).M()
				if abs((muon1+muon2+jets[i]+jets[j]).M()-125) < closestZ and (muon1+muon2+jets[i]+jets[j]).M() > 0 :
					closestZ = abs((muon1+muon2+jets[i]+jets[j]).M()-125)
					jet1index,jet2index = i,j
					jet1, jet2 = jets[i], jets[j]
					indRecoJet1, indRecoJet2 = jetinds[i], jetinds[j]
					gotZjs = True
		#if v == '': print 'Zjet reco ind',indRecoJet1,indRecoJet2,'jets ind',jet1index,jet2index,'M_H_mumujj',(muon1+muon2+jets[jet1index]+jets[jet2index]).M()

	if not gotZjs :
		for i in range(len(jets)):
			if i==highBtagCounter or i==secondBtagCounter: continue
			jet1=jets[i]
			indRecoJet1=jetinds[i]
			jet1index = i
			break
		for i in range(len(jets)):
			if i==highBtagCounter or i==secondBtagCounter: continue
			if i==jet1index: continue
			jet2=jets[i]
			indRecoJet2=jetinds[i]
			jet2index = i
			break
		for i in range(len(jets)):
			if i==highBtagCounter or i==secondBtagCounter: continue
			if i==jet1index or i==jet2index: continue
			jet3=jets[i]
			indRecoJet3=jetinds[i]
			break
		gotZjs = True
	#if v == '': print 'Zjet reco ind',indRecoJet1,indRecoJet2,'jets ind',jet1index,jet2index,'M_H_mumujj',(muon1+muon2+jet1+jet2).M()
	#if v == '' :
	#	print 'pts:',bjet1.Pt(),bjet2.Pt(),jet1.Pt(),jet2.Pt()
	#	print 'btag scores:', highBtag,secondBtag,jet1Btag,jet2Btag
	
	regr_corrF1 = bjetRegressionCorrectionFactor(RegressionReaderBJet1, _regrvarsnamesBjet1, bjet1, jetinds[highBtagCounter], T, met)
	regr_corrF2 = bjetRegressionCorrectionFactor(RegressionReaderBJet2, _regrvarsnamesBjet2, bjet2, jetinds[secondBtagCounter], T, met)
	regr_bjet1 = TLorentzVector()
	regr_bjet2 = TLorentzVector()
	regr_bjet1.SetPtEtaPhiE(regr_corrF1*bjet1.Pt(), bjet1.Eta(), bjet1.Phi(), regr_corrF1*bjet1.Energy())
	regr_bjet2.SetPtEtaPhiE(regr_corrF2*bjet2.Pt(), bjet2.Eta(), bjet2.Phi(), regr_corrF2*bjet2.Energy())
	#if v == '' : print ' regr_corrF1 ', regr_corrF1, ' regr_corrF2 ', regr_corrF2
	return [bjet1,highBtagCSV,highBtag,bjet2,secondBtagCSV,secondBtag,jet1,jet2,jet3,indRecoBJet1,indRecoBJet2,indRecoJet1,indRecoJet2,indRecoJet3,regr_bjet1,regr_bjet2]

def bjetRegressionCorrectionFactor(RegressionReader, _regrvarsnames, bjet, ind_orig, T, met):
	# see https://github.com/ResonantHbbHgg/bbggTools/blob/master/src/bbggJetRegression.cc#L229
	_regrvarsnames['Jet_pt'][0]				= bjet.Pt()
	_regrvarsnames['Jet_corr'][0]			= T.PFJetPtAK4CHS[ind_orig]/T.PFJetPtRawAK4CHS[ind_orig]
	_regrvarsnames['Jet_eta'][0]			= bjet.Eta()
	_regrvarsnames['Jet_mt'][0]				= T.PFJetMtAK4CHS[ind_orig]
	_regrvarsnames['Jet_leadTrackPt'][0]	= T.PFJetLeadTrackPtAK4CHS[ind_orig]
	_regrvarsnames['Jet_leptonPtRel'][0]	= T.PFJetSoftLepRatioAK4CHS[ind_orig]
	_regrvarsnames['Jet_leptonPt'][0]		= T.PFJetSoftLepPtAK4CHS[ind_orig]
	_regrvarsnames['Jet_leptonDeltaR'][0]	= T.PFJetSoftLepDrAK4CHS[ind_orig] # default is 0 ==> ok
	_regrvarsnames['Jet_totHEF'][0]			= T.PFJetChargedHadronEnergyFractionAK4CHS[ind_orig]+T.PFJetNeutralHadronEnergyFractionAK4CHS[ind_orig]
	_regrvarsnames['Jet_neEmEF'][0]			= T.PFJetNeutralEmEnergyFractionAK4CHS[ind_orig]
	_regrvarsnames['Jet_vtxPt'][0]			= math.sqrt(T.PFJetVtxPxAK4CHS[ind_orig]*T.PFJetVtxPxAK4CHS[ind_orig] + T.PFJetVtxPyAK4CHS[ind_orig]*T.PFJetVtxPyAK4CHS[ind_orig])
	_regrvarsnames['Jet_vtxMass'][0]		= T.PFJetVtxMassAK4CHS[ind_orig]
	_regrvarsnames['Jet_vtx3dL'][0]			= T.PFJetVtx3DValAK4CHS[ind_orig]
	_regrvarsnames['Jet_vtxNtrk'][0]		= T.PFJetVtxNtracksAK4CHS[ind_orig]
	if(T.PFJetVtx3DSigAK4CHS[ind_orig] == 0):
		_regrvarsnames['Jet_vtx3deL'][0]	= 0
	else:
		_regrvarsnames['Jet_vtx3deL'][0]	= T.PFJetVtx3DValAK4CHS[ind_orig]/T.PFJetVtx3DSigAK4CHS[ind_orig]
	_regrvarsnames['nPVs'][0]				= CountVertices(T)
	_regrvarsnames['Jet_PFMET'][0]			= T.PFMETType1Cor[0]
	_regrvarsnames['Jet_METDPhi'][0]		= bjet.DeltaPhi(met) # range from mpi to pi

	# calculate corr factor
	RegressedValues = RegressionReader.EvaluateRegression("BDTG method")
	regr_corrF = RegressedValues[0]

#	if v == '' :
#		print ' Calculation of regression corr factor '
#		print ' Jet_pt ', _regrvarsnames['Jet_pt'][0]
#		print ' Jet_corr ', _regrvarsnames['Jet_corr'][0]
#		print ' Jet_eta ', _regrvarsnames['Jet_eta'][0]
#		print ' Jet_mt ', _regrvarsnames['Jet_mt'][0]
#		print ' Jet_leadTrackPt ', _regrvarsnames['Jet_leadTrackPt'][0]
#		print ' Jet_leptonPtRel ', _regrvarsnames['Jet_leptonPtRel'][0]
#		print ' Jet_leptonPt ', _regrvarsnames['Jet_leptonPt'][0]
#		print ' Jet_leptonDeltaR ', _regrvarsnames['Jet_leptonDeltaR'][0]
#		print ' Jet_totHEF ', _regrvarsnames['Jet_totHEF'][0]
#		print ' Jet_neEmEF ', _regrvarsnames['Jet_neEmEF'][0]
#		print ' Jet_vtxPt ', _regrvarsnames['Jet_vtxPt'][0], T.PFJetVtxPxAK4CHS[ind_orig], T.PFJetVtxPyAK4CHS[ind_orig]
#		print ' Jet_vtxMass ', _regrvarsnames['Jet_vtxMass'][0]
#		print ' Jet_vtx3dL ', _regrvarsnames['Jet_vtx3dL'][0]
#		print ' Jet_vtxNtrk ', _regrvarsnames['Jet_vtxNtrk'][0]
#		print ' Jet_vtx3deL ', _regrvarsnames['Jet_vtx3deL'][0]
#		print ' nPVs ', _regrvarsnames['nPVs'][0]
#		print ' Jet_PFMET ', _regrvarsnames['Jet_PFMET'][0]
#		print ' Jet_METDPhi ', _regrvarsnames['Jet_METDPhi'][0]
#		print ' regr_corrF ', regr_corrF
	return regr_corrF

def calculateBDTdiscriminant(reader, classifierTag, _bdtvarnames, _cosThetaStarMu, _Mbb_H, _phi0, _ptmu1, _ptmu2, bscoreMVA1, _dRbb_H, _dRjj_Z, _DRuu, _Muu4j, _Muu, _Mjj_Z,
							 _isMuonEvent, _Pt_Hjet1, _Pt_Hjet2, _Pt_Zjet1, _Pt_Zjet2, bscoreMVA2, _bMVAj1, _bMVAj2, _qmu1, _qmu2,
							 _cosTheta_hbb, _cosTheta_zuu_hzz, _dRuubb_H) :
	
	if 'abs(cosThetaStarMu)' in _bdtvarnames: _bdtvarnames['abs(cosThetaStarMu)'][0]	= math.fabs(_cosThetaStarMu)
	if 'Mbb_H'               in _bdtvarnames: _bdtvarnames['Mbb_H'][0]					= _Mbb_H
	if 'abs(phi0)'           in _bdtvarnames: _bdtvarnames['abs(phi0)'][0]				= math.fabs(_phi0)
	if 'Pt_muon1'            in _bdtvarnames: _bdtvarnames['Pt_muon1'][0]				= _ptmu1
	if 'Pt_muon2'            in _bdtvarnames: _bdtvarnames['Pt_muon2'][0]				= _ptmu2
	if 'CMVA_bjet1'          in _bdtvarnames: _bdtvarnames['CMVA_bjet1'][0]				= bscoreMVA1
	if 'DR_bb_H'             in _bdtvarnames: _bdtvarnames['DR_bb_H'][0]				= _dRbb_H
	if 'DR_jj_Z'             in _bdtvarnames: _bdtvarnames['DR_jj_Z'][0]				= _dRjj_Z
	if 'DR_muon1muon2'       in _bdtvarnames: _bdtvarnames['DR_muon1muon2'][0]			= _DRuu
	if 'M_uu4j'              in _bdtvarnames: _bdtvarnames['M_uu4j'][0]					= _Muu4j
	if 'M_uu'                in _bdtvarnames: _bdtvarnames['M_uu'][0]					= _Muu
	if 'Mjj_Z'               in _bdtvarnames: _bdtvarnames['Mjj_Z'][0]					= _Mjj_Z
	
	if 'CMVA_bjet2'          in _bdtvarnames: _bdtvarnames['CMVA_bjet2'][0]				= bscoreMVA2
	if 'cosTheta_hbb'        in _bdtvarnames: _bdtvarnames['cosTheta_hbb'][0]			= _cosTheta_hbb
	if 'cosTheta_zuu_hzz'    in _bdtvarnames: _bdtvarnames['cosTheta_zuu_hzz'][0]		= _cosTheta_zuu_hzz
	if 'DR_uu_bb_H'          in _bdtvarnames: _bdtvarnames['DR_uu_bb_H'][0]				= _dRuubb_H
	
	# calculate BDT disriminator
	out_bdtdisc = -999.
	# preselections
	if (_ptmu1 > 20 and _ptmu2 > 10 and _Pt_Hjet1 > 20 and _Pt_Hjet2 > 20 and _Pt_Zjet1 > 20 and _Pt_Zjet2 > 20 and _Muu > 12 and _isMuonEvent and (_qmu1*_qmu2) < 0 and ((bscoreMVA1>-0.5884)+(bscoreMVA2>-0.5884)+(_bMVAj1>-0.5884)+(_bMVAj2>-0.5884)) > 0) :
		out_bdtdisc = reader.EvaluateMVA(classifierTag)
	#if v == '' : print ' out_bdtdisc ', out_bdtdisc
	return out_bdtdisc


def getCosThetaStar_CS(h1, h2, ebeam = 6500.) :
	#cos theta star angle in the Collins Soper frame
	p1, p2, hh = TLorentzVector(), TLorentzVector(), TLorentzVector()
	p1.SetPxPyPzE(0, 0,  ebeam, ebeam)
	p2.SetPxPyPzE(0, 0, -ebeam, ebeam)
	hh = h1 + h2
	boost = TVector3(- hh.BoostVector())	
	#boost = - hh.BoostVector();
	p1.Boost(boost)
	p2.Boost(boost)
	h1.Boost(boost)
	#TVector3 CSaxis = p1.Vect().Unit() - p2.Vect().Unit()
	CSaxis = TVector3(p1.Vect().Unit() - p2.Vect().Unit())
	CSaxis.Unit()
	
	return math.cos(   CSaxis.Angle( h1.Vect().Unit() )    )

def HelicityCosTheta(Booster, Boosted) :
	BoostVector = TVector3( Booster.BoostVector() )
	Boosted.Boost( -BoostVector.x(), -BoostVector.y(), -BoostVector.z() )
	return Boosted.CosTheta()

def HelicityCosTheta2(Booster, Boosted) :
	BoostVector = TVector3( - Booster.BoostVector() )
	Boosted.Boost( BoostVector )
	return Boosted.CosTheta()

def CosThetaAngles(Hj1, Hj2, Zj1, Zj2, mu1, mu2) :
	bb, zz, diHiggsCandidate = TLorentzVector(), TLorentzVector(), TLorentzVector()
	zz = Zj1 + Zj2 + mu1 + mu2
	bb = Hj1 + Hj2
	diHiggsCandidate = Hj1 + Hj2 + Zj1 + Zj2 + mu1 + mu2
	
	helicityThetas = []
	BoostedHgg, HHforBoost = TLorentzVector(), TLorentzVector()
	HHforBoost.SetPtEtaPhiE(diHiggsCandidate.Pt(), diHiggsCandidate.Eta(), diHiggsCandidate.Phi(), diHiggsCandidate.Energy())
	BoostedHgg.SetPtEtaPhiE(zz.Pt(), zz.Eta(), zz.Phi(), zz.Energy())
	helicityThetas.append( HelicityCosTheta(HHforBoost, BoostedHgg) ) # CosThetaStar

	BoostedLeadingJet, HbbforBoost = TLorentzVector(), TLorentzVector()
	HbbforBoost.SetPtEtaPhiE(bb.Pt(), bb.Eta(), bb.Phi(), bb.Energy())
	if (Hj1.Pt() >= Hj2.Pt()) : # is this leading jet ?
		BoostedLeadingJet.SetPtEtaPhiE(Hj1.Pt(), Hj1.Eta(), Hj1.Phi(), Hj1.Energy())
	else :
		BoostedLeadingJet.SetPtEtaPhiE(Hj2.Pt(), Hj2.Eta(), Hj2.Phi(), Hj2.Energy())
	helicityThetas.append( HelicityCosTheta(HbbforBoost, BoostedLeadingJet) ) # CosTheta_hbb


	BoostedZjj, BoostedZuu, BoostedLeadingZj, BoostedLeadingZu, HzzforBoost = TLorentzVector(), TLorentzVector(), TLorentzVector(), TLorentzVector(), TLorentzVector()
	HzzforBoost.SetPtEtaPhiE(zz.Pt(), zz.Eta(), zz.Phi(), zz.Energy())

	BoostedZjj.SetPtEtaPhiE((Zj1+Zj2).Pt(), (Zj1+Zj2).Eta(), (Zj1+Zj2).Phi(), (Zj1+Zj2).Energy())
	#if v == '': print 'before:', BoostedZjj.Pt(), BoostedZjj.Eta()
	helicityThetas.append( HelicityCosTheta(HzzforBoost, BoostedZjj) ) # CosTheta_zjj_hzz
	#if v == '': print 'after :', BoostedZjj.Pt(), BoostedZjj.Eta()

	BoostedZuu.SetPtEtaPhiE((mu1 + mu2).Pt(), (mu1 + mu2).Eta(), (mu1 + mu2).Phi(), (mu1 + mu2).Energy())
	helicityThetas.append( HelicityCosTheta(HzzforBoost, BoostedZuu) ) # CosTheta_zuu_hzz

	BoostedLeadingZj.SetPtEtaPhiE(Zj1.Pt(), Zj1.Eta(), Zj1.Phi(), Zj1.Energy())
	helicityThetas.append( HelicityCosTheta(HzzforBoost, BoostedLeadingZj) ) # CosTheta_zj1_hzz
	#if v == '': print 'CosTheta_zz:', helicityThetas[2], 'CosTheta_zz_test', helicityThetas[3]
	
	BoostedLeadingZu.SetPtEtaPhiE(mu1.Pt(), mu1.Eta(), mu1.Phi(), mu1.Energy())
	helicityThetas.append( HelicityCosTheta(HzzforBoost, BoostedLeadingZu) ) # CosTheta_zu1_hzz
	
	return helicityThetas

def CosThetaAngles_ZZ(Zj1, Zj2, mu1, mu2) :
	zz = TLorentzVector()
	zz = Zj1 + Zj2 + mu1 + mu2
	zjj = Zj1 + Zj2
	zmumu = mu1 + mu2
	
	helicityThetas = []
	
	ZZforBoost, BoostedZuu, BoostedZjj = TLorentzVector(), TLorentzVector(), TLorentzVector()
	ZZforBoost.SetPtEtaPhiE(zz.Pt(), zz.Eta(), zz.Phi(), zz.Energy())
	
	BoostedZuu.SetPtEtaPhiE(zmumu.Pt(), zmumu.Eta(), zmumu.Phi(), zmumu.Energy())
	helicityThetas.append( HelicityCosTheta(ZZforBoost, BoostedZuu) ) # CosThetaStar_Zuu

	BoostedZjj.SetPtEtaPhiE(zjj.Pt(), zjj.Eta(), zjj.Phi(), zjj.Energy())
	helicityThetas.append( HelicityCosTheta(ZZforBoost, BoostedZjj) ) # CosThetaStar_Zjj
	
	return helicityThetas

def norm_planes_hi(partons, dihiggs) :
	boost_H = TVector3( - dihiggs.BoostVector() )

	partons3v = []
	for i in range(len(partons)) :
		partons_i_boosted = TLorentzVector()
		partons_i_boosted = partons[i]
		partons_i_boosted.Boost(boost_H)
		partons3v.append( partons_i_boosted.Vect().Unit() )
	
	vnorm = []
	R = TRandom()
	for i in range(2) :
		rndm = R.Uniform(1)
		#if v == '': print 'i:', i, 'rndm', rndm
		if (rndm > 0.5) :
			vnorm.append( (partons3v[i*2].Cross(partons3v[i*2+1])).Unit() )
		else :
			vnorm.append( -1*(partons3v[i*2].Cross(partons3v[i*2+1])).Unit() )

	return vnorm

def getPhi(Hj1, Hj2, Zj1, Zj2, mu1, mu2) :
	vPhi = []
	if (Hj1.Pt()<=0. or Hj2.Pt()<=0. or Zj1.Pt()<=0. or Zj2.Pt()<=0. or mu1.Pt()<=0. or mu2.Pt()<=0.) :
		vPhi.append(-3.5)
		vPhi.append(-3.5)
	else :
		zz, diHiggsCandidate = TLorentzVector(), TLorentzVector()
		zz = Zj1 + Zj2 + mu1 + mu2
		diHiggsCandidate = Hj1 + Hj2 + Zj1 + Zj2 + mu1 + mu2
		
		partons = []
		partons.append(Zj1 + Zj2) #leadingPhoton
		partons.append(mu1 + mu2) #subleadingPhoton
		partons.append(Hj1) #leadingJet
		partons.append(Hj2) #subleadingJet
		
		# Define hzz direction
		hzz = TLorentzVector()
		hzz = Zj1 + Zj2 + mu1 + mu2
		
		boost_H = TVector3( - diHiggsCandidate.BoostVector() )
		hzz.Boost(boost_H);
		
		hzz_vect = TVector3( hzz.Vect().Unit() ) # hzz_vect has been boosted
		#hzz_vect_nobst = TVector3( zz.Vect().Unit() ) # hzz_vect_nobst has not been boosted
		
		#if v == '': print 'hzz_vect       :', hzz_vect.Pt(), hzz_vect.Eta(), hzz_vect.Phi()
		#if v == '': print 'hzz_vect_nobst :', hzz_vect_nobst.Pt(), hzz_vect_nobst.Eta(), hzz_vect_nobst.Phi()
		
		# Calculate the normal to Hzz and hbb decay plane
		vnorm = norm_planes_hi(partons, diHiggsCandidate)
		
		# Calculate Phi
		dsignhgg = hzz_vect.Dot(vnorm[1].Cross(vnorm[0]))/(abs(hzz_vect.Dot(vnorm[1].Cross(vnorm[0])))) # hzz_vect here is not important
		vPhi.append( dsignhgg*(-1) * math.acos(vnorm[0].Dot(vnorm[1])) )
		
		# Define z direction
		p1 = TLorentzVector()
		p1.SetPxPyPzE(0, 0,  6500, 6500)
		z_vect = TVector3( p1.Vect().Unit() )
		
		# Calcuate the normal to Hzz and z-direction plane
		zzprime = TVector3((z_vect.Cross(hzz_vect)).Unit())
		#zzprime = TVector3((z_vect.Cross(hzz_vect_nobst)).Unit())
		
		# Calculate Phi1
		dsignhgg2 = hzz_vect.Dot(zzprime.Cross(vnorm[0]))/(abs(hzz_vect.Dot(zzprime.Cross(vnorm[0]))))  # hzz_vect here is not important
		vPhi.append( dsignhgg2 * math.acos(zzprime.Dot(vnorm[0])) )
	
	return vPhi

def getPhi_ZZ(Zj1, Zj2, mu1, mu2) :
	vPhi = []
	if (Zj1.Pt()<=0. or Zj2.Pt()<=0. or mu1.Pt()<=0. or mu2.Pt()<=0.) :
		vPhi.append(-3.5)
		vPhi.append(-3.5)
		vPhi.append(-3.5)
	else :
		zz = TLorentzVector()
		zz = Zj1 + Zj2 + mu1 + mu2
		
		partons = []
		partons.append(mu1) #leadingPhoton
		partons.append(mu2) #subleadingPhoton
		partons.append(Zj1) #leadingJet
		partons.append(Zj2) #subleadingJet
		
		# Define Zuu direction
		zuu = TLorentzVector()
		zuu = mu1 + mu2

		boost_ZZ = TVector3( - zz.BoostVector() )
		zuu.Boost(boost_ZZ);
		zuu_vect = TVector3( zuu.Vect().Unit() ) # zuu_vect has been boosted
		
		# Calculate the normal to Zuu and Zjj decay plane
		vnorm = norm_planes_hi(partons, zz)
		
		# Calculate Phi
                #fixme Morse division by zero very small amount of the time
		if abs(zuu_vect.Dot(vnorm[1].Cross(vnorm[0])))>0:
			dsignhgg = zuu_vect.Dot(vnorm[1].Cross(vnorm[0]))/(abs(zuu_vect.Dot(vnorm[1].Cross(vnorm[0])))) # zuu_vect here is NOT important
		else:
			dsignhgg = 0
		vPhi.append( dsignhgg*(-1) * math.acos(vnorm[0].Dot(vnorm[1])) )
		
		# Define z direction
		p1 = TLorentzVector()
		p1.SetPxPyPzE(0, 0,  6500, 6500)
		z_vect = TVector3( p1.Vect().Unit() )
		
		# Calcuate the normal to Zuu and z-direction plane
		zz1prime = TVector3((z_vect.Cross(zuu_vect)).Unit())  # zuu_vect here IS important
		
		# Calculate Phi1_zuu
                #fixme Morse division by zero very small amount of the time
		if abs(zuu_vect.Dot(zz1prime.Cross(vnorm[0])))>0:
			dsignhgg2 = zuu_vect.Dot(zz1prime.Cross(vnorm[0]))/(abs(zuu_vect.Dot(zz1prime.Cross(vnorm[0]))))  # zuu_vect here is NOT important
		else:
			dsignhgg2 = 0
		vPhi.append( dsignhgg2 * math.acos(zz1prime.Dot(vnorm[0])) )
		
		
		# Define Zjj direction
		zjj = TLorentzVector()
		zjj = Zj1 + Zj2
		
		zjj.Boost(boost_ZZ);
		zjj_vect = TVector3( zjj.Vect().Unit() ) # zjj_vect has been boosted

		# Calcuate the normal to Zjj and z-direction plane
		zz2prime = TVector3((z_vect.Cross(zjj_vect)).Unit())  # zjj_vect here IS important
		
		# Calculate Phi1_zjj
		if abs(zjj_vect.Dot(zz2prime.Cross(vnorm[1])))>0:
			dsignhgg2 = zjj_vect.Dot(zz2prime.Cross(vnorm[1]))/(abs(zjj_vect.Dot(zz2prime.Cross(vnorm[1]))))  # zjj_vect here is NOT important
		else:
			dsignhgg2 = 0
		vPhi.append( dsignhgg2 * math.acos(zz2prime.Dot(vnorm[1])) )

	return vPhi



##########################################################################################
###########      FULL CALCULATION OF ALL VARIABLES, REPEATED FOR EACH SYS   ##############
##########################################################################################

def FullKinematicCalculation(T,variation):
	# Purpose: This is the magic function which calculates all kinematic quantities using
	#         the previous functions. It returns them as a simple list of doubles. 
	#         It will be used in the loop over events. The 'variation' argument is passed
	#         along when getting the sets of leptons and jets, so the kinematics will vary.
	#         This function is repeated for all the sytematic variations inside the event
	#         loop. The return arguments ABSOLUELY MUST be in the same order they are 
	#         listed in the branch declarations. Modify with caution.  

	_passWptCut = checkWorZpt(T,0,100,'W')
	_passZptCut = checkWorZpt(T,0,50,'Z')
	_WorZSystemPt = T.GenParticleWorZSystemPt
        #print 'passWptCut:',_passWptCut
        
        #ptHat
	_ptHat = T.PtHat
	# MET as a vector
	met = MetVector(T)
	# ID Muons,Electrons
	[muons,goodmuoninds,met,trkisosMu,chargesMu,dpts,chi2,pfid,layers] = MediumIDMuons(T,met,variation,T.isData)
	#[muons,goodmuoninds,met,trkisosMu,chargesMu,dpts,chi2,pfid,layers] = TightHighPtIDMuons(T,met,variation,T.isData)
	# muons_forjetsep = MuonsForJetSeparation(T)
	# taus_forjetsep = TausForJetSeparation(T)
	#[electrons,electroninds,met] = HEEPElectrons(T,met,variation)
	[electrons,electroninds,met,trkisosEle,chargesEle] = TightElectrons(T,met,variation,T.isData)
	# ID Jets and filter from leptons
	[jets,jetinds,met,failthreshold,neutralhadronEF,neutralemEF,btagCSVscores,btagMVAscores] = LooseIDJets(T,met,variation,T.isData)
	#jetsTemp = jets
	_jetCntPreFilter = len(jets)
	## jets = GeomFilterCollection(jets,muons_forjetsep,0.5)
	
	[jets,btagCSVscores,btagMVAscores,jetinds] = GeomFilterCollection(jets,muons,0.3,btagCSVscores,btagMVAscores,jetinds)#fixme todo was 0.5 - changing to 0.3 following HH->wwbb. In any case 0.5 is too big now that cone size is 0.4 - put back in!
	[jets,btagCSVscores,btagMVAscores,jetinds] = GeomFilterCollection(jets,electrons,0.3,btagCSVscores,btagMVAscores,jetinds)#fixme todo was 0.5 - changing to 0.3 following HH->wwbb. In any case 0.5 is too big now that cone size is 0.4 - put back in!
	
	##[jetsTemp,jetinds] = GeomFilterCollection(jetsTemp,muons,0.3,jetinds)
	##[jetsTemp,jetinds] = GeomFilterCollection(jetsTemp,electrons,0.3,jetinds)
	## jets = GeomFilterCollection(jets,taus_forjetsep,0.5)
	# Empty lorentz vector for bookkeeping
	EmptyLorentz = TLorentzVector()
	EmptyLorentz.SetPtEtaPhiM(0,0,0,0)

	# Muon and Jet Counts
	_mucount = len(muons)
	_elcount = len(electrons)
	_jetcount = len(jets)
	#if v == '': print '_mucount',_mucount,'_elcount',_elcount,'_jetcount',_jetcount

	# Make sure there are two of every object, even if zero
	if len(muons) < 1 : 
		muons.append(EmptyLorentz)
		trkisosMu.append(0.0)
		chargesMu.append(0.0)
		dpts.append(-1.0)
		chi2.append(-1.0)
		pfid.append(-1.0)
		layers.append(-1.0)

	if len(muons) < 2 : 
		muons.append(EmptyLorentz)
		trkisosMu.append(0.0)
		chargesMu.append(0.0)		
		dpts.append(-1.0)
		chi2.append(-1.0)
		pfid.append(-1.0)
		layers.append(-1.0)

	if len(electrons) < 1 : 
		electrons.append(EmptyLorentz)
		trkisosEle.append(0.0)
		chargesEle.append(0.0)
	if len(electrons) < 2 : 
		electrons.append(EmptyLorentz)	
		trkisosEle.append(0.0)
		chargesEle.append(0.0)
	if len(jets) < 1 : 
		jets.append(EmptyLorentz)
		neutralhadronEF.append(0.0)
		neutralemEF.append(0.0)
		btagCSVscores.append(-5.0)
		btagMVAscores.append(-5.0)
		jetinds.append(-1)
	if len(jets) < 2 : 
		jets.append(EmptyLorentz)
		neutralhadronEF.append(0.0)
		neutralemEF.append(0.0)
		btagCSVscores.append(-5.0)
		btagMVAscores.append(-5.0)
		jetinds.append(-1)
	_ismuon_muon1 = 1.0
	_ismuon_muon2 = 1.0

	if emuswitch == True:
		if muons[0].Pt() > electrons[0].Pt():
			muons[1] = electrons[0]
			_ismuon_muon2 = 0.0
		else:
			muons[1] = muons[0]
			muons[0] = eletrons[0]
			_ismuon_muon1=0.0

	[_genMuons,_matchedRecoMuons,muonInd] = MuonsFromLQ(T)
	[_genJets,_matchedRecoJets,jetInd] = JetsFromLQ(T)
	[_genMuonsZ,_matchedRecoMuonsZ,muonIndZ,_genElectronsZ,_matchedRecoElectronsZ,electronIndZ,_genJetsH,_matchedRecoJetsH,jetIndH,_genJetsZ,_matchedRecoJetsZ,jetIndZ,onShellZMu,onShellZEle] = LeptonsAndJetsFromHH(T)

	_muonInd1=muonInd[0]
	_muonInd2=muonInd[1]
	_jetInd1=jetInd[0]
	_jetInd2=jetInd[1]

	[_ptu1_gen,_ptu2_gen] = [_genMuonsZ[0].Pt(),_genMuonsZ[1].Pt()]
	[_ptHj1_gen,_ptHj2_gen,_ptZj1_gen,_ptZj2_gen]=[_genJetsH[0].Pt(),_genJetsH[1].Pt(),_genJetsZ[0].Pt(),_genJetsZ[1].Pt()]
	[_phiHj1_gen,_phiHj2_gen,_phiZj1_gen,_phiZj2_gen]=[_genJetsH[0].Phi(),_genJetsH[1].Phi(),_genJetsZ[0].Phi(),_genJetsZ[1].Phi()]
	[_etaHj1_gen,_etaHj2_gen,_etaZj1_gen,_etaZj2_gen]=[_genJetsH[0].Eta(),_genJetsH[1].Eta(),_genJetsZ[0].Eta(),_genJetsZ[1].Eta()]
	[_ptu1_genMatched,_ptu2_genMatched]=[_matchedRecoMuonsZ[0].Pt(),_matchedRecoMuonsZ[1].Pt()]
	[_ptHj1_genMatched,_ptHj2_genMatched]=[_matchedRecoJetsH[0].Pt(),_matchedRecoJetsH[1].Pt()]
	[_ptZj1_genMatched,_ptZj2_genMatched]=[_matchedRecoJetsZ[0].Pt(),_matchedRecoJetsZ[1].Pt()]
	_dRu1Hj1_gen = abs(_genMuonsZ[0].DeltaR(_genJetsH[0]))
	_dRu1Hj2_gen = abs(_genMuonsZ[0].DeltaR(_genJetsH[1]))
	_dRu1Zj1_gen = abs(_genMuonsZ[0].DeltaR(_genJetsZ[0]))
	_dRu1Zj2_gen = abs(_genMuonsZ[0].DeltaR(_genJetsZ[1]))
	_dRu2Hj1_gen = abs(_genMuonsZ[1].DeltaR(_genJetsH[0]))
	_dRu2Hj2_gen = abs(_genMuonsZ[1].DeltaR(_genJetsH[1]))
	_dRu2Zj1_gen = abs(_genMuonsZ[1].DeltaR(_genJetsZ[0]))
	_dRu2Zj2_gen = abs(_genMuonsZ[1].DeltaR(_genJetsZ[1]))
	_dRu1Hj1_genMatched = abs(_matchedRecoMuonsZ[0].DeltaR(_matchedRecoJetsH[0]))
	_dRu1Hj2_genMatched = abs(_matchedRecoMuonsZ[0].DeltaR(_matchedRecoJetsH[1]))
	_dRu1Zj1_genMatched = abs(_matchedRecoMuonsZ[0].DeltaR(_matchedRecoJetsZ[0]))
	_dRu1Zj2_genMatched = abs(_matchedRecoMuonsZ[0].DeltaR(_matchedRecoJetsZ[1]))
	_dRu2Hj1_genMatched = abs(_matchedRecoMuonsZ[1].DeltaR(_matchedRecoJetsH[0]))
	_dRu2Hj2_genMatched = abs(_matchedRecoMuonsZ[1].DeltaR(_matchedRecoJetsH[1]))
	_dRu2Zj1_genMatched = abs(_matchedRecoMuonsZ[1].DeltaR(_matchedRecoJetsZ[0]))
	_dRu2Zj2_genMatched = abs(_matchedRecoMuonsZ[1].DeltaR(_matchedRecoJetsZ[1]))


	leptons=_genLeptonsZ=_matchedRecoLeptonsZ=[]
	_isMuonEvent,_isElectronEvent = False,False
	if muons[0].Pt()>=electrons[0].Pt() or electrons[1].Pt()<1:#prioritize muons: cases where muon1 pt > ele1 pt, or where there is no 2nd electron
		if electrons[0]>16 and electrons[1]>8 and muons[1]<8:#single case where first muon pt is higher, but there is only one good muon and 2 valid electrons
			leptons = electrons
			charges = chargesEle
			trkisos = trkisosEle
			_genLeptonsZ=_genElectronsZ
			_matchedRecoLeptonsZ=_matchedRecoElectronsZ
			_isElectronEvent=True
		else:
			leptons = muons
			charges = chargesMu
			trkisos = trkisosMu
			_genLeptonsZ=_genMuonsZ
			_matchedRecoLeptonsZ=_matchedRecoMuonsZ
			_isMuonEvent=True
	else:#cases where ele1 pt > muon1 pt
		if muons[0]>16 and muons[1]>8 and electrons[1]<8:#single case where first electron pt is higher, but there is only one good electron and 2 valid muons
			leptons = muons
			charges = chargesMu
			trkisos = trkisosMu
			_genLeptonsZ=_genMuonsZ
			_matchedRecoLeptonsZ=_matchedRecoMuonsZ
			_isMuonEvent=True
		else:
			leptons = electrons
			charges = chargesEle
			trkisos = trkisosEle
			_genLeptonsZ=_genElectronsZ
			_matchedRecoLeptonsZ=_matchedRecoElectronsZ
			_isElectronEvent=True


	# Get kinematic quantities
	[_ptmu1,_etamu1,_phimu1,_isomu1,_qmu1,_dptmu1] = [muons[0].Pt(),muons[0].Eta(),muons[0].Phi(),trkisosMu[0],chargesMu[0],dpts[0]]
	[_ptmu2,_etamu2,_phimu2,_isomu2,_qmu2,_dptmu2] = [muons[1].Pt(),muons[1].Eta(),muons[1].Phi(),trkisosMu[1],chargesMu[1],dpts[1]]

	[_chimu1,_chimu2] = [chi2[0],chi2[1]]
	[_ispfmu1,ispfmu2] = [pfid[0],pfid[1]]
	[_layersmu1,_layersmu2] = [layers[0],layers[1]]

	[_ptele1,_etaele1,_phiele1,_isoele1,_qele1] = [electrons[0].Pt(),electrons[0].Eta(),electrons[0].Phi(),trkisosEle[0],chargesEle[0]]
	[_ptele2,_etaele2,_phiele2,_isoele2,_qele2] = [electrons[1].Pt(),electrons[1].Eta(),electrons[1].Phi(),trkisosEle[1],chargesEle[1]]

	[_ptlep1,_etalep1,_philep1,_isolep1,_qlep1] = [leptons[0].Pt(),leptons[0].Eta(),leptons[0].Phi(),trkisos[0],charges[0]]
	[_ptlep2,_etalep2,_philep2,_isolep2,_qlep2] = [leptons[1].Pt(),leptons[1].Eta(),leptons[1].Phi(),trkisos[1],charges[1]]

	[_ptj1,_etaj1,_phij1]    = [jets[0].Pt(),jets[0].Eta(),jets[0].Phi()]
	[_ptj2,_etaj2,_phij2]    = [jets[1].Pt(),jets[1].Eta(),jets[1].Phi()]
	[_ptj3,_ptj4] = [0.,0.]
	if len(jets) > 2 :
		_ptj3 = jets[2].Pt()
	if len(jets) > 3 :
		_ptj4 = jets[3].Pt()

	[_nhefj1,_nhefj2,_nemefj1,_nemefj2] = [neutralhadronEF[0],neutralhadronEF[1],neutralemEF[0],neutralemEF [1]]
	[_ptmet,_etamet,_phimet] = [met.Pt(),0,met.Phi()]
	[_xmiss,_ymiss] = [met.Px(),met.Py()]
	[_CSVj1,_CSVj2] = [btagCSVscores[0],btagCSVscores[1]]
	[_bMVAj1,_bMVAj2] = [btagMVAscores[0],btagMVAscores[1]]

	_stuujj = ST([muons[0],muons[1],jets[0],jets[1]])

	_steejj = ST([electrons[0],electrons[1],jets[0],jets[1]])

	_stlljj = ST([leptons[0],leptons[1],jets[0],jets[1]])

	_Muu = (muons[0]+muons[1]).M()
	_MTuv = TransMass(muons[0],met)
	_Mjj = (jets[0]+jets[1]).M()
	_DRuu = (muons[0]).DeltaR(muons[1])
	_DPHIuv = abs((muons[0]).DeltaPhi(met))
	_DPHIj1v = abs((jets[0]).DeltaPhi(met))
	_DPHIj2v = abs((jets[1]).DeltaPhi(met))

	_Mee = (electrons[0]+electrons[1]).M()
	_DRee = (electrons[0]).DeltaR(electrons[1])
	_DPHIev = abs((electrons[0]).DeltaPhi(met))

	_Mll = (leptons[0]+leptons[1]).M()
	_DRll = (leptons[0]).DeltaR(leptons[1])

	_DRu1j1 = abs(muons[0].DeltaR(jets[0]))
	_DRu1j2 = abs(muons[0].DeltaR(jets[1]))
	_DRu2j1 = abs(muons[1].DeltaR(jets[0]))
	_DRu2j2 = abs(muons[1].DeltaR(jets[1]))

	_DRj1j2   = abs(jets[0].DeltaR(jets[1]))
	_DPhij1j2 = abs(jets[0].DeltaPhi(jets[1]))

	_DPhiu1j1 = abs(muons[0].DeltaPhi(jets[0]))
	_DPhiu1j2 = abs(muons[0].DeltaPhi(jets[1]))
	_DPhiu2j1 = abs(muons[1].DeltaPhi(jets[0]))
	_DPhiu2j2 = abs(muons[1].DeltaPhi(jets[1]))

	_DRe1j1 = abs(electrons[0].DeltaR(jets[0]))
	_DRe1j2 = abs(electrons[0].DeltaR(jets[1]))
	_DRe2j1 = abs(electrons[1].DeltaR(jets[0]))
	_DRe2j2 = abs(electrons[1].DeltaR(jets[1]))
	_DPhie1j1 = abs(electrons[0].DeltaPhi(jets[0]))
	_DPhie1j2 = abs(electrons[0].DeltaPhi(jets[1]))
	_DPhie2j1 = abs(electrons[1].DeltaPhi(jets[0]))
	_DPhie2j2 = abs(electrons[1].DeltaPhi(jets[1]))

	_DRl1j1 = abs(leptons[0].DeltaR(jets[0]))
	_DRl1j2 = abs(leptons[0].DeltaR(jets[1]))
	_DRl2j1 = abs(leptons[1].DeltaR(jets[0]))
	_DRl2j2 = abs(leptons[1].DeltaR(jets[1]))
	_DPhil1j1 = abs(leptons[0].DeltaPhi(jets[0]))
	_DPhil1j2 = abs(leptons[0].DeltaPhi(jets[1]))
	_DPhil2j1 = abs(leptons[1].DeltaPhi(jets[0]))
	_DPhil2j2 = abs(leptons[1].DeltaPhi(jets[1]))

	_Muu_gen=0
	_Muu_genMatched=0


	if len(electrons)>=1 :
		_pte1 = electrons[0].Pt()
		if len(electrons)>=2 : _pte2 = electrons[1].Pt()
		else : _pte2 = 0.
	else :
		_pte1 = 0.


	[bjet1,bscore1,bscoreMVA1,bjet2,bscore2,bscoreMVA2,jet1,jet2,jet3,indRecoBJet1,indRecoBJet2,indRecoJet1,indRecoJet2,indRecoJet3] = [EmptyLorentz,-5.0,-5.0,EmptyLorentz,-5.0,-5.0,EmptyLorentz,EmptyLorentz,EmptyLorentz,-1,-1,-1,-1,-1]
	[unreg_bjet1,unreg_bjet2] = [EmptyLorentz,EmptyLorentz]

	#[bjet1,bscore1,bscoreMVA1,bjet2,bscore2,bscoreMVA2,jet1,jet2,jet3,indRecoBJet1,indRecoBJet2,indRecoJet1,indRecoJet2,indRecoJet3] = GetHHJetsOld(jets,btagCSVscores,btagMVAscores,muons[0],muons[1],jetinds, T)
	#[bjet1,bscore1,bscoreMVA1,bjet2,bscore2,bscoreMVA2,jet1,jet2,jet3,indRecoBJet1,indRecoBJet2,indRecoJet1,indRecoJet2,indRecoJet3,regr_bjet1,regr_bjet2] = GetHHJetsNew(jets,btagCSVscores,btagMVAscores,muons[0],muons[1],jetinds, T, met)
	[unreg_bjet1,bscore1,bscoreMVA1,unreg_bjet2,bscore2,bscoreMVA2,jet1,jet2,jet3,indRecoBJet1,indRecoBJet2,indRecoJet1,indRecoJet2,indRecoJet3,bjet1,bjet2] = GetHHJetsNew(jets,btagCSVscores,btagMVAscores,muons[0],muons[1],jetinds, T, met)

	"""
	#if muons[0].Pt()>20 and muons[1].Pt()>10 and variation=='':
	if variation=='':
		print '    bjet1score, bjet2score, Hmass, Zmass, ZMuMass, uu4jMass, indexbj1, indexbj2, indexj1, indexj2, indexj3 '
		print '1: ',bscore1,bscore2,(bjet1+bjet2).M(),(jet1+jet2).M(),(muons[0]+muons[1]).M(),(muons[0]+muons[1]+jet1+jet2).M(),indRecoBJet1,indRecoBJet2,indRecoJet1,indRecoJet2,indRecoJet3,bjet1.Pt(),bjet2.Pt(),jet1.Pt(),jet2.Pt(),jet3.Pt(), ' ' ,jetIndH[0],jetIndH[1],jetIndZ[0],jetIndZ[1]
		
		print '2: ',bscore1_2,bscore2_2,(bjet1_2+bjet2_2).M(),(jet1_2+jet2_2).M(),(muons[0]+muons[1]).M(),(muons[0]+muons[1]+jet1_2+jet2_2).M()
		print '3: ',bscore1_3,bscore2_3,(bjet1_3+bjet2_3).M(),(jet1_3+jet2_3).M(),(muons[0]+muons[1]).M(),(muons[0]+muons[1]+jet1_3+jet2_3).M()
		print ''
	"""
	
	CorHj1Avail,CorHj2Avail  = False,False
	CorZj1Avail,CorZj2Avail  = False,False
	for j in jetinds :
		if jetIndH[0] == j: CorHj1Avail=True
		if jetIndH[1] == j: CorHj2Avail=True
		if jetIndZ[0] == j: CorZj1Avail=True
		if jetIndZ[1] == j: CorZj2Avail=True

	_CorHj1j2Avail = CorHj1Avail and CorHj2Avail
	_CorZj1j2Avail = CorZj1Avail and CorZj2Avail
	
	[_bscoreMVA1_genMatched, _bscoreMVA2_genMatched, tempBscore1, tempBscore2] = [-5.0,-5.0,-5.0,-5.0]
	if jetIndH[0] >= 0 :
		tempBscore1 = T.PFJetCombinedMVABTagAK4CHS[jetIndH[0]]
		_bscoreMVA1_genMatched = T.PFJetCombinedMVABTagAK4CHS[jetIndH[0]]
	if jetIndH[1] >= 0 :
		tempBscore2 = T.PFJetCombinedMVABTagAK4CHS[jetIndH[1]]
		_bscoreMVA2_genMatched = T.PFJetCombinedMVABTagAK4CHS[jetIndH[1]]
	if tempBscore1 < tempBscore2 : # becareful if you want to do this. I have NOT re-ordered all variables.
		_bscoreMVA1_genMatched = tempBscore2
		_bscoreMVA2_genMatched = tempBscore1

	[_Hj1Matched,_Hj2Matched,_Zj1Matched,_Zj2Matched] = [0,0,0,0]
	if indRecoBJet1 == jetIndH[0] or indRecoBJet1 == jetIndH[1]: _Hj1Matched=1
	if indRecoBJet2 == jetIndH[1] or indRecoBJet2 == jetIndH[0]: _Hj2Matched=1
	if indRecoJet1  == jetIndZ[0] or indRecoJet1  == jetIndZ[1]: _Zj1Matched=1
	if indRecoJet2  == jetIndZ[1] or indRecoJet2  == jetIndZ[0]: _Zj2Matched=1
	[_Hj1Present,_Hj2Present,_Zj1Present,_Zj2Present]=[ bjet1.Pt()>0, bjet2.Pt()>0, jet1.Pt()>0, jet2.Pt()>0 ]

	#if v == '' : print 'CorHj1Avail',CorHj1Avail,'CorHj2Avail',CorHj2Avail,'CorHj1j2Avail',_CorHj1j2Avail
	#if jetIndH[0] >= 0 and jetIndH[1] >= 0 and jetIndZ[0] >= 0 and jetIndZ[1] >= 0 :
	#if jetIndH[0] >= 0 and jetIndH[1] >= 0 and _CorHj1j2Avail and (not (_Hj1Matched and _Hj2Matched)) and len(goodmuoninds) >= 2:
	
#	if jetIndH[0] >= 0 and jetIndH[1] >= 0 and _CorHj1j2Avail and len(goodmuoninds) >= 2:
#
#		if v == '' :
#			print ' dR gen jet:', abs(_genJetsH[0].DeltaR(_genJetsH[1]))
#			for i in range(len(jets)) :
#				if T.PFJetPartonFlavourAK4CHS[jetinds[i]] == 21: continue
#				#if T.PFJetCombinedInclusiveSecondaryVertexBTagAK4CHS[jetinds[i]] < 0.06: continue
#				print '   After Filter Recojet index',jetinds[i], 'flavor', T.PFJetPartonFlavourAK4CHS[jetinds[i]],  'pt',jets[i].Pt(),'eta',jets[i].Eta(), 'phi',jets[i].Phi() ,'btagScores', btagMVAscores[i], 'CSVScore', btagCSVscores[i], 'pileupMVA',T.PFJetPileupMVAAK4CHS[jetinds[i]], T.PFJetPileupMVApassesLooseAK4CHS[jetinds[i]],T.PFJetPileupMVApassesMediumAK4CHS[jetinds[i]],T.PFJetPileupMVApassesTightAK4CHS[jetinds[i]]
#
#			print 'matched bjet indices:',jetIndH
#			print 'matched  jet indices:',jetIndZ
#			print 'reco     jet indices:',jetinds
#			print 'getHH    jet indices:',indRecoBJet1,indRecoBJet2,indRecoJet1,indRecoJet2
#			print ''
#			print 'good muons   indices:',goodmuoninds
#			print 'good elects  indices:',electroninds
#			print ''


	[_Muu4j,_Mee4j,_Mll4j] = [0., 0., 0.]
	#if len(jets)>=4 and ( len(muons)>=2 or len(electrons)>=2 ):
	#	if len(muons)>=2 :
	#		_Muu4j = (muons[0]+muons[1]+jets[0]+jets[1]+jets[2]+jets[3]).M()
	#	if len(electrons)>=2 :
	#		_Mee4j = (electrons[0]+electrons[1]+jets[0]+jets[1]+jets[2]+jets[3]).M()
	#	if _ptmu1 > _pte1 and len(muons)>=2:
	#		_Mll4j = (muons[0]+muons[1]+jets[0]+jets[1]+jets[2]+jets[3]).M()
	#	elif _pte1 > _ptmu1 and len(electrons)>=2 :
	#		_Mll4j = (electrons[0]+electrons[1]+jets[0]+jets[1]+jets[2]+jets[3]).M()
	_Muu4j = (muons[0]+muons[1]+bjet1+bjet2+jet1+jet2).M()
	_Mee4j = (electrons[0]+electrons[1]+bjet1+bjet2+jet1+jet2).M()
	_Mll4j = (leptons[0]+leptons[1]+bjet1+bjet2+jet1+jet2).M()
	_Muujj = (muons[0]+muons[1]+jet1+jet2).M()
	_Meejj = (electrons[0]+electrons[1]+jet1+jet2).M()
	_Mlljj = (leptons[0]+leptons[1]+jet1+jet2).M()
	_Mbb_H = (bjet1+bjet2).M()
	_Mbb_H_orig = (unreg_bjet1+unreg_bjet2).M()
	_Muu4j_orig = (muons[0]+muons[1]+unreg_bjet1+unreg_bjet2+jet1+jet2).M()
	_dRbb_H = abs(bjet1.DeltaR(bjet2))
	_dPhibb_H = abs(bjet1.DeltaPhi(bjet2))
	_Mjj_Z = (jet1+jet2).M()
	_Mjj_Z_3jet = min(abs((jet1+jet2).M()-91.),abs((jet1+jet3).M()-91.),abs((jet2+jet3).M()-91.))
	_dRjj_Z = abs(jet1.DeltaR(jet2))
	_dPhijj_Z = abs(jet1.DeltaPhi(jet2))
	_dRu1Hj1 = abs(muons[0].DeltaR(bjet1))
	_dRu1Hj2 = abs(muons[0].DeltaR(bjet2))
	_dRu1Zj1 = abs(muons[0].DeltaR(jet1))
	_dRu1Zj2 = abs(muons[0].DeltaR(jet2))
	_dRu2Hj1 = abs(muons[1].DeltaR(bjet1))
	_dRu2Hj2 = abs(muons[1].DeltaR(bjet2))
	_dRu2Zj1 = abs(muons[1].DeltaR(jet1))
	_dRu2Zj2 = abs(muons[1].DeltaR(jet2))
	
	_stuu4j = ST([muons[0],muons[1],bjet1,bjet2,jet1,jet2])
	_stee4j = ST([electrons[0],electrons[1],bjet1,bjet2,jet1,jet2])
	_stll4j = ST([leptons[0],leptons[1],bjet1,bjet2,jet1,jet2]) 
	[_Pt_origHjet1,_Pt_origHjet2] = [unreg_bjet1.Pt(),unreg_bjet2.Pt()] # keep only the original bjets pt
	[_Pt_Hjet1,_Pt_Hjet2,_Pt_Zjet1,_Pt_Zjet2] = [bjet1.Pt(),bjet2.Pt(),jet1.Pt(),jet2.Pt()]
	[_Pt_Hjets,_Pt_Zjets] = [(bjet1+bjet2).Pt(),(jet1+jet2).Pt()]
	[_Pt_uu,_Pt_ee,_Pt_ll] = [(muons[0]+muons[1]).Pt(),(electrons[0]+electrons[1]).Pt(),(leptons[0]+leptons[1]).Pt()]

	[_phiHj1,_phiHj2,_phiZj1,_phiZj2]=[bjet1.Phi(),bjet2.Phi(),jet1.Phi(),jet2.Phi()]
	[_etaHj1,_etaHj2,_etaZj1,_etaZj2]=[bjet1.Eta(),bjet2.Eta(),jet1.Eta(),jet2.Eta()]

	_dRuubb_H = abs((muons[0]+muons[1]).DeltaR(bjet1+bjet2))
	_dRuujj_Z = abs((muons[0]+muons[1]).DeltaR(jet1+jet2))
	_dPHIuubb_H = abs((muons[0]+muons[1]).DeltaPhi(bjet1+bjet2))
	_dPHIuujj_Z = abs((muons[0]+muons[1]).DeltaPhi(jet1+jet2))

	_dReebb_H = abs((electrons[0]+electrons[1]).DeltaR(bjet1+bjet2))
	_dReejj_Z = abs((electrons[0]+electrons[1]).DeltaR(jet1+jet2))
	_dPHIeebb_H = abs((electrons[0]+electrons[1]).DeltaPhi(bjet1+bjet2))
	_dPHIeejj_Z = abs((electrons[0]+electrons[1]).DeltaPhi(jet1+jet2))

	_dRllbb_H = abs((leptons[0]+leptons[1]).DeltaR(bjet1+bjet2))
	_dRlljj_Z = abs((leptons[0]+leptons[1]).DeltaR(jet1+jet2))
	_dPHIllbb_H = abs((leptons[0]+leptons[1]).DeltaPhi(bjet1+bjet2))
	_dPHIlljj_Z = abs((leptons[0]+leptons[1]).DeltaPhi(jet1+jet2))

	_minDRuj = abs(min(muons[0].DeltaR(jet1),muons[0].DeltaR(jet2),muons[1].DeltaR(jet1),muons[1].DeltaR(jet2)))
	_minDRej = abs(min(electrons[0].DeltaR(jet1),electrons[0].DeltaR(jet2),electrons[1].DeltaR(jet1),electrons[1].DeltaR(jet2)))
	_minDRlj = abs(min(leptons[0].DeltaR(jet1),leptons[0].DeltaR(jet2),leptons[1].DeltaR(jet1),leptons[1].DeltaR(jet2)))

	_cosThetaStarMu  = getCosThetaStar_CS(bjet1+bjet2,muons[0]+muons[1]+jet1+jet2)
	_cosThetaStarEle = getCosThetaStar_CS(bjet1+bjet2,electrons[0]+electrons[1]+jet1+jet2)
	_cosThetaStarLep = getCosThetaStar_CS(bjet1+bjet2,leptons[0]+leptons[1]+jet1+jet2)

	#### AH ####
	############# hh angular variables #####################
	_cosThetaStarMu_gen = getCosThetaStar_CS(_genJetsH[0]+_genJetsH[1], _genMuonsZ[0]+_genMuonsZ[1]+_genJetsZ[0]+_genJetsZ[1])
	_cosThetaStarEle_gen = getCosThetaStar_CS(_genJetsH[0]+_genJetsH[1],_genElectronsZ[0]+_genElectronsZ[1]+_genJetsZ[0]+_genJetsZ[1])
	
	cosThetaAngles_gen = CosThetaAngles(_genJetsH[0], _genJetsH[1], _genJetsZ[0], _genJetsZ[1], _genMuonsZ[0], _genMuonsZ[1])
	_cosThetaStar_gen = cosThetaAngles_gen[0]
	_cosTheta_hbb_gen = cosThetaAngles_gen[1]
	_cosTheta_zjj_hzz_gen  = cosThetaAngles_gen[2]
	_cosTheta_zuu_hzz_gen  = cosThetaAngles_gen[3]
	_cosTheta_zj1_hzz_gen  = cosThetaAngles_gen[4]
	_cosTheta_zu1_hzz_gen  = cosThetaAngles_gen[5]
	cosThetaAngles = CosThetaAngles(bjet1, bjet2, jet1, jet2, muons[0], muons[1])
	_cosThetaStar = cosThetaAngles[0]
	_cosTheta_hbb  = cosThetaAngles[1]
	_cosTheta_zjj_hzz  = cosThetaAngles[2]
	_cosTheta_zuu_hzz  = cosThetaAngles[3]
	_cosTheta_zj1_hzz  = cosThetaAngles[4]
	_cosTheta_zu1_hzz  = cosThetaAngles[5]
		
	phiAngles_gen = getPhi(_genJetsH[0], _genJetsH[1], _genJetsZ[0], _genJetsZ[1], _genMuonsZ[0], _genMuonsZ[1])
	_phi0_gen = phiAngles_gen[0]
	_phi1_gen = phiAngles_gen[1]
	phiAngles = getPhi(bjet1, bjet2, jet1, jet2, muons[0], muons[1])
	_phi0 = phiAngles[0]
	_phi1 = phiAngles[1]
	
	### Using the ZZ->lljj system instead of the HH system
	_cosThetaStarZuu_CS_gen = getCosThetaStar_CS(_genMuonsZ[0]+_genMuonsZ[1], _genJetsZ[0]+_genJetsZ[1])
	_cosThetaStarZjj_CS_gen = getCosThetaStar_CS(_genJetsZ[0]+_genJetsZ[1], _genMuonsZ[0]+_genMuonsZ[1])
	_cosThetaStarZuu_CS = getCosThetaStar_CS(muons[0]+muons[1], jet1+jet2)
	_cosThetaStarZjj_CS = getCosThetaStar_CS(jet1+jet2, muons[0]+muons[1])
	
	cosThetaAng_ZZ_gen = CosThetaAngles_ZZ(_genJetsZ[0], _genJetsZ[1], _genMuonsZ[0], _genMuonsZ[1])
	_cosTheta_Zuu_gen = cosThetaAng_ZZ_gen[0]
	_cosTheta_Zjj_gen = cosThetaAng_ZZ_gen[1]
	cosThetaAng_ZZ = CosThetaAngles_ZZ(jet1, jet2, muons[0], muons[1])
	_cosTheta_Zuu = cosThetaAng_ZZ[0]
	_cosTheta_Zjj = cosThetaAng_ZZ[1]
		
	phiAngles_ZZ_gen = getPhi_ZZ(_genJetsZ[0], _genJetsZ[1], _genMuonsZ[0], _genMuonsZ[1])
	_phi0_zz_gen  = phiAngles_ZZ_gen[0]
	_phi1_zuu_gen = phiAngles_ZZ_gen[1]
	_phi1_zjj_gen = phiAngles_ZZ_gen[2]
	phiAngles_ZZ = getPhi_ZZ(jet1, jet2, muons[0], muons[1])
	_phi0_zz  = phiAngles_ZZ[0]
	_phi1_zuu = phiAngles_ZZ[1]
	_phi1_zjj = phiAngles_ZZ[2]
	#### AH ####

	didMuon = False
	_Muu4j_gen,_Mee4j_gen,_Mll4j_gen,_Muu4j_genMatched,_Mee4j_genMatched,_Mll4j_genMatched = 0.,0.,0.,0.,0.,0.
	_Muujj_gen,_Muujj_genMatched,_Meejj_gen,_Meejj_genMatched,_Mlljj_gen,_Mlljj_genMatched, = 0.,0.,0.,0.,0.,0.

	_Muujj_gen = (_genJetsZ[0]+_genJetsZ[1]+_genMuonsZ[0]+_genMuonsZ[1]).M()
	_Muujj_genMatched = (_matchedRecoJetsZ[0]+_matchedRecoJetsZ[1]+_matchedRecoMuonsZ[0]+_matchedRecoMuonsZ[1]).M()
	_Meejj_gen = (_genJetsZ[0]+_genJetsZ[1]+_genElectronsZ[0]+_genElectronsZ[1]).M()
	_Meejj_genMatched = (_matchedRecoJetsZ[0]+_matchedRecoJetsZ[1]+_matchedRecoElectronsZ[0]+_matchedRecoElectronsZ[1]).M()
	_Mll4j_gen = (_genJetsZ[0]+_genJetsZ[1]+_genJetsH[0]+_genJetsH[1]+_genLeptonsZ[0]+_genLeptonsZ[1]).M()
	_Mll4j_genMatched = (_matchedRecoJetsZ[0]+_matchedRecoJetsZ[1]+_matchedRecoJetsH[0]+_matchedRecoJetsH[1]+_matchedRecoLeptonsZ[0]+_matchedRecoLeptonsZ[1]).M()
	
	#if v == '' : print 'Gen level ZJets:',len(_genJetsZ),'HJets:',len(_genJetsH),'ZMuons:',len(_genMuonsZ),'ZElectrons:',len(_genElectronsZ)
	if len(_genJetsZ)>=2 and len(_genJetsH)>=2 and len(_genMuonsZ)>=2 and _isMuonEvent:
		_Mll4j_gen = (_genJetsZ[0]+_genJetsZ[1]+_genJetsH[0]+_genJetsH[1]+_genMuonsZ[0]+_genMuonsZ[1]).M()
		didMuon = True

	if len(_genJetsZ)>=2 and len(_genJetsH)>=2 and len(_genElectronsZ)>=2 and not didMuon and _isElectronEvent:
		_Mee4j_gen = (_genJetsZ[0]+_genJetsZ[1]+_genJetsH[0]+_genJetsH[1]+_genElectronsZ[0]+_genElectronsZ[1]).M()
		_Mll4j_gen = (_genJetsZ[0]+_genJetsZ[1]+_genJetsH[0]+_genJetsH[1]+_genElectronsZ[0]+_genElectronsZ[1]).M()

	if len(_matchedRecoJetsZ)>=2 and len(_matchedRecoJetsH)>=2 and len(_matchedRecoMuonsZ)>=2 and didMuon:
		_Mll4j_genMatched = (_matchedRecoJetsZ[0]+_matchedRecoJetsZ[1]+_matchedRecoJetsH[0]+_matchedRecoJetsH[1]+_matchedRecoMuonsZ[0]+_matchedRecoMuonsZ[1]).M()
	
	if len(_matchedRecoJetsZ)>=2 and len(_matchedRecoJetsH)>=2 and len(_matchedRecoElectronsZ)>=2 and not didMuon:
		_Mee4j_genMatched = (_matchedRecoJetsZ[0]+_matchedRecoJetsZ[1]+_matchedRecoJetsH[0]+_matchedRecoJetsH[1]+_matchedRecoElectronsZ[0]+_matchedRecoElectronsZ[1]).M()
		_Mll4j_genMatched = (_matchedRecoJetsZ[0]+_matchedRecoJetsZ[1]+_matchedRecoJetsH[0]+_matchedRecoJetsH[1]+_matchedRecoElectronsZ[0]+_matchedRecoElectronsZ[1]).M()


	_Mjj_Z_gen, _Mbb_H_gen, _Mjj_Z_genMatched, _Mbb_H_genMatched = 0.,0.,0.,0.
	if len(_genJetsZ)>=2 and len(_genJetsH)>=2 :
		_Mjj_Z_gen = (_genJetsZ[0]+_genJetsZ[1]).M()
		_Mbb_H_gen = (_genJetsH[0]+_genJetsH[1]).M()
		#if v == '' : print '_Mjj_Z_gen',_Mjj_Z_gen,'_Mbb_H_gen',_Mbb_H_gen
	if len(_matchedRecoJetsZ)>=2 and len(_matchedRecoJetsH)>=2 :
		_Mjj_Z_genMatched = (_matchedRecoJetsZ[0]+_matchedRecoJetsZ[1]).M()
		_Mbb_H_genMatched = (_matchedRecoJetsH[0]+_matchedRecoJetsH[1]).M()
	

	_genjetcount = 0
	if T.isData==0:
		_genjetcount = len(T.GenJetPtAK4)
	
	_NGenMuonsZ = 0
	_NGenElecsZ = 0
	_NGenMuonsZ = len(_genMuonsZ)
	_NGenElecsZ = len(_genElectronsZ)
	
	#----- calculate BDT disc here
	_bdt_discrims_s1 = [-99.0,-99.0,-99.0,-99.0,-99.0,-99.0,-99.0,-99.0,-99.0,-99.0,-99.0,-99.0,-99.0,-99.0]
	for kth in range(len(_bdt_discrims_s1)):
		_bdt_discrims_s1[kth] = calculateBDTdiscriminant(reader_12vars_set1, str("BDT_classifier_12vars_set1_M" + SignalM[kth]), _bdtvarnames, _cosThetaStarMu, _Mbb_H, _phi0, _ptmu1, _ptmu2, bscoreMVA1, _dRbb_H, _dRjj_Z, _DRuu, _Muu4j, _Muu, _Mjj_Z, _isMuonEvent, _Pt_Hjet1, _Pt_Hjet2, _Pt_Zjet1, _Pt_Zjet2, bscoreMVA2, _bMVAj1, _bMVAj2, _qmu1, _qmu2, _cosTheta_hbb, _cosTheta_zuu_hzz, _dRuubb_H)
	[_bdt_discrim_M260, _bdt_discrim_M270, _bdt_discrim_M300, _bdt_discrim_M350, _bdt_discrim_M400, _bdt_discrim_M450, _bdt_discrim_M500, _bdt_discrim_M550, _bdt_discrim_M600, _bdt_discrim_M650, _bdt_discrim_M750, _bdt_discrim_M800, _bdt_discrim_M900, _bdt_discrim_M1000] = _bdt_discrims_s1
	#if v == '' : print ' _bdt_discrims_s1 ', _bdt_discrims_s1
	#if v == '' : print ' each bdt         ', _bdt_discrim_M260, _bdt_discrim_M270, _bdt_discrim_M300, _bdt_discrim_M350, _bdt_discrim_M400
						   
	[_bdt_discrims2_M300,_bdt_discrims2_M550] = [-99.0,-99.0]
	_bdt_discrims2_M300 = calculateBDTdiscriminant(reader_13vars_set2, "BDT_classifier_13vars_set2_M300", _bdtvarnames_s2, _cosThetaStarMu, _Mbb_H, _phi0, _ptmu1, _ptmu2, bscoreMVA1, _dRbb_H, _dRjj_Z, _DRuu, _Muu4j, _Muu, _Mjj_Z, _isMuonEvent, _Pt_Hjet1, _Pt_Hjet2, _Pt_Zjet1, _Pt_Zjet2, bscoreMVA2, _bMVAj1, _bMVAj2, _qmu1, _qmu2, _cosTheta_hbb, _cosTheta_zuu_hzz, _dRuubb_H)
	_bdt_discrims2_M550 = calculateBDTdiscriminant(reader_13vars_set2, "BDT_classifier_13vars_set2_M550", _bdtvarnames_s2, _cosThetaStarMu, _Mbb_H, _phi0, _ptmu1, _ptmu2, bscoreMVA1, _dRbb_H, _dRjj_Z, _DRuu, _Muu4j, _Muu, _Mjj_Z, _isMuonEvent, _Pt_Hjet1, _Pt_Hjet2, _Pt_Zjet1, _Pt_Zjet2, bscoreMVA2, _bMVAj1, _bMVAj2, _qmu1, _qmu2, _cosTheta_hbb, _cosTheta_zuu_hzz, _dRuubb_H)
	
	[_bdt_discrims3_low,_bdt_discrims3_hig] = [-99.0,-99.0]
	_bdt_discrims3_low = calculateBDTdiscriminant(reader_15vars_set3, "BDT_classifier_15vars_set3_Mlow", _bdtvarnames_s3, _cosThetaStarMu, _Mbb_H, _phi0, _ptmu1, _ptmu2, bscoreMVA1, _dRbb_H, _dRjj_Z, _DRuu, _Muu4j, _Muu, _Mjj_Z, _isMuonEvent, _Pt_Hjet1, _Pt_Hjet2, _Pt_Zjet1, _Pt_Zjet2, bscoreMVA2, _bMVAj1, _bMVAj2, _qmu1, _qmu2, _cosTheta_hbb, _cosTheta_zuu_hzz, _dRuubb_H)
	_bdt_discrims3_hig = calculateBDTdiscriminant(reader_15vars_set3, "BDT_classifier_15vars_set3_Mhig", _bdtvarnames_s3, _cosThetaStarMu, _Mbb_H, _phi0, _ptmu1, _ptmu2, bscoreMVA1, _dRbb_H, _dRjj_Z, _DRuu, _Muu4j, _Muu, _Mjj_Z, _isMuonEvent, _Pt_Hjet1, _Pt_Hjet2, _Pt_Zjet1, _Pt_Zjet2, bscoreMVA2, _bMVAj1, _bMVAj2, _qmu1, _qmu2, _cosTheta_hbb, _cosTheta_zuu_hzz, _dRuubb_H)
	#----- End calculate BDT disc here

	# This MUST have the same structure as _kinematic variables!
	toreturn = [_ptmu1,_ptmu2,_ptele1,_ptele2,_ptlep1,_ptlep2,_ptj1,_ptj2,_ptmet]
	toreturn += [_ptj3,_ptj4]
	toreturn += [_etamu1,_etamu2,_etaele1,_etaele2,_etalep1,_etalep2,_etaj1,_etaj2,_etamet]
	toreturn += [_phimu1,_phimu2,_phiele1,_phiele2,_philep1,_philep2,_phij1,_phij2,_phimet]
	toreturn += [_phiHj1,_phiHj2,_phiZj1,_phiZj2]
	toreturn += [_etaHj1,_etaHj2,_etaZj1,_etaZj2]
	toreturn += [_ptu1_gen,_ptu2_gen]
	toreturn += [_ptHj1_gen,_ptHj2_gen,_ptZj1_gen,_ptZj2_gen]
	toreturn += [_ptu1_genMatched,_ptu2_genMatched]
	toreturn += [_ptHj1_genMatched,_ptHj2_genMatched,_ptZj1_genMatched,_ptZj2_genMatched]
	toreturn += [_phiHj1_gen,_phiHj2_gen,_phiZj1_gen,_phiZj2_gen]
	toreturn += [_etaHj1_gen,_etaHj2_gen,_etaZj1_gen,_etaZj2_gen]
	toreturn += [_xmiss,_ymiss]
	toreturn += [_isomu1,_isomu2,_isoele1,_isoele2,_isolep1,_isolep2]
	toreturn += [_chimu1,_chimu2]
	toreturn += [_ispfmu1,ispfmu2]
	toreturn += [_layersmu1,_layersmu2]
	toreturn += [_qmu1,_qmu2,_qele1,_qele2,_qlep1,_qlep2]
	toreturn += [_dptmu1,_dptmu2]
	toreturn += [_nhefj1,_nhefj2,_nemefj1,_nemefj2]
	toreturn += [_stuujj,_steejj,_stlljj]
	toreturn += [_stuu4j,_stee4j,_stll4j]
	toreturn += [_Muu,_Mee,_Mll]
	toreturn += [_Mjj]
	toreturn += [_DRuu,_DPHIuv,_DPHIj1v,_DPHIj2v]
	toreturn += [_DRee,_DPHIev]
	toreturn += [_DRu1j1,_DRu1j2,_DRu2j1,_DRu2j2]
	toreturn += [_DRe1j1,_DRe1j2,_DRe2j1,_DRe2j2]
	toreturn += [_DRl1j1,_DRl1j2,_DRl2j1,_DRl2j2]
	toreturn += [_DRj1j2,_DPhij1j2]
	toreturn += [_DPhiu1j1,_DPhiu1j2,_DPhiu2j1,_DPhiu2j2]
	toreturn += [_DPhie1j1,_DPhie1j2,_DPhie2j1,_DPhie2j2]
	toreturn += [_DPhil1j1,_DPhil1j2,_DPhil2j1,_DPhil2j2]
	toreturn += [_Muujj, _Meejj, _Mlljj]
	toreturn += [_Muu4j, _Mee4j, _Mll4j]
	toreturn += [_Mbb_H,_Mjj_Z,_Mjj_Z_3jet]
	toreturn += [_Mbb_H_gen,_Mjj_Z_gen]
	toreturn += [_Mbb_H_genMatched,_Mjj_Z_genMatched]
	toreturn += [_Mbb_H_orig,_Muu4j_orig]
	toreturn += [_cosThetaStarMu,_cosThetaStarEle,_cosThetaStarLep]
	toreturn += [_cosThetaStarMu_gen,_cosThetaStarEle_gen]
	toreturn += [_cosThetaStar_gen,_cosTheta_hbb_gen,_cosTheta_zjj_hzz_gen,_cosTheta_zuu_hzz_gen,_cosTheta_zj1_hzz_gen,_cosTheta_zu1_hzz_gen]
	toreturn += [_phi0_gen, _phi1_gen]
	toreturn += [_cosThetaStarZuu_CS_gen, _cosTheta_Zuu_gen]
	toreturn += [_phi0_zz_gen, _phi1_zuu_gen, _phi1_zjj_gen]
	toreturn += [_cosThetaStar,_cosTheta_hbb,_cosTheta_zjj_hzz,_cosTheta_zuu_hzz,_cosTheta_zj1_hzz,_cosTheta_zu1_hzz]
	toreturn += [_phi0, _phi1]
	toreturn += [_cosThetaStarZuu_CS, _cosTheta_Zuu]
	toreturn += [_phi0_zz, _phi1_zuu, _phi1_zjj]
	toreturn += [_Pt_origHjet1,_Pt_origHjet2]
	toreturn += [_Pt_Hjet1,_Pt_Hjet2,_Pt_Zjet1,_Pt_Zjet2]
	toreturn += [_Pt_Hjets,_Pt_Zjets,_Pt_uu,_Pt_ee,_Pt_ll]
	toreturn += [_dRjj_Z,_dRbb_H]
	toreturn += [_dRu1Hj1,_dRu1Hj2,_dRu2Hj1,_dRu2Hj2]
	toreturn += [_dRu1Zj1,_dRu1Zj2,_dRu2Zj1,_dRu2Zj2]
	toreturn += [_dRu1Hj1_gen,_dRu1Hj2_gen,_dRu2Hj1_gen,_dRu2Hj2_gen]
	toreturn += [_dRu1Zj1_gen,_dRu1Zj2_gen,_dRu2Zj1_gen,_dRu2Zj2_gen]
	toreturn += [_dRu1Hj1_genMatched,_dRu1Hj2_genMatched,_dRu2Hj1_genMatched,_dRu2Hj2_genMatched]
	toreturn += [_dRu1Zj1_genMatched,_dRu1Zj2_genMatched,_dRu2Zj1_genMatched,_dRu2Zj2_genMatched]
	toreturn += [_dRuubb_H,_dRuujj_Z,_dPHIuubb_H,_dPHIuujj_Z]
	toreturn += [_dReebb_H,_dReejj_Z,_dPHIeebb_H,_dPHIeejj_Z]
	toreturn += [_dRllbb_H,_dRlljj_Z,_dPHIllbb_H,_dPHIlljj_Z]
	toreturn += [_dPhijj_Z,_dPhibb_H]
	toreturn += [_minDRuj,_minDRej]
	toreturn += [_Muu4j_gen,_Muu4j_genMatched]
	toreturn += [_Mee4j_gen,_Mee4j_genMatched]
	toreturn += [_Mll4j_gen,_Mll4j_genMatched]
	toreturn += [_jetCntPreFilter,_jetcount,_mucount,_elcount,_genjetcount]
	toreturn += [_ismuon_muon1,_ismuon_muon2]
	toreturn += [_muonInd1,_muonInd2]
	toreturn += [_jetInd1,_jetInd2]
	toreturn += [_ptHat]
	toreturn += [_CSVj1,_CSVj2]
	toreturn += [bscore1,bscore2]
	toreturn += [_bMVAj1,_bMVAj2]
	toreturn += [bscoreMVA1,bscoreMVA2]
	toreturn += [_isMuonEvent,_isElectronEvent]
	toreturn += [_Hj1Matched,_Hj2Matched,_Zj1Matched,_Zj2Matched]
	toreturn += [_Hj1Present,_Hj2Present,_Zj1Present,_Zj2Present]
	toreturn += [_NGenMuonsZ, _NGenElecsZ]
	toreturn += [_Muujj_gen, _Muujj_genMatched]
	toreturn += [_Meejj_gen, _Meejj_genMatched]
	toreturn += [_Mlljj_gen, _Mlljj_genMatched]
	toreturn += [_Muu_gen, _Muu_genMatched]
	toreturn += [_bscoreMVA1_genMatched, _bscoreMVA2_genMatched]
	toreturn += [_CorHj1j2Avail,_CorZj1j2Avail]
	toreturn += [_passWptCut,_passZptCut,_WorZSystemPt]
	toreturn += [_bdt_discrim_M260,_bdt_discrim_M270,_bdt_discrim_M300,_bdt_discrim_M350,_bdt_discrim_M400]
	toreturn += [_bdt_discrim_M450,_bdt_discrim_M500,_bdt_discrim_M550,_bdt_discrim_M600,_bdt_discrim_M650]
	toreturn += [_bdt_discrim_M750,_bdt_discrim_M800,_bdt_discrim_M900,_bdt_discrim_M1000]
	toreturn += [_bdt_discrims2_M300,_bdt_discrims2_M550]
	toreturn += [_bdt_discrims3_low,_bdt_discrims3_hig]
	return toreturn

def checkWorZpt(T,lowcut, highcut, WorZ):
	#print 'New event'
	maxPt=0.
	for n in range(len(T.GenParticlePdgId)):
		pdg = T.GenParticlePdgId[n]
		status = T.GenParticleStatus[n]
		pt = T.GenParticlePt[n]
		parts = []
		if WorZ=='W' : parts = [-24,24]
		if WorZ=='Z' : parts = [-22,-23,22,23]
		if pdg in parts:#[-24,24]:#23=Z, 24=W, 22=gamma
			#print n,pdg,pt,status
			if pt>maxPt: maxPt=pt
		#	#print n,pdg,pt,status
		#	if pt<100: return 1
		#	else: return 0
		else: continue
	if maxPt<highcut:
		#print 'less than 100!'
		return 1
	else: 
		#print 'more than 100!'
		return 0
	return 1

def GeomFilterCollection(collection_to_clean,good_collection,dRcut,associatedCollection1,associatedCollection2,associatedCollection3):
	# Purpose: Take a collection of TLorentzVectors that you want to clean (arg 1)
	#         by removing all objects within dR of dRcut (arg 3) of any element in
	#         the collection of other particles (arg 2)
	#         e.g.  argumments (jets,muons,0.3) gets rid of jets within 0.3 of muons. 
	#   Added option for associated collection, i.e.
	output_collection = []
	associated_output_collection1,associated_output_collection2,associated_output_collection3 = [],[],[]
	for i, c in enumerate(collection_to_clean):
		isgood = True
		for g in good_collection:
			if (c.DeltaR(g))<dRcut:
				isgood = False
		if isgood==True:
			output_collection.append(c)
			associated_output_collection1.append(associatedCollection1[i])
			associated_output_collection2.append(associatedCollection2[i])
			associated_output_collection3.append(associatedCollection3[i])
	return [output_collection,associated_output_collection1,associated_output_collection2,associated_output_collection3]


def MetVector(T):
	# Purpose: Creates a TLorentzVector represting the MET. No pseudorapidity, obviously.
	met = TLorentzVector()
	met.SetPtEtaPhiM(T.PFMETType1XYCor[0],0,T.PFMETPhiType1XYCor[0],0)
	return met

##########################################################################################
#################    BELOW IS THE ACTUAL LOOP OVER ENTRIES         #######################
##########################################################################################
startTime = datetime.now()

# Please don't edit here. It is static. The kinematic calulations are the only thing to edit!
lumisection = array.array("L",[0])
t.SetBranchAddress("ls",lumisection)
for n in range(N):

	# This is the loop over events. Due to the heavy use of functions and automation of 
	# systematic variations, this loop is very small. It should not really be editted, 
	# except possibly to add a new flag or weight variable. 
	# All editable contents concerning kinematics are in the function defs.

	# Get the entry
	t.GetEntry(n)
	# if n > 1000:  # Testing....
	# 	break
	if n%100==0:
		print 'Processing event',n, 'of', N # where we are in the loop...

	## ===========================  BASIC SETUP  ============================= ##
	# print '-----'
	# Assign Weights

	Branches['weight_central'][0] = startingweight*GetPUWeight(t,'Central','Basic')
	Branches['weight_pu_down'][0] = startingweight*GetPUWeight(t,'SysDown','Basic')
	Branches['weight_pu_up'][0] = startingweight*GetPUWeight(t,'SysUp','Basic')
	#Branches['weight_central_2012D'][0] = startingweight*GetPUWeight(t,'Central','2012D')
	Branches['weight_nopu'][0] = startingweight
	Branches['weight_topPt'][0]=t.GenParticleTopPtWeight
	if 'amcatnlo' in amcNLOname :
		Branches['weight_central'][0]*=t.amcNLOWeight
		Branches['weight_pu_down'][0]*=t.amcNLOWeight
		Branches['weight_pu_up'][0]*=t.amcNLOWeight
		#Branches['weight_central_2012D'][0]*=t.amcNLOWeight
		Branches['weight_nopu'][0]*=t.amcNLOWeight
	Branches['weight_amcNLO'][0]=0#t.amcNLOWeight

	if 'amcatnlo' in amcNLOname :
		scaleWeights = t.ScaleWeightsAMCNLO
	else:
		scaleWeights = t.ScaleWeights
	if len(t.ScaleWeights) > 7 :
		Branches['scaleWeight_Up'][0]=       t.ScaleWeights[4]
		Branches['scaleWeight_Down'][0]=     t.ScaleWeights[8]
		Branches['scaleWeight_R1_F1'][0]=    t.ScaleWeights[0]
		Branches['scaleWeight_R1_F2'][0]=    t.ScaleWeights[1]
		Branches['scaleWeight_R1_F0p5'][0]=  t.ScaleWeights[2]
		Branches['scaleWeight_R2_F1'][0]=    t.ScaleWeights[3]
		Branches['scaleWeight_R2_F2'][0]=    t.ScaleWeights[4]
		Branches['scaleWeight_R2_F0p5'][0]=  t.ScaleWeights[5]
		Branches['scaleWeight_R0p5_F1'][0]=  t.ScaleWeights[6]
		Branches['scaleWeight_R0p5_F2'][0]=  t.ScaleWeights[7]
		Branches['scaleWeight_R0p5_F0p5'][0]=t.ScaleWeights[8]
	else :
		Branches['scaleWeight_Up'][0]=       1.0
		Branches['scaleWeight_Down'][0]=     1.0
		Branches['scaleWeight_R1_F1'][0]=    1.0
		Branches['scaleWeight_R1_F2'][0]=    1.0
		Branches['scaleWeight_R1_F0p5'][0]=  1.0
		Branches['scaleWeight_R2_F1'][0]=    1.0
		Branches['scaleWeight_R2_F2'][0]=    1.0
		Branches['scaleWeight_R2_F0p5'][0]=  1.0
		Branches['scaleWeight_R0p5_F1'][0]=  1.0
		Branches['scaleWeight_R0p5_F2'][0]=  1.0
		Branches['scaleWeight_R0p5_F0p5'][0]=1.0
	if t.isData:
		dopdf = False
	if dopdf:
		pdfweights = GetPDFWeights(t)
		#if len(pdfweights)==len(_pdfweightsnames) :#fixme put in check that there are the same number of weights as weight names - update when all pdf weights work again
		for p in range(len(pdfweights)):
			Branches[_pdfweightsnames[p]][0] = pdfweights[p]
	
	# Event Flags
	Branches['run_number'][0]   = t.run
	# event_number[0] = int(t.event)
	Branches['event_number'][0] = t.event#fixme todo this is failing for some event in CMSSW_7_1_14
	Branches['lumi_number'][0]  = lumisection[0]
	Branches['GoodVertexCount'][0] = CountVertices(t)

	if t.isData == True:
		Branches['pass_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'][0] = PassTrigger(t,["HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v"],1)         # Data Only
		Branches['pass_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'][0] = PassTrigger(t,["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v"],1)         # Data Only
		Branches['pass_HLT_Mu17_Mu8'][0] = 1 if (PassTrigger(t,["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v"],1) + PassTrigger(t,["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v"],1))>0 else 0        # Data Only
		Branches['passTriggerObjectMatching'][0]  = 1*(True in t.MuonHLTSingleMuonMatched)  # Data Only
		Branches['passBadEESuperCrystal'][0]      = 1*(t.passEEBadScFilter) # Used, Data only
	else:
		Branches['pass_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'][0] = 1#PassTrigger(t,["HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v"],1)         # Data Only
		Branches['pass_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'][0] = 1#PassTrigger(t,["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v"],1)         # Data Only
		Branches['pass_HLT_Mu17_Mu8'][0] = 1#PassTrigger(t,["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v"],1) + PassTrigger(t,["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v"],1)          # Data Only
		Branches['passTriggerObjectMatching'][0]  = 1
		Branches['passBadEESuperCrystal'][0]      = 1
	
	Branches['passPrimaryVertex'][0]          = 1*(t.passGoodVertices)     # checked, data+MC
	Branches['passHBHENoiseFilter'][0]        = 1*(t.passHBHENoiseFilter) # checked, data+MC
	Branches['passHBHENoiseIsoFilter'][0]     = 1*(t.passHBHENoiseIsoFilter) # checked, data+MC
	Branches['passBeamHalo'][0]               = 1*(t.passCSCTightHaloFilter) # checked, data+MC
	Branches['passBeamHalo2016'][0]           = 1*(t.passGlobalTightHalo2016Filter)# checked, data+MC
	Branches['passEcalDeadCellTP'][0]         = 1*(t.passEcalDeadCellTriggerPrimitiveFilter) # Checked, data + MC
	Branches['passBadMuon'][0]                = 1*(t.passBadPFMuonFilter)     # checked, data+MC
	Branches['passBadChargedHadron'][0]       = 1*(t.passBadChargedCandidateFilter)     # checked, data+MC
	Branches['badMuonsFlag'][0]               = 1*(t.badMuonsFlag)
	Branches['duplicateMuonsFlag'][0]         = 1*(t.duplicateMuonsFlag)
	Branches['noBadMuonsFlag'][0]             = 1*(t.noBadMuonsFlag)

	Branches['passDataCert'][0] = 1
	if ( (t.isData==True) and (CheckRunLumiCert(t.run,lumisection[0]) == False) ) : 	
		Branches['passDataCert'][0] = 0


	## ===========================  Calculate everything!  ============================= ##

	# Looping over systematic variations
	for v in _variations:
		# All calucations are done here
		calculations = FullKinematicCalculation(t,v)
		# Now cleverly cast the variables
		for b in range(len(_kinematicvariables)):
			Branches[_kinematicvariables[b]+v][0] = calculations[b]

	## ===========================     Skim out events     ============================= ##

	# Feel like skimming? Do it here. The syntax is just Branches[branchname] > blah, or whatever condition
	# you want to impose. This Branches[blah] mapping was needed because branches must be linked to arrays of length [0]
	# BE MINDFUL: Just because the central (non-systematic) quantity meets the skim, does not mean 
	# that the systematic varied quantity will, and that will throw off systematics calculations later.
	# Make sure your skim is looser than any selection you will need afterward!

	#if (Branches['Pt_lep1'][0] < 16) : continue
	#if (Branches['Pt_lep2'][0] < 8) : continue
	#if (Branches['Pt_muon1'][0] < 16) and (Branches['Pt_ele1'][0] < 16) : continue
	#if (Branches['Pt_muon1'][0] < 16) and (Branches['Pt_ele1'][0] > 16) and (Branches['Pt_ele2'][0]  < 8): continue
	#if (Branches['Pt_muon1'][0] > 16) and (Branches['Pt_muon2'][0] < 8) and (Branches['Pt_ele1'][0] < 16 or Branches['Pt_ele2'][0]  < 8): continue
	if ((Branches['isMuonEvent'][0]==True) and ((Branches['Pt_muon1'][0] < 16) or (Branches['Pt_muon2'][0] < 8) or (Branches['M_uu'][0] < 12))): continue
	if ((Branches['isElectronEvent'][0]==True) and ((Branches['Pt_ele1'][0] < 16) or (Branches['Pt_ele2'][0] < 11) or (Branches['M_ee'][0] < 12))): continue

	#print 'NGenMuonsZ', Branches['NGenMuonsZ'][0], 'NGenElecsZ', Branches['NGenElecsZ'][0]
	#if (Branches['Pt_muon1'][0] < 16) : continue
	#if (Branches['Pt_muon2'][0] < 8) : continue
	#if (Branches['NGenMuonsZ'][0] < 2) : continue

	#if nonisoswitch != True:
	#		if (Branches['Pt_muon2'][0] < 45) and (Branches['Pt_miss'][0] < 45): continue
	if (Branches['Pt_Hjet1'][0] <  18): continue
	if (Branches['Pt_Hjet2'][0] <  18): continue
	if (Branches['Pt_Zjet1'][0] <  18): continue
	if (Branches['Pt_Zjet2'][0] <  18): continue
	#
	#if (Branches['St_uujj'][0] < 260) and (Branches['St_uvjj'][0] < 260): continue
	#if (Branches['M_uu'][0]    <  45) and (Branches['MT_uv'][0]   <  45): continue

	# Fill output tree with event
	tout.Fill()

# All done. Write and close file.
tout.Write()
fout.Close()

# Timing, for debugging and optimization
print(datetime.now()-startTime)

import os
print ('mv '+tmpfout+' '+finalfout)
os.system('mv '+tmpfout+' '+finalfout)
#os.system('rm '+junkfile1)
os.system('rm '+junkfile2)
