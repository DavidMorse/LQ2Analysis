import os

output = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/comboTrees/SummaryFiles/'
y16 = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2016/gmadigan/NTupleAnalyzer_nanoAOD_RunFull2016_BDT_FullSys_PDF_stockNano_2022_05_19_19_13_13/DaveSummaryFiles/'
y17 = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/dmorseSkim/2017/NTupleAnalyzer_nanoAOD_RunFull2017_BDT_fullSys_2022_05_20_23_30_36/SummaryFiles/'
y18 = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/NanoAODv7/2018/gmadigan/NTupleAnalyzer_nanoAOD_RunFull2018_BDT_FullSys_PDF_stockNano_2022_05_24_19_50_25/SummaryFiles/'

for m in ["300","400","500","600","700","800","900","1000","1100","1200","1300","1400","1500","1600","1700","1800","1900","2000","2100","2200","2300","2400","2500","2600","2700","2800","2900","3000","3500","4000"] :
    print "hadd "+output+"LQuujj"+m+".root "+y16+"LQuujj"+m+".root "+y17+"LQuujj"+m+".root "+y18+"LQuujj"+m+".root&"

print ''

for name in ['DiBoson.root','SingleMuData.root','SingleTop.root','TTBar.root','TTV.root','WJets.root','ZJets.root'] :
    print "hadd "+output+name+' '+y18+name+' '+y16+name+' '+y17+name+' &'



