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



def cardtotex(card):
	# print '  --------------------------------------------------   '
	sysnames = []
	signalsystematics = []
	backgroundsystematics = []
	signal_totals  =[]
	for line in card:
		if '.txt' in line:
			mass = line.split('_')[-1].split('.')[0]
			chan = '$\\mu \\mu jj$'*('BetaHalf' not in line) + '$\\mu \\nu jj$'*('BetaHalf' in line) 
			texchan = 'uujj'*('BetaHalf' not in line) + 'uvjj'*('BetaHalf'  in line) 

		if 'rate' in line:
			vals = line.split()
			signal = float(vals[1])
			backgrounds = [float(x) for x in vals[2:]]
			background_total = sum(backgrounds)
		if 'lnN' in line:
			vals = line.split()
			sysname = vals[0]
			sysname = sysname.replace('NORM',' Normalization')
			if 'SHAPE' in sysname:
				sysname = sysname.replace('SHAPE','') + ' Shape'
			if sysname == 'MUONIDISO': sysname = 'Muon ID/Iso'
			if sysname == 'MUONHLT': sysname = 'Trigger'

			if sysname == 'ALIGN': sysname = 'Misalignment'

			if sysname == 'JES': sysname = 'Jet Energy Scale'
			if sysname == 'JER': sysname = 'Jet Energy Resolution'
			if sysname == 'MES': sysname = 'Muon Energy Scale'
			if sysname == 'MER': sysname = 'Muon Energy Resolution'
			if sysname == 'PU': sysname = 'PileUp'

			if sysname == 'LUMI': sysname = 'Lumi'


			signalsystemativalue = float(vals[2]) - 1.0
			backgroundsystematicvalues = [float(x)-1.0 for x in vals[3:]]
			variation=0
			for b in range(len(backgroundsystematicvalues)):
				variation += backgroundsystematicvalues[b]*backgrounds[b]
			relative_b = 0
			if background_total >  0 :
				relative_b = variation/background_total
			relative_s = 0
			if signal > 0:
				relative_s = signalsystemativalue
			relative_b = str(round(100*relative_b, 2))
			relative_s = str(round(100*relative_s, 2))

			signalsystematics.append(relative_s)
			backgroundsystematics.append(relative_b)
			sysnames.append(sysname)



	textable = '\\begin{table}[htbp]\n\\begin{center}\n'
	textable += '\\caption{Systematic uncertainties and their effects on signal ($S$) and background ($B$) in the '+chan+' channel for $M_{LQ}='+mass+'$~GeV final selection. All uncertainties are symmetric.}\n'
	textable += '\\begin{tabular}{|lcc|}\n\\hline\n'

	textable += 'Systematc & Signal (\%) & Background (\%) \\\\ \\hline \n'
	textablelines = []
	for s in range(len(sysnames)):
		ss = signalsystematics[s]
		if ss == '0.0': ss = '--'
		bb = backgroundsystematics[s]
		if bb == '0.0': bb = '--'		
		textableline = sysnames[s] + ' & ' + ss + ' & '+bb+ '\\\\ \n'
		textablelines.append(textableline)
	
	textablelines.sort()
	for tt in textablelines:
		textable += tt

	systot_s = str(round(100*(math.sqrt( (sum([float(x)*float(x)*.01*.01  for x in signalsystematics ])) )),2))
	systot_b = str(round(100*(math.sqrt( (sum([float(x)*float(x)*.01*.01  for x in backgroundsystematics ])) )),2))
	textable += '\\hline\n Total & '+systot_s + ' & ' + systot_b + '\\\\ \\hline\n'
	textable += '\\end{tabular}\n\\label{tab:SysUncertainties_'+texchan+'_'+mass+'}\n\\end{center}\n\\end{table}\n\n'

	if '300' in mass or '500' in mass or '700' in mass or '1000' in mass:
		print textable
	return [mass,str(round(float(systot_b),2)) ]

totinfo = []
for card in cards:
	totinfo.append(cardtotex(card))

sysuncs = []
syslist = ''
for t in totinfo:
	syslist += t[1]+', '
	sysuncs.append(t[1])
# print syslist
# for t in totinfo:
# 	print t[0] ,' & '+t[1]

print 'List of systematics for each card considered:'
print syslist

print '\n Deliniation of systematics list'

for ii in range(len(totinfo)):
	print cards[ii][0].replace('\n',''), sysuncs[ii]