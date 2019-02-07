LQ2Analysis13TeV
===============

Batch-processing facility for EXO Leptons+Jets Ntuples to create light-weight trees, and analyzer facility for histograms, signal-background separation optimization, event-counting and limit-setting. 

Darin Baumgartel (darinb@cern.ch) Feb 2014
cloned to David Morse (dmorse@cern.ch) May 2015

===============
*** Running Instructions: This requires running on the CERN LXPlus5 computing system. ****

--------------------------------------------------------------------------------

[STEP 1]

Checking out the package

git clone git@github.com:DavidMorse/LQ2Analysis.git LQ2Analysis13TeV

cd LQ2Analysis13TeV

--------------------------------------------------------------------------------

[STEP 2]

Running the code to get the pileup-reweighting histograms and integrated-lumi info.

./GetPULumiInfo.tcsh

--------------------------------------------------------------------------------

[STEP 3]

Organize your NTuples by creating a CSV file which contains the NTuple Information.

CSV files should have columns like :
SignalType,Xsections,N_orig,Group,CustomJson,EOSDirectory

A little info:
- SignalType:    A unique identifier at the beginning of the names of the root files.
- Xsections:     The cross-section to normalize the sample to (NLO is better!)
- N_orig:        The original number of events in the sample... more on this in [STEP 4]
- Group:         The group for the files. For instance, you might have three SignalTypes
                like WW, WZ, and ZZ, and want to put them in a Group called "DiBoson"
- CustomJson:    The name of a Json file specifying the good runs/lumis to use. This can 
                be the same for every data type, or different, or 0 for MC
- EOSDirectory:  The eos path where the files are kept for this signaltype. Should be
                like a typical EOS path e.g. /store/group/..../


Please see a convenient example: 
NTupleInfo2016Full.csv

--------------------------------------------------------------------------------

[STEP 4]

Get the original number of events for MC (to fill out the N_orig in the csv file).

Use the counting histograms in the ntuples to determine this. There is a way of batching this and gathering the results, as such:

  > python AnalyzerMakerFastLocal.py -i NTupleInfo2015Full_MiniAODv2.csv -py NTupleEvCounter.py -t PreFullLumiCountUpdate -j Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_Silver_v2.txt -p 0 -q 8nh -s 100 --FileRefresh
  
  Some notes on the arguments:
  
-  -i CSV File:     The CSV file you wish to run on
-  -t Tag name:    Results will output in a directory specified by this tag-name
-  -j JSON file:    Not important here, needed in [STEP 5]
-  -p 0:            Not important here, needed in [STEP 5]
-  -q 8nh:          The batch queue to use.
-  -s 100:          Number of files to analyzer per batch job (the split number)
-  --FileRefresh:   The code will automatically make a list of good ntuple files and store
                    it locally for future use, so it doesn't have to re-read directories 
                    all the time. This demands to re-read directories.


--------------------------------------------------------------------------------

[STEP 5]

Make the analysis trees.

