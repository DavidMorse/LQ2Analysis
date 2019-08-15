import os
import sys
import random
import time
import datetime
import ROOT
from ROOT import *
import array as arr

# python refixHist.py --resType HHres --channel ee -m 260

channel   = ''
resType   = ''
domass    = ''

for x in range(len(sys.argv)):
	if sys.argv[x] == '--channel':
		channel = sys.argv[x+1] # 'ee', 'uu'
	if sys.argv[x] == '--resType':
		resType = sys.argv[x+1] # 'HHres', 'HHBulkGrav'
	if sys.argv[x] == '-m':
		domass = sys.argv[x+1]

hasData  = True # need to check this functionality
qcdscaleInc = False # need to include this functionality

if '--blindData' in sys.argv:
	hasData = False # for blind cards, set this to False

ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)

_mass = ["260","270","300","350","400", "450", "500",  "550",  "600",  "650", "750", "800", "900", "1000"]

primdir = 'rootfiles_final/rootfiles_final_' + channel + '/'
outRootdir = primdir + "newbinningadjust"
os.system("mkdir " + outRootdir)

#nsyst = 37
tagSyst_ELECRON = ["JESAbsoluteMPFBias","JESAbsoluteScale","JESAbsoluteStat","JESFlavorQCD","JESFragmentation","JESPileUpDataMC","JESPileUpPtBB","JESPileUpPtEC1","JESPileUpPtEC2","JESPileUpPtHF","JESPileUpPtRef","JESRelativeBal","JESRelativeFSR","JESRelativeJEREC1","JESRelativeJEREC2","JESRelativeJERHF","JESRelativePtBB","JESRelativePtEC1","JESRelativePtEC2","JESRelativePtHF","JESRelativeStatEC","JESRelativeStatFSR","JESRelativeStatHF","JESSinglePionECAL","JESSinglePionHCAL","JESTimePtEta","CMS_res_j","lumi_13TeV","PU","eeZNORM","eeTTNORM","CMS_eff_e","CMS_eff_trigger_ee","CMS_btag_comb","QCDscale","topPtReweight","pdf"]
#nsyst = 38
tagSyst_MUON = ["JESAbsoluteMPFBias","JESAbsoluteScale","JESAbsoluteStat","JESFlavorQCD","JESFragmentation","JESPileUpDataMC","JESPileUpPtBB","JESPileUpPtEC1","JESPileUpPtEC2","JESPileUpPtHF","JESPileUpPtRef","JESRelativeBal","JESRelativeFSR","JESRelativeJEREC1","JESRelativeJEREC2","JESRelativeJERHF","JESRelativePtBB","JESRelativePtEC1","JESRelativePtEC2","JESRelativePtHF","JESRelativeStatEC","JESRelativeStatFSR","JESRelativeStatHF","JESSinglePionECAL","JESSinglePionHCAL","JESTimePtEta","CMS_res_j","lumi_13TeV","PU","uuZNORM","uuTTNORM","CMS_eff_m","uuHIP","CMS_eff_trigger_uu","CMS_btag_comb","QCDscale","topPtReweight","pdf"]

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

	inpFilename = primdir + "newbinning_xbins/" + resType + _mass[im] + "_" + channel + "_bdt_discrim_M" + _mass[im] + "_13TeV_new"
	outFilename = outRootdir + "/" + resType + _mass[im] + "_" + channel + "_bdt_discrim_M" + _mass[im] + "_13TeV_new"
	print (" opening file : " + inpFilename + ".root")
	storeDir = "HHres" + channel + "jj"
	
	f = ROOT.TFile.Open(inpFilename + ".root",  "READ")
	thedir = f.Get(storeDir)
	
	fout = ROOT.TFile(outFilename + ".root", "RECREATE")
	outDir = fout.mkdir(storeDir)

	for isyst in range(len(tagSyst)):
		thisSyst = tagSyst[isyst]
		print (" copying syst: " + thisSyst)
		
		up_var = "_" + thisSyst + "Up"
		dn_var = "_" + thisSyst + "Down"
		
		h_procs = [] # this is a list of lists
		[h_BG, h_BG_up, h_BG_dn] = [TH1D(),TH1D(),TH1D()]
		for ip in range(len(procs_str)):
			h_pr = [] # this is a list containing cen,up,down
			h_pr += [thedir.Get(procs_str[ip])]
			
			if ( (not qcdscaleInc) and tagSyst[isyst] == "QCDscale"):
				up_fullstr = qcdscale_str[ip] + "Up"
				dn_fullstr = qcdscale_str[ip] + "Down"
			else:
				up_fullstr = procs_str[ip]+up_var
				dn_fullstr = procs_str[ip]+dn_var
		
			h_pr += [thedir.Get(up_fullstr)]
			h_pr += [thedir.Get(dn_fullstr)]
			h_procs += [h_pr]

			# create sum BGs since we will impose condition on the sum of BGs
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

		for bin in range(h_BG_clone.GetNbinsX()):
			i = bin+1
			# for BG
			thisbin    = h_BG.GetBinContent(i)
			thisbin_up = h_BG_up.GetBinContent(i)
			thisbin_dn = h_BG_dn.GetBinContent(i)
			#print i,  thisbin, thisbin_up, thisbin_dn
			if ((thisbin_up-thisbin)*(thisbin_dn-thisbin) > 0):
				if (fabs(thisbin_dn-thisbin) < fabs(thisbin_up-thisbin)):
					#print "     set DOWN to cen"
					for ip in range(len(procs_str)):
						if ip < 2: continue
						else: h_procs[ip][2].SetBinContent(i, h_procs[ip][0].GetBinContent(i))
				
				else:
					#print "     set Up to cen"
					for ip in range(len(procs_str)):
						if ip < 2: continue
						else: h_procs[ip][1].SetBinContent(i, h_procs[ip][0].GetBinContent(i))
			# for Sig
			sig_bin = h_procs[1][0].GetBinContent(i)
			sig_binup =  h_procs[1][1].GetBinContent(i)
			sig_bindn =  h_procs[1][2].GetBinContent(i)
			if ((sig_binup-sig_bin)*(sig_bindn-sig_bin) > 0):
				if (fabs(sig_bindn-sig_bin) < fabs(sig_binup-sig_bin)):
					h_procs[1][2].SetBinContent(i, h_procs[1][0].GetBinContent(i))
				else:
					h_procs[1][1].SetBinContent(i, h_procs[1][0].GetBinContent(i))
							
		# topPtReweight was set equal to central, now we ship it opposite to Up
		for bin in range(h_BG_clone.GetNbinsX()):
			i = bin+1
			if (tagSyst[isyst] == "topPtReweight"):
				for ip in range(len(procs_str)):
					h_procs[ip][2].SetBinContent( i, h_procs[ip][0].GetBinContent(i) + (-1)*(h_procs[ip][1].GetBinContent(i)  - h_procs[ip][0].GetBinContent(i)) )
		
		outDir.cd()
		for ip in range(len(procs_str)):
			if ((not hasData) and ip == 0): continue
			if (isyst == 0):
				h_procs[ip][0].Write(procs_str[ip])
			
			if ( (not qcdscaleInc) and tagSyst[isyst] == "QCDscale"):
				if qcdscale_str[ip] == "sTop_QCDscale_sTop":
					h_procs[ip][1].Write("sTop_QCDscale_SingleTop" + "Up")
					h_procs[ip][2].Write("sTop_QCDscale_SingleTop" + "Down")
				elif qcdscale_str[ip] == resType+"_QCDscale_"+resType:
					h_procs[ip][1].Write(resType+"_QCDscale_ggHH"+"Up")
					h_procs[ip][2].Write(resType+"_QCDscale_ggHH"+"Down")
				elif qcdscale_str[ip] == "SMH_QCDscale_SMH":
					h_procs[ip][1].Write("SMH_QCDscale_VH" + "Up")
					h_procs[ip][2].Write("SMH_QCDscale_VH" + "Down")
				else:
					h_procs[ip][1].Write(qcdscale_str[ip] + "Up")
					h_procs[ip][2].Write(qcdscale_str[ip] + "Down")
			elif thisSyst == "pdf":
				if procs_str[ip] == resType:
					h_procs[ip][1].Write(procs_str[ip]+"_pdf_ggUp")
					h_procs[ip][2].Write(procs_str[ip]+"_pdf_ggDown")
				else:
					h_procs[ip][1].Write(procs_str[ip]+"_pdf_qqbarUp")
					h_procs[ip][2].Write(procs_str[ip]+"_pdf_qqbarDown")
			else:
				if thisSyst == "PU":
					h_procs[ip][1].Write(procs_str[ip]+"_CMS_puUp")
					h_procs[ip][2].Write(procs_str[ip]+"_CMS_puDown")
				elif thisSyst == "uuHIP":
					h_procs[ip][1].Write(procs_str[ip]+"_CMS_eff_m_trackerUp")
					h_procs[ip][2].Write(procs_str[ip]+"_CMS_eff_m_trackerDown")
				elif thisSyst == "CMS_eff_trigger_uu":
					h_procs[ip][1].Write(procs_str[ip]+"_CMS_eff_m_triggerUp")
					h_procs[ip][2].Write(procs_str[ip]+"_CMS_eff_m_triggerDown")
				elif thisSyst == "CMS_eff_trigger_ee":
					h_procs[ip][1].Write(procs_str[ip]+"_CMS_eff_e_triggerUp")
					h_procs[ip][2].Write(procs_str[ip]+"_CMS_eff_e_triggerDown")
				elif thisSyst == "CMS_eff_e":
					h_procs[ip][1].Write(procs_str[ip]+"_CMS_eff_e_IDUp")
					h_procs[ip][2].Write(procs_str[ip]+"_CMS_eff_e_IDDown")
				elif thisSyst == "CMS_btag_comb":
					h_procs[ip][1].Write(procs_str[ip]+"_CMS_btag_lightUp")
					h_procs[ip][2].Write(procs_str[ip]+"_CMS_btag_lightDown")
				elif thisSyst == "CMS_eff_m":
					h_procs[ip][1].Write(procs_str[ip]+"_CMS_eff_m_IDUp")
					h_procs[ip][2].Write(procs_str[ip]+"_CMS_eff_m_IDDown")
				elif thisSyst == "JESFlavorQCD":
					h_procs[ip][1].Write(procs_str[ip]+"_CMS_scale_jUp")
					h_procs[ip][2].Write(procs_str[ip]+"_CMS_scale_jDown")
				else:
					#print 'writing ', procs_str[ip]+up_var, procs_str[ip]+dn_var
					h_procs[ip][1].Write(procs_str[ip]+up_var)
					h_procs[ip][2].Write(procs_str[ip]+dn_var)
									 
	fout.Close()
	f.Close()
									 
									 

									 
									 
									 
									 
									 
									 
					
