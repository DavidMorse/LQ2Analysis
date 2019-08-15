import os
import sys, getopt
import ROOT
from ROOT import *
import random
import time
import datetime
import array
import math

def main():
	### --------------------------- ###
	## python runCheckLimits.py
	## python runCheckLimits.py -m 1000 -ch CombMuEle (--removeNP) (--text2workspace) (--limits) (--FitDiagnos) (--runGOF) (--runGOFToysJobs) (--runGOFpval) (--launch) (-v 1)
	## python runCheckLimits.py -m 1000 -ch CombMuEle --removeNP --launch
	## python runCheckLimits.py -m 1000 -ch CombMuEle --runGOF --launch
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
	else:
		resType = "HHres"
		x_spin = '0'

	## options passed to combines tool
	mn = ' --cminDefaultMinimizerType Minuit'
	
	_mass            = ["260","270","300","350","400", "450", "500",  "550",  "600",  "650", "750", "800", "900", "1000"]


# BDTG 22 vars
## SPIN 0
	if (resType == "HHres") :
		comb_rangesM = [1000 ,1000 ,1000  ,200  ,200   ,200    ,50    ,80     ,80    ,100    ,100    ,200   ,200    ,200]
		comb_rangesP = [1000 ,1000 ,1000  ,200  ,200   ,200    ,50    ,80     ,80    ,100    ,100    ,200   ,200    ,200]
		comb_opts    = ['',    '',   '',   '',   '',    '',     '',     '',     '',    '',     '',      '',    '',     '']

		# range ee
		ee_rangesM   = [2000 ,2000 ,2000 ,1000  ,400   ,200    ,200    ,200    ,400   ,400    ,400    ,400   ,400    ,400]
		ee_rangesP   = [2000 ,2000 ,2000 ,1000  ,400   ,200    ,200    ,200    ,400   ,400    ,400    ,400   ,400    ,400]
		ee_opts      = [ '',   '',   '',   '',   '',    '',    '',      '',     '',    '',     '',      '',    '',     '']

		# range uu
		uu_rangesM   = [2000 ,800 ,2000 ,1000  ,400   ,200    ,200    ,200    ,400   ,400    ,400    ,400   ,400    ,400]
		uu_rangesP   = [2000 ,800 ,2000 ,1000  ,400   ,200    ,200    ,200    ,400   ,400    ,400    ,400   ,400    ,400]
		uu_opts      = [ '',   '',   '',   '',   '',    '',    '',     '',      '',    '',     '',      '',    '',     '']

		rb = ' --robustFit 1'
		#_mass          = ["260", "270", "300", "350", "400", "450", "500", "550", "600", "650", "750", "800", "900", "1000"]
		comb_optsImp    = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		comb_optsRobust = [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]
		comb_optsImp2   = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		comb_optsRobust2= [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]
		
		ee_optsImp      = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		ee_optsRobust   = [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]
		ee_optsImp2     = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		ee_optsRobust2  = [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]
		
		uu_optsImp      = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		uu_optsRobust   = [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]
		uu_optsImp2     = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		uu_optsRobust2  = [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]


	elif (resType == "HHBulkGrav") :
	# SPIN 2
		#            = ["260","270","300","350","400", "450", "500",  "550",  "600", "650", "750",  "800", "900", "1000"]
		comb_rangesM = [1000 ,1000 ,1000  ,200  ,200   ,100    ,50    ,80     ,80    ,100    ,100    ,200   ,200    ,200]
		comb_rangesP = [1000 ,1000 ,1000  ,200  ,200   ,100    ,50    ,80     ,80    ,100    ,100    ,200   ,200    ,200]
		comb_opts    = ['',    '',   '',   '',   '',    '',     '',     '',    '',    '',     '',      '',    '',     '']

		# range ee
		ee_rangesM   = [1000 ,1000 ,1000  ,400  ,200   ,200    ,100   ,100    ,100   ,100    ,200    ,200   ,200    ,200]
		ee_rangesP   = [1000 ,1000 ,1000  ,400  ,200   ,200    ,100   ,100    ,100   ,100    ,200    ,200   ,200    ,200]
		ee_opts      = [ '',   '',   '',   '',   '',    '',    '',     '',     '',    '',     '',      '',    '',     '']

		# range uu
		uu_rangesM   = [1000 ,1000 ,1000  ,300  ,200   ,200    ,100   ,100    ,100   ,100    ,200    ,200   ,200    ,200]
		uu_rangesP   = [1000 ,1000 ,1000  ,300  ,200   ,200   , 100   ,100    ,100   ,100    ,200    ,200   ,200    ,200]
		uu_opts      = [ '',   '',   '',    '',   '',    '',    '',    '',      '',   '',     '',      '',    '',     '']

		rb = ' --robustFit 1'
		#_mass          = ["260", "270", "300", "350", "400", "450", "500", "550", "600", "650", "750", "800", "900", "1000"]
		comb_optsImp    = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		comb_optsRobust = [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]
		comb_optsImp2   = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		comb_optsRobust2= [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]
		
		ee_optsImp      = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		ee_optsRobust   = [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]
		ee_optsImp2     = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		ee_optsRobust2  = [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]
		
		uu_optsImp      = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		uu_optsRobust   = [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]
		uu_optsImp2     = [ '',    '',   '',    '',    '',    '',     '',    '',    '',   '',     '',      '',    '',     '']
		uu_optsRobust2  = [ rb,    rb,   rb,    rb,    rb,    rb,     rb,    rb,    rb,   rb,     rb,      rb,    rb,     rb]



	## obs gof, got from running --runGOF
    #_mass      = ["260"    ,"270"   ,"300"  ,"350"   ,"400"   , "450"   ,"500",  "550",   "600",  "650",   "750",    "800",   "900",   "1000"]
	comb_gofs    = [72.763, 48.2685, 50.5128, 49.8398, 58.6826, 32.6924, 36.3977, 46.1962, 69.5987, 51.2668, 58.1196, 45.2918, 47.6678, 124.632]
	#ee v3 (2019_01_12) fix m350, m1000
	ee_gofs     = [20.0603, 18.9581, 17.3724, 26.3825, 28.1729, 16.908,  15.7939, 7.36142, 20.2398, 18.986,  14.8632, 24.8008, 18.4943, 22.6988]
	#uu v2 (2019_01_13)
	uu_gofs     = [23.8917, 18.6856, 24.5491, 18.4348, 10.0177, 9.93045, 17.0569, 24.6645, 20.9563, 31.5172, 31.5885, 22.0562, 28.8057, 20.0415]


	_analysisChan = ['CombMuEle','uujj','eejj']
	_leptonChan   = ['CombMuEle','uu','ee']
	_leps         = ['CombMuEle','muon','electron']
	kmax_inis     = [49,45,44]

	#np_ignore = ['HF','EC2','QCDscale_']
	np_ignore = ['HF','EC2']

	#gofalgos  = ['saturated', 'AD', 'KS']
	gofalgos  = ['saturated']
	#gofalgos  = ['AD','KS']

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
			cardname = 'GGToX' + x_spin + 'ToHHTo2b2l2j_LimitShapeHH' + _leptonChan[ich] + '_' + resType + _mass[im]
			if _leptonChan[ich] in ['uu','ee']:
				cardname = 'CLSLimits/LimitShapeHH' + _leptonChan[ich] + '/' + cardname
			cardnametxt = cardname + '.txt'
			wsfilename = cardname + '.root'
			#if verbose == '1' : print cardnametxt, wsfilename
			### ----------


			##----- remove NP from cards:
			if '--removeNP' in sys.argv:
				for np in np_ignore:
					sedcomnpdel = 'sed -i \'/' + np + '/d\' ' + cardnametxt
					if verbose == '1' : print sedcomnpdel
					if '--launch' in sys.argv:
						os.system(sedcomnpdel)

				sedcomkmax = 'sed -i \'s#kmax ' + str(kmax_inis[ich]) + '#kmax ' +str(kmax_inis[ich] - 7) + '#g\' ' + cardnametxt
				if verbose == '1' :
					print sedcomkmax
				if '--launch' in sys.argv:
					os.system(sedcomkmax)

			##----- (1) create wprk space
			## text2workspace.py GGToX0ToHHTo2b2l2j_LimitShapeHHCombMuEle_HHres1000.txt
			if '--text2workspace' in sys.argv:
				txt2wpcom = 'text2workspace.py ' + cardnametxt
				if verbose == '1' :
					print txt2wpcom
				if '--launch' in sys.argv:
					os.system(txt2wpcom)

			##----- (2) Limits ---
			if '--limits' in sys.argv:
				if domass == '': flaglog = ''
				else : flaglog = _mass[im]
				
				limitcom = 'combine -M AsymptoticLimits -d ' + wsfilename + '| tee -a outlog_limit_M' + flaglog +'.txt'
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

				fitcom = 'combine -M FitDiagnostics -d ' + wsfilename + ' -m ' + _mass[im] + ' --setParameterRanges r=-'+ str(rangesM[im])+','+str(rangesP[im]) + ' -n ' + n_opt + opts[im] + asimov_opt + log_opt
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
						gofcom_obs = 'combine -M GoodnessOfFit --algorithm ' + gofalgos[igof] + ' -d ' + wsfilename + ' -m ' +_mass[im]+' --setParameterRanges r=-' + str(rangesM[im])+','+str(rangesP[im]) + ' -n ' + dataname + opts[im]
						if verbose == '1' :
							print gofcom_obs + '\n' #+ gofcom_toy
						if '--launch' in sys.argv:
							os.system(gofcom_obs)
					if '--toy' in sys.argv:
						gofcom_toy = 'combine -M GoodnessOfFit --algorithm ' + gofalgos[igof] + ' -d ' + wsfilename + ' -m ' +_mass[im]+' --setParameterRanges r=-' + str(rangesM[im])+','+str(rangesP[im]) + ' -n ' + toysname + opts[im] + ' -t 120'
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


			##----- (4.1) GOF Toys bsub ---
			if '--runGOFToysJobs' in sys.argv:
				dateTo = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
				mtmpdir = 'tmpjobs_gof_' + dateTo
				if '--launch' in sys.argv:
					os.system('mkdir ' + mtmpdir)
				
				nfiles = 10 # number of files splitted for running toy
				ntoy_afile = 100

				for igof in range(len(gofalgos)):
					for _fth in range(nfiles): # number of files splitted for running toy
						seed = 123457 + _fth
						tjobname_out = mtmpdir+'/job_' + 'do' + str('s'+x_spin) + '_M' + str(_mass[im]) + '_p' + str(_fth) + '.out'
						tjobname_err = mtmpdir+'/job_' + 'do' + str('s'+x_spin) + '_M' + str(_mass[im]) + '_p' + str(_fth) + '.err'
						tjobname     = mtmpdir+'/job_' + 'do' + str('s'+x_spin) + '_M' + str(_mass[im]) + '_p' + str(_fth) + '.sh'
						job = '#!/bin/bash\n'
						job += 'cd $CMSSW_BASE/src/\n'
						job += 'eval `scramv1 runtime -sh`\n'
						job += 'cd ' + str(mycwd) + '\n'
						##job += 'cd $CMSSW_BASE/src\n'
						##job += 'cmsenv\n'
						##job += 'mycwd=`pwd`\n'
						##job += 'cd $mycwd\n'

						com = 'combine -M GoodnessOfFit --algorithm ' + gofalgos[igof] + ' -d ' + wsfilename + ' -m ' +_mass[im]+' --setParameterRanges r=-' + str(rangesM[im])+','+str(rangesP[im])  + ' -n ' + str(gofalgos[igof]+'_s'+x_spin+'M'+_mass[im]+_leptonChan[ich])  + opts[im] + ' -t ' + str(ntoy_afile) + ' -s ' + str(seed)
						print '... going to submit run command ==> ', com
						com +='\n\n'

						ajob = str(job)
						if '--launch' in sys.argv:
							tjob = open(tjobname,'w')
							tjob.write(ajob+'\n\n')
							tjob.write(com)
							tjob.close()
							os.system('chmod 755 '+tjobname)
						bsub = 'bsub -q 1nh -o ' +tjobname_out+ ' -e ' +tjobname_err+ ' -J ' +  tjobname + ' < ' + tjobname + ' '
						print bsub, '\n'
						if '--launch' in sys.argv:
							os.system(bsub)
							os.system('sleep 1')

			##----- (4.2) GOF plot p-value ---
			if '--runGOFpval' in sys.argv:
				for igof in range(len(gofalgos)):
					haddcom = 'hadd -f ' + str('sum_'+gofalgos[igof]+'_s'+x_spin+'M'+_mass[im]+_leptonChan[ich]+'.root') + ' ' + str('higgsCombine' + gofalgos[igof]+'_s'+x_spin+'M'+_mass[im]+_leptonChan[ich] + '.GoodnessOfFit*.root')
					if '--launch' in sys.argv:
						#os.system(haddcom)
						os.system('sleep 1')

						infile = ROOT.TFile(str('sum_'+gofalgos[igof]+'_s'+x_spin+'M'+_mass[im]+_leptonChan[ich]+'.root'))
						tree = infile.Get("limit")
						hist=ROOT.TH1F("testStatistic","testStatistic;test statistic;",100,0,400)
						hist.Sumw2()
						selection= ''
						tree.Project("testStatistic","limit",selection)
						hist2 = hist.Clone('tmp')
						hist2.Scale(1/hist.Integral())
						#print 'gof ', gofs[im]
						#print hist2.GetXaxis().FindBin(143.592)
						#print hist2.GetNbinsX()
						p = hist2.GetXaxis().FindBin(gofs[im])
						thepval = hist2.Integral(p,hist2.GetNbinsX())

						print tree.GetEntries(), hist.Integral(), thepval, hist2.Integral()

						can1 = ROOT.TCanvas("can1", "can1", 800, 550)
						can1.cd()
						can1.SetTicks()
						can1.SetGrid()
						hist.SetTitle('Test Stat and P-value for ' + gofalgos[igof]+'_s'+x_spin+'M'+_mass[im]+_leptonChan[ich])
						hist.SetLineColor(kBlue)
						hist.Draw("HIST")

						ar1 = ROOT.TArrow(gofs[im],0.1,gofs[im],10,0.02,"<|") # after deaw hist, the coordinate is set to x-y axis value
						ar1.SetAngle(40)
						ar1.SetLineWidth(2)
						ar1.SetLineColor(kRed)
						ar1.SetFillColor(kRed)
						ar1.Draw()

						txt1 = 'Best fit test statistic: ' + str(gofs[im])
						txt2 = 'P-value : ' + str(thepval)

						pt = ROOT.TPaveText(0.5,0.5,0.7,0.7,"NDC NB")
						pt.SetTextSize(0.04)
						pt.SetFillColor(0)
						pt.SetTextAlign(12)
						pt.AddText(txt1)
						pt.GetListOfLines().Last().SetTextColor(kRed)
						pt.AddText(txt2)
						pt.GetListOfLines().Last().SetTextColor(kRed)
						pt.Draw()

						outnamefull = 'pvalue_' + gofalgos[igof]+'_s'+x_spin+'M'+_mass[im]+_leptonChan[ich] + '.pdf'
						can1.Print(outnamefull);

						del hist
						del tree
						del can1

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
				iniImpcom = 'combineTool.py -M Impacts -d ' + wsfilename + ' -m ' + _mass[im] + ' --doInitialFit --setParameterRanges r=-'+ str(rangesM[im])+','+str(rangesP[im]) + ' -n ' + n_opt + optsImp[im] + optsRobust[im] + asimov_opt
				if verbose == '1' : print iniImpcom
				if '--launch' in sys.argv:
					os.system(iniImpcom)
			if '--runImpactDoFit' in sys.argv:
				dofitImpcom = 'combineTool.py -M Impacts -d ' + wsfilename + ' -m ' + _mass[im] + ' --doFits --parallel 20 --setParameterRanges r=-'+ str(rangesM[im])+','+str(rangesP[im]) + ' -n ' + n_opt + optsImp2[im] + optsRobust2[im] + asimov_opt
				if verbose == '1' : print dofitImpcom
				if '--launch' in sys.argv:
					os.system(dofitImpcom)
			if '--runImpactPDF' in sys.argv:
				pdfImpcom1 = 'combineTool.py -M Impacts -d ' + wsfilename + ' -m ' + _mass[im] + ' -o ' + n_opt + '.json' + ' -n ' + n_opt
				pdfImpcom2 = 'plotImpacts.py -i ' + n_opt + '.json' ' -o ' + n_opt
				#combineTool.py -M Impacts -d GGToX0ToHHTo2b2l2j_LimitShapeHHCombMuEle_HHres1000.root -m 125 -o impacts.json
				#plotImpacts.py -i impacts.json -o impacts_1000
				if verbose == '1' :
					print pdfImpcom1
					print pdfImpcom2
				if '--launch' in sys.argv:
					os.system(pdfImpcom1)
					os.system(pdfImpcom2)

			##----- (6) impacts ---


if __name__ == "__main__":
	main()







