import os
import sys

import math
import random
from glob import glob

# Directory where root files are kept and the tree you want to get root files from
EMuDirectory = '~/neuhome/LQAnalyzerOutput/NTupleAnalyzer_Jan28MuonUpdatesEMuSwitch_2013_01_29_13_47_07/SummaryFiles'
QCDDirectory = '~/neuhome/LQAnalyzerOutput/NTupleAnalyzer_Jan17QCDNonIso_2013_01_17_23_28_27/SummaryFiles'
# NormalDirectory = 'NTupleAnalyzer_Jan28MuonUpdates_2013_01_28_17_27_35/SummaryFiles'
# NormalDirectory = 'NTupleAnalyzer_Jan28QuickTest_2013_01_29_19_51_24/SummaryFiles'
NormalDirectory = '~/neuhome/LQAnalyzerOutput/NTupleAnalyzer_Jan31PreApp_2013_01_31_23_47_21/SummaryFiles'
# NormalDirectory = '~/neuhome/LQAnalyzerOutput/NTupleAnalyzer_Jan14Full_2013_01_14_21_23_01/SummaryFiles'
# NormalDirectory = 'NTupleAnalyzer_TESTQuickTest_2013_02_04_21_18_30/SummaryFiles'
TreeName = "PhysicalVariables"


lumi = 19600.0


singlemuHLT =  '*( 0.94*(abs(Eta_muon1)<=0.9) + 0.84*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) + 0.82*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) )'
doublemuHLT =  '*(1.0-(( 1.0 - 0.94*(abs(Eta_muon1)<=0.9) - 0.84*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) - 0.82*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) )'
doublemuHLT += '*( 1.0 - 0.94*(abs(Eta_muon2)<=0.9) - 0.84*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2) - 0.82*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1) )))'
singlemuHLTEMU = '*((IsMuon_muon1*( 0.94*(abs(Eta_muon1)<=0.9) + 0.84*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) + 0.82*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) ))'
singlemuHLTEMU += '+(IsMuon_muon2*( 0.94*(abs(Eta_muon2)<=0.9) + 0.84*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2) + 0.82*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1) )))'

dataHLTEMUADJ = '*1.0/(1.0'+singlemuHLTEMU+')'

NormalWeightMuMu = str(lumi)+'*weight_central'+doublemuHLT
NormalWeightMuNu = str(lumi)+'*weight_central'+singlemuHLT
NormalWeightEMu = str(lumi)+'*weight_central'+singlemuHLTEMU

NormalWeightEMuNoHLT = str(lumi)+'*weight_central'

dataHLT = '*(pass_HLTMu40_eta2p1)'

passfilter =  '*(passDataCert*passPrimaryVertex)'
passfilter += '*(passBeamScraping*passPhysDeclared*passBeamHalo*passHBHENoiseFilter*passTrackingFailure)'
# passfilter += '*(passEcalDeadCellBE*passEcalDeadCellTP*passBadEESuperCrystal*passEcalLaserCorr*passHcalLaserEvent)'
passfilter += '*(passEcalDeadCellBE*passEcalDeadCellTP*passBadEESuperCrystal*passHcalLaserEvent)'
# passEcalLaserCorr is bad in data
preselectionmumu = '((Pt_muon1>45)*(Pt_muon2>45)*(Pt_jet1>125)*(Pt_jet2>45)*(St_uujj>300)*(M_uu>50))'#*(DR_muon1muon2>0.3))*(DR_muon1jet1>0.6)*(DR_muon1jet2>0.6)*(DR_muon2jet1>0.6)*(DR_muon2jet2>0.6)'
preselectionmunu = '((Pt_muon1>45)*(Pt_muon2<45.0)*(Pt_miss>55)*(Pt_jet1>125)*(Pt_jet2>45)*(Pt_ele1<45.0)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5)*(MT_uv>50.0))'
preselectionemu = '((Pt_muon1>45)*(Pt_muon2>45)*(Pt_jet1>125)*(Pt_jet2>45)*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3))'

preselectionemu += passfilter
preselectionmumu+=passfilter
preselectionmunu+=passfilter
emu_id_eff = 0.534
emu_id_eff_err = 0.008


##########################################################################
########      Put all uses of the plotting funcs into main()      ########
##########################################################################



def main():

	############################################################
    ##############     DEFINE BINNING            ###############
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
	drbinning = [35,0,7]
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


	############################################################
    ##############     STANDARD PLOT ROUTINES    ###############
	############################################################

	version_name = 'Testing_Jan31_Freeze' # scriptflag
	os.system('mkdir Results_'+version_name) 



	MuMuOptCutFile = 'Results_'+version_name+'/Opt_uujjCuts_Smoothed_pol2cutoff.txt' # scriptflag
	MuNuOptCutFile = 'Results_'+version_name+'/Opt_uvjjCuts_Smoothed_pol2cutoff.txt' # scriptflag

	if (False):
		scalefacs = []
		minselectionmumu = '((Pt_muon1>45)*(Pt_muon2>45)*(M_uu>50)*(DR_muon1muon2>0.3))'
		minselectionmunu = '((Pt_muon1>45)*(Pt_muon2<45.0)*(Pt_miss>55)*(Pt_ele1<45.0)*(DPhi_muon1met>0.8)*(MT_uv>50.0))'
		minselectionmumu+=passfilter
		minselectionmunu+=passfilter		

		scalefacs.append('Selection & $R_Z$ & $R_{t \\bar{t}} & R_W & $R_{t \\bar{t}} \\\hline')
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+minselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)*(Pt_miss<100)', '(M_uu>100)*(Pt_miss>=100)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+minselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
		Rz_uujj = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
		Rtt_uujj = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
		Rw_uvjj = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
		Rtt_uvjj = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))	
		scalefacs.append('No Jet Req & ' + str(Rz_uujj)+' & '+str(Rtt_uujj)+' & '+str(Rw_uvjj)+' & '+str(Rtt_uvjj)+' \\\\')

		minselectionmumu += '*(Pt_jet1>45.0)'
		minselectionmunu += '*(Pt_jet1>45.0)*(DPhi_jet1met>0.5)'
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+minselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)*(Pt_miss<100)', '(M_uu>100)*(Pt_miss>=100)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+minselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')		
		Rz_uujj = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
		Rtt_uujj = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
		Rw_uvjj = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
		Rtt_uvjj = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))	
		scalefacs.append('$1^{st}$ Jet $>$ 45 GeV & ' + str(Rz_uujj)+' & '+str(Rtt_uujj)+' & '+str(Rw_uvjj)+' & '+str(Rtt_uvjj)+' \\\\')

		minselectionmumu += '*(Pt_jet2>45.0)'
		minselectionmunu += '*(Pt_jet2>45.0)'
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+minselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)*(Pt_miss<100)', '(M_uu>100)*(Pt_miss>=100)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+minselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')		
		Rz_uujj = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
		Rtt_uujj = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
		Rw_uvjj = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
		Rtt_uvjj = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))	
		scalefacs.append('$2^{nd}$ Jet $>$ 45 GeV & ' + str(Rz_uujj)+' & '+str(Rtt_uujj)+' & '+str(Rw_uvjj)+' & '+str(Rtt_uvjj)+' \\\\')

		minselectionmumu += '*(Pt_jet1>125.0)'
		minselectionmunu += '*(Pt_jet1>125.0)'
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+minselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)*(Pt_miss<100)', '(M_uu>100)*(Pt_miss>=100)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+minselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')		
		Rz_uujj = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
		Rtt_uujj = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
		Rw_uvjj = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
		Rtt_uvjj = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))	
		scalefacs.append('$1^{st}$ Jet $>$ 125 GeV & ' + str(Rz_uujj)+' & '+str(Rtt_uujj)+' & '+str(Rw_uvjj)+' & '+str(Rtt_uvjj)+' \\\\')


		minselectionmumu += '*(St_uujj>300.0)'
		minselectionmunu += '*(St_uvjj>300.0)'
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+minselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)*(Pt_miss<100)', '(M_uu>100)*(Pt_miss>=100)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+minselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')		
		Rz_uujj = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
		Rtt_uujj = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
		Rw_uvjj = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
		Rtt_uvjj = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))	
		scalefacs.append('$S_T>300$ GeV & ' + str(Rz_uujj)+' & '+str(Rtt_uujj)+' & '+str(Rw_uvjj)+' & '+str(Rtt_uvjj)+' \\\\')

		f = open('Results_'+version_name+'/ScaleFactorStudy.txt','w')
		for s in scalefacs:
			f.write(s+'\n')
		f.close()


	if (False):
		# TTBar STudy
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetEMuScaleFactors( NormalWeightEMu+'*'+preselectionemu, EMuDirectory, '(1)', '(1)')
		Rw_uvjj = 1.0
		# # PreSelection Plotsf
		MakeBasicPlotEMu("Pt_miss","E_{T}^{miss} [GeV]",metbinning2,preselectionemu,NormalWeightEMu,EMuDirectory,'emusel','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlotEMu("St_uujj","S_{T}^{e #mu j j} [GeV]",stbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emusel','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlotEMu("M_uu","M^{e #mu} [GeV]",bosonbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emusel','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlotEMu("M_uujj2","M^{e/#mu j}_{2} [GeV]",lqbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emusel','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlotEMu("DR_muon1muon2","#DeltaR(#mu,e})",drbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emusel','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)



	if (False):
		# SysVaried plots


		# for sample in ['ScaleUp','ScaleDown','MatchUp','MatchDown']:
		# 	preselectionmunu_mod = preselectionmunu
		# 	NormalWeightMuNu_mod = NormalWeightMuNu
		# 	Rz_uujj = 1.0
		# 	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactorsMod( NormalWeightMuNu_mod+'*'+preselectionmunu_mod, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)',sample)
		# 	MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# 	MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sysmethod in ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','PUup','PUdown']:
			preselectionmunu_mod = ModSelection(preselectionmunu,sysmethod,MuNuOptCutFile)
			NormalWeightMuNu_mod = ModSelection(NormalWeightMuNu,sysmethod,MuNuOptCutFile)

			Rz_uujj = 1.0
			[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu_mod+'*'+preselectionmunu_mod, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
			MakeBasicPlot(ModSelection("M_uvjj",sysmethod,MuNuOptCutFile),"M^{#mu j} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sysmethod,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot(ModSelection("MT_uv",sysmethod,MuNuOptCutFile),"M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sysmethod,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)


	if (False):
		qcdselectionmumu = '((Pt_muon1>45)*(Pt_muon2>45)*(Pt_jet1>125)*(Pt_jet2>45)*(St_uujj>300)*(DR_muon1muon2>0.3))'
		qcdselectionmunu = '((Pt_muon1>45)*(Pt_muon2<45.0)*(Pt_jet1>125)*(Pt_jet2>45)*(Pt_ele1<45.0)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5))'

		QCDStudy(qcdselectionmumu,qcdselectionmunu,MuMuOptCutFile,MuNuOptCutFile,NormalWeightMuMu,NormalWeightMuNu,version_name)


	if (False):


		for x in [['(1)','study_basic'],['(Chi2_muon1<10)*(Chi2_muon2<10)','study_chi2'],['(TrkMeasLayers_muon1>8)*(TrkMeasLayers_muon2>8)','study_layers8'],['(PFID_muon1>0)*(PFID_muon2>0)','study_pfid']]:
			additionsel = '*'+x[0]
			tag = x[1]
			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)*(Pt_miss>=100)')
			[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
			MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu+additionsel,NormalWeightMuMu,NormalDirectory,tag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)

	if (False):


		# [[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]]  = [[0.922,0.0],[0.919,0.0]]
		# [[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]]  = [[1.0,0.0],[1.0,0.0]]
		# FractionFitterSF("abs(Phi_muon1-Phi_muon2)","#Delta #phi(#mu #mu) [GeV]",[35,0,7],preselectionmumu+'*(M_uu>80)*(M_uu<120)',NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# sys.exit()
		# # Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')


		# # # Control Region Plots
		# MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonzoombinning_uujj_Z,preselectionmumu,NormalWeightMuMu,NormalDirectory,'controlzoom_ZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# # MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metzoombinning_uujj_Z,preselectionmumu+'*(M_uu>80)*(M_uu<100)*(Pt_miss<100)',NormalWeightMuMu,NormalDirectory,'controlzoomZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# # MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonzoombinning_uujj_TT,preselectionmumu+'*(M_uu>100)*(Pt_miss>=100)',NormalWeightMuMu,NormalDirectory,'controlzoom_TTRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# # MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metzoombinning_uujj_TT,preselectionmumu+'*(M_uu>100)*(Pt_miss>=100)',NormalWeightMuMu,NormalDirectory,'controlzoomTTRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)

		# # MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# # MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonslopebinning_uvjj, preselectionmunu,NormalWeightMuNu,NormalDirectory,'controlzoom_SlopeRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",massslopebining_uvjj,preselectionmunu,NormalWeightMuNu,NormalDirectory,'controlzoom_SlopeRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)



		############# AN PLOTS ################
		# # PreSelection Plots

		# MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		# MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		# MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("MH_uujj","M^{#mu j} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uujj1","M^{#mu j}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uujj2","M^{#mu j}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon2jet1","#DeltaR(#mu_{2},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon2jet2","#DeltaR(#mu_{2},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet1met","#Delta #phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet2met","#Delta #phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu_{1},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu_{1},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon2jet1","#Delta #phi(#mu_{2},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon2jet2","#Delta #phi(#mu_{2},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)


		# MakeBasicPlot("MH_uujj","M^{#mu j} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uujj1","M^{#mu j}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uujj2","M^{#mu j}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon2jet1","#DeltaR(#mu_{2},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon2jet2","#DeltaR(#mu_{2},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet1met","#Delta #phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet2met","#Delta #phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu_{1},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu_{1},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon2jet1","#Delta #phi(#mu_{2},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon2jet2","#Delta #phi(#mu_{2},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("abs(Phi_muon1-Phi_muon2)","#Delta #phi(#mu #mu) [GeV]",[35,0,7],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# sys.exit()


		# MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Phi_miss","#phi^{miss} [GeV]",phibinning,preselectionmunu+'',NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("St_uvjj","S_{T}^{#mu #nu j j} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("MT_uvjj","M_{T}^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("MH_uvjj","M^{#mu j} (lead jet only) [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet1met","#Delta #phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet2met","#Delta #phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu,j_{1})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu,j_{2})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)



		# PreSelection Plots w/o Z Mass
		preselectionmumu_zveto = preselectionmumu+'*(M_uu > 120.0)'

		# MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metbinning2,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		# MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		# MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("MH_uujj","M^{#mu j} (lead jet combo) [GeV]",lqbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uujj1","M^{#mu j}_{1} [GeV]",lqbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uujj2","M^{#mu j}_{2} [GeV]",lqbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon2jet1","#DeltaR(#mu_{2},j_{1})",drbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon2jet2","#DeltaR(#mu_{2},j_{2})",drbinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet1met","#Delta #phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet2met","#Delta #phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu_{1},j_{1})",dphibinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu_{1},j_{2})",dphibinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon2jet1","#Delta #phi(#mu_{2},j_{1})",dphibinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon2jet2","#Delta #phi(#mu_{2},j_{2})",dphibinning,preselectionmumu_zveto,NormalWeightMuMu,NormalDirectory,'zveto_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)


		# # Full Selection Plots
		# for lqmass in [300,400,450,500,600,700,900]:
		# 	MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
		#  	MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)

		# 	MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
		# 	MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
		# 	MakeBasicPlot("M_uujj2","M^{#mu j}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
		# 	MakeBasicPlot("St_uvjj","S_{T}^{#mu #nu j j} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
		# 	MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
		# 	MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)



		# ############# PAS PLOTS ################

		# # # PreSelection Plots
		# MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		# MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		# MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("MH_uujj","M^{#mu j} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uujj1","M^{#mu j}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uujj2","M^{#mu j}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon2jet1","#DeltaR(#mu_{2},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DR_muon2jet2","#DeltaR(#mu_{2},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet1met","#Delta #phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet2met","#Delta #phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu_{1},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu_{1},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon2jet1","#Delta #phi(#mu_{2},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon2jet2","#Delta #phi(#mu_{2},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)



		# MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("Phi_miss","#phi^{miss} [GeV]",phibinning,preselectionmunu+'',NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("St_uvjj","S_{T}^{#mu #nu j j} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("MT_uvjj","M_{T}^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("MH_uvjj","M^{#mu j} (lead jet only) [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet1met","#Delta #phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DPhi_jet2met","#Delta #phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu,j_{1})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		# MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu,j_{2})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)


		# Full Selection Plots
		# for lqmass in [300,400,450,500,600,700,900]:
		# 	MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
		#  	MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)

		# 	MakeBasicPlot("St_uujj","S_{T}^{#mu #mu j j} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
		# 	MakeBasicPlot("M_uu","M^{#mu #mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
		# 	MakeBasicPlot("M_uujj2","M^{#mu j}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalPAS','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
		# 	MakeBasicPlot("St_uvjj","S_{T}^{#mu #nu j j} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
		# 	MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
		# 	MakeBasicPlot("M_uvjj","M^{#mu j} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)

		# os.system('echo Combining Figures; convert -density 800 Results_'+version_name+'/*png Results_'+version_name+'/AllPlots.pdf')


		QuickTableTTDD(MuMuOptCutFile, preselectionmumu,NormalWeightMuMu,Rz_uujj, Rw_uvjj,Rtt_uujj)
		# QuickTable(MuNuOptCutFile, preselectionmunu,NormalWeightMuNu,Rz_uujj, Rw_uvjj,Rtt_uvjj)



	if (False):
		dptsel = '*(abs(TrkGlbDpt_muon1) > 0.0000001)'

		biasselectionmumu = '((Pt_muon1>45)*(Pt_muon2>45)*(Pt_jet1>110)*(Pt_jet2>45)*(St_uujj>250)*(M_uu>50)*(DR_muon1muon2>0.3))'
		biasselectionmunu = '((Pt_muon1>45)*(Pt_muon2<45.0)*(Pt_miss>55)*(Pt_jet1>110)*(Pt_jet2>45)*(Pt_ele1<45.0)*(St_uvjj>250)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5)*(MT_uv>50.0))'
		biasselectionmumu+=passfilter
		biasselectionmunu+=passfilter

		BiasStudy ("TrkGlbDpt_muon1","#Delta p_{T}^{-1} (Track - Global) [GeV]",biasselectionmumu,biasselectionmunu,dptsel,NormalWeightMuMu,NormalWeightMuNu,[0.92,0.95,0.98],version_name)
		# MakeBasicPlot("TrkGlbDpt_muon1","#Delta p_{T}^{-1} (Track - Global) [GeV]",[100,-.002,.002],preselectionmumu+dptsel,NormalWeightMuMu,NormalDirectory,'bias','uujj',0.92, 0.95,0.98,'',version_name,500)
		# MakeBasicPlot("TrkGlbDpt_muon1","#Delta p_{T}^{-1} (Track - Global) [GeV]",[100,-.002,.002],preselectionmunu+dptsel,NormalWeightMuNu,NormalDirectory,'bias','uvjj',0.92, 0.95,0.98,'',version_name,500)



	if (True):
		FullAnalysis(MuMuOptCutFile, preselectionmumu,preselectionmunu,NormalDirectory,NormalWeightMuMu,'TTBarDataDriven')  # scriptflag
		FullAnalysis(MuNuOptCutFile, preselectionmumu,preselectionmunu,NormalDirectory,NormalWeightMuNu,'normal')  # scriptflag

		uujjcardfiles = MuMuOptCutFile.replace('.txt','_systable*.txt')
		uvjjcardfiles = MuNuOptCutFile.replace('.txt','_systable*.txt')

		uujjcards = ParseFinalCards(uujjcardfiles)
		uvjjcards = ParseFinalCards(uvjjcardfiles)
		finalcards = FixFinalCards([uujjcards,uvjjcards])

		print 'Final Cards Available in ',finalcards


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
	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+NormalDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print('t_'+f.replace(".root\n","")+" = TFile.Open(\""+NormalDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")

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

def BiasStudy(bvar,xname,sel_uu,sel_uv,sel_dpt,weight_uu,weight_uv,scalefacs,vname):

	allmctrees = [t_WJetsJBin,t_DiBoson,t_TTBarDBin,t_ZJetsJBin,t_SingleTop]
	fitfunc = '[0]*sin([1]+(x))'

	# MakeBasicPlot(bvar,xname,[60,-.003,.003],sel_uu+sel_dpt,weight_uu,NormalDirectory,'bias','uujj',scalefacs[0],scalefacs[1],scalefacs[2],'',vname,500)
	# MakeBasicPlot(bvar,xname,[60,-.003,.003],sel_uv+sel_dpt,weight_uv,NormalDirectory,'bias','uvjj',scalefacs[0],scalefacs[1],scalefacs[2],'',vname,500)
	# ProfileHisto('Phi_muon1',bvar,'Muon #phi [test]' ,xname,[-0.0002,0.0002],sel_uu+sel_dpt+'*(Charge_muon1>0)*(Pt_muon1>200.0)',[16,-3.15,3.15],allmctrees,'uujj','MCbias_test',vname,fitfunc,'Pt_muon1')

	# sys.exit()
	# charges = ['pos','neg']
	charges = ['all']
	# chargecuts = ['(Charge_muon1>0)','(Charge_muon1<0)']
	chargecuts = ['(1)']
	# etacuts = ['(abs(Eta_muon1) < 0.9)','(abs(Eta_muon1) > 0.9)*(abs(Eta_muon1) < 1.2)','(abs(Eta_muon1) > 1.2)*(abs(Eta_muon1) < 2.1)']
	# etaregions = ['barrel','overlap','endcap']
	etacuts = ['(abs(Eta_muon1) < 0.9)']
	etaregions = ['barrel']

	# thresholds = [200,250,300,350,400,450,500,550,600]
	thresholds = [200]
	scalefuncts = []

	AmpX = []
	AmpXErr = []

	AmpY = []
	AmpYErr = []


	for chan in ['uujj']:
		if chan == 'uujj':
			texchan = '#mu#mujj'
			sel = sel_uu
		if chan == 'uvjj':
			texchan = '#mu#nujj'
			sel = sel_uv

		for c in range(len(chargecuts)):
			chargecut = chargecuts[c]
			charge = charges[c]

			for e in range(len(etacuts)):
				etacut = etacuts[e]
				etaregion = etaregions[e]

				for ptthresh in thresholds:
					ptcut = '(Pt_muon1 >'+str(ptthresh)+')*(Pt_muon1 <'+str(ptthresh+10000)+')'
					allcuts = '*'+ptcut + '*'+etacut + '*'+chargecut
					print 'Doing ',chan, charge, etaregion,ptthresh
					print sel+sel_dpt+allcuts
					
					[funct,scalefunct,par1] = ProfileHisto('Phi_muon1',bvar+'*(Charge_muon1)','Muon #phi ['+chan+' channel, '+charge+' charge, '+etaregion+' region, p_{T} > '+str(ptthresh)+'. GeV]' ,xname,[-0.0002,0.0002],sel+sel_dpt+allcuts,[16,-3.15,3.15],allmctrees,chan,'MCbias_'+charge+'_thresh'+str(ptthresh)+'_'+etaregion,vname,fitfunc,'Pt_muon1')
					scalefuncts.append('if '+allcuts+' : '+scalefunct)
					AmpX.append(ptthresh+5000.0)
					AmpXErr.append(5000.0)
					AmpY.append(abs(par1[0]))
					AmpYErr.append(abs(par1[1]))
	# for th in thresholds:
	# 	for e in etaregions:
	# 		os.system('montage Results_'+vname+'/Basic*bias*'+str(th)+'*'+e+'*png -geometry +2+2 Results_'+vname+'/BiasStudy_thresh'+str(th)+'_'+e+'.png')
	# # ProfileHisto('Phi_muon1',bvar,'Muon #phi',xname,[-0.0002,0.0002],sel_uv+sel_dpt+'*(Pt_muon1>200.0)*(Charge_muon1<0.5)',[16,-3.15,3.15],allmctrees,'uvjj','MCbias',vname,fitfunc,'Pt_muon1')

	# for scale in scalefuncts:
	# 	print scale

	# print AmpX
	# print AmpXErr
	# print AmpY
	# print AmpYErr

	# nn = len(AmpX)
	# print nn
	# X = array("d", AmpX)
	# Xplus = array("d", AmpXErr)
	# Xminus = array("d", AmpXErr)
	# Y = array("d", AmpY)
	# Yplus = array("d", AmpYErr)
	# Yminus = array("d", AmpYErr)	
	# hprof = TGraphAsymmErrors(nn,X,Y,Xminus,Xplus,Yminus,Yplus)

	# style=[0,20,.7,1,1]	
	# axis = hprof.GetXaxis();
	# axis.SetLimits(150,700)	
	# hprof.GetXaxis().SetTitle("Muon p_{T}")
	# hprof.GetYaxis().SetTitle("Fit Amplitude")
	# # hprof.SetMinimum()
	# # hprof.SetMaximum(yrange[1])	
	# hprof.SetFillStyle(style[0])
	# hprof.SetMarkerStyle(style[1])
	# hprof.SetMarkerSize(style[2])
	# hprof.SetLineWidth(style[3])
	# hprof.SetMarkerColor(style[4])
	# hprof.SetLineColor(style[4])
	# hprof.SetFillColor(style[4])
	# hprof.SetFillColor(style[4])
	# hprof.GetXaxis().SetTitleFont(132)
	# hprof.GetYaxis().SetTitleFont(132)
	# hprof.GetXaxis().SetLabelFont(132)
	# hprof.GetYaxis().SetLabelFont(132)
	# hprof.GetXaxis().SetTitleSize(.04);
	# hprof.GetYaxis().SetTitleSize(.04);


	# c1 = TCanvas( 'c1', 'c1', 200, 10, 700, 500 )
	# c1.SetFillColor( 0 )
	# hprof.Draw("AP")
	# fitfunc2 = '[0] + [1]*(x) + [2]*(x)*(x)'
	# ft = TF1("ft",fitfunc2,200,650)
	# hprof.Fit('ft')
	# npar = fitfunc2.count('[')
	# outfunc2 = fitfunc2
	# np = 0
	# while np < npar:
	# 	print  str(np),ft.GetParameter(np)
	# 	outfunc2 = outfunc2.replace('['+str(np)+']','('+str(round(ft.GetParameter(np),11))+')' )
	# 	np += 1
	# outfunc2 = outfunc2.replace('(x)','p_{T}')
	# outfunc2 = '('+outfunc2+')'

	# print "Amplitude Fit:",outfunc2
	# l1=TLatex()
	# l1.SetTextAlign(12)
	# l1.SetTextFont(132)
	# l1.SetNDC()
	# l1.SetTextSize(0.03)
 
	# l1.DrawLatex(0.2,0.2,"A(p_{T}) = "+outfunc2)
	# c1.Print("Results_"+vname+'/BiasStudy_YSineAmplitudeFit.png')
	# c1.Print("Results_"+vname+'/BiasStudy_YSineAmplitudeFit.pdf')

	# os.system('convert -density 800 Results_'+vname+'/Bias*png Results_'+vname+'/BiasStudyResults.pdf')


	return 0

def ProfileHisto(variablex,variabley,xname,yname,yrange,selection,binning,treeset,channel,tagname,vname,fitfunc,variabledep):

	xvals = []
	yvals = []

	binset = ConvertBinning(binning)
	rr = str(random.randint(0,10000000))
	_htmp = TFile.Open("biastmp"+rr+".root","RECREATE")

	nevent = 0

	effectivevariabley = variabley.replace('Charge','_thistreeskim.Charge')
	print variablex,variabley
	for _thistree in treeset:
		_thistreeskim = _thistree.CopyTree(selection)
		for evnumber in range(_thistreeskim.GetEntries()):
			_thistreeskim.GetEntry(evnumber)
			exec('xvals.append(_thistreeskim.'+variablex+')')
			exec('yvals.append(_thistreeskim.'+effectivevariabley+')')

			nevent += 1

	[Xmeans,Xerrs,Ymeans,Yerrs] = GetProfile(yvals,xvals,binning)


	X = array("d", Xmeans)
	Xplus = array("d", Xerrs)
	Xminus = array("d", Xerrs)

	Y = array("d", Ymeans)
	Yplus = array("d", Yerrs)
	Yminus = array("d", Yerrs)	
	nn = len(binset)-1
	hprof = TGraphAsymmErrors(nn,X,Y,Xminus,Xplus,Yminus,Yplus)

	style=[0,20,.7,1,1]	

	axis = hprof.GetXaxis();
	axis.SetLimits(binset[0],binset[-1])	
	hprof.GetXaxis().SetTitle(xname)
	hprof.GetYaxis().SetTitle(yname)
	hprof.SetMinimum(yrange[0])
	hprof.SetMaximum(yrange[1])	
	hprof.SetFillStyle(style[0])
	hprof.SetMarkerStyle(style[1])
	hprof.SetMarkerSize(style[2])
	hprof.SetLineWidth(style[3])
	hprof.SetMarkerColor(style[4])
	hprof.SetLineColor(style[4])
	hprof.SetFillColor(style[4])
	hprof.SetFillColor(style[4])
	hprof.GetXaxis().SetTitleFont(132)
	hprof.GetYaxis().SetTitleFont(132)
	hprof.GetXaxis().SetLabelFont(132)
	hprof.GetYaxis().SetLabelFont(132)
	hprof.GetXaxis().SetTitleSize(.04);
	hprof.GetYaxis().SetTitleSize(.04);


	outscale = ''
	outfunc = ''
	c1 = TCanvas( 'c1', 'c1', 200, 10, 700, 500 )
	c1.SetFillColor( 0 )
	hprof.Draw("AP")
	par1 = [0,0]
	if fitfunc != '':
		ft = TF1("ft",fitfunc,binset[0],binset[-1])
		hprof.Fit('ft')
		npar = fitfunc.count('[')
		outfunc = fitfunc
		for n in range(npar):
			outfunc = outfunc.replace('['+str(n)+']','('+str(round(ft.GetParameter(n),7))+')' )
		outfunc = outfunc.replace('(x)',variablex)
		outfunc = '('+outfunc+')'
		# print outfunc
		outscale = ' ((1.0)/( '+outfunc + ' + (1.0/'+variabledep+') )) '
		# print outscale
		par1 = [ft.GetParameter(0),ft.GetParError(0)]

		l1=TLatex()
		l1.SetTextAlign(12)
		l1.SetTextFont(132)
		l1.SetNDC()
		l1.SetTextSize(0.03)
	 
		l1.DrawLatex(0.2,0.2,"F(#phi) = "+outfunc)
		l1.DrawLatex(0.2,0.16,"Based on "+str(nevent)+" MC events.")
	variablex = variablex.replace('*','X')
	c1.Print("Results_"+vname+'/BiasStudy_PhiDep.png')
	c1.Print("Results_"+vname+'/BiasStudy_PhiDep.pdf')

	# c1.Print("Results_"+vname+'/Basic_'+channel+'_'+variablex+'_profile_'+variabley+'_'+tagname+'.png')
	# c1.Print("Results_"+vname+'/Basic_'+channel+'_'+variablex+'_profile_'+variabley+'_'+tagname+'.pdf')

	return [outfunc,outscale,par1]

def FixDrawLegend(legend):
	legend.SetTextFont(132)
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
	hout.GetXaxis().SetTitleFont(132)
	hout.GetYaxis().SetTitleFont(132)
	hout.GetXaxis().SetLabelFont(132)
	hout.GetYaxis().SetLabelFont(132)
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
	histo.GetXaxis().SetTitleFont(132)
	histo.GetYaxis().SetTitleFont(132)
	histo.GetXaxis().SetLabelFont(132)
	histo.GetYaxis().SetLabelFont(132)
	return histo

def BeautifyStack(stack,label):
	stack.GetHistogram().GetXaxis().SetTitleFont(132)
	stack.GetHistogram().GetYaxis().SetTitleFont(132)
	stack.GetHistogram().GetXaxis().SetLabelFont(132)
	stack.GetHistogram().GetYaxis().SetLabelFont(132)
	stack.GetHistogram().GetXaxis().SetTitle(label[0])
	stack.GetHistogram().GetYaxis().SetTitle(label[1])

	return stack

def QuickIntegral(tree,selection,scalefac):

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
	_s = QuickIntegral(_stree,selection,scalefacs[0])
	_bs = [QuickIntegral(_btrees[b],selection,scalefacs[1][b]) for b in range(len(_btrees))]
	_bt = QuickMultiIntegral(_btrees,selection,scalefacs[1])
	_d = QuickEntries (_dtree,selection+dataHLT,scalefacs[2])

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

	print selection
	print texline 

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


def QuickTable(optimlog, selection, weight,rz,rw,rt):
	selection = selection+'*'+weight
	texfile = optimlog.replace('.txt','_table.tex')
	csvfile = optimlog.replace('.txt','_table.csv')

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
		fsel = '*'+fsel.replace(" ","")
		this_sel = '('+selection+fsel+')'

		exec('treefeed = ['+chan+']')
		treefeed.append([t_TTBarDBin,t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		treefeed.append(t_SingleMuData)
		scalefacs = [1,[rt,rz,rw,1,1],1]
		QuickTableLine(treefeed,this_sel,scalefacs,texfile,csvfile)

		nline += 1


def QuickTableTTDD(optimlog, selection, weight,rz,rw,rt):
	# selection = selection+'*'+weight
	texfile = optimlog.replace('.txt','_table.tex')
	csvfile = optimlog.replace('.txt','_table.csv')

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

	# Alignment Unc, [uujj sig, uujj bg, uvjj sig, [uvjj bg] ]
	alignmentuncs = [0.1,1.0,1.0,[0.027,0.072,0.205,0.672,1.268,2.592,3.632,4.518,6.698,6.355,5.131,9.615,12.364,16.176,16.176,16.176,16.176,16.176,16.176,16.176]]

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
			rt = 1.077*rt
		if 'uvjj' in optimlog: 
			rt = 1.199*rt

	if sysmethod == 'SHAPEZ'  : rz = 1.033*rz
	if sysmethod == 'SHAPEW'  : rw = 1.091*rw


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

		exec('treefeed = ['+chan+']')
		treefeed.append(t_SingleMuData)
		treefeed.append([t_TTBarDBin,t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		scalefacs = [1,[rt,rz,rw,1,1],1]
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

	# Alignment Unc, [uujj sig, uujj bg, uvjj sig, [uvjj bg] ]
	alignmentuncs = [0.1,1.0,1.0,[0.027,0.072,0.205,0.672,1.268,2.592,3.632,4.518,6.698,6.355,5.131,9.615,12.364,16.176,16.176,16.176,16.176,16.176,16.176,16.176]]

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

	if sysmethod == 'SHAPEZ'  : rz = 1.033*rz
	if sysmethod == 'SHAPEW'  : rw = 1.091*rw


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


		exec('treefeed = ['+chan+']')
		treefeed.append(te_SingleMuData)
		treefeed.append([te_ZJetsJBin,te_WJetsJBin,te_SingleTop,te_DiBoson])
		treefeed.append([t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		treefeed.append(t_SingleMuData)

		scalefacs = [1,rt,[-1.0*rz,-1.0*rw,-1.0,-1.0],[rz,rw,1,1],1]
		selections = [ this_sel_unmod +dataHLT+dataHLTEMUADJ, this_sel_unmod+'*'+NormalWeightEMuNoHLT, this_sel+weightmod ]		

		QuickSysTableLineTTDD(treefeed,selections,scalefacs,sysfile,chan,rglobals,rglobalb)
		# break

def FullAnalysis(optimlog,selection_uujj,selection_uvjj,NormalDirectory,weight,usedd):
	TTDD = False
	if usedd=='TTBarDataDriven':
		TTDD=True
	_Variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','WNORMup','WNORMdown','TTNORMup','TTNORMdown','SHAPETT','SHAPEZ','SHAPEW','MUONIDISO','MUONHLT','ALIGN']	
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
	if n > 1:
		mean = mean / float(n) 
	else:
		mean = 0
	for a in x: 
		std = std + (a - mean)**2 
	if n>1:	
		std = math.sqrt(std / float(n-1)) 
	else:
		std = 999999
	return [mean, std]

def GetProfile(X,Y,binning):
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
	N1 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

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

	for x in range(1000):
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



def GetEMuScaleFactors( selection, FileDirectory, controlregion_1, controlregion_2):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_SingleMuData,selection + '*' + controlregion_1,1.0)
	# print QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	# sys.exit()
	print selection + '*' + controlregion_1
	N1 = QuickEntries(te_SingleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(te_SingleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

	Z1 = QuickIntegral(te_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(te_TTBarDBin,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(te_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(te_WJetsJBin,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(te_DiBoson,selection + '*' + controlregion_1,1.0)

	Z2 = QuickIntegral(te_ZJetsJBin,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(te_TTBarDBin,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(te_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(te_WJetsJBin,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(te_DiBoson,selection + '*' + controlregion_2,1.0)

	print ' Data:',N1[0]
	print '   TT:',T1[0]
	print '    Z:',Z1[0]
	print ' Stop:',s1 [0]
	print '    W:',w1[0]
	print '   VV:',v1[0]

	Other1 = [ s1[0]+w1[0]+v1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+w2[0]+v2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] ) ]
	zvals = []
	tvals = []

	for x in range(1000):
		variation = (GetSimpleScaleFactors(RR(N1),RR(N2),RR(Z1),RR(Z2),RR(T1),RR(T2),Other1[0],Other2[0]))
		zvals.append(variation[0])
		tvals.append(variation[1])

	zout =  GetStats(zvals)
	tout = GetStats(tvals)

	print 'MuMu: RZ  = ', zout[-1]
	print 'MuMu: Rtt = ', tout[-1]
	return [ [ zout[0], zout[1] ] , [ tout[0],tout[1] ] ]

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



	for x in range(1000):
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

	N1 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

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

	for x in range(1000):
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




def FractionFitterSF(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,cutlog,version_name,plotmass):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "

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

	##############################################################################
	#######      Top Left Plot - Normal Stacked Distributions              #######
	##############################################################################
	# print 'Projecting trees...  ',

	print 'Doing Projections'
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',t_WJetsJBin,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',t_SingleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',t_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',t_ZJetsJBin,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',t_TTBarDBin,recovariable,presentationbinning,selection+'*'+weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',t_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)


	hs_rec_DiBoson.Add(hs_rec_WJets)
	hs_rec_DiBoson.Add(hs_rec_SingleTop)

	def chi2test(ht,hz,ho,hd,rent,renz):
		chi2 = 0
		for x in range(hd.GetNbinsX()):
			ibin = x+1
			nt = ht.GetBinContent(ibin)*rent
			nz = hz.GetBinContent(ibin)*renz
			no = ho.GetBinContent(ibin)
			nd = hd.GetBinContent(ibin)
			chi2 += (nd - nt -nz -no)**2
		return chi2

	bestrs = [0.5,0.5]
	bestchi2 = 999999999
	rz = 0.5
	for a in range((1000)):
		print a
		rt = 0.5
		rz += 0.001
		for b in range((1000)):
			rt += 0.001
			chi2 = chi2test(hs_rec_TTBar,hs_rec_ZJets,hs_rec_DiBoson,hs_rec_Data,rz,rt)
			if chi2 < bestchi2:
				bestchi2 = chi2
				bestrs = [rz,rt]

	print bestrs



	# mc = TObjArray(3)
	# mc.Add(hs_rec_ZJets)
	# mc.Add(hs_rec_TTBar)
	# mc.Add(hs_rec_DiBoson)

	# fit = TFractionFitter(hs_rec_Data, mc)
	# # fit.Constrain(1,0.5,2.0);   
	# # fit.Constrain(2,0.5,2.0);   
	# # fit.Constrain(3,0.999999,1.00001);   
	# status = fit.Fit()



def MakeBasicPlot(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,cutlog,version_name,plotmass):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	# Create Canvas

	if 'PAS' not in tagname:
		c1 = TCanvas("c1","",800,800)
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.47, 1.0, 1.0 )#divide canvas into pads
		pad2 = TPad( 'pad2', 'pad2', 0.0, 0.25, 1.0, 0.44 )
		pad3 = TPad( 'pad3', 'pad3', 0.0, 0.03, 1.0, 0.22 )
		pad1.Draw()
		pad2.Draw()
		pad3.Draw()
	else:
		c1 = TCanvas("c1","",800,550)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
	gStyle.SetOptStat(0)


	pad1.cd()
	pad1.SetGrid()
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

	if 'ScaleUp' in tagname:
		t_W = t_WJetsScaleUp
		t_T = t_TTJetsScaleDown

	elif 'ScaleDown' in tagname:
		t_W = t_WJetsScaleDown
		t_T = t_TTJetsScaleDown

	elif 'MatchUp' in tagname:
		t_W = t_WJetsMatchUp
		t_T = t_TTJetsMatchDown

	elif 'MatchDown' in tagname:
		t_W = t_WJetsMatchDown
		t_T = t_TTJetsMatchDown	

	else:
		t_W = t_WJetsJBin
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
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',t_ZJetsJBin,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
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

	print "THIS NUMBER -->",hs_rec_TTBar.Integral(), hs_rec_TTBar.GetEntries()

	# hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched [Pythia]',t_QCDMu,recovariable,presentationbinning,selection+'*'+weight,QCDStackStyle,Label)

	# for nn in range(hs_rec_WJets.GetNbinsX()+1):
	# 	print hs_rec_Data.GetBinConent(nn), hs_rec_ZJets.GetBinContent(nn), hs_rec_TTBar.GetBinContent(nn)

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

	MCStack=BeautifyStack(MCStack,Label)
	hs_rec_Signal.Draw("HISTSAME")
	if 'final' not in tagname:
		hs_rec_Signal2.Draw("HISTSAME")

	hs_rec_Data.Draw("EPSAME")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	leg = TLegend(0.63,0.62,0.89,0.88,"","brNDC");
	leg.SetTextFont(132);
	leg.SetFillColor(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(.04)
	leg.AddEntry(hs_rec_Data,"Data");
	if channel=='uujj':
		leg.AddEntry(hs_rec_ZJets,'Z/#gamma^{*} + jets')
	if channel=='uvjj':
		leg.AddEntry(hs_rec_WJets,'W + jets')
	leg.AddEntry(hs_rec_TTBar,'t #bar{t} + jets' + (' (e #mu est)')*('TTBarDataDriven' in tagname))

	leg.AddEntry(hs_rec_DiBoson,'Other Backgrounds')
	if 'final' not in tagname:
		leg.AddEntry(hs_rec_Signal,sig1name)
		leg.AddEntry(hs_rec_Signal2,sig2name)
	else:
		leg.AddEntry(hs_rec_Signal,'LQ, M = '+str(plotmass)+' GeV')
	leg.Draw()

	sqrts = "#sqrt{s} = 8 TeV";
	l1=TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(132)
	l1.SetNDC()
	l1.SetTextSize(0.06)
 
	l1.DrawLatex(0.37,0.94,"CMS 2012  "+sqrts+", 19.6 fb^{-1}")
	# l1.DrawLatex(0.13,0.76,sqrts)

	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(132)
	l2.SetNDC()
	l2.SetTextSize(0.06)
	# l2.SetTextAngle(45);	
	l2.DrawLatex(0.15,0.83,"PRELIMINARY")

	gPad.RedrawAxis()

	MCStack.SetMinimum(.03333)
	MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())

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

		RatHistNum.SetMaximum(1.5)
		RatHistNum.SetMinimum(0.5)


		RatHistNum.GetYaxis().SetTitleFont(132);
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


		chiplot.GetYaxis().SetTitleFont(132);
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



def MakeBasicPlotQCD(recovariable,xlabel,presentationbinning,selection,qcdselection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,version_name,qcdrescale):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	# Create Canvas
	c1 = TCanvas("c1","",800,800)
	gStyle.SetOptStat(0)

	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.47, 1.0, 1.0 )#divide canvas into pads
	pad2 = TPad( 'pad2', 'pad2', 0.0, 0.25, 1.0, 0.44 )
	pad3 = TPad( 'pad3', 'pad3', 0.0, 0.03, 1.0, 0.22 )
	if tagname == 'uujj':
		pad1.SetLogx()
		pad2.SetLogx()
		pad3.SetLogx()

	pad1.Draw()
	pad2.Draw()
	pad3.Draw()

	pad1.cd()
	pad1.SetGrid()
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
	leg.SetTextFont(132);
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
	l1.SetTextFont(132)
	l1.SetNDC()
	l1.SetTextSize(0.06)
 
	l1.DrawLatex(0.37,0.94,"CMS 2012  "+sqrts+", 19.6 fb^{-1}")
	# l1.DrawLatex(0.13,0.76,sqrts)

	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(132)
	l2.SetNDC()
	l2.SetTextSize(0.06)
	# l2.SetTextAngle(45);	
	l2.DrawLatex(0.15,0.83,"PRELIMINARY")

	gPad.RedrawAxis()

	MCStack.SetMinimum(.03333)
	MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())

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


	RatHistNum.GetYaxis().SetTitleFont(132);
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


	chiplot.GetYaxis().SetTitleFont(132);
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

	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.47, 1.0, 1.0 )#divide canvas into pads
	pad2 = TPad( 'pad2', 'pad2', 0.0, 0.25, 1.0, 0.44 )
	pad3 = TPad( 'pad3', 'pad3', 0.0, 0.03, 1.0, 0.22 )
	pad1.Draw()
	pad2.Draw()
	pad3.Draw()

	pad1.cd()
	pad1.SetGrid()
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
	leg.SetTextFont(132);
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
	l1.SetTextFont(132)
	l1.SetNDC()
	l1.SetTextSize(0.06)
 
	l1.DrawLatex(0.37,0.94,"CMS 2012  "+sqrts+", 19.6 fb^{-1}")
	# l1.DrawLatex(0.13,0.76,sqrts)

	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(132)
	l2.SetNDC()
	l2.SetTextSize(0.06)
	# l2.SetTextAngle(45);	
	l2.DrawLatex(0.15,0.83,"PRELIMINARY")

	gPad.RedrawAxis()

	MCStack.SetMinimum(.03333)
	MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())

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


	RatHistNum.GetYaxis().SetTitleFont(132);
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


	chiplot.GetYaxis().SetTitleFont(132);
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


def MakeBasicPlotOld(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmp.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  ",
	# Create Canvas
	c1 = TCanvas("c1","",1200,800)
	gStyle.SetOptStat(0)

	# These are the style parameters for certain plots - [FillStyle,MarkerStyle,MarkerSize,LineWidth,Color]
	MCRecoStyle=[0,20,.00001,1,4]
	DataRecoStyle=[0,20,.7,1,1]
	# X and Y axis labels for plot
	Label=[xlabel,"Events/Bin"]

	WStackStyle=[3007,20,.00001,2,6]
	TTStackStyle=[3005,20,.00001,2,4]
	ZStackStyle=[3004,20,.00001,2,2]
	DiBosonStackStyle=[3006,20,.00001,2,30]
	StopStackStyle=[3008,20,.00001,2,40]
	QCDStackStyle=[3013,20,.00001,2,15]

	SignalStyle=[0,22,0.7,3,8]


	
	##############################################################################
	#######      Top Left Plot - Normal Stacked Distributions              #######
	##############################################################################
	c1.cd(1)
	print 'Projecting trees...  ',
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',t_WJetsJBin,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data, 5/fb',t_SingleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',t_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',t_ZJetsJBin,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',t_TTBarDBin,recovariable,presentationbinning,selection+'*('+str(ttscale)+')*'+weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',t_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)

	# hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched [Pythia]',t_QCDMu,recovariable,presentationbinning,selection+'*'+weight,QCDStackStyle,Label)

	if channel == 'lljj':
		hs_rec_Signal=CreateHisto('hs_rec_Signal','LQ, M = 500 GeV',t_LQuujj500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
		hs_rec_DiBoson.SetTitle("Other Backgrounds")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets]

	if channel == 'lvjj':
		hs_rec_Signal=CreateHisto('hs_rec_Signal','LQ, M = 500 GeV',t_LQuvjj500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
		hs_rec_DiBoson.SetTitle("Other Backgrounds")
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)		
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_WJets]
		

	# mcdatascalepres = (1.0*(hs_rec_Data.GetEntries()))/(sum(k.Integral() for k in SM))

	MCStack = THStack ("MCStack","")
	SMIntegral = sum(k.Integral() for k in SM)
	# MCStack.SetMaximum(SMIntegral*100)
	
	print 'Stacking...  ',	
	for x in SM:
		# x.Scale(mcdatascalepres)
		MCStack.Add(x)
		x.SetMaximum(10*hs_rec_Data.GetMaximum())

	MCStack.Draw("HIST")
	c1.cd(1).SetLogy()

	MCStack=BeautifyStack(MCStack,Label)
	hs_rec_Signal.Draw("HISTSAME")

	hs_rec_Data.Draw("EPSAME")

	print 'Legend...  ',
	# Create Legend
	FixDrawLegend(c1.cd(1).BuildLegend())
	gPad.RedrawAxis()

	MCStack.SetMinimum(.03333)
	MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())

	print 'Saving...  ',
	c1.Print('Results_'+version_name+'/Basic_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
	c1.Print('Results_'+version_name+'/Basic_'+channel+'_'+recovariable+'_'+tagname+'.png')
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
		hout.GetXaxis().SetTitleFont(132)
		hout.GetYaxis().SetTitleFont(132)
		hout.GetXaxis().SetLabelFont(132)
		hout.GetYaxis().SetLabelFont(132)
		hout.GetYaxis().SetTitleFont(132);
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

def QuickBDT(identifier,signal_tree, z_tree, w_tree, vv_tree, st_tree, t_ttree, variables,preselection,channel,weight,zscale,ttscale,wscale):

	fout = TFile('Results_'+version_name+'/Output_'+channel+'_BDT.root',"RECREATE")
	factory = TMVA.Factory("TMVAClassification", fout,":".join([ "!V","!Silent","Color", "DrawProgressBar","Transformations=I;D;P;G,D", "AnalysisType=Classification"]))

	trainweight = ('3.0*'+weight)

	for v in variables:
		factory.AddVariable(v,"F")

	factory.AddSignalTree(signal_tree,1.0)
	factory.AddBackgroundTree(z_tree,zscale)
	factory.AddBackgroundTree(t_ttree,ttscale)
	factory.AddBackgroundTree(w_tree,wscale)
	factory.AddBackgroundTree(vv_tree,1.0)
	factory.AddBackgroundTree(st_tree,1.0)

	# cuts defining the signal and background sample
	sigCut =TCut(preselection+'*(Rand1<0.333333)')
	bgCut = TCut(preselection+'*(Rand1<0.333333)')

	factory.SetBackgroundWeightExpression(trainweight);
	factory.SetSignalWeightExpression(trainweight);

	factory.PrepareTrainingAndTestTree(sigCut,  bgCut,   ":".join([ "nTrain_Signal=0", "nTrain_Background=0", "SplitMode=Random", "NormMode=NumEvents","!V"]))
	method = factory.BookMethod(TMVA.Types.kBDT, "BDT",":".join(["!H", "!V", "NTrees=850", "nEventsMin=150","MaxDepth=3", "BoostType=AdaBoost", "AdaBoostBeta=0.5","SeparationType=GiniIndex","nCuts=20","PruneMethod=NoPruning",]))

	factory.TrainAllMethods()
	factory.TestAllMethods()
	factory.EvaluateAllMethods()

	os.system('mv weights Results_'+version_name+'/weights_'+identifier)

def UpdateFilesWithMVA(FileDirectory,variables):

	alltrees = []
	treenames = []
	for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
		exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")	
		exec('alltrees.append(t_'+f.replace(".root\n","")+')')
		treenames.append('t_'+f.replace(".root\n",""))

	allfiles = os.listdir("Results_"+version_name)
	mvas = []
	for a in allfiles:
		if 'weights' in a:
			mvas.append("Results_"+version_name+'/'+a.replace('\n',''))
	print mvas

	for M in mvas:
		reader=TMVA.Reader()
		for v in variables:
			print('v_'+v+' = array(\'f\',[0])')
			print('reader.AddVariable("'+v+'",v_'+v+')')
			exec('v_'+v+' = array(\'f\',[0])')
			exec('reader.AddVariable("'+v+'",v_'+v+')')
		reader.BookMVA("BDT",M+"/TMVAClassification_BDT.weights.xml")


		for t in range(len(alltrees)):
			tname = treenames[t]
			t = alltrees[t]

			N = t.GetEntries()

			for n in range(N):
				t.GetEntry(n)
				for v in variables:
					exec('v_'+v+'[0] = t.'+v)
				print tname,reader.EvaluateMVA("BDT")

def CreateMuMuBDTs(variables,preselection,weight,FileDirectory,zscale,ttscale,wscale):
	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
		exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")	

	QuickBDT('LQToCMu_M_600',t_LQToCMu_M_600,t_ZJets_Sherpa, t_WJets_Sherpa, t_DiBoson, t_SingleTop, t_TTBar,  variables,preselection,'lljj',weight,zscale,ttscale,wscale)

	QuickBDT('LQToCMu_M_500',t_LQToCMu_M_500,t_ZJets_Sherpa, t_WJets_Sherpa, t_DiBoson, t_SingleTop, t_TTBar,  variables,preselection,'lljj',weight,zscale,ttscale,wscale)


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

def MuonTPStudy():

	__m = TFile.Open('root://eoscms//eos/cms/store/group/phys_exotica/darinb/TP2012/tagprobe_mc.root')
	__d = TFile.Open('root://eoscms//eos/cms/store/group/phys_exotica/darinb/TP2012/tagprobe_data.root')

	print 'Fetching MC tree...'
	_m = __m.Get("tpTree/fitter_tree")
	print 'Fetching Data tree...'
	_d = __d.Get("tpTree/fitter_tree")

	n_d = _d.GetEntries()
	n_m = _m.GetEntries()
	print ' '
	print 'Data Events:',n_d
	print 'MC Events:', n_m
	print ' '

	# f = TFile.Open('/tmp/'+person+'/tagprobetmp.root','RECREATE')
	# print 'Skimming MC (this may take a few minutes).'
	# dtag = _d.CopyTree('(pt>45.0)*(abseta<2.1)*(pair_nJets30>2)')
	# print 'Skimming Data (this may take a few minutes).'
	# mtag = _m.CopyTree('(pt>45.0)*(abseta<2.1)*(pair_nJets30>2)')



	np_d = 0
	np_m = 0
	np_hlt_d = 0
	np_id_d = 0
	np_id_m = 0
	np_id_hlt_d = 0
	np_hlt_id_d = 0

	binLowE = [45,50,60,80,100,150,200,600]

	hprof1  = TProfile( 'TagProbe1', '', 7, array('d',binLowE),0,1 )
	hprof1.GetXaxis().SetTitle("Muon p_{T} (GeV)")
	hprof1.GetYaxis().SetTitle("Mu40_eta2p1 [Data]")
	hprof1.SetMinimum(0.6)
	hprof1.SetMaximum(1.2)

	hprof2  = TProfile( 'TagProbe2', 'MC', 7, array('d',binLowE),0,1 )
	hprof2.GetXaxis().SetTitle("Muon p_{T} (GeV)")
	hprof2.GetYaxis().SetTitle("Tight2012")
	hprof2.SetMinimum(0.6)
	hprof2.SetMaximum(1.2)

	hprof3  = TProfile( 'TagProbe3', 'Data', 7, array('d',binLowE),0,1 )
	hprof3.GetXaxis().SetTitle("Muon p_{T} (GeV)")
	hprof3.GetYaxis().SetTitle("Tight2012")
	hprof3.SetMinimum(0.6)
	hprof3.SetMaximum(1.2)	


	for n in range(n_d):
		if n%150000==0: 
			print round(((1.0*n)/(1.0*n_d)*100.0),1) ,'%'
		_d.GetEntry(n)
		if _d.pt<45.0:
			continue
		if _d.pair_nJets30<2:
			continue
		if _d.abseta>2.1:
			continue
		if (_d.tag_pt>45)*(_d.tag_eta>-2.1)*(_d.tag_eta<2.1)*(_d.tag_combRelIso<0.1) < 1:
			continue
		np_d += 1

		di = (_d.Tight2012)*(_d.tkIso/_d.pt < 0.1)
		dh = _d.Mu40_eta2p1

		np_id_d += di
		np_hlt_d += dh

		if dh>0:
			hprof3.Fill( _d.pt, di)
			np_hlt_id_d += 1

		if di>0:
			np_id_hlt_d += dh
			hprof1.Fill( _d.pt, dh)



	for n in range(n_m):
		if n%150000==0: 
			print round(((1.0*n)/(1.0*n_m)*100.0),1) ,'%'
		_m.GetEntry(n)
		if _m.pt<45.0:
			continue
		if _m.pair_nJets30<2:
			continue
		if _m.abseta>2.1:
			continue
		if (_m.tag_pt>45)*(_m.tag_eta>-2.1)*(_m.tag_eta<2.1)*(_m.tag_combRelIso<0.1) < 1:
			continue			
		np_m += 1
		mt = _m.Tight2012
		np_id_m += mt		
	 	hprof2.Fill( _m.pt, mt)

	c1 = TCanvas( 'c1', 'c1', 200, 10, 700, 500 )
	c1.SetFillColor( 0 )
	c1.SetLogx()

	hprof1.Draw()
	c1.Print("TagProbe_Trigger_Data.png")

	c2 = TCanvas( 'c2', 'c2', 200, 10, 700, 500 )
	c2.SetFillColor( 0 )
	c2.SetLogx()


	hprof3.SetMarkerColor(2)
	hprof3.SetLineColor(2)

	hprof2.Draw()
	hprof3.Draw("SAME")

	c2.Print("TagProbe_ID.png")

	print ' '
	print 'Data Probe Events:', np_d
	print 'MC   Probe Events:', np_m
	print 'Data Probe HLT Events:', np_hlt_d
	print 'Data Probe ID  Events:', np_id_d
	print 'Data ID  Probe HLT Events:', np_id_hlt_d
	print 'Data HLT Probe ID  Events:', np_hlt_id_d
	print 'MC   Probe ID  Events:', np_id_m
	print ' '


	return [0,0]

main()
