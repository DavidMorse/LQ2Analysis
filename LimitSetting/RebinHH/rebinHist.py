import os
import sys
import random
import time
import datetime
#os.system('source ~/root/bin/thisroot.sh')
import ROOT
from ROOT import *
import array as arr

# python rebinHist.py --resType HHres --channel ee -m 260 (--constbin 50)
# python rebinHist.py --resType HHres --channel uu --noSyst --linear

channel   = ''
resType   = ''
domass      = ''
nBinconst = ''
for x in range(len(sys.argv)):
	if sys.argv[x] == '--channel':
		channel = sys.argv[x+1] # 'ee', 'uu'
	if sys.argv[x] == '--resType':
		resType = sys.argv[x+1] # 'HHres', 'HHBulkGrav'
	if sys.argv[x] == '-m':
		domass = sys.argv[x+1]
	if sys.argv[x] == '--constbin':
		nBinconst = sys.argv[x+1]

hasData  = True
plotData = False
zoomplot = False
doNoSyst = False
p_linear = False
if '--blindData' in sys.argv:
	hasData = False # for blind cards, set this to False
if '--plotData' in sys.argv:
	plotData = True
if '--zoom' in sys.argv:
	zoomplot = True
if '--noSyst' in sys.argv:
	doNoSyst = True
if '--linear' in sys.argv:
	p_linear = True


ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)


_mass = ["260","270","300","350","400", "450", "500",  "550",  "600",  "650", "750", "800", "900", "1000"]

primdir = 'rootfiles_final/rootfiles_final_' + channel + '/'
outdir    = primdir + "newbinning"
outdirpdf = primdir + "newbinning_pdf"
if (nBinconst != ''):
	outdir    += "_" + nBinconst + "bins"
	outdirpdf += "_" + nBinconst + "bins"
else:
	outdir    += "_xbins"
	outdirpdf += "_xbins"
os.system("mkdir " + outdir)
os.system("mkdir " + outdirpdf)
if zoomplot:
	outdirpdf_z = outdirpdf+'_zoom'
	os.system("mkdir " + outdirpdf_z)
if p_linear:
	outdirpdf_lin = outdirpdf+'_linear'
	os.system("mkdir " + outdirpdf_lin)

#nsyst_ELECRON = 75
tagSyst_ELECRON = ["","JESAbsoluteMPFBiasUp","JESAbsoluteMPFBiasDown","JESAbsoluteScaleUp","JESAbsoluteScaleDown","JESAbsoluteStatUp","JESAbsoluteStatDown","JESFlavorQCDUp","JESFlavorQCDDown","JESFragmentationUp","JESFragmentationDown","JESPileUpDataMCUp","JESPileUpDataMCDown","JESPileUpPtBBUp","JESPileUpPtBBDown","JESPileUpPtEC1Up","JESPileUpPtEC1Down","JESPileUpPtEC2Up","JESPileUpPtEC2Down","JESPileUpPtHFUp","JESPileUpPtHFDown","JESPileUpPtRefUp","JESPileUpPtRefDown","JESRelativeBalUp","JESRelativeBalDown","JESRelativeFSRUp","JESRelativeFSRDown","JESRelativeJEREC1Up","JESRelativeJEREC1Down","JESRelativeJEREC2Up","JESRelativeJEREC2Down","JESRelativeJERHFUp","JESRelativeJERHFDown","JESRelativePtBBUp","JESRelativePtBBDown","JESRelativePtEC1Up","JESRelativePtEC1Down","JESRelativePtEC2Up","JESRelativePtEC2Down","JESRelativePtHFUp","JESRelativePtHFDown","JESRelativeStatECUp","JESRelativeStatECDown","JESRelativeStatFSRUp","JESRelativeStatFSRDown","JESRelativeStatHFUp","JESRelativeStatHFDown","JESSinglePionECALUp","JESSinglePionECALDown","JESSinglePionHCALUp","JESSinglePionHCALDown","JESTimePtEtaUp","JESTimePtEtaDown","CMS_res_jUp","CMS_res_jDown","lumi_13TeVUp","lumi_13TeVDown","PUup","PUdown","eeZNORMup","eeZNORMdown","eeTTNORMup","eeTTNORMdown","CMS_eff_eUp","CMS_eff_eDown","CMS_eff_trigger_eeUp","CMS_eff_trigger_eeDown","CMS_btag_combUp","CMS_btag_combDown","QCDscaleUp","QCDscaleDown","topPtReweightup","topPtReweightdown","pdfUp","pdfDown"]

#nsyst_MUON = 77
tagSyst_MUON = ["","JESAbsoluteMPFBiasUp","JESAbsoluteMPFBiasDown","JESAbsoluteScaleUp","JESAbsoluteScaleDown","JESAbsoluteStatUp","JESAbsoluteStatDown","JESFlavorQCDUp","JESFlavorQCDDown","JESFragmentationUp","JESFragmentationDown","JESPileUpDataMCUp","JESPileUpDataMCDown","JESPileUpPtBBUp","JESPileUpPtBBDown","JESPileUpPtEC1Up","JESPileUpPtEC1Down","JESPileUpPtEC2Up","JESPileUpPtEC2Down","JESPileUpPtHFUp","JESPileUpPtHFDown","JESPileUpPtRefUp","JESPileUpPtRefDown","JESRelativeBalUp","JESRelativeBalDown","JESRelativeFSRUp","JESRelativeFSRDown","JESRelativeJEREC1Up","JESRelativeJEREC1Down","JESRelativeJEREC2Up","JESRelativeJEREC2Down","JESRelativeJERHFUp","JESRelativeJERHFDown","JESRelativePtBBUp","JESRelativePtBBDown","JESRelativePtEC1Up","JESRelativePtEC1Down","JESRelativePtEC2Up","JESRelativePtEC2Down","JESRelativePtHFUp","JESRelativePtHFDown","JESRelativeStatECUp","JESRelativeStatECDown","JESRelativeStatFSRUp","JESRelativeStatFSRDown","JESRelativeStatHFUp","JESRelativeStatHFDown","JESSinglePionECALUp","JESSinglePionECALDown","JESSinglePionHCALUp","JESSinglePionHCALDown","JESTimePtEtaUp","JESTimePtEtaDown","CMS_res_jUp","CMS_res_jDown","lumi_13TeVUp","lumi_13TeVDown","PUup","PUdown","uuZNORMup","uuZNORMdown","uuTTNORMup","uuTTNORMdown","CMS_eff_mUp","CMS_eff_mDown","uuHIPup","uuHIPdown","CMS_eff_trigger_uuUp","CMS_eff_trigger_uuDown","CMS_btag_combUp","CMS_btag_combDown","QCDscaleUp","QCDscaleDown","topPtReweightup","topPtReweightdown","pdfUp","pdfDown"]

if doNoSyst:
	tagSyst = [""]
else:
	if channel == 'ee':
		tagSyst = tagSyst_ELECRON
	if channel == 'uu':
		tagSyst = tagSyst_MUON


for im in range(len(_mass)):
	if domass != '':
		if _mass[im] != domass: continue

	inpFilename = primdir + "oribins/" + resType + _mass[im] + "_" + channel + "_bdt_discrim_M" + _mass[im] + "_13TeV_new"
	outFilename = outdir + "/" + resType + _mass[im] + "_" + channel + "_bdt_discrim_M" + _mass[im] + "_13TeV_new"
	storeDir = "HHres" + channel + "jj"

	f = ROOT.TFile.Open(inpFilename + ".root",  "READ")
	thedir = f.Get(storeDir)

	fout = ROOT.TFile(outFilename + ".root", "RECREATE")
	outDir = fout.mkdir(storeDir)

	histdatacheck = thedir.Get('data_obs')
	nBinsOri = histdatacheck.GetNbinsX()
	xmin = histdatacheck.GetXaxis().GetBinLowEdge(1)
	xmax = histdatacheck.GetXaxis().GetBinUpEdge(nBinsOri)
	incre = float(xmax-xmin)/nBinsOri
	print 'nBinsOri ', nBinsOri, 'xmin ', xmin, ' xmax ', xmax, ' incre ', incre

	BinsArray = arr.array('d', [])
	nBinsStd = 0

	##----------- For Constant bining ------------------------------
	nConstBinsStd = 0
	BinsStdList = []
	if nBinconst != '' :
		nConstBinsStd = int(nBinconst) # this has to be a divider of the original binning (100) ***
		if int(nBinsOri) % nConstBinsStd != 0:
			print ' ERROR new # of bins('+nBinconst+') not a divider of the original binning ('+str(nBinsOri)+')'
			exit()
		incre = float(xmax-xmin)/nConstBinsStd
		for i in range(nConstBinsStd+1):
			BinsStdList += [xmin+(incre*i)]
		nBinsStd = nConstBinsStd
		print " New binning : array size is", nBinsStd+1, len(BinsStdList), "incre", incre
		BinsArray = arr.array('d', BinsStdList)
		for i in range(len(BinsStdList)):
			print BinsStdList[i],',',
		print '\n'
	#print BinsArray[0], BinsStdList[0], BinsArray[nBinsStd], BinsStdList[nBinsStd]
	##------------------------------------------------------------


	if nBinconst == '' :
		

		##---------- BINNING MUON ----------##
		BinsList_all_dic_MUON = {}
		
		BinsList_all_dic_MUON['1000'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.86 , 0.912 , 1.0]

		BinsList_all_dic_MUON['900'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.86 , 0.912 , 1.0]

		BinsList_all_dic_MUON['800'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.792 , 0.86 , 0.924 , 1.0]

		BinsList_all_dic_MUON['750'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.78 , 0.84 , 0.888 , 0.944 , 1.0]

		BinsList_all_dic_MUON['650'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.78 , 0.86 , 0.912 , 0.952 , 1.0]

		BinsList_all_dic_MUON['600'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.78 , 0.86 , 0.912 , 0.948 , 1.0]
		
		BinsList_all_dic_MUON['550'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.78, 0.856 , 0.904, 0.94 , 1.0]

		BinsList_all_dic_MUON['500'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.78 , 0.86 , 0.916 , 0.94 , 1.0]

		BinsList_all_dic_MUON['450'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.68 , 0.76, 0.84 , 0.892, 0.92 , 1.0]

		BinsList_all_dic_MUON['400'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7, 0.78, 0.82 ,0.86, 0.9 , 1.0]

		BinsList_all_dic_MUON['350'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.76 , 0.82, 0.86 , 1.0]

		BinsList_all_dic_MUON['300'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.78 , 0.828 , 1.0]

		BinsList_all_dic_MUON['270'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.68 , 0.76 , 0.828 , 1.0]

		BinsList_all_dic_MUON['260'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.68 , 0.76 , 0.828 , 1.0]
		##---------- END BINNING MUON ----------##

		##---------- BINNING ELECTRON ----------##
		BinsList_all_dic_ELECTRON = {}

		BinsList_all_dic_ELECTRON['1000'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.86 , 0.92 , 1.0]

		BinsList_all_dic_ELECTRON['900'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.86 , 0.92 , 1.0]

		BinsList_all_dic_ELECTRON['800'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.88 , 0.94 , 1.0]

		BinsList_all_dic_ELECTRON['750'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.78 , 0.848 ,0.912, 0.948 , 1.0]

		BinsList_all_dic_ELECTRON['650'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.68 ,0.752, 0.816, 0.88 , 0.92, 0.952 , 1.0]

		BinsList_all_dic_ELECTRON['600'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.78,  0.852 , 0.908 , 0.948, 1.0]

		BinsList_all_dic_ELECTRON['550'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.78,  0.86, 0.912 , 0.944 , 1.0]

		BinsList_all_dic_ELECTRON['500'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.78,  0.86, 0.912 , 0.94 , 1.0]

		BinsList_all_dic_ELECTRON['450'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8, 0.88 , 0.92 , 1.0]

		BinsList_all_dic_ELECTRON['400'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7, 0.78 , 0.856 , 0.892 , 1.0]

		BinsList_all_dic_ELECTRON['350'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7, 0.76 , 0.8 , 0.84 , 1.0]

		BinsList_all_dic_ELECTRON['300'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6, 0.68 , 0.74 , 0.8 , 1.0]

		BinsList_all_dic_ELECTRON['270'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.68 , 0.74 , 0.792 , 1.0]

		BinsList_all_dic_ELECTRON['260'] = [-1.0 , -0.9 , -0.8 , -0.7 , -0.6 , -0.5 , -0.4 , -0.3 , -0.2 , -0.1 , 0.0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6, 0.68 , 0.74 , 0.792 , 1.0]
		##---------- END BINNING ELECTRON ----------##

		if channel == 'ee':
			BinsList_all_dic = BinsList_all_dic_ELECTRON
		if channel == 'uu':
			BinsList_all_dic = BinsList_all_dic_MUON

		nBinsStd = len(BinsList_all_dic[_mass[im]]) -1
		BinsArray = arr.array('d', BinsList_all_dic[_mass[im]])
		print " New binning : array size is", nBinsStd+1, len(BinsList_all_dic[_mass[im]])


	for isyst in range(len(tagSyst)):
		#if (tagSyst[isyst] != "JERup"): continue # this can be used to look at a particular syst
		#if (tagSyst[isyst] != "JESAbsoluteMPFBiasDown"): continue # this can be used to look at a particular syst
		if (tagSyst[isyst] == ""):
			thisSyst = tagSyst[isyst]
		else:
			thisSyst = "_" + tagSyst[isyst]
			# adjust up, down label to Capital Letter
			thisSyst = thisSyst.replace("up","Up")
			thisSyst = thisSyst.replace("down","Down")
		if (tagSyst[isyst] == ""):
		#if True:
			print  " Doing syst: ", tagSyst[isyst]
			print  " Doing mass: ", _mass[im],  " Doing syst ", thisSyst

		datstr = "data_obs" + thisSyst
		sigstr = resType + thisSyst
		ttstr  = "TTBar" + thisSyst
		zjstr  = "ZJets" + thisSyst
		wjstr  = "WJets" + thisSyst
		ststr  = "sTop"  + thisSyst
		vvstr  = "VV"    + thisSyst
		qcdstr = "QCD"   + thisSyst
		smhstr = "SMH"   + thisSyst

		h_data  = thedir.Get(datstr)
		h_sig   = thedir.Get(sigstr)
		h_TTBar = thedir.Get(ttstr)
		h_ZJets = thedir.Get(zjstr)
		h_WJets = thedir.Get(wjstr)
		h_sTop  = thedir.Get(ststr)
		h_VV    = thedir.Get(vvstr)
		h_QCD   = thedir.Get(qcdstr)
		h_SMH   = thedir.Get(smhstr)

		hEdit_ZJets = h_ZJets.Clone("EditZJets")

		h_Bgd = h_TTBar.Clone()
		h_Bgd.Add(hEdit_ZJets)
		h_Bgd.Add(h_WJets)
		h_Bgd.Add(h_sTop)
		h_Bgd.Add(h_VV)
		h_Bgd.Add(h_QCD)
		h_Bgd.Add(h_SMH)

		for i in range(nBinsOri):
			if (tagSyst[isyst] == ""):
				print "  Low edge bin:", i+1, "BinsArrayOri:", h_data.GetXaxis().GetBinLowEdge(i+1), "Sig:", h_sig.GetBinContent(i+1), "Data:", h_data.GetBinContent(i+1), "BG:", h_Bgd.GetBinContent(i+1)

		h_data_rebin  = h_data.Rebin  (nBinsStd,"h_data_rebin", BinsArray)
		h_Bgd_rebin   = h_Bgd.Rebin   (nBinsStd,"h_Bgd_rebin" , BinsArray)
		h_sig_rebin   = h_sig.Rebin   (nBinsStd,"h_sig_rebin" , BinsArray)
		h_TTBar_rebin = h_TTBar.Rebin (nBinsStd,"h_TTBar_rebin" , BinsArray)
		h_ZJets_rebin = hEdit_ZJets.Rebin(nBinsStd,"h_ZJets_rebin" , BinsArray)
		h_WJets_rebin = h_WJets.Rebin (nBinsStd,"h_WJets_rebin" , BinsArray)
		h_sTop_rebin  = h_sTop.Rebin  (nBinsStd,"h_sTop_rebin" , BinsArray)
		h_VV_rebin    = h_VV.Rebin    (nBinsStd,"h_VV_rebin" , BinsArray)
		h_QCD_rebin   = h_QCD.Rebin   (nBinsStd,"h_QCD_rebin" , BinsArray)
		h_SMH_rebin   = h_SMH.Rebin   (nBinsStd,"h_SMH_rebin" , BinsArray)

		if (not hasData):
			for i in range(nBinsStd):
				h_data_rebin.SetBinContent(i+1,0)
				h_data_rebin.SetBinError(i+1,0)

			
		#----- print out results after rebin
		for i in range(nBinsStd):
			evnt_lim = 0
			if h_Bgd_rebin.GetBinError(i+1) > 0:
				evnt_lim = int (((h_Bgd_rebin.GetBinContent(i+1)**2)/(h_Bgd_rebin.GetBinError(i+1)**2)) + 0.5)
			bg_err = 0
			if (h_Bgd_rebin.GetBinContent(i+1)>0):
				bg_err = 100*h_Bgd_rebin.GetBinError(i+1)/h_Bgd_rebin.GetBinContent(i+1)
			if (tagSyst[isyst] == ""):
				#print "bin", i+1, "Low edge:", h_sig_rebin.GetXaxis().GetBinLowEdge(i+1), "bin width", h_sig_rebin.GetXaxis().GetBinUpEdge(i+1) - h_sig_rebin.GetXaxis().GetBinLowEdge(i+1), "Sig", h_sig_rebin.GetBinContent(i+1), "Data", h_data_rebin.GetBinContent(i+1), "BG", h_Bgd_rebin.GetBinContent(i+1), "evnt_lim", evnt_lim, "\t bg_err (%)", bg_err
				print "bin", i+1, "Low edge:", h_sig_rebin.GetXaxis().GetBinLowEdge(i+1), "bin width", h_sig_rebin.GetXaxis().GetBinUpEdge(i+1) - h_sig_rebin.GetXaxis().GetBinLowEdge(i+1), "Sig", h_sig_rebin.GetBinContent(i+1), "BG", h_Bgd_rebin.GetBinContent(i+1), "\t evnt_lim", evnt_lim, "\t bg_err (%)", bg_err

			#if False:
				#cout << "     h_TTBar " << h_TTBar_rebin->GetBinContent(i)<< " err " << h_TTBar_rebin->GetBinError(i)<< endl;
				#cout << "     h_ZJets " << h_ZJets_rebin->GetBinContent(i)<< " err " << h_ZJets_rebin->GetBinError(i)<< endl;
				#cout << "     h_WJets " << h_WJets_rebin->GetBinContent(i)<< " err " << h_WJets_rebin->GetBinError(i)<< endl;
				#cout << "     h_sTop  " << h_sTop_rebin->GetBinContent(i)<< " err " << h_sTop_rebin->GetBinError(i)<< endl;
				#cout << "     h_VV    " << h_VV_rebin->GetBinContent(i) << " err " << h_VV_rebin->GetBinError(i)<< endl;
				#cout << "     h_QCD   " << h_QCD_rebin->GetBinContent(i)<< " err " << h_QCD_rebin->GetBinError(i)<< endl;
				#cout << "     h_SMH   " << h_SMH_rebin->GetBinContent(i)<< " err " << h_SMH_rebin->GetBinError(i)<< endl;

		# checking if we have all events
		if (tagSyst[isyst] == ""):
			print " integral befor rebin :", h_sig.Integral(), h_data.Integral(), h_Bgd.Integral(), h_Bgd.GetNbinsX()
			print " integral after rebin :", h_sig_rebin.Integral(), h_data_rebin.Integral(), h_Bgd_rebin.Integral(), h_Bgd_rebin.GetNbinsX()


		# assume that when - is put on a prcess, the corresponding histogram is not required to be present
		if (tagSyst[isyst] == "QCDscaleUp" or tagSyst[isyst] == "QCDscaleDown") :
			tagUD = ""
			if (tagSyst[isyst] == "QCDscaleUp"):
				tagUD = "Up"
			elif (tagSyst[isyst] == "QCDscaleDown"):
				tagUD = "Down"
			sigstr = resType + "_QCDscale_" + resType + tagUD
			ttstr  = "TTBar_QCDscale_ttbar" + tagUD
			zjstr  = "ZJets_QCDscale_ZJets" + tagUD
			wjstr  = "WJets_QCDscale_WJets" + tagUD
			ststr  =  "sTop_QCDscale_sTop"  + tagUD
			vvstr  =    "VV_QCDscale_VV"    + tagUD
			qcdstr =   "QCD_QCDscale_QCD"   + tagUD
			smhstr =   "SMH_QCDscale_SMH"   + tagUD

		outDir.cd()
		h_data_rebin .Write((datstr))
		h_sig_rebin  .Write((sigstr))
		h_TTBar_rebin.Write( (ttstr))
		h_ZJets_rebin.Write( (zjstr))
		h_WJets_rebin.Write( (wjstr))
		h_sTop_rebin .Write( (ststr))
		h_VV_rebin   .Write( (vvstr))
		h_QCD_rebin  .Write((qcdstr))
		h_SMH_rebin  .Write((smhstr))

		if True :
			if (tagSyst[isyst] != ""): continue
				
			can1 = TCanvas("can1", "can1", 800, 550)
			can1.cd()
			can1.SetTicks()
			can1.SetGrid()
			#--- TLegend ---
			legend = TLegend(0.47, 0.54, 0.99, 0.98)
			legend.SetX1(0.8)
			legend.SetY1(0.8)
			legend.SetX2(0.9)
			legend.SetY2(0.9)
			legend.SetTextSize(.024)
			legend.SetFillColor(0)
			legend.SetFillStyle(1001)
			legend.SetBorderSize(0)
			
			h_Bgd_rebin.SetMarkerStyle(2)
			h_Bgd_rebin.SetMarkerColor(kBlue)
			h_Bgd_rebin.SetLineColor(kBlue)
			h_Bgd_rebin.SetMarkerStyle(2)
			h_Bgd_rebin.SetTitle("")
			h_Bgd_rebin.GetXaxis().SetTitle(channel + " BDT "+_mass[im])
			h_Bgd_rebin.Draw("hist")
			
			h_sig_rebin.SetMarkerColor(kGreen)
			h_sig_rebin.SetLineColor(kGreen)
			h_sig_rebClon = h_sig_rebin.Clone()
			h_sig_rebClon.Scale(20000.)
			h_sig_rebClon.Draw("hist same")
			
			if (plotData):
				h_data_rebin.SetMarkerStyle(2)
				h_data_rebin.Draw("hist same")
				legend.AddEntry(h_data_rebin, "h_data", "pl")
			
			can1.SetLogy()

			legend.AddEntry(h_Bgd_rebin, "h_Bgd", "l")
			legend.AddEntry(h_sig_rebClon, "h_sig x 20k", "l")
			legend.Draw()
			outpdfname = "output" + thisSyst
			outpdfname += "_" + resType + "_" + channel + "_" + _mass[im] + ".pdf"
			can1.Print(outdirpdf+"/"+outpdfname)

			#--- to plot contribution from each bg
			if (zoomplot):
				can2 = TCanvas("can2", "can2", 800, 550)
				can2.cd()
				can2.SetTicks()
				can2.SetGrid()
				
				h_Bgd_rebin.GetYaxis().SetRangeUser(-15, 30)
				h_Bgd_rebin.Draw("hist")
				
				legend_z = TLegend(0.47, 0.54, 0.99, 0.98)
				legend_z.SetX1(0.8)
				legend_z.SetY1(0.65)
				legend_z.SetX2(0.9)
				legend_z.SetY2(0.85)
				legend_z.AddEntry(h_Bgd_rebin, "h_Bgd", "l")
				
				h_TTBar_rebin.SetLineColor(kCyan)
				h_ZJets_rebin.SetLineColor(kBlack)
				h_WJets_rebin.SetLineColor(kMagenta)
				h_sTop_rebin.SetLineColor(kRed)
				h_VV_rebin.SetLineColor(kBlue+2)
				h_QCD_rebin.SetLineColor(kGreen+2)
				h_SMH_rebin.SetLineColor(kRed+2)
				#h_TTBar_rebin->Draw("hist same")
				h_ZJets_rebin.Draw("hist same")
				h_WJets_rebin.Draw("hist same")
				#h_sTop_rebin->Draw("hist same")
				#h_VV_rebin->Draw("hist same")
				#h_QCD_rebin->Draw("hist same")
				#h_SMH_rebin->Draw("hist same")
				
				#legend_z->AddEntry(h_TTBar_rebin, "h_TTBar", "l")
				legend_z.AddEntry(h_ZJets_rebin, "h_ZJets", "l")
				legend_z.AddEntry(h_WJets_rebin, "h_WJets", "l")
				#legend_z->AddEntry(h_sTop_rebin, "h_sTop", "l")
				#legend_z->AddEntry(h_VV_rebin, "h_VV", "l")
				#legend_z->AddEntry(h_QCD_rebin, "h_QCD", "l")
				#legend_z->AddEntry(h_SMH_rebin, "h_SMH", "l")
				can2.SetLogy(0)
				outpdfname_z = "output" + thisSyst
				outpdfname_z += "_" + resType + "_" + channel + "_" + _mass[im] + "_zoom.pdf"
				can2.Print(outdirpdf_z+"/"+outpdfname_z)

			if (p_linear):
				can3 = TCanvas("can3", "can3", 800, 550)
				can3.cd()
				can3.SetTicks()
				can3.SetGrid()
				#--- TLegend ---
				leg_lin = TLegend(0.47, 0.54, 0.99, 0.98)
				leg_lin.SetX1(0.8)
				leg_lin.SetY1(0.8)
				leg_lin.SetX2(0.9)
				leg_lin.SetY2(0.9)
				leg_lin.SetTextSize(.024)
				leg_lin.SetFillColor(0)
				leg_lin.SetFillStyle(1001)
				leg_lin.SetBorderSize(0)
				h_Bgd_rebin.Draw("hist")
				h_sig_rebClon.Draw("hist same")
				if (plotData):
					h_data_rebin.Draw("hist same")
					legend.AddEntry(h_data_rebin, "h_data", "pl")
				can3.SetLogy(0)
				leg_lin.AddEntry(h_Bgd_rebin, "h_Bgd", "l")
				leg_lin.AddEntry(h_sig_rebClon, "h_sig x 20k", "l")
				leg_lin.Draw()
				outpdfname_lin = "output" + thisSyst
				outpdfname_lin += "_" + resType + "_" + channel + "_" + _mass[im] + "_linear.pdf"
				can3.Print(outdirpdf_lin+"/"+outpdfname_lin)

	fout.Close()
	f.Close()



