#################################################################################################
##########                    N Tuple Analyzer Script Producer                        ###########
##########      Store NTuple Info In NTupleInfo.csv File in current Directory         ###########
##########      Darin Baumgartel - May 31, 2011 - darin.carl.baumgartel@cern.ch      ###########
#################################################################################################

import os # For direcory scanning abilities, etc
from time import strftime
import sys
import random
import time

print 'Importing root...',
from ROOT import *
print '   ... done.'


a = sys.argv
tagname = 'default'
json = ''
dopdf = '0'
nsplit = 25
bq = '1nd'
override_dir = ''

helpmessage = 'OPTIONS SUMMARY: \n -i  CSVFILE.csv \n -py ANALYZER.py \n -t  TAGNAME (optional) [default "default"] ' 
helpmessage += '\n -j  JSONFILE (needed, but ignored for MC) \n -p  0 or 1 (optional boolean to store PDF uncertainties in trees) [default 0] \n -q  Batch Queue (optional) [default "1nd"] '
helpmessage += ' \n -d  /path/to/directory (optional override output dir, use only when you have incomplete output in exisitng dir) '
helpmessage += ' \n -s 25  (number of files to analyzer per batch job)'
helpmessage += ' \n -h  (show this message)'
helpmessage += '\n'
for x in range(len(a)):
	if a[x] == '-i':
		ifile = a[x+1]
	if a[x] == '-py':
		pyfile = a[x+1]
	if a[x] == '-t':
		tagname = a[x+1]
	if a[x] == '-j':
		json = a[x+1]
	if a[x] == '-p':
		dopdf = a[x+1]
	if a[x] == '-s':
		nsplit = int(a[x+1])
	if a[x] == '-q':
		bq = (a[x+1])
	if a[x] == '-d':
		override_dir = (a[x+1])
	if a[x] == '--help':
		print helpmessage
		sys.exit()
	if a[x] == '-h':
		print helpmessage
		sys.exit()

if pyfile == ''  or ifile == '' or json == '':
	print 'Must specify input python script, .csv file, and json file, e.g.:\n\npython AnalyzerMakerFast.py -i NTupleInfoSpring2011.csv -py NTupleAnalyzer.py \n   Exiting   \n\n'
	sys.exit()

import csv
csvfile = open(ifile,'r')
table=[]

for row in csv.reader(csvfile):
	if len(row) == 0:
		continue
	if row[0][0]=='#':
		continue
	table.append(row)
for r in range(1,len(table)):
	for c in range(1,len(table[0])):
		table[r][c]=(table[r][c])
table2= map(list,zip(*table[1:]))
for x in range(0,len(table2)):
	exec (table[0][x]+'='+`table2[x]`)	

###----------------------------------------------------------------------###


c2file = pyfile.split('/')[-1]

now=str(strftime("%Y-%m-%d-%H:%M:%S"))
now = now.replace(" ","")
now = now.replace("\t","")
now = now.replace("-","_")
now = now.replace(":","_")

# initialize file that stores root processes to be run

f_sub = open("sub_AllAnalyzer.csh", 'w')
f_sub.write('#!/bin/csh')


thisdir = os.popen('pwd').readlines()[0].replace('\n','')
person = os.popen('whoami').readlines()[0].replace('\n','')
thiseos = thisdir+'/'+c2file.replace('.py','')+'_'+tagname+'_'+now


if override_dir != '':
	if override_dir[-1] == '/':
		override_dir = override_dir[:-1]
	if '/' not in override_dir:
		override_dir = thisdir + '/'+override_dir
	thiseos = override_dir


os.system(' mkdir '+ thiseos)
print ' \n-------------------------------------------------------------------'
bjobs = []

possiblemasterdirs = []
mastersubdirs = []
posdir = ''
mastersubdirs = EOSDirectory
#print mastersubdirs
for p in EOSDirectory[0]:
	posdir += p
	possiblemasterdirs.append(posdir)
#print possiblemasterdirs	
masterdir = ''
for p in possiblemasterdirs:
	isgood=1
	for c in EOSDirectory:
		if p not in c:
			isgood = 0
	if isgood==1 and p[-1]=='/':
		masterdir=p
#print masterdir
print '\n\n Reading File List, please wait ...\n\n'


def IsNotCorruptionTest(afile):
	# print afile
	isGood = True
	f = TFile.Open(afile,'READ')
	isGood = '0x(nil)' not in str(f)
	if isGood==True:
		strh=str(f.Get('h_counts'))
		# if 'ROOT.TObject' in strh:
		# 	isGood=False
		# else:
		# 	nent = f.Get('h_counts').GetEntries()
		# 	# print nent
		# 	isGood = nent>0
		f.Close()
	# print isGood
	return isGood


def GetGoodFiles(edir):

	print 'Getting eos info...'
	def GetSpaceUse():
		#print 'edir',edir
		#command =  'cmsLs -R '+edir + '| grep root | grep -v failed'
		command =  '/afs/cern.ch/project/eos/installation/0.3.121-aquamarine/bin/eos.select find '+edir + '| grep root | grep -v failed'
		dircont = [ x.replace('\n','') for x in os.popen(command).readlines()]
		print 'Total files (', len(dircont),') reduced to ',
		
		gooddircont = []
		for d in dircont:
			#print d
			isgoodcont = False
			for mm in mastersubdirs:
				# print mm
				if mm in d:
					gooddircont.append(d)	
					break	
			# sys.exit()
		print len(gooddircont),'.'
		# sys.exit()
		return gooddircont

	i = GetSpaceUse()
	print 'Done.'

	def identifier(f):
		fsp = f.split('_')
		i = ''
		for x in range(len(fsp)):
			i += fsp[x] + '_'
			if x > (len(fsp)-4):
				break
		return i
	files = []
	Ni = len(i)
	ni = 0
	for x in i:
		ni += 1
		print ni,'of',Ni
		#print x
		if ".root" not in x:
			continue
		x = x.split()
		#print x
		newCommand = '/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls -l '+x[-1]
		lsDashL =  os.popen(newCommand).readlines()
		#print lsDashL[0]
		pieces = lsDashL[0].split()
		#print pieces
		size=int(pieces[4])#size is size of file, now taken as eos ls -l of eos find result - stupid and slow but it works....
		#size = int(x[0])#was 1
		name = x[-1]
		if '/eos/cms' in name:
			name = name[8:]
		#print name
		ident = identifier(name)
		# goodeval = IsNotCorruptionTest('root://eoscms//eos/cms/'+name)
		# goodeval = IsNotCorruptionTest('~/eos/cms'+name)
		goodeval = True
		print name,goodeval
		if goodeval == True:
			files.append([size,name,ident])
		time.sleep(.0075)#fixme todo Morse added because eos

	checkedfiles = []


	def checkid(f):
		checkedfiles = []
		goodfiles = []
		dups = []
		for x in files:
			if x[-2]==f[-2]:
				dups.append(x)
				checkedfiles.append(x)

		maxsize = -1	
		for x in checkedfiles:
			if x[0]>maxsize:
				maxsize=x[0]
			 	bestfile=x

		for c in checkedfiles:
			if c == bestfile:
				goodfiles.append(c[1])
				# print c[1]

		return [goodfiles,checkedfiles]

	allgoodfiles = []
	allcheckedfiles = []
	nfiles = len(files)
	for f in range(nfiles):
		if f%1 == 0: 
			print 'Checking file',f,' = ',files[f],' of',nfiles,'.'

		[gg,cc] = checkid(files[f])
		if files[f] not in allcheckedfiles:
			allgoodfiles += gg

		allcheckedfiles += cc

	return allgoodfiles

masterdirlist = masterdir.replace('/','__')+'.txt'

if masterdirlist not in os.listdir('.') or  '--FileRefresh' in sys.argv:
	print '\n','(Re)'*('--FileRefresh' in sys.argv)+'Generating file list',masterdirlist,' for files in ',masterdir,'\n'
	# allfiles = os.popen('cmsLs  -R '+masterdir+' | grep ".root" | awk \'{print $5}\'').readlines()
	_allfiles = GetGoodFiles(masterdir)
	print len(_allfiles)
	fmas = open(masterdirlist,'w')
	for x in _allfiles:
		fmas.write(x+'\n')
	fmas.close()
else:
	print '\n Reading files from: ',masterdirlist
	print '\n *** NOTE: You can refresh the file list at anytime with the argument: --FileRefresh\n\n'
	_allfiles = [line for line in open(masterdirlist,'r')]

blacklist = []
# blacklist = ['/store/group/phys_exotica/leptonsPlusJets/RootNtuple/eberry/RootNtuple-V00-03-09-Summer12MC_DYNJetsToLL_MG_20121104_171728/DY3JetsToLL_M-50_TuneZ2Star_8TeV-madgraph__Summer12_DR53X-PU_S10_START53_V7A-v1__AODSIM_17_2_9nV.root']
# blacklist.append('/store/group/phys_exotica/leptonsPlusJets/RootNtuple/eberry/RootNtuple-V00-03-09-Summer12MC_DYNJetsToLL_MG_20121104_171728/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph__Summer12_DR53X-PU_S10_START53_V7A-v1__AODSIM_426_1_dk8.root')
# blacklist.append('/store/group/phys_exotica/leptonsPlusJets/RootNtuple/darinb/RootNtuple-V00-03-08-Summer12MC_WJetsToLNu_Systematics_MG_20130103_171750/WJetsToLNu_matchingup_8TeV-madgraph-tauola__Summer12_DR53X-PU_S10_START53_V7A-v1__AODSIM_235_1_aqW.root')


allfiles = []
for a in _allfiles:
	if a.replace('\n','') not in blacklist:
		allfiles.append(a)

# sys.exit()

# thiseos = '/afs/cern.ch/work/d/darinb/NTupleAnalyzerV3/NTupleAnalyzer_quicktest_2012_11_27_19_12_31'

jobs = []

output_subfolders = [thiseos+'/outputdir'+str(random.randint(1,999999999)) for nnn in range(20)]
for f in output_subfolders:
	os.system('mkdir '+f)

for x in range(len(SignalType)):

	signal = SignalType[x]
	path = EOSDirectory[x]	
	sigma = Xsections[x]
	Norig = N_orig[x]
	group = Group[x]
	thisjson = json
	if len(CustomJson[x]) > 2:
		thisjson = CustomJson[x]


	fcont = []
	for subfile in allfiles:
		if path.replace('\n','') in subfile and signal in subfile:
			fcont.append(subfile)

	print 'Preparing '+ SignalType[x],':', len(fcont),'files.'

	for f in fcont:
		jobs.append('python '+pyfile.replace('\n','')+' -f '+f.replace('\n','').replace('//','/')+' -s '+sigma+' -n '+Norig+' -j '+thisjson + ' -l 1.0 -p '+dopdf+' -d '+random.choice(output_subfolders).replace('\n',''))

# Some NTuple sets have larger files then others. Avoid grouping of large files by shuffling. 
random.shuffle(jobs)

print 'Total file count: ',len(jobs)

def FolderizeOutput(MainFolder):
	foldername = MainFolder+'/outputdir'+str(random.randint(1,999999999))
	os.system('mkdir '+foldername)
	foldername += '/'
	mvs = ['mv '+MainFolder+'/'+x.replace('\n','') + ' '+foldername  for x in os.popen('ls '+MainFolder+' | grep -v Summary | grep txt').readlines()]
	mvs += ['mv '+MainFolder+'/'+x.replace('\n','') + ' '+foldername  for x in os.popen('ls '+MainFolder+' | grep -v Summary | grep root').readlines()]
	lenmvs = str(len(mvs))
	print 'Relocating '+lenmvs+' files to avoid afs directory limits.'
	nn=0
	for mv in mvs:
		nn+=1
		if nn%100 == 0:
			print 'Moved',nn,'of',lenmvs,'files.'
		os.system( mv )
	# os.system('mv '+MainFolder+'/*root '+foldername)
	# os.system('mv '+MainFolder+'/*txt '+foldername)
	# sys.exit()

def MakeJobs(njobs):
	Nj = 0

	jlist = []
	jstr = str(os.popen('find '+thiseos).readlines())
	for j in jobs:
		filesig1 = (((j.split(' -f ')[-1]).split(' ')[0]))
		#print filesig1
		filesig = filesig1.split('/')[-5]+'__'+filesig1.split('/')[-1].replace('.root','')#changed -2 to -5 to get dataset name instead of 0000
		#print filesig
		#print jstr
			# .replace('/','___').)replace('.root','')
		# print filesig
		if filesig not in jstr:
			# print '**', filesig
			# sys.exit()
			# print j
			jlist.append(j)
		# else:
		# 	print 'file found'

	bsubs = []

	jobgroups = []
	jobset = []
	nj=0

	bjq = bq
	#if len(jlist) < 1000:
	#	njobs = 5
	#if len(jlist) < 500:
	#	njobs = 3
	#	bjq = '8nh'
	#if len(jlist) < 200:
	#	njobs = 2
	#	bjq = '8nh'
	#if len(jlist) < 50:
	#	njobs = 1
	#	bjq = '8nh'

	for ii in range(len(jlist)):
		nj += 1
		if nj >= njobs:
			jobset.append(jlist[ii])
			jobgroups.append(jobset)
			jobset = []
			nj=0
		else:
			jobset.append(jlist[ii])
	if len(jobset)>0:
		jobgroups.append(jobset)

	print 'subbing: ',len(jobgroups),'jobs.'
	findircont =   str(os.popen('ls '+thiseos).readlines())
	# if '.txt' in findircont or '.root' in findircont:
	# 	FolderizeOutput(thiseos)

	# FolderizeOutput(thiseos)
	os.system('rm '+thiseos+'/subber_*.tcsh')
	for j in jobgroups:
		Nj += 1
		subber = open(thiseos+'/subber_'+str(Nj)+'.tcsh','w')
		#subber.write('#!/bin/tcsh\n\nscram project CMSSW CMSSW_5_3_18\ncd CMSSW_5_3_18/src\ncmsenv\ncd -\n\n')
		#subber.write('#!/bin/tcsh\n\nscram project CMSSW CMSSW_7_4_16\ncd CMSSW_7_4_16/src\ncmsenv\ncd -\n\n')
		subber.write('#!/bin/tcsh\n\nscram project CMSSW CMSSW_8_0_26_patch1\ncd CMSSW_8_0_26_patch1/src\ncmsenv\ncd -\n\n')
		subber.write('\ncp '+thisdir+'/'+pyfile+' .')
		subber.write('\ncp '+thisdir+'/'+json+' .')
		#subber.write('\ncp '+thisdir+'/*json .')
		#subber.write('\ncp '+thisdir+'/metFilterLists/* .')
		subber.write('\ncp '+thisdir+'/PU*root .\n\n')

		# if Nj*njobs>5000:
		# 	continue
		for x in j:
			subber.write(x+'\n')

		subber.close()
		os.system('chmod 777 '+thiseos+'/subber_'+str(Nj)+'.tcsh')

		#Morse
		#os.system( 'bsub -R "pool>40000" -q '+bjq+'  -o /dev/null -e /dev/null -J job_'+str(Nj)+'_'+now+' < '+thiseos+'/subber_'+str(Nj)+'.tcsh')
		os.system( 'bsub -R "pool>40000" -q '+bjq+'  -o '+thiseos+'_'+str(Nj)+' -e '+thiseos+'_'+str(Nj)+' -J job_'+str(Nj)+'_'+now+' < '+thiseos+'/subber_'+str(Nj)+'.tcsh')
		os.system('sleep 0.4')
		# sys.exit()

	return len(jlist)


keep_going = 1

while keep_going != 0:
	print 'Launching jobs...'
	keep_going = MakeJobs(nsplit)
	if keep_going == 0:
		break

	print 'Jobs remaining, waiting for jobs to finish'

	done=0
	ncheck = 0
	while done!=1:
		os.system('sleep 60')
		jobinfo = os.popen('bjobs -w | grep '+now).readlines()
		if 'PEND' not in str(jobinfo):
			ncheck += 1
		jobinfo = len(jobinfo)
		jobsleft = jobinfo -1
		if jobsleft == -1:
			done = 1
		if jobsleft>=0:
			print  str(jobsleft+1) +' jobs remaining.'

		if (ncheck > 2000) or ((ncheck>1250) and jobsleft<3):
			 print "\nJobs taking too long. Killing remaining jobs. \n"
			 os.system('bjobs -w | grep '+now+' |awk \'{if (NR!=1) print $1}\' | xargs bkill')
			 os.system('sleep 10')
			 break

os.system('rm '+thiseos+'/subber_*tcsh')
os.system('mkdir '+thiseos+'/logs')
os.system('mv '+thiseos+'_* '+thiseos+'/logs/')

#sys.exit()

findircont =   str(os.popen('ls '+thiseos).readlines())

if '.txt' in findircont or '.root' in findircont:
	FolderizeOutput(thiseos)

if '--merge' not in sys.argv:
	print "\nMerging not demanded. Finishing. Gather files with \'--merge\'\n"
	sys.exit()
	
print 'Merging results...'

if 'Counter' in pyfile:
	rms = []
	txtfiles = [x.split(thiseos+'/')[-1] for x in os.popen('find '+thiseos+' | grep txt').readlines()]
	# for t in txtfiles:
	# 	print t
	# 	sys.exit()
	countlog = open(thisdir+ '/'+ifile.replace('.','_EventCountLog.'),'w')
	for x in range(len(SignalType)):
		print 'Collecting results for',SignalType[x]
		subdirsig = EOSDirectory[x]
		subdirsig = subdirsig.split('/')
		subdir = subdirsig[-1]
		if subdir =='':
			subdir = subdirsig[-2]

		sigfiles = []
		print SignalType[x], subdir
		# sys.exit()
		for ftxt in txtfiles:
			#print SignalType[x],subdir,ftxt
			if SignalType[x] in ftxt:# and subdir in ftxt:
				sigfiles.append(ftxt)
		OCount = 0
		for s in sigfiles:
			# print 'cat '+thiseos+'/'+s
			scount = os.popen('cat '+thiseos+'/'+s).readlines()	
			if len(scount) < 1:
				rms.append('rm '+thiseos+'/'+s)
				scount = '0.0'
			else:
				scount = scount[0].replace(' ','')
			# scount = (os.popen('cat '+thiseos+'/'+s).readlines()[0]).replace(' ','')
			scount = scount.replace('\n','')
			scount = float(scount)
			OCount += scount

		Ostr = str(SignalType[x]) +' , '+ str(int(OCount))+'\n'
		countlog.write(Ostr)
	countlog.close()
	os.system('cat '+thisdir+ '/'+ifile.replace('.','_EventCountLog.'))
	print '\n\n\n'
	for r in rms:
		print r
		os.system(r)

	print 'Output is in ',thisdir+ '/'+ifile.replace('.','_EventCountLog.'),' ...'


def listsplit(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def splithadd(hstring):
	lscoms = hstring.split( ' ' )[2:]
	allfiles = []
	for a in lscoms:
		print a
		morefiles = files = [x.replace('\n','') for x in os.popen('find '+a).readlines()]
		allfiles += morefiles

	fileblocks = listsplit(allfiles,200)

	haddout = hstring.split( ' ' )[1]

	nn = 0
	haddouts = []
	for block in fileblocks:
		rmcoms = []
		nn +=1
		newhaddout = haddout.replace('.root','_part'+str(nn)+'.root')
		HADD = 'hadd '+newhaddout 
		for b in block:
			HADD += ' '+b
			rmcoms.append('rm '+b)
		os.system( HADD )
		if '--forceDelete' in sys.argv:
			for rmcom in rmcoms:
				os.system(rmcom)
		haddouts.append(newhaddout)

	finalhadd = 'hadd '+haddout 
	for hh in haddouts:
		finalhadd += ' '+hh
	os.system( finalhadd )
	os.system('rm '+thiseos+'/SummaryFiles/*part*root')

# sys.exit()

if 'Analyz' in pyfile:
	os.system('mkdir '+thiseos+'/SummaryFiles')	
	groups = []
	for x in range(len(SignalType)):
		if Group[x] not in groups:
			groups.append(Group[x])	
	haddstructure = []
	for g in groups:	

		allfiles = []
		haddstring = 'hadd '+thiseos+'/SummaryFiles/'+g+'.root'

		for x in range(len(SignalType)):
			if Group[x] != g:
				continue
			subdirsig = EOSDirectory[x]
			subdirsig = subdirsig.split('/')
			subdir = subdirsig[-1]
			if subdir =='':
				subdir = subdirsig[-2]

			#signifier = thiseos+'/output*/*'+subdir+'*'+SignalType[x]+'*.root'
			signifier = thiseos+'/output*/*'+SignalType[x]+'*.root'
			#signifier = thiseos+'/output*/*'+subdir+'*.root'
			haddstring += ' '+signifier

		for x in range(10):
			haddsring = haddstring.replace('//','/')

		splithadd(haddstring)
		os.system('rm '+thiseos+'/SummaryFiles/*part*root')



	print ('\n\n'+140*'*'+ '\n\n      Analysis Complete. A full set of output files can be found in  \n\n       '+thiseos+'/SummaryFiles\n')
	os.system('ls '+thiseos+'/SummaryFiles')
	print ('\n\n'+140*'*'+ '\n\n')
