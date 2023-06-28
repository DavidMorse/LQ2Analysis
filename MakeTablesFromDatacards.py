import os
import sys
import math
import collections
from argparse import ArgumentParser
from copy import deepcopy


class Rate():
	def __init__(self, name = "", year = "2016", mass = "300", rate = 0.0, statHigh = 0.0, statLow = 0.0, dataType = ""):
		self.name = name

		if "c" in year or "C" in year:
			self.year = "combined"
		elif "2016" in year or "2017" in year or "2018" in year:
			self.year = year
		else:
			self.year = "2016"

		self.mass = str(mass)
		self.rate = float(rate)
		self.statHigh = float(statHigh)
		self.statLow = float(statLow)
		self.relSys = {"Total": 0.0}
		self.sys = {"Total": 0.0}

		self.dataType = ""
		self.isData = False
		self.isBkg = False
		self.isSig = False

		if "b" in dataType or "B" in dataType:
			self.isBkg = True
			self.dataType = "background"
		elif "s" in dataType or "S" in dataType: 
			self.isSig = True
			self.dataType = "signal"
		else:
			self.isData = True
			self.dataType = "data"
		
	def SetName(self,name):
		self.name = name

	def SetYear(self,year):
		self.year = year

	def SetMass(self,mass):
		self.mass = mass

	def SetRate(self,rate):
		self.rate = float(rate)
		self.UpdateSysDict()

	def SetDataType(self,dataType):
		self.dataType = ""
		self.isData = False
		self.isBkg = False
		self.isSig = False
		if "b" in dataType or "B" in dataType:
			self.isBkg = True
			self.dataType = "background"
		elif "s" in dataType or "S" in dataType: 
			self.isSig = True
			self.dataType = "signal"
		else:
			self.isData = True
			self.dataType = "data"

	def isData(self):
		return self.isData

	def isBackground(self):
		return self.isBkg

	def isSignal(self):
		return self.isSig

	def GetDataType(self):
		return self.dataType

	def SetStatHigh(self,statHigh):
		self.statHigh = float(statHigh)

	def SetStatLow(self,statLow):
		self.statLow = float(statLow)

	def AddRelSys(self,sysName,relSys):
		try: 
			sysName not in self.relSys
		except: 
			raise SystemExit("Systematic already added. Try SetRelSys() method.")
		self.relSys[sysName] = float(relSys)
		self.UpdateSysDict()
		self.UpdateSysTotal()

	def SetRelSys(self,sysName,relSys):
		try: 
			sysName in self.relSys
		except: 
			raise SystemExit("Systematic not found. Try AddRelSys() method.")
		self.relSys[sysName] = float(relSys)
		self.UpdateSysDict()
		self.UpdateSysTotal()

	def SetAllRelSys(self,relSysDict):
		self.relSys.clear()
		self.relSys = relSysDict
		self.UpdateSysDict()
		self.UpdateSysTotal()

	def UpdateSysTotal(self):
		del self.relSys["Total"]
		self.relSys["Total"] = math.sqrt( sum([relSys*relSys for (sysName, relSys) in self.relSys.items()]) )

		del self.sys["Total"]
		self.sys["Total"] = self.relSys["Total"]*self.rate

	def UpdateSysDict(self):
		self.sys.clear()
		self.sys = {sysName: relSys*self.rate for (sysName, relSys) in self.relSys.items()}

	def GetYear(self):
		return self.year

	def GetName(self):
		return self.name

	def GetMass(self):
		return self.mass

	def GetRate(self):
		return self.rate

	def GetStatHigh(self):
		return self.statHigh

	def GetStatLow(self):
		return self.statLow

	def GetRelStatHigh(self):
		return self.statHigh/self.rate

	def GetRelStatLow(self):
		return self.statLow/self.rate

	def GetMaxStat(self):
		return max(self.statHigh, self.statLow)

	def GetMinStat(self):
		return min(self.statHigh, self.statLow)

	def GetMaxRelStat(self):
		return max(self.statHigh, self.statLow)/self.rate

	def GetMinRelStat(self):
		return min(self.statHigh, self.statLow)/self.rate

	def GetRelSys(self,sysName):
		return self.relSys[sysName]

	def GetAllRelSys(self):
		return self.relSys

	def GetSys(self, sysName):
		return self.sys[sysName]

	def GetAllSys(self):
		return self.sys

	def GetSysNames(self):
		return [sysName for sysName in self.relSys]

	def GetStatSysHigh(self):
		return math.sqrt(self.statHigh*self.statHigh + self.sys["Total"]*self.sys["Total"])

	def GetStatSysLow(self):
		return math.sqrt(self.statLow*self.statLow + self.sys["Total"]*self.sys["Total"])

	def CombineCorrelatedSys(self, sysBaseNames):
		newSys = {}
		for sysBase in sysBaseNames:
			sysTotal = 0.0
			for sysName in self.relSys:
				if sysBase in sysName or ("GE" in sysName and "MES" in sysBase):
					sysTotal += self.relSys[sysName]*self.relSys[sysName]
			newSys[sysBase] = round(math.sqrt(sysTotal), 5)
		self.relSys = newSys 
		self.UpdateSysDict()
		self.UpdateSysTotal()

	def CombineRates(self, rateObj):
		if self.year != rateObj.GetYear(): self.year = "combined"
		elif self.name != rateObj.GetName(): self.name += "/" + rateObj.GetName()

		self.rate += rateObj.GetRate()
		self.statHigh = math.sqrt( self.statHigh*self.statHigh + rateObj.GetStatHigh()*rateObj.GetStatHigh() )
		self.statLow = math.sqrt( self.statLow*self.statLow + rateObj.GetStatLow()*rateObj.GetStatLow() )
		for sysName in rateObj.GetAllRelSys():
			if sysName not in self.relSys: 
				self.AddRelSys(sysName, rateObj.GetRelSys(sysName))
			else: 
				self.SetRelSys(sysName, math.sqrt(self.relSys[sysName]*self.relSys[sysName] + rateObj.GetRelSys(sysName)*rateObj.GetRelSys(sysName)))

def GetCards(datacard):

	card = []
	cards = []

	for line in datacard:
		if '.txt' in line:
			if len(card) > 2:
				cards.append(card)
			card = []
			card.append(line)
		else:
			if len(line) > 2:
				card.append(line)
	cards.append(card)

	return cards

def ParseRateLine(line,years,nProcessesPerYear,processesPerYear):

	# Dictionary to store all rates, returned by function
	rates = {}

	# Just the rates (remove 'rate' title)
	entries = line.split()[1:]

	# loop through ordered list of years (e.g., 'lqtoBMu' or 'a2016')
	for i,year in enumerate(years):
		yearCounter = i*nProcessesPerYear[year]
		backgroundRate = 0.0
		signalRate = 0.0
		rates[year] = {}

		# loop through ordered list of processes in each year (e.g., 'LQ_M_300' or 'sTop') and get the rate for each
		for j,proc in enumerate(processesPerYear[year]):
			rates[year][proc] = float(entries[yearCounter+j])

	return rates

def ParseSystematicLine(line,years,nProcessesPerYear,processesPerYear,ratesPerYear):

	# Dictionary to store all systematics, returned by function
	sysPerYear = {}

	# First we get the name of a given source of systematic uncertainty (e.g., 'BTAG,' 'BTAG17,' 'LUMI16Uncorr,' 'LUMI1718,' 'LUMICorr,' or 'PDF')
	sysName = line.split()[0]

	# Just the systematic uncertainties (remove systematic name and 'lnN' flag)
	entries = line.split()[2:]

	# loop through ordered list of years (e.g., 'lqtoBMu' or 'a2016')
	for i,year in enumerate(years): 

		yearCounter = i*nProcessesPerYear[year]
		sysPerYear[year] = {}

		# loop through ordered list of processes in each year (e.g., 'LQ_M_300' or 'sTop') and get the systematic for each
		for j, proc in enumerate(processesPerYear[year]):
			
			entry = entries[yearCounter+j]
			systematic = 0.0

			if entry == "-": pass
			elif "Signal" in proc and sysName == "PDF": pass
			else: systematic = (float(entry) - 1.0)
			sysPerYear[year][proc] = systematic

	return [sysName, sysPerYear]

def ParseStatLine(line,years,nProcessesPerYear,processesPerYear,ratesPerYear):

	# Dictionary to store all systematics, returned by function
	statPerYear = {}

	# First we get the name of a given source of systematic uncertainty (e.g., 'BTAG,' 'BTAG17,' 'LUMI16Uncorr,' 'LUMI1718,' 'LUMICorr,' or 'PDF')
	statName = line.split()[0]

	# Just the statistical uncertainties (remove stat name, 'gmN' flag, and event counts)
	entries = line.split()[3:]

	# Event counts
	events = line.split()[2]

	# loop through ordered list of years (e.g., 'lqtoBMu' or 'a2016')
	for i,year in enumerate(years):
		yearCounter = i*nProcessesPerYear[year]
		statPerYear[year] = {}

		# loop through ordered list of processes in each year (e.g., 'LQ_M_300' or 'sTop') and get the systematic for each
		for j,proc in enumerate(processesPerYear[year]):

			entry = entries[yearCounter+j]
			statUp = 0.0
			statDown = 0.0

			if entry == "-": pass
			elif ratesPerYear[year][proc] < 0.00001 or float(events) == 0.0: statUp = float(entry)
			else: 
				statUp = ratesPerYear[year][proc]*math.sqrt(1.0/float(events))
				statDown = statUp 
			statPerYear[year][proc] = {"up": statUp, "down": statDown}

	return [statName, statPerYear]

def AddBackgroundToRates(inputDict, mass):

	returnDict = deepcopy(inputDict)
	for year in inputDict:
		returnDict[year]["Background"] = Rate("Background", year, mass, dataType = "background")
		returnDict[year]["Background"].SetRate(sum([inputDict[year][process].GetRate() for process in inputDict[year] if inputDict[year][process].isBackground()]))

		returnDict[year]["Background"].SetStatHigh( math.sqrt(sum([inputDict[year][process].GetStatHigh()*inputDict[year][process].GetStatHigh() for process in inputDict[year] if inputDict[year][process].isBackground()])) )
		returnDict[year]["Background"].SetStatLow( math.sqrt(sum([inputDict[year][process].GetStatLow()*inputDict[year][process].GetStatHigh() for process in inputDict[year] if inputDict[year][process].isBackground()])) )

		sysNames = inputDict[year][list(inputDict[year].keys())[0]].GetSysNames()
		for sysName in sysNames:
			if returnDict[year]["Background"].GetRate() < 0.0001: 
				returnDict[year]["Background"].AddRelSys(sysName, 0.0)
			else:
				returnDict[year]["Background"].AddRelSys(sysName, sum([inputDict[year][process].GetRelSys(sysName)*inputDict[year][process].GetRate() for process in inputDict[year] if inputDict[year][process].isBackground()])/returnDict[year]["Background"].GetRate())

	return returnDict

def AddYearCombinationToRates(inputDict):

	returnDict = {}
	returnDict["Combined"] = {}
	initYear = list(inputDict.keys())[0]
	for process in inputDict[initYear]:
		returnDict["Combined"][process] = Rate(process, "combined", inputDict[initYear][process].GetMass(), dataType = inputDict[initYear][process].GetDataType())
		for year in inputDict:
			returnDict["Combined"][process].CombineRates( deepcopy(inputDict[year][process]) )

	returnDict.update(inputDict)

	return returnDict

def AddProcessCombinationToRates(inputDict, proc1, proc2):
	
	newName = str(proc1)+"/"+str(proc2)
	returnDict = deepcopy(inputDict)
	for year in inputDict:
		returnDict[year][newName] = deepcopy(inputDict[year][proc1])
		returnDict[year][newName].CombineRates( deepcopy(inputDict[year][proc2]) )

	return returnDict

def GetData(card):
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
	processYears = []
	nProcessesPerYear = {}
	processesPerYear = {}
	allRates = {}
	allSystematics = {}
	allStats = {}

	returnDict = {}

	# loop through each line in datacard and fill dictionary with data
	for line in card:

		title = line.split()[0]

		# Get the LQ mass point and decay channel of the datacard
		if '.txt' in title:
			mass = title.split('_')[-1].split('.')[0]

		# Get the bin names (e.g., 'lqtoBMu' or 'a2016')
		# Bins are ordered so use a list here
		if 'bin' in title and not binFlag:
			years = [b.strip('a') if "c" in globYear or "C" in globYear else globYear for b in line.split()[1:]]
			binFlag = True

		if 'observation' in title:
			observationsPerYear = {year: obs for year, obs in zip(years,line.split()[1:])}

		# Get number of processes per bin
		if 'bin' in title and binFlag:
			processYears = [b.strip('a') if "c" in globYear or "C" in globYear else globYear for b in line.split()[1:]]
			nProcessesPerYear = collections.Counter(processYears)
		
		# Get the process names in each bin (e.g., 'LQ_M_300' or 'sTop')
		# Processes are ordered so use lists here
		if 'process' in title and not processFlag:
			for year in nProcessesPerYear:
				processesPerYear[year] = []
				for i, process in enumerate(line.split()[1:]):
					if "LQ" in process and processYears[i] == year:
						processesPerYear[year].append("Signal")
					elif processYears[i] == year:
						processesPerYear[year].append(process)
			#processesPerYear = {year: [proc for i, proc in enumerate(line.split()[1:]) if processYears[i] == year] for year in nProcessesPerYear}
			processFlag = True

		# Store the rates for each year and process
		if 'rate' in title:
			ratesPerYear = ParseRateLine(line,years,nProcessesPerYear,processesPerYear)

		# Store the systematic uncertainties for each year and process
		if 'lnN' in line:
			[sysName, systematicsPerYear] = ParseSystematicLine(line,years,nProcessesPerYear,processesPerYear,ratesPerYear)
			allSystematics[sysName] = systematicsPerYear

		# Store the statistical uncertainties for each year and process (up and down)
		if 'gmN' in line:
			[statName, statsPerYear] = ParseStatLine(line,years,nProcessesPerYear,processesPerYear,ratesPerYear)
			allStats[statName] = statsPerYear

	# Compile all info into a single dictionary filled with Rate objects
	for year in years:

		# Set observed data
		returnDict[year] = {}
		returnDict[year]["Data"] = Rate("Data", year, mass, dataType = "data")
		returnDict[year]["Data"].SetRate(float(observationsPerYear[year]))
		returnDict[year]["Data"].SetStatHigh(math.sqrt(float(observationsPerYear[year])))
		returnDict[year]["Data"].SetStatLow(math.sqrt(float(observationsPerYear[year])))

		# Get signal and background rates and add systematics
		for process in processesPerYear[year]:

			# Set Rates
			if "Signal" in process: returnDict[year][process] = Rate(process, year, mass, dataType = "signal")
			else: returnDict[year][process] = Rate(process, year, mass, dataType = "background")
			returnDict[year][process].SetRate(ratesPerYear[year][process])
			
			# Set Stats
			statUp = 0.0
			statDown = 0.0
			for statName in allStats:
				statUp += allStats[statName][year][process]["up"]*allStats[statName][year][process]["up"]
				statDown += allStats[statName][year][process]["down"]*allStats[statName][year][process]["down"]
			returnDict[year][process].SetStatHigh(math.sqrt(statUp))
			returnDict[year][process].SetStatLow(math.sqrt(statDown))

			# Set systematics
			for sysName in allSystematics:
				returnDict[year][process].AddRelSys(sysName, allSystematics[sysName][year][process])

	# Add the total background to the dictionary
	returnDict = AddBackgroundToRates(returnDict, mass)

	# Add the year combination to the dictionary
	returnDict = AddYearCombinationToRates(returnDict)

	# Combine TTV/VV and SingleTop/WJets DO THIS AFTER ADDING BACKGROUND TO RATES
	returnDict = AddProcessCombinationToRates(returnDict, "TTV", "VV")
	returnDict = AddProcessCombinationToRates(returnDict, "sTop", "WJets")

	return [mass, returnDict]

def ParseCards(enhancedSelCards,finalSelCards):

	# Loop through all the datacards
	# Make a prime dictionary where each key is the mass corresponding to a card
	# Values are systematics dictionaries for that card
	
	sysData = {}
	finalData = {}

	for card in enhancedSelCards:
		[sysMass, systematics] = GetData(card)
		sysData[sysMass] = systematics

	for card in finalSelCards:
		[finalMass, finalRates] = GetData(card)
		finalData[finalMass] = finalRates

	for mass in finalData:
		for year in finalData[mass]:
			for process in finalData[mass][year]:
				relSys = sysData[mass][year][process].GetAllRelSys()
				finalData[mass][year][process].SetAllRelSys(sysData[mass][year][process].GetAllRelSys())
				finalData[mass][year][process].CombineCorrelatedSys(baseSysNames)

	return finalData

def RatePlotLines(rates, masses):

	lines = ''
	step1_initMass = 300
	step1 = 100
	step2_initMass = 3000
	step2 = 500
	for mass in masses:
		lines += "# M = "+mass+'\n'
		if int(mass) <= step2_initMass: massBin = str( int((float(mass)-step1_initMass)/step1+1) )
		else: massBin = str( int((step2_initMass-step1_initMass)/step1+1) + int((float(mass)-step2_initMass-step2)/step2+1) )

		for process in rates[mass]["Combined"]:
			rate = round(rates[mass]["Combined"][process].GetRate(), 5)
			err = round(rates[mass]["Combined"][process].GetStatSysHigh(), 5)
			if "Signal" in process: hist = "sig"
			elif "ZJets" in process: hist = "zjets"
			elif "TTBar" in process: hist = "ttbar"
			elif "TTV" in process and "VV" in process: hist = "vvttv"
			elif "sTop" in process and "WJets" in process: hist = "st"
			elif "Background" in process: hist = "totBG"
			elif "Data" in process: hist = "data"
			else: continue
			lines += hist+'.SetBinContent('+massBin+','+str(rate)+')\n'
			lines += hist+'.SetBinError('+massBin+','+str(err)+')\n'

	return lines

def YieldsTable(rates, masses, year):
	from datetime import date

	if "c" in year or "C" in year:
		year = "Combined"
		labelYear = "combined"
		captionYear = "combined 2016, 2017, and 2018"
	else:
		captionYear = str(year)

	today = date.today().strftime("%m/%d/%y")

	cleanTable = '% ' + year + ' final selection event yields - ' + today + ' \n'
	cleanTable += r'\begin{table}[htbp]' + '\n'
	cleanTable += '\t' + r'\tiny' + '\n'
	cleanTable += '\t' + r'\begin{center}' + '\n'
	cleanTable += '\t\t' + r'\caption{Event yields in ' + captionYear + r' data at the final selection level. Uncertainties are statistical unless otherwise indicated.}' + '\n'
	cleanTable += '\t\t' + r'\begin{tabular}{cccccccc}' + '\n'
	cleanTable += '\t\t\t' + r'\hline\hline \\' + '\n'
	cleanTable += '\t\t\t' + r'\MLQ & Signal (stat + sys) & \ZJETS & \ttbar & \TTV & \VV & single top & All BG (stat + sys) & Data \\ \hline' + '\n'

	for mass in masses:
		
		sigYield 	= str(round(rates[mass][year]["Signal"].GetRate(), 2)) 
		zjetsYield 	= str(round(rates[mass][year]["ZJets"].GetRate(), 2)) 
		ttbarYield 	= str(round(rates[mass][year]["TTBar"].GetRate(), 2)) 
		ttvYield	= str(round(rates[mass][year]["TTV"].GetRate(), 2)) 
		vvYield 	= str(round(rates[mass][year]["VV"].GetRate(), 2)) 
		wjetsYield 	= str(round(rates[mass][year]["WJets"].GetRate(), 2)) 
		stYield 	= str(round(rates[mass][year]["sTop"].GetRate(), 2)) 
		bkgYield 	= str(round(rates[mass][year]["Background"].GetRate(), 2)) 
		dataYield 	= str(int(rates[mass][year]["Data"].GetRate())) 

		sigStatErrHigh	 	= str(round(rates[mass][year]["Signal"].GetStatHigh(), 2)) 
		zjetsStatErrHigh 	= str(round(rates[mass][year]["ZJets"].GetStatHigh(), 2)) 
		ttbarStatErrHigh 	= str(round(rates[mass][year]["TTBar"].GetStatHigh(), 2)) 
		ttvStatErrHigh		= str(round(rates[mass][year]["TTV"].GetStatHigh(), 2)) 
		vvStatErrHigh 		= str(round(rates[mass][year]["VV"].GetStatHigh(), 2)) 
		wjetsStatErrHigh	= str(round(rates[mass][year]["WJets"].GetStatHigh(), 2)) 
		stStatErrHigh 		= str(round(rates[mass][year]["sTop"].GetStatHigh(), 2)) 
		bkgStatErrHigh 		= str(round(rates[mass][year]["Background"].GetStatHigh(), 2)) 
		dataStatErrHigh 	= str(round(rates[mass][year]["Data"].GetStatHigh(), 2)) 

		sigStatErrLow 	= str(round(rates[mass][year]["Signal"].GetStatLow(), 2))
		zjetsStatErrLow = str(round(rates[mass][year]["ZJets"].GetStatLow(), 2))
		ttbarStatErrLow = str(round(rates[mass][year]["TTBar"].GetStatLow(), 2))
		ttvStatErrLow 	= str(round(rates[mass][year]["TTV"].GetStatLow(), 2))
		vvStatErrLow 	= str(round(rates[mass][year]["VV"].GetStatLow(), 2))
		wjetsStatErrLow	= str(round(rates[mass][year]["WJets"].GetStatLow(), 2))
		stStatErrLow 	= str(round(rates[mass][year]["sTop"].GetStatLow(), 2))
		bkgStatErrLow 	= str(round(rates[mass][year]["Background"].GetStatLow(), 2))
		dataStatErrLow 	= str(round(rates[mass][year]["Data"].GetStatLow(), 2))

		if sigStatErrLow == sigStatErrHigh: 
			sigStat = ' \pm ' + sigStatErrHigh
		else:
			sigStat = '_{-' + sigStatErrLow + '}^{+' + sigStatErrHigh + '}'
		if zjetsStatErrLow == zjetsStatErrHigh: 
			zjetsStat = ' \pm ' + zjetsStatErrHigh
		else:
			zjetsStat = '_{-' + zjetsStatErrLow + '}^{+' + zjetsStatErrHigh + '}'
		if ttbarStatErrLow == ttbarStatErrHigh: 
			ttbarStat = ' \pm ' + ttbarStatErrHigh
		else:
			ttbarStat = '_{-' + ttbarStatErrLow + '}^{+' + ttbarStatErrHigh + '}'
		if ttvStatErrLow == ttvStatErrHigh: 
			ttvStat = ' \pm ' + ttvStatErrHigh
		else:
			ttvStat = '_{-' + ttvStatErrLow + '}^{+' + ttvStatErrHigh + '}'
		if vvStatErrLow == vvStatErrHigh: 
			vvStat = ' \pm ' + vvStatErrHigh
		else:
			vvStat = '_{-' + vvStatErrLow + '}^{+' + vvStatErrHigh + '}'
		if wjetsStatErrLow == wjetsStatErrHigh: 
			wjetsStat = ' \pm ' + wjetsStatErrHigh
		else:
			wjetsStat = '_{-' + wjetsStatErrLow + '}^{+' + wjetsStatErrHigh + '}'
		if stStatErrLow == stStatErrHigh: 
			stStat = ' \pm ' + stStatErrHigh
		else:
			stStat = '_{-' + stStatErrLow + '}^{+' + stStatErrHigh + '}'
		if bkgStatErrLow == bkgStatErrHigh: 
			bkgStat = ' \pm ' + bkgStatErrHigh
		else:
			bkgStat = '_{-' + bkgStatErrLow + '}^{+' + bkgStatErrHigh + '}'

		sigSys = str(round(rates[mass][year]["Signal"].GetSys("Total"), 2)) 
		bkgSys = str(round(rates[mass][year]["Background"].GetSys("Total"), 2)) 

		sig		= '$' + sigYield	+ sigStat	+ ' \pm ' + sigSys + '$'
		zjets	= '$' + zjetsYield	+ zjetsStat	+ '$'
		ttbar	= '$' + ttbarYield	+ ttbarStat	+ '$'
		ttv		= '$' + ttvYield	+ ttvStat	+ '$'
		vv		= '$' + vvYield		+ vvStat	+ '$'
		wjets	= '$' + wjetsYield	+ wjetsStat	+ '$'
		st		= '$' + stYield		+ stStat	+ '$'
		bkg		= '$' + bkgYield	+ bkgStat	+ ' \pm ' + bkgSys + '$'
		data	= '$' + dataYield	+ '$'

		cleanTable += '\t\t\t' + mass + " & " + sig + " & " + zjets + " & " + ttbar + " & " + ttv + " & " + vv + " & " + st + " & " + bkg + " & " + data + r" \\" + "\n"

	cleanTable = cleanTable.rstrip() 
	cleanTable += r' \hline\hline' + '\n'
	cleanTable += '\t\t' + r'\end{tabular}' + '\n'
	cleanTable += '\t\t' + r'\label{tab:eventyields' + labelYear + '}\n'
	cleanTable += '\t' + r'\end{center}' + '\n'
	cleanTable += r'\end{table}'

	return cleanTable
	
def SystematicsTable(rates, mass, sysList, sysNames, year):
	from datetime import date

	year = str(year)
	mass = str(mass)

	if "c" in year or "C" in year:
		year = "Combined"
		labelYear = "combined"
		captionYear = "combined 2016, 2017, and 2018"
	else:
		captionYear = year
		labelYear = year

	today = date.today().strftime("%m/%d/%y")

	sysTable = '% ' + year + ' systematic uncertainties M = ' + mass + ' - ' + today + ' \n'
	sysTable += r'\begin{table}[htbp]' + '\n'
	sysTable += '\t' + r'\begin{center}' + '\n'
	sysTable += '\t\t' + r'\caption{Systematic uncertainties in ' + captionYear + r' signal acceptance and background yields at $\MLQ = \SI{' + mass + r'}{\GeV}$ final selection.. The last two lines show the total systematic uncertainty and the total statistical uncertainty in the simulated samples, respectively.}' + '\n'
	sysTable += '\t\t' + r'\begin{tabular}{lcc}' + '\n'
	sysTable += '\t\t\t' + r'\hline\hline' + '\n'
	sysTable += '\t\t\t' + r'Uncertainty & Signal (\%) & Background (\%) \\ \hline' + '\n'

	sigSysNames = rates[mass][year]["Signal"].GetAllRelSys()
	bkgSysNames = rates[mass][year]["Background"].GetAllRelSys()	

	for sysName in sysList:

		sigSys = round(100*rates[mass][year]["Signal"].GetRelSys(sysName), 2)
		bkgSys = round(100*rates[mass][year]["Background"].GetRelSys(sysName), 2)

		if sysName in sigSysNames and sysName in bkgSysNames and "Total" not in sysName:
			if sysName in ["PDF","TOPPT","TTNORM","SHAPETT","VVNORM","SHAPEVV","ZNORM","SHAPEZ"]:
				sysTable += '\t\t\t' + sysNames[sysName] + ' & -- & ' + str(bkgSys) + r' \\' + '\n'
			else:
				sysTable += '\t\t\t' + sysNames[sysName] + ' & ' + str(sigSys) + ' & ' + str(bkgSys) + r' \\' + '\n'

	sigSysTotal = round(100*rates[mass][year]["Signal"].GetRelSys("Total"), 2)
	bkgSysTotal = round(100*rates[mass][year]["Background"].GetRelSys("Total"), 2)

	sigStatTotal = round(100*min(1.0,rates[mass][year]["Signal"].GetMaxRelStat()), 2)
	bkgStatTotal = round(100*min(1.0,rates[mass][year]["Background"].GetMaxRelStat()), 2)

	sysTable = sysTable.rstrip() 
	sysTable += r' \hline' + '\n'
	sysTable += '\t\t\t' + r'Total syst. uncertainty & ' + str(sigSysTotal) + ' & ' + str(bkgSysTotal) + r' \\ \hline' + '\n'
	sysTable += '\t\t\t' + r'Total stat. uncertainty & ' + str(sigStatTotal) + ' & ' + str(bkgStatTotal) + r' \\ \hline\hline' + '\n'
	sysTable += '\t\t' + r'\end{tabular}' + '\n'
	sysTable += '\t\t' + r'\label{tab:SysUncertainties_M' + mass + '_' + labelYear + '}\n'
	sysTable += '\t' + r'\end{center}' + '\n'
	sysTable += r'\end{table}'

	return sysTable




parser = ArgumentParser()
parser.add_argument("-y", "--year", dest="year", help="option to pick running year (2016,2017,2018,comb)", metavar="YEAR")
parser.add_argument("-e", "--enhanced", dest="sys", help="path to datacard for systematic uncertainties (enhanced selection)", metavar="SYS")
parser.add_argument("-f", "--final", dest="stat", help="path to datacard for statistical uncertainties (final selection)", metavar="STAT")
options = parser.parse_args()
globYear = str(options.year)
sysFile = str(options.sys)
statFile = str(options.stat)

sysInfo = [line for line in open(sysFile,'r')]
statInfo = [line for line in open(statFile,'r')]

sysCards = GetCards(sysInfo)
statCards = GetCards(statInfo)

massNames = ["300","400","500","600","700","800","900","1000","1100","1200","1300","1400","1500","1600","1700","1800","1900","2000","2100","2200","2300","2400","2500","2600","2700","2800","2900","3000","3500"]#,"4000"]
baseSysNames = ["BTAG","JER","JES","LUMI","MER","MES","MUONID","MUONISO","MUONRECO","MUONHLT","PREFIRE","PU","PDF","TOPPT","TTNORM","SHAPETT","VVNORM","SHAPEVV","ZNORM","SHAPEZ","Total"]
sysTableNames = {
	"BTAG": "b-jet tagging efficiency",
	"JER": "Jet energy resolution",
	"JES": "Jet energy scale",
	"LUMI": "Luminosity",
	"MER": "Muon energy resolution",
	"MES": "Muon energy scale",
	"MUONID": "Muon identification",
	"MUONISO": "Muon isolation",
	"MUONRECO": "Muon reconstruction",
	"MUONHLT": "Muon trigger",
	"PREFIRE": "Prefire weighting",
	"PU": "Pileup",
	"PDF": "PDF",
	"TOPPT": "Top \pt reweighting",
	"TTNORM": r"\ttbar normalization",
	"SHAPETT": r"\ttbar shape",
	"VVNORM": "Diboson normalization",
	"SHAPEVV": "Diboson shape",
	"ZNORM": "\ZJETS normalization ",
	"SHAPEZ": "\ZJETS shape"
}

allRates = ParseCards(sysCards,statCards)

# Print tables here
# print YieldsTable(allRates, massNames, "Combined")
print SystematicsTable(allRates, "1800", baseSysNames, sysTableNames, "Combined")
#print RatePlotLines(allRates, massNames)