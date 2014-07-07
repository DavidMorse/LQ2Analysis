import os
import sys
import subprocess
import math 

import random
 #betas = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6,0.61,0.62,0.63,0.64,0.65,0.66,0.67,0.68,0.69,0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,0.99999]
#betas = [.3,0.5]
#betas = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99]
betas = [0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.18,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,0.9995]
ESTIMATIONMETHOD = ' -M Asymptotic '
METHOD = '-M HybridNew --rule CLs --frequentist CONFIGURATION --clsAcc=0 -s -1 -T 70 -i 70 --singlePoint SINGLEPOINT --saveToys --saveHybridResult'
person = (os.popen('whoami').readlines())[0].replace('\n','')



masses = []
do_BetaOne = 0
do_BetaHalf = 0 
do_combo = 0
do_observedonly = 0
cdir = ''
if 'do_BetaOne' in str(sys.argv):
	do_BetaOne = 1
if 'do_BetaHalf' in str(sys.argv):
	do_BetaHalf = 1
if 'do_Combo' in str(sys.argv):
	do_combo = 1
if 'just_observed' in str(sys.argv):
	do_observedonly = 1	
singlebeta = -1

numdo = 1	
queue = '1nd'
if 'CLSLimits' not in os.listdir('.'):
	os.system('mkdir CLSLimits')
if 'ShellScriptsForBatch' not in os.listdir('.'):
	os.system('mkdir ShellScriptsForBatch')

dobatch = True
for x in range(len(sys.argv)):
	if sys.argv[x] == '-c':
		cdir = sys.argv[x+1]

		os.system('mkdir CLSLimits/BetaOne'+cdir)
		os.system('mkdir CLSLimits/BetaHalf'+cdir)
		os.system('mkdir CLSLimits/Combo'+cdir)

	if sys.argv[x] == '-n':
		numdo = int(sys.argv[x+1])
	if sys.argv[x] == '-q':
		queue = str(sys.argv[x+1])
	if sys.argv[x] == '--single_beta':
		singlebeta = float(sys.argv[x+1])
	if '--Asymptotic_Only' in sys.argv[x]:
		dobatch = False 
from ROOT import *
from array import array


if singlebeta>0:
	betas = []
	betas.append(singlebeta)
beta_combo = []
m_combo = []
dif_combo = []
cr = '  \n'

fullcards = open('FinalCards.txt','r')
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

BetaHalfObs = []
BetaHalf95down = []
BetaHalf95up = []
BetaHalf68down = []
BetaHalf68up = []
BetaHalfExp = []

ComboObs = []
Combo95down = []
Combo95up = []
Combo68down = []
Combo68up = []
ComboExp = []

ComboBetaOneObs = []
ComboBetaOne95down = []
ComboBetaOne68down = []
ComboBetaOneExp = []
ComboBetaOne68up = []
ComboBetaOne95up = []


ComboBetaHalfObs = []
ComboBetaHalf95down = []
ComboBetaHalf68down = []
ComboBetaHalfExp = []
ComboBetaHalf68up = []
ComboBetaHalf95up = []
						
if do_BetaOne == 1:
	masses_betaone = []

	for x in range(len(name)):
		if 'BetaHalf' in name[x]:
			continue
		print 'Calculating limit for: ' + name[x]
		f = open('CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg','w')
		count = 0
		# print name[x]

		for l in mycards:

			if '.txt' in l and name[x] in l:
				count = 1
				for m in masses:
					if str(m) in l and int(m) not in masses_betaone:
						masses_betaone.append(int(m))
			if '.txt' in l and name[x] not in l:
				count = 0


			if count ==1 and '.txt' not in l:
				f.write(l+'\n')
	

		f.close()

		os.system('mkdir CLSLimits/BetaOne'+cdir+'/'+name[x])

		mdir = (os.popen('pwd').readlines())[0]
		mdir = mdir.replace('\n','')
		fsub = open('ShellScriptsForBatch/subbetaone_'+cdir+name[x]+'.csh','w')
		fsub.write('#!/bin/csh'+ cr)
		fsub.write('cd ' + mdir+ cr)
		fsub.write('eval `scramv1 runtime -csh`'+ cr)
		fsub.write('cd -'+ cr)
		fsub.write('cp '+mdir+'/CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+ '.cfg . '+ cr)
		fsub.write('SUBCOMMAND'+'\n')
		fsub.close()
		
		## Estimate the r values with Asymptotic CLs
		EstimationInformation = [' r < 0.0000']
		rmax = 10000.0
		breaker = False
		ntry = 0 
		while 'r < 0.0000' in str(EstimationInformation):
			ntry += 1
			EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg --rMax '+str(rmax)).readlines()
			if breaker ==True:
				break
			if 'r < 0.0000' not in str(EstimationInformation):
				effrmax = -999999
				for e in EstimationInformation:
					if 'r <'  in e and 'Expected' in e:
						thisrval = e.split('<')[-1]
						thisrval = thisrval.replace('\n','')
						thisrval = float(thisrval)
						if thisrval>effrmax:
							effrmax = thisrval
				rmax = effrmax*2.0
				EstimationInformation = [' r < 0.0000']
				if ntry>3:
					breaker = True
			# rmax = rmax/5.0
		## Estimation Complete

		
		expectedlines = []
		for line in EstimationInformation:
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

		vstart = round((min(values)/3),5)
		vstop = round((max(values)*3),5)
		rvalues = []
		interval = abs(vstop-vstart)/100.0
		
		nindex = 0
		thisr = 0
		while thisr<vstop:
			thisr = vstart*1.05**(float(nindex))
			rvalues.append(thisr)
			nindex +=1
		strRvalues = []
		for r in rvalues:
			strRvalues.append(str(round(r,5)))
		# print strRvalues
		
		for r in strRvalues:
			command = 'combine '+METHOD.replace('SINGLEPOINT',r).replace('CONFIGURATION','confbetaone_'+cdir+'_'+name[x]+'.cfg')
			strR = r.replace('.','_')
			os.system('cat ShellScriptsForBatch/subbetaone_'+cdir+name[x]+'.csh | sed  \'s/SUBCOMMAND/'+command+'/g\'  > ShellScriptsForBatch/subbetaone_'+strR+'_'+cdir+name[x]+'.csh')
			os.system('chmod 777 ShellScriptsForBatch/subbetaone_'+strR+'_'+cdir+name[x]+'.csh')

			for nn in range(numdo):
				if (dobatch):
					os.system('bsub -o /dev/null -e /dev/null -q '+queue+' -J jobbetaone'+str(nn)+'_R_'+strR+'_'+name[x]+' < ShellScriptsForBatch/subbetaone_'+strR+'_'+cdir+name[x]+'.csh')

if do_BetaHalf == 1:
	masses_betahalf = []
	for x in range(len(name)):
		if 'BetaHalf' not in name[x]:
			continue		
		print 'Calculating limit for: ' + name[x]			
		f = open('CLSLimits/BetaHalf'+cdir+'/confbetahalf_'+cdir+'_'+name[x]+'.cfg','w')
		count = 0
		# print name[x]
		for l in mycards:
			if '.txt' in l and name[x] in l:
				count = 1
				for m in masses:
					if str(m) in l and int(m) not in masses_betahalf:
						masses_betahalf.append(int(m))

				
			if '.txt' in l and name[x] not in l:
				count = 0
			if count ==1 and '.txt' not in l:
				f.write(l+'\n')
					
		f.close()
	
		os.system('mkdir CLSLimits/BetaHalf'+cdir+'/'+name[x])

		mdir = (os.popen('pwd').readlines())[0]
		mdir = mdir.replace('\n','')
		fsub = open('ShellScriptsForBatch/subbetahalf_'+cdir+name[x]+'.csh','w')
		fsub.write('#!/bin/csh'+ cr)
		fsub.write('cd ' + mdir+ cr)
		fsub.write('eval `scramv1 runtime -csh`'+ cr)
		fsub.write('cd -'+ cr)
		fsub.write('cp '+mdir+'/CLSLimits/BetaHalf'+cdir+'/confbetahalf_'+cdir+'_'+name[x]+ '.cfg . '+ cr)
		fsub.write('SUBCOMMAND'+'\n')
		fsub.close()
		
		## Estimate the r values with Asymptotic CLs
		EstimationInformation = [' r < 0.0000']
		rmax = 10000.0
		breaker = False 
		ntry = 0
		while 'r < 0.0000' in str(EstimationInformation):
			ntry += 1
			EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/BetaHalf'+cdir+'/confbetahalf_'+cdir+'_'+name[x]+'.cfg --rMax '+str(rmax)).readlines()
			# print('combine '+ESTIMATIONMETHOD+' CLSLimits/BetaHalf'+cdir+'/confbetahalf_'+cdir+'_'+name[x]+'.cfg --rMax '+str(rmax))
			if breaker ==True:
				break
			if 'r < 0.0000' not in str(EstimationInformation):
				effrmax = -999999
				for e in EstimationInformation:
					if 'r <'  in e and 'Expected' in e:
						thisrval = e.split('<')[-1]
						thisrval = thisrval.replace('\n','')
						thisrval = float(thisrval)
						if thisrval>effrmax:
							effrmax = thisrval
				rmax = effrmax*2.0
				EstimationInformation = [' r < 0.0000']
				if ntry > 3:
					breaker = True
		## Estimation Complete
		
		expectedlines = []
		for line in EstimationInformation:
			if 'Expected' in line and 'r <' in line:
				expectedlines.append(line.replace('\n',''))
		values = []
		for e in expectedlines:
			print e
			values.append(float(e.split()[-1]))

		## Fill the arrays of Asymptotic Values
		for line in EstimationInformation:
			if 'Observed' in line and '<' in line:
				BetaHalfObs.append((line.split('<')[-1]).replace('\n',''))
				print line
			if 'Expected' in line and '<' in line:
				if '2.5%' in line:
					BetaHalf95down.append((line.split('<')[-1]).replace('\n',''))
				if '16.0%' in line:
					BetaHalf68down.append((line.split('<')[-1]).replace('\n',''))
				if '50.0%' in line:
					BetaHalfExp.append((line.split('<')[-1]).replace('\n',''))
				if '84.0%' in line:
					BetaHalf68up.append((line.split('<')[-1]).replace('\n',''))
				if '97.5%' in line:
					BetaHalf95up.append((line.split('<')[-1]).replace('\n',''))
		
		vstart = round((min(values)/3),5)
		vstop = round((max(values)*3),5)
		rvalues = []
		interval = abs(vstop-vstart)/100.0
		
		nindex = 0
		thisr = 0
		while thisr<vstop:
			thisr = vstart*1.05**(float(nindex))
			rvalues.append(thisr)
			nindex += 1
		strRvalues = []
		for r in rvalues:
			strRvalues.append(str(round(r,5)))
		# print strRvalues
		
		for r in strRvalues:
			command = 'combine '+METHOD.replace('SINGLEPOINT',r).replace('CONFIGURATION','confbetahalf_'+cdir+'_'+name[x]+'.cfg')
			strR = r.replace('.','_')
			os.system('cat ShellScriptsForBatch/subbetahalf_'+cdir+name[x]+'.csh | sed  \'s/SUBCOMMAND/'+command+'/g\'  > ShellScriptsForBatch/subbetahalf_'+strR+'_'+cdir+name[x]+'.csh')
			os.system('chmod 777 ShellScriptsForBatch/subbetahalf_'+strR+'_'+cdir+name[x]+'.csh')

			for nn in range(numdo):
				if (dobatch):
					os.system('bsub -o /dev/null -e /dev/null -q '+queue+' -J jobbetahalf'+str(nn)+'_R_'+strR+'_'+name[x]+' < ShellScriptsForBatch/subbetahalf_'+strR+'_'+cdir+name[x]+'.csh')
					
		# sys.exit()
################################################################################################################
################################################################################################################

if do_combo == 1:
	digits = '0123456789'

	cards = []
	cardmasses = []
	cardcontent = []
	card = ''

	flog = open('FinalCards.txt','r')
	os.system('rm -r TMPComboCards/; mkdir TMPComboCards')	
	for line in flog:
		if '.txt' not in line:
			card += line
		if '.txt' in line:
			cardcontent.append(card)
	
			card  = ''
			
			line = line.replace('.txt\n','')
			cards.append(line)
			m = ''
			for x in line:
				if x in digits:
					m+=(x)
			cardmasses.append(m)
			
	cardcontent.append(card)
	
	cardcontent = cardcontent[1:]
	combocards = []
	for x in cardcontent:
		for y in cards:
			if y in x:
				fout = open('combocard_'+y+'.cfg','w')
				x = x.replace('stat_','stat_'+y)
				fout.write(x)
				fout.close()
				combocards.append('combocard_'+y+'.cfg')
	uniquecardmasses = []
	for x in cardmasses:
		if x not in uniquecardmasses:
			uniquecardmasses.append(x)
	for m in uniquecardmasses:
		print 'Printing cards for mass ' +str(m)
		pair = ['','']
		nn = 0
		for x in combocards:
			if m in x:
				pair[nn] = x
				nn += 1
		if 'BetaHalf' in pair[0]:
			bcard = pair[0]
			ocard = pair[1]
		if 'BetaHalf' not in pair[0]:
			bcard = pair[1]
			ocard = pair[0]	

		os.system('combineCards.py '+bcard+ ' '+ocard+ '  > TMPComboCards/combocard_COMBO_M_'+m+'.cfg ' )
		os.system('combineCards.py '+bcard+' > TMPComboCards/combocard_COMBO_BetaHalf_M_'+m+'.cfg ' )
		os.system('combineCards.py '+ocard+' > TMPComboCards/combocard_COMBO_BetaOne_M_'+m+'.cfg ' )
		print pair

	for m in uniquecardmasses:
		combocards.append('TMPComboCards/combocard_COMBO_M_'+m+'.cfg')

	betaind = -1

	for beta in betas:
		betaind += 1
		ComboObs.append([])
		Combo95down.append([])
		Combo68down.append([])
		ComboExp.append([])
		Combo68up.append([])
		Combo95up.append([])

		ComboBetaOneObs.append([])
		ComboBetaOne95down.append([])
		ComboBetaOne68down.append([])
		ComboBetaOneExp.append([])
		ComboBetaOne68up.append([])
		ComboBetaOne95up.append([])
		

		ComboBetaHalfObs.append([])
		ComboBetaHalf95down.append([])
		ComboBetaHalf68down.append([])
		ComboBetaHalfExp.append([])
		ComboBetaHalf68up.append([])
		ComboBetaHalf95up.append([])
						
								
		betaval = str(beta).replace('.','_')
		os.system('mkdir CLSLimits/Combo'+cdir+'/Combo_beta_'+betaval)

		for x in range(len(uniquecardmasses)):	
			print 'Calculating limit for combination mass: ' + str(uniquecardmasses[x]) + ' , beta = '+str(beta)			
			newcard = ('CLSLimits/Combo'+cdir+'/combocard_COMBO_M_'+uniquecardmasses[x]+'.cfg').replace('COMBO','beta_'+betaval+'_COMBO')

			newcard_BetaOne = ('CLSLimits/Combo'+cdir+'/combocard_COMBO_BetaOne_M_'+uniquecardmasses[x]+'.cfg').replace('COMBO_BetaOne','beta_'+betaval+'_COMBO_BetaOne')
			
			newcard_BetaHalf = ('CLSLimits/Combo'+cdir+'/combocard_COMBO_BetaHalf_M_'+uniquecardmasses[x]+'.cfg').replace('COMBO_BetaHalf','beta_'+betaval+'_COMBO_BetaHalf')
			
			ctypes = ['','_BetaOne','_BetaHalf']
			for c in ctypes:
				tcard = newcard
				if 'BetaHalf' in c:
					tcard = newcard_BetaHalf
				if 'BetaOne' in c:
					tcard = newcard_BetaOne
				ftmp = open(tcard,'w')
				fnorm = open('TMPComboCards/combocard_COMBO'+c+'_M_'+str(uniquecardmasses[x])+'.cfg','r')
				
				betahalfplace = 99
				betaoneplace = 99
				for line in fnorm:
	
					if ('LQ' in line and 'process' in line):
						linesplit = line.split()
						for place in range(len(linesplit)):
							if 'LQ' in linesplit[place] and 'BetaHalf' in linesplit[place]:
								betahalfplace = place
							if 'LQ' in linesplit[place] and 'BetaHalf' not in linesplit[place]:
								betaoneplace = place
								
					if ( 'rate' in line):
	
						linesplit = line.split()
						linesplit2 = []
						for place in range(len(linesplit)):
							arg = linesplit[place]
							if betahalfplace == place:
								arg = str(float(arg)*beta*(1.0-beta)*4.0)
							
							if betaoneplace == place:						
								arg = str(float(arg)*beta*beta)
							linesplit2.append(arg)
						line2 = ''
						for xpart in linesplit2:
							line2 += xpart + '    '
						line2 += '\n'
						line = line2
					if  'stat' in line and 'Signal' in line and 'gmN' in line:
						linesplit = line.split()
						print linesplit
						for nsp in range(len(linesplit)):
							if 'BetaHalf' not in line and nsp == betaoneplace+1:
								repsold =  str(linesplit[nsp+1])
								repsnew = str(float(repsold)*beta*beta)
								line = line.replace(repsold,repsnew)
							if 'BetaHalf' in line and nsp == betahalfplace+1:
								repsold =  str(linesplit[nsp+1])
								repsnew = str(float(repsold)*beta*(1.0-beta)*4.0)
								line = line.replace(repsold,repsnew)
					ftmp.write(line)
				ftmp.close()
		
			thisname ='beta_'+ betaval + '_M_'+str(uniquecardmasses[x])
			mdir = (os.popen('pwd').readlines())[0]
			mdir = mdir.replace('\n','')
			fsub = open('ShellScriptsForBatch/subcombo_'+cdir+thisname+'.csh','w')
			fsub.write('#!/bin/csh'+ cr)
			fsub.write('cd ' + mdir+ cr)
			fsub.write('eval `scramv1 runtime -csh`'+ cr)
			fsub.write('cd -'+ cr)
			fsub.write('cp '+mdir+'/'+newcard+' .'+ cr)
			fsub.write('cp '+mdir+'/'+newcard_BetaOne+' .'+ cr)
			fsub.write('cp '+mdir+'/'+newcard_BetaHalf+' .'+ cr)

			fsub.write('SUBCOMMAND0'+'\n')
			fsub.write('mv higgs*root Combo_'+thisname+'_R_RVALUE0_ind_`bash -c \'echo $RANDOM\'`.root \n')			
			fsub.write('SUBCOMMAND1'+'\n')
			fsub.write('mv higgs*root ComboBetaOne_'+thisname+'_R_RVALUE1_ind_`bash -c \'echo $RANDOM\'`.root \n')			
			fsub.write('SUBCOMMAND2'+'\n')
			fsub.write('mv higgs*root ComboBetaHalf_'+thisname+'_R_RVALUE2_ind_`bash -c \'echo $RANDOM\'`.root \n')						
			fsub.close()
			
			## Estimate the r values with Asymptotic CLs
			EstimationInformation0 = [' r < 0.0000']
			rmax = 10000.0
			breaker = False 
			ntry = 0
			while 'r < 0.0000' in str(EstimationInformation0):
				ntry += 1
				print 'combine '+ESTIMATIONMETHOD+' '+newcard +' --rMax '+str(rmax)
				EstimationInformation0 = os.popen('combine '+ESTIMATIONMETHOD+' '+newcard +' --rMax '+str(rmax)).readlines()
				
				if breaker ==True:
					break
				if 'r < 0.0000' not in str(EstimationInformation0):
					effrmax = -999999
					for e in EstimationInformation0:
						if 'r <'  in e and 'Expected' in e:
							thisrval = e.split('<')[-1]
							thisrval = thisrval.replace('\n','')
							thisrval = float(thisrval)
							if thisrval>effrmax:
								effrmax = thisrval
					rmax = effrmax*2.0
					EstimationInformation0 = [' r < 0.0000']
					if ntry > 3:
						breaker = True


			EstimationInformation1 = [' r < 0.0000']
			rmax = 10000.0
			breaker = False 
			ntry = 0

			while 'r < 0.0000' in str(EstimationInformation1):
				ntry += 1				
				print 'combine '+ESTIMATIONMETHOD+' '+newcard_BetaOne +' --rMax '+str(rmax)
				EstimationInformation1 = os.popen('combine '+ESTIMATIONMETHOD+' '+newcard_BetaOne +' --rMax '+str(rmax)).readlines()
				
				if breaker ==True:
					break
				if 'r < 0.0000' not in str(EstimationInformation1):
					effrmax = -999999
					for e in EstimationInformation1:
						if 'r <'  in e and 'Expected' in e:
							thisrval = e.split('<')[-1]
							thisrval = thisrval.replace('\n','')
							thisrval = float(thisrval)
							if thisrval>effrmax:
								effrmax = thisrval
					rmax = effrmax*2.0
					EstimationInformation1 = [' r < 0.0000']
					if ntry > 3:
						breaker = True
				
			EstimationInformation2 = [' r < 0.0000']
			rmax = 10000.0
			breaker = False 
			ntry = 0

			while 'r < 0.0000' in str(EstimationInformation2):
				ntry += 1
				print 'combine '+ESTIMATIONMETHOD+' '+newcard_BetaHalf +' --rMax '+str(rmax)
				EstimationInformation2 = os.popen('combine '+ESTIMATIONMETHOD+' '+newcard_BetaHalf +' --rMax '+str(rmax)).readlines()
				
				if breaker ==True:
					break
				if 'r < 0.0000' not in str(EstimationInformation2):
					effrmax = -999999
					for e in EstimationInformation2:
						if 'r <'  in e and 'Expected' in e:
							thisrval = e.split('<')[-1]
							thisrval = thisrval.replace('\n','')
							thisrval = float(thisrval)
							if thisrval>effrmax:
								effrmax = thisrval
					rmax = effrmax*2.0
					EstimationInformation2 = [' r < 0.0000']
					if ntry > 3:
						breaker = True
			
			expectedlines0 = []
			for line in EstimationInformation0:
				if 'Expected' in line and 'r <' in line:
					expectedlines0.append(line.replace('\n',''))
			values0 = []
			for e in expectedlines0:
				print e
				values0.append(float(e.split()[-1]))


			expectedlines1 = []
			for line in EstimationInformation1:
				if 'Expected' in line and 'r <' in line:
					expectedlines1.append(line.replace('\n',''))
			values1 = []
			for e in expectedlines1:
				print e
				values1.append(float(e.split()[-1]))
				
				
			expectedlines2 = []
			for line in EstimationInformation2:
				if 'Expected' in line and 'r <' in line:
					expectedlines2.append(line.replace('\n',''))
			values2 = []
			for e in expectedlines2:
				print e
				values2.append(float(e.split()[-1]))				

			## Estimation Complete


			## Fill the arrays of Asymptotic Values
			for line in EstimationInformation0:
				if 'Observed' in line and '<' in line:
					ComboObs[betaind].append((line.split('<')[-1]).replace('\n',''))
				if 'Expected' in line and '<' in line:
					if '2.5%' in line:
						Combo95down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '16.0%' in line:
						Combo68down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '50.0%' in line:
						ComboExp[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '84.0%' in line:
						Combo68up[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '97.5%' in line:
						Combo95up[betaind].append((line.split('<')[-1]).replace('\n',''))

			for line in EstimationInformation1:
				if 'Observed' in line and '<' in line:
					ComboBetaOneObs[betaind].append((line.split('<')[-1]).replace('\n',''))
				if 'Expected' in line and '<' in line:
					if '2.5%' in line:
						ComboBetaOne95down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '16.0%' in line:
						ComboBetaOne68down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '50.0%' in line:
						ComboBetaOneExp[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '84.0%' in line:
						ComboBetaOne68up[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '97.5%' in line:
						ComboBetaOne95up[betaind].append((line.split('<')[-1]).replace('\n',''))

			for line in EstimationInformation2:
				if 'Observed' in line and '<' in line:
					ComboBetaHalfObs[betaind].append((line.split('<')[-1]).replace('\n',''))
				if 'Expected' in line and '<' in line:
					if '2.5%' in line:
						ComboBetaHalf95down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '16.0%' in line:
						ComboBetaHalf68down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '50.0%' in line:
						ComboBetaHalfExp[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '84.0%' in line:
						ComboBetaHalf68up[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '97.5%' in line:
						ComboBetaHalf95up[betaind].append((line.split('<')[-1]).replace('\n',''))
			
			## Asymptotic Information Filled
			
			
			vstart0 = round((min(values0)/2),5)
			vstop0 = round((max(values0)*2),5)
			rvalues0 = []


			vstart1 = round((min(values1)/2),5)
			vstop1 = round((max(values1)*2),5)
			rvalues1 = []
			
			vstart2 = round((min(values2)/2),5)
			vstop2 = round((max(values2)*2),5)
			rvalues2 = []			
			
			nindex0 = 0
			thisr0 = 0

			nindex1 = 0
			thisr1= 0
			
			nindex2 = 0
			thisr2 = 0
			
			print 'vstop0 '+str(vstop0) + '   vstart0  '+str(vstart0)
			print 'vstop1 '+str(vstop1) + '   vstart1  '+str(vstart1)
			print 'vstop2 '+str(vstop2) + '   vstart2  '+str(vstart2)

			expinc0 = 0.9999*(2.718281828**((0.0666666666667*(math.log(vstop0/vstart0)))))
			expinc1 = 0.9999*(2.718281828**((0.0666666666667*(math.log(vstop1/vstart1)))))
			expinc2 = 0.9999*(2.718281828**((0.0666666666667*(math.log(vstop2/vstart2)))))
			
			
			while thisr0<vstop0:
				thisr0 = vstart0*expinc0**(float(nindex0))
				rvalues0.append(thisr0)
				nindex0 += 1
			strRvalues0 = []
			for r in rvalues0:
				strRvalues0.append(str(round(r,5)))
			#print strRvalues0


			while thisr1<vstop1:
				thisr1 = vstart1*expinc1**(float(nindex1))
				rvalues1.append(thisr1)
				nindex1 += 1
			strRvalues1 = []
			for r in rvalues1:
				strRvalues1.append(str(round(r,5)))
			#print strRvalues1

			while thisr2<vstop2:
				thisr2 = vstart2*expinc2**(float(nindex2))
				rvalues2.append(thisr2)
				nindex2 += 1
			strRvalues2 = []
			for r in rvalues2:
				strRvalues2.append(str(round(r,5)))
			#print strRvalues2
			

			
			for rind in range(len(strRvalues0)):
				r0 = strRvalues0[rind]
				r1 = strRvalues1[rind]
				r2 = strRvalues2[rind]

				command0 = 'combine '+METHOD.replace('SINGLEPOINT',r0).replace('CONFIGURATION',newcard.split('/')[-1])
				command1 = 'combine '+METHOD.replace('SINGLEPOINT',r1).replace('CONFIGURATION',newcard_BetaOne.split('/')[-1])
				command2 = 'combine '+METHOD.replace('SINGLEPOINT',r2).replace('CONFIGURATION',newcard_BetaHalf.split('/')[-1])

				strR0 = r0.replace('.','_')
				strR1 = r1.replace('.','_')
				strR2 = r2.replace('.','_')

				os.system('cat ShellScriptsForBatch/subcombo_'+cdir+thisname+'.csh | sed  \'s/SUBCOMMAND0/'+command0+'/g\' | sed  \'s/RVALUE0/'+strR0+'/g\' | sed  \'s/SUBCOMMAND1/'+command1+'/g\' | sed  \'s/RVALUE1/'+strR1+'/g\' | sed  \'s/SUBCOMMAND2/'+command2+'/g\' | sed  \'s/RVALUE2/'+strR2+'/g\' > ShellScriptsForBatch/subcombo_R_'+str(rind)+'_'+cdir+thisname+'.csh')
				os.system('chmod 777 ShellScriptsForBatch/subcombo_R_'+str(rind)+'_'+cdir+thisname+'.csh')
	
				for nn in range(numdo):
					if (dobatch):
						os.system('bsub -o /dev/null -e /dev/null -q '+queue+' -J jobcombo'+str(nn)+'_R_'+str(rind)+'_'+thisname+' < ShellScriptsForBatch/subcombo_R_'+str(rind)+'_'+cdir+thisname+'.csh')


################################################################################################################
################################################################################################################






os.system('rm higgsCombineTest*root')

print '\n\n\n'

#### ASYMPTOTIC CLS PRINTOUT ###


mTh = [ 0.200E+03,0.210E+03,0.220E+03,0.230E+03,0.240E+03,0.250E+03,0.260E+03,0.270E+03,0.290E+03,0.300E+03,0.310E+03,0.320E+03,0.330E+03,0.340E+03,0.350E+03,0.360E+03,0.370E+03,0.380E+03,0.390E+03,0.400E+03,0.410E+03,0.420E+03,0.430E+03,0.440E+03,0.450E+03,0.460E+03,0.470E+03,0.480E+03,0.490E+03,0.500E+03,0.510E+03,0.520E+03,0.530E+03,0.540E+03,0.550E+03,0.560E+03,0.570E+03,0.580E+03,0.590E+03,0.600E+03,0.610E+03,0.620E+03,0.630E+03,0.640E+03,0.650E+03,0.660E+03,0.670E+03,0.680E+03,0.690E+03,0.700E+03,0.710E+03,0.720E+03,0.730E+03,0.740E+03,0.750E+03,0.760E+03,0.770E+03,0.780E+03,0.790E+03,0.800E+03,0.810E+03,0.820E+03,0.830E+03,0.840E+03,0.850E+03,0.860E+03,0.870E+03,0.880E+03,0.890E+03,0.900E+03,0.910E+03,0.920E+03,0.930E+03,0.940E+03,0.950E+03,0.960E+03,0.970E+03,0.980E+03,0.990E+03,0.100E+04,0.101E+04,0.102E+04,0.103E+04,0.104E+04,0.105E+04,0.106E+04,0.107E+04,0.108E+04,0.109E+04,0.110E+04,0.111E+04,0.112E+04,0.113E+04,0.114E+04,0.115E+04,0.116E+04,0.117E+04,0.118E+04,0.119E+04,0.120E+04,0.121E+04,0.122E+04,0.123E+04,0.124E+04,0.125E+04,0.126E+04,0.127E+04,0.128E+04,0.129E+04,0.130E+04,0.131E+04,0.132E+04,0.133E+04,0.134E+04,0.135E+04,0.136E+04,0.137E+04,0.138E+04,0.139E+04,0.140E+04,0.141E+04,0.142E+04,0.143E+04,0.144E+04,0.145E+04,0.146E+04,0.147E+04,0.148E+04,0.149E+04,0.150E+04,0.151E+04,0.152E+04,0.153E+04,0.154E+04,0.155E+04,0.156E+04,0.157E+04,0.158E+04,0.159E+04,0.160E+04,0.161E+04,0.162E+04,0.163E+04,0.164E+04,0.165E+04,0.166E+04,0.167E+04,0.168E+04,0.169E+04,0.170E+04,0.171E+04,0.172E+04,0.173E+04,0.174E+04,0.175E+04,0.176E+04,0.177E+04,0.178E+04,0.179E+04,0.180E+04,0.181E+04,0.182E+04,0.183E+04,0.184E+04,0.185E+04,0.186E+04,0.187E+04,0.188E+04,0.189E+04,0.190E+04,0.191E+04,0.192E+04,0.193E+04,0.194E+04,0.195E+04,0.196E+04,0.197E+04,0.198E+04,0.199E+04,0.200E+04,0.201E+04,0.202E+04,0.203E+04,0.204E+04,0.205E+04,0.206E+04,0.207E+04,0.208E+04,0.209E+04,0.210E+04,0.211E+04,0.212E+04,0.213E+04,0.214E+04,0.215E+04,0.216E+04,0.217E+04,0.218E+04,0.219E+04,0.220E+04,0.221E+04,0.222E+04,0.223E+04,0.224E+04,0.225E+04,0.226E+04,0.227E+04,0.228E+04,0.229E+04,0.230E+04,0.231E+04,0.232E+04,0.233E+04,0.234E+04,0.235E+04,0.236E+04,0.237E+04,0.238E+04,0.239E+04,0.240E+04,0.241E+04,0.242E+04,0.243E+04,0.244E+04,0.245E+04,0.246E+04,0.247E+04,0.248E+04,0.249E+04,0.250E+04,0.251E+04,0.252E+04,0.253E+04,0.254E+04,0.255E+04,0.256E+04,0.257E+04,0.258E+04,0.259E+04,0.260E+04,0.261E+04,0.262E+04,0.263E+04,0.264E+04,0.265E+04,0.266E+04,0.267E+04,0.268E+04,0.269E+04,0.270E+04,0.271E+04,0.272E+04,0.273E+04,0.274E+04,0.275E+04,0.276E+04,0.277E+04,0.278E+04,0.279E+04,0.280E+04,0.281E+04,0.282E+04,0.283E+04,0.284E+04,0.285E+04,0.286E+04,0.287E+04,0.288E+04,0.289E+04,0.290E+04,0.291E+04,0.292E+04,0.293E+04,0.294E+04,0.295E+04,0.296E+04,0.297E+04,0.298E+04,0.299E+04 ]
xsTh = [ 0.174E+02,0.134E+02,0.105E+02,0.827E+01,0.657E+01,0.526E+01,0.424E+01,0.344E+01,0.230E+01,0.189E+01,0.157E+01,0.130E+01,0.109E+01,0.914E+00,0.770E+00,0.650E+00,0.551E+00,0.469E+00,0.400E+00,0.342E+00,0.294E+00,0.253E+00,0.218E+00,0.188E+00,0.163E+00,0.142E+00,0.123E+00,0.107E+00,0.937E-01,0.820E-01,0.719E-01,0.631E-01,0.555E-01,0.489E-01,0.431E-01,0.381E-01,0.337E-01,0.298E-01,0.265E-01,0.235E-01,0.209E-01,0.186E-01,0.166E-01,0.148E-01,0.132E-01,0.118E-01,0.106E-01,0.946E-02,0.848E-02,0.761E-02,0.683E-02,0.614E-02,0.552E-02,0.497E-02,0.448E-02,0.404E-02,0.364E-02,0.329E-02,0.297E-02,0.269E-02,0.243E-02,0.220E-02,0.199E-02,0.181E-02,0.164E-02,0.149E-02,0.135E-02,0.123E-02,0.111E-02,0.101E-02,0.922E-03,0.839E-03,0.764E-03,0.696E-03,0.634E-03,0.578E-03,0.527E-03,0.481E-03,0.439E-03,0.401E-03,0.366E-03,0.335E-03,0.306E-03,0.280E-03,0.256E-03,0.234E-03,0.214E-03,0.196E-03,0.180E-03,0.165E-03,0.151E-03,0.138E-03,0.127E-03,0.116E-03,0.107E-03,0.980E-04,0.899E-04,0.825E-04,0.758E-04,0.696E-04,0.639E-04,0.587E-04,0.540E-04,0.496E-04,0.456E-04,0.419E-04,0.385E-04,0.355E-04,0.326E-04,0.300E-04,0.276E-04,0.254E-04,0.234E-04,0.215E-04,0.198E-04,0.182E-04,0.168E-04,0.155E-04,0.142E-04,0.131E-04,0.121E-04,0.111E-04,0.103E-04,0.945E-05,0.871E-05,0.802E-05,0.740E-05,0.682E-05,0.628E-05,0.579E-05,0.534E-05,0.492E-05,0.454E-05,0.418E-05,0.385E-05,0.355E-05,0.328E-05,0.302E-05,0.278E-05,0.257E-05,0.237E-05,0.218E-05,0.201E-05,0.186E-05,0.171E-05,0.158E-05,0.145E-05,0.134E-05,0.124E-05,0.114E-05,0.105E-05,0.968E-06,0.893E-06,0.823E-06,0.758E-06,0.699E-06,0.644E-06,0.594E-06,0.547E-06,0.504E-06,0.465E-06,0.428E-06,0.394E-06,0.363E-06,0.335E-06,0.308E-06,0.284E-06,0.261E-06,0.241E-06,0.222E-06,0.204E-06,0.188E-06,0.173E-06,0.159E-06,0.147E-06,0.135E-06,0.124E-06,0.114E-06,0.105E-06,0.965E-07,0.888E-07,0.816E-07,0.750E-07,0.690E-07,0.634E-07,0.583E-07,0.535E-07,0.492E-07,0.452E-07,0.415E-07,0.381E-07,0.349E-07,0.321E-07,0.294E-07,0.270E-07,0.248E-07,0.227E-07,0.208E-07,0.191E-07,0.175E-07,0.160E-07,0.147E-07,0.134E-07,0.123E-07,0.113E-07,0.103E-07,0.943E-08,0.862E-08,0.788E-08,0.720E-08,0.658E-08,0.601E-08,0.549E-08,0.501E-08,0.457E-08,0.417E-08,0.381E-08,0.347E-08,0.316E-08,0.288E-08,0.262E-08,0.239E-08,0.217E-08,0.198E-08,0.180E-08,0.163E-08,0.148E-08,0.135E-08,0.122E-08,0.111E-08,0.101E-08,0.913E-09,0.827E-09,0.749E-09,0.678E-09,0.614E-09,0.555E-09,0.502E-09,0.453E-09,0.409E-09,0.369E-09,0.333E-09,0.300E-09,0.270E-09,0.243E-09,0.219E-09,0.197E-09,0.177E-09,0.159E-09,0.143E-09,0.128E-09,0.115E-09,0.103E-09,0.919E-10,0.821E-10,0.734E-10,0.655E-10,0.585E-10,0.521E-10,0.464E-10,0.413E-10,0.368E-10,0.327E-10,0.290E-10,0.257E-10,0.228E-10,0.202E-10,0.178E-10,0.158E-10,0.139E-10,0.123E-10,0.108E-10,0.950E-11,0.835E-11,0.733E-11,0.643E-11,0.563E-11,0.493E-11,0.431E-11 ]



#### BETA ONE CHANNEL
if do_BetaOne == 1:


	masses = masses_betaone
	print "*"*40 + '\n BETA ONE ASYMPTOTIC CLS RESULTS\n\n' +"*"*40
	
	band1sigma = 'Double_t y_1sigma['+str(int(len(masses)*2))+']={'
	band2sigma = 'Double_t y_2sigma['+str(int(len(masses)*2))+']={'
	excurve = 'Double_t xsUp_expected['+str(int(len(masses)))+'] = {' 
	obcurve = 'Double_t xsUp_observed['+str(int(len(masses)))+'] = {'  
 	mcurve = 'Double_t mData['+str(int(len(masses)))+'] = {'  
 	scurve = 'Double_t x_shademasses['+str(int(len(masses)*2))+'] = {'  
	
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
		band2sigma += str(float(down2[x])*float(sigma[x])) + ' , ' 
		mcurve += str(float(masses[x])) + ' , '
		scurve += str(float(masses[x])) + ' , '

	for x in range(len(masses)):
		band1sigma += str(float(up1[-(x+1)])*float(sigma[-(x+1)])) + ' , ' 
		band2sigma += str(float(up2[-(x+1)])*float(sigma[-(x+1)])) + ' , ' 
		scurve += str(float(masses[-x-1])) + ' , '
	excurve += '}'
	obcurve += '}'
	mcurve += '}'
	scurve += '}'
	band1sigma += '}'
	band2sigma += '}'
	excurve = excurve.replace(' , }',' }; ' )
	obcurve = obcurve.replace(' , }',' }; ' )
	mcurve = mcurve.replace(' , }',' }; ' )
	scurve = scurve.replace(' , }',' }; ' )

	band1sigma = band1sigma.replace(' , }',' }; ' )
	band2sigma = band2sigma.replace(' , }',' }; ' )
	
	print '\n'
	print mcurve
	print scurve
	print excurve
	print obcurve
	print band1sigma
	print band2sigma
	print '\n'

#### BETA HALF CHANNEL
if do_BetaHalf == 1:

	masses = masses_betahalf
	print "*"*40 + '\n BETA HALF ASYMPTOTIC CLS RESULTS\n' +"*"*40
	
	band1sigma = 'Double_t y_1sigma['+str(int(len(masses)*2))+']={'
	band2sigma = 'Double_t y_2sigma['+str(int(len(masses)*2))+']={'
	excurve = 'Double_t xsUp_expected['+str(int(len(masses)))+'] = {' 
	obcurve = 'Double_t xsUp_observed['+str(int(len(masses)))+'] = {'  
 	mcurve = 'Double_t mData['+str(int(len(masses)))+'] = {'  
 	scurve = 'Double_t x_shademasses['+str(int(len(masses)*2))+'] = {'  

	
	ob = BetaHalfObs 
	down2 = BetaHalf95down 
	up2 = BetaHalf95up 
	down1 = BetaHalf68down 
	up1 = BetaHalf68up 
	med = BetaHalfExp 

	fac = 0.5
	sigma = []
	for x in range(len(mTh)):
		if (mTh[x]) in masses: 
			sigma.append(xsTh[x]*fac)
			# print '*',mTh[x],xsTh[x]
	
	for x in range(len(masses)):
		excurve += str(float(med[x])*float(sigma[x])) + ' , ' 
		obcurve += str(float(ob[x])*float(sigma[x])) + ' , ' 
		band1sigma += str(float(down1[x])*float(sigma[x])) + ' , ' 
		band2sigma += str(float(down2[x])*float(sigma[x])) + ' , ' 
		mcurve += str(float(masses[x])) + ' , '
		scurve += str(float(masses[x])) + ' , '
	
	for x in range(len(masses)):
		band1sigma += str(float(up1[-(x+1)])*float(sigma[-(x+1)])) + ' , ' 
		band2sigma += str(float(up2[-(x+1)])*float(sigma[-(x+1)])) + ' , ' 
		scurve += str(float(masses[-x-1])) + ' , '

	excurve += '}'
	obcurve += '}'
	mcurve += '}'
	scurve += '}'		
	band1sigma += '}'
	band2sigma += '}'
	excurve = excurve.replace(' , }',' }; ' )
	obcurve = obcurve.replace(' , }',' }; ' )
	mcurve = mcurve.replace(' , }',' }; ' )	
	scurve = scurve.replace(' , }',' }; ' )	
	band1sigma = band1sigma.replace(' , }',' }; ' )
	band2sigma = band2sigma.replace(' , }',' }; ' )
	

	print '\n'
	print mcurve
	print scurve	
	print excurve
	print obcurve
	print band1sigma
	print band2sigma
	print '\n'
	


#### COMBINATION CHANNEL
if do_combo == 1:

	print "*"*40 + '\n COMBINATION ASYMPTOTIC CLS RESULTS\n' +"*"*40

					

	sigma = []
	fac = 1.0
	for x in range(len(mTh)):
		if (mTh[x]) in masses: 
			sigma.append(xsTh[x]*fac)
	
	def re_eval(rlist):
		outlist = []
		for mset in rlist:
			newset = []
			for r_ind in range(len(mset)):
				newset.append(sigma[r_ind]*float(mset[r_ind]))		
			outlist.append(newset)
		return outlist
	
	s_ComboObs = re_eval(ComboObs)
	s_Combo95down = re_eval(Combo95down)
	s_Combo68down = re_eval(Combo68down)
	s_ComboExp = re_eval(ComboExp)
	s_Combo68up = re_eval(Combo68up)
	s_Combo95up = re_eval(Combo95up)
	
	s_ComboBetaOneObs = re_eval(ComboBetaOneObs)
	s_ComboBetaOne95down = re_eval(ComboBetaOne95down)
	s_ComboBetaOne68down = re_eval(ComboBetaOne68down)
	s_ComboBetaOneExp = re_eval(ComboBetaOneExp)
	s_ComboBetaOne68up = re_eval(ComboBetaOne68up)
	s_ComboBetaOne95up = re_eval(ComboBetaOne95up)
	
	s_ComboBetaHalfObs = re_eval(ComboBetaHalfObs)
	s_ComboBetaHalf95down = re_eval(ComboBetaHalf95down)
	s_ComboBetaHalf68down = re_eval(ComboBetaHalf68down)
	s_ComboBetaHalfExp = re_eval(ComboBetaHalfExp)
	s_ComboBetaHalf68up = re_eval(ComboBetaHalf68up)
	s_ComboBetaHalf95up = re_eval(ComboBetaHalf95up)


	from ROOT import *
	from array import array
		

	#xx = (spline.Eval(310));
	M_th=[ xm for xm in mTh]
	X_th=[ xx for xx in xsTh]
		
	mTh = array("d",mTh)
	xsTh = array("d",xsTh)
	

	g = TGraph(len(mTh),mTh,xsTh);
	spline = TSpline3("xsection",g) 
	
		
	def sigmaval(mval):
		return spline.Eval(mval)
		
	
	def mval(sigma):
		testm = 150
		oldtestm = 1300
		inc = 50
		dif = 55
		olddif = 000
		while abs(oldtestm - testm)>0.01:
			testsigma = sigmaval(testm)
			olddif = dif
			dif = testsigma -sigma
			if testm>1200:
				break
			if dif*olddif <= 0.0:
				inc = -inc/2.3
			oldtestm = testm
			#print '**' + str(testm) + '  ' + str(testsigma) +'  ' +str(dif) + '   ' + str(dif*olddif)
	
			testm = testm + inc
		return testm
	import math
	inputarrayX = []
	inputarrayY = []

	def loggraph(inputarrayX,inputarrayY):
		logarray = []
		for j in inputarrayY:
			logarray.append(math.log10(j))
		x = array("d",inputarrayX)
		y = array("d",logarray)
		g = TGraph(len(x),x,y)
		return g
		
	logtheory = loggraph(M_th,X_th)

	def logspline(inputarrayX,inputarrayY):
		logarray = []
		for j in inputarrayY:
			logarray.append(math.log(j))
		x = array("d",inputarrayX)
		y = array("d",logarray)
		g = TGraph(len(x),x,y)
		outspline = TSpline3("",g)
		return outspline
	
	from math import exp
	def get_intersection(spline1, spline2, xmin,xmax):
		num = xmax-xmin
		inc = (xmax - xmin)/num
		dif = []
		sdif = []
		x = xmin
		xvals = []
		xx = []
		yy = []
		xvals = []
		while x<xmax:
			thisdif = (exp(spline1.Eval(x)) - exp(spline2.Eval(x)))
			#print (str(x)) + '   ' + str(thisdif)
			xx.append(exp(spline1.Eval(x)))
			yy.append(exp(spline2.Eval(x)))
			sdif.append(thisdif)
			dif.append(abs(thisdif))
			xvals.append(x)
			#print  str(x) + '   ' +str(exp(spline1.Eval(x))) + '    '+str(exp(spline2.Eval(x))) + '    ' + str(thisdif)
			x = x+inc
		mindif = min(dif)
		bestmass = 0	
		
	
		for x in range(len(dif)-2):
			a = sdif[x]
			b = sdif[x+1]	
			#print str(xvals[x+1]) +'    '+str(a)  + '     ' +str(b) 
			if ((a/abs(a))*(b/abs(b))) < 0.0 and a >0.0 :
				#print 'Limit found at: '+ (str(xvals[x]))
				bestmass = xvals[x]
				break;
						
		return [bestmass,mindif]
		
	def get_simple_intersection(graph1, graph2, xmin,xmax):
		num = (xmax-xmin)*10
		inc = (xmax - xmin)/(1.0*num)

		dif = []
		sdif = []
		x = xmin +0.1
		xvals = []
		xx = []
		yy = []
		xvals = []
		while x<(xmax-.1):
			thisdif = (exp(graph1.Eval(x)) - exp(graph2.Eval(x)))
			#print (str(x)) + '   '+ str(xmax-.1) +'   '+ str(thisdif)
			xx.append(exp(graph1.Eval(x)))
			yy.append(exp(graph2.Eval(x)))
			sdif.append(thisdif)
			dif.append(abs(thisdif))
			xvals.append(x)
			#print  str(x) + '   ' +str(exp(graph1.Eval(x))) + '    '+str(exp(graph2.Eval(x))) + '    ' + str(thisdif)
			x = x+inc
		#print 'Done Looping for Difs'
		mindif = min(dif)
		bestmass = 0	
		
	
		for x in range(len(dif)-2):
			a = sdif[x]
			b = sdif[x+1]	
			#print str(xvals[x+1]) +'    '+str(a)  + '     ' +str(b) 
			if ((a/abs(a))*(b/abs(b))) < 0.0 and a >0.0 :
				print 'Limit found at: '+ (str(xvals[x]))
				bestmass = xvals[x]
				break;
						
		return [bestmass,mindif]
		


	def fill_mlists(clist):
		mlist = []
		for limit_set in clist:
			fitted_limits = loggraph(masses,limit_set)
			goodm = get_simple_intersection(logtheory,fitted_limits,300,1300)
			mlist.append(str(round(goodm[0],2)))
		return mlist
		
	m_ComboObs = fill_mlists(s_ComboObs)
	m_Combo95down = fill_mlists(s_Combo95down)
	m_Combo68down = fill_mlists(s_Combo68down)
	m_ComboExp = fill_mlists(s_ComboExp)
	m_Combo68up = fill_mlists(s_Combo68up)
	m_Combo95up = fill_mlists(s_Combo95up)

	m_ComboBetaOneObs = fill_mlists(s_ComboBetaOneObs)
	m_ComboBetaOne95down = fill_mlists(s_ComboBetaOne95down)
	m_ComboBetaOne68down = fill_mlists(s_ComboBetaOne68down)
	m_ComboBetaOneExp = fill_mlists(s_ComboBetaOneExp)
	m_ComboBetaOne68up = fill_mlists(s_ComboBetaOne68up)
	m_ComboBetaOne95up = fill_mlists(s_ComboBetaOne95up)

	m_ComboBetaHalfObs = fill_mlists(s_ComboBetaHalfObs)
	m_ComboBetaHalf95down = fill_mlists(s_ComboBetaHalf95down)
	m_ComboBetaHalf68down = fill_mlists(s_ComboBetaHalf68down)
	m_ComboBetaHalfExp = fill_mlists(s_ComboBetaHalfExp)
	m_ComboBetaHalf68up = fill_mlists(s_ComboBetaHalf68up)
	m_ComboBetaHalf95up = fill_mlists(s_ComboBetaHalf95up)
	
	
	betav = []
	for x in betas:
		betav.append(str(round(x,4)))
	betastring = 'static int numbetas = '+str(len(betas))+';\n'+'Double_t beta_vals['+str(len(betas))+'] = {' +str(betav).replace('[','').replace(']','').replace('\'','')+'};'

	band1sigma_combo = 'Double_t m_1sigma_combo['+str(2*len(betas))+']={'
	band2sigma_combo = 'Double_t m_2sigma_combo['+str(2*len(betas))+']={'
	excurve_combo = 'Double_t m_expected_combo['+str(len(betas))+'] = {' 
	obcurve_combo = 'Double_t m_observed_combo['+str(len(betas))+'] = {'  

	band1sigma_lljj = 'Double_t m_1sigma_lljj['+str(2*len(betas))+']={'
	band2sigma_lljj = 'Double_t m_2sigma_lljj['+str(2*len(betas))+']={'
	excurve_lljj = 'Double_t m_expected_lljj['+str(len(betas))+'] = {' 
	obcurve_lljj = 'Double_t m_observed_lljj['+str(len(betas))+'] = {'  
	
	band1sigma_lvjj = 'Double_t m_1sigma_lvjj['+str(2*len(betas))+']={'
	band2sigma_lvjj = 'Double_t m_2sigma_lvjj['+str(2*len(betas))+']={'
	excurve_lvjj = 'Double_t m_expected_lvjj['+str(len(betas))+'] = {' 
	obcurve_lvjj = 'Double_t m_observed_lvjj['+str(len(betas))+'] = {'  
	
	
	excurve_combo += str(m_ComboExp).replace('[','').replace(']','').replace('\'','')+'};'
	obcurve_combo += str(m_ComboObs).replace('[','').replace(']','').replace('\'','')+'};'

	excurve_lljj += str(m_ComboBetaOneExp).replace('[','').replace(']','').replace('\'','')+'};'
	obcurve_lljj += str(m_ComboBetaOneObs).replace('[','').replace(']','').replace('\'','')+'};'
	
	excurve_lvjj += str(m_ComboBetaHalfExp).replace('[','').replace(']','').replace('\'','')+'};'
	obcurve_lvjj += str(m_ComboBetaHalfObs).replace('[','').replace(']','').replace('\'','')+'};'	

	m_Combo68up.reverse()
	m_Combo95up.reverse()

	m_ComboBetaOne68up.reverse()
	m_ComboBetaOne95up.reverse()
	
	m_ComboBetaHalf68up.reverse()
	m_ComboBetaHalf95up.reverse()
	
		
	band1sigma_combo += str(m_Combo68down).replace('[','').replace(']','').replace('\'','')+ ', '+  str(m_Combo68up).replace('[','').replace(']','').replace('\'','')+'};'
	band2sigma_combo += str(m_Combo95down).replace('[','').replace(']','').replace('\'','') + ', '+ str(m_Combo95up).replace('[','').replace(']','').replace('\'','')+'};'

	band1sigma_lljj += str(m_ComboBetaOne68down).replace('[','').replace(']','').replace('\'','') + ', '+  str(m_ComboBetaOne68up).replace('[','').replace(']','').replace('\'','')+'};'
	band2sigma_lljj += str(m_ComboBetaOne95down).replace('[','').replace(']','').replace('\'','') + ', '+ str(m_ComboBetaOne95up).replace('[','').replace(']','').replace('\'','')+'};'
	
	band1sigma_lvjj += str(m_ComboBetaHalf68down).replace('[','').replace(']','').replace('\'','') + ', '+  str(m_ComboBetaHalf68up).replace('[','').replace(']','').replace('\'','')+'};'
	band2sigma_lvjj += str(m_ComboBetaHalf95down).replace('[','').replace(']','').replace('\'','') + ', '+ str(m_ComboBetaHalf95up).replace('[','').replace(']','').replace('\'','')+'};'
	
	
	
	print '\n'
	print betastring
	print '\n'
	print excurve_combo
	print obcurve_combo
	print band1sigma_combo
	print band2sigma_combo

	print '\n'
	print excurve_lljj
	print obcurve_lljj
	print band1sigma_lljj
	print band2sigma_lljj
	
	print '\n'
	print excurve_lvjj
	print obcurve_lvjj
	print band1sigma_lvjj
	print band2sigma_lvjj	
	print '\n'
	print '\n'
	
	
