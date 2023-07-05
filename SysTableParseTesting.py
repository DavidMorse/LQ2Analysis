import os
import sys
import math
import collections
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-y", "--year", dest="year", help="option to pick running year (2016,2017,2018,comb)", metavar="YEAR")
parser.add_argument("-e", "--enhanced", dest="sys", help="path to datacard for systematic uncertainties (enhanced selection)", metavar="SYS")
parser.add_argument("-f", "--final", dest="stat", help="path to datacard for statistical uncertainties (final selection)", metavar="STAT")

options = parser.parse_args()

year = str(options.year)
sysFile = str(options.sys)
statFile = str(options.stat)

if year == '':
	if '16' in sysFile and '17' in sysFile and '18' in sysFile or 'comb' in sysFile:
		year = 'combined'
	else:
		year = sysFile.split('/')[-1].split('_')[-1].split('.')[0]

print "year =",year

sysInfo = [line for line in open(sysFile,'r')]
statInfo = [line for line in open(statFile,'r')]

sysCards = []
statCards = []

sysCard = []
statCard = []

for x in sysInfo:
	if '.txt' in x:
		if len(sysCard) > 2:
			sysCards.append(sysCard)
		sysCard = []
		sysCard.append(x)
	else:
		if len(x) > 2:
			sysCard.append(x)
sysCards.append(sysCard)

for x in statInfo:
	if '.txt' in x:
		if len(statCard) > 2:
			statCards.append(statCard)
		statCard = []
		statCard.append(x)
	else:
		if len(x) > 2:
			statCard.append(x)
statCards.append(statCard)

massNames = ["300","400","500","600","700","800","900","1000","1100","1200","1300","1400","1500","1600","1700","1800","1900","2000","2100","2200","2300","2400","2500","2600","2700","2800","2900","3000","3500"]#,"4000"]
baseSysNames = ["MUONISO","TOPPT","MUONID","JES","MUONHLT","BTAG","PREFIRE","PDF","GE","MER","JER","MES","MUONRECO","LUMI","PU","VVNORM","SHAPEVV","TTNORM","SHAPETT","ZNORM","SHAPEZ","Total"]
baseStatNames = ["Signal","TTBar","TTV","VV","sTop","ZJets","WJets","Total"]
baseRateNames = ["TTBar","TTV","VV","sTop","ZJets","WJets","Total","LQ_M_300","LQ_M_400","LQ_M_500","LQ_M_600","LQ_M_700","LQ_M_800","LQ_M_900","LQ_M_1000","LQ_M_1100","LQ_M_1200","LQ_M_1300","LQ_M_1400","LQ_M_1500","LQ_M_1600","LQ_M_1700","LQ_M_1800","LQ_M_1900","LQ_M_2000","LQ_M_2100","LQ_M_2200","LQ_M_2300","LQ_M_2400","LQ_M_2500","LQ_M_2600","LQ_M_2700","LQ_M_2800","LQ_M_2900","LQ_M_3000","LQ_M_3500","LQ_M_4000"]

def ParseRateLine(line,bins,nProcessesPerBin,processesPerBin,backgroundsPerBin,signalsPerBin):

	# Dictionary to store all rates, returned by function
	rates = {}

	# Just the rates (remove 'rate' title)
	entries = line.split()[1:]

	# loop through ordered list of bins (e.g., 'lqtoBMu' or 'a2016')
	for i,_bin in enumerate(bins):
		binCounter = i*nProcessesPerBin[_bin]
		backgroundRate = 0.0
		signalRate = 0.0
		rates[_bin] = {}

		# loop through ordered list of processes in each bin (e.g., 'LQ_M_300' or 'sTop') and get the rate for each
		for j,proc in enumerate(processesPerBin[_bin]):
			rates[_bin][proc] = float(entries[binCounter+j])

	return rates

def RestructureRateDict(rates):
	# We want to retain the same dictionary structure as stat and sys dictionaries
	# For stat, each "name" is a line in the datacard and corresponds to a process, e.g., Signal, TTBar, etc., with a subdict = bin[sig, bkg]
	# For the rate, the "name" is just "rate", but we will change this to make a "name" corresponding to each process with a subdict = bin[sig, bkg]
	# We are just flipping the order of the nested dictionaries, which makes the dictionary compatiable with the rest of the code (it is identical in structure to the stat dict)

	flippedRates = collections.defaultdict(dict)
	for _bin, process in rates.items():
		for proc, rate in process.items():
			flippedRates[proc][_bin] = rate

	return dict(flippedRates)

def ParseSystematicLine(line,bins,nProcessesPerBin,processesPerBin,backgroundsPerBin,signalsPerBin,ratesPerBin):

	# Dictionary to store all systematics, returned by function
	relativeSysPerBin = {}

	# First we get the name of a given source of systematic uncertainty (e.g., 'BTAG,' 'BTAG17,' 'LUMI16Uncorr,' 'LUMI1718,' 'LUMICorr,' or 'PDF')
	sysName = line.split()[0]

	# Just the systematic uncertainties (remove systematic name and 'lnN' flag)
	entries = line.split()[2:]

	# loop through ordered list of bins (e.g., 'lqtoBMu' or 'a2016')
	for i,_bin in enumerate(bins):
		binCounter = i*nProcessesPerBin[_bin]
		relativeSysPerBin[_bin] = {"background": 0.0, "signal": 0.0}

		# Get toal background rate here
		totalBackgroundRate = sum([ratesPerBin[_bin][proc] for proc in backgroundsPerBin[_bin]])
		# loop through ordered list of processes in each bin (e.g., 'LQ_M_300' or 'sTop') and get the systematic for each
		for j,proc in enumerate(processesPerBin[_bin]):
			entry = entries[binCounter+j]

			# For total background relative systematic uncertainty, use weighted average of systematics, weighted by process rate
			if proc in backgroundsPerBin[_bin]:
				# Interpret the entry string to get the actual percent systematic or fill with a 0.0 for null entries
				if entry == "-": systematic = 0.0
				elif totalBackgroundRate == 0.0: systematic = 0.0
				else: systematic = (float(entry) - 1.0)*ratesPerBin[_bin][proc]/totalBackgroundRate
				relativeSysPerBin[_bin]["background"] += systematic

			elif proc in signalsPerBin[_bin]:
				# Interpret the entry string to get the actual percent systematic or fill with a 0.0 for null entries
				if entry == "-": systematic = 0.0
				else: systematic = float(entry) - 1.0
				relativeSysPerBin[_bin]["signal"] += systematic 


		relativeSysPerBin[_bin]["background"] = round(100*relativeSysPerBin[_bin]["background"], 5)
		relativeSysPerBin[_bin]["signal"] = round(100*relativeSysPerBin[_bin]["signal"], 5)

	return [sysName, relativeSysPerBin]

def ParseStatLine(line,bins,nProcessesPerBin,processesPerBin,backgroundsPerBin,signalsPerBin,ratesPerBin):

	# Dictionary to store all systematics, returned by function
	relativeStatPerBin = {}

	# First we get the name of a given source of systematic uncertainty (e.g., 'BTAG,' 'BTAG17,' 'LUMI16Uncorr,' 'LUMI1718,' 'LUMICorr,' or 'PDF')
	statName = line.split()[0]

	# Just the statistical uncertainties (remove stat name, 'gmN' flag, and event counts)
	entries = line.split()[3:]

	event = line.split()[2]

	# loop through ordered list of bins (e.g., 'lqtoBMu' or 'a2016')
	for i,_bin in enumerate(bins):
		binCounter = i*nProcessesPerBin[_bin]
		relativeStatPerBin[_bin] = {"background": {"up": 0.0, "down": 0.0}, "signal": {"up": 0.0, "down": 0.0}}

		# Get toal background rate here
		totalBackgroundRate = sum([ratesPerBin[_bin][proc] for proc in backgroundsPerBin[_bin]])
		totalSignalRate = sum([ratesPerBin[_bin][proc] for proc in signalsPerBin[_bin]])

		# loop through ordered list of processes in each bin (e.g., 'LQ_M_300' or 'sTop') and get the systematic for each
		for j,proc in enumerate(processesPerBin[_bin]):
			entry = entries[binCounter+j]
			statUp = 0.0
			statDown = 0.0

			if proc in backgroundsPerBin[_bin]:

				if entry == "-": 
					pass
				elif totalBackgroundRate < 0.0001: 
					pass
				elif ratesPerBin[_bin][proc] < 0.0001 or float(event) == 0.0: 
					statUp = float(entry)/totalBackgroundRate
				else: 
					statUp = ratesPerBin[_bin][proc]*math.sqrt(1.0/float(event))/totalBackgroundRate #ratesPerBin[_bin][proc]*math.sqrt(float(entry)/ratesPerBin[_bin][proc])
					statDown = statUp 
				relativeStatPerBin[_bin]["background"]["up"] += statUp*statUp
				relativeStatPerBin[_bin]["background"]["down"] += statDown*statDown

			elif proc in signalsPerBin[_bin]:

				if entry == "-": 
					pass
				elif totalSignalRate < 0.0001: 
					pass
				elif ratesPerBin[_bin][proc] < 0.0001  or float(event) == 0.0: 
					statUp = float(entry)/totalSignalRate
				else: 
					statUp = ratesPerBin[_bin][proc]*math.sqrt(1.0/float(event))/totalSignalRate #ratesPerBin[_bin][proc]*math.sqrt(float(entry)/ratesPerBin[_bin][proc])
					statDown = statUp
				relativeStatPerBin[_bin]["signal"]["up"] += statUp*statUp
				relativeStatPerBin[_bin]["signal"]["down"] += statDown*statDown
		
		relativeStatPerBin[_bin]["background"]["up"] = min(100.0, round(100*math.sqrt(relativeStatPerBin[_bin]["background"]["up"]), 5))
		relativeStatPerBin[_bin]["background"]["down"] = min(100.0, round(100*math.sqrt(relativeStatPerBin[_bin]["background"]["down"]), 5))
		relativeStatPerBin[_bin]["signal"]["up"] = min(100.0, round(100*math.sqrt(relativeStatPerBin[_bin]["signal"]["up"]), 5))
		relativeStatPerBin[_bin]["signal"]["down"] = min(100.0, round(100*math.sqrt(relativeStatPerBin[_bin]["signal"]["down"]), 5))


	return [statName, relativeStatPerBin]

def AddTotalToSystematics(systematics, bins):

	# Loop over each systematic and add in quadrature
	# Gives the total systematic for signal and background per bin

	sysTotal = {}

	for _bin in bins:
		sysTotal[_bin] = {"background": 0.0, "signal": 0.0}
		for sysname in systematics:
			if "Total" not in sysname:
				sysTotal[_bin]["background"] += systematics[sysname][_bin]["background"]*systematics[sysname][_bin]["background"]
				sysTotal[_bin]["signal"] 	 += systematics[sysname][_bin]["signal"]*systematics[sysname][_bin]["signal"]

		sysTotal[_bin]["background"] = round(math.sqrt(sysTotal[_bin]["background"]), 5)
		sysTotal[_bin]["signal"] = round(math.sqrt(sysTotal[_bin]["signal"]), 5)

	systematics["Total"] = sysTotal

	return systematics

def AddTotalToStatistics(statistics, bins):

	# Loop over each statistic and add in quadrature
	# Gives the total statistic for signal and background per bin

	statTotal = {}

	for _bin in bins:
		statTotal[_bin] = {"background": {"up": 0.0, "down": 0.0}, "signal": {"up": 0.0, "down": 0.0}}
		for statname in statistics:
			if "Total" not in statname:
				statTotal[_bin]["background"]["up"] += statistics[statname][_bin]["background"]["up"]*statistics[statname][_bin]["background"]["up"]
				statTotal[_bin]["background"]["down"] += statistics[statname][_bin]["background"]["down"]*statistics[statname][_bin]["background"]["down"]
				statTotal[_bin]["signal"]["up"] += statistics[statname][_bin]["signal"]["up"]*statistics[statname][_bin]["signal"]["up"]
				statTotal[_bin]["signal"]["down"] += statistics[statname][_bin]["signal"]["down"]*statistics[statname][_bin]["signal"]["down"]

		statTotal[_bin]["background"]["up"] = min(100.00, round(math.sqrt(statTotal[_bin]["background"]["up"]), 5))
		statTotal[_bin]["background"]["down"] = min(100.00, round(math.sqrt(statTotal[_bin]["background"]["down"]), 5))
		statTotal[_bin]["signal"]["up"] = min(100.00, round(math.sqrt(statTotal[_bin]["signal"]["up"]), 5))
		statTotal[_bin]["signal"]["down"] = min(100.00, round(math.sqrt(statTotal[_bin]["signal"]["down"]), 5))

	statistics["Total"] = statTotal

	return statistics

#Rates[mass][name][bin][sig/bkg][central]

def AddTotalToRate(rates, bins):

	# Loop over each statistic and add in quadrature
	# Gives the total statistic for signal and background per bin

	rateTotal = {}

	for _bin in bins:
		rateTotal[_bin] = {"background":  0.0, "signal": 0.0}
		for ratename in rates:
			if "Total" not in ratename:
				rateTotal[_bin]["background"] += rates[ratename][_bin]["background"]
				rateTotal[_bin]["signal"] += rates[ratename][_bin]["signal"]

		rateTotal[_bin]["background"] = round(rateTotal[_bin]["background"], 5)
		rateTotal[_bin]["signal"] = round(rateTotal[_bin]["signal"], 5)

	rates["Total"] = rateTotal

	return rates

def GetSystematics(card):

	# Reads in 'card' list
	# Fills a dictionary where keys are systematic names
	# For each stat key, values are dictionaries whose keys are bins (aka years)
	# For each 'year' key, values are dictionaries whose keys are 'signal' and 'background'
	# For 'signal' and 'background' keys, values are systematic values (relative to events) as a percentage
	# Returns list with first element is mass and second element is the systematics dictionary
	# Also combines correlated systematics like LUMI
	
	# 'bin' and 'process' occur twice in datacards; flag gets turned on (True) after passing first instance
	binFlag = False 
	processFlag = False

	# Data to be filled:
	mass = ""
	bins = []
	processBins = []
	nProcessesPerBin = {}
	processesPerBin = {}
	backgroundsPerBin = {}
	signalsPerBin = {}
	allSystematics = {}

	# loop through each line in datacard and fill dictionary with data
	for line in card:

		title = line.split()[0]

		# Get the LQ mass point and decay channel of the datacard
		if '.txt' in title:
			mass = title.split('_')[-1].split('.')[0]

		# Get the bin names (e.g., 'lqtoBMu' or 'a2016')
		# Bins are ordered so use a list here
		if 'bin' in title and not binFlag:
			bins = [b for b in line.split()[1:]]
			binFlag = True

		# Get number of processes per bin
		if 'bin' in title and binFlag:
			processBins = line.split()[1:]
			nProcessesPerBin = collections.Counter(line.split()[1:])
		
		# Get the process names in each bin (e.g., 'LQ_M_300' or 'sTop')
		# Processes are ordered so use lists here
		if 'process' in title and not processFlag:
			processesPerBin = {_bin : [proc for i, proc in enumerate(line.split()[1:]) if processBins[i] == _bin] for _bin in nProcessesPerBin}
			backgroundsPerBin = {_bin : [bkg for bkg in processesPerBin[_bin] if "LQ" not in bkg] for _bin in processesPerBin}
			signalsPerBin = {_bin : [sig for sig in processesPerBin[_bin] if "LQ" in sig] for _bin in processesPerBin}
			processFlag = True

		if 'rate' in title:
			ratesPerBin = ParseRateLine(line,bins,nProcessesPerBin,processesPerBin,backgroundsPerBin,signalsPerBin)
		
		# Store the systematic uncertainties for each bin (year) and process (signal + background)
		if 'lnN' in line:
			[sysName, systematicsPerBin] = ParseSystematicLine(line,bins,nProcessesPerBin,processesPerBin,backgroundsPerBin,signalsPerBin,ratesPerBin)
			allSystematics[sysName] = systematicsPerBin

	# Get the total systematics and add as a new key with sys name = "Total"
	allSystematics = AddTotalToSystematics(allSystematics, bins)

	return [mass, allSystematics]

def GetStatistics(card):

	# Reads in 'card' list
	# Fills a dictionary where keys are statistical error names
	# For each stat key, values are dictionaries whose keys are bins (aka years)
	# For each 'year' key, values are dictionaries whose keys are 'signal' and 'background'
	# For 'signal' and 'background' keys, values are statistical error values (relative to events) as a percentage
	# Returns list with first element is mass and second element is the statistics dictionary
	# Also combines statistics
	
	# 'bin' and 'process' occur twice in datacards; flag gets turned on (True) after passing first instance
	binFlag = False 
	processFlag = False

	# Data to be filled:
	mass = ""
	bins = []
	processBins = []
	nProcessesPerBin = {}
	processesPerBin = {}
	backgroundsPerBin = {}
	signalsPerBin = {}
	allStatistics = {}

	# loop through each line in datacard and fill dictionary with data
	for line in card:

		title = line.split()[0]

		# Get the LQ mass point and decay channel of the datacard
		if '.txt' in title:
			mass = title.split('_')[-1].split('.')[0]

		# Get the bin names (e.g., 'lqtoBMu' or 'a2016')
		# Bins are ordered so use a list here
		if 'bin' in title and not binFlag:
			bins = [b for b in line.split()[1:]]
			binFlag = True

		# Get number of processes per bin
		if 'bin' in title and binFlag:
			processBins = line.split()[1:]
			nProcessesPerBin = collections.Counter(line.split()[1:])
		
		# Get the process names in each bin (e.g., 'LQ_M_300' or 'sTop')
		# Processes are ordered so use lists here
		if 'process' in title and not processFlag:
			processesPerBin = {_bin : [proc for i, proc in enumerate(line.split()[1:]) if processBins[i] == _bin] for _bin in nProcessesPerBin}
			backgroundsPerBin = {_bin : [bkg for bkg in processesPerBin[_bin] if "LQ" not in bkg] for _bin in processesPerBin}
			signalsPerBin = {_bin : [sig for sig in processesPerBin[_bin] if "LQ" in sig] for _bin in processesPerBin}
			processFlag = True

		if 'rate' in title:
			ratesPerBin = ParseRateLine(line,bins,nProcessesPerBin,processesPerBin,backgroundsPerBin,signalsPerBin)
		
		# Store the statistical uncertainties for each bin (year) and process (signal + background)
		if 'gmN' in line:
			[statName, statsPerBin] = ParseStatLine(line,bins,nProcessesPerBin,processesPerBin,backgroundsPerBin,signalsPerBin,ratesPerBin)
			allStatistics[statName] = statsPerBin

	# Get the total systematics and add as a new key with sys name = "Total"
	allStatistics = AddTotalToStatistics(allStatistics, bins)

	return [mass, allStatistics]

def GetRates(card):
	# Reads in 'card' list
	# Fills a dictionary with single key "rate"
	# For the "rate" key, values are dictionaries whose keys are bins (aka years)
	# For each 'year' key, values are dictionaries whose keys are 'signal', all background processes (e.g., 'ttbar'), and 'background' (total)
	# For each process key, values are the rates (relative to events) as a percentage
	# Returns list with first element is mass and second element is the rate dictionary
	# Also combines statistics
	
	# 'bin' and 'process' occur twice in datacards; flag gets turned on (True) after passing first instance
	binFlag = False 
	processFlag = False

	# Data to be filled:
	mass = ""
	bins = []
	processBins = []
	nProcessesPerBin = {}
	processesPerBin = {}
	backgroundsPerBin = {}
	signalsPerBin = {}
	allRates = {}

	# loop through each line in datacard and fill dictionary with data
	for line in card:

		title = line.split()[0]

		# Get the LQ mass point and decay channel of the datacard
		if '.txt' in title:
			mass = title.split('_')[-1].split('.')[0]

		# Get the bin names (e.g., 'lqtoBMu' or 'a2016')
		# Bins are ordered so use a list here
		if 'bin' in title and not binFlag:
			bins = [b for b in line.split()[1:]]
			binFlag = True

		# Get number of processes per bin
		if 'bin' in title and binFlag:
			processBins = line.split()[1:]
			nProcessesPerBin = collections.Counter(line.split()[1:])
		
		# Get the process names in each bin (e.g., 'LQ_M_300' or 'sTop')
		# Processes are ordered so use lists here
		if 'process' in title and not processFlag:
			processesPerBin = {_bin : [proc for i, proc in enumerate(line.split()[1:]) if processBins[i] == _bin] for _bin in nProcessesPerBin}
			backgroundsPerBin = {_bin : [bkg for bkg in processesPerBin[_bin] if "LQ" not in bkg] for _bin in processesPerBin}
			signalsPerBin = {_bin : [sig for sig in processesPerBin[_bin] if "LQ" in sig] for _bin in processesPerBin}
			processFlag = True

		if 'rate' in title:
			ratesPerBinShort = ParseRateLine(line,bins,nProcessesPerBin,processesPerBin,backgroundsPerBin,signalsPerBin)
			ratesPerBin = {}
			for _bin in bins:
				ratesPerBin[_bin] = {}
				for bkgProc in backgroundsPerBin[_bin]:
					ratesPerBin[_bin][bkgProc] = {}
					ratesPerBin[_bin][bkgProc]["background"] = ratesPerBinShort[_bin][bkgProc]
					ratesPerBin[_bin][bkgProc]["signal"] = 0.0
				for sigProc in signalsPerBin[_bin]:
					ratesPerBin[_bin][sigProc] = {}
					ratesPerBin[_bin][sigProc]["background"] = 0.0
					ratesPerBin[_bin][sigProc]["signal"] = ratesPerBinShort[_bin][sigProc]

	flippedRates = RestructureRateDict(ratesPerBin)
	allRates = AddTotalToRate(flippedRates, bins)

	return [mass, allRates]

def ParseCards(sysCards,statCards):

	# Loop through all the datacards
	# Make a prime dictionary where each key is the mass corresponding to a card
	# Values are systematics dictionaries for that card
	
	sysData = {}
	statData = {}
	rateData = {}

	for sysCard in sysCards:
		[sysMass, systematics] = GetSystematics(sysCard)
		sysData[sysMass] = systematics

	for statCard in statCards:
		[statMass, statistics] = GetStatistics(statCard)
		statData[statMass] = statistics

		[rateMass, rates] = GetRates(statCard)
		rateData[rateMass] = rates

	return [sysData, statData, rateData]


def CombineCorrelatedSystematics(systematics, baseSysNames):

	import copy

	newDict = {}
	for mass in systematics:
		newDict[mass] = {}
		for sysBase in baseSysNames: 

			# Setup dictionary to store combined systematics
			# Make a copy of a single sys dictionary (which one is arbitrary) in systematics but replace the sys values with total lumis
			# Initialize lumis to 0.0
			sysTotal = {} #copy.deepcopy(systematics[mass]).values()[0]
			#for _bin in sysTotal:
			sysTotal["background"] = 0.0
			sysTotal["signal"] = 0.0

			# loop through systematics and add the systematic of each bin in quadrature
			for sysname in systematics[mass]:
				if sysBase in sysname or ("GE" in sysname and "MES" in sysBase):
					for _bin in systematics[mass][sysname]:
						sysTotal["background"] += systematics[mass][sysname][_bin]["background"]*systematics[mass][sysname][_bin]["background"]
						sysTotal["signal"] += systematics[mass][sysname][_bin]["signal"]*systematics[mass][sysname][_bin]["signal"]

			sysTotal["background"] = round(math.sqrt(sysTotal["background"]), 5)
			sysTotal["signal"] = round(math.sqrt(sysTotal["signal"]), 5)

			newDict[mass][sysBase] = sysTotal

	return newDict

def CombineStatistics(statistics, baseStatNames):

	newDict = {}
	for mass in statistics:

		newDict[mass] = {}
		# Setup dictionary to store combined statistics
		# Initialize lumis to 0.0
		statTotal = {} 

		statTotal["background"] = {"up": 0.0, "down": 0.0}
		statTotal["signal"] = {"up": 0.0, "down": 0.0}

		for statBase in baseStatNames: 

			statTotal["background"] = {"up": 0.0, "down": 0.0}
			statTotal["signal"] = {"up": 0.0, "down": 0.0}
			# loop through statistics and add the statistic of each bin in quadrature
			for statname in statistics[mass]:

				if statBase in statname and "Signal" in statBase:

					for _bin in statistics[mass][statname]:

						statTotal["signal"]["up"] += statistics[mass][statname][_bin]["signal"]["up"]*statistics[mass][statname][_bin]["signal"]["up"]
						statTotal["signal"]["down"] += statistics[mass][statname][_bin]["signal"]["down"]*statistics[mass][statname][_bin]["signal"]["down"]

				elif statBase in statname and "Total" not in statBase:

					for _bin in statistics[mass][statname]:

						statTotal["background"]["up"] += statistics[mass][statname][_bin]["background"]["up"]*statistics[mass][statname][_bin]["background"]["up"]
						statTotal["background"]["down"] += statistics[mass][statname][_bin]["background"]["down"]*statistics[mass][statname][_bin]["background"]["down"]

				elif statBase in statname and "Total" in statBase:

					for _bin in statistics[mass][statname]:

						statTotal["background"]["up"] += statistics[mass][statname][_bin]["background"]["up"]*statistics[mass][statname][_bin]["background"]["up"]
						statTotal["background"]["down"] += statistics[mass][statname][_bin]["background"]["down"]*statistics[mass][statname][_bin]["background"]["down"]

						statTotal["signal"]["up"] += statistics[mass][statname][_bin]["signal"]["up"]*statistics[mass][statname][_bin]["signal"]["up"]
						statTotal["signal"]["down"] += statistics[mass][statname][_bin]["signal"]["down"]*statistics[mass][statname][_bin]["signal"]["down"]


			statTotal["background"]["up"] = min(100.0, round(math.sqrt(statTotal["background"]["up"]), 5))
			statTotal["background"]["down"] = min(100.0, round(math.sqrt(statTotal["background"]["down"]), 5))
			statTotal["signal"]["up"] = min(100.0, round(math.sqrt(statTotal["signal"]["up"]), 5))
			statTotal["signal"]["down"] = min(100.0, round(math.sqrt(statTotal["signal"]["down"]), 5))

			newDict[mass][statBase] = statTotal


	return newDict

def CombineRates(rates, baseRateNames):

	newDict = {}
	for mass in rates:

		newDict[mass] = {}
		# Setup dictionary to store combined rates
		# Initialize lumis to 0.0


		for rateBase in baseRateNames: 

			newDict[mass][rateBase] = {}
			rateTotal = {"background": 0.0, "signal": 0.0}

			# loop through rates and add the rate of each bin
			for ratename in rates[mass]:

				if rateBase == ratename: # and "LQ_M_" in rateBase:

					for _bin in rates[mass][ratename]:

						rateTotal["signal"] += rates[mass][ratename][_bin]["signal"]
						rateTotal["background"] += rates[mass][ratename][_bin]["background"]
						
				#elif rateBase == ratename and "Total" not in rateBase:

				#	for _bin in rates[mass][ratename]:

				#		rateTotal["background"] += rates[mass][ratename][_bin]["background"]
				#		
				#elif rateBase == ratename and "Total" in rateBase:

				#	for _bin in rates[mass][ratename]:

				#		rateTotal["background"] += rates[mass][ratename][_bin]["background"]

				#		rateTotal["signal"] += rates[mass][ratename][_bin]["signal"]

			#rateTotal["background"] = rateTotal["background"]
			#rateTotal["signal"] = rateTotal["signal"]

			newDict[mass][rateBase]["background"] = rateTotal["background"]
			newDict[mass][rateBase]["signal"] = rateTotal["signal"]
			#print mass, rateBase, newDict[mass][rateBase]
	#print newDict
	return newDict	




def GetSysRanges(systematics):

	# Get the global minimum and maximum for each systematic accross all datacards
	# Return dictionary with structure: { sys : { bin : { process { min/max : value } } } }

	import copy

	# Setup dictionary to store systematic ranges
	# Make a copy of a single mass dictionary (which one is arbitrary) in systematics but replace the sys values with a "min" and "max"
	# Initialize min and max to 999 and 0, respectively
	sysRanges = copy.deepcopy(systematics).values()[0]
	for sys in sysRanges:
		for _bin in sysRanges[sys]:
			sysRanges[sys][_bin]["background"] = {"min" : 999.0, "max" : 0.0}
			sysRanges[sys][_bin]["signal"] = {"min" : 999.0, "max" : 0.0}

	# Loop through systematics for each mass 
	# Check if larger than global max or smaller than global min
	# If true, reset global max/min to that systematic value
	for mass in systematics:
		if mass == "3500" or mass == "4000":
			continue
		else:
			for sys in systematics[mass]:
				for _bin in systematics[mass][sys]:

					bkgSys = systematics[mass][sys][_bin]["background"]
					bkgMin = sysRanges[sys][_bin]["background"]["min"]
					bkgMax = sysRanges[sys][_bin]["background"]["max"]

					sigSys = systematics[mass][sys][_bin]["signal"]
					sigMin = sysRanges[sys][_bin]["signal"]["min"]
					sigMax = sysRanges[sys][_bin]["signal"]["max"]

					if bkgSys < bkgMin: bkgMin = bkgSys
					if bkgSys > bkgMax: bkgMax = bkgSys
					if sigSys < sigMin: sigMin = sigSys
					if sigSys > sigMax: sigMax = sigSys

					sysRanges[sys][_bin]["background"]["min"] = bkgMin
					sysRanges[sys][_bin]["background"]["max"] = bkgMax
					sysRanges[sys][_bin]["signal"]["min"] = sigMin
					sysRanges[sys][_bin]["signal"]["max"] = sigMax

	return sysRanges

def GetCombSysRanges(systematics):

	# Get the global minimum and maximum for each systematic accross all datacards
	# Return dictionary with structure: { sys : { bin : { process { min/max : value } } } }

	import copy

	# Setup dictionary to store systematic ranges
	# Make a copy of a single mass dictionary (which one is arbitrary) in systematics but replace the sys values with a "min" and "max"
	# Initialize min and max to 999 and 0, respectively
	sysRanges = copy.deepcopy(systematics).values()[0]
	for sys in sysRanges:
		for _bin in sysRanges[sys]:
			sysRanges[sys]["background"] = {"min" : 999.0, "max" : 0.0}
			sysRanges[sys]["signal"] = {"min" : 999.0, "max" : 0.0}

	# Loop through systematics for each mass 
	# Check if larger than global max or smaller than global min
	# If true, reset global max/min to that systematic value
	for mass in systematics:
		if mass == "3500" or mass == "4000":
			continue
		else:
			for sys in systematics[mass]:

				bkgSys = systematics[mass][sys]["background"]
				bkgMin = sysRanges[sys]["background"]["min"]
				bkgMax = sysRanges[sys]["background"]["max"]

				sigSys = systematics[mass][sys]["signal"]
				sigMin = sysRanges[sys]["signal"]["min"]
				sigMax = sysRanges[sys]["signal"]["max"]

				if bkgSys < bkgMin: bkgMin = bkgSys
				if bkgSys > bkgMax: bkgMax = bkgSys
				if sigSys < sigMin: sigMin = sigSys
				if sigSys > sigMax: sigMax = sigSys

				sysRanges[sys]["background"]["min"] = round(bkgMin, 2)
				sysRanges[sys]["background"]["max"] = round(bkgMax, 2)
				sysRanges[sys]["signal"]["min"] = round(sigMin, 2)
				sysRanges[sys]["signal"]["max"] = round(sigMax, 2)

	return sysRanges


def GetCombStatRanges(statistics):

	# Get the global minimum and maximum for each stat accross all datacards
	# Return dictionary with structure: { stat : { bin : { process { min/max : value } } } }

	import copy

	# Setup dictionary to store stat ranges
	# Make a copy of a single mass dictionary (which one is arbitrary) in statistics but replace the stat values with a "min" and "max"
	# Initialize min and max to 999 and 0, respectively
	statRanges = copy.deepcopy(statistics).values()[0]
	for stat in statRanges:
		for _bin in statRanges[stat]:
			statRanges[stat]["background"] = {"min" : 999.0, "max" : 0.0}
			statRanges[stat]["signal"] = {"min" : 999.0, "max" : 0.0}

	# Loop through statistics for each mass 
	# Check if larger than global max or smaller than global min
	# If true, reset global max/min to that stat value
	for mass in statistics:
		if mass == "3500" or mass == "4000":
			continue
		else:
			for stat in statistics[mass]:

				bkgUpStat = statistics[mass][stat]["background"]["up"]
				bkgDownStat = statistics[mass][stat]["background"]["down"]
				bkgMin = statRanges[stat]["background"]["min"]
				bkgMax = statRanges[stat]["background"]["max"]

				sigUpStat = statistics[mass][stat]["signal"]["up"]
				sigDownStat = statistics[mass][stat]["signal"]["down"]
				sigMin = statRanges[stat]["signal"]["min"]
				sigMax = statRanges[stat]["signal"]["max"]

				if bkgUpStat < bkgMin: bkgMin = bkgUpStat
				if bkgDownStat < bkgMin: bkgMin = bkgDownStat

				if bkgUpStat > bkgMax: bkgMax = bkgUpStat
				if bkgDownStat > bkgMax: bkgMax = bkgDownStat

				if sigUpStat < sigMin: sigMin = sigUpStat
				if sigDownStat < sigMin: sigMin = sigDownStat

				if sigUpStat > sigMax: sigMax = sigUpStat
				if sigDownStat > sigMax: sigMax = sigDownStat

				statRanges[stat]["background"]["min"] = round(bkgMin, 2)
				statRanges[stat]["background"]["max"] = round(bkgMax, 2)
				statRanges[stat]["signal"]["min"] = round(sigMin, 2)
				statRanges[stat]["signal"]["max"] = round(sigMax, 2)

	return statRanges

def MakeCleanTable(rates, masses):

	cleanTable = '\\begin{table}[htbp]\n'
	cleanTable += '\t \\begin{center}\n'
	cleanTable += '\t\t' + r'\hline\hline \\' + '\n'
	cleanTable += '\t\t' + r'\MLQ & Signal & \ZJets & \ttbar & \TTV & \VV & \WJets & single top & All BG & Data \\ \hline' + '\n'
	for mass in masses:
		#print rates[mass]["LQ_M_"+mass]
		sig = str(round(rates[mass]["LQ_M_"+mass]["signal"], 2)) 
		zjets = str(round(rates[mass]["ZJets"]["background"], 2)) 
		ttbar = str(round(rates[mass]["TTBar"]["background"], 2)) 
		ttv = str(round(rates[mass]["TTV"]["background"], 2)) 
		vv = str(round(rates[mass]["VV"]["background"], 2)) 
		wjets = str(round(rates[mass]["WJets"]["background"], 2)) 
		st = str(round(rates[mass]["sTop"]["background"], 2)) 
		bkg = str(round(rates[mass]["Total"]["background"], 2)) 
		cleanTable += '\t\t' + mass + " & " + sig + " & " + zjets + " & " + ttbar + " & " + ttv + " & " + vv + " & " + wjets + " & " + st + " & " + bkg + r" \\" + "\n"
	cleanTable += r'\hline\hline'

	return cleanTable

def MakeRangesTable(sysRanges, statRanges):

	SysRangeTable = '\\begin{table}[htbp]\n'
	SysRangeTable += '\t \\begin{center}\n'
	if 'comb' in year:
		SysRangeTable += '\t\t \\caption{Range of systematic uncertainties in signal acceptance and background yields in combined 2016, 2017, and 2018 simulated data. The last two lines show the total systematic uncertainty and total statistical uncertainty in the simulated samples, respectively.}\n'
	else:
		SysRangeTable += '\t\t \\caption{Range of systematic uncertainties on signal acceptance and background yields in '+year+' simulated data. The last two lines show the total systematic uncertainty and the total statistical uncertainty in the simulated samples, respectively}\n'
	SysRangeTable += '\t\t \\begin{tabular}{lcc}\\hline\\hline\n'
	SysRangeTable += '\t\t\t Uncertainty 			& Signal (\%)	& Background (\%) ' + r' \\ \hline' + '\n'
	SysRangeTable += '\t\t\t b-jet tagging efficiency	& ' + str(sysRanges["BTAG"]["signal"]["min"]) + '--' + str(sysRanges["BTAG"]["signal"]["max"]) + ' 		& ' + str(sysRanges["BTAG"]["background"]["min"]) + '--' + str(sysRanges["BTAG"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Jet energy resolution 		& ' + str(sysRanges["JER"]["signal"]["min"]) + '--' + str(sysRanges["JER"]["signal"]["max"]) + ' 		& ' + str(sysRanges["JER"]["background"]["min"]) + '--' + str(sysRanges["JER"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Jet energy scale 		& ' + str(sysRanges["JES"]["signal"]["min"]) + '--' + str(sysRanges["JES"]["signal"]["max"]) + ' 		& ' + str(sysRanges["JES"]["background"]["min"]) + '--' + str(sysRanges["JES"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Luminosity 			& ' + str(sysRanges["LUMI"]["signal"]["min"]) + '--' + str(sysRanges["LUMI"]["signal"]["max"]) + ' 		& ' + str(sysRanges["LUMI"]["background"]["min"]) + '--' + str(sysRanges["LUMI"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Muon energy resolution 	& ' + str(sysRanges["MER"]["signal"]["min"]) + '--' + str(sysRanges["MER"]["signal"]["max"]) + ' 		& ' + str(sysRanges["MER"]["background"]["min"]) + '--' + str(sysRanges["MER"]["background"]["max"]) + r' \\' + '\n'
	#SysRangeTable += '\t\t\t Generalized Endpoint 		& ' + str(sysRanges["GE"]["signal"]["min"]) + '--' + str(sysRanges["GE"]["signal"]["max"]) + ' 		& ' + str(sysRanges["GE"]["background"]["min"]) + '--' + str(sysRanges["GE"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Muon energy scale	 		& ' + str(sysRanges["MES"]["signal"]["min"]) + '--' + str(sysRanges["MES"]["signal"]["max"]) + ' 		& ' + str(sysRanges["MES"]["background"]["min"]) + '--' + str(sysRanges["MES"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Muon identification 		& ' + str(sysRanges["MUONID"]["signal"]["min"]) + '--' + str(sysRanges["MUONID"]["signal"]["max"]) + ' 		& ' + str(sysRanges["MUONID"]["background"]["min"]) + '--' + str(sysRanges["MUONID"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Muon isolation 		& ' + str(sysRanges["MUONISO"]["signal"]["min"]) + '--' + str(sysRanges["MUONISO"]["signal"]["max"]) + ' 		& ' + str(sysRanges["MUONISO"]["background"]["min"]) + '--' + str(sysRanges["MUONISO"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Muon reconstruction 		& ' + str(sysRanges["MUONRECO"]["signal"]["min"]) + '--' + str(sysRanges["MUONRECO"]["signal"]["max"]) + ' 		& ' + str(sysRanges["MUONRECO"]["background"]["min"]) + '--' + str(sysRanges["MUONRECO"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Muon trigger 			& ' + str(sysRanges["MUONHLT"]["signal"]["min"]) + '--' + str(sysRanges["MUONHLT"]["signal"]["max"]) + ' 		& ' + str(sysRanges["MUONHLT"]["background"]["min"]) + '--' + str(sysRanges["MUONHLT"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t PDF 				& --  		& ' + str(sysRanges["PDF"]["background"]["min"]) + '--' + str(sysRanges["PDF"]["background"]["max"]) + r' \\' + '\n'
	if 'comb' not in year and year == '2018': 
		SysRangeTable += '\t\t\t Prefire weighting			& -- & --' + r' \\' + '\n'
	else:
		SysRangeTable += '\t\t\t Prefire weighting 		& ' + str(sysRanges["PREFIRE"]["signal"]["min"]) + '--' + str(sysRanges["PREFIRE"]["signal"]["max"]) + ' 		& ' + str(sysRanges["PREFIRE"]["background"]["min"]) + '--' + str(sysRanges["PREFIRE"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Pileup 			& ' + str(sysRanges["PU"]["signal"]["min"]) + '--' + str(sysRanges["PU"]["signal"]["max"]) + ' 		& ' + str(sysRanges["PU"]["background"]["min"]) + '--' + str(sysRanges["PU"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Top $p_T$ reweighting 		& ' + str(sysRanges["TOPPT"]["signal"]["min"]) + '--' + str(sysRanges["TOPPT"]["signal"]["max"]) + ' 		& ' + str(sysRanges["TOPPT"]["background"]["min"]) + '--' + str(sysRanges["TOPPT"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t TT normalization 		& -- 			& ' + str(sysRanges["TTNORM"]["background"]["min"]) + '--' + str(sysRanges["TTNORM"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t TT shape 			& -- 			& ' + str(sysRanges["SHAPETT"]["background"]["min"]) + '--' + str(sysRanges["SHAPETT"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t VV normalization		& -- 			& ' + str(sysRanges["VVNORM"]["background"]["min"]) + '--' + str(sysRanges["VVNORM"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t VV shape 			& -- 			& ' + str(sysRanges["SHAPEVV"]["background"]["min"]) + '--' + str(sysRanges["SHAPEVV"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Z normalization 		& -- 			& ' + str(sysRanges["ZNORM"]["background"]["min"]) + '--' + str(sysRanges["ZNORM"]["background"]["max"]) + r' \\' + '\n'
	SysRangeTable += '\t\t\t Z shape 			& -- 			& ' + str(sysRanges["SHAPEZ"]["background"]["min"]) + '--' + str(sysRanges["SHAPEZ"]["background"]["max"]) + r' \\ \hline' + '\n'
	SysRangeTable += '\t\t\t Total syst. uncertainty		& ' + str(sysRanges["Total"]["signal"]["min"]) + '--' + str(sysRanges["Total"]["signal"]["max"]) + ' 	& ' + str(sysRanges["Total"]["background"]["min"]) + '--' + str(sysRanges["Total"]["background"]["max"]) + r' \\ \hline\hline' + '\n'
	SysRangeTable += '\t\t\t Total stat. uncertainty		& ' + str(statRanges["Total"]["signal"]["min"]) + '--' + str(statRanges["Total"]["signal"]["max"]) + ' 	& ' + str(statRanges["Total"]["background"]["min"]) + '--' + str(statRanges["Total"]["background"]["max"]) + r' \\ \hline\hline' + '\n'
	SysRangeTable += '\t\t \\end{tabular}\n'
	if 'comb' in year:
		SysRangeTable += '\t\t \\label{tab:SysRangesCombined}\n'
	else:
		SysRangeTable += '\t\t \\label{tab:SysRanges'+year+'}\n'
	SysRangeTable += '\t \\end{center}\n'
	SysRangeTable += '\\end{table}\n'
	SysRangeTable += '\n'

	return SysRangeTable



[systematics, statistics, rates] = ParseCards(sysCards,statCards)
combinedSystematics = CombineCorrelatedSystematics(systematics, baseSysNames)
combinedStatistics = CombineStatistics(statistics, baseStatNames)
combinedRates = CombineRates(rates, baseRateNames)

print MakeCleanTable(combinedRates, massNames)