#!/bin/tcsh

# Set up CMSSW
scramv1 p -n CMSSW_7_4_16_PUCALC CMSSW_7_4_16

cd CMSSW_7_4_16_PUCALC/src
cmsenv
#git clone https://github.com/cms-sw/RecoLuminosity-LumiDB.git RecoLuminosity/LumiDB
#cd RecoLuminosity/LumiDB
#git checkout V04-02-10
#scramv1 b
#cmsenv
#cd scripts
###################################################################
# Integrated Luminosity and Pileup Calculation
# https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2015Analysis
###################################################################

# Set the LumiJSON and PUJSON for PU Calculations
#set LumiJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt
set LumiJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt

#set PUJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_JSON_DCSONLY_190389-208686_corr.txt
set PUJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt

#./pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec 69400 --maxPileupBin 60 --numPileupBins 60 PU_Central.root
#./pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec 73564 --maxPileupBin 60 --numPileupBins 60 PU_Up.root
#./pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec 65236 --maxPileupBin 60 --numPileupBins 60 PU_Down.root

#pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec 69000 --maxPileupBin 52 --numPileupBins 52 PU_Central_69mb.root

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec 69000 --maxPileupBin 52 --numPileupBins 52 PU_Central.root

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec 72450 --maxPileupBin 52 --numPileupBins 52 PU_Up.root

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec 65500 --maxPileupBin 52 --numPileupBins 52 PU_Down.root

#echo "(19.712 +/- 0.513)/fb">LumiLog.txt
echo "( 2154.493 +/- ....)/pb">LumiLog.txt

cp $LumiJSON ../../
cp LumiLog.txt ../../
cp PU*root ../../
cd ../../
rm -r CMSSW_7_4_16_PUCALC

echo "\n ------ Done! ------\n"
echo "\nPlease find LumiLog at:"
ls LumiLog.txt
echo "\nPlease find PU files at:"
ls PU*root
echo "These results were built for good json file:"
echo $LumiJSON
echo "which has been copied to the current directory"
#echo "\n\n Note, results valid for Jan2013 ReReco with (19.712 +/- 0.513)/fb.\n\n"
