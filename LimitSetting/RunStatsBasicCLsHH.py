#1100:
#observed: Limit: r < 0.826408 +/- 0.0112619 @ 95% CL
#median expected:Limit: r < 0.957764 +/- 0.0139413 @ 95% CL
#expected+1sigma:Limit: r < 1.34497 +/- 0.0210123 @ 95% CL
#expected+2sigma:Limit: r < 1.82489 +/- 0.0116509 @ 95% CL
#expected-1sigma:Limit: r < 0.843578 +/- 0.0188071 @ 95% CL
#expected-2sigma:
#
#
#-- Asymptotic -- 
#Observed Limit: r < 0.6758
#Expected  2.5%: r < 0.3972
#Expected 16.0%: r < 0.5865
#Expected 50.0%: r < 0.9416
#Expected 84.0%: r < 1.5797
#Expected 97.5%: r < 2.5324

###### TO RUN THIS SCRIPT #####
#----
# python RunStatsBasicCLsHH.py --do_BetaOne --HHresuujj -c LimitShapeHH (--StatOnly) --Asymptotic_Only (--FastRun) (--doSpin2) (--noAbsAcc --NpIgnore)
# python RunStatsBasicCLsHH.py --do_BetaOne --HHreseejj -c LimitShapeHH (--StatOnly) --Asymptotic_Only (--FastRun) (--doSpin2) (--noAbsAcc --NpIgnore)
#
#--- Combined Muon ELectron
# python RunStatsBasicCLsHH.py --doMakeCombineCards --HHresCombMuEle -c LimitShapeHH (--doSpin2)
# python RunStatsBasicCLsHH.py --do_BetaOne --HHresCombMuEle -c LimitShapeHH (--StatOnly) --Asymptotic_Only (--doSpin2) (--noAbsAcc --NpIgnore)
#
####### ###### ######


import os
import sys
import subprocess
import math 

import random

#ESTIMATIONMETHOD = ' -M Asymptotic '
ESTIMATIONMETHOD = ' -M AsymptoticLimits '

#person = (os.popen('whoami').readlines())[0].replace('\n','')

masses = []
lqtype = 'LQ'
resType = 'HHres'

do_BetaOne = 0
do_CombineCards = 0
_StatOnly = 0
_CombMuEleLimit = 0
_FastRun = 0
_autoMC_stats = 1 # this is default now
_spin = '0'
_noData = 0
_noAbsAcc = 0
_npignore = 0

cdir = ''
ell = ''
queue = '1nd'
dobatch = True

fullcardfile = 'FinalCardsLQ'

##--------------------------------------------
##--------------------------------------------
if '--doSpin2' in sys.argv:
	_spin = '2'
	resType = 'HHBulkGrav'

##--------------------------------------------
##--------------------------------------------
if '--do_BetaOne' in str(sys.argv):
	do_BetaOne = 1

##--------------------------------------------
##--------------------------------------------
# Here I want to run quickly without iterations for the optimized --rAbsAcc
if '--noAbsAcc' in sys.argv:
	_noAbsAcc = 1

if '--NpIgnore' in sys.argv:
	_npignore = 1

if '--doMakeCombineCards' in sys.argv:
	do_CombineCards = 1

##--------------------------------------------
##--------------------------------------------
if '--HHresCombMuEle' in sys.argv:
	lqtype = 'HHresCombMuEle' # need at least str 'HHres'
	fullcardfile = 'FinalCardsLQuu' # set to 'uu' to run through the code, to get 'masses'
	_CombMuEleLimit = 1

if '--HHresuujj' in sys.argv:
	lqtype = 'HHresuujj'
	ell = 'u'
	fullcardfile = 'FinalCardsLQuu'

if '--HHreseejj' in sys.argv:
	lqtype = 'HHreseejj'
	ell = 'e'
	fullcardfile = 'FinalCardsLQee'

##--------------------------------------------
##--------------------------------------------
if '--StatOnly' in sys.argv:
	_StatOnly = 1

if '--FastRun' in sys.argv:
	_FastRun = 1
	ESTIMATIONMETHOD = ' -M AsymptoticLimits --run blind'

if '--doNoData' in sys.argv:
	_noData = 1
	ESTIMATIONMETHOD = ' -M AsymptoticLimits --run blind'


if 'CLSLimits' not in os.listdir('.'):
	os.system('mkdir CLSLimits')
if 'ShellScriptsForBatch' not in os.listdir('.'):
	os.system('mkdir ShellScriptsForBatch')

##--------------------------------------------
##--------------------------------------------
for x in range(len(sys.argv)):
	if sys.argv[x] == '-c':
		cdir = sys.argv[x+1]
		cdir_ori = cdir
		cdir += ell+ell
		if do_CombineCards:
			os.system('mkdir CLSLimits/'+cdir_ori+'CombMuEle')
		else:
			os.system('mkdir CLSLimits/'+cdir)
	if sys.argv[x] == '-q':
		queue = str(sys.argv[x+1])
	if '--Asymptotic_Only' in sys.argv[x]:
		dobatch = False

##----------------------------------------------------------------------------------------
##----------------------------------------------------------------------------------------

from ROOT import *
from array import array

print ' process lqtype ', lqtype
fullcardfile += '_s' + _spin + '.txt'
cr = '  \n'

fullcards = open(fullcardfile,'r')
mycards = []
for line in fullcards:
	mycards.append(line.replace('\n',''))

digis = '0123456789'
name = []
for x in mycards:
	if '.txt' in x:
		name.append((x.replace('.txt','')).replace('\n','')) 
		mm = ''
		for a in x:
			if a in digis:
				mm += a
		if int(mm) not in masses:
			masses.append(int(mm))

BetaOneObs = []
BetaOne95down = []
BetaOne95up = []
BetaOne68down = []
BetaOne68up = []
BetaOneExp = []

sysmedths_uu = ['JESAbsoluteMPFBias','JESAbsoluteScale','JESAbsoluteStat','JESFlavorQCD','JESFragmentation','JESPileUpDataMC','JESPileUpPtBB','JESPileUpPtEC1','JESPileUpPtEC2','JESPileUpPtHF','JESPileUpPtRef','JESRelativeBal','JESRelativeFSR','JESRelativeJEREC1','JESRelativeJEREC2','JESRelativeJERHF','JESRelativePtBB','JESRelativePtEC1','JESRelativePtEC2','JESRelativePtHF','JESRelativeStatEC','JESRelativeStatFSR','JESRelativeStatHF','JESSinglePionECAL','JESSinglePionHCAL','JESTimePtEta','JER','LUMI','PU','ZNORM','TTNORM','MUONIDISO','HIP','MUONHLT','BTAG','QCDSCALE','topPtReweight','PDF']

sysmedths_ee = ['JESAbsoluteMPFBias','JESAbsoluteScale','JESAbsoluteStat','JESFlavorQCD','JESFragmentation','JESPileUpDataMC','JESPileUpPtBB','JESPileUpPtEC1','JESPileUpPtEC2','JESPileUpPtHF','JESPileUpPtRef','JESRelativeBal','JESRelativeFSR','JESRelativeJEREC1','JESRelativeJEREC2','JESRelativeJERHF','JESRelativePtBB','JESRelativePtEC1','JESRelativePtEC2','JESRelativePtHF','JESRelativeStatEC','JESRelativeStatFSR','JESRelativeStatHF','JESSinglePionECAL','JESSinglePionHCAL','JESTimePtEta','JER','LUMI','PU','ZNORM','TTNORM','ELEIDISO','ELEHLT','BTAG','QCDSCALE','topPtReweight','PDF']

unCorrelat_Vars = ['ZNORM','TTNORM','MUONIDISO','HIP','MUONHLT','ELEIDISO','ELEHLT']

np_ignore = []
if _npignore :
	np_ignore = ['HF','EC2']

if _StatOnly:
	sysmedths = []
else:
	if lqtype == 'HHreseejj' : sysmedths = sysmedths_ee
	else : sysmedths = sysmedths_uu
	#sysmedths += ['JER','LUMI','PU','ZNORM','TTNORM','MUONIDISO','HIP','MUONHLT','BTAG','QCDSCALE','topPtReweight','PDF']
	#sysmedths += ['JES','MES','JER','MER','LUMI','PU','ZNORM','TTNORM','MUONIDISO','MUONHLT','HIP','BTAG','QCDSCALE','PDF']


if (resType == "HHres") :
	## SPIN 0
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

if '--HHresCombMuEle' in sys.argv:
	rangesM = comb_rangesM
	rangesP = comb_rangesP

if '--HHresuujj' in sys.argv:
	rangesM = uu_rangesM
	rangesP = uu_rangesP

if '--HHreseejj' in sys.argv:
	rangesM = ee_rangesM
	rangesP = ee_rangesP


if do_CombineCards:
	print ' ... combining the card of uu and ee channels from 2l2q analysis ...'
	for hhmass in masses:
		cardinuu = 'CLSLimits/'+cdir_ori+'uu'+'/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir_ori+'uu'+'_'+resType+str(hhmass)+'.txt'
		cardinee = 'CLSLimits/'+cdir_ori+'ee'+'/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir_ori+'ee'+'_'+resType+str(hhmass)+'.txt'
		comm_combcards = 'combineCards.py HHresuujj=' + cardinuu + ' HHreseejj=' + cardinee + ' > CLSLimits/'+cdir_ori+'CombMuEle/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir_ori+'CombMuEle_'+resType+str(hhmass)+'.txt'
		print comm_combcards+'\n'
		os.system(comm_combcards)
		#print cardinuu, cardinee
		os.system('cp *uu*_13TeV_new.root CLSLimits/'+cdir_ori+'uu'+'/.')
		os.system('cp *ee*_13TeV_new.root CLSLimits/'+cdir_ori+'ee'+'/.')
		print '... ... Done with mass ', str(hhmass)
	print ' ... Done. Exiting the program ...'
	sys.exit()


if do_BetaOne == 1:
	
	masses_betaone = []

	for x in range(len(name)):
		
		print 'Calculating limit for: ' + name[x] + ' ' + lqtype + ' ' + resType
		
		# generate data cards from fullcardfile
		if not _CombMuEleLimit:
			print '... ... create cards in ', cdir
			f = open('CLSLimits/'+cdir+'/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir+'_'+name[x]+'.txt','w')
			count = 0
			# print name[x]
			nbin_write = 1
			for l in mycards:

				written = 0
				if '.txt' in l and name[x] in l and str(name[x]+'0') not in l:
					count = 1
					for m in masses:
						if str(m) in l and int(m) not in masses_betaone: # AH: basically 'masses_betaone' is equal to 'masses'
							masses_betaone.append(int(m))
				if '.txt' in l and name[x] not in l:
					count = 0


				if count ==1 and '.txt' not in l:
					if 'Shape' in cdir:
						# for stat only datacard ignore the JES line
						if _StatOnly and 'JES' in l:
							continue
						#elif 'JES' in l:
						#	#f.write('JES lnN')
						#	#f.write(nbin_write*' 1.0')
						#	#f.write('\n')
						#	f.write(l+'\n')

						if 'ALIGN' in l :
							continue # to make sure ALIGN is removed
						
						for sysmed in sysmedths:
							sysm_towrite = ''
							if sysmed in l: ## I always put JER after JESs, this makes sure that JER will not be matched to JESRelativeJEREC1
								if sysmed == 'MUONIDISO' :sysm_towrite = 'CMS_eff_m'
								elif sysmed == 'MUONHLT'   :sysm_towrite = 'CMS_eff_trigger_uu'
								elif sysmed == 'ELEIDISO'  :sysm_towrite = 'CMS_eff_e'
								elif sysmed == 'ELEHLT'    :sysm_towrite = 'CMS_eff_trigger_ee'
								elif sysmed == 'BTAG'      :sysm_towrite = 'CMS_btag_comb'
								elif sysmed == 'JER'       :sysm_towrite = 'CMS_res_j'
								elif sysmed == 'LUMI'      :sysm_towrite = 'lumi_13TeV'
								elif sysmed == 'PDF'       :sysm_towrite = 'pdf'
								elif sysmed == 'QCDSCALE'  :sysm_towrite = 'QCDscale'
								elif sysmed in unCorrelat_Vars:
									sysm_towrite = ell+ell+sysmed
								else:
									if any(np in sysmed for np in np_ignore):
										sysm_towrite = '#'+sysmed
									else:
										sysm_towrite = sysmed
								
								print ' ++++++++ writing sysmed ', sysmed, sysm_towrite
								if sysmed != 'QCDSCALE':
									f.write(sysm_towrite +' shape')
									if sysmed == 'TTNORM' :
										f.write(' - 1 - - - - - -\n')
									elif sysmed == 'topPtReweight' :
										f.write(' - 1 - - - - - -\n')
									elif sysmed == 'ZNORM' :
										f.write(' - - 1 - - - - -\n')
									elif sysmed == 'LUMI' :
										f.write(' 1 - - 1 1 1 1 1\n')
									else :
										f.write(nbin_write*' 1')
										f.write('\n')
									written = 1
									break
								elif sysmed == 'QCDSCALE':
									f.write('QCDscale_'+resType +' shape 1 - - - - - - -\n')
									f.write('QCDscale_ttbar shape - 1 - - - - - -\n')
									f.write('QCDscale_ZJets shape - - 1 - - - - -\n')
									f.write('QCDscale_WJets shape - - - 1 - - - -\n')
									f.write('QCDscale_sTop shape - - - - 1 - - -\n')
									f.write('QCDscale_VV shape - - - - - 1 - -\n')
									f.write('QCDscale_QCD shape - - - - - - 1 -\n')
									f.write('QCDscale_SMH shape - - - - - - - 1\n')
									written = 1
									break
						
						if 'jmax' in l:
							f.write(l+'\n')
							nbin_write = int(l.replace('jmax','').replace('\n','').replace(' ','')) + 1
						elif 'bin  1  1' in l:
							f.write('bin')
							f.write(nbin_write * str(' HHres'+ell+ell+'jj'))
							f.write('\n')
						elif 'bin 1' in l:
							f.write('bin HHres'+ell+ell+'jj'+'\n')
						elif name[x] in l:
							f.write(l.replace(name[x],resType)+'\n')
						elif 'kmax' in l:
							if _StatOnly:
								if not _autoMC_stats:
									nkmax = int(l.replace('kmax','').replace('\n','').replace(' ','')) - 1 # to remove fake JES
									f.write('kmax '+str(nkmax)+'\n')
								else:
									f.write('kmax 0 \n')
							else:
								if not _autoMC_stats:
									f.write(l+'\n')
								else:
									nkmax = int(l.replace('kmax','').replace('\n','').replace(' ','')) - 8 + 7 # hard coded value for now (-8 for stat, +7 for QCDscale) FIX ME: NEED to know how many "stat_" to be removed
									if _npignore:
										f.write('kmax '+str(nkmax-7)+'\n')
									else:
										f.write('kmax '+str(nkmax)+'\n')
											
							f.write((15*'-')+'\n')
							#f.write('shapes * * '+ name[x] + '_' +ell+ell +'_bdt_discrim_M' + str(name[x].replace(resType,'')) +'_13TeV_new.root $CHANNEL/$PROCESS'+'\n')
							if _StatOnly:
								f.write('shapes * * '+ name[x] + '_' +ell+ell +'_bdt_discrim_M' + str(name[x].replace(resType,'')) +'_13TeV_new.root $CHANNEL/$PROCESS'+'\n')
							else:
								f.write('shapes * * '+ name[x] + '_' +ell+ell +'_bdt_discrim_M' + str(name[x].replace(resType,'')) +'_13TeV_new.root $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC'+'\n')
							
							#if float(name[x].replace(resType,''))<400:
							#	f.write('shapes * * '+ name[x] +'_bdt_discrims3_low_13TeV_new.root $CHANNEL/$PROCESS'+'\n')
							#elif float(name[x].replace(resType,''))>=400:
							#	f.write('shapes * * '+ name[x] +'_bdt_discrims3_high_13TeV_new.root $CHANNEL/$PROCESS'+'\n')
							f.write((15*'-')+'\n')
						elif 'stat_' in l:
							if not _autoMC_stats:
								f.write(ell+ell+'_'+l+'\n')
							else:
								f.write('')
								if 'stat_SMH' in l:
									f.write('* autoMCStats 0' + '\n')
						elif 'observation' in l:
							if _noData:
								f.write('observation 0'+'\n')
							else:
								f.write(l+'\n')
						else:
							if not written:
								if (_autoMC_stats or _StatOnly) and ('lnN' in l):
									f.write('')
								else:
									f.write(l+'\n')
					else:
						f.write(l+'\n')
			f.close()
		
		if dobatch:
			os.system('mkdir CLSLimits/'+cdir+'/'+name[x])
			mdir = (os.popen('pwd').readlines())[0]
			mdir = mdir.replace('\n','')
			fsub = open('ShellScriptsForBatch/subbetaone_'+cdir+name[x]+'.csh','w')
			fsub.write('#!/bin/csh'+ cr)
			fsub.write('cd ' + mdir+ cr)
			fsub.write('eval `scramv1 runtime -csh`'+ cr)
			fsub.write('cd -'+ cr)
			fsub.write('cp '+mdir+'/CLSLimits/'+cdir+'/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir+'_'+name[x]+ '.txt . '+ cr)
			fsub.write('SUBCOMMAND'+'\n')
			fsub.close()
		
		## Estimate the r values with Asymptotic CLs
		EstimationInformation = [' r < 0.000000']
		rmax = 1000.0
		if 'HHres' in lqtype:
			rmax = 10000.0
			#if float(name[x].replace(resType,''))<900:
			#	rmax = float(name[x].replace(resType,''))/100.#fixme was 10000.0
			#elif float(name[x].replace(resType,''))<1200:
			#	rmax = float(name[x].replace(resType,''))/10.#fixme was 10000.0
			#else:
			#	rmax = float(name[x].replace(resType,''))/4.#fixme was 10000.0

		breaker = False
		ntry = 0 
		oldrmax = 100000.0
		print '\n AH: EstimationInformation  is : ', str(EstimationInformation), '\n' # AH:

		while 'r < 0.000000' in str(EstimationInformation):
			ntry += 1
			rAbsAcc='.00005'
			
			if _FastRun or _noData:
				print ('combine '+ESTIMATIONMETHOD+' CLSLimits/'+cdir+'/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir+'_'+name[x]+'.txt')
				EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/'+cdir+'/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir+'_'+name[x]+'.txt').readlines()
			elif _CombMuEleLimit:
				if _noAbsAcc :
					print ('combine '+ESTIMATIONMETHOD+' CLSLimits/'+cdir_ori+'CombMuEle/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir_ori+'CombMuEle_'+name[x]+'.txt' + ' --rMin -'+ str(rangesM[x])+' --rMax '+str(rangesP[x]))
					EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/'+cdir_ori+'CombMuEle/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir_ori+'CombMuEle_'+name[x]+'.txt' + ' --rMin -'+ str(rangesM[x])+' --rMax '+str(rangesP[x])).readlines()
				else:
					print ('combine '+ESTIMATIONMETHOD+' CLSLimits/'+cdir_ori+'CombMuEle/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir_ori+'CombMuEle_'+name[x]+'.txt --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc)
					EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/'+cdir_ori+'CombMuEle/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir_ori+'CombMuEle_'+name[x]+'.txt --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc).readlines()
			else:
				if _noAbsAcc :
					print ('combine '+ESTIMATIONMETHOD+' CLSLimits/'+cdir+'/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir+'_'+name[x]+'.txt')
					EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/'+cdir+'/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir+'_'+name[x]+'.txt').readlines()
				else:
					print ('combine '+ESTIMATIONMETHOD+' CLSLimits/'+cdir+'/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir+'_'+name[x]+'.txt --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc)
					EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/'+cdir+'/GGToX'+_spin+'ToHHTo2b2l2j_'+cdir+'_'+name[x]+'.txt --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc).readlines()

			#print '\n AH I am in while Loop : EstimationInformation  is : ', str(EstimationInformation), '\n' # AH:
			print 'oldrmax is ', oldrmax , ' rmax is ', rmax, ' abs(rmax - oldrmax) is ', abs(rmax - oldrmax)
			if abs(rmax - oldrmax)<.1*rmax:
				breaker=True # AH: real exit loop condition is here
			if _FastRun:
				breaker=True # AH: real exit loop condition is here
			if _noData:
				breaker=True # AH: real exit loop condition is here
			if _noAbsAcc :
				breaker=True
			if breaker ==True:
				break

			effrmax = -999999
			for e in EstimationInformation:
				if 'r <'  in e and 'Expected' in e:
					thisrval = e.split('<')[-1]
					thisrval = thisrval.replace('\n','')
					thisrval = float(thisrval)
					if thisrval>effrmax:
						effrmax = thisrval

			oldrmax = float(rmax)
			
			print '\n AH: effrmax  is : ', effrmax , '\n' # AH:
			if effrmax < 0:
				rmax = 0.6*rmax
			else:
				rmax = effrmax*2.0
			print '\n AH: rmax  is : ', rmax , '\n' # AH:
			
			EstimationInformation = [' r < 0.000000']
			if ntry>100:
				breaker = True

		
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


################################################################################################################
################################################################################################################



################################################################################################################
################################################################################################################


os.system('rm higgsCombineTest*root')

print '\n\n\n'

#### ASYMPTOTIC CLS PRINTOUT ###

# for 'HHres'
mTh = [260.0,270.0,300.0,350.0,400.0,450.0,500.0,550.0,600.0,650.0,750.0,800.0,900.0,1000.0]
xsTh = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]


#### BETA ONE CHANNEL
if do_BetaOne == 1:
	if not _CombMuEleLimit:
		masses = masses_betaone
		#if 'LQ' in lqtype:
		#	masses=[200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000]

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
		if not _FastRun and not _noData:
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




	
	
