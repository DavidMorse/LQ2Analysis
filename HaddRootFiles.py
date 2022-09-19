import os

for icopy in range(51):
    # copy files from SummaryFiles
    print 'From ', str('/eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles'),':\n\n'
    print 'Copying DiBoson_amcNLO.root ...\n'
    os.system('cp /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/DiBoson_amcNLO.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17')

    print 'Copying DiBoson_Powheg.root ...\n'
    os.system('cp /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/DiBoson_Powheg.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17')

    print 'Copying TTBar_Inc.root ...\n'
    os.system('cp /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/TTBar_Inc.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17')

    print 'Copying WJetsPtBin.root ...\n'
    os.system('cp /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/WJetsPtBin.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17')

    print 'Copying ZJetsPtBin.root ...\n'
    os.system('cp /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/ZJetsPtBin.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17')

    print 'Copying ZJetsM10-50.root ...\n'
    os.system('cp /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/ZJetsM10-50.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17')

    #hadd ZJets
    print 'hadd ZJetsPtBin.root and ZJetsM10-50.root into ZJetsPtBinM10-50.root ...\n'
    os.system('hadd /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/ZJetsPtBinM10-50.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/ZJetsPtBin.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/ZJetsM10-50.root')

    #hadd 
    print 'hadd DiBoson_Powheg.root and DiBoson_amcNLO.root into DiBoson_Powheg_amcNLO.root ...\n'
    os.system('hadd /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/DiBoson_Powheg_amcNLO.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/DiBoson_Powheg.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/DiBoson_amcNLO.root')

    #Create symlinks
    print 'Creating symlink of DiBoson_Powheg_amcNLO.root as DiBoson.root in SummaryFiles ...\n'
    os.system('ln -s /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/DiBoson_Powheg_amcNLO.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/DiBoson.root')

    print 'Creating symlink of TTBar_Inc.root as TTBar.root in SummaryFiles ...\n'
    os.system('ln -s /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/TTBar_Inc.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/TTBar.root')

    print 'Creating symlink of WJetsPtBin.root as WJets.root in SummaryFiles ...\n'
    os.system('ln -s /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/WJetsPtBin.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/WJets.root')

    print 'Creating symlink of ZJetsPtBinM10-50.root as ZJets.root in SummaryFiles ...\n'
    os.system('ln -s /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/ZJetsPtBinM10-50.root /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/ZJets.root')

    # Remove redundant files in SummaryFiles
    #print 'Removing DiBoson_amcNLO.root from SummaryFiles ...\n'
    #os.system('rm /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/DiBoson_amcNLO.root')

    #print 'Removing DiBoson_Powheg.root from SummaryFiles ...\n'
    #os.system('rm /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/DiBoson_Powheg.root')

    #print 'Removing TTBar_Inc.root from SummaryFiles ...\n'
    #os.system('rm /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/TTBar_Inc.root')

    #print 'Removing WJetsPtBin.root from SummaryFiles ...\n'
    #os.system('rm /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/WJetsPtBin.root')

    #print 'Removing ZJetsPtBin.root from SummaryFiles ...\n'
    #os.system('rm /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/ZJetsPtBin.root')

    #print 'Removing ZJetsM10-50.root from SummaryFiles ...\n'
    #os.system('rm /eos/user/g/gmadigan/MES_Syst_Study/NTupleAnalyzer_nanoAOD_GESystVar2_FullMC2016_stockNano_GEcopy'+str(icopy)+'_2022_02_23_22_53_17/SummaryFiles/ZJetsM10-50.root')

    print 'Done.\n\n'

