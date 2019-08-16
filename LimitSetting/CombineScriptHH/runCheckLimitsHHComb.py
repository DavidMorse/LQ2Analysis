import os
import sys, getopt
import ROOT
from ROOT import *
import random
import time
import datetime
import array
import math

import subprocess
import random


def main():
	### --------------------------- ###
	## python runCheckLimitsComb.py
	## python runCheckLimitsComb.py -m 1000 -ch CombMuEle (--modifycard) (--combinecards) (--text2workspace) (--limits) (--FitDiagnos) (--runGOF) (--runGOFToysJobs) (--runGOFpval) (--launch) (-v 1)
	
	### --------------------------- ###
	
	ROOT.gROOT.SetBatch(1) # no window pop up when drawing
	#ROOT.gStyle.SetOptStat(0)
	mycwd = os.getcwd()
	#os.system('mkdir ' + mtmpdir)
	
	domass = ''
	doch = ''
	verbose = ''
	
	for x in range(len(sys.argv)):
		if sys.argv[x] == '-ch':
			doch = sys.argv[x+1]
		if sys.argv[x] == '-m':
			domass = sys.argv[x+1]
		if sys.argv[x] == '-v':
			verbose = sys.argv[x+1]

	#txtDir = "Results_Testing_diHiggs_newNtuples_MuCutsMC0p49_"
	
	#_resHypos = ['HHres', 'HHBulkGrav']
	if '--Spin2' in sys.argv:
		resType = "HHBulkGrav"
		x_spin = '2'
		_2l2nudir = 'Graviton'
	else:
		resType = "HHres"
		x_spin = '0'
		_2l2nudir = 'Radion'

	## options to freeze rateParam
	#frz = ' --freezeParameters R_2l2q,R_2l2nu'
	frz = ' --freezeParameters R_2l2q'

	## options passed to combines tool
	mn = ' --cminDefaultMinimizerType Minuit'
	
	_mass            = ["260","270","300","350","400", "450", "451", "500",  "550",  "600",  "650", "750", "800", "900", "1000"]


	# BDTG 22 vars
	## SPIN 0
	if (resType == "HHres") :
		#_mass       = ["260", "270",  "300", "350", "400", "450", "451", "500", "550", "600", "650", "750", "800", "900", "1000"]
		comb_rangesM = [-500,   -500,   -300,  -200,  -400,  -200,   -40,   -20,   -30,   -20,   -10,  -80,   -20,   -50,    -40]
		comb_rangesP = [ 500,    500,    300,   200,   400,   200,    40,    20,    30,    20,    18,   80,    20,    50,     40]
		comb_opts    = [  '',     '',     mn,    mn,    '',    '',    mn,    mn,    mn,    mn,    mn,    mn,    mn,    '',     mn]

		# range ee
		ee_rangesM   = []
		ee_rangesP   = []
		ee_opts      = []

		# range uu
		uu_rangesM   = []
		uu_rangesP   = []
		uu_opts      = []

		rb = ' --robustFit 1'
		#_mass          = ["260", "270", "300", "350", "400", "450", "451", "500", "550", "600", "650", "750", "800", "900", "1000"]
		comb_optsImp    = [ '',    '',   '',    mn,    '',    '',     mn,     mn,    mn,    mn,   mn,     mn,      mn,    mn,     '']
		comb_optsRobust = [ rb,    rb,   '',    '',    rb,    rb,     rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     '']
		comb_optsImp2   = [ '',    '',   mn,    mn,    '',    '',     mn,     mn,    mn,    mn,   mn,     mn,      mn,    mn,     '']
		comb_optsRobust2= [ '',    '',   '',    '',    '',    '',     '',     '',    '',    '',   '',     '',      '',    '',     '']
		
		ee_optsImp      = []
		ee_optsRobust   = []
		ee_optsImp2     = []
		ee_optsRobust2  = []
		
		uu_optsImp      = []
		uu_optsRobust   = []
		uu_optsImp2     = []
		uu_optsRobust2  = []


	elif (resType == "HHBulkGrav") :
	# SPIN 2
		#            = ["260", "270",  "300", "350", "400", "450", "451", "500", "550", "600", "650", "750", "800", "900", "1000"]
		comb_rangesM = [-500,   -500,   -300,   -50,  -400,  -200,  -400,  -100,  -300,  -20,   -40,   -20,   -30,   -50,    -40]
		comb_rangesP = [ 500,    500,    300,    50,   400,   200,   400,   100,   300,   5,     40,    20,    30,    50,     40]
		comb_opts    = [   '',    '',    '',     mn,    mn,    '',    mn,    mn,    mn,   mn,    mn,    mn,    mn,    mn,     mn]

		# range ee
		ee_rangesM   = []
		ee_rangesP   = []
		ee_opts      = []

		# range uu
		uu_rangesM   = []
		uu_rangesP   = []
		uu_opts      = []

		rb = ' --robustFit 1'
		#_mass          = ["260", "270", "300", "350", "400", "450", "451", "500", "550", "600", "650", "750", "800", "900", "1000"]
		comb_optsImp    = [   '',    '',    '',    mn,   mn,    '',     '',     mn,    mn,    mn,    mn,    mn,    mn,    mn,     mn]
		comb_optsRobust = [   rb,    rb,    rb,    rb,   rb,    rb,     rb,     rb,    rb,    rb,    rb,    rb,    rb,    rb,     rb]
		comb_optsImp2   = [   '',    '',    '',    mn,   mn,    '',     '',     mn,    mn,    mn,    mn,    mn,    mn,    mn,     mn]
		comb_optsRobust2= [   '',    '',    '',    '',   '',    '',     '',     '',    '',    '',    '',    '',    '',    '',     '']
		
		ee_optsImp      = []
		ee_optsRobust   = []
		ee_optsImp2     = []
		ee_optsRobust2  = []
		
		uu_optsImp      = []
		uu_optsRobust   = []
		uu_optsImp2     = []
		uu_optsRobust2  = []


	## obs gof, got from running --runGOF
	comb_gofs   = []
	ee_gofs     = []
	uu_gofs     = []

	_analysisChan = ['CombMuEle','uujj','eejj']
	_leptonChan   = ['CombMuEle','uu','ee']
	_leps         = ['CombMuEle','muon','electron']
	kmax_inis     = [42,0,0]

	#np_ignore = ['HF','EC2','QCDscale_']
	#np_ignore = ['HF','EC2']
	np_ignore = []

	#gofalgos  = ['saturated', 'AD', 'KS']
	gofalgos  = ['saturated']
	#gofalgos  = ['AD','KS']
	
	BetaOneObs = []
	BetaOne95down = []
	BetaOne95up = []
	BetaOne68down = []
	BetaOne68up = []
	BetaOneExp = []

	for ich in range(len(_leptonChan)):
		if _leptonChan[ich] == 'CombMuEle':
			rangesM = comb_rangesM
			rangesP = comb_rangesP
			opts = comb_opts
			gofs = comb_gofs
			optsImp = comb_optsImp
			optsRobust = comb_optsRobust
			optsImp2 = comb_optsImp2
			optsRobust2 = comb_optsRobust2

		
		elif _leptonChan[ich] == 'ee':
			rangesM = ee_rangesM
			rangesP = ee_rangesP
			opts = ee_opts
			gofs = ee_gofs
			optsImp = ee_optsImp
			optsRobust = ee_optsRobust
			optsImp2 = ee_optsImp2
			optsRobust2 = ee_optsRobust2

		elif _leptonChan[ich] == 'uu':
			rangesM = uu_rangesM
			rangesP = uu_rangesP
			opts = uu_opts
			gofs = uu_gofs
			optsImp = uu_optsImp
			optsRobust = uu_optsRobust
			optsImp2 = uu_optsImp2
			optsRobust2 = uu_optsRobust2

		if doch != '':
			if _leptonChan[ich] != doch: continue
		for im in range(len(_mass)):
			if domass != '':
				if _mass[im] != domass: continue
			
			### ---------- the procerdures start here ---------------
			### ---- set up things that are used for all procerdures
			if _mass[im] == "451":
				cardname = 'spin'+ x_spin +'/GGToX' + x_spin + 'ToHHTo2b2l2j_LimitShapeHH' + _leptonChan[ich] + '_' + resType + "450"
			else:
				cardname = 'spin'+ x_spin +'/GGToX' + x_spin + 'ToHHTo2b2l2j_LimitShapeHH' + _leptonChan[ich] + '_' + resType + _mass[im]
			if _leptonChan[ich] in ['uu','ee']:
				cardname = 'CLSLimits/LimitShapeHH' + _leptonChan[ich] + '/' + cardname
			cardnametxt = cardname + '.txt'

			card2l2nu = _2l2nudir + '/combinedCards_' + _mass[im] + '/comb_tot_nominalCombination_M' + _mass[im] + '_mc'
			card2l2nutxt = card2l2nu + '.txt'

			outcombcard    = 'GGToX' + x_spin + 'ToHHTo2b2Z_' + _mass[im]
			outcombcardtxt = outcombcard + '.txt'
			wsfilename     = outcombcard + '.root'

			#if verbose == '1' : print cardnametxt, wsfilename
			### ----------


			##----- fixing some NP of 2l2q cards :
			if '--modifycard' in sys.argv:
				if _mass[im] == "451": continue
				for np in np_ignore:
					sedcomnpdel = 'sed -i \'/' + np + '/d\' ' + cardnametxt
					if verbose == '1' : print sedcomnpdel
					if '--launch' in sys.argv:
						os.system(sedcomnpdel)
				# 2l2q card
				sedcomkmax = 'sed -i \'s#kmax ' + str(kmax_inis[ich]) + '#kmax ' +str(43) + '#g\' ' + cardnametxt
				sedcom1  = 'sed -i \'s#QCDscale_'+resType+'#QCDscale_ggHH#g\' ' + cardnametxt
				sedcom2  = 'sed -i \'s#QCDscale_sTop#QCDscale_SingleTop#g\' ' + cardnametxt
				sedcom3  = 'sed -i \'s#CMS_eff_e#CMS_eff_e_ID#g\' ' + cardnametxt
				sedcom4  = 'sed -i \'s#CMS_eff_trigger_ee#CMS_eff_e_trigger#g\' ' + cardnametxt
				sedcom5  = 'sed -i \'s#CMS_eff_trigger_uu#CMS_eff_m_trigger#g\' ' + cardnametxt
				sedcom6  = 'sed -i \'s#PU#CMS_pu#g\' ' + cardnametxt
				sedcom7  = 'sed -i \'s#uuHIP#CMS_eff_m_tracker#g\' ' + cardnametxt

				sedcom21 = 'sed -i \'s#QCDscale_SMH#QCDscale_VH#g\' ' + cardnametxt
				sedcom22 = 'sed -i \'s#CMS_btag_comb#CMS_btag_light#g\' ' + cardnametxt
				sedcom23 = 'sed -i \'s#CMS_eff_m #CMS_eff_m_ID #g\' ' + cardnametxt
				sedcom24 = 'sed -i \'s#JESFlavorQCD#CMS_scale_j#g\' ' + cardnametxt

				addl1 = 'pdf_qqbar  shape    -   1.0 1.0 1.0 1.0 1.0 1.0 1.0 - 1.0 1.0 1.0 1.0 1.0 1.0 1.0'
				addl2 = 'pdf_gg     shape    1.0 -  -  - - - - - 1.0 - - - - - - -'
				#addl3 = 'R_2l2q  rateParam * '+ resType +' 0.141204218\\n'
				addl3 = 'R_2l2q  rateParam * '+ resType +' 4.3075917\\n'
				sedcom8  = 'sed -i \'/pdf/i ' + addl2 + '\' ' + cardnametxt
				sedcom9  = 'sed -i \'/pdf_gg/i ' + addl1 + '\' ' + cardnametxt
				sedcom10 = 'sed -i \'/pdf /d\' ' + cardnametxt
				sedcom11 = 'sed -i \'/HHresuujj autoMCStats 0 0 1/i \\\\n\\' + addl3 + '\' ' + cardnametxt
				# 2l2nu card
				#addl4 = 'R_2l2nu rateParam * signal_h* 0.032780316\\n'
				#sedcom12 = 'sed -i \'/* autoMCStats 0/i \\\\n\\' + addl4 + '\' ' + card2l2nutxt


				if verbose == '1' :
					print sedcomkmax
				if '--launch' in sys.argv:
					print  " modifycard for ", cardnametxt
					os.system(sedcomkmax)
					os.system(sedcom1)
					os.system(sedcom2)
					os.system(sedcom3)
					os.system(sedcom4)
					os.system(sedcom5)
					os.system(sedcom6)
					os.system(sedcom7)
					
					os.system(sedcom21)
					os.system(sedcom22)
					os.system(sedcom23)
					os.system(sedcom24)
					
					os.system(sedcom8)
					os.system(sedcom9)
					os.system(sedcom10)
					os.system(sedcom11)
					#os.system(sedcom12)

			##----- (0) combine 2l2q, 2l2nu cards
			if '--combinecards' in sys.argv:
				mergecom = 'combineCards.py ' + cardnametxt + ' ' + card2l2nutxt + ' > ' + outcombcardtxt
				if verbose == '1' :
					print mergecom
				if '--launch' in sys.argv:
					os.system(mergecom)

			##----- (1) create wprk space
			## text2workspace.py GGToX0ToHHTo2b2l2j_LimitShapeHHCombMuEle_HHres1000.txt
			if '--text2workspace' in sys.argv:
				txt2wpcom = 'text2workspace.py ' + outcombcardtxt
				if verbose == '1' :
					print txt2wpcom
				if '--launch' in sys.argv:
					os.system(txt2wpcom)

			##----- (2) Limits ---
			if '--limits' in sys.argv:
				if domass == '': flaglog = ''
				else : flaglog = _mass[im]
				
				limitcom = 'combine -M AsymptoticLimits -d ' + wsfilename + frz + ' --setParameterRanges r='+ str(rangesM[im])+','+str(rangesP[im]) + ' | tee -a outlog_limit_M' + flaglog +'.txt'
				if verbose == '1' : print limitcom
				if '--launch' in sys.argv:
					f=open(str('outlog_limit_M' + flaglog +'.txt'), 'a+')
					f.write(limitcom + '\n')
					f.close()
					os.system(limitcom)

			##----- (3) Fit test ---
			if '--FitDiagnos' in sys.argv:
				
				if '--bo_asimov' in sys.argv:
					n_opt = 'BgOnlyAsimovM' + _mass[im] + 's' + x_spin + _leptonChan[ich]
					asimov_opt = ' -t -1 --expectSignal 0'
					log_opt = ' | tee -a outlog_fitdiag_' + n_opt +'.txt'
				elif '--bs_asimov' in sys.argv:
					n_opt = 'BgPSigAsimovM' + _mass[im] + 's' + x_spin + _leptonChan[ich]
					asimov_opt = ' -t -1 --expectSignal 1'
					log_opt = ' | tee -a outlog_fitdiag_' + n_opt +'.txt'
				else:
					n_opt = 'dataobsM' + _mass[im] + 's' + x_spin + _leptonChan[ich]
					asimov_opt = ''
					log_opt = ''

				fitcom = 'combine -M FitDiagnostics -d ' + wsfilename + ' -m ' + _mass[im] + ' --setParameterRanges r='+ str(rangesM[im])+','+str(rangesP[im]) + ' -n ' + n_opt + opts[im] + asimov_opt + frz + log_opt
				diagcom = 'python /afs/cern.ch/user/a/ahortian/HiggsCombine_2018_05_29/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics'+n_opt+'.root -g plots_'+n_opt+'.root' + log_opt # '--abs --all'
				if verbose == '1' :
					print fitcom
					#print diagcom
				#if verbose == '1' : print diagcom
				if '--launch' in sys.argv:
					if ('--bo_asimov' in sys.argv) or ('--bs_asimov' in sys.argv):
						flogname = str( log_opt.replace(' | tee -a ',''))
						os.system('rm ' + flogname)
						f=open(flogname, 'a+')
						f.write(fitcom + '\n')
						f.write(diagcom + '\n')
						f.close()
						os.system(fitcom)
						os.system(diagcom)
					else:
						os.system(fitcom)

			##----- (4) GOF ---
			if '--runGOF' in sys.argv:
				for igof in range(len(gofalgos)):
					dataname = '_' + gofalgos[igof] + '_dataobsM' + _mass[im] + 's' + x_spin + _leptonChan[ich]
					toysname = '_' + gofalgos[igof] + '_ToysmcsM' + _mass[im] + 's' + x_spin + _leptonChan[ich]
					if '--data' in sys.argv:
						gofcom_obs = 'combine -M GoodnessOfFit --algorithm ' + gofalgos[igof] + ' -d ' + wsfilename + ' -m ' +_mass[im]+' --setParameterRanges r=' + str(rangesM[im])+','+str(rangesP[im]) + ' -n ' + dataname + opts[im] + frz
						if verbose == '1' :
							print gofcom_obs + '\n' #+ gofcom_toy
						if '--launch' in sys.argv:
							os.system(gofcom_obs)
					if '--toy' in sys.argv:
						gofcom_toy = 'combine -M GoodnessOfFit --algorithm ' + gofalgos[igof] + ' -d ' + wsfilename + ' -m ' +_mass[im]+' --setParameterRanges r=' + str(rangesM[im])+','+str(rangesP[im]) + ' -n ' + toysname + opts[im] + ' -t 120' + frz
						if verbose == '1' :
							print gofcom_toy
						if '--launch' in sys.argv:
							os.system(gofcom_toy)
					if '--pval' in sys.argv:
						colcom = 'combineTool.py -M CollectGoodnessOfFit --input ' + 'higgsCombine'+dataname+'.GoodnessOfFit.mH'+_mass[im]+'.root ' + 'higgsCombine'+toysname+'.GoodnessOfFit.mH'+_mass[im]+'.*.root ' + '-o collectGoodness'+dataname+'.json'
						pltpdf = 'python /afs/cern.ch/user/a/ahortian/HiggsCombine_2018_05_29/CMSSW_8_1_0/src/CombineHarvester/CombineTools/scripts/plotGof.py --statistic '+gofalgos[igof]+' --mass '+_mass[im]+'.0 collectGoodness' +dataname+'.json --title-right="35.9 fb^{-1} (13 TeV)" --output=\"' + dataname + '\"'
						if verbose == '1' :
							print colcom
							print pltpdf
 						if '--launch' in sys.argv:
							os.system(colcom)
							os.system(pltpdf)

			##----- (5) impacts ---
			if ('--runImpactIni' in sys.argv) or ('--runImpactDoFit' in sys.argv) or ('--runImpactPDF' in sys.argv) :
				if '--bo_asimov' in sys.argv:
					n_opt = 'impactsBgOnlyM' + _mass[im] + 's' + x_spin + _leptonChan[ich]
					asimov_opt = ' -t -1 --expectSignal 0'
				elif '--bs_asimov' in sys.argv:
					n_opt = 'impactsBgPSigM' + _mass[im] + 's' + x_spin + _leptonChan[ich]
					asimov_opt = ' -t -1 --expectSignal 1'
				else:
					n_opt = 'impactsDataObsM' + _mass[im] + 's' + x_spin + _leptonChan[ich]
					asimov_opt = ''

			if '--runImpactIni' in sys.argv:
				iniImpcom = 'combineTool.py -M Impacts -d ' + wsfilename + ' -m ' + _mass[im] + ' --doInitialFit --setParameterRanges r='+ str(rangesM[im])+','+str(rangesP[im]) + ' -n ' + n_opt + optsImp[im] + optsRobust[im] + asimov_opt  + frz
				if verbose == '1' : print iniImpcom
				if '--launch' in sys.argv:
					os.system(iniImpcom)
			if '--runImpactDoFit' in sys.argv:
				dofitImpcom = 'combineTool.py -M Impacts -d ' + wsfilename + ' -m ' + _mass[im] + ' --doFits --parallel 20 --setParameterRanges r='+ str(rangesM[im])+','+str(rangesP[im]) + ' -n ' + n_opt + optsImp2[im] + optsRobust2[im] + asimov_opt  + frz
				if verbose == '1' : print dofitImpcom
				if '--launch' in sys.argv:
					os.system(dofitImpcom)
			if '--runImpactPDF' in sys.argv:
				pdfImpcom1 = 'combineTool.py -M Impacts -d ' + wsfilename + ' -m ' + _mass[im] + ' -o ' + n_opt + '.json' + ' -n ' + n_opt  + frz
				pdfImpcom2 = 'plotImpacts.py -i ' + n_opt + '.json' ' -o ' + n_opt
				#combineTool.py -M Impacts -d GGToX0ToHHTo2b2l2j_LimitShapeHHCombMuEle_HHres1000.root -m 125 -o impacts.json
				#plotImpacts.py -i impacts.json -o impacts_1000
				if verbose == '1' :
					print pdfImpcom1
					print pdfImpcom2
				if '--launch' in sys.argv:
					os.system(pdfImpcom1)
					os.system(pdfImpcom2)

			if '--allLimitsPrint' in sys.argv:
				all_lim_com = 'combine -M AsymptoticLimits -d ' + wsfilename + frz + ' --rMin '+str(rangesM[im])+' --rMax '+str(rangesP[im])
				
				print 'Calculating limit for: ' + _mass[im] + ' ' + _leptonChan[ich] + ' ' + resType
				## Estimate the r values with Asymptotic CLs
				EstimationInformation = [' r < 0.000000']
				breaker = False
				print '\n AH: EstimationInformation  is : ', str(EstimationInformation), '\n' # AH:
				while 'r < 0.000000' in str(EstimationInformation):
					rAbsAcc='.00005'
					if _leptonChan[ich] == 'CombMuEle':
						## Run command here
						print (all_lim_com)
						if '--launch' in sys.argv:
							EstimationInformation = os.popen(all_lim_com).readlines()
					breaker=True
					if breaker ==True:
						break

				expectedlines = []
				for line in EstimationInformation:
					print line
					if 'Expected' in line and 'r <' in line:
						expectedlines.append(line.replace('\n',''))
				values = []
				for e in expectedlines:
					print e
					values.append(float(e.split()[-1]))

				## Fill the arrays of Asymptotic Values
				for line in EstimationInformation:
					if 'Observed' in line and '<' in line:
						BetaOneObs.append((line.split('<')[-1]).replace('\n',''))
						print line
					if 'Expected' in line and '<' in line:
						if '2.5%' in line:
							BetaOne95down.append((line.split('<')[-1]).replace('\n',''))
						if '16.0%' in line:
							BetaOne68down.append((line.split('<')[-1]).replace('\n',''))
						if '50.0%' in line:
							BetaOneExp.append((line.split('<')[-1]).replace('\n',''))
						if '84.0%' in line:
							BetaOne68up.append((line.split('<')[-1]).replace('\n',''))
						if '97.5%' in line:
							BetaOne95up.append((line.split('<')[-1]).replace('\n',''))

				vstart = round((min(values)/3),14)
				vstop = round((max(values)*3),14)
				rvalues = []
				interval = abs(vstop-vstart)/100.0

				nindex = 0
				thisr = 0
				while thisr<vstop:
					thisr = vstart*1.05**(float(nindex))
					rvalues.append(thisr)
					# print thisr
					nindex +=1

				strRvalues = []
				for r in rvalues:
					strRvalues.append(str(round(r,14)))
				# print strRvalues


		##----- () all limits print out ---
		if '--allLimitsPrint' in sys.argv:
			print '\n\n\n'
			masses = []
			for x in _mass:
				masses += [float(x)]
			#### ASYMPTOTIC CLS PRINTOUT ###
			#### BETA ONE CHANNEL
			# for 'HHres'
			mTh = [260.0,270.0,300.0,350.0,400.0,450.0,451.0,500.0,550.0,600.0,650.0,750.0,800.0,900.0,1000.0]
			xsTh = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]

			print "*"*40 + '\n BETA ONE ASYMPTOTIC CLS RESULTS\n\n' +"*"*40

			band1sigma = 'y_1sigma = ['
			band1sigma1 = 'y_1sigma_1 = ['
			band1sigma2 = 'y_1sigma_2 = ['
			band2sigma = 'y_2sigma = ['
			band2sigma1 = 'y_2sigma_1 = ['
			band2sigma2 = 'y_2sigma_2 = ['
			excurve = 'xsUp_expected = ['
			obcurve = 'xsUp_observed = ['
			mcurve = 'mData = ['
			scurve = 'x_shademasses = ['

			ob = BetaOneObs
			down2 = BetaOne95down
			up2 = BetaOne95up
			down1 = BetaOne68down
			up1 = BetaOne68up
			med = BetaOneExp

			fac = 1.0
			sigma = []
			for x in range(len(mTh)):
				if (mTh[x]) in masses:
					sigma.append(xsTh[x]*fac)
			for x in range(len(masses)):
				excurve += str(float(med[x])*float(sigma[x])) + ' , '
				obcurve += str(float(ob[x])*float(sigma[x])) + ' , '
				band1sigma += str(float(down1[x])*float(sigma[x])) + ' , '
				band1sigma1 += str(float(down1[x])*float(sigma[x])) + ' , '
				band2sigma += str(float(down2[x])*float(sigma[x])) + ' , '
				band2sigma1 += str(float(down2[x])*float(sigma[x])) + ' , '
				mcurve += str(float(masses[x])) + ' , '
				scurve += str(float(masses[x])) + ' , '

			for x in range(len(masses)):
				band1sigma += str(float(up1[-(x+1)])*float(sigma[-(x+1)])) + ' , '
				band2sigma += str(float(up2[-(x+1)])*float(sigma[-(x+1)])) + ' , '
				band1sigma2 += str(float(up1[x])*float(sigma[x])) + ' , '
				band2sigma2 += str(float(up2[x])*float(sigma[x])) + ' , '
				scurve += str(float(masses[-x-1])) + ' , '
			excurve += '}'
			obcurve += '}'
			mcurve += '}'
			scurve += '}'
			band1sigma += '}'
			band1sigma1 += '}'
			band1sigma2 += '}'
			band2sigma += '}'
			band2sigma1 += '}'
			band2sigma2 += '}'
			excurve = excurve.replace(' , }',' ] ' )
			obcurve = obcurve.replace(' , }',' ] ' )
			mcurve = mcurve.replace(' , }',' ] ' )
			scurve = scurve.replace(' , }',' ] ' )

			band1sigma = band1sigma.replace(' , }',' ] ' )
			band1sigma1 = band1sigma1.replace(' , }',' ] ' )
			band1sigma2 = band1sigma2.replace(' , }',' ] ' )
			band2sigma = band2sigma.replace(' , }',' ] ' )
			band2sigma1 = band2sigma1.replace(' , }',' ] ' )
			band2sigma2 = band2sigma2.replace(' , }',' ] ' )

			print '\n'
			print mcurve
			print scurve
			print excurve
			print obcurve
			print band1sigma
			print band1sigma1
			print band1sigma2
			print band2sigma
			print band2sigma1
			print band2sigma2
			print '\n'


if __name__ == "__main__":
	main()







