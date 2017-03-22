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

jer=[999.,0.]
jes=[999.,0.]
lumi=[999.,0.]
align=[999.,0.]
mer=[999.,0.]
mes=[999.,0.]
muid=[999.,0.]
pdf=[999.,0.]
pu=[999.,0.]
ttnorm=[999.,0.]
ttshape=[999.,0.]
trig=[999.,0.]
wnorm=[999.,0.]
wshape=[999.,0.]
znorm=[999.,0.]
zshape=[999.,0.]

jerSig=[999.,0.]
jesSig=[999.,0.]
lumiSig=[999.,0.]
alignSig=[999.,0.]
merSig=[999.,0.]
mesSig=[999.,0.]
muidSig=[999.,0.]
pdfSig=[999.,0.]
puSig=[999.,0.]
ttnormSig=[999.,0.]
ttshapeSig=[999.,0.]
trigSig=[999.,0.]
wnormSig=[999.,0.]
wshapeSig=[999.,0.]
znormSig=[999.,0.]
zshapeSig=[999.,0.]
gotToBetaHalf=False
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
			if 'BetaHalf' in line: gotToBetaHalf=True

		if 'rate' in line:
			vals = line.split()
			signal = float(vals[1])
			backgrounds = [float(x) for x in vals[2:]]
			background_total = sum(backgrounds)
		if 'lnN' in line:
			global gotToBetaHalf
			vals = line.split()

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


			r_b=float(relative_b)
			r_s=float(relative_s)
			sysname = vals[0]
			sysname = sysname.replace('NORM',' Normalization')
			if 'SHAPE' in sysname:
				sysname = sysname.replace('SHAPE','') + ' Shape'
			sysnames.append(sysname)
			#if float(mass)>1500 : continue
			if gotToBetaHalf==True : continue
			print sysname
			if 'TT Shape' in sysname:
				if r_b < ttshape[0]:ttshape[0]=r_b
				if r_b > ttshape[1]:ttshape[1]=r_b
				if r_s < ttshapeSig[0]:ttshapeSig[0]=r_s
				if r_s > ttshapeSig[1]:ttshapeSig[1]=r_s
			if 'W Shape' in sysname:
				if r_b < wshape[0]:wshape[0]=r_b
				if r_b > wshape[1]:wshape[1]=r_b
				if r_s < wshapeSig[0]:wshapeSig[0]=r_s
				if r_s > wshapeSig[1]:wshapeSig[1]=r_s
			if 'Z Shape' in sysname:
				if r_b < zshape[0]:zshape[0]=r_b
				if r_b > zshape[1]:zshape[1]=r_b
				if r_s < zshapeSig[0]:zshapeSig[0]=r_s
				if r_s > zshapeSig[1]:zshapeSig[1]=r_s
			if 'TT Normalization' in sysname:
				if r_b < ttnorm[0]:ttnorm[0]=r_b
				if r_b > ttnorm[1]:ttnorm[1]=r_b
				if r_s < ttnormSig[0]:ttnormSig[0]=r_s
				if r_s > ttnormSig[1]:ttnormSig[1]=r_s
			if 'W Normalization' in sysname:
				if r_b < wnorm[0]:wnorm[0]=r_b
				if r_b > wnorm[1]:wnorm[1]=r_b
				if r_s < wnormSig[0]:wnormSig[0]=r_s
				if r_s > wnormSig[1]:wnormSig[1]=r_s
			if 'Z Normalization' in sysname:
				if r_b < znorm[0]:znorm[0]=r_b
				if r_b > znorm[1]:znorm[1]=r_b
				if r_s < znormSig[0]:znormSig[0]=r_s
				if r_s > znormSig[1]:znormSig[1]=r_s
			if sysname == 'MUONIDISO':
				sysname = 'Muon ID/Iso'
				if r_b < muid[0]:muid[0]=r_b
				if r_b > muid[1]:muid[1]=r_b
				if r_s < muidSig[0]:muidSig[0]=r_s
				if r_s > muidSig[1]:muidSig[1]=r_s
			if sysname == 'MUONHLT': 
				sysname = 'Trigger'
				if r_b < trig[0]:trig[0]=r_b
				if r_b > trig[1]:trig[1]=r_b
				if r_s < trigSig[0]:trigSig[0]=r_s
				if r_s > trigSig[1]:trigSig[1]=r_s
			if sysname == 'ALIGN':
				sysname = 'Misalignment'
				if r_b < align[0]:align[0]=r_b
				if r_b > align[1]:align[1]=r_b
				if r_s < alignSig[0]:alignSig[0]=r_s
				if r_s > alignSig[1]:alignSig[1]=r_s

			if sysname == 'JES':
				sysname = 'Jet Energy Scale'
				if r_b < jes[0]:jes[0]=r_b
				if r_b > jes[1]:jes[1]=r_b
				if r_s < jesSig[0]:jesSig[0]=r_s
				if r_s > jesSig[1]:jesSig[1]=r_s
			if sysname == 'JER':
				sysname = 'Jet Energy Resolution'
				if r_b < jer[0]:jer[0]=r_b
				if r_b > jer[1]:jer[1]=r_b
				if r_s < jerSig[0]:jerSig[0]=r_s
				if r_s > jerSig[1]:jerSig[1]=r_s
			if sysname == 'MES':
				sysname = 'Muon Energy Scale'
				if r_b < mes[0]:mes[0]=r_b
				if r_b > mes[1]:mes[1]=r_b
				if r_s < mesSig[0]:mesSig[0]=r_s
				if r_s > mesSig[1]:mesSig[1]=r_s
			if sysname == 'MER':
				sysname = 'Muon Energy Resolution'
				if r_b < mer[0]:mer[0]=r_b
				if r_b > mer[1]:mer[1]=r_b
				if r_s < merSig[0]:merSig[0]=r_s
				if r_s > merSig[1]:merSig[1]=r_s
			if sysname == 'PU':
				sysname = 'PileUp'
				if r_b < pu[0]:pu[0]=r_b
				if r_b > pu[1]:pu[1]=r_b
				if r_s < puSig[0]:puSig[0]=r_s
				if r_s > puSig[1]:puSig[1]=r_s

			if sysname == 'LUMI': 
				sysname = 'Lumi'
				if r_b < lumi[0]:lumi[0]=r_b
				if r_b > lumi[1]:lumi[1]=r_b
				if r_s < lumiSig[0]:lumiSig[0]=r_s
				if r_s > lumiSig[1]:lumiSig[1]=r_s

			if sysname == 'PDF': 
				if r_b < pdf[0]:pdf[0]=r_b
				if r_b > pdf[1]:pdf[1]=r_b
				if r_s < pdfSig[0]:pdfSig[0]=r_s
				if r_s > pdfSig[1]:pdfSig[1]=r_s




	textable = '\\begin{table}[htbp]\n\\begin{center}\n'
	textable += '\\caption{Systematic uncertainties and their effects on signal ($S$) and background ($B$) in the '+chan+' channel for $M_{LQ}='+mass+'$~GeV final selection. All uncertainties are symmetric.}\n'
	textable += '\\begin{tabular}{|lcc|}\n\\hline\n'

	textable += 'Systematic & Signal (\%) & Background (\%) \\\\ \\hline \n'
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

#this is temporary to remove incorrect systematics which are too high#	signalsystematics2=[]
#	for x in signalsystematics:
#		if float(x)<9:
#			signalsystematics2.append(x)
#	backgroundsystematics2=[]
#	for x in backgroundsystematics:
#		if float(x)<20:
#			backgroundsystematics2.append(x)
#
#	systot_s = str(round(100*(math.sqrt( (sum([float(x)*float(x)*.01*.01  for x in signalsystematics2 ])) )),2))
#	systot_b = str(round(100*(math.sqrt( (sum([float(x)*float(x)*.01*.01  for x in backgroundsystematics2 ])) )),2))

	systot_s = str(round(100*(math.sqrt( (sum([float(x)*float(x)*.01*.01  for x in signalsystematics ])) )),2))
	systot_b = str(round(100*(math.sqrt( (sum([float(x)*float(x)*.01*.01  for x in backgroundsystematics ])) )),2))
	textable += '\\hline\n Total & '+systot_s + ' & ' + systot_b + '\\\\ \\hline\n'
	textable += '\\end{tabular}\n\\label{tab:SysUncertainties_'+texchan+'_'+mass+'}\n\\end{center}\n\\end{table}\n\n'

	# if '300' in mass or '500' in mass or '700' in mass or '1000' in mass:
	#if '400' in mass or '650' in mass:
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

for x in [jer,jes,lumi,align,mer,mes,muid,pdf,pu,trig,ttnorm,ttshape,wnorm,wshape,znorm,zshape,jerSig,jesSig,lumiSig,alignSig,merSig,mesSig,muidSig,pdfSig,puSig,trigSig,ttnormSig,ttshapeSig,wnormSig,wshapeSig,znormSig,zshapeSig] :
	if x[0]==999.0: x[0]=0.0

print 'Range of systematics:'
print 'systematic, Signal min - max, BACKGROUND min - max'
print 'Jet Energy Resolution  ', jerSig[0],'-',jerSig[1],'  ,  ',jer[0],'-',jer[1]
print 'Jet Energy Scale       ', jesSig[0],'-',jesSig[1],'  ,  ',jes[0],'-',jes[1]
print 'Lumi                   ', lumiSig[0],'-',lumiSig[1],'  ,  ',lumi[0],'-',lumi[1]
print 'Misalignment           ', alignSig[0],'-',alignSig[1],'  ,  ',align[0],'-',align[1]
print 'Muon Energy Resolution ', merSig[0],'-',merSig[1],'  ,  ',mer[0],'-',mer[1]
print 'Muon Energy Scale      ', mesSig[0],'-',mesSig[1],'  ,  ',mes[0],'-',mes[1]
print 'Muon ID/Iso            ', muidSig[0],'-',muidSig[1],'  ,  ',muid[0],'-',muid[1]
print 'PDF                    ', pdfSig[0],'-',pdfSig[1],'  ,  ',pdf[0],'-',pdf[1]
print 'PileUp                 ', puSig[0],'-',puSig[1],'  ,  ',pu[0],'-',pu[1]
print 'Trigger                ', trigSig[0],'-',trigSig[1],'  ,  ',trig[0],'-',trig[1]
print 'TT Normalization       ', ttnormSig[0],'-',ttnormSig[1],'  ,  ',ttnorm[0],'-',ttnorm[1]
print 'TT Shape               ', ttshapeSig[0],'-',ttshapeSig[1],'  ,  ',ttshape[0],'-',ttshape[1]
print 'W Normalization        ', wnormSig[0],'-',wnormSig[1],'  ,  ',wnorm[0],'-',wnorm[1]
print 'W Shape                ', wshapeSig[0],'-',wshapeSig[1],'  ,  ',wshape[0],'-',wshape[1]
print 'Z Normalization        ', znormSig[0],'-',znormSig[1],'  ,  ',znorm[0],'-',znorm[1]
print 'Z Shape                ', zshapeSig[0],'-',zshapeSig[1],'  ,  ',zshape[0],'-',zshape[1]
