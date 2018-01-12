import os
import sys
import math

sysfile = sys.argv[1]

info = [line for line in open(sysfile,'r')]

cards = []

card = []
for x in info:
	if '.txt' in x:
		if len(card) > 2:
			cards.append(card)
		card = []
		card.append(x)
	else:
		if len(x) > 2:
			card.append(x)
cards.append(card)



def syssummary(systab):
	tab = [list(i) for i in zip(*systab)]
	systematics = []
	for x in tab:
		systematic = 0
		for y in x:
			val= abs(float(y)-1.0)
			systematic += val**2
		systematic = math.sqrt(systematic)
		systematics.append(systematic)
	return systematics

from math import log10, floor


def cutoff_place(num):
	sig=2
	l = (num.split('.')[0])
	r = (num.split('.')[1])
	if len(l) >=2:
		return len(l)-3
	else:
		if l!='0':
			return -2
		else:
			nn =0
			for x in r:
				if x =='0':
					nn = nn -1
				else:
					return nn -3

def round_sig(x,sig):
	if x > 0.005:
		val = str(round(x, sig-int(floor(log10(x)))-1))
		return [val,cutoff_place(val)]
	else:
		return ['0.00',99]

def round_set(nums):
	cutoffs = []
	for n in nums:
		cutoffs.append(round_sig(n,2)[1])
	cutoff = -1*(min(cutoffs))-1 
	outputs = []
	for n in nums:
		newnum = str(round(n,cutoff))
		if newnum[-1] == '0' and newnum[-2]=='.' and len(newnum)>3:
			newnum = newnum.replace('.0','')

		outputs.append(newnum)
	return outputs

# print round_set([234.23434532452,2.9234523452345834,34.234523450234,0.078])
# print round_sig(3345.345)
# print round_sig(3.2092)
# print round_sig(.20932)
# print round_sig(.0003332)

# sys.exit()

def tableentryfromraw(rates, stats, syss,flagsys):
	r = 0
	st = [0,0]
	sy = 0

	for x in range(len(rates)):
		r += rates[x]
		sy += (syss[x]*rates[x])**2
		if rates[x]<0.000001:
			sterr = [0,stats[x][1]]
			#sterr = [0,stats[x][1]*1.14]#fixme why multiply by sqrt(2)????
		else:
			nomerr = math.sqrt(1.0/(1.0*stats[x][0]))*rates[x]
			sterr = [nomerr,nomerr]

		st[0] += sterr[0]**2
		st[1] += sterr[1]**2



	st[0] = math.sqrt(st[0])
	st[1] = math.sqrt(st[1])
	sy = math.sqrt(sy)

	values =  round_set([r,sy,st[0],st[1]])

	if values[2]==values[3]:
		statpart = ' $\\pm$ '+values[2]
	else:
		signchar = '-'
		# if (float(values[2]) == -1*float(values[2])):
		# 	signchar = ' '
		statpart = ' $ _{'+signchar+values[2]+'}^{+'+values[3]+'}$ '
	# tex += statpart + ' (stat)'

	tex = values[0] + statpart + ' '+ (' $\\pm$ '+values[1]+' ')*flagsys

	return tex

def cardtotex(card):
	# print '  --------------------------------------------------   '
	sysnames = []
	signalsystematics = []
	backgroundsystematics = []
	signal_totals  =[]
	systable = []
	staterrs = []
	for line in card:
		if 'observation' in line:
			data = line.split()[1]
		if '.txt' in line:
			mass = line.split('_')[-1].split('.')[0]
			chan = '$\\mu \\mu jj$'*('BetaHalf' not in line) + '$\\mu \\nu jj$'*('BetaHalf' in line) 
			texchan = 'uujj'*('BetaHalf' not in line) + 'uvjj'*('BetaHalf'  in line) 

		if 'process' in line and 'LQ' in line:
			backgroundnames = line.split()[2:]


		if 'rate' in line:
			vals = line.split()
			signal = float(vals[1])
			backgrounds = [float(x) for x in vals[2:]]

		if texchan == 'uujj':
			#backcols = [['Z+Jets',['ZJets']],['$\\ttbar$',['TTBar']],['Other BG',['WJets','sTop','VV','QCD']]]
			#backcols = [['Z+Jets',['ZJets']],['$\\ttbar$',['TTBar']],['W+Jets',['WJets']],['sTop',['sTop']],['VV',['VV']],['QCD',['QCD']]]
			backcols = [['Z+Jets',['ZJets']],['$\\ttbar$',['TTBar']],['W+Jets',['WJets']],['sTop',['sTop']],['VV',['VV']]]

		if texchan == 'uvjj':
			#backcols = [['W+Jets',['WJets']],['$\\ttbar$',['TTBar']],['Other BG',['ZJets','sTop','VV','QCD']]]
			#backcols = [['W+Jets',['WJets']],['$\\ttbar$',['TTBar']],['Z+Jets',['ZJets']],['sTop',['sTop']],['VV',['VV']],['QCD',['QCD']]]
			backcols = [['W+Jets',['WJets']],['$\\ttbar$',['TTBar']],['Z+Jets',['ZJets']],['sTop',['sTop']],['VV',['VV']]]


		if 'lnN' in line:
			sysline = [float(x) for x in line.split()[2:]]
			sysline.append(x)
			systable.append(sysline)

		if 'gmN' in line:
			staterr = []
			entry = line.split()
			for e in entry:
				if 'stat' not in e and 'gmN' not in e and '-' not in e:
					staterr.append(float(e))
			staterrs.append(staterr)

	systematics = syssummary(systable)

	rates = [signal]
	rates += backgrounds

	names = [mass]
	names += backgroundnames

	# print backgroundnames
	# print rates
	# print systematics
	# print staterrs

	# signalentry = [rates[0],staterrs[0]*rates[0], systematics[0]*rates[0]]


	__Sh = names[0]
	__S = tableentryfromraw([rates[0]],[staterrs[0]],[systematics[0]],0)

	tabhead = '$M_{LQ}$ & Signal & '
	tabline = mass+' & '+__S+' & '
	
	for b in backcols:
		__Bh = b[0]
		tabhead += __Bh+' & '
		btypes = b[1]
		__setrates = []
		__setstats = []
		__setsys = []
		for x in btypes:
			for y in range(len(names)):
				if x in names[y]:
					__setrates.append(rates[y])
					__setstats.append(staterrs[y])
					__setsys.append(systematics[y])
		__B = tableentryfromraw(__setrates,__setstats,__setsys,0)
		tabline += __B+' & '

	tabhead += ' All BG (stat + syst)& '
	__setrates = []
	__setstats = []
	__setsys = []

	for b in backcols:
		btypes = b[1]
		for x in btypes:
			for y in range(len(names)):
				if x in names[y]:
					__setrates.append(rates[y])
					__setstats.append(staterrs[y])
					__setsys.append(systematics[y])
	__B = tableentryfromraw(__setrates,__setstats,__setsys,1)
	tabline += __B+' & '

	tabhead += 'Data \\\\ \\hline'
	tabline += data +' \\\\'

	#print tabhead
	#print tabline


	return tabhead,tabline



totinfo = []
for card in cards:
	totinfo += cardtotex(card)

cleaninfo = []
for t in totinfo:
	t = t.replace('&','&@').split('@')
	if t not in cleaninfo:
		cleaninfo.append(t)


def fancyTable(arrays):

	def areAllEqual(lst):
		return not lst or [lst[0]] * len(lst) == lst

	if not areAllEqual(map(len, arrays)):
		exit('Cannot print a table with unequal array lengths.')


	verticalMaxLengths = [max(value) for value in map(lambda * x:x, *[map(len, a) for a in arrays])]

	spacedLines = []

	for array in arrays:
		spacedLine = ''
		for i, field in enumerate(array):
			diff = verticalMaxLengths[i] - len(field)
			spacedLine += field + ' ' * diff + '\t'
		spacedLines.append(spacedLine)

	return '\n'.join(spacedLines)

print fancyTable(cleaninfo)
