#!/bin/tcsh

# Set up CMSSW
scramv1 p -n CMSSW_10_3_3_PUCALC CMSSW_10_3_3

cd CMSSW_10_3_3_PUCALC/src
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

set minBCentral = 69200
set minBUp      = 72383.2
set minBDown    = 66016.8

echo "------- Making PU distributions for 2016 ------"

set LumiJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt
set PUJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec $minBcentral --maxPileupBin 100 --numPileupBins 100 PU_Central_2016.root

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec $minBUp --maxPileupBin 100 --numPileupBins 100 PU_Up_2016.root

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec $minBDown --maxPileupBin 100 --numPileupBins 100 PU_2016.root

echo "( 35863.308 +/- 932.446)/pb">LumiLog.txt

echo "------- Making PU distributions for 2017 ------"

set LumiJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt
set PUJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/pileup_latest.txt

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec $minBcentral --maxPileupBin 100 --numPileupBins 100 PU_Central_2017.root

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec $minBUp --maxPileupBin 100 --numPileupBins 100 PU_Up_2017.root

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec $minBDown --maxPileupBin 100 --numPileupBins 100 PU_2017.root

echo "(  +/-  )/pb">LumiLog.txt

echo "------- Making PU distributions for 2018 ------"

set LumiJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt
set PUJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PileUp/pileup_latest.txt

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec $minBcentral --maxPileupBin 100 --numPileupBins 100 PU_Central_2018.root

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec $minBUp --maxPileupBin 100 --numPileupBins 100 PU_Up_2018.root

pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec $minBDown --maxPileupBin 100 --numPileupBins 100 PU_2018.root

echo "(  +/-  )/pb">LumiLog.txt


cp $LumiJSON ../../
cp LumiLog.txt ../../
cp PU*root ../../
cd ../../
rm -r CMSSW_10_3_3_PUCALC

echo "\n ------ Done! ------\n"
echo "\nPlease find LumiLog at:"
ls LumiLog.txt
echo "\nPlease find PU files at:"
ls PU*root
echo "These results were built for good json file:"
echo $LumiJSON
echo "which has been copied to the current directory"
