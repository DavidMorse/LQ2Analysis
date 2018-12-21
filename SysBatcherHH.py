import os 
import sys
import math
import random

# Read teh LQ Result Producer
f = [line for line in open('HHResultProducer.py','r')]

# Find the line the FullAnalysis function that contains the systematic variations, and get all those variations
for line in f:
	if '_Variations = ' in line and '#' not in line: 
		line = line.replace('\t','')
		line = line.replace('\n','')
		line = line.replace(' ','')
		exec(line)

# Get the current working drectory (to be used in making launcher scripts)
pwd = os.popen('pwd').readlines()[0].replace('\n','')
tmpnum = 1


# Loop over channels and systematic variations
#for c in ['uujj','uvjj']:
for c in ['uujj','eejj']:
	for v in _Variations:
		tmpnum += 1
		# this will be the new .py file for this channel/variation
		runfile = '__'+('HHResultProducer.py').replace('.py','__'+v+'__'+c+'.py')
		fout = open(runfile,'w')

		# Loop over lines, and detect whether the line is in the main function
		mainon = 0
		for line in f:
			if 'def' in line and 'main()' in line:
				mainon = 1
			if line[0] == '#':
				mainon = 0

			if 'analysisChannel = \'muon\'' in line:
				if c=='eejj': line = '#'+line
				if c=='uujj': line = line.replace('#','')
			if 'analysisChannel = \'electron\'' in line:
				if c=='uujj': line = '#'+line
				if c=='eejj': line = line.replace('#','')
			
			# Replace the _Variations = [ ... ] line with our single variation
			if '_Variations = ' in line and '#' not in line: 
				line = line.split('=')[0]+' = [\''+v+'\']\n'
			
			if v == '':
				if '_13TeV_new.root' in line and 'RECREATE' in line:
					line = line.replace('_13TeV_new.root', str('_' + v + '_13TeV_new.root'))
			else:
				if '_13TeV_new.root' in line and 'UPDATE' in line:
					line = line.replace('UPDATE', 'RECREATE')
					line = line.replace('_13TeV_new.root', str('_' + v + '_13TeV_new.root'))
			
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
					if 'Muon'  not in line:
						line = '#'+line
				if c=='eejj':
					if 'Muon'  not in line:
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
		ftcsh = runfile.replace('.py','.tcsh')

		# Open tcsh script
		fout = open(ftcsh,'w')

		# Lines for CMSSW setup
		fout.write('#!/bin/csh\nsetenv SCRAM_ARCH slc6_amd64_gcc530\ncmsrel CMSSW_8_0_26_patch1\ncd CMSSW_8_0_26_patch1/src\ncmsenv\ncd '+pwd+'\n')
		# Line for running the .py file
		fout.write('python '+runfile+'\n\n')
		# Close tcsh script
		fout.close()
		# bsub command
		os.system('chmod 755 '+ftcsh)
		bsub =  'bsub -q 8nh -e /dev/null -J '+runfile.split('.')[0]+' < '+ftcsh #was 1nw
		#bsub =  'bsub -q 2nd -e /dev/null -J '+runfile.split('.')[0]+' < '+ftcsh #was 1nw
		print bsub
		# Run bsub command if using "--launch" argument
		if '--launch' in sys.argv:
			os.system(bsub)


