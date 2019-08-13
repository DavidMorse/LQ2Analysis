import os
import sys
import random
import time
import datetime
import ROOT
from ROOT import *
import array as arr

# python plotSystHist.py --resType HHres --channel ee -m 260 (--preadjust) (--syst lumi_13TeV)
# python plotSystHist.py --resType HHres --channel ee -m 260 --preadjust

channel   = ''
resType   = ''
domass    = ''
dovar = ''

for x in range(len(sys.argv)):
	if sys.argv[x] == '--channel':
		channel = sys.argv[x+1] # 'ee', 'uu'
	if sys.argv[x] == '--resType':
		resType = sys.argv[x+1] # 'HHres', 'HHBulkGrav'
	if sys.argv[x] == '-m':
		domass = sys.argv[x+1]
	if sys.argv[x] == '--syst':
		dovar = sys.argv[x+1]

qcdscaleInc = False
preadjust = False

inputdir = "newbinningadjust"
output_plotdir = "plot_syst_out_post_adjust"
if '--preadjust' in sys.argv:
	preadjust = True
	inputdir = "newbinning_xbins"
	output_plotdir = "plot_syst_out_pre_adjust"


ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)

_mass = ["260","270","300","350","400", "450", "500",  "550",  "600",  "650", "750", "800", "900", "1000"]

primdir = 'rootfiles_final/rootfiles_final_' + channel + '/'

#nsyst = 37
#tagSyst_ELECRON = ["JESAbsoluteMPFBias","JESAbsoluteScale","JESAbsoluteStat","JESFlavorQCD","JESFragmentation","JESPileUpDataMC","JESPileUpPtBB","JESPileUpPtEC1","JESPileUpPtEC2","JESPileUpPtHF","JESPileUpPtRef","JESRelativeBal","JESRelativeFSR","JESRelativeJEREC1","JESRelativeJEREC2","JESRelativeJERHF","JESRelativePtBB","JESRelativePtEC1","JESRelativePtEC2","JESRelativePtHF","JESRelativeStatEC","JESRelativeStatFSR","JESRelativeStatHF","JESSinglePionECAL","JESSinglePionHCAL","JESTimePtEta","CMS_res_j","lumi_13TeV","PU","eeZNORM","eeTTNORM","CMS_eff_e","CMS_eff_trigger_ee","CMS_btag_comb","QCDscale","topPtReweight","pdf"]

tagSyst_ELECRON = {"JESAbsoluteMPFBias":0.1, "JESAbsoluteScale":0.1, "JESAbsoluteStat":0.1, "JESFlavorQCD":0.4, "JESFragmentation":0.1, "JESPileUpDataMC":0.1, "JESPileUpPtBB":0.1, "JESPileUpPtEC1":0.1, "JESPileUpPtEC2":0.002, "JESPileUpPtHF":0.002, "JESPileUpPtRef":0.1, "JESRelativeBal":0.1, "JESRelativeFSR":0.1, "JESRelativeJEREC1":0.1, "JESRelativeJEREC2":0.002, "JESRelativeJERHF":0.002, "JESRelativePtBB":0.1, "JESRelativePtEC1":0.1, "JESRelativePtEC2":0.002, "JESRelativePtHF":0.002, "JESRelativeStatEC":0.1, "JESRelativeStatFSR":0.1, "JESRelativeStatHF":0.002, "JESSinglePionECAL":0.1, "JESSinglePionHCAL":0.1, "JESTimePtEta":0.1, "CMS_res_j":0.1, "lumi_13TeV":0.1, "PU":0.1, "eeZNORM":0.1, "eeTTNORM":0.1, "CMS_eff_e":0.1, "CMS_eff_trigger_ee":0.1, "CMS_btag_comb":0.1, "QCDscale":0.8, "topPtReweight":0.002, "pdf":0.1}

#nsyst = 38
#tagSyst_MUON = ["JESAbsoluteMPFBias","JESAbsoluteScale","JESAbsoluteStat","JESFlavorQCD","JESFragmentation","JESPileUpDataMC","JESPileUpPtBB","JESPileUpPtEC1","JESPileUpPtEC2","JESPileUpPtHF","JESPileUpPtRef","JESRelativeBal","JESRelativeFSR","JESRelativeJEREC1","JESRelativeJEREC2","JESRelativeJERHF","JESRelativePtBB","JESRelativePtEC1","JESRelativePtEC2","JESRelativePtHF","JESRelativeStatEC","JESRelativeStatFSR","JESRelativeStatHF","JESSinglePionECAL","JESSinglePionHCAL","JESTimePtEta","CMS_res_j","lumi_13TeV","PU","uuZNORM","uuTTNORM","CMS_eff_m","uuHIP","CMS_eff_trigger_uu","CMS_btag_comb","QCDscale","topPtReweight","pdf"]

tagSyst_MUON = {"JESAbsoluteMPFBias":0.1, "JESAbsoluteScale":0.1, "JESAbsoluteStat":0.1, "JESFlavorQCD":0.4, "JESFragmentation":0.1, "JESPileUpDataMC":0.1, "JESPileUpPtBB":0.1, "JESPileUpPtEC1":0.1, "JESPileUpPtEC2":0.002, "JESPileUpPtHF":0.002, "JESPileUpPtRef":0.1, "JESRelativeBal":0.1, "JESRelativeFSR":0.1, "JESRelativeJEREC1":0.1, "JESRelativeJEREC2":0.002, "JESRelativeJERHF":0.002, "JESRelativePtBB":0.1, "JESRelativePtEC1":0.1, "JESRelativePtEC2":0.002, "JESRelativePtHF":0.002, "JESRelativeStatEC":0.1, "JESRelativeStatFSR":0.1, "JESRelativeStatHF":0.002, "JESSinglePionECAL":0.1, "JESSinglePionHCAL":0.1, "JESTimePtEta":0.1, "CMS_res_j":0.1, "lumi_13TeV":0.1, "PU":0.1,"uuZNORM":0.1, "uuTTNORM":0.1, "CMS_eff_m":0.1, "uuHIP":0.1, "CMS_eff_trigger_uu":0.1, "CMS_btag_comb":0.1, "QCDscale":0.8, "topPtReweight":0.002, "pdf":0.2}

if channel == 'ee':
	tagSyst = tagSyst_ELECRON
if channel == 'uu':
	tagSyst = tagSyst_MUON

procs_str = ["data_obs",resType,"TTBar","ZJets","WJets","sTop","VV","QCD","SMH"]
qcdscale_str = ["data_obs_QCDscale",
				resType+"_QCDscale_"+resType,
				"TTBar_QCDscale_ttbar",
				"ZJets_QCDscale_ZJets",
				"WJets_QCDscale_WJets",
				"sTop_QCDscale_sTop",
				"VV_QCDscale_VV",
				"QCD_QCDscale_QCD",
				"SMH_QCDscale_SMH"
				]

for im in range(len(_mass)):
	if domass != '':
		if _mass[im] != domass: continue
	
	outpdfdir = primdir + output_plotdir + _mass[im]
	os.system("mkdir " + outpdfdir)

	
	inpFilename = primdir + inputdir + "/" + resType + _mass[im] + "_" + channel + "_bdt_discrim_M" + _mass[im] + "_13TeV_new"
	print (" opening file : " + inpFilename + ".root")
	storeDir = "HHres" + channel + "jj"
	
	f = ROOT.TFile.Open(inpFilename + ".root",  "READ")
	thedir = f.Get(storeDir)

	for key in tagSyst.iterkeys():
		if dovar != '':
			if key != dovar: continue
		
		thisSyst = key
		print (" ploting syst: " + thisSyst)

		up_var = "_" + thisSyst + "Up";
		dn_var = "_" + thisSyst + "Down";
		[h_BG, h_BG_up, h_BG_dn] = [TH1D(),TH1D(),TH1D()]

		for ip in range(len(procs_str)):
			if ( (not qcdscaleInc) and thisSyst == "QCDscale"):
				up_fullstr = qcdscale_str[ip] + "Up"
				dn_fullstr = qcdscale_str[ip] + "Down"
			else:
				up_fullstr = procs_str[ip]+up_var
				dn_fullstr = procs_str[ip]+dn_var

			if (ip < 2) :
				continue
			if (ip == 2) :
				h_BG = thedir.Get(procs_str[ip])
				h_BG_up = thedir.Get(up_fullstr)
				h_BG_dn = thedir.Get(dn_fullstr)
			if (ip > 2):
				h_BG.Add(thedir.Get(procs_str[ip]))
				h_BG_up.Add(thedir.Get(up_fullstr))
				h_BG_dn.Add(thedir.Get(dn_fullstr))
			h_BG_clone = h_BG.Clone("h_BG_clone")
	
		print (" getting histo :  BG "  + up_var + " " + dn_var)
		print (" Integral      : " + str(h_BG.Integral()) +  " " + str(h_BG_up.Integral()) + " " + str(h_BG_dn.Integral()) )
	
	
		for bin in range (h_BG_clone.GetNbinsX()):
			i = bin+1
			if (h_BG_clone.GetBinContent(i) != 0):
				h_BG.SetBinContent   (i, float(h_BG.GetBinContent(i))/h_BG_clone.GetBinContent(i))
				h_BG_up.SetBinContent(i, float(h_BG_up.GetBinContent(i))/h_BG_clone.GetBinContent(i))
				h_BG_dn.SetBinContent(i, float(h_BG_dn.GetBinContent(i))/h_BG_clone.GetBinContent(i))
				
				h_BG.SetBinError   (i, float(h_BG.GetBinError(i))/h_BG_clone.GetBinContent(i))
				h_BG_up.SetBinError(i, float(h_BG_up.GetBinError(i))/h_BG_clone.GetBinContent(i))
				h_BG_dn.SetBinError(i, float(h_BG_dn.GetBinError(i))/h_BG_clone.GetBinContent(i))
			
			else:
				h_BG.SetBinContent(i, 1.)
				h_BG_up.SetBinContent(i, 1.)
				h_BG_dn.SetBinContent(i, 1.)
				
				h_BG.SetBinError(i, 0.)
				h_BG_up.SetBinError(i, 0.)
				h_BG_dn.SetBinError(i, 0.)

		h_BG.SetMarkerStyle(2)
		h_BG.SetMarkerColor(kBlack)
		h_BG.SetLineColor(kBlack)
		
		h_BG.GetXaxis().SetTitleSize(0.05)
		h_BG.GetYaxis().SetTitleOffset(0.8)
		
		h_BG_up.SetMarkerStyle(2)
		h_BG_up.SetMarkerColor(kRed)
		h_BG_up.SetLineColor(kRed)

		h_BG_dn.SetMarkerStyle(2)
		h_BG_dn.SetMarkerColor(kGreen)
		h_BG_dn.SetLineColor(kGreen)
		
		
		h_BG.GetYaxis().SetRangeUser(1.0-tagSyst[key],1.0+tagSyst[key])
		h_BG.SetMarkerSize(0.5)
		
		can1 = TCanvas("can1", "can1", 800, 550)
		can1.cd();
		can1.SetTicks()
		can1.SetGrid()
		gStyle.SetOptStat(0)
		
		legend = TLegend(0.47, 0.54, 0.99, 0.98)
		legend.SetX1(0.8)
		legend.SetY1(0.8)
		legend.SetX2(0.9)
		legend.SetY2(0.9)
		
		h_BG.Draw("hist e")
		h_BG_up.Draw("hist same")
		h_BG_dn.Draw("hist same")
		
		legend.AddEntry(h_BG_up, "Up", "l")
		legend.AddEntry(h_BG_dn, "Down", "l")
		legend.Draw()
		#//cout << __LINE__ << endl;

		h_BG.SetTitle("")
		h_BG.SetXTitle("BDT output " + thisSyst)
		h_BG.SetYTitle("Ratio to Central")
		
		outname = thisSyst + "_" + channel + "_" + _mass[im] + ".pdf"
		outname = outpdfdir  + "/" + outname
		can1.Update()
		can1.Print(outname)

	f.Close()

