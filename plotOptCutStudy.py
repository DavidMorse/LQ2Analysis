import os
import matplotlib.pyplot as plt
import json
import math
import numpy as np
from matplotlib.ticker import MaxNLocator

# Information for signal type, channel, b-jet tag requirements, BDT variable, etc.
signalType = 'LQ'
channelDict = {'uujj':'pair','uuj':'single','1':'BMu','2':'BMu','0':'SMu'}
BDTstring = 'LQToBMu_pair_uubj_BDT_discrim_M'

# Create list of background samples (e.g., 'ZJets')
backgrounds =  ['DiBoson','WJets','TTBar','ZJets','SingleTop','TTV']

# Create list of signal samples (e.g., 'LQuujj300')
signals = ['LQuujj300','LQuujj400','LQuujj500','LQuujj600','LQuujj700','LQuujj800','LQuujj900','LQuujj1000','LQuujj1100','LQuujj1200','LQuujj1300','LQuujj1400','LQuujj1500','LQuujj1600','LQuujj1700','LQuujj1800','LQuujj1900','LQuujj2000','LQuujj2100','LQuujj2200','LQuujj2300','LQuujj2400','LQuujj2500','LQuujj2600','LQuujj2700','LQuujj2800','LQuujj2900','LQuujj3000','LQuujj3500','LQuujj4000']

lumi = 137620.

def ConvertBinning(binning):
	binset=[]
	if len(binning)==3:
		for x in range(binning[0]+1):
			binset.append(((binning[2]-binning[1])/(1.0*binning[0]))*x*1.0+binning[1])
	else:
		binset=binning
	return binset

def OptimizeCutsBDT(bins, cutfile, year, channel, btags):

	# Get number of bins
	lowBound = bins[0]
	upBound = bins[1]
	binWidth = bins[2]
	binning = [int(round((upBound-lowBound)/binWidth)),lowBound,upBound]

	# Set bin range and number of bins in 'binning'
	nBins = binning[0]
	binLow = binning[1]
	binHigh = binning[2]

	# dictironary to return
	punziDict = {}

	nf = os.popen('cat '+cutfile+' | wc -l').readlines()[0]
	nf = int(nf)
	nd = 0

	# Loop through each line of cutfile
	for c in open(cutfile):
		nd += 1
		if nd%100==0:
			# Prints periodic status as percentage
			print str(100*round( (1.0*nd)/(1.0*nf),3 )), '% complete'

		# Executes each line in cutfile
		# Initializes a dictionary for each sample
		# Fills each dictionary with subdictionaries corresponding to each BDT variable
		# Fills each subdictionary with the number of events corresponding to each cut
		exec(c)

	# Initialize a dictionary to store all signal dictionaries (e.g., events_LQuujj300, ...) containing event counts for all cut values
	signalEventsAll = {}

	# Initialize a dictionary to store all SM background dictionaries (e.g., events_ZJets, ...) containing event counts for all cut values
	backgroundEventsAll = {}

	# Assign signal dictionary with key = 'signal' (e.g., 'LQuujj') and value = subdictionary (e.g., events_LQuujj300)
	for signal in signals:
		exec('signalEventsAll[signal] = events_'+signal )

	# Assign background dictionary with key = 'background' (e.g., 'ZJets') and value = subdictionary (e.g., events_ZJets)
	for background in backgrounds:
		exec('backgroundEventsAll[background] = events_'+background )

	# Table (list) that will store the cut values
	valuetable = []

	xsecs = {}

	# Get LQ cross sections from ntuple info csv files
	# Store in a dictionary with key = 'signal' (e.g., 'LQuujj300') and value = xsec
	with open('NTupleInfo'+year+'Full_stockNano.csv','r') as NTupleInfocsv:
		for line in NTupleInfocsv:
			if signalType+'To'+channelDict[btags] in line and channelDict[channel] in line:
				xsecs[signalType+channel+line.split(',')[0].split('-')[-1].split('_')[0]] = float(line.split(',')[1])
				#xsecs = {signalType+channel+line.split(',')[0].split('-')[-1].split('_')[0] : float(line.split(',')[1]) for line in NTupleInfocsv if signalType+'To'+channelDict[btags] in line and channelDict[channel] in line}

	# Get a list of the cut values, i.e., bin edges (e.g., -1.0, -0.95, ..., 0.95, 1.0)
	binList = [str(b) for b in ConvertBinning(binning)[:-1]]

	# Loop to optimze the cut value for each signal hypothesis
	# Use the Punzi significance as a figure of merit (FOM)

	# Start by looping through 'signal' keys (e.g., 'LQuujj300')
	# This also determines which variable will be cut on, i.e., 'LQToBMu_pair_uubj_BDT_discrim_M' + signal mass
	# Sort dictionary by signal mass first
	#for signal in sorted(signalEventsAll.items(), key=lambda signal: int(signal.strip(signalType+channel)) ):
	for signal in signalEventsAll:

		print "Optimizing signal ",signal,"..."

		# Initalize
		maxPunziFOM = -99999
		bestCutVal = binning[1]

		punziDict[signal] = []

		# Get signal mass as a string
		signalMass = signal.strip(signalType+channel)
		#print "binList = ",binList
		# Loop through each cut value
		for cutValue in binList:
			#print "cutvalue = ",cutValue

			# Number of signal events when cut (cutValue) is applied to variable 'LQToBMu_pair_uubj_BDT_discrim_M'+signalMass, e.g., (LQToBMu_pair_uubj_BDT_discrim_M300 > 0.0)
			nSignal = signalEventsAll[signal][BDTstring+signalMass][str(cutValue)]

			# Initialize background events
			nBackground = 0.0

			# Get original number of signal events from luminosity x cross section (lumi is a global variable)
			nSignalOrig = xsecs[signal]*lumi

			# Loop through 'background' keys (e.g., 'ZJets')
			# Add event counts of all the backgrounds together (ZJets + TTBar + DiBoson + ...) for the current cut
			for background in backgroundEventsAll:
				nBackground += backgroundEventsAll[background][BDTstring+signalMass][str(cutValue)]
			#if nSignal + nBackground < 0.001:
			#	continue

			# Initialize the signal efficiency
			nSignalEff  = nSignal / nSignalOrig

			# Initialize the FOM value
			punziFOM = 0

			# Prevents negative event counts from amc@NLO backgrounds and division by zero
			if nBackground > 0.0:
				# Calculate the FOM for cut value using the definition of the Punzi significance
				punziFOM = nSignalEff/(2.5+math.sqrt(nBackground))

			#print "Appending [",cutValue,",",punziFOM,"] to punziDict[",signal,"]"
			punziDict[signal].append([cutValue,punziFOM])

			# Optimization test; compare current FOM to the best FOM for each cut value
			if punziFOM > maxPunziFOM :
				# Update current FOM value as the 'maximized' FOM value
				maxPunziFOM = punziFOM
				# Update current cut value as the 'best' cut value
				bestCutVal = cutValue

		## String with optimized cut for current signal mass
		#opt = 'opt_'+signal + ' = (' + BDTstring+signalMass + '>' + str(bestCutVal) + ')\n'  
		#print opt

		## Save optimized cut string to list along with mass and then sort by mass
		#valuetable.append((int(signalMass),opt))
		#valuetable = sorted(valuetable)

	# Here we write the cuts to a log file
	#with open('Results_'+tag+'/Opt'+signalType+'_'+channel+'Cuts_BDT.txt','w') as optimlog:
	#	for mass in range(len(valuetable)):
	#		# Write string to optimization log file
	#		optimlog.write(valuetable[mass][1])

	print "Done."
	return punziDict

def main():

	print "Getting Punzi significance for each mass..."

	fullPath = "/afs/cern.ch/work/g/gmadigan/CMS/Analysis/Leptoquarks/MakeTreesStockNanoAODv6_2/LQ2Analysis13TeV/Results_combined_CoarseGrainOpt_10bins"

	os.system("mkdir "+fullPath+"/Plots")
	os.system("mkdir "+fullPath+"/Plots/Optimization")

	bdtBins = [0.0,1.0,0.1]

	data = OptimizeCutsBDT(bdtBins, fullPath+"/Log_LQuujj_BDT_Cuts.txt", "2016", "uujj", "1")

	optCuts = {}
	with open(fullPath+"/Opt_LQuujj_Cuts.txt","r") as optcutfile:
		for line in optcutfile:
			mass = line.split('=')[0].split('opt_LQuujj')[-1].strip()
			bdtcut = float(line.split(mass+'>')[-1].split(')')[0].strip())
			optCuts[mass] = bdtcut

	for signal in signals:

		print "Plotting for signal:",signal,"..."

		x = np.linspace(0.0,.9,10)
		y = [pair[1] for pair in data[signal] if pair[0] != '1.0']

		mass = signal.split("LQuujj")[-1]
		
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)

		ax.plot(x,y,'-')

		ax.set_ylabel("Punzi Significance",fontsize=16)
		ax.set_xlabel(r"BDT score ($M_{LQ}$ = "+mass+" GeV)",fontsize=16)

		ax.axvline(x=optCuts[mass], color='orange', linestyle='-')

		fig.savefig(fullPath+'/Plots/Optimization/Opt_BDT_M'+mass+'.pdf')
		plt.close(fig)
		

main()