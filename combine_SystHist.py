import os
import sys, getopt
import ROOT
#from ROOT import *
import array
import math

def main():
	#inpDir = "systRootFiles/"
	
	txtDir = "Results_Testing_diHiggs_newNtuples_MuCutsMC0p49_"
	
	#_resHypos = ['HHres', 'HHBulkGrav']
	
	if '--Spin2' in sys.argv:
		resType = "HHBulkGrav"
	else:
		resType = "HHres"

	if (resType == 'HHres'):
		x_spin = '0'
	if (resType == 'HHBulkGrav'):
		x_spin = '2'

	doindiv = False ## this is to use LowM bdt in the electron channel (for M260 M270 M300 GeV)
	#doindiv = True   ## this is to use individually trained bdt for all cases
	
	procs = ["HHres","data_obs","TTBar","ZJets","WJets","sTop","VV","QCD","SMH"]
	#procs = ["data_obs","HHres"]

	_mass = ["260","270","300","350","400", "450", "500", "550", "600","650", "750", "800", "900", "1000"]
	#_mass = ["260"]
	
	_analysisChan = ['uujj','eejj']
	_leptonChan = ['uu','ee']
	_leps = ['muon','electron']
	
	## xx variations (include PDF) : this is what present in the final systematic variations
	## use for --Standard
	## need individual set for uu and ee channels
	#_Variations = ['','JERup','JERdown','MER','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','TTNORMup','TTNORMdown','MUONIDISOup','MUONIDISOdown','HIPup','HIPdown','MUONHLTup','MUONHLTdown','BTAGup','BTAGdown','QCDSCALEup','QCDSCALEdown','PDFup','PDFdown']
	## current one
	_Variations_uu = ['','JESAbsoluteMPFBiasUp','JESAbsoluteMPFBiasDown','JESAbsoluteScaleUp','JESAbsoluteScaleDown','JESAbsoluteStatUp','JESAbsoluteStatDown','JESFlavorQCDUp','JESFlavorQCDDown','JESFragmentationUp','JESFragmentationDown','JESPileUpDataMCUp','JESPileUpDataMCDown','JESPileUpPtBBUp','JESPileUpPtBBDown','JESPileUpPtEC1Up','JESPileUpPtEC1Down','JESPileUpPtEC2Up','JESPileUpPtEC2Down','JESPileUpPtHFUp','JESPileUpPtHFDown','JESPileUpPtRefUp','JESPileUpPtRefDown','JESRelativeBalUp','JESRelativeBalDown','JESRelativeFSRUp','JESRelativeFSRDown','JESRelativeJEREC1Up','JESRelativeJEREC1Down','JESRelativeJEREC2Up','JESRelativeJEREC2Down','JESRelativeJERHFUp','JESRelativeJERHFDown','JESRelativePtBBUp','JESRelativePtBBDown','JESRelativePtEC1Up','JESRelativePtEC1Down','JESRelativePtEC2Up','JESRelativePtEC2Down','JESRelativePtHFUp','JESRelativePtHFDown','JESRelativeStatECUp','JESRelativeStatECDown','JESRelativeStatFSRUp','JESRelativeStatFSRDown','JESRelativeStatHFUp','JESRelativeStatHFDown','JESSinglePionECALUp','JESSinglePionECALDown','JESSinglePionHCALUp','JESSinglePionHCALDown','JESTimePtEtaUp','JESTimePtEtaDown','JERup','JERdown','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','TTNORMup','TTNORMdown','MUONIDISOup','MUONIDISOdown','HIPup','HIPdown','MUONHLTup','MUONHLTdown','BTAGup','BTAGdown','QCDSCALEup','QCDSCALEdown','topPtReweight','PDFup','PDFdown']
	
	_Variations_ee = ['','JESAbsoluteMPFBiasUp','JESAbsoluteMPFBiasDown','JESAbsoluteScaleUp','JESAbsoluteScaleDown','JESAbsoluteStatUp','JESAbsoluteStatDown','JESFlavorQCDUp','JESFlavorQCDDown','JESFragmentationUp','JESFragmentationDown','JESPileUpDataMCUp','JESPileUpDataMCDown','JESPileUpPtBBUp','JESPileUpPtBBDown','JESPileUpPtEC1Up','JESPileUpPtEC1Down','JESPileUpPtEC2Up','JESPileUpPtEC2Down','JESPileUpPtHFUp','JESPileUpPtHFDown','JESPileUpPtRefUp','JESPileUpPtRefDown','JESRelativeBalUp','JESRelativeBalDown','JESRelativeFSRUp','JESRelativeFSRDown','JESRelativeJEREC1Up','JESRelativeJEREC1Down','JESRelativeJEREC2Up','JESRelativeJEREC2Down','JESRelativeJERHFUp','JESRelativeJERHFDown','JESRelativePtBBUp','JESRelativePtBBDown','JESRelativePtEC1Up','JESRelativePtEC1Down','JESRelativePtEC2Up','JESRelativePtEC2Down','JESRelativePtHFUp','JESRelativePtHFDown','JESRelativeStatECUp','JESRelativeStatECDown','JESRelativeStatFSRUp','JESRelativeStatFSRDown','JESRelativeStatHFUp','JESRelativeStatHFDown','JESSinglePionECALUp','JESSinglePionECALDown','JESSinglePionHCALUp','JESSinglePionHCALDown','JESTimePtEtaUp','JESTimePtEtaDown','JERup','JERdown','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','TTNORMup','TTNORMdown','ELEIDISOup','ELEIDISOdown','ELEHLTup','ELEHLTdown','BTAGup','BTAGdown','QCDSCALEup','QCDSCALEdown','topPtReweight','PDFup','PDFdown']
	
	_VariationsNoUD = ['topPtReweight']
	
	#correLated_Vars = ['JESAbsoluteMPFBiasUp','JESAbsoluteMPFBiasDown','JESAbsoluteScaleUp','JESAbsoluteScaleDown','JESAbsoluteStatUp','JESAbsoluteStatDown','JESFlavorQCDUp','JESFlavorQCDDown','JESFragmentationUp','JESFragmentationDown','JESPileUpDataMCUp','JESPileUpDataMCDown','JESPileUpPtBBUp','JESPileUpPtBBDown','JESPileUpPtEC1Up','JESPileUpPtEC1Down','JESPileUpPtEC2Up','JESPileUpPtEC2Down','JESPileUpPtHFUp','JESPileUpPtHFDown','JESPileUpPtRefUp','JESPileUpPtRefDown','JESRelativeBalUp','JESRelativeBalDown','JESRelativeFSRUp','JESRelativeFSRDown','JESRelativeJEREC1Up','JESRelativeJEREC1Down','JESRelativeJEREC2Up','JESRelativeJEREC2Down','JESRelativeJERHFUp','JESRelativeJERHFDown','JESRelativePtBBUp','JESRelativePtBBDown','JESRelativePtEC1Up','JESRelativePtEC1Down','JESRelativePtEC2Up','JESRelativePtEC2Down','JESRelativePtHFUp','JESRelativePtHFDown','JESRelativeStatECUp','JESRelativeStatECDown','JESRelativeStatFSRUp','JESRelativeStatFSRDown','JESRelativeStatHFUp','JESRelativeStatHFDown','JESSinglePionECALUp','JESSinglePionECALDown','JESSinglePionHCALUp','JESSinglePionHCALDown','JESTimePtEtaUp','JESTimePtEtaDown','JERup','JERdown','LUMIup','LUMIdown','PUup','PUdown','BTAGup','BTAGdown','QCDSCALEup','QCDSCALEdown','topPtReweight']
	unCorrelat_Vars = ['ZNORMup','ZNORMdown','TTNORMup','TTNORMdown','MUONIDISOup','MUONIDISOdown','HIPup','HIPdown','MUONHLTup','MUONHLTdown','ELEIDISOup','ELEIDISOdown','ELEHLTup','ELEHLTdown']
	
	
	
	## this is what actually was run in HHResultsProducer, note that qcdscale is splitted into 6 variations
	## use for --checkfiles
	_Variations_toRun_uu = ['','JESAbsoluteMPFBiasUp','JESAbsoluteMPFBiasDown','JESAbsoluteScaleUp','JESAbsoluteScaleDown','JESAbsoluteStatUp','JESAbsoluteStatDown','JESFlavorQCDUp','JESFlavorQCDDown','JESFragmentationUp','JESFragmentationDown','JESPileUpDataMCUp','JESPileUpDataMCDown','JESPileUpPtBBUp','JESPileUpPtBBDown','JESPileUpPtEC1Up','JESPileUpPtEC1Down','JESPileUpPtEC2Up','JESPileUpPtEC2Down','JESPileUpPtHFUp','JESPileUpPtHFDown','JESPileUpPtRefUp','JESPileUpPtRefDown','JESRelativeBalUp','JESRelativeBalDown','JESRelativeFSRUp','JESRelativeFSRDown','JESRelativeJEREC1Up','JESRelativeJEREC1Down','JESRelativeJEREC2Up','JESRelativeJEREC2Down','JESRelativeJERHFUp','JESRelativeJERHFDown','JESRelativePtBBUp','JESRelativePtBBDown','JESRelativePtEC1Up','JESRelativePtEC1Down','JESRelativePtEC2Up','JESRelativePtEC2Down','JESRelativePtHFUp','JESRelativePtHFDown','JESRelativeStatECUp','JESRelativeStatECDown','JESRelativeStatFSRUp','JESRelativeStatFSRDown','JESRelativeStatHFUp','JESRelativeStatHFDown','JESSinglePionECALUp','JESSinglePionECALDown','JESSinglePionHCALUp','JESSinglePionHCALDown','JESTimePtEtaUp','JESTimePtEtaDown','JERup','JERdown','JESup','JESdown','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','TTNORMup','TTNORMdown','MUONIDISOup','MUONIDISOdown','HIPup','HIPdown','MUONHLTup','MUONHLTdown','BTAGup','BTAGdown','QCDscaleR1F2','QCDscaleR2F1','QCDscaleR2F2','QCDscaleR1F0p5','QCDscaleR0p5F1','QCDscaleR0p5F0p5','topPtReweight']
	
	_Variations_toRun_ee = ['','JESAbsoluteMPFBiasUp','JESAbsoluteMPFBiasDown','JESAbsoluteScaleUp','JESAbsoluteScaleDown','JESAbsoluteStatUp','JESAbsoluteStatDown','JESFlavorQCDUp','JESFlavorQCDDown','JESFragmentationUp','JESFragmentationDown','JESPileUpDataMCUp','JESPileUpDataMCDown','JESPileUpPtBBUp','JESPileUpPtBBDown','JESPileUpPtEC1Up','JESPileUpPtEC1Down','JESPileUpPtEC2Up','JESPileUpPtEC2Down','JESPileUpPtHFUp','JESPileUpPtHFDown','JESPileUpPtRefUp','JESPileUpPtRefDown','JESRelativeBalUp','JESRelativeBalDown','JESRelativeFSRUp','JESRelativeFSRDown','JESRelativeJEREC1Up','JESRelativeJEREC1Down','JESRelativeJEREC2Up','JESRelativeJEREC2Down','JESRelativeJERHFUp','JESRelativeJERHFDown','JESRelativePtBBUp','JESRelativePtBBDown','JESRelativePtEC1Up','JESRelativePtEC1Down','JESRelativePtEC2Up','JESRelativePtEC2Down','JESRelativePtHFUp','JESRelativePtHFDown','JESRelativeStatECUp','JESRelativeStatECDown','JESRelativeStatFSRUp','JESRelativeStatFSRDown','JESRelativeStatHFUp','JESRelativeStatHFDown','JESSinglePionECALUp','JESSinglePionECALDown','JESSinglePionHCALUp','JESSinglePionHCALDown','JESTimePtEtaUp','JESTimePtEtaDown','JERup','JERdown','JESup','JESdown','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','TTNORMup','TTNORMdown','ELEHLTup','ELEHLTdown','ELEIDISOup','ELEIDISOdown','BTAGup','BTAGdown','QCDscaleR1F2','QCDscaleR2F1','QCDscaleR2F2','QCDscaleR1F0p5','QCDscaleR0p5F1','QCDscaleR0p5F0p5','topPtReweight']
	
	
	## qcdscale has 6 variations to be combined to up down
	## use for --QCDScale
	_qcdSc_Variations = ['','QCDscaleR1F2','QCDscaleR2F1','QCDscaleR2F2','QCDscaleR1F0p5','QCDscaleR0p5F1','QCDscaleR0p5F0p5']
	
	
	## pdf has 101 variations to be combined to up down
	## use for '--PDF
	_PDFVariations = []
	for n in range(101) :
		#print 'factor_nnpdf_' + str(n+1)
		pdf_varname = 'factor_nnpdf_' + str(n+1)
		_PDFVariations += [pdf_varname]
	

	##---- process PDF variations
	if '--PDF' in sys.argv:
		variationName = 'PDF'
		listOfVariations = _PDFVariations # copy the reference to the listOfVariations

		for ilep in range(len(_leps)):
			fup = open(txtDir + _leps[ilep] + '/OptHH_resCuts_Smoothed_pol2cutoff_systable_'+variationName+'up.txt','w')
			fdn = open(txtDir + _leps[ilep] + '/OptHH_resCuts_Smoothed_pol2cutoff_systable_'+variationName+'down.txt','w')
			headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV', 'QCD', 'SMH']
			header = 'headers = '+str(headers)
			fup.write(header+'\n')
			fdn.write(header+'\n')
			fmiss = []
			for m in _mass :
				print '  doing mass ', m
				if (not doindiv) and _leptonChan[ilep] == 'ee' and int(m) <= 300:
					bdtname = "_s"+x_spin+"_bdt_discrim_LowM"
				else:
					bdtname = "_s"+x_spin+"_bdt_discrim_M" + m
				outStrUp = resType + m + "_" + _leptonChan[ilep] + bdtname + "_"+variationName+"up_13TeV_new.root"
				outRootFileUp = ROOT.TFile(outStrUp,"RECREATE")
				dirThisUp = outRootFileUp.mkdir(resType + _analysisChan[ilep])
				
				outStrDn = resType + m + "_" + _leptonChan[ilep] + bdtname + "_"+variationName+"down_13TeV_new.root"
				outRootFileDn = ROOT.TFile(outStrDn,"RECREATE")
				dirThisDn = outRootFileDn.mkdir(resType + _analysisChan[ilep])

				inputFiles = []
				for qcdScVar in listOfVariations :
					finStr = resType + m + "_" + _leptonChan[ilep] + bdtname + "_" + qcdScVar + "_13TeV_new.root"
					input = ROOT.TFile.Open(finStr, "READ")
					print 'opening file ', finStr, ' ---> ', input.IsOpen()
					if (not input.IsOpen()):
						fmiss += [finStr]
					inputFiles += [input]
				#print 'inputFiles ', inputFiles

				hups_rate = []
				hdns_rate = []
				for proc in procs :
					print ' doing proc: ', proc
					histos_var = []
					for i in range(len(listOfVariations)) :

						if listOfVariations[i] == '' :
							histopath = resType + _analysisChan[ilep] + '/' + proc
						else :
							histopath = resType + _analysisChan[ilep] + '/' + proc + '_' + listOfVariations[i].replace('up','Up').replace('down','Down')
						#print '     retrieving hist ', histopath
						hist = inputFiles[i].Get(histopath)
						histos_var += [hist]
						del hist
					#print '   histos_var ', histos_var

					#--- calculation to get half of the 16th and 84th pecentile band as uncertainty (symmetric)
					[histOutUp, histOutDn] = CreatePDFHistos_Ordering(histos_var)
					#--- write histo for this proc
					dirThisUp.cd()
					histOutUp.Write(proc+"_"+variationName+"Up")
					dirThisDn.cd()
					histOutDn.Write(proc+"_"+variationName+"Down")

					hup_rate = str([histOutUp.Integral(), int(histOutUp.GetEntries())])
					hdn_rate = str([histOutDn.Integral(), int(histOutDn.GetEntries())])
					hups_rate += [hup_rate]
					hdns_rate += [hdn_rate]

				sysline_up = 'L_t_' + resType + m + ' = ['
				for x in hups_rate:
					sysline_up += ' '+(x)
					sysline_up += ' , '
				sysline_up = sysline_up[0:-2]+' ]'

				sysline_dn = 'L_t_' + resType + m + ' = ['
				for x in hdns_rate:
					sysline_dn += ' '+(x)
					sysline_dn += ' , '
				sysline_dn = sysline_dn[0:-2]+' ]'
				print sysline_up
				print sysline_dn
				fup.write(sysline_up+'\n')
				fdn.write(sysline_dn+'\n')

				#--- close files for this mass
				outRootFileUp.Close()
				outRootFileDn.Close()
				for inFile in inputFiles:
					inFile.Close()
			fup.close()
			fdn.close()

			print ' missing files for ' + _analysisChan[ilep] + ' : ', len(fmiss)
			for fm in fmiss:
				print fm

	##---- process the QCD Scale variations ---
	if '--QCDScale' in sys.argv:
		variationName = 'QCDSCALE'
		listOfVariations = _qcdSc_Variations # copy the reference to the listOfVariations
		
		for ilep in range(len(_leps)):
			fup = open(txtDir + _leps[ilep] + '/OptHH_resCuts_Smoothed_pol2cutoff_systable_'+variationName+'up.txt','w')
			fdn = open(txtDir + _leps[ilep] + '/OptHH_resCuts_Smoothed_pol2cutoff_systable_'+variationName+'down.txt','w')
			headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV', 'QCD', 'SMH']
			header = 'headers = '+str(headers)
			fup.write(header+'\n')
			fdn.write(header+'\n')
			fmiss = []
			for m in _mass :
				print '  doing mass ', m
				if (not doindiv) and _leptonChan[ilep] == 'ee' and int(m) <= 300:
					bdtname = "_s"+x_spin+"_bdt_discrim_LowM"
				else:
					bdtname = "_s"+x_spin+"_bdt_discrim_M" + m
				outStrUp = resType + m + "_" + _leptonChan[ilep] + bdtname + "_"+variationName+"up_13TeV_new.root"
				outRootFileUp = ROOT.TFile(outStrUp,"RECREATE")
				#dirThisDn = outRootFileDn.mkdir("HHresuujj")
				dirThisUp = outRootFileUp.mkdir(resType + _analysisChan[ilep])

				outStrDn = resType + m + "_" + _leptonChan[ilep] + bdtname + "_"+variationName+"down_13TeV_new.root"
				outRootFileDn = ROOT.TFile(outStrDn,"RECREATE")
				#dirThisDn = outRootFileDn.mkdir("HHresuujj")
				dirThisDn = outRootFileDn.mkdir(resType + _analysisChan[ilep])

				inputFiles = []
				for qcdScVar in listOfVariations :
					finStr = resType + m + "_" + _leptonChan[ilep] + bdtname + "_" + qcdScVar + "_13TeV_new.root"
					input = ROOT.TFile.Open(finStr, "READ")
					print 'opening file ', finStr, ' ---> ', input.IsOpen()
					if (not input.IsOpen()):
						fmiss += [finStr]
					inputFiles += [input]
				#print 'inputFiles ', inputFiles

				hups_rate = []
				hdns_rate = []
				for proc in procs :
					histos_var = []
					for i in range(len(listOfVariations)) :

						if listOfVariations[i] == '' :
							#histopath = 'HHresuujj/'+ proc
							histopath = resType + _analysisChan[ilep] + '/' + proc
						else :
							#histopath = 'HHresuujj/'+ proc + '_' + listOfVariations[i].replace('up','Up').replace('down','Down')
							histopath = resType + _analysisChan[ilep] + '/' + proc + '_' + listOfVariations[i].replace('up','Up').replace('down','Down')
						#print '     retrieving hist ', histopath
						hist = inputFiles[i].Get(histopath)
						histos_var += [hist]
						del hist
					#print '   histos_var ', histos_var
					#print '  proc ', proc

					#--- calculation to get largest deviation
					histOutUp = CreateScaleUpHisto(histos_var)
					histOutDn = CreateScaleDnHisto(histos_var)
					
					hup_int = histOutUp.Integral()
					hup_ent = histOutUp.GetEntries()
					hdn_int = histOutDn.Integral()
					hdn_ent = histOutDn.GetEntries()
					
					hup_rate = str([hup_int, int(hup_ent)]) #the number of entries will be wrong but we do not care
					hdn_rate = str([hdn_int, int(hdn_ent)]) #the number of entries will be wrong but we do not care
					
					#--- write histo for this proc
					dirThisUp.cd()
					histOutUp.Write(proc+"_"+variationName+"Up")
					dirThisDn.cd()
					histOutDn.Write(proc+"_"+variationName+"Down")
					
					hups_rate += [hup_rate]
					hdns_rate += [hdn_rate]
					#if proc == 'WJets': print ' ', proc, ' hup_rate ', hup_rate, ' hdn_rate ', hdn_rate
					#if proc == 'WJets': print ' CenEntry ', histos_var[0].GetEntries(), ' Out eff entry ', histOutUp.GetEffectiveEntries(), histOutDn.GetEffectiveEntries()
					
				sysline_up = 'L_t_' + resType + m + ' = ['
				for x in hups_rate:
					sysline_up += ' '+(x)
					sysline_up += ' , '
				sysline_up = sysline_up[0:-2]+' ]'

				sysline_dn = 'L_t_' + resType + m + ' = ['
				for x in hdns_rate:
					sysline_dn += ' '+(x)
					sysline_dn += ' , '
				sysline_dn = sysline_dn[0:-2]+' ]'
				print sysline_up
				print sysline_dn
				fup.write(sysline_up+'\n')
				fdn.write(sysline_dn+'\n')

				#--- close files for this mass
				outRootFileUp.Close()
				outRootFileDn.Close()
				for inFile in inputFiles:
					inFile.Close()
			fup.close()
			fdn.close()

			print ' missing files for ' + _analysisChan[ilep] + ' : ', len(fmiss)
			for fm in fmiss:
				print fm

	##---- process the std variations ---
	if '--Standard' in sys.argv:
		for ilep in range(len(_leps)):
			if _analysisChan[ilep] == 'uujj': _Variations = _Variations_uu
			if _analysisChan[ilep] == 'eejj': _Variations = _Variations_ee
			fmiss = []
			for m in _mass :
				if (not doindiv) and _leptonChan[ilep] == 'ee' and int(m) <= 300:
					bdtname = "_s"+x_spin+"_bdt_discrim_LowM"
				else:
					bdtname = "_s"+x_spin+"_bdt_discrim_M" + m
				
				output = resType + m + "_" + _leptonChan[ilep] + "_bdt_discrim_M" + m + "_13TeV_new.root"
				outputRootFile = ROOT.TFile(output,"RECREATE")
				dirThis = outputRootFile.mkdir("HHres" + _analysisChan[ilep])
				
				#fnameInps = []
				for var in _Variations :
					finStr = resType + m + "_" + _leptonChan[ilep] + bdtname + "_" + var + "_13TeV_new.root"
					tmp_var = var
					var = var.replace('up','Up')
					var = var.replace('down','Down')
					#fnameInps += [finStr]
					input = ROOT.TFile.Open(finStr, "READ")
					print 'opening file ', finStr, ' ---> ', input.IsOpen()
					if (not input.IsOpen()):
						fmiss += [finStr]
					for proc in procs :
						if var == '' :
							histopath = resType + _analysisChan[ilep] + '/' + proc
						else :
							histopath = resType + _analysisChan[ilep] + '/' + proc + '_' + var
						#print 'retrieving hist ', histopath
						hist = input.Get(histopath)
						dirThis.cd()
						if proc == "HHres": proc = resType
						if var == '' :
							hist.Write(proc)
							for v_noud in _VariationsNoUD :
								hist.Write(proc + '_' + v_noud + 'Down') # write the central as 'Down' of the single-sided
							# write the central as for the mising ones
							#hist.Write(proc + '_ZNORMUp') # to be fix (removed),
							#hist.Write(proc + '_MESUp') # to be fix (removed)
						elif var in _VariationsNoUD :
							hist.Write(proc + '_' + var + 'Up') # write the single-sided as 'Up'
						else :
							if tmp_var == 'MUONIDISOup':
								hist.Write(proc + '_CMS_eff_mUp')
							elif tmp_var == 'MUONIDISOdown':
								hist.Write(proc + '_CMS_eff_mDown')
							elif tmp_var == 'MUONHLTup':
								hist.Write(proc + '_CMS_eff_trigger_uuUp')
							elif tmp_var == 'MUONHLTdown':
								hist.Write(proc + '_CMS_eff_trigger_uuDown')
							elif tmp_var == 'ELEIDISOup':
								hist.Write(proc + '_CMS_eff_eUp')
							elif tmp_var == 'ELEIDISOdown':
								hist.Write(proc + '_CMS_eff_eDown')
							elif tmp_var == 'ELEHLTup':
								hist.Write(proc + '_CMS_eff_trigger_eeUp')
							elif tmp_var == 'ELEHLTdown':
								hist.Write(proc + '_CMS_eff_trigger_eeDown')
							elif tmp_var == 'BTAGup':
								hist.Write(proc + '_CMS_btag_combUp')
							elif tmp_var == 'BTAGdown':
								hist.Write(proc + '_CMS_btag_combDown')
							elif tmp_var == 'JERup':
								hist.Write(proc + '_CMS_res_jUp')
							elif tmp_var == 'JERdown':
								hist.Write(proc + '_CMS_res_jDown')
							elif tmp_var == 'LUMIup':
								hist.Write(proc + '_lumi_13TeVUp')
							elif tmp_var == 'LUMIdown':
								hist.Write(proc + '_lumi_13TeVDown')
							elif tmp_var == 'PDFup':
								hist.Write(proc + '_pdfUp')
							elif tmp_var == 'PDFdown':
								hist.Write(proc + '_pdfDown')
							elif tmp_var == 'QCDSCALEup':
								hist.Write(proc + '_QCDscaleUp')
							elif tmp_var == 'QCDSCALEdown':
								hist.Write(proc + '_QCDscaleDown')
							elif tmp_var in unCorrelat_Vars:
								hist.Write(proc + '_' + _leptonChan[ilep] + var)
							else:
								hist.Write(proc + '_' + var)
						del hist
					input.Close()
				outputRootFile.Close()
			
			print ' missing files for ' + _analysisChan[ilep] +  ' : ', len(fmiss)
			for fm in fmiss:
				print fm

	##---- checking process of the std variations ---
	if '--checkfiles' in sys.argv:
		uu_varToResub = []
		ee_varToResub = []
		fmiss = []
		for c in _leptonChan:
			if c == 'uu':
				_VariationsCheck = _Variations_toRun_uu # copy the reference to the _VariationsCheck
			elif c == 'ee':
				_VariationsCheck = _Variations_toRun_ee # copy the reference to the _VariationsCheck
			if '--checkpdffiles' in sys.argv:
				_VariationsCheck = _PDFVariations # copy the reference to the _VariationsCheck
							
			for v in _VariationsCheck:
				for m in _mass :
					if (not doindiv) and c == 'ee' and int(m) <= 300:
						bdtname = "_s"+x_spin+"_bdt_discrim_LowM"
					else:
						bdtname = "_s"+x_spin+"_bdt_discrim_M" + m
					finStr = resType + m + '_' + c + bdtname + "_" + v + "_13TeV_new.root"
					input = ROOT.TFile.Open(finStr, "READ")
					try:
						isop = input.IsOpen()
					except ReferenceError:
						isop = False
					if (not isop): print 'checking file ', finStr, ' ---> ', isop
					if (isop):
						input.Close()
					else:
						fmiss += [finStr]
						if c == 'uu':
							if v not in uu_varToResub:
								uu_varToResub+=[v]
						elif c == 'ee':
							if v not in ee_varToResub:
								ee_varToResub+=[v]
		print ' missing root files : ', len(fmiss)
		for fm in fmiss:
			print fm

		txt_f_miss = []
		for ilep in range(len(_leptonChan)):
			if _leptonChan[ilep] == 'uu':
				_VariationsCheck = _Variations_toRun_uu # copy the reference to the _VariationsCheck
			elif _leptonChan[ilep] == 'ee':
				_VariationsCheck = _Variations_toRun_ee # copy the reference to the _VariationsCheck
			if '--checkpdffiles' in sys.argv:
				_VariationsCheck = _PDFVariations # copy the reference to the _VariationsCheck

			for v in _VariationsCheck:
				txt_finStr = txtDir + _leps[ilep] + "/OptHH_resCuts_Smoothed_pol2cutoff_systable_" + v + ".txt"
				isop = True
				try:
					input = open(txt_finStr,'r')
				except IOError:
					isop = False
				if (not isop): print 'checking txt file ', txt_finStr, ' ---> ', isop
				if (isop):
					input.close()
				else:
					txt_f_miss += [txt_finStr]
					if _leptonChan[ilep] == 'uu':
						if v not in uu_varToResub:
							uu_varToResub+=[v]
					elif _leptonChan[ilep] == 'ee':
						if v not in ee_varToResub:
							ee_varToResub+=[v]
		print ' missing txt files : ', len(txt_f_miss)
		for fm in txt_f_miss:
			print fm

		print ' variations to be resub uu : ', len(uu_varToResub)
		for vresub in uu_varToResub:
			print vresub
		print ' variations to be resub ee : ', len(ee_varToResub)
		for vresub in ee_varToResub:
			print vresub

		print '***** Resubmitting missing jobs *****'
		for ilep in range(len(_analysisChan)):
			if _analysisChan[ilep] == 'uujj':
				_thesevars = uu_varToResub
			
			elif _analysisChan[ilep] == 'eejj':
				_thesevars = ee_varToResub

			for v in _thesevars:
				txt_finStr = txtDir + _leps[ilep] + "/OptHH_resCuts_Smoothed_pol2cutoff_systable_" + v + ".txt"
				delete_txtFileCom = 'rm ' + txt_finStr
				print delete_txtFileCom
				# delete unfinished txt files if using "--launch" argument
				if '--launch' in sys.argv:
					os.system(delete_txtFileCom)
				runfile = '__'+('HHResultProducer.py').replace('.py','__'+v+'__'+_analysisChan[ilep]+'.py')
				ftcsh = runfile.replace('.py','.tcsh')
				#bsub = 'bsub -q 2nd -e /dev/null -J '+runfile.split('.')[0]+' < '+ftcsh #was 1nw
				bsub = 'bsub -q 8nh -e /dev/null -J '+runfile.split('.')[0]+' < '+ftcsh #was 1nw
				print bsub
				# Run bsub command if using "--launch" argument
				if '--launch' in sys.argv:
						os.system(bsub)

	##---- Organizing root files and txt files
	if '--organizefiles' in sys.argv:
		#--- root files and job submission files
		roocom1 = 'mv *0_13TeV_new.root  rootfiles_final/.'
		roocom2 = 'mv *QCDscale*.root  rootfiles_QCDscale/.'
		roocom3 = 'mv *_factor_nnpdf_*.root rootfiles_pdfs/.'
		roocom4 = 'mv *_13TeV_new.root rootfiles_std/.'
		roocom5 = 'mv __HHResultProducer__* runfiles_tmp/.'
		roocom6 = 'mv LSFJOB_* runfiles_tmp/.'
		if '--launch' in sys.argv:
			os.system ('mkdir rootfiles_final')
			os.system ('mkdir rootfiles_QCDscale')
			os.system ('mkdir rootfiles_pdfs')
			os.system ('mkdir rootfiles_std')
			os.system ('mkdir runfiles_tmp')
			os.system (roocom1)
			os.system (roocom2)
			os.system (roocom3)
			os.system (roocom4)
			os.system (roocom5)
			os.system (roocom6)
		print '  going to run command '
		print roocom1 + '\n' + roocom2 + '\n' + roocom3 + '\n' + roocom4 + '\n'
		print roocom5 + '\n' + roocom6 + '\n'
		
		#--- txt file
		uudir = 'Results_Testing_diHiggs_newNtuples_MuCutsMC0p49_muon/'
		eedir = 'Results_Testing_diHiggs_newNtuples_MuCutsMC0p49_electron/'

		uucom1 = 'mv '+ uudir + 'Opt*_systable_JESdown.txt ' + uudir + 'files_JES_old/.'
		uucom2 = 'mv '+ uudir + 'Opt*_systable_JESup.txt ' + uudir + 'files_JES_old/.'
		uucom3 = 'mv '+ uudir + '*ELE*.txt '            + uudir + 'files_ELE/.'
		uucom4 = 'mv '+ uudir + '*_factor_nnpdf_*.txt ' + uudir + 'files_pdfs/.'
		uucom5 = 'mv '+ uudir + '*QCDscale*.txt '       + uudir + 'files_QCDscale/.'
		print '  going to run command '
		print uucom1 + '\n' + uucom2 + '\n' + uucom3 + '\n' + uucom4 + '\n' + uucom5 + '\n'
		if '--launch' in sys.argv:
			os.system ('mkdir -p ' + uudir + 'files_JES_old')
			os.system ('mkdir -p ' + uudir + 'files_ELE')
			os.system ('mkdir -p ' + uudir + 'files_pdfs')
			os.system ('mkdir -p ' + uudir + 'files_QCDscale')
			os.system (uucom1)
			os.system (uucom2)
			os.system (uucom3)
			os.system (uucom4)
			os.system (uucom5)
		eecom1 = 'mv '+ eedir + 'Opt*_systable_JESdown.txt ' + eedir + 'files_JES_old/.'
		eecom2 = 'mv '+ eedir + 'Opt*_systable_JESup.txt ' + eedir + 'files_JES_old/.'
		eecom3 = 'mv '+ eedir + '*MUON*.txt '           + eedir + 'files_MUON/.'
		eecom4 = 'mv '+ eedir + '*_factor_nnpdf_*.txt ' + eedir + 'files_pdfs/.'
		eecom5 = 'mv '+ eedir + '*QCDscale*.txt '       + eedir + 'files_QCDscale/.'
		eecom6 = 'mv '+ eedir + '*systable_HIP*.txt '       + eedir + 'files_MUON/.'
		print '  going to run command '
		print eecom1 + '\n' + eecom2 + '\n' + eecom3 + '\n' + eecom4 + '\n' + eecom5 + '\n' + eecom6 + '\n'
		if '--launch' in sys.argv:
			os.system ('mkdir -p ' + eedir + 'files_JES_old')
			os.system ('mkdir -p ' + eedir + 'files_MUON')
			os.system ('mkdir -p ' + eedir + 'files_pdfs')
			os.system ('mkdir -p ' + eedir + 'files_QCDscale')
			os.system (eecom1)
			os.system (eecom2)
			os.system (eecom3)
			os.system (eecom4)
			os.system (eecom5)
			os.system (eecom6)


def GetStats(List):
	av = 0.0
	n = 1.0*len(List)
	for x in List:
		av += x
	av = av/n
	dev = 0.0
	while True:
		N=0
		dev += 0.00001
		for x in List:
			if abs(x-av)<dev:
				N+= 1
		if N>.68*len(List):
			break
	return [av,dev, str(round(av,3)) +' +- '+str(round(dev,3))]

def CreatePDFHistos(histos_var):
	houtUp = histos_var[0].Clone()
	houtDn = histos_var[0].Clone()
	for bin in range(histos_var[0].GetNbinsX()+2) :
		cenval = histos_var[0].GetBinContent(bin)
		cenerr = histos_var[0].GetBinError(bin)
		l = []
		for ipdf in range(len(histos_var)) :
			a = histos_var[ipdf].GetBinContent(bin)
			l += [a]
		out = GetStats(l)
		houtUp.SetBinContent(bin, cenval+out[1])
		houtUp.SetBinError(bin, 0.0)
		houtDn.SetBinContent(bin, cenval-out[1])
		houtDn.SetBinError(bin, 0.0)
		print ' --- finish doing bin ', bin, ' central val ', cenval, ' PDFup val ', cenval+out[1]
	return [houtUp,houtDn]

def CreatePDFHistos_Ordering(histos_var):
	houtUp = histos_var[0].Clone()
	houtDn = histos_var[0].Clone()
	for bin in range(histos_var[0].GetNbinsX()+2) :
		cenval = histos_var[0].GetBinContent(bin)
		#cenerr = histos_var[0].GetBinError(bin)
		l = []
		for ipdf in range(len(histos_var)) :
			a = histos_var[ipdf].GetBinContent(bin)
			l += [a]
		sortL = mergesort(l)
		dev = (sortL[84]-sortL[16])/2.0
		houtUp.SetBinContent(bin, cenval+dev)
		houtUp.SetBinError(bin, 0.0)
		houtDn.SetBinContent(bin, cenval-dev)
		houtDn.SetBinError(bin, 0.0)
		print ' --- finish doing bin: ', bin, 'central val:', cenval, 'PDFdn val:', cenval-dev, 'PDFup val:', cenval+dev, '16th:',sortL[16], '84th:',sortL[84]
	return [houtUp,houtDn]



def CreateScaleUpHisto(histos_var):
	hout = histos_var[0].Clone()
	hout_tmp = histos_var[0].Clone()
	for bin in range(hout.GetNbinsX()+2) :
		maxval = histos_var[0].GetBinContent(bin)
		maxerr = histos_var[0].GetBinError(bin)
		#print ' --- doing bin ', bin, ' initial max val ', maxval
		for scal in range(len(histos_var)) :
			#print '     --- doing histo ',scal, histos_var[scal].GetTitle()
			if (histos_var[scal].GetBinContent(bin) > maxval) :
				maxval = histos_var[scal].GetBinContent(bin)
				maxerr = histos_var[scal].GetBinError(bin)
				#print '         max is ', maxval, maxerr
		#print ' --- got maxval ', maxval, maxerr
		hout.SetBinContent(bin, maxval)
		#hout.SetBinError(bin, maxerr)
		hout.SetBinError(bin, 0.) # I decide to set the error to 0
	if (hout.Integral() <= 0): hout = hout_tmp.Clone() ### combine tool does not like when the integral <= 0
	return hout

def CreateScaleDnHisto(histos_var):
	hout = histos_var[0].Clone()
	hout_tmp = histos_var[0].Clone()
	for bin in range(hout.GetNbinsX()+2) :
		maxval = histos_var[0].GetBinContent(bin)
		maxerr = histos_var[0].GetBinError(bin)
		#print ' --- doing bin ', bin, ' initial max val ', maxval
		for scal in range(len(histos_var)) :
			#print '     --- doing histo ',scal, histos_var[scal].GetTitle()
			if (histos_var[scal].GetBinContent(bin) < maxval) :
				maxval = histos_var[scal].GetBinContent(bin)
				maxerr = histos_var[scal].GetBinError(bin)
				#print '         min is ', maxval, maxerr
		#print ' --- got minval ', maxval, maxerr
		hout.SetBinContent(bin, maxval)
		#hout.SetBinError(bin, maxerr)
		hout.SetBinError(bin, 0.) # I decide to set the error to 0
	if (hout.Integral() <= 0): hout = hout_tmp.Clone() ### combine tool does not like when the integral <= 0
	return hout



def merge(left, right):
	result = []
	i,j = 0, 0
	while (i < len(left) and j < len(right)):
		if (left[i] < right[j]):
			result += [left[i]]
			i += 1
		else:
			result += [right[j]]
			j += 1
	while (i < len(left)):
		result += [left[i]]
		i += 1
	while (j < len(right)):
		result += [right[j]]
		j += 1
	return result

def mergesort(L):
	""" Returns a new sorted list containing the same elements as L"""
	#print L
	if len(L) < 2:
		#print ' reach 1 element', L
		return L[:]
	else:
		middle = len(L)/2
		left = mergesort(L[:middle])
		right = mergesort(L[middle:])
		#print 'left ', left, 'right ', right
		together = merge(left,right)
		#print 'merged ', together, ' length ', len(together)
		return together



if __name__ == "__main__":
	main()

# I have to check if JER Up and Down are the same ? no they are different ?





