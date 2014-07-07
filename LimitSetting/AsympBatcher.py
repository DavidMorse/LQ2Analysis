import os
import sys

# betas = [0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.18,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,0.9995]
# betas = [0.1,0.4,0.9]
betas = []
b = 0.00
while b<0.9999:
	if b < 0.1 or b > 0.9:
		b = b + 0.002
	else: 
		b = b + 0.010
	if b < 1.0:
		betas.append( b )
betas.append(0.9995)
os.system('rm -r BatcherResults')
os.system(' mkdir BatcherResults')

sysargs = ''
for x in sys.argv:
	if '.py' not in x:
		sysargs += ' '+x
sysargs +=' --single_beta '

person = (os.popen('whoami').readlines())[0].replace('\n','')
mdir = (os.popen('pwd').readlines())[0]
mdir = mdir.replace('\n','')

bsubs = []
for b in betas:
	bs = str(b).replace('.','_')
	f = open('BatcherResults/batch_R_'+bs+'.csh','w')
	f.write('#!/bin/csh\n\n')
	f.write('cd '+mdir+'/CMSSW_5_3_4/src/\n')
	f.write('cmsenv\n')
	f.write('cd -\n')
	f.write('cp '+mdir+'/RunStatsBasicCLs.py .\n')
	f.write('cp '+mdir+'/FinalCards.txt .\n')

	f.write('python RunStatsBasicCLs.py '+sysargs+' '+str(b)+' > Result_'+bs+'.txt\n')
	f.write('cp Result* '+mdir+'/BatcherResults/\n\n')
	
	f.close()
	bsubs .append('bsub  -e /dev/null -q 1nd -J job_'+bs+' < ' +'BatcherResults/batch_R_'+bs+'.csh')
	#bsubs .append('bsub -q 1nd -J job_'+bs+' < ' +'BatcherResults/batch_R_'+bs+'.csh')

	
os.system('chmod 777 BatcherResults/*.csh')

for x in bsubs:
	os.system('sleep 0.2')
	print x
	os.system(x)

 