import os
import sys
import math

sysfile = sys.argv[1]

year = sysfile.split('/')[-1].split('_')[-1].split('.')[0]

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

lumis=[]
lumi16s=[]
lumi17s=[]
lumi18s=[]
lumi1718s=[]
jers=[]
jess=[]
aligns=[]
mers=[]
mess=[]
muids=[]
muisos=[]
murecos=[]
pdfs=[]
pus=[]
prefires=[]
ttnorms=[]
ttshapes=[]
trigs=[]
wnorms=[]
wshapes=[]
znorms=[]
zshapes=[]
vvshapes=[]
hips=[]
btags=[]
toppts=[]

lumi=[999.,0.]
lumi16=[999.,0.]
lumi17=[999.,0.]
lumi18=[999.,0.]
lumi1718=[999.,0.]
jer=[999.,0.]
jes=[999.,0.]
align=[999.,0.]
mer=[999.,0.]
mes=[999.,0.]
muid=[999.,0.]
muiso=[999.,0.]
mureco=[999.,0.]
pdf=[999.,0.]
pu=[999.,0.]
prefire=[999.,0.]
ttnorm=[999.,0.]
ttshape=[999.,0.]
trig=[999.,0.]
wnorm=[999.,0.]
wshape=[999.,0.]
znorm=[999.,0.]
zshape=[999.,0.]
vvshape=[999.,0.]
hip=[999.,0.]
btag=[999.,0.]
toppt=[999.,0.]

lumiSig=[999.,0.]
lumi16Sig=[999.,0.]
lumi17Sig=[999.,0.]
lumi18Sig=[999.,0.]
lumi1718Sig=[999.,0.]
jerSig=[999.,0.]
jesSig=[999.,0.]
alignSig=[999.,0.]
merSig=[999.,0.]
mesSig=[999.,0.]
muidSig=[999.,0.]
muisoSig=[999.,0.]
murecoSig=[999.,0.]
pdfSig=[999.,0.]
puSig=[999.,0.]
prefireSig=[999.,0.]
ttnormSig=[999.,0.]
ttshapeSig=[999.,0.]
trigSig=[999.,0.]
wnormSig=[999.,0.]
wshapeSig=[999.,0.]
znormSig=[999.,0.]
zshapeSig=[999.,0.]
vvshapeSig=[999.,0.]
hipSig=[999.,0.]
btagSig=[999.,0.]
topptSig=[999.,0.]

systot = []
systotSig = []

lumiBkgForLumiTot = []
lumiSigForLumiTot = []
lumi16BkgForLumiTot = []
lumi16SigForLumiTot = []
lumi17BkgForLumiTot = []
lumi17SigForLumiTot = []
lumi18BkgForLumiTot = []
lumi18SigForLumiTot = []
lumi1718BkgForLumiTot = []
lumi1718SigForLumiTot = []
lumiTotBkg = []
lumiTotSig = []

gotToBetaHalf=False
def cardtotex(card):
	# print '  --------------------------------------------------   '
	sysnames = []
	signalsystematics = []
	backgroundsystematics = []
	signal_totals  =[]
	lumi_totals = []
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

			#sysname = sysname.replace('NORM',' Normalization')
			#if 'SHAPE' in sysname:
			#	sysname = sysname.replace('SHAPE','') + ' Shape'
			
			#if float(mass)>1500 : continue
			if gotToBetaHalf==True : continue #== for mumujj, != for munujj, commented out for both
			#print sysname
                        #if mass=='2300': continue
                        #if mass=='2900': continue
			if sysname == 'LUMICorr': 
				sysname = 'LUMICorr'
				if r_b < lumi[0]:lumi[0]=r_b
				if r_b > lumi[1]:lumi[1]=r_b
				if r_s < lumiSig[0]:lumiSig[0]=r_s
				if r_s > lumiSig[1]:lumiSig[1]=r_s
				lumis.append(r_b)
				lumiBkgForLumiTot.append(r_b) 
				lumiSigForLumiTot.append(r_s)
			if sysname == 'LUMI16Uncorr':
				sysname = 'LUMI16Uncorr'
				if r_b < lumi16[0]:lumi16[0]=r_b
				if r_b > lumi16[1]:lumi16[1]=r_b
				if r_s < lumi16Sig[0]:lumi16Sig[0]=r_s
				if r_s > lumi16Sig[1]:lumi16Sig[1]=r_s
				lumi16s.append(r_b)
				lumi16BkgForLumiTot.append(r_b) 
				lumi16SigForLumiTot.append(r_s)
			if sysname == 'LUMI17Uncorr': 
				sysname = 'LUMI17Uncorr'
				if r_b < lumi17[0]:lumi17[0]=r_b
				if r_b > lumi17[1]:lumi17[1]=r_b
				if r_s < lumi17Sig[0]:lumi17Sig[0]=r_s
				if r_s > lumi17Sig[1]:lumi17Sig[1]=r_s
				lumi17s.append(r_b)
				lumi17BkgForLumiTot.append(r_b) 
				lumi17SigForLumiTot.append(r_s)
			if sysname == 'LUMI18Uncorr': 
				sysname = 'LUMI18Uncorr'
				if r_b < lumi18[0]:lumi18[0]=r_b
				if r_b > lumi18[1]:lumi18[1]=r_b
				if r_s < lumi18Sig[0]:lumi18Sig[0]=r_s
				if r_s > lumi18Sig[1]:lumi18Sig[1]=r_s
				lumi18s.append(r_b)
				lumi18BkgForLumiTot.append(r_b) 
				lumi18SigForLumiTot.append(r_s)
			if sysname == 'LUMI1718': 
				sysname = 'LUMI1718'
				if r_b < lumi1718[0]:lumi1718[0]=r_b
				if r_b > lumi1718[1]:lumi1718[1]=r_b
				if r_s < lumi1718Sig[0]:lumi1718Sig[0]=r_s
				if r_s > lumi1718Sig[1]:lumi1718Sig[1]=r_s
				lumi1718s.append(r_b)
				lumi1718BkgForLumiTot.append(r_b) 
				lumi1718SigForLumiTot.append(r_s)
			if 'SHAPETT' in sysname:
				sysname = "SHAPETT"
				if r_b < ttshape[0]:ttshape[0]=r_b
				if r_b > ttshape[1]:ttshape[1]=r_b
				if r_s < ttshapeSig[0]:ttshapeSig[0]=r_s
				if r_s > ttshapeSig[1]:ttshapeSig[1]=r_s
				ttshapes.append(r_b)
			#if 'SHAPEW' in sysname:
			#	sysname = "SHAPEW"
			#	if r_b < wshape[0]:wshape[0]=r_b
			#	if r_b > wshape[1]:wshape[1]=r_b
			#	if r_s < wshapeSig[0]:wshapeSig[0]=r_s
			#	if r_s > wshapeSig[1]:wshapeSig[1]=r_s
			#	wshapes.append(r_b)
			if 'SHAPEZ' in sysname:
				sysname = "SHAPEZ"
				if r_b < zshape[0]:zshape[0]=r_b
				if r_b > zshape[1]:zshape[1]=r_b
				if r_s < zshapeSig[0]:zshapeSig[0]=r_s
				if r_s > zshapeSig[1]:zshapeSig[1]=r_s
				zshapes.append(r_b)
			if 'SHAPEVV' in sysname:
				sysname = "SHAPEVV"
				if r_b < vvshape[0]:vvshape[0]=r_b
				if r_b > vvshape[1]:vvshape[1]=r_b
				if r_s < vvshapeSig[0]:vvshapeSig[0]=r_s
				if r_s > vvshapeSig[1]:vvshapeSig[1]=r_s
				vvshapes.append(r_b)
			if 'TTNORM' in sysname:
				sysname = "TTNORM"
				if r_b < ttnorm[0]:ttnorm[0]=r_b
				if r_b > ttnorm[1]:ttnorm[1]=r_b
				if r_s < ttnormSig[0]:ttnormSig[0]=r_s
				if r_s > ttnormSig[1]:ttnormSig[1]=r_s
				ttnorms.append(r_b)
			#if 'WNORM' in sysname:
			#	sysname = "WNORM"
			#	if r_b < wnorm[0]:wnorm[0]=r_b
			#	if r_b > wnorm[1]:wnorm[1]=r_b
			#	if r_s < wnormSig[0]:wnormSig[0]=r_s
			#	if r_s > wnormSig[1]:wnormSig[1]=r_s
			#	wnorms.append(r_b)
			if 'ZNORM' in sysname:
				sysname = "ZNORM"
				if r_b < znorm[0]:znorm[0]=r_b
				if r_b > znorm[1]:znorm[1]=r_b
				if r_s < znormSig[0]:znormSig[0]=r_s
				if r_s > znormSig[1]:znormSig[1]=r_s
				znorms.append(r_b)
			if 'MUONID' in sysname:
				sysname = 'MUONID'
				if r_b < muid[0]:muid[0]=r_b
				if r_b > muid[1]:muid[1]=r_b
				if r_s < muidSig[0]:muidSig[0]=r_s
				if r_s > muidSig[1]:muidSig[1]=r_s
				muids.append(r_b)
			if 'MUONISO' in sysname:
				sysname = 'MUONISO'
				if r_b < muiso[0]:muiso[0]=r_b
				if r_b > muiso[1]:muiso[1]=r_b
				if r_s < muisoSig[0]:muisoSig[0]=r_s
				if r_s > muisoSig[1]:muisoSig[1]=r_s
				muisos.append(r_b)
			if 'MUONHLT' in sysname: 
				sysname = 'MUONHLT'
				if r_b < trig[0]:trig[0]=r_b
				if r_b > trig[1]:trig[1]=r_b
				if r_s < trigSig[0]:trigSig[0]=r_s
				if r_s > trigSig[1]:trigSig[1]=r_s
				trigs.append(r_b)
			if 'MUONRECO' in sysname:
				sysname = 'MUONRECO'
				if r_b < mureco[0]:mureco[0]=r_b
				if r_b > mureco[1]:mureco[1]=r_b
				if r_s < murecoSig[0]:murecoSig[0]=r_s
				if r_s > murecoSig[1]:murecoSig[1]=r_s
				murecos.append(r_b)
			#if 'ALIGN':
			#	sysname = 'Misalignment'
			#	if r_b < align[0]:align[0]=r_b
			#	if r_b > align[1]:align[1]=r_b
			#	if r_s < alignSig[0]:alignSig[0]=r_s
			#	if r_s > alignSig[1]:alignSig[1]=r_s
			#	aligns.append(r_b)
			if 'JES' in sysname:
				sysname = 'JES'
				if r_b < jes[0]:jes[0]=r_b
				if r_b > jes[1]:jes[1]=r_b
				if r_s < jesSig[0]:jesSig[0]=r_s
				if r_s > jesSig[1]:jesSig[1]=r_s
				jess.append(r_b)
			if 'JER' in sysname:
				sysname = 'JER'
				if r_b < jer[0]:jer[0]=r_b
				if r_b > jer[1]:jer[1]=r_b
				if r_s < jerSig[0]:jerSig[0]=r_s
				if r_s > jerSig[1]:jerSig[1]=r_s
				jers.append(r_b)
			if 'MES' in sysname:
				sysname = 'MES'
				if r_b < mes[0]:mes[0]=r_b
				if r_b > mes[1]:mes[1]=r_b
				if r_s < mesSig[0]:mesSig[0]=r_s
				if r_s > mesSig[1]:mesSig[1]=r_s
				mess.append(r_b)
			if 'MER' in sysname:
				sysname = 'MER'
				if r_b < mer[0]:mer[0]=r_b
				if r_b > mer[1]:mer[1]=r_b
				if r_s < merSig[0]:merSig[0]=r_s
				if r_s > merSig[1]:merSig[1]=r_s
				mers.append(r_b)
			if 'PU' in sysname:
				sysname = 'PU'
				if r_b < pu[0]:pu[0]=r_b
				if r_b > pu[1]:pu[1]=r_b
				if r_s < puSig[0]:puSig[0]=r_s
				if r_s > puSig[1]:puSig[1]=r_s
				pus.append(r_b)
			if 'PDF' in sysname:
				sysname = "PDF"
				if r_b < pdf[0]:pdf[0]=r_b
				if r_b > pdf[1]:pdf[1]=r_b
				if r_s < pdfSig[0]:pdfSig[0]=r_s
				if r_s > pdfSig[1]:pdfSig[1]=r_s
				pdfs.append(r_b)
			#if 'HIP' in sysname:
			#	if r_b < hip[0]:hip[0]=r_b
			#	if r_b > hip[1]:hip[1]=r_b
			#	if r_s < hipSig[0]:hipSig[0]=r_s
			#	if r_s > hipSig[1]:hipSig[1]=r_s
			#	hips.append(r_b)
			if 'BTAG' in sysname:
				sysname = "BTAG"
				if r_b < btag[0]:btag[0]=r_b
				if r_b > btag[1]:btag[1]=r_b
				if r_s < btagSig[0]:btagSig[0]=r_s
				if r_s > btagSig[1]:btagSig[1]=r_s
				btags.append(r_b)
			if 'TOPPT' in sysname:
				sysname = "TOPPT"
				if r_b < toppt[0]:toppt[0]=r_b
				if r_b > toppt[1]:toppt[1]=r_b
				if r_s < topptSig[0]:topptSig[0]=r_s
				if r_s > topptSig[1]:topptSig[1]=r_s
				toppts.append(r_b)
			if 'PREFIRE' in sysname:
				sysname = "PREFIRE"
				if r_b < prefire[0]:prefire[0]=r_b
				if r_b > prefire[1]:prefire[1]=r_b
				if r_s < prefireSig[0]:prefireSig[0]=r_s
				if r_s > prefireSig[1]:prefireSig[1]=r_s
				prefires.append(r_b)
			sysnames.append(sysname)

	# Get the total luminosity by adding in quadriture the correlated, partially correlated, and uncorrelated components

	for i in range(len(lumiBkgForLumiTot)):
		bkgTot = lumiBkgForLumiTot[i]*lumiBkgForLumiTot[i]
		sigTot = lumiSigForLumiTot[i]*lumiSigForLumiTot[i]

		if len(lumi16BkgForLumiTot) == 0:
			pass
		else:
			bkgTot += lumi16BkgForLumiTot[i]*lumi16BkgForLumiTot[i]
			sigTot += lumi16SigForLumiTot[i]*lumi16SigForLumiTot[i]
		if len(lumi17BkgForLumiTot) == 0:
			pass
		else:
			bkgTot += lumi17BkgForLumiTot[i]*lumi17BkgForLumiTot[i]
			sigTot += lumi17SigForLumiTot[i]*lumi17SigForLumiTot[i]
		if len(lumi18BkgForLumiTot) == 0:
			pass
		else:
			bkgTot += lumi18BkgForLumiTot[i]*lumi18BkgForLumiTot[i]
			sigTot += lumi18SigForLumiTot[i]*lumi18SigForLumiTot[i]
		if len(lumi1718BkgForLumiTot) == 0:
			pass
		else:
			bkgTot += lumi1718BkgForLumiTot[i]*lumi1718BkgForLumiTot[i]
			sigTot += lumi1718SigForLumiTot[i]*lumi1718SigForLumiTot[i]
		bkgTot = round(math.sqrt(bkgTot), 2)
		sigTot = round(math.sqrt(sigTot), 2)
		lumiTotBkg.append(bkgTot)
		lumiTotSig.append(sigTot)

	for i,sys in enumerate(lumiTotBkg):
		if sys < 0.0: lumiTotBkg[i] = 0.0
	for i,sys in enumerate(lumiTotSig):
		if sys < 0.0: lumiTotSig[i] = 0.0

	lumiTotBkgSorted = sorted(lumiTotBkg)
	lumiTotSigSorted = sorted(lumiTotSig)

	textable = r'%'+year+r'% %'+mass+r'%'+'\n'
	textable += '\\begin{table}[htbp]\n\\begin{center}\n'
	textable += '\\caption{Systematic uncertainties and their effects on signal ($S$) and background ($B$) in '+year+' for $M_{LQ}='+mass+'$~GeV final selection. All uncertainties are symmetric.}\n'
	textable += '\\begin{tabular}{lcc}\n\\hline\\hline\n'

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
	textable += 'Total & '+systot_s + ' & ' + systot_b + '\\\\ \\hline \\hline\n'
	textable += '\\end{tabular}\n\\label{tab:SysUncertainties_'+texchan+'_'+mass+'}\n\\end{center}\n\\end{table}\n\n'
	systotSig.append(systot_s)
	systot.append(systot_b)
	# if '300' in mass or '500' in mass or '700' in mass or '1000' in mass:
	#if '400' in mass or '650' in mass:
	print textable

	with open(sysTableTex,'a') as outtex:
		outtex.write(textable)

	return [mass,str(round(float(systot_b),2)) ]

sysTableTex = ''
sysTableTex += sysfile.strip(sysfile.split('/')[-1]).strip('/')
if sysTableTex == '':
	sysTableTex = '.'
else:
	sysTableTex += '/SysTables_'+year+'.tex'

with open(sysTableTex,'w') as outtex:
	pass

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

for x in [jer,jes,lumi,lumi16,lumi17,lumi18,lumi1718,align,mer,mes,muid,muiso,mureco,pdf,pu,prefire,trig,hip,btag,ttnorm,ttshape,wnorm,wshape,znorm,zshape,vvshape,toppt,jerSig,jesSig,lumiSig,lumi16Sig,lumi17Sig,lumi18Sig,lumi1718Sig,alignSig,merSig,mesSig,muidSig,muisoSig,murecoSig,pdfSig,puSig,prefireSig,trigSig,hipSig,btagSig,ttnormSig,ttshapeSig,wnormSig,wshapeSig,znormSig,zshapeSig,vvshapeSig,topptSig] :
	if x[0]==999.0: x[0]=0.0


SysRangeTable = '\\begin{table}[htbp]\n\\begin{center}\n'
SysRangeTable += '\\caption{Range of systematic uncertainties on signal (Sig.) and background (Bkg.) in '+year+'.}\n'
SysRangeTable += '\\begin{tabular}{lcc}\n\\hline\\hline\n'
SysRangeTable += 'Systematic		&  Sig. (min - max) [\%] &  Bkg. (min - max) [\%] ' + r' \\ \hline' + '\n'
SysRangeTable += 'b-jet tagging		& ' + str(btagSig[0]) + '-' + str(btagSig[1]) + ' & ' + str(btag[0]) + '-' + str(btag[1]) + r' \\' + '\n'
SysRangeTable += 'Jet energy resolution  	& ' + str(jerSig[0]) + '-' + str(jerSig[1]) + ' & ' + str(jer[0]) + '-' + str(jer[1]) + r' \\' + '\n'
SysRangeTable += 'Jet energy scale       	& ' + str(jesSig[0]) + '-' + str(jesSig[1]) + ' & ' + str(jes[0]) + '-' + str(jes[1]) + r' \\' + '\n'
#if year == '2016': SysRangeTable += 'Luminosity (uncorrelated) & ' + str(lumi16Sig[0]) + '-' + str(lumi16Sig[1]) + ' & ' + str(lumi16[0]) + '-' + str(lumi16[1]) + r' \\' + '\n'
#if year == '2017': SysRangeTable += 'Luminosity (uncorrelated) & ' + str(lumi17Sig[0]) + '-' + str(lumi17Sig[1]) + ' & ' + str(lumi17[0]) + '-' + str(lumi17[1]) + r' \\' + '\n'
#if year == '2018': SysRangeTable += 'Luminosity (uncorrelated) & ' + str(lumi18Sig[0]) + '-' + str(lumi18Sig[1]) + ' & ' + str(lumi18[0]) + '-' + str(lumi18[1]) + r' \\' + '\n'
#if year == '2017': SysRangeTable += 'Luminosity (2018-correlated)   & ' + str(lumi1718Sig[0]) + '-' + str(lumi1718Sig[1]) + ' & ' + str(lumi1718[0]) + '-' + str(lumi1718[1]) + r' \\' + '\n'
#if year == '2018': SysRangeTable += 'Luminosity (2017-correlated)   & ' + str(lumi1718Sig[0]) + '-' + str(lumi1718Sig[1]) + ' & ' + str(lumi1718[0]) + '-' + str(lumi1718[1]) + r' \\' + '\n'
#SysRangeTable += 'Luminosity (fully-correlated) 	& ' + str(lumiSig[0]) + '-' + str(lumiSig[1]) + ' & ' + str(lumi[0]) + '-' + str(lumi[1]) + r' \\' + '\n'
SysRangeTable += 'Luminosity		 		& ' + str(lumiTotSig[0]) + '-' + str(lumiTotSig[-1]) + ' & ' + str(lumiTotBkg[0]) + '-' + str(lumiTotBkg[-1]) + r' \\' + '\n'
SysRangeTable += 'Muon energy resolution 	& ' + str(merSig[0]) + '-' + str(merSig[1]) + ' & ' + str(mer[0]) + '-' + str(mer[1]) + r' \\' + '\n'
SysRangeTable += 'Muon energy scale      	& ' + str(mesSig[0]) + '-' + str(mesSig[1]) + ' & ' + str(mes[0]) + '-' + str(mes[1]) + r' \\' + '\n'
SysRangeTable += 'Muon trigger           	& ' + str(trigSig[0]) + '-' + str(trigSig[1]) + ' & ' + str(trig[0]) + '-' + str(trig[1]) + r' \\' + '\n'
SysRangeTable += 'Muon identification    	& ' + str(muidSig[0]) + '-' + str(muidSig[1]) + ' & ' + str(muid[0]) + '-' + str(muid[1]) + r' \\' + '\n'
SysRangeTable += 'Muon isolation         	& ' + str(muisoSig[0]) + '-' + str(muisoSig[1]) + ' & ' + str(muiso[0]) + '-' + str(muiso[1]) + r' \\' + '\n'
SysRangeTable += 'Muon reconstruction    	& ' + str(murecoSig[0]) + '-' + str(murecoSig[1]) + ' & ' + str(mureco[0]) + '-' + str(mureco[1]) + r' \\' + '\n'
SysRangeTable += 'PDF                    	& ' + str(pdfSig[0]) + '-' + str(pdfSig[1]) + ' & ' + str(pdf[0]) + '-' + str(pdf[1]) + r' \\' + '\n'
SysRangeTable += 'Prefire weighting			& ' + str(prefireSig[0]) + '-' +  str(prefireSig[1]) + ' & ' + str(prefire[0]) + '-' +  str(prefire[1]) + r' \\' + '\n'
SysRangeTable += 'Pileup                	& ' + str(puSig[0]) + '-' + str(puSig[1]) + ' & ' + str(pu[0]) + '-' + str(pu[1]) + r' \\' + '\n'
SysRangeTable += 'TT shape               	& ' + str(ttshapeSig[0]) + '-' + str(ttshapeSig[1]) + ' & ' + str(ttshape[0]) + '-' + str(ttshape[1]) + r' \\' + '\n'
SysRangeTable += 'Diboson shape          	& ' + str(vvshapeSig[0]) + '-' + str(vvshapeSig[1]) + ' & ' + str(vvshape[0]) + '-' + str(vvshape[1]) + r' \\' + '\n'
SysRangeTable += 'Z shape                	& ' + str(zshapeSig[0]) + '-' + str(zshapeSig[1]) + ' & ' + str(zshape[0]) + '-' + str(zshape[1]) + r' \\' + '\n'
SysRangeTable += 'Top $p_T$ reweighting     & ' + str(topptSig[0]) + '-' + str(topptSig[1]) + ' & ' + str(toppt[0]) + '-' + str(toppt[1]) + r' \\' + '\n'
SysRangeTable += 'TT normalization       	& ' + str(ttnormSig[0]) + '-' + str(ttnormSig[1]) + ' & ' + str(ttnorm[0]) + '-' + str(ttnorm[1]) + r' \\' + '\n'
SysRangeTable += 'Z normalization        	& ' + str(znormSig[0]) + '-' + str(znormSig[1]) + ' & ' + str(znorm[0]) + '-' + str(znorm[1]) + r' \\ \hline\hline' + '\n'
#SysRangeTable += 'Total                 	& ' + str(systotSig[0]) + '-' + str(systotSig[-1]) + ' & ' + str(systot[0]) + '-' + str(systot[-1]) + r' \\ \hline\hline' + '\n'
SysRangeTable += '\\end{tabular}\n\\label{tab:SysRanges'+year+'}\n\\end{center}\n\\end{table}\n\n'

print '\n'
print SysRangeTable

with open(sysTableTex.replace('SysTables','SysRangesTable'),'w') as outFile:
	outFile.write(SysRangeTable)

#print '\n\n'
systos = ['jers','jess','lumis','lumi16s','lumi17s','lumi18s','lumi1718s','aligns','mers','mess','muids','muisos','pdfs','pus','prefires','ttnorms','ttshapes','trigs','wnorms','wshapes','znorms','zshapes','vvshapes','hips','btags','toppts']
i=0
for x in [jers,jess,lumis,lumi16s,lumi17s,lumi18s,lumi1718s,aligns,mers,mess,muids,muisos,pdfs,pus,prefires,ttnorms,ttshapes,trigs,wnorms,wshapes,znorms,zshapes,vvshapes,hips,btags,toppts]:
	print systos[i],'= ',
	i=i+1
	print x
