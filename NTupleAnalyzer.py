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
from random import normalvariate
##########################################################################################
#################      SETUP OPTIONS - File, Normalization, etc    #######################
##########################################################################################

# Input Options - file, cross-section, number of events
#parser = OptionParser()
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help="input root file", metavar="FILE")
parser.add_argument("-b", "--batch", dest="dobatch", help="run in batch mode", metavar="BATCH")
parser.add_argument("-s", "--sigma", dest="crosssection", help="specify the process cross-section", metavar="SIGMA")
parser.add_argument("-n", "--ntotal", dest="ntotal", help="total number of MC events for the sample", metavar="NTOTAL")
parser.add_argument("-l", "--lumi", dest="lumi", help="integrated luminosity for data taking", metavar="LUMI")
parser.add_argument("-j", "--json", dest="json", help="json file for certified run:lumis", metavar="JSON")
parser.add_argument("-d", "--dir", dest="dir", help="output directory", metavar="DIR")
parser.add_argument("-p", "--pdf", dest="pdf", help="option to produce pdf uncertainties", metavar="PDF")

#global options
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
startingweight = _TopPtFactor*(float(options.crosssection)*float(options.lumi)/float(options.ntotal))
#print '_TopPtFactor:',_TopPtFactor

to = fin.Get("rootTupleTree/tree")
No = to.GetEntries()



# Here we are going to pre-skim the file to reduce running time.
indicator = ((name.split('/'))[-1]).replace('.root','')
#print indicator
junkfile1 = str(randint(100000000,1000000000))+indicator+'junk.root'

# At least one 44 GeV Muon - offline cut is 53
fj1 = TFile.Open(junkfile1,'RECREATE')
t1 = to.CopyTree('MuonPt[]>47')
Nm1 = t1.GetEntries()

junkfile2 = str(randint(100000000,1000000000))+indicator+'junk.root'

# At least one 44 GeV jet - offline cut is 50
fj2 = TFile.Open(junkfile2,'RECREATE')
t = t1.CopyTree('PFJetPtAK4CHS[]>45')
N = t.GetEntries()

# Print the reduction status
print 'Original events:          ',No
print 'After demand 1 pT46 muon: ',Nm1
print 'After demand 1 pT45 jet:  ',N

##########################################################################################
#################      PREPARE THE VARIABLES FOR THE OUTPUT TREE   #######################
##########################################################################################

# Branches will be created as follows: One branch for each kinematic variable for each 
# systematic variation determined in _variations. One branch for each weight and flag.
# So branch names will include weight_central, run_number, Pt_muon1, Pt_muon1MESUP, etc.

_kinematicvariables =  ['Pt_muon1','Pt_muon2','Pt_ele1','Pt_ele2','Pt_jet1','Pt_jet2','Pt_miss']
_kinematicvariables += ['Pt_muon1_noTuneP','Pt_muon2_noTuneP']
_kinematicvariables += ['Pt_mu1mu2']
_kinematicvariables += ['Eta_muon1','Eta_muon2','Eta_ele1','Eta_ele2','Eta_jet1','Eta_jet2','Eta_miss']
_kinematicvariables += ['Phi_muon1','Phi_muon2','Phi_ele1','Phi_ele2','Phi_jet1','Phi_jet2','Phi_miss']
_kinematicvariables += ['X_miss','Y_miss']
_kinematicvariables += ['TrkIso_muon1','TrkIso_muon2']
_kinematicvariables += ['Chi2_muon1','Chi2_muon2']
_kinematicvariables += ['PFID_muon1','PFID_muon2']
_kinematicvariables += ['TrkMeasLayers_muon1','TrkMeasLayers_muon2']
_kinematicvariables += ['Charge_muon1','Charge_muon2']
_kinematicvariables += ['TrkGlbDpt_muon1','TrkGlbDpt_muon2']
_kinematicvariables += ['NHEF_jet1','NHEF_jet2','NEMEF_jet1','NEMEF_jet2']
_kinematicvariables += ['St_uujj','St_uvjj']
_kinematicvariables += ['M_uu','MT_uv']
_kinematicvariables += ['M_jj']
_kinematicvariables += ['DR_muon1muon2','DPhi_muon1met','DPhi_jet1met','DPhi_jet2met']
_kinematicvariables += ['DR_muon1jet1','DR_muon1jet2','DR_muon2jet1','DR_muon2jet2']
_kinematicvariables += ['DR_jet1jet2','DPhi_jet1jet2']
_kinematicvariables += ['DPhi_muon1jet1','DPhi_muon1jet2','DPhi_muon2jet1','DPhi_muon2jet2']
_kinematicvariables += ['M_uujj1_gen','M_uujj2_gen','M_uujjavg_gen']
_kinematicvariables += ['M_uujj1_genMatched','M_uujj2_genMatched','M_uujjavg_genMatched']
_kinematicvariables += ['M_uujj1','M_uujj2','M_uujjavg']
_kinematicvariables += ['M_uujj1_rel','M_uujj2_rel','M_uujjavg_rel']
_kinematicvariables += ['M_uujj']
_kinematicvariables += ['M_uuj1','M_uuj2','M_u1j1j2','M_u2j1j2']
_kinematicvariables += ['MT_uvjj1','MT_uvjj2','M_uvjj','MT_uvjj']
_kinematicvariables += ['MH_uujj','MH_uvjj']
_kinematicvariables += ['JetCount','MuonCount','ElectronCount','GenJetCount']
_kinematicvariables += ['IsMuon_muon1','IsMuon_muon2']
_kinematicvariables += ['passTrigMu1','passTrigMu2']
_kinematicvariables += ['muonIndex1','muonIndex2']
_kinematicvariables += ['jetIndex1','jetIndex2']
_kinematicvariables += ['ptHat']
_kinematicvariables += ['CISV_jet1','CISV_jet2']
_kinematicvariables += ['CMVA_jet1','CMVA_jet2']
_kinematicvariables += ['PULoosej1','PUMediumj1','PUTightj1']
_kinematicvariables += ['PULoosej2','PUMediumj2','PUTightj2']
_kinematicvariables += ['passWptCut','passZptCut','WorZSystemPt']
_kinematicvariables += ['WSystemPt','ZSystemPt']
_kinematicvariables += ['matchedLQ','matchedLQ_LVJJ']

#_weights = ['scaleWeight_Up','scaleWeight_Down','scaleWeight_R1_F1','scaleWeight_R1_F2','scaleWeight_R1_F0p5','scaleWeight_R2_F1','scaleWeight_R2_F2','scaleWeight_R2_F0p5','scaleWeight_R0p5_F1','scaleWeight_R0p5_F2','scaleWeight_R0p5_F0p5','scaleWeight_R2_F2','weight_amcNLO','weight_nopu','weight_central', 'weight_pu_up', 'weight_pu_down','weight_central_2012D','weight_topPt']
_weights = ['scaleWeight_Up','scaleWeight_Down','scaleWeight_R1_F1','scaleWeight_R1_F2','scaleWeight_R1_F0p5','scaleWeight_R2_F1','scaleWeight_R2_F2','scaleWeight_R2_F0p5','scaleWeight_R0p5_F1','scaleWeight_R0p5_F2','scaleWeight_R0p5_F0p5','scaleWeight_R2_F2','weight_amcNLO','weight_nopu','weight_central', 'weight_pu_up', 'weight_pu_down','weight_topPt']
_flagDoubles = ['run_number','event_number','lumi_number']
_flags = ['pass_HLTIsoMu27','pass_HLTMu45_eta2p1','pass_HLTMu50','pass_HLTTkMu50','GoodVertexCount']
_flags += ['passPrimaryVertex','passHBHENoiseFilter','passHBHENoiseIsoFilter','passBeamHalo','passTriggerObjectMatching','passDataCert']
_flags += ['passBadEESuperCrystal','passEcalDeadCellTP','passBeamHalo2016','passBadEcalSC','passBadMuon','passBadChargedHadron','badMuonsFlag','duplicateMuonsFlag','noBadMuonsFlag']
_variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER']
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

	#MCDistStartup15 = [4.8551E-07,1.74806E-06,3.30868E-06,1.62972E-05,4.95667E-05,0.000606966,0.003307249,0.010340741,0.022852296,0.041948781,0.058609363,0.067475755,0.072817826,0.075931405,0.076782504,0.076202319,0.074502547,0.072355135,0.069642102,0.064920999,0.05725576,0.047289348,0.036528446,0.026376131,0.017806872,0.011249422,0.006643385,0.003662904,0.001899681,0.00095614,0.00050028,0.000297353,0.000208717,0.000165856,0.000139974,0.000120481,0.000103826,8.88868E-05,7.53323E-05,6.30863E-05,5.21356E-05,4.24754E-05,3.40876E-05,2.69282E-05,2.09267E-05,1.5989E-05,4.8551E-06,2.42755E-06,4.8551E-07,2.42755E-07,1.21378E-07,4.8551E-08]#Updated to 2015, from https://github.com/cms-sw/cmssw/blob/CMSSW_7_6_X/SimGeneral/MixingModule/python/mix_2015_25ns_Startup_PoissonOOTPU_cfi.py and https://twiki.cern.ch/twiki/bin/view/CMS/PdmVPileUpDescription#Run_2_and_Upgrades

	#MCDistStartup16 = [0.000829312873542,0.00124276120498,0.00339329181587,0.00408224735376,0.00383036590008,0.00659159288946,0.00816022734493,0.00943640833116,0.0137777376066,0.017059392038,0.0213193035468,0.0247343174676,0.0280848773878,0.0323308476564,0.0370394341409,0.0456917721191,0.0558762890594,0.0576956187107,0.0625325287017,0.0591603758776,0.0656650815128,0.0678329011676,0.0625142146389,0.0548068448797,0.0503893295063,0.040209818868,0.0374446988111,0.0299661572042,0.0272024759921,0.0219328403791,0.0179586571619,0.0142926728247,0.00839941654725,0.00522366397213,0.00224457976761,0.000779274977993,0.000197066585944,7.16031761328e-05,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]#Updated to 2016, from https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/SimGeneral/MixingModule/python/mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi.py and https://twiki.cern.ch/twiki/bin/view/CMS/PdmVPileUpDescription#Run_2_and_Upgrades

	MCDistSummer16 = [1.78653e-05 ,2.56602e-05 ,5.27857e-05 ,8.88954e-05 ,0.000109362 ,0.000140973 ,0.000240998 ,0.00071209 ,0.00130121 ,0.00245255 ,0.00502589 ,0.00919534 ,0.0146697 ,0.0204126 ,0.0267586 ,0.0337697 ,0.0401478 ,0.0450159 ,0.0490577 ,0.0524855 ,0.0548159 ,0.0559937 ,0.0554468 ,0.0537687 ,0.0512055 ,0.0476713 ,0.0435312 ,0.0393107 ,0.0349812 ,0.0307413 ,0.0272425 ,0.0237115 ,0.0208329 ,0.0182459 ,0.0160712 ,0.0142498 ,0.012804 ,0.011571 ,0.010547 ,0.00959489 ,0.00891718 ,0.00829292 ,0.0076195 ,0.0069806 ,0.0062025 ,0.00546581 ,0.00484127 ,0.00407168 ,0.00337681 ,0.00269893 ,0.00212473 ,0.00160208 ,0.00117884 ,0.000859662 ,0.000569085 ,0.000365431 ,0.000243565 ,0.00015688 ,9.88128e-05 ,6.53783e-05 ,3.73924e-05 ,2.61382e-05 ,2.0307e-05 ,1.73032e-05 ,1.435e-05 ,1.36486e-05 ,1.35555e-05 ,1.37491e-05 ,1.34255e-05 ,1.33987e-05 ,1.34061e-05 ,1.34211e-05 ,1.34177e-05 ,1.32959e-05 ,1.33287e-05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]# from https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2016Analysis and https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/SimGeneral/MixingModule/python/mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi.py

    # This is the standard (all of 2016) pileup scenario
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
	#finalfout = options.dir+'/'+name.replace('.root','_tree.root')
	finalfout = options.dir+'/'+name.split('/')[-1].replace('.root','_tree.root')

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

#BadEcalSCRunLumiEventsNew = GetRunLumiEventListNew('ecalscn1043093.txt')
#BadMuonRunLumiEventsNew = GetRunLumiEventListNew('muonBadTrack.txt')
#BadTrackResRunLumiEventsNew = GetRunLumiEventListNew('badResolutionTrack.txt')
#BadBeamHaloRunLumiEventsNew = GetRunLumiEventListNew('csc2015.txt')

#BadBeamHaloRunLumiEvents = GetRunLumiEventList('csc2015.txt')
#BadEcalSCRunLumiEvents = GetRunLumiEventList('ecalscn1043093.txt')

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
	global options
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

def CheckTriggerObjects(T,mu1,mu2,trig1,trig2):
	#Purpose: check whether muon1 or muon2 (or both, or neither) triggered one of the required HLT paths in the event
	mu1Matches,mu2Matches=False,False
	for n in range(len(T.HLTriggerObjPt)):
		lf1,lf2 = False,False
		hltObj = TLorentzVector()
		hltObj.SetPtEtaPhiM(T.HLTriggerObjPt[n], T.HLTriggerObjEta[n], T.HLTriggerObjPhi[n], 0)
		pt,eta,phi=T.HLTriggerObjPt[n],T.HLTriggerObjEta[n],T.HLTriggerObjPhi[n]
		for nn in range(len(T.HLTriggerObjPathNames[n])):
			pathName = T.HLTriggerObjPathNames[n][nn]
			if trig1 in pathName:
				lf1 = bool(T.HLTriggerObjPassedPathLastFilter[n][nn])
				#print trig1,lf1
			if trig2 in pathName:
				lf2 = bool(T.HLTriggerObjPassedPathLastFilter[n][nn])
				#print trig2,lf2
		if lf1==True:
			#print '---------'
			#print trig1,lf1
			#print pt,eta,phi
			#print mu1.Pt(),mu2.Pt()
			#print abs((pt-mu1.Pt()))/mu1.Pt(),abs(eta-mu1.Eta()),hltObj.DeltaPhi(mu1)
			#print abs((pt-mu2.Pt()))/mu2.Pt(),abs(eta-mu2.Eta()),hltObj.DeltaPhi(mu2)
			#print '---------'
			if abs((pt-mu1.Pt()))/mu1.Pt()<0.15 and abs(eta-mu1.Eta())<0.01 and hltObj.DeltaPhi(mu1)<0.01:
				mu1Matches=True
				#return mu1Matches,mu2Matches

			if abs((pt-mu2.Pt()))/mu2.Pt()<0.15 and abs(eta-mu2.Eta())<0.01 and hltObj.DeltaPhi(mu2)<0.01:
				mu2Matches=True
				#return mu1Matches,mu2Matches
		if lf2==True:
			#print '---------'
			#print trig2,lf2
			#print pt,eta,phi
			#print mu1.Pt(),mu2.Pt()
			#print abs((pt-mu1.Pt()))/mu1.Pt(),abs(eta-mu1.Eta()),hltObj.DeltaPhi(mu1)
			#print abs((pt-mu2.Pt()))/mu2.Pt(),abs(eta-mu2.Eta()),hltObj.DeltaPhi(mu2)
			#print '---------'
			if abs((pt-mu1.Pt()))/mu1.Pt()<0.15 and abs(eta-mu1.Eta())<0.01 and hltObj.DeltaPhi(mu1)<0.01:
				mu1Matches=True
				#return mu1Matches,mu2Matches

			if abs((pt-mu2.Pt()))/mu2.Pt()<0.15 and abs(eta-mu2.Eta())<0.01 and hltObj.DeltaPhi(mu2)<0.01:
				mu2Matches=True
				#return mu1Matches,mu2Matches
	return mu1Matches,mu2Matches


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
		if pdg not in [4,-4,3,-3]: #Get charm and strange quarks
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

def PropagatePTChangeToMET(met,original_object,varied_object):
	# Purpose: This takes an input TLorentzVector met representing the missing ET
	#         (no eta component), and an original object (arg 2), which has been
	#         kinmatically modified for a systematic (arg 3), and modifies the 
	#         met to compensate for the change in the object.
	return  met + varied_object - original_object


# def MuonsForJetSeparation(T):

# 	# Attempting to be the same as process.analysisPatMuons.finalCut = cms.string("isGlobalMuon & muonID('GlobalMuonPromptTight') & pt > 20")
# 	# GlobalTightPrompt is muon.isGlobalMuon() && muon.globalTrack()->normalizedChi2() < 10. && muon.globalTrack()->hitPattern().numberOfValidMuonHits() > 0
# 	muons = []
# 	for n in range(len(T.MuonPt)):
# 		Pass = True
# 		Pass *= T.MuonIsGlobal[n]
# 		Pass *= T.MuonGlobalChi2[n]<10.
# 		Pass *= T.MuonGlobalTrkValidHits[n]>=1
# 		Pass *= T.MuonPt[n] > 20.
# 		if Pass == True:
# 			ThisMu = TLorentzVector()
# 			ThisMu.SetPtEtaPhiM(T.MuonPt[n],T.MuonEta[n],T.MuonPhi[n],0)
# 			muons.append(ThisMu)
# 	return muons

# def TausForJetSeparation(T):
# 	# process.analysisPatTaus.preselection = cms.string(
# 	#     'tauID("decayModeFinding") > 0.5 &'
# 	#     ' tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits") > 0.5 &'
# 	#     ' tauID("againstMuonLoose3") > 0.5 &'
# 	#     ' tauID("againstElectronLooseMVA3") > 0.5'
# 	# )
# 	# process.analysisPatTaus.finalCut = cms.string('pt > 20. & abs(eta) < 2.3')
# 	taus = []
# 	for n in range(len(T.HPSTauPt)):
# 		Pass = True
# 		Pass *= T.HPSTauDecayModeFindingDiscr[n] > 0.5
# 		Pass *= T.HPSTauLooseCombinedIsolationDeltaBetaCorr3HitsDiscr[n] > 0.5
# 		Pass *= T.HPSTauAgainstMuonLoose3Discr[n]>0.5
# 		Pass *= T.HPSTauAgainstElectronLooseMVA3Discr[n] > 0.5
# 		Pass *= (T.HPSTauEta[n] > -2.3)*(T.HPSTauEta[n] < 2.3)
# 		Pass *= T.HPSTauPt[n] > 20.
# 		if Pass == True:
# 			ThisTau = TLorentzVector()
# 			ThisTau.SetPtEtaPhiM(T.HPSTauPt[n],T.HPSTauEta[n],T.HPSTauPhi[n],0)
# 			taus.append(ThisTau)
# 	return taus

def MEScorr(_T,_n,upordown):
	#print '\n'
	#print _n,len(_T.MuonCocktailPt)
	pt     = _T.MuonCocktailPt[_n]
	eta    = _T.MuonCocktailEta[_n]
	phi    = _T.MuonCocktailPhi[_n]
	charge = _T.MuonCharge[_n]
	#print pt,eta,phi,charge,upordown,
	while phi>math.pi: phi=phi-2.*math.pi
	while phi<-math.pi: phi=phi+2.*math.pi
	if pt<0 : return pt
	if eta<-2.4:
		print 'Eta<-2.4, setting to -2.399 for MES'
		eta=-2.399
	if eta>2.4:
		print 'Eta>2.4, setting to 2.399 for MES'
		eta=2.399
	etabins=[[-2.4, -2.1],[-2.1, -1.2],[-1.2, 0.],[-0., 1.2],[1.2, 2.1],[2.1, 2.4]]
	phibins=[[-math.pi,-math.pi/3],[-math.pi/3,math.pi/3],[math.pi/3,math.pi]]
	corrections    = [[-0.388122,0.376061,-0.153950],[-0.039346,0.041069,-0.113320],[0.,0.,0.],[0.,0.,0.],[0.005114,0.035573,0.070002],[-0.235470,-0.122719,0.091502]]
	correctionsErr = [[0.045881,0.090062,0.063053],[0.031655,0.030070,0.028683],[0.025,0.025,0.025],[0.025,0.025,0.025],[0.033115,0.038574,0.035002],[0.077534,0.061283,0.074502]]

	etabin,phibin = -999,-999
	for x in range(len(etabins)):
		if eta>etabins[x][0] and eta<etabins[x][1]:
			etabin=x
			break
	for x in range(len(phibins)):
		if phi>phibins[x][0] and phi<phibins[x][1]:
			phibin=x
			break
	correction    = corrections[etabin][phibin]
	correctionErr = correctionsErr[etabin][phibin]

	kappaBias = tRand.Gaus(correction,correctionErr)

	newPt = pt/1000.     #convert to TeV
	newPt = charge*newPt #convert to signed pt
	newPt = 1./newPt     #convert to curvature
	if upordown=='up': newPt = newPt + kappaBias
	elif upordown=='down': newPt = newPt - kappaBias
	else : print '-----------MES variation not up or down!!!!'

	newPt = 1./newPt     #return to pt
	newPt = abs(newPt)   #return unsigned pt
	newPt = newPt*1000.  #return to GeV
	#print newPt
	return newPt

def MERcorr(_T,_n):
	pt     = _T.MuonCocktailPt[_n]
	eta    = _T.MuonCocktailEta[_n]
	pt = pt+pt*tRand.Gaus(0.0,  (eta<1.4442)*(0.003*(pt<=200.0) + (0.005)*(pt>200.0)*(pt<=500.0) + 0.01*(pt>500.0)) + (eta>1.4442)*(0.006*(pt<=200.0) + (0.01)*(pt>200.0)*(pt<=500.0) + 0.02*(pt>500.0)))
	return pt
	
def TightHighPtIDMuons(T,_met,variation,isdata):
	# Purpose: Gets the collection of muons passing tight muon ID. 
	#         Returns muons as TLorentzVectors, and indices corrresponding
	#         to the surviving muons of the muon collection. 
	#         Also returns modified MET for systematic variations.
	muons = []
	muoninds = []
	_defaultPts = []
	if variation=='MESup':	
		#_MuonCocktailPt = [(pt + pt*(0.05*pt/1000.0)) for pt in T.MuonCocktailPt]#original
		#_MuonCocktailPt = [(pt + pt*(0.10*pt/1000.0)) for pt in T.MuonCocktailPt]#updated to Zprime 13TeV study number
		_MuonCocktailPt = [ MEScorr(T,ind,'up') for ind in range(len(T.MuonCocktailPt))]#updated to Generalized Endpoint method
	elif variation=='MESdown':	
		#_MuonCocktailPt = [(pt - pt*(0.05*pt/1000.0)) for pt in T.MuonCocktailPt]
		#_MuonCocktailPt = [(pt - pt*(0.10*pt/1000.0)) for pt in T.MuonCocktailPt]
		_MuonCocktailPt = [ MEScorr(T,ind,'down') for ind in range(len(T.MuonCocktailPt))]#updated to Generalized Endpoint method
	elif variation=='MER':	
		#_MuonCocktailPt = [pt+pt*tRand.Gaus(0.0,  0.01*(pt<=200.0) + (0.04)*(pt>200.0) ) for pt in T.MuonCocktailPt]
		# Updating to 2016 Zprime
		_MuonCocktailPt = [MERcorr(T,ind) for ind in range(len(T.MuonCocktailPt))]
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

	#nequiv = []
	#for n in range(len(T.MuonPt)):
	#	#if T.MuonIsGlobal[n] or newntupleswitch==True: #not necessary anymore - global muon requirement encompassed later
	#	nequiv.append(n)

	# Loop over muons using the pT array from above
	for n in range(len(_MuonCocktailPt)):

		# Some muon alignment studies use the inverse diff of the high pT and Trk pT values
		deltainvpt = -1.0	
		if ( T.MuonTrkPt[n] > 0.0 ) and (_MuonCocktailPt[n]>0.0):
			deltainvpt = ( 1.0/T.MuonTrkPt[n] - 1.0/_MuonCocktailPt[n])
	
		# For alignment correction studies in MC, the pT is modified according to
		# parameterizations of the position
		if alignementcorrswitch == True and isdata==False:
			if abs(deltainvpt) > 0.0000001:
				__Pt_mu = _MuonCocktailPt[n]
				__Eta_mu = T.MuonCocktailEta[n]
				__Phi_mu = T.MuonCocktailPhi[n]
				__Charge_mu = T.MuonCharge[n]
				if (__Pt_mu >200)*(abs(__Eta_mu) < 0.9)      : 
					_MuonCocktailPt[n] =  ( (1.0) / ( -5e-05*__Charge_mu*sin(-1.4514813+__Phi_mu ) + 1.0/__Pt_mu ) ) 
				deltainvpt = ( 1.0/T.MuonTrkPt[n] - 1.0/_MuonCocktailPt[n])


		# For the ID, begin by assuming it passes. Veto if it fails any condition
		# High PT conditions from https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId
		# NTuple definitions in https://raw.githubusercontent.com/CMSLQ/RootTupleMakerV2/master/src/RootTupleMakerV2_Muons.cc
		Pass = True
		# A preliminary pT cut. This also encompasses the GlobalMuon conditions, since
		# all non-global muons have cocktail pT of -1 in the ntuples.
		Pass *= (_MuonCocktailPt[n] > 45)     
		# Eta requirement
		Pass *= abs(T.MuonCocktailEta[n])<2.4

	        """
		#this uses the muon id flag for id, except for QCD study - produces many VERY high pt muons, don't trust it....
	        if nonisoswitch != True:
			Pass *= T.MuonIsHighPtMuon[n]>0
		        Pass *= (T.MuonTrackerIsoSumPT[n]/_MuonCocktailPt[n])<0.1
		else:	#For QCD study still need ID cuts in order to not apply isolation
			# Number of valid hits
			Pass *= T.MuonGlobalTrkValidHits[n]>=1
		        # Number of station matches
	                Pass *= T.MuonStationMatches[n]>1 
		        # Impact parameters
		        # Pass *= abs(T.MuonCocktailTrkVtxDXY[n]) < 0.2     
		        # Pass *= abs(T.MuonCocktailTrkVtxDZ[n]) < 0.5      
		        Pass *= abs(T.MuonBestTrackVtxDistXY[n]) < 0.2     # Fixed
		        Pass *= abs(T.MuonBestTrackVtxDistZ[n]) < 0.5      #Fixed 
		        # Pixel hits
		        Pass *= T.MuonTrkPixelHits[n]>=1  
		        # Layers with measurement (high PT ID cut is 5, used to be tight id cut at 8)
		        Pass *= T.MuonTrackLayersWithMeasurement[n] > 5 
		        Pass *= T.MuonCocktailPtError[n]/_MuonCocktailPt[n]  < 0.3
		        # Isolation condition using tracker-only isolation
		        if nonisoswitch != True:
			        Pass *= (T.MuonTrackerIsoSumPT[n]/_MuonCocktailPt[n])<0.1
		"""

		# this applies the cuts manually - safer
		# Number of valid hits
		Pass *= T.MuonGlobalTrkValidHits[n]>=1
                # Number of station matches
	        Pass *= T.MuonStationMatches[n]>1 
	        # Impact parameters
                # Pass *= abs(T.MuonCocktailTrkVtxDXY[n]) < 0.2     
		# Pass *= abs(T.MuonCocktailTrkVtxDZ[n]) < 0.5      
	        Pass *= abs(T.MuonBestTrackVtxDistXY[n]) < 0.2     # Fixed
	        Pass *= abs(T.MuonBestTrackVtxDistZ[n]) < 0.5      #Fixed 
	        # Pixel hits
	        Pass *= T.MuonTrkPixelHits[n]>=1  
		# Layers with measurement (high PT ID cut is 5, used to be tight id cut at 8)
		Pass *= T.MuonTrackLayersWithMeasurement[n] > 5 
		Pass *= T.MuonCocktailPtError[n]/_MuonCocktailPt[n]  < 0.3
		# Isolation condition using tracker-only isolation
		if nonisoswitch != True:
			Pass *= (T.MuonTrackerIsoSumPT[n]/_MuonCocktailPt[n])<0.1

		# Propagate MET changes if undergoing systematic variation
		if (Pass):
			NewMu = TLorentzVector()
			OldMu = TLorentzVector()
			NewMu.SetPtEtaPhiM(_MuonCocktailPt[n],T.MuonCocktailEta[n],T.MuonCocktailPhi[n],0)
			OldMu.SetPtEtaPhiM(T.MuonCocktailPt[n],T.MuonCocktailEta[n],T.MuonCocktailPhi[n],0)
			_met = PropagatePTChangeToMET(_met,OldMu,NewMu)

			# Append items to retun if the muon is good

			muons.append(NewMu)
			trk_isos.append((T.MuonTrackerIsoSumPT[n]/_MuonCocktailPt[n]))
			chi2.append(T.MuonGlobalChi2[n])
			pfid.append(T.MuonIsPF[n])
			layers.append(T.MuonTrackLayersWithMeasurement[n])
			charges.append(T.MuonCocktailCharge[n])
			muoninds.append(n)
			deltainvpts.append(deltainvpt)
			_defaultPts.append(T.MuonPt[n])

	return [muons,muoninds,_met,trk_isos,charges,deltainvpts,chi2,pfid,layers,_defaultPts]


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
		Pass *= (_ElectronPt > 45)
		Pass *= abs(T.ElectronEta[n])<2.5

		barrel = bool((abs(T.ElectronSCEta[n]))<1.4442)
		endcap = bool((abs(T.ElectronSCEta[n]))>1.566)
		Pass *= (barrel or endcap)
	
	        Pass *=bool( T.ElectronPassHEEPID[n])#fixme trying tag again instead of manual cuts
                """
		if barrel:
			Pass *= bool(T.ElectronIsEcalDriven[n])
			Pass *= T.ElectronDeltaEtaTrkSeedSC[n] < 0.004
			Pass *= T.ElectronDeltaPhiTrkSC[n] < 0.06
			Pass *= T.ElectronHoE[n] < 0.05 + 1./T.ElectronSCEnergy[n]
			Pass *= ((T.ElectronFull5x5E2x5OverE5x5[n] > 0.94) or (T.ElectronFull5x5E1x5OverE5x5[n] > 0.83) )
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
			if _ElectronPt[n]<50:
				Pass *= ((T.ElectronHcalIsoD1DR03[n] + T.ElectronEcalIsoDR03[n]) < (2.5 + 0.28*T.ElectronRhoIsoHEEP[n]))
			else:
				Pass *= ((T.ElectronHcalIsoD1DR03[n] + T.ElectronEcalIsoDR03[n]) < (2.5 + 0.03*(_ElectronPt[n]-50.0) + 0.28*T.ElectronRhoIsoHEEP[n]))
			Pass *= T.ElectronHeep70TrkIso < 5.0
			Pass *= T.ElectronMissingHits[n] <=1
			Pass *= T.ElectronLeadVtxDistXY[n]<0.05
		"""
		if (Pass):
			NewEl = TLorentzVector()
			OldEl = TLorentzVector()
			NewEl.SetPtEtaPhiM(_ElectronPt[n],T.ElectronEta[n],T.ElectronPhi[n],0)
			OldEl.SetPtEtaPhiM(T.ElectronPtHeep[n],T.ElectronEta[n],T.ElectronPhi[n],0)
			met = PropagatePTChangeToMET(_met,OldEl,NewEl)

		if (Pass):
			electrons.append(NewEl)
			electroninds.append(n)
	return [electrons,electroninds,_met]

def JERModifiedPt(res,resSF,resSFup,resSFdown,pt,eta,phi,T,modtype):
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
		if dR<bestdR:# and dR<0.3 :
			bestdR = dR
			bestn = n
			bestdpt = pt-gjet.Pt()

	abseta = abs(eta)
	#if abseta >= 0   : jfacs = [  0.05200 , 0.11515 , -0.00900 ]
	#if abseta >= 0.5 : jfacs = [  0.05700 , 0.11427 , 0.00200  ]
	#if abseta >= 1.1 : jfacs = [  0.09600 , 0.16125 , 0.03400  ]
	#if abseta >= 1.7 : jfacs = [  0.13400 , 0.22778 , 0.04900  ]
	#if abseta >= 2.3 : jfacs = [  0.28800 , 0.48838 , 0.13500  ]

        #13 TeV 74X (2015) DATA/MC SFs
	#if abseta >= 0   : jfacs = [  0.061 , 0.084 , 0.038  ]
	#if abseta >= 0.8 : jfacs = [  0.088 , 0.117 , 0.059  ]
	#if abseta >= 1.3 : jfacs = [  0.106 , 0.136 , 0.076  ]
	#if abseta >= 1.9 : jfacs = [  0.126 , 0.220 , 0.032  ]
	#if abseta >= 2.5 : jfacs = [  0.343 , 0.466 , 0.220  ]
	#if abseta >= 3.0 : jfacs = [  0.303 , 0.414 , 0.192  ]
	#if abseta >= 3.2 : jfacs = [  0.320 , 0.606 , 0.034  ]

        #13 TeV 80X (2016, ICHEP) DATA/MC SFs
	#if abseta >= 0   : jfacs = [  0.122 , 0.148 , 0.096  ]
	#if abseta >= 0.5 : jfacs = [  0.167 , 0.215 , 0.119  ]
	#if abseta >= 0.8 : jfacs = [  0.168 , 0.214 , 0.122  ]
	#if abseta >= 1.1 : jfacs = [  0.029 , 0.095 ,-0.037  ]
	#if abseta >= 1.3 : jfacs = [  0.115 , 0.145 , 0.085  ]
	#if abseta >= 1.7 : jfacs = [  0.041 , 0.103 ,-0.021  ]
	#if abseta >= 1.9 : jfacs = [  0.167 , 0.253 , 0.081  ]
	#if abseta >= 2.1 : jfacs = [  0.094 , 0.187 , 0.001  ]
	#if abseta >= 2.3 : jfacs = [  0.168 , 0.288 , 0.048  ]
	#if abseta >= 2.5 : jfacs = [  0.266 , 0.398 , 0.134  ]
	#if abseta >= 2.8 : jfacs = [  0.595 , 0.770 , 0.420  ]
	#if abseta >= 3.0 : jfacs = [ -0.002 , 0.064 ,-0.068  ]
	#if abseta >= 3.2 : jfacs = [  0.226 , 0.371 , 0.081  ]

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


	adjustmentfactor=0.0
	#Using hybrid method: https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution#Smearing_procedures
	if bestdR>0.2 or abs(bestdpt)>3*res*pt:#stochastic method
		if modtype == '':
			adjustmentfactor =  pt*normalvariate(0,res)*math.sqrt(max(resSF**2-1,0))
		if modtype == 'up':
			adjustmentfactor =  pt*normalvariate(0,res)*math.sqrt(max(resSFup**2-1,0))
		if modtype == 'down':
			adjustmentfactor =  pt*normalvariate(0,res)*math.sqrt(max(resSFdown**2-1,0))
	else:#scaling method
		if modtype == '':
			adjustmentfactor = (resSF-1)*bestdpt
		if modtype == 'up':
			adjustmentfactor = (resSFup-1)*bestdpt
		if modtype == 'down':
			adjustmentfactor = (resSFdown-1)*bestdpt
	#if modtype=='' :
	#	print (bestdR>0.2 or abs(bestdpt)>3*res*pt)*"did stochastic"+(bestdR<0.2 and abs(bestdpt)<3*res*pt)*"did scaling"
	#	print "bestdR:",bestdR,"abs(bestdpt)<3*res*pt:",abs(bestdpt)<3*res*pt
	#	print "pt:",pt,"factor:",adjustmentfactor,"adjusted pt:",pt+adjustmentfactor,"\n"

	"""
	if modtype == '':
		adjustmentfactor = jfacs[0]
	if modtype == 'up':
		adjustmentfactor = jfacs[1]
	if modtype == 'down':
		adjustmentfactor = jfacs[2]
	"""

	#ptadjustment = adjustmentfactor*bestdpt
	#pt += ptadjustment
	pt += adjustmentfactor
	return max(0.,pt)

def LooseIDJets(T,met,variation,isdata):
	# Pupose: Gets the collection of jets passing loose PFJet ID. 
	#         Returns jets as TLorentzVectors, and indices corrresponding
	#         to the surviving jetss of the jet collection. 
	#         Also returns modified MET for systematic variations.	

	if variation!='JERup' and variation!='JERdown':
		#_PFJetPt = [JERModifiedPt(T.PFJetJERResAK4CHS[n],T.PFJetJERResSFAK4CHS[n],T.PFJetJERResSFUpAK4CHS[n],T.PFJetJERResSFDownAK4CHS[n],T.PFJetPtAK4CHS[n],T.PFJetEtaAK4CHS[n],T.PFJetPhiAK4CHS[n],T,'') for n in range(len(T.PFJetPtAK4CHS))] 	
		_PFJetPt = [pt for pt in T.PFJetPtAK4CHS]				
	if variation=='JERup':	
		_PFJetPt = [JERModifiedPt(T.PFJetJERResAK4CHS[n],T.PFJetJERResSFAK4CHS[n],T.PFJetJERResSFUpAK4CHS[n],T.PFJetJERResSFDownAK4CHS[n],T.PFJetPtAK4CHS[n],T.PFJetEtaAK4CHS[n],T.PFJetPhiAK4CHS[n],T,'up') for n in range(len(T.PFJetPtAK4CHS))] 
	if variation=='JERdown':	
		_PFJetPt = [JERModifiedPt(T.PFJetJERResAK4CHS[n],T.PFJetJERResSFAK4CHS[n],T.PFJetJERResSFUpAK4CHS[n],T.PFJetJERResSFDownAK4CHS[n],T.PFJetPtAK4CHS[n],T.PFJetEtaAK4CHS[n],T.PFJetPhiAK4CHS[n],T,'down') for n in range(len(T.PFJetPtAK4CHS))] 		

	if variation=='JESup':	
		_PFJetPt = [ _PFJetPt[n]*(1.0+T.PFJetJECUncAK4CHS[n]) for n in range(len(_PFJetPt))]
	if variation=='JESdown':	
		_PFJetPt = [ _PFJetPt[n]*(1.0-T.PFJetJECUncAK4CHS[n]) for n in range(len(_PFJetPt))]

	if (isdata):
		_PFJetPt = [pt for pt in T.PFJetPtAK4CHS]	
		#_PFJetPt = [T.PFJetPtAK4CHS[n]*T.PFJetL2L3ResJECAK4CHS[n] for n in range(len(T.PFJetPtAK4CHS))]	

	# print met.Pt(),


	JetFailThreshold=0.0

	jets=[]
	jetinds = []
	NHFs = []
	NEMFs = []
	CSVscores = []
	CMVAscores = []
	PUIds = []
	for n in range(len(_PFJetPt)):
		if _PFJetPt[n]>40 and abs(T.PFJetEtaAK4CHS[n])<2.4 :
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
			if looseJetID:#T.PFJetPassLooseIDAK4CHS[n]==1:
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
				CMVAscores.append(T.PFJetCombinedMVABTagAK4CHS[n])
				PUIds.append([T.PFJetPileupMVApassesLooseAK4CHS[n],T.PFJetPileupMVApassesMediumAK4CHS[n],T.PFJetPileupMVApassesTightAK4CHS[n]])
			else:
				if _PFJetPt[n] > JetFailThreshold:
					JetFailThreshold = _PFJetPt[n]

	# print met.Pt()

	return [jets,jetinds,met,JetFailThreshold,NHFs,NEMFs,CSVscores,CMVAscores,PUIds]
def GetLLJJMasses(l1,l2,j1,j2):
	# Purpose: For LLJJ channels, this function returns two L-J Masses, corresponding to the
	#         pair of L-Js which minimizes the difference between LQ masses in the event

	# These are the invariant mass combinations 
	m11 = (l1+j1).M()
	m12 = (l1+j2).M()
	m21 = (l2+j1).M()
	m22 = (l2+j2).M()
	mh = 0.0 # This will be the invariant mass of the lepton and leading jet

	# Difference in Mass for the two matching scenarios
	diff1 = abs(m21-m12)
	diff2 = abs(m11-m22)

	# The ideal match minimizes the Mass difference above
	# Based on the the diffs, store the appropriate pairs	
	if diff1 < diff2:
		pair =  [m21,m12] # The invariant mass pair
		mh = m21          # invariant mass corresponding to leading jet
	else:
		pair = [m11,m22]  # The invariant mass pair
		mh = m11          # invariant mass corresponding to leading jet
	least = min(diff1,diff2)
	#print '2Jet min:',least,'masses: ',pair[0],pair[1]
	pair.sort()
	pair.reverse()
	pair.append(mh)
	return pair

def GetLLJJMassesRelative(l1,l2,j1,j2):
	# Purpose: For LLJJ channels, this function returns two L-J Masses, corresponding to the
	#         pair of L-Js which minimizes the difference between LQ masses in the event

	# These are the invariant mass combinations 
	m11 = (l1+j1).M()
	m12 = (l1+j2).M()
	m21 = (l2+j1).M()
	m22 = (l2+j2).M()
	mh = 0.0 # This will be the invariant mass of the lepton and leading jet

	# Difference in Mass for the two matching scenarios
	if m12>0:
		diff1 = abs(m21-m12)/m12
	else:
		diff1 = 9999
	if m11>0:
		diff2 = abs(m11-m22)/m11
	else:
		diff2 = 10000

	# The ideal match minimizes the Mass difference above
	# Based on the the diffs, store the appropriate pairs	
	if diff1 < diff2:
		pair =  [m21,m12] # The invariant mass pair
		mh = m21          # invariant mass corresponding to leading jet
	else:
		pair = [m11,m22]  # The invariant mass pair
		mh = m11          # invariant mass corresponding to leading jet
	least = min(diff1,diff2)
	#print '2Jet min:',least,'masses: ',pair[0],pair[1]
	pair.sort()
	pair.reverse()
	pair.append(mh)
	return pair

def GetLLJJMasses3JetsRelative(l1,l2,j1,j2,j3):

	m11 = (l1+j1).M()
	m12 = (l1+j2).M()
	m13 = (l1+j3).M()
	m21 = (l2+j1).M()
	m22 = (l2+j2).M()
	m23 = (l2+j3).M()

	j1pt = j1.Pt()
	j2pt = j2.Pt()

	if j1pt > 0:
		diff1 = abs(m11-m22)/j1pt
		diff2 = abs(m11-m23)/j1pt
		diff3 = abs(m12-m21)/j1pt
		diff5 = abs(m13-m21)/j1pt
	else:
		diff1 = 9999
		diff2 = 10000
		diff3 = 10000
		diff5 = 10000
	if j2pt > 0:
		diff4 = abs(m12-m23)/j2pt
		diff6 = abs(m13-m22)/j2pt
	else:
		diff4 = 9999
		diff6 = 10000

	least = min(diff1,diff2,diff3,diff4,diff5,diff6)
	
	if least == diff1 :
		pair = [m11,m22] # The invariant mass pair
		mh = m11 # invariant mass corresponding to leading jet
	elif least == diff2:
		pair = [m11,m23] # The invariant mass pair
		mh = m11 # invariant mass corresponding to leading jet
	elif least == diff3:
		pair = [m12,m21] # The invariant mass pair
		mh = m21 # invariant mass corresponding to leading jet
	elif least == diff4:
		pair = [m12,m23] # The invariant mass pair
		mh = m12 # invariant mass corresponding to leading jet
	elif least == diff5:
		pair = [m13,m21] # The invariant mass pair
		mh = m21 # invariant mass corresponding to leading jet
	elif least == diff6:
		pair = [m13,m22] # The invariant mass pair
		mh = m22 # invariant mass corresponding to leading jet
        else:
		pair = [0,0]
		mh=0
	#print '3Jet min:',least,'masses: ',pair[0],pair[1]
	pair.sort()
	pair.reverse()
	pair.append(mh)
	return pair

def GetLLJJMasses4Jets(l1,l2,j1,j2,j3,j4):

	m11 = (l1+j1).M()
	m12 = (l1+j2).M()
	m13 = (l1+j3).M()
	m14 = (l1+j4).M()
	m21 = (l2+j1).M()
	m22 = (l2+j2).M()
	m23 = (l2+j3).M()
	m24 = (l2+j4).M()

	diff1  = abs(m11-m22)
	diff2  = abs(m11-m23)
	diff3  = abs(m11-m24)
	diff4  = abs(m12-m21)
	diff5  = abs(m12-m23)
	diff6  = abs(m12-m24)
	diff7  = abs(m13-m21)
	diff8  = abs(m13-m22)
	diff9  = abs(m13-m24)
	diff10 = abs(m14-m21)
	diff11 = abs(m14-m22)
	diff12 = abs(m14-m23)

	least = min(diff1,diff2,diff3,diff4,diff5,diff6,diff7,diff8,diff9,diff10,diff11,diff12)
	if least == diff1 :
		pair = [m11,m22] # The invariant mass pair
		mh = m11 # invariant mass corresponding to leading jet
	elif least == diff2:
		pair = [m11,m23] # The invariant mass pair
		mh = m11 # invariant mass corresponding to leading jet
	elif least == diff3:
		pair = [m12,m21] # The invariant mass pair
		mh = m21 # invariant mass corresponding to leading jet
	elif least == diff4:
		pair = [m12,m23] # The invariant mass pair
		mh = m12 # invariant mass corresponding to leading jet
	elif least == diff5:
		pair = [m13,m21] # The invariant mass pair
		mh = m21 # invariant mass corresponding to leading jet
	elif least == diff6:
		pair = [m13,m22] # The invariant mass pair
		mh = m22 # invariant mass corresponding to leading jet
	elif least == diff7 :
		pair = [m13,m21] # The invariant mass pair
		mh = m21 # invariant mass corresponding to leading jet
	elif least == diff8:
		pair = [m13,m22] # The invariant mass pair
		mh = m22 # invariant mass corresponding to leading jet
	elif least == diff9:
		pair = [m13,m24] # The invariant mass pair
		mh = m13 # invariant mass corresponding to leading jet
	elif least == diff10:
		pair = [m14,m21] # The invariant mass pair
		mh = m21 # invariant mass corresponding to leading jet
	elif least == diff11:
		pair = [m14,m22] # The invariant mass pair
		mh = m22 # invariant mass corresponding to leading jet
	elif least == diff12:
		pair = [m14,m23] # The invariant mass pair
		mh = m23 # invariant mass corresponding to leading jet
        else:
		pair = [0,0]
		mh=0

	#print '4Jet min:',least,'masses: ',pair[0],pair[1]
	pair.sort()
	pair.reverse()
	pair.append(mh)
	return pair

def GetLVJJMasses(l1,met,j1,j2):
	# Purpose: For LVJJ channels, this function returns two L-J Masses, and an LJ mass and mT, 
	#         Quantities corresponding to the pair of L-Js which minimizes the difference 
	#         between LQ masses in the event

	# These are the lepton-jet masses
	m11 = (l1+j1).M()
	m12 = (l1+j2).M()
	# These are the lepton-jet transverse masses
	mt11 = TransMass(l1,j1)
	mt12 = TransMass(l1,j2)
	# These are the met-jet transverse masses
	mte1 = TransMass(met,j1)
	mte2 = TransMass(met,j2)
	mh = 0.0	
	# Difference in MT for the two matching scenarios
	diff1 = abs(mte1-mt12)  # MET matched to jet1, lepton matched to jet2
	diff2 = abs(mt11-mte2)  # MET matched to jet2, lepton matched to jet1
	# The ideal match minimizes the MT difference above
	# Based on the the diffs, store the appropriate pairs
	if diff1 < diff2:
		pair =  [mte1,mt12]      # These are the two trans-mass values
		pairwithinv = [m12,mte1] # Instead we could store one invariant mass and one trans mass
	# This is the other matching possibility
	else:
		pair = [mt11,mte2]
		invmass = m11
		mh = m11 # The invariant mass pair with the leading jet
		pairwithinv = [m11,mte2]
	# Let put the pair of trans-masses in pT order
	pair.sort()
	pair.reverse()
	
	return [pair,pairwithinv,mh]

def compareMatchingLVJJ(mus,matchedMus,jets,matchedJets):
	#Purpose: check how often the muons and jets are picked correctly - munujj
	#print 'len(matchedMus):',len(matchedMus)
	#print 'len(matchedJets):',len(matchedJets)
	if len(matchedMus)<1 or len(matchedJets)<2 :
		return -1
	#print 'mus[0].Pt():',mus[0].Pt()
	#print 'mus[1].Pt():',mus[1].Pt()
	#print 'matchedMus[0].Pt()',matchedMus[0].Pt()
	#print 'matchedMus[1].Pt()',matchedMus[1].Pt()
	#print 'jets[0].Pt():',jets[0].Pt()
	#print 'jets[1].Pt():',jets[1].Pt()
	#print 'matchedJets[0].Pt()',matchedJets[0].Pt()
	#print 'matchedJets[1].Pt()',matchedJets[1].Pt()
	if (matchedMus[0].Pt()<5 and matchedMus[1].Pt()<5) or matchedJets[0].Pt()<5 or matchedJets[1].Pt()<5 or (mus[0].Pt()<5 and mus[1].Pt()<5) or jets[0].Pt()<5 or jets[1].Pt()<5:
		return -1
	dRmu11 =  mus[0].DeltaR(matchedMus[0])
	dRmu12 =  mus[0].DeltaR(matchedMus[1])
	#dRmu21 =  mus[1].DeltaR(matchedMus[0])
	#dRmu22 =  mus[1].DeltaR(matchedMus[1])
	dRj11  = jets[0].DeltaR(matchedJets[0])
	dRj12  = jets[0].DeltaR(matchedJets[1])
	dRj21  = jets[1].DeltaR(matchedJets[0])
	dRj22  = jets[1].DeltaR(matchedJets[1])
	#if( (dRmu11<0.1 or dRmu12<0.1) and (dRmu21<0.1 or dRmu22<0.1) and (dRj11<0.1 or dRj12<0.1) and (dRj21<0.1 or dRj22<0.1) ):
	if( (dRmu11<0.1 or dRmu12<0.1) and (dRj11<0.1 or dRj12<0.1) and (dRj21<0.1 or dRj22<0.1) ):
		return 1
	else:
		return 0

def compareMatching(mus,matchedMus,jets,matchedJets):
	#Purpose: check how often the muons and jets are picked correctly
	if len(matchedMus)<2 or len(matchedJets)<2 :
		return -1
	if matchedMus[0].Pt()<5 or matchedMus[1].Pt()<5 or matchedJets[0].Pt()<5 or matchedJets[1].Pt()<5 or mus[0].Pt()<5 or mus[1].Pt()<5 or jets[0].Pt()<5 or jets[1].Pt()<5:
		return -1
	dRmu11 =  mus[0].DeltaR(matchedMus[0])
	dRmu12 =  mus[0].DeltaR(matchedMus[1])
	dRmu21 =  mus[1].DeltaR(matchedMus[0])
	dRmu22 =  mus[1].DeltaR(matchedMus[1])
	dRj11  = jets[0].DeltaR(matchedJets[0])
	dRj12  = jets[0].DeltaR(matchedJets[1])
	dRj21  = jets[1].DeltaR(matchedJets[0])
	dRj22  = jets[1].DeltaR(matchedJets[1])
	if( (dRmu11<0.1 or dRmu12<0.1) and (dRmu21<0.1 or dRmu22<0.1) and (dRj11<0.1 or dRj12<0.1) and (dRj21<0.1 or dRj22<0.1) ):
		return 1
	else:
		return 0

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

	#_passWptCut = T.GenParticleWorZSystemPt<100.0#checkWpt(T,0,100)
	[_passWptCut,_WSystemPt] = checkWorZpt(T,0,100,'W')
	[_passZptCut,_ZSystemPt] = checkWorZpt(T,0,50,'Z')
	_WorZSystemPt = T.GenParticleWorZSystemPt
	#print 'passWptCut:',passWptCut

        #ptHat
	_ptHat = T.PtHat
	# MET as a vector
	met = MetVector(T)
	# ID Muons,Electrons
	[muons,goodmuoninds,met,trkisos,charges,dpts,chi2,pfid,layers,defaultPts] = TightHighPtIDMuons(T,met,variation,T.isData)
	# muons_forjetsep = MuonsForJetSeparation(T)
	# taus_forjetsep = TausForJetSeparation(T)
	[electrons,electroninds,met] = HEEPElectrons(T,met,variation)
	# ID Jets and filter from muons
	[jets,jetinds,met,failthreshold,neutralhadronEF,neutralemEF,btagCSVscores,btagCMVAscores,PUIds] = LooseIDJets(T,met,variation,T.isData)
	# jets = GeomFilterCollection(jets,muons_forjetsep,0.5)
	jets = GeomFilterCollection(jets,muons,0.5)
	jets = GeomFilterCollection(jets,electrons,0.5)
	# jets = GeomFilterCollection(jets,taus_forjetsep,0.5)
	# Empty lorenz vector for bookkeeping
	EmptyLorentz = TLorentzVector()
	EmptyLorentz.SetPtEtaPhiM(.01,0,0,0)

	# Muon and Jet Counts
	_mucount = len(muons)
	_elcount = len(electrons)
	_jetcount = len(jets)

	# Make sure there are two of every object, even if zero
	if len(muons) < 1 : 
		muons.append(EmptyLorentz)
		trkisos.append(0.0)
		charges.append(0.0)
		dpts.append(-1.0)
		chi2.append(-1.0)
		pfid.append(-1.0)
		layers.append(-1.0)
		defaultPts.append(-1.0)

	if len(muons) < 2 : 
		muons.append(EmptyLorentz)
		trkisos.append(0.0)
		charges.append(0.0)		
		dpts.append(-1.0)
		chi2.append(-1.0)
		pfid.append(-1.0)
		layers.append(-1.0)
		defaultPts.append(-1.0)

	if len(electrons) < 1 : electrons.append(EmptyLorentz)
	if len(electrons) < 2 : electrons.append(EmptyLorentz)	
	if len(jets) < 1 : 
		jets.append(EmptyLorentz)
		neutralhadronEF.append(0.0)
		neutralemEF.append(0.0)
		btagCSVscores.append(-5.0)
		btagCMVAscores.append(-5.0)
		PUIds.append([-5.0,-5.0,-5.0])
	if len(jets) < 2 : 
		jets.append(EmptyLorentz)
		neutralhadronEF.append(0.0)
		neutralemEF.append(0.0)		
		btagCSVscores.append(-5.0)
		btagCMVAscores.append(-5.0)
		PUIds.append([-5.0,-5.0,-5.0])
	_ismuon_muon1 = 1.0
	_ismuon_muon2 = 1.0

	if emuswitch == True:
		if muons[0].Pt() > electrons[0].Pt():
			muons[1] = electrons[0]
			_ismuon_muon2 = 0.0
		else:
			muons[1] = muons[0]
			muons[0] = electrons[0]
			_ismuon_muon1=0.0


	_passTrigMu1,_passTrigMu2 = CheckTriggerObjects(t,muons[0],muons[1],"HLT_Mu50_v","HLT_TkMu50_v")
	#print 	_passTrigMu1,_passTrigMu2,"\n"

	[_genMuons,_matchedRecoMuons,muonInd] = MuonsFromLQ(T)
	[_genJets,_matchedRecoJets,jetInd] = JetsFromLQ(T)
	#print 'muon index:',muonInd,'  jet index:',jetInd
	_muonInd1=muonInd[0]
	_muonInd2=muonInd[1]
	_jetInd1=jetInd[0]
	_jetInd2=jetInd[1]

	#[_Muujj1_gen,_Muujj2_gen]=GetLLJJMassesGen(muonInd,jetInd);


	# Get kinematic quantities
	[_ptmu1,_etamu1,_phimu1,_isomu1,_qmu1,_dptmu1] = [muons[0].Pt(),muons[0].Eta(),muons[0].Phi(),trkisos[0],charges[0],dpts[0]]
	[_ptmu2,_etamu2,_phimu2,_isomu2,_qmu2,_dptmu2] = [muons[1].Pt(),muons[1].Eta(),muons[1].Phi(),trkisos[1],charges[1],dpts[1]]
	_ptmu1mu2 = (muons[0]+muons[1]).Pt()
	_ptmu1_default = defaultPts[0]
	_ptmu2_default = defaultPts[1]

	[_chimu1,_chimu2] = [chi2[0],chi2[1]]
	[_ispfmu1,ispfmu2] = [pfid[0],pfid[1]]
	[_layersmu1,_layersmu2] = [layers[0],layers[1]]

	[_ptel1,_etael1,_phiel1] = [electrons[0].Pt(),electrons[0].Eta(),electrons[0].Phi()]
	[_ptel2,_etael2,_phiel2] = [electrons[1].Pt(),electrons[1].Eta(),electrons[1].Phi()]
	[_ptj1,_etaj1,_phij1]    = [jets[0].Pt(),jets[0].Eta(),jets[0].Phi()]
	[_ptj2,_etaj2,_phij2]    = [jets[1].Pt(),jets[1].Eta(),jets[1].Phi()]
	[_nhefj1,_nhefj2,_nemefj1,_nemefj2] = [neutralhadronEF[0],neutralhadronEF[1],neutralemEF[0],neutralemEF [1]]
	[_ptmet,_etamet,_phimet] = [met.Pt(),0,met.Phi()]
	[_xmiss,_ymiss] = [met.Px(),met.Py()]
	[_CSVj1,_CSVj2] = [btagCSVscores[0],btagCSVscores[1]]
	[_CMVAj1,_CMVAj2] = [btagCMVAscores[0],btagCMVAscores[1]]
	[_PULoosej1,_PUMediumj1,_PUTightj1] = PUIds[0]
	[_PULoosej2,_PUMediumj2,_PUTightj2] = PUIds[1]

	_stuujj = ST([muons[0],muons[1],jets[0],jets[1]])
	_stuvjj = ST([muons[0],met,jets[0],jets[1]])

	_steejj = ST([electrons[0],electrons[1],jets[0],jets[1]])
	_stevjj = ST([electrons[0],met,jets[0],jets[1]])


	_Muu = (muons[0]+muons[1]).M()
	_MTuv = TransMass(muons[0],met)
	_Mjj = (jets[0]+jets[1]).M()
	_DRuu = (muons[0]).DeltaR(muons[1])
	_DPHIuv = abs((muons[0]).DeltaPhi(met))
	_DPHIj1v = abs((jets[0]).DeltaPhi(met))
	_DPHIj2v = abs((jets[1]).DeltaPhi(met))

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

	_Muujj1_gen=0
	_Muujj2_gen=0
	_MHuujj_gen=0
	_Muujjavg_gen=0
	#if(_jetInd1 != -99 and _jetInd2 != -99 and len(jets) > _jetInd2 and len(jets) > _jetInd1): 
	#	print _muonInd1,_muonInd2,_jetInd1,_jetInd2
	#	print '#jets: ',len(jets)
	if (len(_genMuons)>1 and len(_genJets)>1) :
		[_Muujj1_gen,_Muujj2_gen,_MHuujj_gen] = GetLLJJMasses(_genMuons[0],_genMuons[1],_genJets[0],_genJets[1])
		_Muujjavg_gen = 0.5*(_Muujj1_gen + _Muujj1_gen)
	else :
		[_Muujj1_gen,_Muujj2_gen,_MHuujj_gen] = [0,0,0]
		_Muujjavg_gen = 0

	if len(_matchedRecoMuons)>1 and len(_matchedRecoJets)>1 :
		[_Muujj1_genMatched,_Muujj2_genMatched,_MHuujj_genMatched] = GetLLJJMasses(_matchedRecoMuons[0],_matchedRecoMuons[1],_matchedRecoJets[0],_matchedRecoJets[1])
		_Muujjavg_genMatched = 0.5*(_Muujj1_genMatched + _Muujj1_genMatched)
	else :
		
		[_Muujj1_genMatched,_Muujj2_genMatched,_MHuujj_genMatched] = [0,0,0]
		_Muujjavg_genMatched = 0

	[_Muujj1, _Muujj2,_MHuujj] = GetLLJJMasses(muons[0],muons[1],jets[0],jets[1])

	_matchedLQ     = compareMatching(muons,_matchedRecoMuons,jets,_matchedRecoJets)
	while len(_matchedRecoMuons)<2:
		_matchedRecoMuons.append(EmptyLorentz)
	while len(_matchedRecoJets)<2:
		_matchedRecoJets.append(EmptyLorentz)
	_matchedLQ_LVJJ = compareMatchingLVJJ(muons,_matchedRecoMuons,jets,_matchedRecoJets)

	_Muujj = (muons[0]+muons[1]+jets[0]+jets[1]).M()
	_Muuj1   = (muons[0]+muons[1]+jets[0]).M()
	_Muuj2   = (muons[0]+muons[1]+jets[1]).M()
	_Mu1j1j2 = (muons[0]+jets[0]+jets[1]).M()
	_Mu2j1j2 = (muons[1]+jets[0]+jets[1]).M()

	if len(electrons)>=1 :
		_pte1 = electrons[0].Pt()
		if len(electrons)>=2 : _pte2 = electrons[1].Pt()
		else : _pte2 = 0.
	else :
		_pte1 = 0.


	[[_MTuvjj1, _MTuvjj2], [_Muvjj, _MTuvjj],_MHuvjj] = GetLVJJMasses(muons[0],met,jets[0],jets[1])

	[_Meejj1, _Meejj2,_MHeejj] = GetLLJJMasses(electrons[0],electrons[1],jets[0],jets[1])
	[[_MTevjj1, _MTevjj2], [_Mevjj, _MTevjj],_MHevjj] = GetLVJJMasses(electrons[0],met,jets[0],jets[1])

	_Muujjavg = 0.5*(_Muujj1+_Muujj2)

	[_Muujj1_rel, _Muujj2_rel,_MHuujj_rel] = GetLLJJMassesRelative(muons[0],muons[1],jets[0],jets[1])
	_Muujjavg_rel = 0.5*(_Muujj1_rel+_Muujj2_rel)



	if _ptmu1>42 and  _ptmu2>42 and _ptmet>35 and _ptj1>110 and _ptj2>40 and _stuujj>250 and _stuvjj>250:
		#print ' Here we go:'
		if len(jets)>= 4: GetLLJJMasses4Jets(muons[0],muons[1],jets[0],jets[1],jets[2],jets[3])
		if len(jets)>= 3: GetLLJJMasses3Jets(muons[0],muons[1],jets[0],jets[1],jets[2])
		GetLLJJMasses(muons[0],muons[1],jets[0],jets[1])

	_genjetcount = 0
	if T.isData==0:
		_genjetcount = len(T.GenJetPtAK4)

	# This MUST have the same structure as _kinematic variables!
	toreturn  = [_ptmu1,_ptmu2,_ptel1,_ptel2,_ptj1,_ptj2,_ptmet]
	toreturn += [_ptmu1_default,_ptmu2_default]
	toreturn += [_ptmu1mu2]
	toreturn += [_etamu1,_etamu2,_etael1,_etael2,_etaj1,_etaj2,_etamet]
	toreturn += [_phimu1,_phimu2,_phiel1,_phiel2,_phij1,_phij2,_phimet]
	toreturn += [_xmiss,_ymiss]
	toreturn += [_isomu1,_isomu2]
	
	toreturn += [_chimu1,_chimu2]
	toreturn += [_ispfmu1,ispfmu2]
	toreturn += [_layersmu1,_layersmu2]

	toreturn += [_qmu1,_qmu2]
	toreturn += [_dptmu1,_dptmu2]
	toreturn += [_nhefj1,_nhefj2,_nemefj1,_nemefj2]
	toreturn += [_stuujj,_stuvjj]
	toreturn += [_Muu,_MTuv]
	toreturn += [_Mjj]
	toreturn += [_DRuu,_DPHIuv,_DPHIj1v,_DPHIj2v]
	toreturn += [_DRu1j1,_DRu1j2,_DRu2j1,_DRu2j2]
	toreturn += [_DRj1j2,_DPhij1j2]
	toreturn += [_DPhiu1j1,_DPhiu1j2,_DPhiu2j1,_DPhiu2j2]
	toreturn += [_Muujj1_gen, _Muujj2_gen,_Muujjavg_gen]
	toreturn += [_Muujj1_genMatched, _Muujj2_genMatched,_Muujjavg_genMatched]
	toreturn += [_Muujj1, _Muujj2,_Muujjavg]
	toreturn += [_Muujj1_rel, _Muujj2_rel,_Muujjavg_rel]
	toreturn += [_Muujj]
	toreturn += [_Muuj1,_Muuj2,_Mu1j1j2,_Mu2j1j2]
	toreturn += [_MTuvjj1, _MTuvjj2,_Muvjj, _MTuvjj]
	toreturn += [_MHuujj,_MHuvjj]
	toreturn += [_jetcount,_mucount,_elcount,_genjetcount]
	toreturn += [_ismuon_muon1,_ismuon_muon2]
	toreturn += [_passTrigMu1,_passTrigMu2]
	toreturn += [_muonInd1,_muonInd2]
	toreturn += [_jetInd1,_jetInd2]
	toreturn += [_ptHat]
	toreturn += [_CSVj1,_CSVj2]
	toreturn += [_CMVAj1,_CMVAj2]
	toreturn += [_PULoosej1,_PUMediumj1,_PUTightj1]
	toreturn += [_PULoosej2,_PUMediumj2,_PUTightj2]
	toreturn += [_passWptCut,_passZptCut,_WorZSystemPt]
	toreturn += [_WSystemPt,_ZSystemPt]
	toreturn += [_matchedLQ,_matchedLQ_LVJJ]
	return toreturn

#fixme Had to move these below FullKinematicCalculation, wouldn't find function otherwise. Why only these?
def checkWorZpt(T,lowcut, highcut, WorZ):
	#print 'New event'
	maxPt,maxPtV=0.,0.
	hardProcessLeptonPts = []
	for n in range(len(T.GenParticlePdgId)):
		pdg = T.GenParticlePdgId[n]
		status = T.GenParticleStatus[n]
		pt = T.GenParticlePt[n]
		hard = T.GenParticleIsHardProcess[n]
		lor = TLorentzVector()
		lor.SetPtEtaPhiE(pt,T.GenParticleEta[n],T.GenParticlePhi[n],T.GenParticleEnergy[n])
		parts = []
		#if WorZ=='W' : parts = [-24,24]
		#if WorZ=='Z' : parts = [-22,-23,22,23]
		#if pdg in parts:#[-24,24]:#23=Z, 24=W, 22=gamma
		#	#print n,pdg,pt,status
		#	if pt>maxPtV: maxPtV=pt
		##	#print n,pdg,pt,status
		##	if pt<100: return 1
		##	else: return 0
		if hard and abs(pdg)>=11 and abs(pdg)<=18:
			hardProcessLeptonPts.append(lor)
		else: continue
	if len(hardProcessLeptonPts)==2:
		maxPt = (hardProcessLeptonPts[0]+hardProcessLeptonPts[1]).Pt()
	#print maxPtV,
	#print maxPt,"\n"
	if maxPt<highcut:
		#print 'less than 100!'
		return [1,maxPt]
	else: 
		#print 'more than 100!'
		return [0,maxPt]
	return [1,maxPt]

def GeomFilterCollection(collection_to_clean,good_collection,dRcut):
	# Purpose: Take a collection of TLorentzVectors that you want to clean (arg 1)
	#         by removing all objects within dR of dRcut (arg 3) of any element in
	#         the collection of other particles (arg 2)
	#         e.g.  arguments (jets,muons,0.3) gets rid of jets within 0.3 of muons. 
	output_collection = []
	for c in collection_to_clean:
		isgood = True
		for g in good_collection:
			if (c.DeltaR(g))<dRcut:
				isgood = False
		if isgood==True:
			output_collection.append(c)
	return output_collection

def MetVector(T):
	# Purpose: Creates a TLorentzVector representing the MET. No pseudorapidity, obviously.
	met = TLorentzVector()
	#met.SetPtEtaPhiM(T.PFMETType1XYCor[0],0,T.PFMETPhiType1XYCor[0],0)#fixme moving away from xy cor
	met.SetPtEtaPhiM(T.PFMETType1Cor[0],0,T.PFMETPhiType1Cor[0],0)
	return met



def GetLLJJMasses3Jets(l1,l2,j1,j2,j3):

	m11 = (l1+j1).M()
	m12 = (l1+j2).M()
	m13 = (l1+j3).M()
	m21 = (l2+j1).M()
	m22 = (l2+j2).M()
	m23 = (l2+j3).M()

	diff1 = abs(m11-m22)
	diff2 = abs(m11-m23)
	diff3 = abs(m12-m21)
	diff4 = abs(m12-m23)
	diff5 = abs(m13-m21)
	diff6 = abs(m13-m22)

	least = min(diff1,diff2,diff3,diff4,diff5,diff6)
	
	if least == diff1 :
		pair = [m11,m22] # The invariant mass pair
		mh = m11 # invariant mass corresponding to leading jet
	elif least == diff2:
		pair = [m11,m23] # The invariant mass pair
		mh = m11 # invariant mass corresponding to leading jet
	elif least == diff3:
		pair = [m12,m21] # The invariant mass pair
		mh = m21 # invariant mass corresponding to leading jet
	elif least == diff4:
		pair = [m12,m23] # The invariant mass pair
		mh = m12 # invariant mass corresponding to leading jet
	elif least == diff5:
		pair = [m13,m21] # The invariant mass pair
		mh = m21 # invariant mass corresponding to leading jet
	elif least == diff6:
		pair = [m13,m22] # The invariant mass pair
		mh = m22 # invariant mass corresponding to leading jet
        else:
		pair = [0,0]
		mh=0
	#print '3Jet min:',least,'masses: ',pair[0],pair[1]
	pair.sort()
	pair.reverse()
	pair.append(mh)
	return pair


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
	if len(scaleWeights) > 7 :
		Branches['scaleWeight_Up'][0]=       scaleWeights[4]
		Branches['scaleWeight_Down'][0]=     scaleWeights[8]
		Branches['scaleWeight_R1_F1'][0]=    scaleWeights[0]
		Branches['scaleWeight_R1_F2'][0]=    scaleWeights[1]
		Branches['scaleWeight_R1_F0p5'][0]=  scaleWeights[2]
		Branches['scaleWeight_R2_F1'][0]=    scaleWeights[3]
		Branches['scaleWeight_R2_F2'][0]=    scaleWeights[4]
		Branches['scaleWeight_R2_F0p5'][0]=  scaleWeights[5]
		Branches['scaleWeight_R0p5_F1'][0]=  scaleWeights[6]
		Branches['scaleWeight_R0p5_F2'][0]=  scaleWeights[7]
		Branches['scaleWeight_R0p5_F0p5'][0]=scaleWeights[8]
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

	if t.isData == True:#fixme check all these.
		Branches['pass_HLTIsoMu27'][0]            = PassTrigger(t,["HLT_IsoMu27_v"],1)      # Data Only
		Branches['pass_HLTMu45_eta2p1'][0]        = PassTrigger(t,["HLT_Mu45_eta2p1_v"],1)  # Data Only - turned affter for inst. lumi >= 8.5e33
		Branches['pass_HLTMu50'][0]               = PassTrigger(t,["HLT_Mu50_v"],1)         # Data Only
		Branches['pass_HLTTkMu50'][0]             = PassTrigger(t,["HLT_TkMu50_v"],1)       # Data Only
		Branches['passTriggerObjectMatching'][0]  = 1*(True in t.MuonHLTSingleMuonMatched)  # Data Only
		Branches['passBadEESuperCrystal'][0]      = 1*(t.passEEBadScFilter) # Used, Data only

	else:
		Branches['pass_HLTIsoMu27'][0]            = PassTrigger(t,["HLT_IsoMu27_v"],1)
		Branches['pass_HLTMu45_eta2p1'][0]        = PassTrigger(t,["HLT_Mu45_eta2p1_v"],1)        
		Branches['pass_HLTMu50'][0]               = PassTrigger(t,["HLT_Mu50_v"],1)
		Branches['pass_HLTTkMu50'][0]             = PassTrigger(t,["HLT_TkMu50_v"],1)
		Branches['passTriggerObjectMatching'][0]  = 1*(True in t.MuonHLTSingleMuonMatched)  
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
		# All calculations are done here
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
	
	if (Branches['Pt_muon1'][0] < 47): continue
	if nonisoswitch != True:
			if (Branches['Pt_muon2'][0] < 47) and (Branches['Pt_miss'][0] < 49): continue
	if (Branches['Pt_jet1'][0] <  45): continue
	#if (Branches['Pt_jet2'][0] <  45): continue #fixme turned off for qcd check.....turn back on!
	if (Branches['St_uujj'][0] < 275) and (Branches['St_uvjj'][0] < 275): continue
	if (Branches['M_uu'][0]    <  45) and (Branches['MT_uv'][0]   <  45): continue
	
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
os.system('rm '+junkfile1)
os.system('rm '+junkfile2)
