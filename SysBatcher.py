import os 
import sys
import math
import random
from argparse import ArgumentParser

# Get year and b tag requirement
# Input Options - data-taking year and b tag requirement
parser = ArgumentParser()
parser.add_argument("-y", "--year", dest="year", help="option to pick running year (2016,2017,2018)", metavar="YEAR")
parser.add_argument("-b", "--btags", dest="btags", help="option to pick minimum number of b-tagged jets required (0,1,2)", metavar="BTAGS")
options = parser.parse_args()
year = str(options.year)
btags = str(options.btags)

if year not in ['2016','2017','2018']: 
	print "Please enter year with argument '-y' [2016, 2017, 2018]\nExiting..."
	exit()
if btags not in ['0','1','2']:
	print "Please enter b tag requirement with argument '-b' [0, 1, 2]\nExiting..."
	exit()

# Read the LQ Result Producer
f = [line for line in open('LQResultProducer.py','r')]

# Find the line the FullAnalysis function that contains the systematic variations, and get all those variations
for line in f:
	if '_Variations'+year+' = ' in line and '#' not in line: 
		line = line.replace('\t','')
		line = line.replace('\n','')
		line = line.replace(' ','')
		exec(line)
	if "_Variations = _Variations"+year in line and '#' not in line:
		line = line.replace('\t','')
		line = line.replace('\n','')
		exec(line)

# Get the current working drectory (to be used in making launcher scripts)
pwd = os.popen('pwd').readlines()[0].replace('\n','')
tmpnum = 1


# Loop over channels and systematic variations
for c in ['uujj']: #,'uvjj']:
	for v in _Variations:
		tmpnum += 1
		# this will be the new .py file for this channel/variation
		runfile = '__'+('LQResultProducer.py').replace('.py','__'+year+'__'+v+'__'+c+'.py')
		fout = open(runfile,'w')

		# Loop over lines, and detect whether the line is in the main function
		mainon = 0
		for line in f:
			if 'def' in line and 'main()' in line:
				mainon = 1
			if line[0] == '#':
				mainon = 0


			# Replace the _Variations = [ ... ] line with our single variation
			if '_Variations'+year+' = ' in line and '#' not in line: 
				line = line.split('=')[0]+' = [\''+v+'\']\n'
			dowrite = True

			# If we are in the main function, only keep the "scriptflag" lines
			if mainon==1:
				dowrite=False
				if 'main()' in line or 'scriptflag' in line:
					dowrite = True
					if 'main()' not in line:
						line = line.replace(' ','')
						line = line.replace('\t','')
						line = '\t'+line+'\n'
						if len(line)>0:
							if line[1] =='#':
								line = line[0]+line[2:]

			# Comment out lines for the channel we aren't using
			if 'FullAnalysis' in line and '#' not in line[1] and '#' not in line[0] and 'def' not in line:
				if c=='uujj':
					if 'MuMu'  not in line:
						line = '#'+line
				if c=='uvjj':
					if 'MuNu'  not in line:
						line = '#'+line

			# Replace the "tmp.root" file with a unique file so jobs can run simultaneously
			line = line.replace('tmp.root','tmp'+str(tmpnum)+'.root')

			# Write the modified line to the new py script
			if dowrite:
				fout.write(line)

		# Close the py script
		fout.close()

		# Now, write a csh script for launching the job (same name as .py file, except for extension)
		#ftcsh = runfile.replace('.py','.tcsh')

		## Open tcsh script
		#fout = open(ftcsh,'w')

		## Lines for CMSSW setup
		#fout.write('#!/bin/csh\nsetenv SCRAM_ARCH slc6_amd64_gcc530\ncmsrel CMSSW_8_0_26_patch1\ncd #CMSSW_8_0_26_patch1/src\ncmsenv\ncd '+pwd+'\n')
		## Line for running the .py file
		#fout.write('python '+runfile+'\n\n')
		## Close tcsh script
		#fout.close()
		## bsub command
		#os.system('chmod 755 '+ftcsh)
		#bsub =  'bsub -q cmscaf1nd -e /dev/null -J '+runfile.split('.')[0]+' < '+ftcsh #was 1nw
		#print bsub
		## Run bsub command if using "--launch" argument
		#if '--launch' in sys.argv:
		#	os.system(bsub)




		#Run with HTCondor:
		bjq = '\"longlunch\"'
		runname = runfile.split('.')[0]
		ftcsh = runfile.replace('.py','.tcsh')
		fsub = runfile.replace('.py','.sub')
		subber = open(ftcsh,'w')

		subber.write('#!/bin/tcsh\n\n')
		subber.write('setenv SCRAM_ARCH slc7_amd64_gcc700\n\n')
		subber.write('source /cvmfs/cms.cern.ch/cmsset_default.csh\n')
		subber.write('scram project CMSSW CMSSW_10_6_4\ncd CMSSW_10_6_4/src\n')#')scramv1 runtime -csh\ncd -\n\n')
		subber.write('cmsenv\n')
		subber.write('cd '+pwd+'\n')
		subber.write('python '+runfile+' -y '+year+' -b '+btags+'\n\n')


		subber.close()

		subber = open(fsub,'w')
		subber.write('executable            = '+ftcsh)
		subber.write('\narguments             =  $(ClusterID) $(ProcId)')
		subber.write('\n+JobFlavour           = '+bjq)
		subber.write('\noutput                 = '+runname+'_out.txt')
		subber.write('\nerror                  = '+runname+'_err.txt')
		subber.write('\nlog                    = '+runname+'.log')

		subber.write('\nrequirements = (OpSysAndVer =?= "CentOS7")')
		subber.write('\nqueue\n')

		subber.close()

		os.system('chmod 777 '+ftcsh)
		os.system('chmod 777 '+fsub)

		print 'condor_submit '+fsub
		os.system('condor_submit '+fsub)
		os.system('sleep 0.4')
