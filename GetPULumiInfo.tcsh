#!/bin/tcsh


# Set up CMSSW

scramv1 p -n CMSSW_5_3_9_PUCALC CMSSW_5_3_9

cd CMSSW_5_3_9_PUCALC/src
cmsenv
git clone https://github.com/cms-sw/RecoLuminosity-LumiDB.git RecoLuminosity/LumiDB
cd RecoLuminosity/LumiDB
git checkout V04-02-10
scramv1 b
cmsenv
cd scripts
###################################################################
# Integrated Luminosity and Pileup Calculation
# https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2012Analysis#Analysis_based_on_CMSSW_5_3_X_re
###################################################################

# Set the LumiJSON and PUJSON for PU Calculations
set LumiJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt

set PUJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_JSON_DCSONLY_190389-208686_corr.txt

./pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec 69400 --maxPileupBin 60 --numPileupBins 60 PU_Central.root

./pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec 73564 --maxPileupBin 60 --numPileupBins 60 PU_Up.root

./pileupCalc.py -i $LumiJSON --inputLumiJSON $PUJSON --calcMode true --minBiasXsec 65236 --maxPileupBin 60 --numPileupBins 60 PU_Down.root

echo "(19.712 +/- 0.513)/fb">LumiLog.txt

cp $LumiJSON ../../../../../
cp LumiLog.txt ../../../../../
cp PU*root ../../../../../
cd ../../../../../
rm -r CMSSW_5_3_9_PUCALC

echo "\n ------ Done! ------\n"
echo "\nPlease find LumiLog at:"
ls LumiLog.txt
echo "\nPlease find PU files at:"
ls PU*root
echo"These resulst were built for good json file:"
echo $LumiJSON
echo "which has been copied to the current directory"
echo "\n\n Note, results valid for Jan2013 ReReco with (19.712 +/- 0.513)/fb.\n\n"
