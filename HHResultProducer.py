import os, sys, math, random
from glob import glob


#global preselectionmumu 

##########################################################################
########    GLOBAL VARIABLES NEEDED FOR PLOTS AND ANALYSIS        ########
##########################################################################

# Directory where root files are kept and the tree you want to get root files from
# QCDDirectory = '/store/group/phys_exotica/darinb/SharedAnalyzer/NTupleAnalyzer_FullJuly24QCDNonIsoQuickTest_2014_07_25_15_39_48/SummaryFiles'
# EMuDirectory = '/store/group/phys_exotica/darinb/SharedAnalyzer/NTupleAnalyzer_FullJuly24EMuSwitch_2014_07_25_03_54_54/SummaryFiles'
# NormalDirectory='/store/group/phys_exotica/darinb/SharedAnalyzer/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles'
#QCDDirectory  = 'NTupleAnalyzer_FullJuly24QCDNonIsoQuickTest_2014_07_25_15_39_48/SummaryFiles'
#EMuDirectory  = 'NTupleAnalyzer_FullJuly24EMuSwitch_2014_07_25_03_54_54/SummaryFiles'
#NormalDirectory='NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles'

#NormalDirectory = '/media/dataPlus/dmorse/hhNtuples/NTupleAnalyzerHH_Full2016HH_2016_11_25/SummaryFiles'
NormalDirectory = '/media/dataPlus/dmorse/hhNtuples/NTupleAnalyzerHH_Full2016HH_QuickTest_2017_06_01_15_10_10/SummaryFiles'
QCDDirectory = '/media/dataPlus/dmorse/hhNtuples/NTupleAnalyzerHH_Full2016HH_v236_QCDNonIsoQuickTest_2017_05_15/SummaryFiles'
EMuDirectory = 'emu'

#NormalDirectory = 'NTupleAnalyzer_Jan30_76X_FULL_2016_02_06_18_41_13/SummaryFiles'
#QCDDirectory    = '/store/user/dmorse/leptoQuark/NTupleAnalyzer_Dec10_Spring2015Full_QCDNonIsoQuickTest_2015_12_11_11_39_40/SummaryFiles'
#EMuDirectory    = 'NTupleAnalyzer_Jan30_76X_EMuSwitch_2016_02_08_11_57_48/SummaryFiles'

# The name of the main ttree (ntuple structure)
TreeName = "PhysicalVariables"

# Integrated luminosity for normalization
#lumi =  2318.348
#lumi = 2690.707
#lumi = 40000.0
#lumi = 21780.339
lumi= 35863.308

#HLT_Ele17_Ele12...DZ
##lumi=20809.806

#HLT_Ele23_Ele12...DZ
#lumi=27213.867

#Muon HLT MC scale factor
#https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2

# Single-mu trigger efficiencies as a function of muon Eta. 
# This is for the case of one muon
#2012#singlemuHLT =  '*( 0.93*(abs(Eta_muon1)<=0.9) + 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) + 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) )'
singlemuHLT =  '*( 0.9494*(abs(Eta_muon1)<=0.9)*(Pt_muon1>50)*(Pt_muon1<60) + 0.9460*(abs(Eta_muon1)<=0.9)*(Pt_muon1>60) + 0.9030*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>50)*(Pt_muon1<60) + 0.8968*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>60) + 0.9153*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>50)*(Pt_muon1<60) + 0.9175*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>60) )'
# This is for the case of two muons (i.e. the above factors, but for the case where the event has two muons)
#2012#doublemuHLT =  '*(1.0-(( 1.0 - 0.93*(abs(Eta_muon1)<=0.9) - 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) - 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) )'
#2012#doublemuHLT += '*( 1.0 - 0.93*(abs(Eta_muon2)<=0.9) - 0.83*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2) - 0.80*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1) )))'
#doublemuHLT =  '*(1.0-(( 1.0 - 0.9494*(abs(Eta_muon1)<=0.9)*(Pt_muon1>50)*(Pt_muon1<60) - 0.9460*(abs(Eta_muon1)<=0.9)*(Pt_muon1>60) - 0.9030*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>50)*(Pt_muon1<60) - 0.8968*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>60) - 0.9153*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>50)*(Pt_muon1<60) - 0.9175*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>60) )'
#doublemuHLT += '*( 1.0 - 0.9494*(abs(Eta_muon2)<=0.9)*(Pt_muon2>50)*(Pt_muon2<60) - 0.9460*(abs(Eta_muon2)<=0.9)*(Pt_muon2>60) - 0.9030*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>50)*(Pt_muon2<60) - 0.8968*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>60) - 0.9153*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>50)*(Pt_muon2<60) - 0.9175*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>60) )))'


#fixme todo this is applying a weight of .995 for two central muons, which is 1-(1-eff1)*(1-eff2)= eff1+eff2 - eff1*eff2.  Using now instead just eff1*eff2
#doublemuHLT =  '*((( 0.93*(abs(Eta_muon1)<=0.9) + 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) + 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) ))'
#doublemuHLT += '*( 0.93*(abs(Eta_muon2)<=0.9) + 0.83*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2) + 0.80*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1) ))'

#2015 values, taken from AN2016_021_v6.pdf
doublemuHLT = '*((abs(Eta_muon1)<=0.9)*(0.9490*(abs(Eta_muon2)<=0.9)+0.9490*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.4)+0.9376*(abs(Eta_muon2)>1.4)*(abs(Eta_muon2)<=2.1)+0.9207*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4))+(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.4)*(0.9628*(abs(Eta_muon2)<=0.9)+0.9576*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.4)+0.9288*(abs(Eta_muon2)>1.4)*(abs(Eta_muon2)<=2.1)+0.9684*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4))+(abs(Eta_muon1)>1.4)*(abs(Eta_muon1)<=2.1)*(0.9477*(abs(Eta_muon2)<=0.9)+0.9493*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.4)+0.9216*(abs(Eta_muon2)>1.4)*(abs(Eta_muon2)<=2.1)+0.9333*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4))+(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<=2.4)*(0.9420*(abs(Eta_muon2)<=0.9)+0.9142*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.4)+0.9470*(abs(Eta_muon2)>1.4)*(abs(Eta_muon2)<=2.1)+0.9252*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4)))'

# This is for the case of the E-mu sample, where one "muon" is replaced by an electron. In that case, we check
# which muon is a real muon (IsMuon_muon1) and apply the trigger efficiency based on the muon
#2012#singlemuHLTEMU = '*((IsMuon_muon1*( 0.93*(abs(Eta_muon1)<=0.9) + 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) + 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) ))'
#2012#singlemuHLTEMU += '+(IsMuon_muon2*( 0.93*(abs(Eta_muon2)<=0.9) + 0.83*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2) + 0.80*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1) )))'
singlemuHLTEMU = '*((IsMuon_muon1*( 0.9494*(abs(Eta_muon1)<=0.9)*(Pt_muon1>50)*(Pt_muon1<60) + 0.9460*(abs(Eta_muon1)<=0.9)*(Pt_muon1>60) + 0.9030*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>50)*(Pt_muon1<60) + 0.8968*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>60) + 0.9153*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>50)*(Pt_muon1<60) + 0.9175*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>60) ))'
singlemuHLTEMU += '+(IsMuon_muon2*( 0.9494*(abs(Eta_muon2)<=0.9)*(Pt_muon2>50)*(Pt_muon2<60) + 0.9460*(abs(Eta_muon2)<=0.9)*(Pt_muon2>60) + 0.9030*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>50)*(Pt_muon2<60) + 0.8968*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>60) + 0.9153*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>50)*(Pt_muon2<60) + 0.9175*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>60) )))'

#Muon ID and Iso MC scale factors
#https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2


#doubleMuIdAndIsoScale = '*((0.9837160408450394*(Eta_muon1>-2.4)*(Eta_muon1>-2.1)+0.9945438368059955*(Eta_muon1>-2.1)*(Eta_muon1>-1.6)+0.9970378022168973*(Eta_muon1>-1.6)*(Eta_muon1>-1.2)+0.9956615088416513*(Eta_muon1>-1.2)*(Eta_muon1>-0.9)+0.9978576536660979*(Eta_muon1>-0.9)*(Eta_muon1>-0.3)+0.9924072276003321*(Eta_muon1>-0.0)*(Eta_muon1>-0.2)+0.9966624814619885*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.9940334796698915*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998044399081353*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.9952984093114865*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.9967601541976385*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.9959660681513732*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.9858520897236493*(Eta_muon1>2.1)*(Eta_muon1<2.4))*(0.9837160408450394*(Eta_muon1>-2.4)*(Eta_muon1>-2.1)+0.9945438368059955*(Eta_muon1>-2.1)*(Eta_muon1>-1.6)+0.9970378022168973*(Eta_muon1>-1.6)*(Eta_muon1>-1.2)+0.9956615088416513*(Eta_muon1>-1.2)*(Eta_muon1>-0.9)+0.9978576536660979*(Eta_muon1>-0.9)*(Eta_muon1>-0.3)+0.9924072276003321*(Eta_muon1>-0.0)*(Eta_muon1>-0.2)+0.9966624814619885*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.9940334796698915*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998044399081353*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.9952984093114865*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.9967601541976385*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.9959660681513732*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.9858520897236493*(Eta_muon1>2.1)*(Eta_muon1<2.4)))'

doubleMuIdAndIsoScale = '*((0.9837*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.9945*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.9970*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.9957*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.9979*(Eta_muon1>-0.9)*(Eta_muon1<-0.3)+0.9924*(Eta_muon1>-0.0)*(Eta_muon1<-0.2)+0.9967*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.9940*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.9980*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.9953*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.9968*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.9960*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.9859*(Eta_muon1>2.1)*(Eta_muon1<2.4))*(0.9837*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.9945*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.9970*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.9957*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.9979*(Eta_muon1>-0.9)*(Eta_muon1<-0.3)+0.9924*(Eta_muon1>-0.0)*(Eta_muon1<-0.2)+0.9967*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.9940*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.9980*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.9953*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.9968*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.9960*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.9859*(Eta_muon1>2.1)*(Eta_muon1<2.4)))'

doubleMuIdScale = '*(0.9682423360434217*(Eta_muon1<-2.4)*(Eta_muon1>-2.1)+0.9893833099668479*(Eta_muon1<-2.1)*(Eta_muon1>-1.6)+0.9943077120257308*(Eta_muon1<-1.6)*(Eta_muon1>-1.2)+0.9916914851938796*(Eta_muon1<-1.2)*(Eta_muon1>-0.9)+0.995621634743804*(Eta_muon1<-0.9)*(Eta_muon1>-0.3)+0.9852246225934387*(Eta_muon1<-0.0)*(Eta_muon1>-0.2)+0.9939788646593908*(Eta_muon1<-0.2)*(Eta_muon1>0.2)+0.9885359568100729*(Eta_muon1<0.2)*(Eta_muon1>0.3)+0.9958132831910403*(Eta_muon1<0.3)*(Eta_muon1>0.9)+0.9902529688519877*(Eta_muon1<0.9)*(Eta_muon1>1.2)+0.9934874686188648*(Eta_muon1<1.2)*(Eta_muon1>1.6)+0.9923028170743358*(Eta_muon1<1.6)*(Eta_muon1>2.1)+0.9724438481770842*(Eta_muon1<2.1)*(Eta_muon1>2.4))*(0.9682423360434217*(Eta_muon2<-2.4)*(Eta_muon2>-2.1)+0.9893833099668479*(Eta_muon2<-2.1)*(Eta_muon2>-1.6)+0.9943077120257308*(Eta_muon2<-1.6)*(Eta_muon2>-1.2)+0.9916914851938796*(Eta_muon2<-1.2)*(Eta_muon2>-0.9)+0.995621634743804*(Eta_muon2<-0.9)*(Eta_muon2>-0.3)+0.9852246225934387*(Eta_muon2<-0.0)*(Eta_muon2>-0.2)+0.9939788646593908*(Eta_muon2<-0.2)*(Eta_muon2>0.2)+0.9885359568100729*(Eta_muon2<0.2)*(Eta_muon2>0.3)+0.9958132831910403*(Eta_muon2<0.3)*(Eta_muon2>0.9)+0.9902529688519877*(Eta_muon2<0.9)*(Eta_muon2>1.2)+0.9934874686188648*(Eta_muon2<1.2)*(Eta_muon2>1.6)+0.9923028170743358*(Eta_muon2<1.6)*(Eta_muon2>2.1)+0.9724438481770842*(Eta_muon2<2.1)*(Eta_muon2>2.4))'

#doubleMuIdScale = '*((0.9813326964101629*(Pt_muon1>50)*(Pt_muon1<55)+0.9811215588407185*(Pt_muon1>55)*(Pt_muon1<60)+0.9888030350742609*(Pt_muon1>60)*(Pt_muon1<120)+1.0179598732419621*(Pt_muon1>120))*(0.9813326964101629*(Pt_muon2>50)*(Pt_muon2<55)+0.9811215588407185*(Pt_muon2>55)*(Pt_muon2<60)+0.9888030350742609*(Pt_muon2>60)*(Pt_muon2<120)+1.0179598732419621*(Pt_muon2>120)))'

doubleMuIsoScale = '*(0.999189745646657*(Eta_muon1<-2.4)*(Eta_muon1>-2.1)+0.999704363645143*(Eta_muon1<-2.1)*(Eta_muon1>-1.6)+0.9997678924080637*(Eta_muon1<-1.6)*(Eta_muon1>-1.2)+0.9996315324894229*(Eta_muon1<-1.2)*(Eta_muon1>-0.9)+1.0000936725883918*(Eta_muon1<-0.9)*(Eta_muon1>-0.3)+0.9995898326072254*(Eta_muon1<-0.0)*(Eta_muon1>-0.2)+0.9993460982645863*(Eta_muon1<-0.2)*(Eta_muon1>0.2)+0.9995310025297102*(Eta_muon1<0.2)*(Eta_muon1>0.3)+1.0002755149716656*(Eta_muon1<0.3)*(Eta_muon1>0.9)+1.0003438497709853*(Eta_muon1<0.9)*(Eta_muon1>1.2)+1.0000328397764122*(Eta_muon1<1.2)*(Eta_muon1>1.6)+0.9996293192284107*(Eta_muon1<1.6)*(Eta_muon1>2.1)+0.9992603312702144*(Eta_muon1<2.1)*(Eta_muon1>2.4))*(0.999189745646657*(Eta_muon2<-2.4)*(Eta_muon2>-2.1)+0.999704363645143*(Eta_muon2<-2.1)*(Eta_muon2>-1.6)+0.9997678924080637*(Eta_muon2<-1.6)*(Eta_muon2>-1.2)+0.9996315324894229*(Eta_muon2<-1.2)*(Eta_muon2>-0.9)+1.0000936725883918*(Eta_muon2<-0.9)*(Eta_muon2>-0.3)+0.9995898326072254*(Eta_muon2<-0.0)*(Eta_muon2>-0.2)+0.9993460982645863*(Eta_muon2<-0.2)*(Eta_muon2>0.2)+0.9995310025297102*(Eta_muon2<0.2)*(Eta_muon2>0.3)+1.0002755149716656*(Eta_muon2<0.3)*(Eta_muon2>0.9)+1.0003438497709853*(Eta_muon2<0.9)*(Eta_muon2>1.2)+1.0000328397764122*(Eta_muon2<1.2)*(Eta_muon2>1.6)+0.9996293192284107*(Eta_muon2<1.6)*(Eta_muon2>2.1)+0.9992603312702144*(Eta_muon2<2.1)*(Eta_muon2>2.4))'

#doubleMuIsoScale = '*((0.9985465327438463*(Pt_muon1>50)*(Pt_muon1<55)+0.9988891755735836*(Pt_muon1>55)*(Pt_muon1<60)+0.9989480835906359*(Pt_muon1>60)*(Pt_muon1<120)+1.0006806854046033*(Pt_muon1>120))*(0.9985465327438463*(Pt_muon2>50)*(Pt_muon2<55)+0.9988891755735836*(Pt_muon2>55)*(Pt_muon2<60)+0.9989480835906359*(Pt_muon2>60)*(Pt_muon2<120)+1.0006806854046033*(Pt_muon2>120)))'


singleMuIdScale = '*(0.9813326964101629*(Pt_muon1>50)*(Pt_muon1<55)+0.9811215588407185*(Pt_muon1>55)*(Pt_muon1<60)+0.9888030350742609*(Pt_muon1>60)*(Pt_muon1<120)+1.0179598732419621*(Pt_muon1>120))'

singleMuIsoScale = '*(0.9985465327438463*(Pt_muon1>50)*(Pt_muon1<55)+0.9988891755735836*(Pt_muon1>55)*(Pt_muon1<60)+0.9989480835906359*(Pt_muon1>60)*(Pt_muon1<120)+1.0006806854046033*(Pt_muon1>120))'

MuIdScaleEMU = '*(IsMuon_muon1*(0.9813326964101629*(Pt_muon1>50)*(Pt_muon1<55)+0.9811215588407185*(Pt_muon1>55)*(Pt_muon1<60)+0.9888030350742609*(Pt_muon1>60)*(Pt_muon1<120)+1.0179598732419621*(Pt_muon1>120))+IsMuon_muon2*(0.9813326964101629*(Pt_muon2>50)*(Pt_muon2<55)+0.9811215588407185*(Pt_muon2>55)*(Pt_muon2<60)+0.9888030350742609*(Pt_muon2>60)*(Pt_muon2<120)+1.0179598732419621*(Pt_muon2>120)))'

MuIsoScaleEMU = '*(IsMuon_muon1*(0.9985465327438463*(Pt_muon1>50)*(Pt_muon1<55)+0.9988891755735836*(Pt_muon1>55)*(Pt_muon1<60)+0.9989480835906359*(Pt_muon1>60)*(Pt_muon1<120)+1.0006806854046033*(Pt_muon1>120))+IsMuon_muon2*(0.9985465327438463*(Pt_muon2>50)*(Pt_muon2<55)+0.9988891755735836*(Pt_muon2>55)*(Pt_muon2<60)+0.9989480835906359*(Pt_muon2>60)*(Pt_muon2<120)+1.0006806854046033*(Pt_muon2>120)))'


# This is the rescaling of the EMu data for the ttbar estimate (2 - Eff_trigger)
dataHLTEMUADJ = '*(2.0 - 1.0'+singlemuHLTEMU+')'

bTagSF = '*(0.901114+(1.32145e-05*(Pt_Hjet1)))*(0.931535+(1.40704e-05*(Pt_Hjet2)))'


#This is for HIP problem https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2#Tracking_efficiency_provided_by
trackerHIP1 = '*(0.991237*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.994853*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.996413*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.997157*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.997512*(Eta_muon1>-0.9)*(Eta_muon1<-0.6)+0.99756*(Eta_muon1>-0.6)*(Eta_muon1<-0.3)+0.996745*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.996996*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.99772*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998604*(Eta_muon1>0.3)*(Eta_muon1<0.6)+0.998321*(Eta_muon1>0.6)*(Eta_muon1<0.9)+0.997682*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.995252*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.994919*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.987334*(Eta_muon1>2.1)*(Eta_muon1<2.4) )'
trackerHIP2 = '*(0.991237*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.994853*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.996413*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.997157*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.997512*(Eta_muon2>-0.9)*(Eta_muon2<-0.6)+0.99756*(Eta_muon2>-0.6)*(Eta_muon2<-0.3)+0.996745*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.996996*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.99772*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.998604*(Eta_muon2>0.3)*(Eta_muon2<0.6)+0.998321*(Eta_muon2>0.6)*(Eta_muon2<0.9)+0.997682*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.995252*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.994919*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.987334*(Eta_muon2>2.1)*(Eta_muon2<2.4) )'

trackerHIPEMU  = '*((IsMuon_muon1)*(0.991237*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.994853*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.996413*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.997157*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.997512*(Eta_muon1>-0.9)*(Eta_muon1<-0.6)+0.99756*(Eta_muon1>-0.6)*(Eta_muon1<-0.3)+0.996745*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.996996*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.99772*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998604*(Eta_muon1>0.3)*(Eta_muon1<0.6)+0.998321*(Eta_muon1>0.6)*(Eta_muon1<0.9)+0.997682*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.995252*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.994919*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.987334*(Eta_muon1>2.1)*(Eta_muon1<2.4) )'
trackerHIPEMU += '+(IsMuon_muon2)*(0.991237*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.994853*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.996413*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.997157*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.997512*(Eta_muon2>-0.9)*(Eta_muon2<-0.6)+0.99756*(Eta_muon2>-0.6)*(Eta_muon2<-0.3)+0.996745*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.996996*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.99772*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.998604*(Eta_muon2>0.3)*(Eta_muon2<0.6)+0.998321*(Eta_muon2>0.6)*(Eta_muon2<0.9)+0.997682*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.995252*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.994919*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.987334*(Eta_muon2>2.1)*(Eta_muon2<2.4) ))'

eleRECOScale = '*((1-IsMuon_muon1)*(((Eta_muon1>-2.5)*(Eta_muon1<-2.45)*1.3176)+((Eta_muon1>-2.45)*(Eta_muon1<-2.4)*1.11378)+((Eta_muon1>-2.4)*(Eta_muon1<-2.3)*1.02463)+((Eta_muon1>-2.3)*(Eta_muon1<-2.2)*1.01364)+((Eta_muon1>-2.2)*(Eta_muon1<-2)*1.00728)+((Eta_muon1>-2)*(Eta_muon1<-1.8)*0.994819)+((Eta_muon1>-1.8)*(Eta_muon1<-1.63)*0.994786)+((Eta_muon1>-1.63)*(Eta_muon1<-1.566)*0.991632)+((Eta_muon1>-1.566)*(Eta_muon1<-1.444)*0.963128)+((Eta_muon1>-1.444)*(Eta_muon1<-1.2)*0.989701)+((Eta_muon1>-1.2)*(Eta_muon1<-1)*0.985656)+((Eta_muon1>-1)*(Eta_muon1<-0.6)*0.981595)+((Eta_muon1>-0.6)*(Eta_muon1<-0.4)*0.984678)+((Eta_muon1>-0.4)*(Eta_muon1<-0.2)*0.981614)+((Eta_muon1>-0.2)*(Eta_muon1<0)*0.980433)+((Eta_muon1>0)*(Eta_muon1<0.2)*0.984552)+((Eta_muon1>0.2)*(Eta_muon1<0.4)*0.988764)+((Eta_muon1>0.4)*(Eta_muon1<0.6)*0.987743)+((Eta_muon1>0.6)*(Eta_muon1<1)*0.987743)+((Eta_muon1>1)*(Eta_muon1<1.2)*0.987743)+((Eta_muon1>1.2)*(Eta_muon1<1.444)*0.98768)+((Eta_muon1>1.444)*(Eta_muon1<1.566)*0.967598)+((Eta_muon1>1.566)*(Eta_muon1<1.63)*0.989627)+((Eta_muon1>1.63)*(Eta_muon1<1.8)*0.992761)+((Eta_muon1>1.8)*(Eta_muon1<2)*0.991761)+((Eta_muon1>2)*(Eta_muon1<2.2)*0.99794)+((Eta_muon1>2.2)*(Eta_muon1<2.3)*1.00104)+((Eta_muon1>2.3)*(Eta_muon1<2.4)*0.989507)+((Eta_muon1>2.4)*(Eta_muon1<2.45)*0.970519)+((Eta_muon1>2.45)*(Eta_muon1<2.5)*0.906667))+((1-IsMuon_muon2)*(((Eta_muon2>-2.5)*(Eta_muon2<-2.45)*1.3176)+((Eta_muon2>-2.45)*(Eta_muon2<-2.4)*1.11378)+((Eta_muon2>-2.4)*(Eta_muon2<-2.3)*1.02463)+((Eta_muon2>-2.3)*(Eta_muon2<-2.2)*1.01364)+((Eta_muon2>-2.2)*(Eta_muon2<-2)*1.00728)+((Eta_muon2>-2)*(Eta_muon2<-1.8)*0.994819)+((Eta_muon2>-1.8)*(Eta_muon2<-1.63)*0.994786)+((Eta_muon2>-1.63)*(Eta_muon2<-1.566)*0.991632)+((Eta_muon2>-1.566)*(Eta_muon2<-1.444)*0.963128)+((Eta_muon2>-1.444)*(Eta_muon2<-1.2)*0.989701)+((Eta_muon2>-1.2)*(Eta_muon2<-1)*0.985656)+((Eta_muon2>-1)*(Eta_muon2<-0.6)*0.981595)+((Eta_muon2>-0.6)*(Eta_muon2<-0.4)*0.984678)+((Eta_muon2>-0.4)*(Eta_muon2<-0.2)*0.981614)+((Eta_muon2>-0.2)*(Eta_muon2<0)*0.980433)+((Eta_muon2>0)*(Eta_muon2<0.2)*0.984552)+((Eta_muon2>0.2)*(Eta_muon2<0.4)*0.988764)+((Eta_muon2>0.4)*(Eta_muon2<0.6)*0.987743)+((Eta_muon2>0.6)*(Eta_muon2<1)*0.987743)+((Eta_muon2>1)*(Eta_muon2<1.2)*0.987743)+((Eta_muon2>1.2)*(Eta_muon2<1.444)*0.98768)+((Eta_muon2>1.444)*(Eta_muon2<1.566)*0.967598)+((Eta_muon2>1.566)*(Eta_muon2<1.63)*0.989627)+((Eta_muon2>1.63)*(Eta_muon2<1.8)*0.992761)+((Eta_muon2>1.8)*(Eta_muon2<2)*0.991761)+((Eta_muon2>2)*(Eta_muon2<2.2)*0.99794)+((Eta_muon2>2.2)*(Eta_muon2<2.3)*1.00104)+((Eta_muon2>2.3)*(Eta_muon2<2.4)*0.989507)+((Eta_muon2>2.4)*(Eta_muon2<2.45)*0.970519)+((Eta_muon2>2.45)*(Eta_muon2<2.5)*0.906667))))'

eleHEEPScale = '*((1-IsMuon_muon1)*(((Eta_muon1>-2.5)*(Eta_muon1<-1.566)*0.984)+((Eta_muon1>-1.4442)*(Eta_muon1<-0.5)*0.971)+((Eta_muon1>-0.5)*(Eta_muon1<-0.0)*0.961)+((Eta_muon1>0.0)*(Eta_muon1<0.5)*0.973)+((Eta_muon1>0.5)*(Eta_muon1<1.4442)*0.978)+((Eta_muon1>1.566)*(Eta_muon1<2.5)*0.980))+(1-IsMuon_muon2)*(((Eta_muon2>-2.5)*(Eta_muon2<-1.566)*0.984)+((Eta_muon2>-1.4442)*(Eta_muon2<-0.5)*0.971)+((Eta_muon2>-0.5)*(Eta_muon2<-0.0)*0.961)+((Eta_muon2>0.0)*(Eta_muon2<0.5)*0.973)+((Eta_muon2>0.5)*(Eta_muon2<1.4442)*0.978)+((Eta_muon2>1.566)*(Eta_muon2<2.5)*0.980)))'

# Weights for different MC selections, including integrated luminosity, event weight, and trigger weight
NormalWeightMuMu = str(lumi)+'*weight_central*weight_topPt'+trackerHIP1+trackerHIP2+doublemuHLT+doubleMuIdAndIsoScale#+bTagSF #fixme turning off trigger eff. for now
NormalWeightMuNu = str(lumi)+'*weight_central*weight_topPt'+singlemuHLT+singleMuIdScale+singleMuIsoScale+trackerHIP1
NormalWeightEMu = str(lumi)+'*weight_central*weight_topPt'+singlemuHLTEMU+MuIdScaleEMU+MuIsoScaleEMU+eleRECOScale+eleHEEPScale+trackerHIPEMU
NormalWeightEMuNoHLT = str(lumi)+'*weight_central*weight_topPt'+MuIdScaleEMU+MuIsoScaleEMU+eleRECOScale+eleHEEPScale+trackerHIPEMU#fixme do we need scale factors here?

# This is the real data trigger condition
dataHLT = '*(pass_HLT_Mu17_Mu8)'

# This is the set of event filters used
passfilter =  '*(passDataCert*passPrimaryVertex*(GoodVertexCount>=1))'
passfilter += '*(passHBHENoiseFilter*passHBHENoiseIsoFilter)'
passfilter += '*(passBadEESuperCrystal*passEcalDeadCellTP)'
passfilter += '*(passBeamHalo2016)'
passfilter += '*(passBadMuon*passBadChargedHadron)'
#passfilter += '*(noBadMuonsFlag*(1-duplicateMuonsFlag))'

# This defines the preselections for the mu-mu, mu-nu, and e-mu samples
preselectionmumu = '((Pt_muon1>20)*(Pt_muon2>10)*(Pt_Hjet1>20)*(Pt_Hjet2>20)*(Pt_Zjet1>20)*(Pt_Zjet2>20)*(M_uu>12))'
#preselectionmumu = '((Pt_muon1>20)*(Pt_muon2>10)*(Pt_Hjet1>25)*(Pt_Hjet2>25)*(Pt_Zjet1>20)*(Pt_Zjet2>20)*(Charge_muon1*Charge_muon2<0)*(CISV_bjet1>0.8)*(CISV_bjet2>0.46)*(abs(cosThetaStarMu)<0.9)*(M_uu>10)*(DPhi_uu_jj_Z<2.75)*(Pt_miss<150)*(M_uu<105)*(isMuonEvent>0))'

preselectionmunu = '((Pt_muon1>50)*(Pt_muon2<50.0)*(Pt_miss>55)*(Pt_jet1>200)*(Pt_jet2>50)*(Pt_ele1<50.0)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5)*(MT_uv>50.0))'
preselectionemu  = '((Pt_muon1>50)*(Pt_muon2>50)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3))'

# Add the filters to the preselections
preselectionemu  += passfilter
preselectionmumu += passfilter
preselectionmunu += passfilter


##########################################################################
########    HARD CODED RESULTS USED IN ANALYSIS                   ########
##########################################################################

# These are hard-coded results for the more grueling studies we don't want to repeat every time. 

# First is the ttbar data-driven e-mu scale factor.
#emu_id_eff = 0.5716
#emu_id_eff_err = 0.00606
emu_id_eff = 1.0
useDataDrivenTTbar = False
if useDataDrivenTTbar:
	#emu_id_eff = 0.598
	emu_id_eff = 0.5748#v7 JEC
#emu_id_eff_err = 0.00305
emu_id_eff_err = 0.0027#v7 JEC

# Next are the PDF uncertainties. 
pdf_MASS   =[ 200, 250, 300 , 350 , 400 , 450 , 500 , 550 , 600 , 650 , 700 , 750 , 800 , 850 , 900 , 950 , 1000 , 1050 , 1100 , 1150 , 1200 , 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000]               
pdf_MASS_displaced = [ 200, 300, 400, 500, 800, 900, 1000, 1100, 1200 ]

pdf_uujj_TTBar = [0,0,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1,4.1]
pdf_uujj_WJets = [0,0,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58,3.58]
pdf_uujj_VV = [3.15,3.15,3.15,3.33,3.63,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15,4.15]
pdf_uujj_ZJets = [0.58,0.58,0.58,1.34,1.93,2.8,4.07,5.96,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62,8.62]
pdf_uujj_sTop = [8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43,8.43]

pdf_uvjj_WJets = [1.06,1.06,1.06,1.46,2.3,3.67,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72]
pdf_uvjj_sTop = [8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78]
pdf_uvjj_TTBar = [2.18,2.18,2.18,3.54,5.16,6.33,7.34,10.01,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36]
pdf_uvjj_ZJets = [2.98,2.98,2.98,3.15,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49]
pdf_uvjj_VV = [3.35,3.35,3.35,3.41,3.62,3.73,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03]

pdf_uvjj_Signal = [0.35,0.35,0.35,0.53,0.83,0.83,0.83,0.83,0.83,0.83,0.83,0.84,1.21,1.21,1.62,1.62,2.22,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35]
pdf_uujj_Signal = [0.1,0.1,0.1,0.17,0.18,0.21,0.26,0.26,0.26,0.27,0.29,0.31,0.35,0.36,0.46,0.65,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06,1.06]
pdf_uujj_Signal = [2.0 for x in pdf_MASS]               
pdf_uvjj_Signal = [3.0 for x in pdf_MASS]               

#new 13tev numbers
pdf_uujj_WJets = [5.83,5.83,5.83,5.83,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42,6.42]
pdf_uujj_Signal = [0.926,0.926,1.271,1.271,1.271,4.341,4.341,4.341,4.341,4.341,4.341,3.58,4.341,4.341,4.341,4.341,4.341,4.341,4.341,4.341,9.07,9.07,9.07,9.07,9.07,9.07,9.07,9.07,9.07,9.07,9.07,9.07,9.07,9.07,9.07,9.07,9.07]
pdf_uujj_ZJets = [0.44,0.44,0.66,0.92,1.16,1.73,1.88,1.99,2.14,2.35,2.64,2.82,3.54,3.74,4.41,4.46,4.85,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15,14.15]
pdf_uujj_TTBar = [32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579,32.579]


#pdf_uujj_WJets = [26.77,26.96,29.39,29.39,29.39,29.39,29.39,29.39,29.39,29.39,29.39,29.39,29.39,29.39,29.39,29.39]
pdf_uujj_Signal = [1.88,2.36,2.36,2.36,2.44,3.81,3.81,3.81,3.81,3.81,3.81,3.81,3.81,3.81,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96,3.96]
pdf_uujj_ZJets = [0.95,0.95,2.11,2.98,5.09,5.8,6.73,7.41,7.41,7.62,7.69,8.11,8.48,11.43,11.43,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11,14.11]



# These are the total background uncertainties. They are used just to make some error bands on plots. 
# totunc_uujj = [3.36, 2.57, 2.79, 3.36, 5.28, 5.67, 6.85, 6.79, 10.29, 10.59, 11.95, 32.6, 14.88, 45.57, 53.55, 53.55, 53.55, 53.55, 53.55 ]
# totunc_uvjj = [7.36, 7.58, 9.62, 10.52, 11.75, 14.42, 18.26, 24.61, 23.88, 38.78, 27.65, 30.1, 47.37, 53.7, 53.99, 53.99, 53.99, 53.99, 53.99]
#old#totunc_uujj = [3.8,3.8,3.8, 3.05, 4.2, 5.31, 6.98, 7.68, 10.44, 14.04, 21.9, 27.56, 27.67, 42.04, 32.78, 55.57, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98, 64.98]
totunc_uvjj = [7.42,7.42,7.42, 7.65, 9.94, 11.06, 12.39, 15.64, 19.79, 27.6, 32.69, 51.06, 50.28, 39.12, 51.71, 58.42, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18, 60.18]



#JECv6#totunc_uujj = [5.95, 5.95, 6.39, 7.71, 10.38, 8.69, 10.52, 10.01, 9.96, 10.13, 10.64, 10.7, 12.05, 12.64, 16.9, 12.79, 20.1, 24.54, 25.32, 26.45, 29.38, 37.44, 34.46, 29.4, 30.79, 35.2, 29.3, 32.44, 25.84, 25.71, 25.51, 25.51, 25.51, 25.51, 25.51, 25.51, 25.51]

#totunc_uujj = [3.19, 4.46, 5.33, 4.58, 5.6, 7.09, 9.84, 9.25, 10.92, 9.68, 16.46, 16.04, 15.71, 20.42, 19.52, 34.73, 25.34, 28.49, 31.98, 62.54, 25.85, 32.57, 31.61, 45.26, 27.38, 32.8, 37.03, 37.03, 37.03, 37.03, 37.03, 37.03, 37.03, 37.03, 37.03, 37.03, 37.03]

#JECv7
totunc_uujj = [3.13, 4.39, 5.28, 4.48, 5.35, 6.73, 9.86, 9.5, 11.75, 10.44, 17.41, 16.75, 15.75, 20.46, 19.52, 34.74, 25.37, 28.51, 31.97, 62.55, 25.86, 32.56, 31.63, 45.3, 27.41, 32.82, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 3.13, 4.39, 5.28, 4.48, 5.35, 6.73, 9.86, 9.5, 11.75, 10.44, 17.41, 16.75, 15.75, 20.46, 19.52, 34.74, 25.37, 28.51, 31.97, 62.55, 25.86, 32.56, 31.63, 45.3, 27.41, 32.82, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05, 37.05]



# Muon alignment Uncs, [uujj sig, uujj bg, uvjj sig, [uvjj bg] ] Only uvjj BG significantly varies with mass
alignmentuncs = [0.1,1.0,1.0,[0.027,0.027,0.027,0.072,0.205,0.672,1.268,2.592,3.632,4.518,6.698,6.355,5.131,9.615,12.364,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176]]

# Shape systematics (from running ShapeSystematics.py) in percent
shapesys_uujj_zjets = 2.99
shapesys_uujj_ttbar = 6.27
shapesys_uvjj_wjets = 4.13
shapesys_uvjj_ttbar = 4.72


#shapesysvar_uujj_zjets = [4.57,4.57,4.57,4.8,7.39,9.18,9.76,10.42,14.54,22.64,36.79,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91,36.91]
shapesysvar_uvjj_wjets = [4.92,4.92,4.92,4.98,7.71,9.07,9.63,12.37,16.22,23.75,41.81,55.82,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55,70.55]


#shapesysvar_uujj_zjets =  [17.14, 16.0, 16.53, 17.01, 16.68, 16.4, 16.34, 16.22, 16.22, 16.25, 16.09, 16.25, 16.57, 16.74, 16.88, 17.3, 17.45, 17.94, 18.16, 18.12, 19.22, 18.91, 19.42, 19.37, 19.56, 19.51, 18.3, 17.77, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24]
#shapesysvar_uujj_wjets =  [24.0, 23.73, 24.28, 24.46, 24.55, 24.32, 25.25, 25.76, 26.19, 25.6, 26.6, 26.98, 28.27, 28.01, 27.78, 27.78, 27.78, 27.78, 27.78, 27.78, 27.78, 27.78, 27.44, 27.44, 28.36, 28.36, 28.36, 28.36, 28.36, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#shapesysvar_uujj_ttjets =  [35.19, 35.24, 36.16, 37.41, 39.09, 40.03, 40.9, 41.67, 42.47, 43.18, 43.87, 44.21, 44.56, 45.91, 47.12, 47.9, 48.52, 49.2, 47.6, 47.23, 47.62, 47.73, 45.32, 43.66, 44.82, 45.28, 44.54, 45.37, 45.37, 45.37, 47.85, 47.85, 47.85, 47.85, 47.85, 47.85, 47.85]

#v7 JEC
#shapesysvar_uujj_zjets =  [1.04, 1.4, 2.27, 3.43, 5.05, 5.96, 6.65, 6.7, 7.09, 7.44, 7.66, 7.64, 8.76, 8.43, 8.48, 8.77, 8.41, 8.32, 8.86, 9.66, 9.66, 10.1, 10.01, 9.99, 9.65, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6]
#shapesysvar_uujj_wjets =  [25.25, 25.12, 22.73, 22.02, 25.2, 26.02, 21.82, 27.85, 32.59, 28.58, 28.37, 28.37, 28.37, 28.37, 28.37, 28.37, 28.37, 28.37, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36, 28.36]
#shapesysvar_uujj_ttjets =  [0.71, 1.29, 2.61, 3.75, 4.68, 5.16, 5.66, 6.64, 6.76, 7.92, 9.5, 10.16, 10.34, 12.14, 13.01, 13.19, 15.11, 16.32, 15.21, 15.21, 14.51, 14.51, 15.12, 16.89, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24]

shapesysvar_uujj_zjets = [0.9615743327776682,1.56163540234714,2.3365782899091405,3.4209690609168204,5.154155464600462,5.911262221864894,6.570105158566167,6.703568067746186,7.104024672180886,7.687825148341801,7.713262965634159,7.73479094813844,8.95051930009977,8.630201339967677,8.703291928072183,8.14053185339924,8.390623615695011,8.385949832848613,8.844345435953441,9.599576307358504,9.600693126824625,10.031218398625724,9.948658347208864,9.586417947814706,9.586417947814706,10.533128304233378,10.717359116935159,10.717359116935159,10.717359116935159,10.717359116935159,10.717359116935159,10.717359116935159,10.717359116935159,10.717359116935159,10.717359116935159,10.717359116935159,10.717359116935159]
shapesysvar_uujj_wjets = [25.252645416344947,25.074011794921,22.733059765099586,23.212760761303635,25.05643328342816,25.835297646866724,26.825191558218,27.850334202063763,32.58849615133643,28.57988606386589,28.36512298790254,28.36512298790254,28.36512298790254,28.36512298790254,28.36512298790254,28.36512298790254,28.36512298790254,28.36512298790254,28.36512298790254,28.36512298790254,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829,28.36526434530829]
shapesysvar_uujj_ttjets = [0.6635227788798514,1.459799890556999,2.609970717472059,3.6478841350141114,4.598398021274462,5.182098696437037,5.897514193942096,6.603035122911292,6.523556319073647,7.870382431591672,8.744373761415329,9.457336370842532,10.033088322305407,11.856850696410762,11.943863407430188,12.509110426649203,13.405037892205005,13.740921331139608,15.124498734333585,12.883657347545704,12.186173685169654,12.183608615583474,11.962738559614735,12.05870097191865,12.924739727863118,12.924739727863118,12.924739727863118,12.924739727863118,12.924739727863118,12.924739727863118,12.924739727863118,12.924739727863118,12.924739727863118,12.924739727863118,12.924739727863118,12.924739727863118,12.924739727863118]

shapesysvar_uvjj_zjets =  [15.52, 15.87, 17.23, 18.13, 18.56, 18.75, 19.17, 19.52, 20.8, 21.59, 20.22, 19.03, 17.67, 16.22, 17.5, 17.41, 17.22, 16.53, 14.67, 14.66, 16.1, 15.61, 15.61, 19.67, 19.67, 19.67, 19.67, 19.67, 19.67, 19.67, 19.67, 19.67, 19.67, 19.67, 19.67, 19.67, 19.67]
shapesysvar_uvjj_wjets =  [13.36, 14.0, 15.87, 16.82, 16.65, 16.48, 16.53, 15.85, 16.06, 15.83, 18.46, 17.84, 16.93, 16.11, 15.63, 14.79, 14.62, 15.83, 15.95, 16.35, 16.53, 16.84, 17.24, 16.27, 15.12, 27.12, 27.12, 26.89, 26.91, 26.91, 26.88, 26.88, 26.88, 26.88, 26.88, 26.88, 26.88]
shapesysvar_uvjj_ttjets =  [34.43, 34.7, 35.84, 36.87, 38.38, 38.97, 39.35, 39.77, 40.17, 39.91, 40.12, 40.14, 39.99, 39.44, 39.08, 38.48, 38.78, 38.77, 38.66, 38.41, 39.45, 40.36, 40.36, 35.31, 35.31, 35.31, 34.51, 35.51, 34.96, 34.96, 34.96, 34.96, 34.96, 34.96, 34.96, 34.96, 34.96]
  

############################################################
#####  The binning (const or variable) used for plots ######
############################################################

ptbinning = [10,15]#was [40,60], changed because pt cut is now 50
ptbinning2 = [10,15]
metbinning2 = [0,5]

stbinning = [200,225]#was [250,275]
bosonbinning = [50,60,70,80,90,100,110,120]
bosonzoombinning_uujj_Z = [40,20,140]#fixme was [30,50,140]
bosonzoombinning_uujj_TT = [95,100]
metzoombinning_uujj_TT = [95,100]
metzoombinning_uujj_Z = [0,5,10,15,22,30,40,55,75,100]
	
bosonzoombinning_uvjj = [50,65,115]
bosonslopebinning_uvjj = [40,70,270]
massslopebining_uvjj = [25,100,600]

lqbinning = [50,60]
etabinning = [26,-2.6,2.6]
costhetastarbinning = [84,-1.05,1.05]
drbinning = [70,0,7]
phibinning = [26,-3.1416,3.1416]
phi0binning = [13,0,3.1416]
dphibinning = [64,0,3.2]

for x in range(40):
	if ptbinning[-1] < 1500:
       		ptbinning.append(ptbinning[-1]+(ptbinning[-1] - ptbinning[-2])*1.2)
       	if ptbinning2[-1] < 700:
       		ptbinning2.append(ptbinning2[-1]+(ptbinning2[-1] - ptbinning2[-2])*1.2)
       	if metbinning2[-1] < 700:
       		metbinning2.append(metbinning2[-1]+(metbinning2[-1] - metbinning2[-2])*1.2)		
       	if stbinning[-1] < 3200:
       		stbinning.append(stbinning[-1]+(stbinning[-1] - stbinning[-2])*1.2)
       	if bosonbinning[-1]<1000:
       		bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.2 )
       	if lqbinning[-1]<2000:
       		lqbinning.append(lqbinning[-1]+(lqbinning[-1] - lqbinning[-2])*1.1)
       	if bosonzoombinning_uujj_TT[-1] < 900:
       		bosonzoombinning_uujj_TT.append(bosonzoombinning_uujj_TT[-1] + (bosonzoombinning_uujj_TT[-1] - bosonzoombinning_uujj_TT[-2])*1.25)	       	
	if metzoombinning_uujj_TT[-1] < 900:
	       	metzoombinning_uujj_TT.append(metzoombinning_uujj_TT[-1] + (metzoombinning_uujj_TT[-1] - metzoombinning_uujj_TT[-2])*1.4)		
vbinning = [50,0,50]
nbinning = [10,0,10]
njetbinning = [8,2,10]
ptbinning = [round(x) for x in ptbinning]
ptbinning2 = [round(x) for x in ptbinning2]
metbinning2 = [round(x) for x in metbinning2]
stbinning = [round(x) for x in stbinning]
bosonbinning = [round(x) for x in bosonbinning]
lqbinning = [round(x) for x in lqbinning]




##########################################################################
########    THE MAIN FUNCTION THAT DEFINES WHAT STUDIES TO DO     ########
##########################################################################



def main():


	#######################################################################################
    ######  The output directories, and the files that define final selection cuts  #######
	#######################################################################################

	# Please retain the "script flag" comment. Some python scripts are available which search
	# for this, and make use of it. e.g. For systematic variations, we can in batch instead
	# of running serially, which speeds things up.


	version_name = 'Testing_diHiggs' # scriptflag
	os.system('mkdir Results_'+version_name) 

	MuMuOptCutFile = 'Results_'+version_name+'/OptHH_resCuts_Smoothed_pol2cutoff.txt' # scriptflag
	MuNuOptCutFile = 'Results_'+version_name+'/OptLQ_uvjjCuts_Smoothed_pol2cutoff.txt' # scriptflag


	############################################################
    #####  The binning (const or variable) used for plots ######
	############################################################

#
#	ptbinning = [40,60]
#	ptbinning2 = [40,60]
#	metbinning2 = [0,5]
#
#	stbinning = [250,275]
#	bosonbinning = [50,60,70,80,90,100,110,120]
#	bosonzoombinning_uujj_Z = [30,50,140]
#	bosonzoombinning_uujj_TT = [95,100]
#	metzoombinning_uujj_TT = [95,100]
#	metzoombinning_uujj_Z = [0,5,10,15,22,30,40,55,75,100]
#
#	bosonzoombinning_uvjj = [50,65,115]
#	bosonslopebinning_uvjj = [40,70,270]
#	massslopebining_uvjj = [25,100,600]
#
#	lqbinning = [50,60]
#	etabinning = [26,-2.6,2.6]
#	drbinning = [70,0,7]
#	phibinning = [26,-3.1416,3.1416]
#	dphibinning = [64,0,3.2]
#
#	for x in range(40):
#		if ptbinning[-1] < 1500:
#			ptbinning.append(ptbinning[-1]+(ptbinning[-1] - ptbinning[-2])*1.2)
#		if ptbinning2[-1] < 700:
#			ptbinning2.append(ptbinning2[-1]+(ptbinning2[-1] - ptbinning2[-2])*1.2)
#		if metbinning2[-1] < 700:
#			metbinning2.append(metbinning2[-1]+(metbinning2[-1] - metbinning2[-2])*1.2)		
#		if stbinning[-1] < 3200:
#			stbinning.append(stbinning[-1]+(stbinning[-1] - stbinning[-2])*1.2)
#		if bosonbinning[-1]<1000:
#			bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.2 )
#		if lqbinning[-1]<2000:
#			lqbinning.append(lqbinning[-1]+(lqbinning[-1] - lqbinning[-2])*1.1)
#		if bosonzoombinning_uujj_TT[-1] < 900:
#			bosonzoombinning_uujj_TT.append(bosonzoombinning_uujj_TT[-1] + (bosonzoombinning_uujj_TT[-1] - bosonzoombinning_uujj_TT[-2])*1.25)			
#		if metzoombinning_uujj_TT[-1] < 900:
#			metzoombinning_uujj_TT.append(metzoombinning_uujj_TT[-1] + (metzoombinning_uujj_TT[-1] - metzoombinning_uujj_TT[-2])*1.4)		
#
#	vbinning = [60,0,60]
#	nbinning = [10,0,10]
#
#	ptbinning = [round(x) for x in ptbinning]
#	ptbinning2 = [round(x) for x in ptbinning2]
#	metbinning2 = [round(x) for x in metbinning2]
#	stbinning = [round(x) for x in stbinning]
#	bosonbinning = [round(x) for x in bosonbinning]
#	lqbinning = [round(x) for x in lqbinning]


	#################################################################################
    ##############     A FEW STANDARD PLOTTING ROUTINES AND STUDIES   ###############
	#################################################################################

	# ====================================================================================================================================================== #
	# These are PDF uncertainty studies.
	# ====================================================================================================================================================== #

	if False:
		PDF4LHCUncStudy(MuMuOptCutFile,MuNuOptCutFile,version_name)
		#PDF4LHCUncStudy('Results_Testing_Feb21/OptLQ_uujjCuts_Smoothed_pol2cutoff_forPDFStudy.txt',MuNuOptCutFile,version_name)
		PDF4LHCPlotsFromResultDict('Results_'+version_name+'/PDFVariationsDictionary.json',version_name)


	# ====================================================================================================================================================== #
	# The ttbar e-mu data-driven study. You only need to do this once, check the validation output, and use the scale-factor as global variable "emu_id_eff"
	# The scale-factor should be near 0.5
	# ====================================================================================================================================================== #
	if False:
		# TTBar STudy

		# Some modifications to the ST and LQ mass binning
		bosonbinning = [50,60,70,80,90,100,110,120]
		for x in range(40):
			if bosonbinning[-1]<1000:
				bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.2 )
		bosonbinning = [round(x) for x in bosonbinning]
		stbinning = [280 ,300]
		lqbinning = [-20,0]
		for x in range(27):#was 22
			stbinning.append(stbinning[-1]+10+stbinning[-1]-stbinning[-2])
		for x in range(15):#was 22
			if x<9: lqbinning.append(lqbinning[-1]+5+lqbinning[-1]-lqbinning[-2])
			else:   lqbinning.append(lqbinning[-1]+20+lqbinning[-1]-lqbinning[-2])
		stbinning = stbinning[1:]
		lqbinning = lqbinning[1:]
		stbinning = [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1075, 1200, 1350, 1500, 1650, 1800, 1980, 2170, 2370, 2580, 2800, 3000]#added 3500	


		[Rtt_uujj,Rtt_uujj_err] = GetEMuScaleFactors( NormalWeightEMu+'*'+preselectionemu, EMuDirectory)
		Rw_uvjj,Rz_uujj = [1.0,1.0]
		# # PreSelection Plots
		MakeBasicPlotEMu("St_uujj","S_{T}^{e#mujj} [GeV]",stbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuseltagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("Pt_miss","E_{T}^{miss} [GeV]",metbinning2,preselectionemu,NormalWeightEMu,EMuDirectory,'emuseltagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("M_uu","M^{e #mu} [GeV]",bosonbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuseltagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("M_uujj2","M^{e/#muj}_{2} [GeV]",lqbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuseltagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("DR_muon1muon2","#DeltaR(#mu,e})",drbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuseltagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuseltagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuseltagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("JetCount","N_{jet}",nbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuseltagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)

		MakeBasicPlotEMu("St_uujj","S_{T}^{e#mujj} [GeV]",stbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuselPAStagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("Pt_miss","E_{T}^{miss} [GeV]",metbinning2,preselectionemu,NormalWeightEMu,EMuDirectory,'emuselPAStagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("M_uu","M^{e #mu} [GeV]",bosonbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuselPAStagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("M_uujj2","M^{e/#muj}_{2} [GeV]",lqbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuselPAStagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlotEMu("DR_muon1muon2","#DeltaR(#mu,e})",drbinning,preselectionemu,NormalWeightEMu,EMuDirectory,'emuselPAStagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)


	# ====================================================================================================================================================== #
	# This is the QCD study. It will make a couple plots, and test QCD contamination at final selection. We consider QCD negligible, but is good to test this once!
	# ====================================================================================================================================================== #
	if False :
		qcdselectionmumu = '((Pt_muon1>50)*(Pt_muon2>50)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(DR_muon1muon2>0.3))'
		qcdselectionmunu = '((Pt_muon1>50)*(Pt_muon2<50)*(Pt_jet1>50)*(Pt_jet2>50)*(Pt_ele1<50)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5))'

		QCDStudy(qcdselectionmumu,qcdselectionmunu,MuMuOptCutFile,MuNuOptCutFile,NormalWeightMuMu,NormalWeightMuNu,version_name)


	# ====================================================================================================================================================== #
	# This is a testing plot routine for use with the new Displaced SUSY (l+b) samples
        # Following samples are still missing: 
	# ====================================================================================================================================================== #
	if False :

		# Some modifications to the ST and LQ mass binning
		bjetbinning = [0,.05]
		for x in range(20):
			bjetbinning.append(bjetbinning[-1]+.05)
		stbinning = [280 ,300]
		lqbinning = [-20,0]
		for x in range(27):#was 22
			stbinning.append(stbinning[-1]+10+stbinning[-1]-stbinning[-2])
		for x in range(28):#was 22
			lqbinning.append(lqbinning[-1]+5+lqbinning[-1]-lqbinning[-2])
		stbinning = stbinning[1:]
		lqbinning = lqbinning[1:]
		##bosonbinning = [50, 70, 105, 150,200,300,425, 600, 750, 900, 1105, 1330, 1575, 1840, 2125, 2430, 2590]
		##lqbinning = [50, 75, 105, 175, 280, 405, 550, 715, 900, 1105, 1330, 1575, 1840, 2125, 2430, 2590]
		#stbinning = [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000, 3500]#added 3500	
		##stbinning = [250,300,350,400,450,500,550,600,650,710, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000, 3500]#coarser binning for now	

		bosonbinning = [50,60,70,80,90,100,110,120]
		for x in range(40):
			if bosonbinning[-1]<1000:
				bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.2 )	       	
		bosonbinning = [round(x) for x in bosonbinning]

		MakeEfficiencyPlot(NormalDirectory,NormalWeightMuMu,'Results_'+version_name+'/OptBLCTau1_uujjCuts_Smoothed_pol2cutoff.txt','BL',version_name)

		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1)
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))<1)', '(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))>=1)')#fixme todo varying control sample MT window
		

		# UUJJ plots at preselection, Note that putting 'TTBarDataDriven' in the name turns on the use of data-driven ttbar e-mu sample in place of MC
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[60,0,600],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		#MakeBasicPlot("M_jj","M^{jj} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)

		# Full Selection Plots
		for lqmass in [200,300,400,500,600,700,800,900,1000]:
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
                        MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("CISV_jet1","Jet1 CSV score",bjetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("CISV_jet2","Jet2 CSV score",bjetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuMuOptCutFile,version_name,lqmass)

	# ====================================================================================================================================================== #
	# This is a testing plot routine for use with the new RPV susy samples
	# ====================================================================================================================================================== #
	if False :

		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1)
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
		
		# UUJJ plots at preselection, Note that putting 'TTBarDataDriven' in the name turns on the use of data-driven ttbar e-mu sample in place of MC
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[60,0,600],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MH_uujj","M_{#muj} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon2jet1","#DeltaR(#mu_{2},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon2jet2","#DeltaR(#mu_{2},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_jet1met","#Delta#phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_jet2met","#Delta#phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1jet1","#Delta#phi(#mu_{1},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1jet2","#Delta#phi(#mu_{1},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon2jet1","#Delta#phi(#mu_{2},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon2jet2","#Delta#phi(#mu_{2},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)


	# ====================================================================================================================================================== #
	# This is a basic plotting routine to make Analysis Note style plots with ratio plots. AN Analysis-Note
	# ====================================================================================================================================================== #
	if True :
		global preselectionmumu 
		# Some modifications to the ST and LQ mass binning
		bjetbinning = [-1.2,-1.01]
		for x in range(24):
			bjetbinning.append(bjetbinning[-1]+.1)
		#stbinning = [280 ,300]
		stbinning = [0,5]
		lqbinning = [-20,0]
		#for x in range(27):#was 22
		while stbinning[-1]<4500:#was 22
			#stbinning.append(stbinning[-1]+10+stbinning[-1]-stbinning[-2])
			stbinning.append(stbinning[-1]+5+stbinning[-1]-stbinning[-2])
		for x in range(28):#was 22
			lqbinning.append(lqbinning[-1]+5+lqbinning[-1]-lqbinning[-2])
		stbinning = stbinning[1:]
		lqbinning = lqbinning[1:]
		##bosonbinning = [50, 70, 105, 150,200,300,425, 600, 750, 900, 1105, 1330, 1575, 1840, 2125, 2430, 2590]
		##lqbinning = [50, 75, 105, 175, 280, 405, 550, 715, 900, 1105, 1330, 1575, 1840, 2125, 2430, 2590]
		#stbinning = [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000, 3500]#added 3500	
		##stbinning = [250,300,350,400,450,500,550,600,650,710, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000, 3500]#coarser binning for now	

		bosonbinning = [0,10,20,30,40,50,60,70,80,90,100,110,120]
		for x in range(40):
			if bosonbinning[-1]<1000:
				bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.2 )	       	
		bosonbinning = [round(x) for x in bosonbinning]

		binning2D = [0,12]
		for x in range(100):
			if binning2D[-1]<650:
				binning2D.append(binning2D[-1]+12)	       	
		binning2D = [round(x) for x in binning2D]

		MassMinusbinning = [-120]
		for x in range(200):
			if MassMinusbinning[-1]<650:
				MassMinusbinning.append(MassMinusbinning[-1]+10)	       	
		MassMinusbinning = [round(x) for x in MassMinusbinning]


		#print lqbinning,stbinning
		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)*(((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)', '(M_uu>100)*(Pt_miss>100)',0)
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))<1)', '(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))>=1)')#fixme todo varying control sample MT window
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
		#[[Rz_uujj,Rz_uujj_err]]=[[1.,0.]]
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]]=[[1.,0.],[1.,0,]]
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]]=[[1.,0.],[1.,0,]]
		#CSVv2L	0.460
		#CSVv2M	0.8
		#CSVv2T	0.935

		#preselectionmumu = preselectionmumu+'*(Charge_muon1<0)*(Charge_muon2<0)'#FIXME checking same sign

		# Optionally, you can make an event-count table for each selection. Useful if testing a new optimization
		# We will do this later wtih full systematics for our set of stable cuts. 
		if False:
			QuickTableTTDD(MuMuOptCutFile, preselectionmumu+"*(M_uu>100)",NormalWeightMuMu,Rz_uujj, Rw_uvjj,Rtt_uujj,0)#Use data-driven TTbar
			#QuickTable(MuMuOptCutFile, preselectionmumu+"*(M_uu>100)",NormalWeightMuMu,Rz_uujj, Rw_uvjj,Rtt_uujj,0)#Use MC-driven TTbar
			#QuickTable(MuNuOptCutFile, preselectionmunu,NormalWeightMuNu,Rz_uujj, Rw_uvjj,Rtt_uvjj,0)

		#MakeBasicPlot("sqrt(abs(2*Pt_jet1*Pt_jet2*(cosh(Eta_jet1-Eta_jet2) - (((Phi_jet1-Phi_jet2)<-1*pi)*cos(Phi_jet1-Phi_jet2+2*pi)) - (((Phi_jet1-Phi_jet2)>-1*pi)*((Phi_jet1-Phi_jet2)<1*pi)*cos(Phi_jet1-Phi_jet2)) - (((Phi_jet1-Phi_jet2)> 1*pi)*cos(Phi_jet1-Phi_jet2-2*pi)) )))","M_{jj} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)

                #Signal efficiency*acceptance at final selection
		#MuMuOptCutFile = 'Results_Testing_Feb21_tmp/OptLQ_uujjCuts_Smoothed_pol2cutoff.txt'
		#MakeEfficiencyPlot(NormalDirectory,NormalWeightMuMu,MuMuOptCutFile,'LQuujj',version_name)
		

		# Here are a few plots which are zoomed-in on control regions. 
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonzoombinning_uujj_Z,preselectionmumu,NormalWeightMuMu,NormalDirectory,'controlzoom_ZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metzoombinning_uujj_Z,preselectionmumu+'*(M_uu>80)*(M_uu<100)*(Pt_miss<100)',NormalWeightMuMu,NormalDirectory,'controlzoomZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonzoombinning_uujj_TT,preselectionmumu+'*(M_uu>100)*(Pt_miss>=100)',NormalWeightMuMu,NormalDirectory,'controlzoom_TTRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metzoombinning_uujj_TT,preselectionmumu+'*(M_uu>100)*(Pt_miss>=100)',NormalWeightMuMu,NormalDirectory,'controlzoomTTRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)

		#Here are some 2D plots
		"""
		MakeBasicPlot2D("M_uu","Mjj_Z","M_{uu} [GeV]","M_{(Z)jj} [GeV]",binning2D,binning2D,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot2D("M_uu","Mjj_Z","M_{uu} [GeV]","M_{(Z)jj} [GeV]",binning2D,binning2D,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,900)
		MakeBasicPlot2D("Mbb_H","Mjj_Z","M_{(H)bb} [GeV]","M_{(Z)jj} [GeV]",binning2D,binning2D,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot2D("Mbb_H","Mjj_Z","M_{(H)bb} [GeV]","M_{(Z)jj} [GeV]",binning2D,binning2D,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,900)
		MakeBasicPlot2D("Mbb_H-125","Mjj_Z-91","M_{bb}-125 [GeV]","M_{jj}-91 [GeV]",MassMinusbinning,MassMinusbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot2D("Mbb_H-125","Mjj_Z-91","M_{bb}-125 [GeV]","M_{jj}-91 [GeV]",MassMinusbinning,MassMinusbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,900)
		MakeBasicPlot2D("abs(cosThetaStarMu)","M_uu4j","|cos(#Theta*)|","M_{uu4j} [GeV]",costhetastarbinning,lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot2D("abs(cosThetaStarMu)","M_uu4j","|cos(#Theta*)|","M_{uu4j} [GeV]",costhetastarbinning,lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,900)
		"""

		#bosonzoombinning_uvjj = [20,70,110]
		bosonzoombinning_uvjj = [50,50,150]#fixme todo changed from [20,70,110]
		##MakeBasicPlot("CISV_jet1","Jet1 CSV score",bjetbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)#fixme todo turning off all munujj plots for now
		##MakeBasicPlot("CISV_jet2","Jet2 CSV score",bjetbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		##MakeBasicPlot("CISV_jet1","Jet1 CSV score",bjetbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		##MakeBasicPlot("CISV_jet2","Jet2 CSV score",bjetbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		##MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))<1)',NormalWeightMuNu,NormalDirectory,'controlzoom_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		##MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))>=1)',NormalWeightMuNu,NormalDirectory,'controlzoom_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		#MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>50)*(MT_uv<130)*(JetCount<3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)#fixme todo changed 70-110 to 60-120
		#MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>50)*(MT_uv<130)*(JetCount>4.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)#fixme todo changed ttbar from 3.5 to 4.5 and 70-110 to 60-120
		##MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonslopebinning_uvjj, preselectionmunu,NormalWeightMuNu,NormalDirectory,'controlzoom_SlopeRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		##MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",massslopebining_uvjj,preselectionmunu,NormalWeightMuNu,NormalDirectory,'controlzoom_SlopeRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)

		
		# UUJJ plots at preselection, Note that putting 'TTBarDataDriven' in the name turns on the use of data-driven ttbar e-mu sample in place of MC

		MakeBasicPlot("cosTheta_hbb","cos(#Theta) (H->bb)",costhetastarbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("cosTheta_zuu_hzz","cos(#Theta) (Z->uu, H->ZZ)",costhetastarbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("cosThetaStarMu","cos(#Theta*)",costhetastarbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("phi0","#phi0",phi0binning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("phi0_zz","#phi0_zz",phi0binning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("phi1","#phi1",phi0binning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("phi1_zuu","#phi1_zuu",phi0binning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("phi1_zjj","#phi1_zjj",phi0binning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("CMVA_bjet1","Jet1(H->bb) CMVA score",bjetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("CMVA_bjet2","Jet2(H->bb) MVA score",bjetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		#MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Hjet1","p_{T}(bjet_{1}) (H) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Hjet2","p_{T}(bjet_{2}) (H) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Zjet1","p_{T}(jet_{1}) (Z) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Zjet2","p_{T}(jet_{2}) (Z) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Hjets","p_{T}(bb) (H) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Zjets","p_{T}(jj) (Z) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_uu","p_{T}(#mu#mu) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[60,0,600],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)	
		#MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)	
		MakeBasicPlot("M_uu4j-Mbb_H+125","M_{X} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("M_uu4j-Mbb_H+125-M_uujj+125","M_{X2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("M_jj","M_{jj} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("M_ee","M^{ee} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Mbb_H","M^{bb} from H [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Mbb_H-125","(M^{bb}-125) from H [GeV]",MassMinusbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Mjj_Z","M^{jj} from Z [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Mjj_Z-91","(M^{jj-91)} from Z [GeV]",MassMinusbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("MH_uujj","M_{#muj} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("M_uujjavg","M_{#muj}_{avg} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("M_uujj","M_{#mu#mujj} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("M_uu4j","M_{#mu#mu4j} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("JetCount","N_{jet}",njetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)#removing TTBarDataDriven cause this makes weird muon count comparison
		MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)#removing TTBarDataDriven cause this makes weird muon count comparison
		MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_u1Hj1","#DeltaR(#mu_{1},Hj_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_u1Hj2","#DeltaR(#mu_{1},Hj_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_u2Hj1","#DeltaR(#mu_{2},Hj_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_u2Hj2","#DeltaR(#mu_{2},Hj_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_u1Zj1","#DeltaR(#mu_{1},Zj_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_u1Zj2","#DeltaR(#mu_{1},Zj_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_u2Zj1","#DeltaR(#mu_{2},Zj_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_u2Zj2","#DeltaR(#mu_{2},Zj_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("DR_muon2jet1","#DeltaR(#mu_{2},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("DR_muon2jet2","#DeltaR(#mu_{2},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_jj_Z","#DeltaR(j_{1},j_{2}) (Z)",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_bb_H","#DeltaR(b_{1},b_{2}) (H)",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_uu_bb_H","#DeltaR(#mu#mu,bb(H))",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_uu_jj_Z","#DeltaR(#mu#mu,jj(Z))",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("minDR_muonjet","#DeltaR_{min}(#mu,j)",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_jet1met","#Delta#phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("DPhi_jet2met","#Delta#phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("DPhi_muon1jet1","#Delta#phi(#mu_{1},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("DPhi_muon1jet2","#Delta#phi(#mu_{1},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("DPhi_muon2jet1","#Delta#phi(#mu_{2},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("DPhi_muon2jet2","#Delta#phi(#mu_{2},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_uu_jj_Z","#Delta#phi(#mu#mu,jj(Z))",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_uu_bb_H","#Delta#phi(#mu#mu,bb(H))",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_bb_H","#Delta#phi(bb) (H)",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_jj_Z","#Delta#phi(jj) (Z)",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		# UVJJ plots at preselection, 
		#fixme todo turning off all munujj plots for now
		"""
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("Phi_miss","#phi^{miss} [GeV]",[100,-3.1416,3.1416],preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("St_uvjj","S_{T}^{#mu#nujj} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("MT_uvjj","M_{T}^{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("MH_uvjj","M_{#muj} (lead jet only) [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("DPhi_muon1met","#Delta#phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("DPhi_jet1met","#Delta#phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("DPhi_jet2met","#Delta#phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu,j_{1})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,300)
		MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu,j_{2})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		"""
		
		#fixme turning off final selection
		# Full Selection Plots
		#for lqmass in [200,250,300,500,550,600,650,800]:
		for lqmass in [300,900]:
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','HHres',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','HHres',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_uu","M^{#mu#mu} [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','HHres',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uu4j","M_{#mu@mu4j} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','HHres',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			##MakeBasicPlot("St_uvjj","S_{T}^{#mu#nujj} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)#fixme todo turning off all munujj plots for now
			##MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			##MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)

			MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','HHres',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("CISV_jet1","Jet1 CSV score",bjetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','HHres',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("CISV_jet2","Jet2 CSV score",bjetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'final','HHres',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuMuOptCutFile,version_name,lqmass)
		

		#fixme todo removing this, its not helpful at the moment
		#os.system('echo Combining Figures; convert -density 800 Results_'+version_name+'/*png Results_'+version_name+'/AllPlots.pdf')



	# ====================================================================================================================================================== #
	# This is a plotting routine for PAS-style publication-quality plots
	# ====================================================================================================================================================== #

	if False:

		# Some modifications to the ST and LQ mass binning
		stbinning = [280 ,300]
		lqbinning = [-20,0]
		for x in range(27):#was 22
			stbinning.append(stbinning[-1]+10+stbinning[-1]-stbinning[-2])
		for x in range(28):#was 22
			lqbinning.append(lqbinning[-1]+5+lqbinning[-1]-lqbinning[-2])
		stbinning = stbinning[1:]
		lqbinning = lqbinning[1:]
		#stbinning = [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000, 3500]

		bosonbinning = [50,60,70,80,90,100,110,120]
		for x in range(40):
			if bosonbinning[-1]<1000:
				bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.2 )	       	
		bosonbinning = [round(x) for x in bosonbinning]


		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1)
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))<1)', '(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))>=1)')#fixme todo varying control sample MT window
		

		# Here are a few plots which are zoomed-in on control regions. 
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",[20,80,100],preselectionmumu,NormalWeightMuMu,NormalDirectory,'controlzoomPASTTBarDataDriven_ZRegiontagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonzoombinning_uujj_Z,preselectionmumu,NormalWeightMuMu,NormalDirectory,'controlzoomPAS_ZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		bosonzoombinning_uvjj = [20,70,110]
		MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))<1)',NormalWeightMuNu,NormalDirectory,'controlzoomPAS_WRegiontagfree','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))>=1)',NormalWeightMuNu,NormalDirectory,'controlzoomPAS_TTRegiontagfree','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		# The two flags are for regular plots, and tagfree plots (plots that don't say CMS Preliminary - for notes or thesis)
		for flag in ['','tagfree']:

			# Preselection plots in the UUJJ channel in the PAS style (no subplot)
			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("MH_uujj","M_{#muj} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uujj2","M_{#muj}^{min} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			#fixme todo added version with MC based ttbar background
			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("MH_uujj","M_{#muj} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uujj2","M_{#muj}^{min} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)

			# Preselection plots in the UVJJ channel in the PAS style (no subplot)
			#fixme removing all uvjj plots for now
			"""
			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("St_uvjj","S_{T}^{#mu#nujj} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("MT_uvjj","M_{T}^{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("MH_uvjj","M_{#muj} (lead jet only) [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			"""
			# Full Selection Plots in the PAS style
			for lqmass in [200,250,300,500,550,600,650,800]:
			#for lqmass in [500,900]:
				MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDrivenPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDrivenPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uujj2","M_{#muj}^{min} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDrivenPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			        #fixme todo added version with MC based ttbar background
				MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uujj2","M_{#muj}^{min} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
				#
			        #fixme removing all uvjj plots for now
				"""
				MakeBasicPlot("St_uvjj","S_{T}^{#mu#nujj} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
				MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
				"""


	# ====================================================================================================================================================== #
	# This runs a "FullAnalysis" - i.e. produces tables with full systematis included. 
	# ====================================================================================================================================================== #

	# You can run this to make the full set of tables needed to construct the higgs card. This takes a long time!
	# Alternatively, you can run > python SysBatcher.py --launch to do each table in a separate batch job
	# When done, proceed to the next step to make higgs limit cards
	if False : 
		FullAnalysis(MuMuOptCutFile, preselectionmumu,preselectionmunu,NormalDirectory,NormalWeightMuMu,'TTBarDataDriven')  # scriptflag
		#FullAnalysis(MuNuOptCutFile, preselectionmumu,preselectionmunu,NormalDirectory,NormalWeightMuNu,'normal')  # scriptflag

	if False :
		uujjcardfiles = MuMuOptCutFile.replace('.txt','_systable*.txt')
		uvjjcardfiles = MuNuOptCutFile.replace('.txt','_systable*.txt')

		uujjcards = ParseFinalCards(uujjcardfiles)
		#uvjjcards = ParseFinalCards(uvjjcardfiles)#fixme using uujj for now for speed
		uvjjcards = ParseFinalCards(uujjcardfiles)#fixme using uujj for now for speed
		finalcards = FixFinalCards([uujjcards,uvjjcards])

		print 'Final Cards Available in',finalcards




	# ====================================================================================================================================================== #
	# These are some plots with the systematic variations turned on. They are just sanity checks and not part of any normal procedure
	# ====================================================================================================================================================== #
	if False :

		for sample in ['ScaleUp','ScaleDown','MatchUp','MatchDown']:
			preselectionmunu_mod = preselectionmunu
			NormalWeightMuNu_mod = NormalWeightMuNu
			Rz_uujj = 1.0
			[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactorsMod( NormalWeightMuNu_mod+'*'+preselectionmunu_mod, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)',sample)
			MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2}) "+sample,drbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sysmethod in ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','PUup','PUdown']:
			preselectionmunu_mod = ModSelection(preselectionmunu,sysmethod,MuNuOptCutFile)
			NormalWeightMuNu_mod = ModSelection(NormalWeightMuNu,sysmethod,MuNuOptCutFile)

			Rz_uujj = 1.0
			[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu_mod+'*'+preselectionmunu_mod, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
			MakeBasicPlot(ModSelection("M_uvjj",sysmethod,MuNuOptCutFile),"M_{#muj} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sysmethod,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot(ModSelection("MT_uv",sysmethod,MuNuOptCutFile),"M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sysmethod,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sample in ['ScaleUp','ScaleDown','MatchUp','MatchDown']:
			Rw_uvjj = 1.0
			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactorsMod( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',sample)
			# MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			# MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV] "+sample,ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardTTBarDataDriven_sys'+sample,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV] "+sample,ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardTTBarDataDriven_sys'+sample,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			rescale_string = MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)',NormalWeightMuNu,NormalDirectory,'standard_rescaletest_pre','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sysmethod in ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','PUup','PUdown']:
			preselectionmumu_mod = ModSelection(preselectionmumu,sysmethod,MuMuOptCutFile)
			NormalWeightMuMu_mod = ModSelection(NormalWeightMuMu,sysmethod,MuMuOptCutFile)

			Rw_uvjj = 1.0

			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu_mod+'*'+preselectionmumu_mod, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1)

			MakeBasicPlot(ModSelection("Pt_jet1",sysmethod,MuMuOptCutFile),"p_{T}(jet_{1}) [GeV] "+sysmethod,ptbinning,preselectionmumu_mod,NormalWeightMuMu_mod,NormalDirectory,'standard_sys'+sysmethod,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot(ModSelection("Pt_jet2",sysmethod,MuMuOptCutFile),"p_{T}(jet_{2}) [GeV] "+sysmethod,ptbinning,preselectionmumu_mod,NormalWeightMuMu_mod,NormalDirectory,'standard_sys'+sysmethod,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)



	# ====================================================================================================================================================== #
	# This is for Optimization of cuts
	# ====================================================================================================================================================== #

	if False :
		doLongLived = False
		# Get Scale Factors
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0)
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))<1)', '(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))>=1)')#fixme todo varying control sample MT window
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]]=[[1.,0.],[1.,0,]]
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]]=[[1.,0.],[1.,0,]]
		scaleFactors = [Rz_uujj,Rtt_uujj,Rw_uvjj]
		if not doLongLived :
			MuMuOptTestCutFile = 'Results_'+version_name+'/OptLQ_uujjCuts_Smoothed_pol2cutoff.txt'
	          	#variableSpace = ['Pt_jet1:10:0:1000']
			variableSpace = ['Pt_uu:50:0:1000','St_uujj:50:0:4000','M_uu4j:50:100:2500',]
			OptimizeCuts3D(variableSpace,preselectionmumu,NormalWeightMuMu,version_name,scaleFactors,'','uujj')
			#scaleFactors = [Rz_uujj,Rtt_uvjj,Rw_uvjj]
			#variableSpace = ['MT_uv:25:120:1200','St_uvjj:25:300:2000','M_uvjj:25:100:1000',]
		        #OptimizeCuts3D(variableSpace,preselectionmunu,NormalWeightMuNu,version_name,scaleFactors,'','uvjj')#FIXME turned off uvjj for now
		#Now we can do it for long-lived samples
		if doLongLived :
			scaleFactors = [Rz_uujj,Rtt_uujj,Rw_uvjj]
		        #variableSpace = ['Pt_jet1:10:0:1000']
			variableSpace = ['M_uu:15:100:500','St_uujj:15:300:1800','M_uujj2:15:100:900',]
			OptimizeCuts3D(variableSpace,preselectionmumu,NormalWeightMuMu,version_name,scaleFactors,'','BLuujj')


	# ====================================================================================================================================================== #
	# This is for shape systematics
	# ====================================================================================================================================================== #

	if False :
		MuMuOptTestCutFile = 'Results_'+version_name+'/OptLQ_uujjCuts_Smoothed_pol2cutoff_1150On.txt'
		MuNuOptTestCutFile = 'Results_'+version_name+'/OptLQ_uvjjCuts_Smoothed_pol2cutoff.txt'
		# Get Scale Factors
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0)
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>100)*(MT_uv<200)*(JetCount<3.5)*(((CISV_jet1>0.97)+(CISV_jet2>0.97))<1)', '(MT_uv>100)*(MT_uv<200)*(JetCount>3.5)*(((CISV_jet1>0.97)+(CISV_jet2>0.97))>=1)')#fixme todo varying control sample MT window
		
		ShapeSystematic('uujj',NormalWeightMuMu,preselectionmumu,MuMuOptTestCutFile)
		#ShapeSystematic('uvjj',NormalWeightMuNu,preselectionmunu,MuNuOptTestCutFile)


####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################

signal = 'LQToCMu_M_300'

for n in range(len(sys.argv)):
	if sys.argv[n]=='-v' or sys.argv[n]=='--version_name':
		if len(sys.argv)<=n+1:
			print 'No version name specified. Exiting.'
			exit()
		version_name=sys.argv[n+1]
	if sys.argv[n]=='-s' or sys.argv[n]=='--signal':
		if len(sys.argv)<=n+1:
			print 'No signal specified. Exiting.'
			exit()
		signal=sys.argv[n+1]

# os.system('rm -r Results_'+version_name)


##########################################################################
########            All functions and Details Below               ########
##########################################################################

import math
sys.argv.append( '-b' )
from ROOT import *
gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")
#TFormula.SetMaxima(100000,1000,1000000)
import numpy
import math
rnd= TRandom3()
person = (os.popen('whoami').readlines()[0]).replace("\n",'')


if '/store' in NormalDirectory:
	NormalFiles = [(x.split('/')[-1]).replace('\n','') for x in os.popen('cmsLs '+NormalDirectory+"| grep \".root\" | awk '{print $1}'").readlines()]
else:
	NormalFiles = [ff.replace('\n','') for ff in os.popen('ls '+NormalDirectory+"| grep \".root\"").readlines()]

if '/store' in EMuDirectory:
	EMuFiles = [(x.split('/')[-1]).replace('\n','') for x in os.popen('cmsLs '+EMuDirectory+"| grep \".root\" | awk '{print $1}'").readlines()]
else:
	EMuFiles = [ff.replace('\n','') for ff in os.popen('ls '+EMuDirectory+"| grep \".root\"").readlines()]

if '/store' in QCDDirectory:	
	QCDFiles = [(x.split('/')[-1]).replace('\n','') for x in os.popen('cmsLs '+QCDDirectory+"| grep \".root\" | awk '{print $1}'").readlines()]
else:
	QCDFiles = [ff.replace('\n','') for ff in os.popen('ls '+QCDDirectory+"| grep \".root\"").readlines()]

for f in NormalFiles:
	_tree = 't_'+f.split('/')[-1].replace(".root","")
	_treeTmp = _tree+"_tmp"
	_prefix = '' +'root://eoscms//eos/cms'*('/store' in NormalDirectory)
	print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

for f in EMuFiles:
	_tree = 'te_'+f.split('/')[-1].replace(".root","")	
	_treeTmp = _tree+"_tmp"
	_prefix = '' +'root://eoscms//eos/cms'*('/store' in EMuDirectory)	
	print(_tree+" = TFile.Open(\""+_prefix+EMuDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+EMuDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

for f in QCDFiles:
	_tree = 'tn_'+f.split('/')[-1].replace(".root","")
	_treeTmp = _tree+"_tmp"
	_prefix = '' +'root://eoscms//eos/cms'*('/store' in QCDDirectory)	
	print(_tree+" = TFile.Open(\""+_prefix+QCDDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+QCDDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

# for f in os.popen('ls '+NormalDirectory+"| grep \".root\"").readlines():
# 	exec ('t_'+f.replace(".root\n","")+" = TFile.Open(\""+NormalDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
# 	print('t_'+f.replace(".root\n","")+" = TFile.Open(\""+NormalDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")

# for f in os.popen('ls '+EMuDirectory+"| grep \".root\"").readlines():
# 	exec('te_'+f.replace(".root\n","")+" = TFile.Open(\""+EMuDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")

# for f in os.popen('ls '+QCDDirectory+"| grep \".root\"").readlines():
# 	exec('tn_'+f.replace(".root\n","")+" = TFile.Open(\""+QCDDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")



##########################################################################
########              Clean up ROOT  Style                        ########
##########################################################################
gROOT.SetStyle('Plain')
gStyle.SetOptTitle(0)
from array import array
NCont = 50
NRGBs = 5
stops = array("d",[ 0.00, 0.34, 0.61, 0.84, 1.00])
red= array("d",[ 0.00, 0.00, 0.87, 1.00, 0.51 ])
green= array("d",[ 0.00, 0.81, 1.00, 0.20, 0.00 ])
blue= array("d",[ 0.51, 1.00, 0.12, 0.00, 0.00 ])
TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
gStyle.SetNumberContours(NCont)
##########################################################################
##########################################################################


def PDF4LHCUncStudy(MuMuOptCutFile,MuNuOptCutFile,versionname):
	print '\n\n--------------\n--------------\nGetting PDF uncertainties based on PDF4LHC prescription'
	N_cteq = 53
	N_nnpdf = 101
	N_mmth = 51

	#cteqweights = ['*(factor_cteq_'+str(n+1)+'/factor_cteq_1)' for n in range(N_cteq)]
	#nnpdfweights = ['*(factor_nnpdf_'+str(n+1)+'/factor_cteq_1)' for n in range(N_nnpdf)]
	#mmthweights = ['*(factor_mmth_'+str(n+1)+'/factor_cteq_1)' for n in range(N_mmth)]


	#cteqweights = ['*(factor_cteq_'+str(n+1+N_cteq)+')' for n in range(N_cteq)]
	#nnpdfweights = ['*(factor_nnpdf_'+str(n+1+N_nnpdf)+')' for n in range(N_nnpdf)]
	#mmthweights = ['*(factor_mmth_'+str(n+1+N_mmth)+')' for n in range(N_mmth)]
	cteqweights = ['*(factor_cteq_'+str(n+1)+')' for n in range(N_cteq)]
	nnpdfweights = ['*(factor_nnpdf_'+str(n+1)+')' for n in range(N_nnpdf)]
	mmthweights = ['*(factor_mmth_'+str(n+1)+')' for n in range(N_mmth)]

	#cteqweights = ['*(factor_cteq_'+str(n+1+N_cteq)+'/factor_cteq_'+str(N_cteq+1)+')' for n in range(N_cteq)]
	#nnpdfweights = ['*(factor_nnpdf_'+str(n+1+N_nnpdf)+'/factor_nnpdf_'+str(N_nnpdf+1)+')' for n in range(N_nnpdf)]
	#mmthweights = ['*(factor_mmth_'+str(n+1+N_mmth)+'/factor_mmth_'+str(N_mmth+1)+')' for n in range(N_mmth)]

	#cteqweightsSig = ['*(factor_cteq_'+str(n+1)+')' for n in range(N_cteq)]
	#nnpdfweightsSig = ['*(factor_nnpdf_'+str(n+1)+')' for n in range(N_nnpdf)]
	#mmthweightsSig = ['*(factor_mmth_'+str(n+1)+')' for n in range(N_mmth)]

	#cteqweightsSig = ['*(factor_cteq_'+str(n+1)+'/factor_cteq_1)' for n in range(N_cteq)]
	#nnpdfweightsSig = ['*(factor_nnpdf_'+str(n+1)+'/factor_nnpdf_1)' for n in range(N_nnpdf)]
	#mmthweightsSig = ['*(factor_mmth_'+str(n+1)+'/factor_mmth_1)' for n in range(N_mmth)]

	ResultList = []
	ResultDict = {}
	MuMuSels = []
	MuNuSels = []

	# Get selections
	for line in open(MuMuOptCutFile,'r'):
		if '=' in line:
			MuMuSels.append([line.split('=')[0].replace('\n','').replace(' ','').replace('opt_LQuujj',''),line.split('=')[-1].replace('\n','').replace(' ','')])
	for line in open(MuNuOptCutFile,'r'):
		if '=' in line:
			MuNuSels.append(line.split('=')[-1].replace('\n','').replace(' ',''))


	# UUJJ CHANNEL SYSTEMATICS

	# treenames = ['ZJets','Signal']
	#treenames = ['ZJets','TTBar','WJets','VV','sTop','Signal']#original
	treenames = ['ZJets','WJets','Signal']
	#treenames = ['ZJets','WJets','Signal']
	#treenames = ['TTBar','Signal']
	#treenames = ['Signal']
	uncnames = ['pdf_uujj_'+x for x in treenames]
	# trees  = [[t_ZJetsJBin]]
	#trees  = [[t_ZJetsJBin],[t_TTBarDBin],[t_WJetsJBin],[t_DiBoson],[t_SingleTop]]#original
	#treesNames = [['t_ZJetsJBin'],['t_TTBarDBin'],['t_WJetsJBin'],['t_DiBoson'],['t_SingleTop']]#original
	trees  = [[t_ZJetsJBin],[t_WJetsJBin]]
	treesNames = [['t_ZJetsJBin'],['t_WJetsJBin']]
	#trees  = [[t_ZJetsJBin],[t_WJetsJBin]]
	#trees  = [[t_TTBarDBin]]
	#trees  = [[t_WJetsJBin],[t_DiBoson],[t_SingleTop],[t_TTBarDBin]]
	#trees.append([t_LQuujj200,t_LQuujj250,t_LQuujj300,t_LQuujj350,t_LQuujj400,t_LQuujj450,t_LQuujj500,t_LQuujj550,t_LQuujj600,t_LQuujj650,t_LQuujj700,t_LQuujj750,t_LQuujj800,t_LQuujj850,t_LQuujj900,t_LQuujj950,t_LQuujj1000,t_LQuujj1050,t_LQuujj1100,t_LQuujj1150,t_LQuujj1200,t_LQuujj1250,t_LQuujj1300,t_LQuujj1350,t_LQuujj1400,t_LQuujj1450,t_LQuujj1500,t_LQuujj1550,t_LQuujj1600,t_LQuujj1650,t_LQuujj1700,t_LQuujj1750,t_LQuujj1800,t_LQuujj1850,t_LQuujj1900,t_LQuujj1950,t_LQuujj2000])
	trees.append([t_LQuujj200,t_LQuujj250,t_LQuujj300,t_LQuujj350,t_LQuujj400,t_LQuujj450,t_LQuujj500,t_LQuujj550,t_LQuujj600,t_LQuujj650,t_LQuujj700,t_LQuujj750,t_LQuujj800,t_LQuujj850,t_LQuujj900,t_LQuujj950,t_LQuujj1000,t_LQuujj1050,t_LQuujj1100,t_LQuujj1150,t_LQuujj1200,t_LQuujj1250,t_LQuujj1300,t_LQuujj1350,t_LQuujj1400,t_LQuujj1450,t_LQuujj1500,t_LQuujj1550,t_LQuujj1600,t_LQuujj1650,t_LQuujj1700,t_LQuujj1750,t_LQuujj1800,t_LQuujj1850,t_LQuujj1900,t_LQuujj1950,t_LQuujj2000])
	treesNames.append(['t_LQuujj200','t_LQuujj250','t_LQuujj300','t_LQuujj350','t_LQuujj400','t_LQuujj450','t_LQuujj500','t_LQuujj550','t_LQuujj600','t_LQuujj650','t_LQuujj700','t_LQuujj750','t_LQuujj800','t_LQuujj850','t_LQuujj900','t_LQuujj950','t_LQuujj1000','t_LQuujj1050','t_LQuujj1100','t_LQuujj1150','t_LQuujj1200','t_LQuujj1250','t_LQuujj1300','t_LQuujj1350','t_LQuujj1400','t_LQuujj1450','t_LQuujj1500','t_LQuujj1550','t_LQuujj1600','t_LQuujj1650','t_LQuujj1700','t_LQuujj1750','t_LQuujj1800','t_LQuujj1850','t_LQuujj1900','t_LQuujj1950','t_LQuujj2000'])


	# ================================================================================================================
	# Loop over trees to consider
	for ii in range(len(trees)):
		junkfile = TFile.Open('myjunkfileforpdfanalysis_'+str(random.randint(1,999))+'.root','RECREATE')

		# Speed up by copying to new preselection tree
		ntree = 0
		systematic = '0.0'
		_t = trees[ii][ntree]
		norm_sel = '(1)'
		print 'Analyzing',  uncnames[ii], 'in the uujj channel. Systematics are:'
		result = uncnames[ii]+' = ['
		ResultDict[uncnames[ii]+'_uujj'] = {}
		#ResultDict[uncnames[ii]+'_uujj']['cteq'] = []
		#ResultDict[uncnames[ii]+'_uujj']['mmth'] = []
		ResultDict[uncnames[ii]+'_uujj']['nnpdf'] = []		
		if 'ZJets' in uncnames[ii]:
			norm_sel = '(M_uu>80)*(M_uu<100)'
		_tnew = _t.CopyTree(preselectionmumu + '*'+norm_sel)
		# Get the preselection values for all PDF members
		presel_central_value = QuickIntegral(_tnew,NormalWeightMuMu,1.0)[0]
		#if 'Signal' in uncnames[ii]:
		#	presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweightsSig]#fixme update when names are uniform across samples
		#	presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in nnpdfweightsSig]
		#	presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in mmthweightsSig]
		#else:
		#presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweights]#fixme update when names are uniform across samples
		#presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in mmthweights]
		presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in nnpdfweights]
		# Loop over selections
		for _sel in MuMuSels:
			#print '   ... using tree',trees[ii][ntree]
			print '   ... using tree',treesNames[ii][ntree],'for M_LQ =',_sel[0]
			if 'Signal' in uncnames[ii]:
				_t = trees[ii][ntree]
				ntree += 1
				_tnew = _t.CopyTree(preselectionmumu + '*'+norm_sel)
				# Get the preselection values for all PDF members
				presel_central_value = QuickIntegral(_tnew,NormalWeightMuMu,1.0)[0]
				#if 'Signal' in uncnames[ii]:
				#	presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweightsSig]#fixme update when names are uniform across samples
				#	presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in nnpdfweightsSig]
				#	presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in mmthweightsSig]
				#else:
				#presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweights]#fixme update when names are uniform across samples
				#presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in mmthweights]
				presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in nnpdfweights]

			# Copy tree to new final selection tree
			_tnewsel = _t.CopyTree(preselectionmumu+'*'+_sel[1])
			if _tnewsel.GetEntries()<50 and ResultDict[uncnames[ii]+'_uujj']['nnpdf'] != []:#fixme changed 100 to 50
				#ResultDict[uncnames[ii]+'_uujj']['cteq'].append(  ResultDict[uncnames[ii]+'_uujj']['cteq'][-1] )
				#ResultDict[uncnames[ii]+'_uujj']['mmth'].append(  ResultDict[uncnames[ii]+'_uujj']['mmth'][-1] )
				ResultDict[uncnames[ii]+'_uujj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uujj']['nnpdf'][-1] )					
				continue
			# Get the final-selection integrals
			finsel_central_value=QuickIntegral(_tnewsel,NormalWeightMuMu,1.0)[0]
			#if 'Signal' in uncnames[ii]:
			#	finsel_varied_cteq_values = [QuickIntegral(_tnewsel,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweightsSig]#fixme update when names are uniform across samples
			#	finsel_varied_nnpdf_values = [QuickIntegral(_tnewsel,NormalWeightMuMu+_fact,1.0)[0] for _fact in nnpdfweightsSig]
			#	finsel_varied_mmth_values = [QuickIntegral(_tnewsel,NormalWeightMuMu+_fact,1.0)[0] for _fact in mmthweightsSig]
			#else:
				#finsel_varied_cteq_values = [QuickIntegral(_tnewsel,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweights]#fixme update when names are uniform across samples
				#finsel_varied_mmth_values = [QuickIntegral(_tnewsel,NormalWeightMuMu+_fact,1.0)[0] for _fact in mmthweights]
			finsel_varied_nnpdf_values = [QuickIntegral(_tnewsel,NormalWeightMuMu+_fact,1.0)[0] for _fact in nnpdfweights]
					

			# Normalize Z and Signal at preselection
			if 'ZJet' in uncnames[ii] or 'Signal' in uncnames[ii]:
				finsel_central_value /= presel_central_value
				#finsel_varied_cteq_values = [finsel_varied_cteq_values[jj]/presel_varied_cteq_values[jj] for jj in range(len(presel_varied_cteq_values))]
				#finsel_varied_mmth_values = [finsel_varied_mmth_values[jj]/presel_varied_mmth_values[jj] for jj in range(len(presel_varied_mmth_values))]
				finsel_varied_nnpdf_values = [finsel_varied_nnpdf_values[jj]/presel_varied_nnpdf_values[jj] for jj in range(len(presel_varied_nnpdf_values))]

			if finsel_central_value >0.0:
				# Get the variations w.r.t the central member
				#finsel_varied_cteq_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_cteq_values]
				#finsel_varied_mmth_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_mmth_values]
				finsel_varied_nnpdf_diffs =[abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_nnpdf_values]

				#sfinsel_varied_cteq_diffs = [(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_cteq_values]
				#sfinsel_varied_mmth_diffs = [(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_mmth_values]
				sfinsel_varied_nnpdf_diffs =[(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_nnpdf_values]

				# Adjust cteq to 68% CL
				#finsel_varied_cteq_diffs = [xx/1.645  for xx in finsel_varied_cteq_diffs]
				#ResultDict[uncnames[ii]+'_uujj']['cteq'].append(  [100*jj for jj in sfinsel_varied_cteq_diffs])
				#ResultDict[uncnames[ii]+'_uujj']['mmth'].append(  [100*jj for jj in sfinsel_varied_mmth_diffs])
				ResultDict[uncnames[ii]+'_uujj']['nnpdf'].append( [100*jj for jj in sfinsel_varied_nnpdf_diffs])
		

				old_systematic = str(systematic)
				#systematic = str(round(100.0*max( finsel_varied_cteq_diffs + finsel_varied_mmth_diffs + finsel_varied_nnpdf_diffs ),3))
				systematic = str(round(100.0*max(finsel_varied_nnpdf_diffs),3))
				if float(systematic) < float(old_systematic):
					systematic = str(old_systematic)

				if float(systematic) > 100.0:
					systematic = '100.0'
			else:
				#ResultDict[uncnames[ii]+'_uujj']['cteq'].append(  ResultDict[uncnames[ii]+'_uujj']['cteq'][-1] )
				#ResultDict[uncnames[ii]+'_uujj']['mmth'].append(  ResultDict[uncnames[ii]+'_uujj']['mmth'][-1] )
				ResultDict[uncnames[ii]+'_uujj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uujj']['nnpdf'][-1] )		
			# print ResultDict
			print systematic+'%'
			result += systematic+','
			junkfile.Close()


		result = result[:-1]+']'
		ResultList.append(result)



#	# ================================================================================================================
#	# UVJJ CHANNEL SYSTEMATICS
#
#	# treenames = ['TTBar','WJets','Signal']
#	treenames = ['ZJets','TTBar','WJets','VV','sTop','Signal']
#	uncnames = ['pdf_uvjj_'+x for x in treenames]
#	# trees  = [[t_TTBarDBin],[t_WJetsJBin]]
#	trees  = [[t_ZJetsJBin],[t_TTBarDBin],[t_WJetsJBin],[t_DiBoson],[t_SingleTop]]
#	trees.append([t_LQuvjj200,t_LQuvjj250,t_LQuvjj300,t_LQuvjj350,t_LQuvjj400,t_LQuvjj450,t_LQuvjj500,t_LQuvjj550,t_LQuvjj600,t_LQuvjj650,t_LQuvjj700,t_LQuvjj750,t_LQuvjj800,t_LQuvjj850,t_LQuvjj900,t_LQuvjj950,t_LQuvjj1000,t_LQuvjj1050,t_LQuvjj1100,t_LQuvjj1150,t_LQuvjj1200,t_LQuvjj1250,t_LQuvjj1300,t_LQuvjj1350,t_LQuvjj1400,t_LQuvjj1450,t_LQuvjj1500,t_LQuvjj1550,t_LQuvjj1600,t_LQuvjj1650,t_LQuvjj1700,t_LQuvjj1750,t_LQuvjj1800,t_LQuvjj1850,t_LQuvjj1900,t_LQuvjj1950,t_LQuvjj2000])
#
#
#	# Loop over trees to consider
#	for ii in range(len(trees)):
#		junkfile = TFile.Open('myjunkfileforpdfanalysis.root','RECREATE')
#
#		# Speed up by copying to new preselection tree
#		ntree = 0
#		systematic = '0.0'
#		_t = trees[ii][ntree]
#		norm_sel = '(1)'
#		print 'Analyzing',  uncnames[ii], 'in the uvjj channel. Systematics are:'
#		result = uncnames[ii]+' = ['
#		ResultDict[uncnames[ii]+'_uvjj'] = {}
#		ResultDict[uncnames[ii]+'_uvjj']['cteq'] = []
#		ResultDict[uncnames[ii]+'_uvjj']['mmth'] = []
#		ResultDict[uncnames[ii]+'_uvjj']['nnpdf'] = []				
#		result = uncnames[ii]+' = ['
#		if 'WJets' in uncnames[ii]:
#			norm_sel = '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)'
#		if 'TTBar' in uncnames[ii]:
#			norm_sel = '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)'		
#		_tnew = _t.CopyTree(preselectionmunu + '*'+norm_sel)
#		# Get the preselection values for all PDF members
#		presel_central_value = QuickIntegral(_tnew,NormalWeightMuNu,1.0)[0]
#		presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in cteqweights]
#		presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in nnpdfweights]
#		presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in mmthweights]
#		# Loop over selections
#		for _sel in MuNuSels:
#			print '   ... using tree',trees[ii][ntree]
#			if 'Signal' in uncnames[ii]:
#				_t = trees[ii][ntree]
#				ntree += 1
#				_tnew = _t.CopyTree(preselectionmunu + '*'+norm_sel)
#				# Get the preselection values for all PDF members
#				presel_central_value = QuickIntegral(_tnew,NormalWeightMuNu,1.0)[0]
#				presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in cteqweights]
#				presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in nnpdfweights]
#				presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in mmthweights]
#
#			# Copy tree to new final selection tree
#			_tnewsel = _t.CopyTree(preselectionmunu+'*'+_sel)
#			if _tnewsel.GetEntries()<100  and ResultDict[uncnames[ii]+'_uvjj']['cteq'] != []:
#				ResultDict[uncnames[ii]+'_uvjj']['cteq'].append(  ResultDict[uncnames[ii]+'_uvjj']['cteq'][-1] )
#				ResultDict[uncnames[ii]+'_uvjj']['mmth'].append(  ResultDict[uncnames[ii]+'_uvjj']['mmth'][-1] )
#				ResultDict[uncnames[ii]+'_uvjj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uvjj']['nnpdf'][-1] )	
#				continue				
#			# Get the final-selection integrals
#			finsel_central_value=QuickIntegral(_tnewsel,NormalWeightMuNu,1.0)[0]
#			finsel_varied_cteq_values = [QuickIntegral(_tnewsel,NormalWeightMuNu+_fact,1.0)[0] for _fact in cteqweights]
#			finsel_varied_nnpdf_values = [QuickIntegral(_tnewsel,NormalWeightMuNu+_fact,1.0)[0] for _fact in nnpdfweights]
#			finsel_varied_mmth_values = [QuickIntegral(_tnewsel,NormalWeightMuNu+_fact,1.0)[0] for _fact in mmthweights]
#
#			# Normalize W, TTBar, and Z at preselection
#			if 'WJet' in uncnames[ii] or 'TTBar' in uncnames[ii] or 'Signal' in uncnames[ii]:
#				finsel_central_value /= presel_central_value
#				finsel_varied_cteq_values = [finsel_varied_cteq_values[jj]/presel_varied_cteq_values[jj] for jj in range(len(presel_varied_cteq_values))]
#				finsel_varied_mmth_values = [finsel_varied_mmth_values[jj]/presel_varied_mmth_values[jj] for jj in range(len(presel_varied_mmth_values))]
#				finsel_varied_nnpdf_values = [finsel_varied_nnpdf_values[jj]/presel_varied_nnpdf_values[jj] for jj in range(len(presel_varied_nnpdf_values))]
#
#			if finsel_central_value >0.0:
#				# Get the variations w.r.t the central memeber
#				finsel_varied_cteq_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_cteq_values]
#				finsel_varied_mmth_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_mmth_values]
#				finsel_varied_nnpdf_diffs =[abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_nnpdf_values]
#
#				sfinsel_varied_cteq_diffs = [(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_cteq_values]
#				sfinsel_varied_mmth_diffs = [(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_mmth_values]
#				sfinsel_varied_nnpdf_diffs =[(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_nnpdf_values]
#
#				# Adjust cteq to 68% CL
#				finsel_varied_cteq_diffs = [xx/1.645  for xx in finsel_varied_cteq_diffs]
#				ResultDict[uncnames[ii]+'_uvjj']['cteq'].append([100*jj for jj in sfinsel_varied_cteq_diffs])
#				ResultDict[uncnames[ii]+'_uvjj']['mmth'].append([100*jj for jj in sfinsel_varied_mmth_diffs])
#				ResultDict[uncnames[ii]+'_uvjj']['nnpdf'].append([100*jj for jj in sfinsel_varied_nnpdf_diffs])
#
#				old_systematic = str(systematic)
#				systematic = str(round(100.0*max( finsel_varied_cteq_diffs + finsel_varied_mmth_diffs + finsel_varied_nnpdf_diffs ),3))
#				if float(systematic) < float(old_systematic):
#					systematic = str(old_systematic)
#
#				if float(systematic) > 100.0:
#					systematic = '100.0'
#			else:
#				ResultDict[uncnames[ii]+'_uvjj']['cteq'].append(  ResultDict[uncnames[ii]+'_uvjj']['cteq'][-1] )
#				ResultDict[uncnames[ii]+'_uvjj']['mmth'].append(  ResultDict[uncnames[ii]+'_uvjj']['mmth'][-1] )
#				ResultDict[uncnames[ii]+'_uvjj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uvjj']['nnpdf'][-1] )	
#			print systematic+'%'
#			result += systematic+','
#			junkfile.Close()
#
#		result = result[:-1]+']'
#		ResultList.append(result)

	json_name = 'Results_'+versionname+'/PDFVariationsDictionary.json'
	print ' -------- Creating JSON file:',json_name
	import json
	json.dump(ResultDict, open(json_name, 'wb'))


	# print '\n\n---------- Summary of PDF systematics as percentages --------\n'
	# for result in ResultList:
	# 	print result
	# print '\n\n'


def PDF4LHCPlotsFromResultDict(filename,versionname):
	import json
	dictionary = json.load(open(filename))
	
	#mass = [200 + x*50 for x in range(37)]
	mass = [250 + x*50 for x in range(16)]

	resultlist = []

	def rms(X):
		n = 0.0
		rms = 0.0
		for x in X:
			n += 1.0
			rms += x*x
		rms = rms/n
		rms = math.sqrt(rms)
		return rms

	for key in dictionary:
		result = key + ' = ['
		print 'Evaluating PDF bands for',key
		basename = key.split('_')
		chan = '#mu #mujj'*('uujj' in basename) + '#mu #nujj'*('uvjj' in basename)
		data = dictionary[key]

		c0 = TCanvas("c1","",1200,900)
		gStyle.SetOptStat(0)
		cl = TH1F('cl','cl',1,175,2025)
		cl.SetLineStyle(2)
		gStyle.SetOptTitle(1)
		cl.GetXaxis().SetTitle("LQ Mass [GeV]")
		cl.GetYaxis().SetTitle("Percent Variation")
		cl.SetTitle(basename[2]+' '+chan) 
		rmax = 1.0
		for pdfset in data:
			vsets = data[pdfset]
			for vset in vsets:
				for v in vset:
					if abs(v) > rmax:
						rmax = abs(v)
		# rmax *=0.6
		if rmax > 200.0:
			rmax = 200.0
		print '    ... Drawing for variations up to',rmax,'percent.'

		cl.SetMaximum(1.0*rmax)
		cl.SetMinimum(-1.0*(rmax))
		cl.Draw()

		hlist = []
		Crms, Mrms, Nrms, Ms = [],[],[],[]

		cteq,mstw,nnpd = [],[],[]
		old_systematic = 0.0
		systematic = 0.0
		for imass in range(len(mass)):


			old_cteq = list(cteq)
			old_mstw = list(mstw)
			old_nnpd = list(nnpd)

			cteq = data['cteq'][imass]
			mstw = data['mstw'][imass]
			nnpd = data['nnpdf'][imass]

			if cteq == old_cteq or old_cteq == [0]:
				cteq = [0]
			if mstw == old_mstw or old_mstw == [0]:
				mstw = [0]
			if nnpd == old_nnpd or  old_nnpd == [0]:
				nnpd = [0]

			C, M, N = array('d',cteq), array('d',mstw), array('d',nnpd)
			m = mass[imass]
			Cm = array('d',[m for x in C])
			Mm = array('d',[m-7. for x in M])
			Nm = array('d',[m+7. for x in N])

			# print C
			Crms.append(rms(C))
			Mrms.append(rms(M))
			Nrms.append(rms(N))

			old_systematic = systematic
			systematic = max([ Crms[-1],Mrms[-1],Nrms[-1] ])
			if systematic < old_systematic:
				systematic = old_systematic
			result += (str(round(systematic,2))) + ','
			Ms.append(1.0*m)

			hlist.append(TGraph(len(C), Cm, C))
			hlist[-1].SetMarkerStyle(24)
			hlist[-1].SetMarkerColor(6)
			hlist[-1].SetMarkerSize(0.3)

			hlist.append(TGraph(len(M), Mm, M))
			hlist[-1].SetMarkerStyle(24)
			hlist[-1].SetMarkerColor(2)
			hlist[-1].SetMarkerSize(0.3)	

			hlist.append(TGraph(len(N), Nm, N))
			hlist[-1].SetMarkerStyle(24)
			hlist[-1].SetMarkerColor(4)	
			hlist[-1].SetMarkerSize(0.3)


		result = result[:-1]
		result += ']'
		resultlist.append(result)
		print result
		for plot in hlist:
			plot.Draw("P")



		leg = TLegend(0.12,0.77,0.27,0.89,"","brNDC")
		leg.SetTextFont(42)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetBorderSize(0)
		leg.SetTextSize(.037)


		Crmsclone = list(Crms)
		Nrmsclone = list(Nrms)
		Mrmsclone = list(Mrms)
		Msclone = list(Ms)

		for xx in range(len(Crms)):
			Crms.append(-1.0*Crmsclone[-1-xx])
			Nrms.append(-1.0*Nrmsclone[-1-xx])
			Mrms.append(-1.0*Mrmsclone[-1-xx])
			Ms.append(Msclone[-1-xx])

		Crms.append(Crms[0])
		Mrms.append(Mrms[0])
		Nrms.append(Nrms[0])
		Ms.append(Ms[0])

		Crms = array('d',Crms)
		Nrms = array('d',Nrms)
		Mrms = array('d',Mrms)
		Ms = array('d',Ms)

		cwin = TPolyLine(len(Crms),Ms,Crms,"")
		cwin.SetFillColor(6)
		cwin.SetLineColor(6)
		cwin.SetLineWidth(2)
		cwin.Draw("L")

		mwin = TPolyLine(len(Mrms),Ms,Mrms,"")
		mwin.SetFillColor(2)
		mwin.SetLineColor(2)
		mwin.SetLineWidth(2)
		mwin.Draw("L")

		nwin = TPolyLine(len(Nrms),Ms,Nrms,"")
		nwin.SetFillColor(4)
		nwin.SetLineColor(4)
		nwin.SetLineWidth(2)
		nwin.Draw("L")

		ch=TH1F()
		ch.SetLineColor(6)
		ch.SetMarkerColor(6)
		ch.SetLineWidth(2)

		mh=TH1F()
		mh.SetLineColor(2)
		mh.SetMarkerColor(2)
		mh.SetLineWidth(2)

		nh=TH1F()
		nh.SetLineColor(4)
		nh.SetMarkerColor(4)
		nh.SetLineWidth(2)

		leg.AddEntry(ch,"CT10")
		leg.AddEntry(mh,"MSTW")
		leg.AddEntry(nh,"NNPDF")
		leg.Draw()


		c0.Print('Results_'+versionname+'/LQPDFValidation_'+key+'.pdf')
		c0.Print('Results_'+versionname+'/LQPDFValidation_'+key+'.png')

	print '\n\n---------- Summary of PDF systematics as percentages --------\n'
	for result in resultlist:
		print result
	print '\n\n'

	# os.system('convert -density 400 Results_'+versionname+'/PDFValidation*png Results_'+versionname+'/PDFValidation_ValPlots.pdf')
	gStyle.SetOptTitle(0)


def FixDrawLegend(legend):
	legend.SetTextFont(42)
	legend.SetFillColor(0)
	legend.SetBorderSize(0)
	legend.Draw()
	return legend

def ConvertBinning(binning):
	binset=[]
	if len(binning)==3:
		for x in range(binning[0]+1):
			binset.append(((binning[2]-binning[1])/(1.0*binning[0]))*x*1.0+binning[1])
	else:
		binset=binning
	return binset

gStyle.SetPadTopMargin(0.1);
gStyle.SetPadBottomMargin(0.16);
gStyle.SetPadLeftMargin(0.12);
#gStyle.SetPadRightMargin(0.12);
gStyle.SetPadRightMargin(0.1);

def setZeroBinErrors(data, bg):
	start = False
	nBins = data.GetNbinsX()
	for bins in range(nBins+2):
		bin = data.GetBinContent(bins)
		binBG = bg.GetBinContent(bins)
		if bin>0 or binBG>0:
			start=True
		#if start: print "\n----Bin:"+str(bins)+" bg:"+str(bg.GetStack().Last().GetBinContent(bins))+"\n"
		#if start and bin<10 and bin!=0:
		#	data.SetBinErrorOption(TH1.kPoisson)
		if start and bin==0 and bg.GetStack().Last().GetBinContent(bins)>.1:
			#print "\n----------- setting error bars for 0 bin!  Bin:"+str(bins)+" bg:"+str(bg.GetStack().Last().GetBinContent(bins))+"\n"
			data.SetBinError(bins,1.84102164458)
			#data.SetBinErrorOption(TH1.kPoisson)
	return data

def setZeroBinErrors_tgraph(data_hist,data, bg, sig_hist1, sig_hist2):
	start = False
	nBins = data.GetN()
	for bins in range(nBins):
		alpha = 1 - 0.6827;
		N = data.GetY()[bins]
		w = data_hist.GetBinWidth(bins+1);
		bin = data.GetY()[bins]
		binBG = bg.GetStack().Last().GetBinContent(bins+1)
		if N!=0: L = ROOT.Math.gamma_quantile(alpha/2,N,1.)
		else: L = 0
		U =  ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
		if bin>0 or binBG>0:
			start=True
		#if start: print "\n----Bin:"+str(bins)+" bg:"+str(bg.GetStack().Last().GetBinContent(bins))+"\n"
		if start and (bg.GetStack().Last().GetBinContent(bins+1)>.04 or sig_hist1.GetBinContent(bins+1)>0.04 or sig_hist2.GetBinContent(bins+1)>0.04):#and bin<=10 :#and bg.GetStack().Last().GetBinContent(bins+1)>.05:# and bin!=0:
		#	data.SetBinErrorOption(TH1.kPoisson)
			data.SetPointEYlow(bins,N-L)
			data.SetPointEYhigh(bins,U-N)
		#if start and bin==0 and bg.GetStack().Last().GetBinContent(bins+1)>.01:
			#print "\n----------- setting error bars for 0 bin!  Bin:"+str(bins)+" bg:"+str(bg.GetStack().Last().GetBinContent(bins))+"\n"
			#data.SetBinError(bins,1.84102164458)
		#	data.SetPointEYhigh(bins,1.84102164458)
			#data.SetBinErrorOption(TH1.kPoisson)
	return data
def setZeroBinErrors_tgraph_emu(data_hist,data, bg):
	start = False
	nBins = data.GetN()
	for bins in range(nBins):
		alpha = 1 - 0.6827;
		N = data.GetY()[bins]
		w = data_hist.GetBinWidth(bins+1);
		bin = data.GetY()[bins]
		if N!=0: L = ROOT.Math.gamma_quantile(alpha/2,N,1.)
		else: L = 0
		U =  ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
		if bin>0:
			start=True
		#if start: print "\n----Bin:"+str(bins)+" bg:"+str(bg.GetStack().Last().GetBinContent(bins))+"\n"
		if start and (bg.GetStack().Last().GetBinContent(bins+1)>.04):#and bin<=10 :#and bg.GetStack().Last().GetBinContent(bins+1)>.05:# and bin!=0:
		#	data.SetBinErrorOption(TH1.kPoisson)
			data.SetPointEYlow(bins,N-L)
			data.SetPointEYhigh(bins,U-N)
		#if start and bin==0 and bg.GetStack().Last().GetBinContent(bins+1)>.01:
			#print "\n----------- setting error bars for 0 bin!  Bin:"+str(bins)+" bg:"+str(bg.GetStack().Last().GetBinContent(bins))+"\n"
			#data.SetBinError(bins,1.84102164458)
		#	data.SetPointEYhigh(bins,1.84102164458)
			#data.SetBinErrorOption(TH1.kPoisson)
	return data

def CreateHisto(name,legendname,tree,variable,binning,selection,style,label):
	binset=ConvertBinning(binning)
	n = len(binset)-1
	hout= TH1D(name,legendname,n,array('d',binset))
	hout.Sumw2()
	tree.Project(name,variable,selection)
	hout.SetFillStyle(style[0])
	hout.SetMarkerStyle(style[1])
	hout.SetMarkerSize(style[2])
	hout.SetLineWidth(style[3])
	hout.SetMarkerColor(style[4])
	hout.SetLineColor(style[4])
	hout.SetFillColor(style[4])
	hout.SetFillColor(style[4])

	# hout.SetMaximum(2.0*hout.GetMaximum())
	hout.GetXaxis().SetTitle(label[0])
	hout.GetYaxis().SetTitle(label[1])
	hout.GetXaxis().SetTitleFont(42)
	hout.GetYaxis().SetTitleFont(42)
	hout.GetXaxis().SetLabelFont(42)
	hout.GetYaxis().SetLabelFont(42)
	hout.GetXaxis().SetLabelOffset(0.007)
	hout.GetYaxis().SetLabelOffset(0.007)
	hout.GetXaxis().SetLabelSize(0.05)
	hout.GetYaxis().SetLabelSize(0.05)

	hout.GetXaxis().SetTitleOffset(0.92)
	hout.GetYaxis().SetTitleOffset(0.92)
	hout.GetXaxis().SetTitleSize(0.06)
	hout.GetYaxis().SetTitleSize(0.06)
	hout.GetXaxis().CenterTitle(1)
	hout.GetYaxis().CenterTitle(1)

	return hout


def CreateHisto2D(name,legendname,tree,variableX,variableY,binningX,binningY,selection,style,label):
	binsetX=ConvertBinning(binningX)
	nX = len(binsetX)-1
	binsetY=ConvertBinning(binningY)
	nY = len(binsetY)-1
	hout= TH2D(name,legendname,nX,array('d',binsetX),nY,array('d',binsetY))
	hout.Sumw2()
	variable = variableY+':'+variableX
	tree.Project(name,variable,selection)
	hout.SetFillStyle(style[0])
	hout.SetMarkerStyle(style[1])
	hout.SetMarkerSize(style[2])
	hout.SetLineWidth(style[3])
	hout.SetMarkerColor(style[4])
	hout.SetLineColor(style[4])
	hout.SetFillColor(style[4])
	hout.SetFillColor(style[4])

	# hout.SetMaximum(2.0*hout.GetMaximum())
	hout.GetXaxis().SetTitle(label[0])
	hout.GetYaxis().SetTitle(label[1])
	hout.GetXaxis().SetTitleFont(42)
	hout.GetYaxis().SetTitleFont(42)
	hout.GetXaxis().SetLabelFont(42)
	hout.GetYaxis().SetLabelFont(42)
	hout.GetXaxis().SetLabelOffset(0.007)
	hout.GetYaxis().SetLabelOffset(0.007)
	hout.GetXaxis().SetLabelSize(0.05)
	hout.GetYaxis().SetLabelSize(0.05)

	hout.GetXaxis().SetTitleOffset(0.92)
	hout.GetYaxis().SetTitleOffset(0.92)
	hout.GetXaxis().SetTitleSize(0.06)
	hout.GetYaxis().SetTitleSize(0.06)
	hout.GetXaxis().CenterTitle(1)
	hout.GetYaxis().CenterTitle(1)

	return hout

def BeautifyHisto(histo,style,label,newname):
	histo.SetTitle(newname)	
	histo.SetFillStyle(style[0])
	histo.SetMarkerStyle(style[1])
	histo.SetMarkerSize(style[2])
	histo.SetLineWidth(style[3])
	histo.SetMarkerColor(style[4])
	histo.SetLineColor(style[4])
	histo.SetFillColor(style[4])
	histo.SetFillColor(style[4])
	histo.GetXaxis().SetTitle(label[0])
	histo.GetYaxis().SetTitle(label[1])
	histo.GetXaxis().SetTitleFont(42)
	histo.GetYaxis().SetTitleFont(42)
	histo.GetXaxis().SetLabelFont(42)
	histo.GetYaxis().SetLabelFont(42)
	return histo

def BeautifyStack(stack,label):
	stack.GetHistogram().GetXaxis().SetTitleFont(42)
	stack.GetHistogram().GetYaxis().SetTitleFont(42)
	stack.GetHistogram().GetXaxis().SetLabelFont(42)
	stack.GetHistogram().GetYaxis().SetLabelFont(42)
	stack.GetHistogram().GetXaxis().SetTitle(label[0])
	stack.GetHistogram().GetYaxis().SetTitle(label[1])
	stack.GetHistogram().GetXaxis().SetTitle(label[0])
	stack.GetHistogram().GetYaxis().SetTitle(label[1])
	stack.GetHistogram().GetXaxis().SetTitleFont(42)
	stack.GetHistogram().GetYaxis().SetTitleFont(42)
	stack.GetHistogram().GetXaxis().SetLabelFont(42)
	stack.GetHistogram().GetYaxis().SetLabelFont(42)
	stack.GetHistogram().GetXaxis().SetLabelOffset(0.007)
	stack.GetHistogram().GetYaxis().SetLabelOffset(0.007)
	stack.GetHistogram().GetXaxis().SetLabelSize(0.05)
	stack.GetHistogram().GetYaxis().SetLabelSize(0.05)

	stack.GetHistogram().GetXaxis().SetTitleOffset(0.92)
	stack.GetHistogram().GetYaxis().SetTitleOffset(0.92)
	stack.GetHistogram().GetXaxis().SetTitleSize(0.06)
	stack.GetHistogram().GetYaxis().SetTitleSize(0.06)
	stack.GetHistogram().GetXaxis().CenterTitle(1)
	stack.GetHistogram().GetYaxis().CenterTitle(1)
	return stack

def QuickFIntegral(tree,selection,scalefac):

	h = TH1F('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection+'*'+str(scalefac))
	I = h.GetBinContent(1)
	E = h.GetBinError(1)
	return [I,E]

def QuickIntegral(tree,selection,scalefac):

	# print selection+'*'+str(scalefac)
	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection+'*'+str(scalefac))
	I = h.GetBinContent(1)
	E = h.GetBinError(1)
	return [I,E]

def QuickSysIntegral(tree,selection,scalefac,globalscalefac):

	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection+'*'+str(globalscalefac*scalefac))
	I = h.Integral()
	E = h.GetEntries()
	return str([I,int(E)])

def QuickMultiIntegral(trees,selection,scalefacs):

	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
 	nn = -1
 	for _ib in trees:
 		nn += 1
 		exec('_bb'+str(n)+' = TH1D(\''+'_bb'+str(n)+'\',\'_bb'+str(n)+'\',1,-1,3)')
 		exec('_bb'+str(n)+'.Sumw2()')
		_ib.Project('_bb'+str(n),'1.0',selection+'*'+str(scalefacs[nn]))
 		exec('h.Add(_bb'+str(n)+')')
	I = h.GetBinContent(1)
	E = h.GetBinError(1)
	return [I,E]

def QuickEntries(tree,selection,scalefac):

	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection)
	I = h.GetEntries()
	return [1.0*I*scalefac, math.sqrt(1.0*I*scalefac)]

def QuickSysEntries(tree,selection,scalefac):

	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection)
	I = h.GetEntries()
	return str([int(1.0*I*scalefac),int(1.0*I*scalefac)]) 

def QCDStudy(sel_mumu,sel_munu,cutlogmumu,cutlogmunu,weight_mumu,weight_munu,version_name):

	print '\n\n--------------\n--------------\nPerforming QCD Study'
	#################################
	######## DIMUON CHANNEL #########
	#################################	
	print '\n------ DIMUON CHANNEL -------\n'
	#intQCD = QuickIntegral(tn_QCD,sel_mumu+"*"+weight_mumu,1.0)
	#intQCDReweight = QuickIntegral(tn_QCD,sel_mumu+"*"+weight_mumu+"*(1./pow(ptHat,4.5))",1.0)
	#ptHatReweight = intQCD[0] / intQCDReweight[0]
	#ptHatReweightStr = str(ptHatReweight)
	#intQCDNu = QuickIntegral(tn_QCD,sel_munu+"*"+weight_munu,1.0)
	#intQCDReweightNu = QuickIntegral(tn_QCD,sel_munu+"*"+weight_munu+"*(1./pow(ptHat,4.5))",1.0)
	#ptHatReweightNu = intQCDNu[0] / intQCDReweightNu[0]
	#ptHatReweightStr = str(ptHatReweight)
	#ptHatReweightStrNu = str(ptHatReweightNu)
	#weight_mumu_qcd = weight_mumu+"*(1./pow(ptHat,4.5))*"+ptHatReweightStr
	#weight_munu_qcd = weight_munu+"*(1./pow(ptHat,4.5))*"+ptHatReweightStrNu
	#Q_ss = QuickIntegral(tn_QCD,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu_qcd,1.0)	
	#Q_os = QuickIntegral(tn_QCD,sel_mumu + '*(Charge_muon1*Charge_muon2 < 0)*'+weight_mumu_qcd,1.0)
	Q_ss = QuickIntegral(tn_QCD,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)	
	Q_os = QuickIntegral(tn_QCD,sel_mumu + '*(Charge_muon1*Charge_muon2 < 0)*'+weight_mumu,1.0)


	print 'Number of events in QCD MC:'
	print 'Q_ss:',Q_ss
	print 'Q_os:',Q_os

	D_ss = QuickIntegral(tn_QCD,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print 'Test: In normal Iso data, the number of same-sign events is',QuickEntries(t_DoubleMuData,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)',1.0)
	print 'Test: In normal Iso MC, the number of same-sign events is'
	print '    Z:',QuickIntegral(t_ZJetsJBin,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print '    W:',QuickIntegral(t_WJetsJBin,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print '    t:',QuickIntegral(t_SingleTop,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print '   VV:',QuickIntegral(t_DiBoson,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print '   tt:',QuickIntegral(t_TTBarDBin,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print 'Test: QCD Prediction in SS Isolated:', QuickIntegral(tn_QCD,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu+'*(TrkIso_muon1<0.1)*(TrkIso_muon2<0.1)',1.0)

	#sys.exit()
	
	studyvals = []
	for x in range(10000):#fixme todo changed from 1,000 to 10,000
		same = RR(Q_ss)
		opp = RR(Q_os)	
		studyvals.append( (same + opp) /same )
	sameoppscale =  GetStats(studyvals)
	print "\nIn QCD MC, the conversion factor between same-sign muon events and all events is:", texentry4(sameoppscale)

	Q_ssiso = QuickIntegral(tn_QCD,sel_mumu+'*(TrkIso_muon1<0.1)*'+weight_mumu,1.0)
	studyvals = []
	for x in range(10000):#fixme todo changed from 1,000 to 10,000
		same = RR(Q_ss)
		isosame  = RR(Q_ssiso)	
		studyvals.append( isosame/same )
	singleisoscale =  GetStats(studyvals)
	print "In QCD MC, the single-muon isolation acceptance is:", texentry4(singleisoscale)

	isoscale = [singleisoscale[0]**2, 2*singleisoscale[0]*singleisoscale[1]]
	print "In QCD MC, the conversion factor between non-isolated di-muon events and isolated dimuon events is:", texentry4(isoscale)

	SSNonIsoDataRescale = [isoscale[0]*sameoppscale[0], isoscale[0]*sameoppscale[0]*(math.sqrt( (isoscale[1]/isoscale[0])**2 + (sameoppscale[1]/sameoppscale[0])**2) )    ]
	print "Thus, in same-sign non-iso data, a factor of:", texentry4(SSNonIsoDataRescale), 'will give the QCD estimate.\n'

	#qcdBinning = [0.001,0.04,0.1,0.25,0.5,1.0,1.5,2.0]
	qcdBinning=[0.001,0.05,0.1,0.25,0.75,1.5,2.5,5.0]

	sel_mumu_ss = sel_mumu#+'*(Charge_muon1*Charge_muon2 > 0)'
	#sel_mumu_ss = sel_mumu+'*(Charge_muon1*Charge_muon2 > 0)'#fixme todo put same sign back in
	#MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,2.0,5.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	#MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,2.0,5.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	#MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,1.5,2.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisoPAStagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	#MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,1.5,2.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisoPAStagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	#fixme todo added SSNonIsoDataRescale for data rescale
	###MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.02,0.04,0.075,0.1,0.15,0.2,0.4,0.75,1.0,1.5,2.0,3.5],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu_qcd,weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	###MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.02,0.04,0.075,0.1,0.15,0.2,0.4,0.75,1.0,1.5,2.0,3.5],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu_qcd,weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",qcdBinning,sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu+'*(Charge_muon1*Charge_muon2 > 0)',weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,SSNonIsoDataRescale[0])
	MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",qcdBinning,sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu+'*(Charge_muon1*Charge_muon2 > 0)',weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,SSNonIsoDataRescale[0])
	#MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,1.5,2.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisoPAStagfree','uujj',1.0,1.0,1.0,version_name,SSNonIsoDataRescale[0])
	#MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,1.5,2.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisoPAStagfree','uujj',1.0,1.0,1.0,version_name,SSNonIsoDataRescale[0])


	print '\nFor final selections, this gives estimates:\n'


	for plotmass in [ 200, 250, 300 , 350 , 400 , 450 , 500 , 550 , 600 , 650 , 700 , 750 , 800 , 850 , 900 , 950 , 1000 , 1050 , 1100 , 1150 , 1200 , 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000] :
	#for plotmass in [200]:
		channel='uujj'
		fsel = ((os.popen('cat '+cutlogmumu+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+sel_mumu+fsel+')'

		Nss_noniso_data = QuickEntries(tn_DoubleMuData,selection + '*(Charge_muon1*Charge_muon2 > 0)',1.0)
		Nss_noniso_mc = QuickMultiIntegral([tn_DiBoson,tn_TTBarDBin,tn_WJetsJBin,tn_ZJetsJBin,tn_SingleTop],selection+'*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,[1.0,1.0,1.0,1.0,1.0])		
		Nss_noniso_qcdest = [Nss_noniso_data[0] - Nss_noniso_mc[0] ,  math.sqrt(Nss_noniso_data[1]**2 + Nss_noniso_mc[1]**2)]
		N_iso_qcdest = [ Nss_noniso_qcdest[0]*SSNonIsoDataRescale[0], (math.sqrt((Nss_noniso_qcdest[1]/Nss_noniso_qcdest[0])**2 + (SSNonIsoDataRescale[1]/SSNonIsoDataRescale[0])**2))*Nss_noniso_qcdest[0]*SSNonIsoDataRescale[0] ]

		print plotmass ,'&',texentry4(N_iso_qcdest),'\\\\'

	print '\n'

	#################################
	######## 1 MUON CHANNEL #########
	#################################	
	print '\n------ MUON+MET CHANNEL -------\n'

	sel_low_munu = sel_munu + '*(Pt_miss<10)'

	# print sel_low_munu

	D_noniso = QuickEntries(tn_DoubleMuData,sel_low_munu,1.0)	
	D_iso = QuickEntries(tn_DoubleMuData,sel_low_munu + '*(TrkIso_muon1<0.1)',1.0)	

	Q_noniso = QuickIntegral(tn_QCD,sel_low_munu+'*'+weight_munu,1.0)	
	Q_iso = QuickIntegral(tn_QCD,sel_low_munu + '*(TrkIso_muon1<0.1)*'+weight_munu,1.0)	

	B_noniso = QuickMultiIntegral([tn_DiBoson,tn_TTBarDBin,tn_WJetsJBin,tn_ZJetsJBin,tn_SingleTop],sel_low_munu+'*'+weight_munu,[1.0,1.0,1.0,1.0,1.0])
	B_iso = QuickMultiIntegral([tn_DiBoson,tn_TTBarDBin,tn_WJetsJBin,tn_ZJetsJBin,tn_SingleTop],sel_low_munu+'*(TrkIso_muon1<0.1)*'+weight_munu,[1.0,1.0,1.0,1.0,1.0])

	# print '  Data (noniso):',D_noniso
	# print ' SM BG (noniso):',B_noniso
	# print 'QCD MC (noniso):',Q_noniso

	# print '  Data (iso):',D_iso
	# print ' SM BG (iso):',B_niso
	# print 'QCD MC (iso):',Q_iso

	ScaleFactor_QCD = (D_noniso[0] - B_noniso[0])/Q_noniso[0]
	ScaleFactor_QCD_Err  = (math.sqrt((math.sqrt(D_noniso[1]**2 + B_noniso[1]**2)/(D_noniso[0] - B_noniso[0]))**2 + (Q_noniso[1]/Q_noniso[0])**2))*ScaleFactor_QCD


	FakeRate = (D_iso[0] - B_iso[0])/(D_noniso[0]-B_noniso[0])
	FakeRate_err = (math.sqrt(( math.sqrt(D_iso[1]**2 + B_iso[1]**2) / (D_iso[0] - B_iso[0]) )**2 + ( math.sqrt(D_noniso[1]**2 + B_noniso[1]**2) / (D_noniso[0] - B_noniso[0]) )**2))*FakeRate

	MCFakeRate = Q_iso[0]/Q_noniso[0]
	MCFakeRate_err = (math.sqrt((Q_iso[1]/Q_iso[0])**2  + (Q_noniso[1]/Q_noniso[0])**2))*MCFakeRate


	print "\nIn the non_isolated low-MET region, the global QCD rescaling is:", texentry4([ScaleFactor_QCD,ScaleFactor_QCD_Err])
	print "\nThe data-driven fake-rate is:", texentry4([FakeRate,FakeRate_err])
	print "\nThe MC-driven fake-rate is:", texentry4([MCFakeRate,MCFakeRate_err])

	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated)",[25,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_mumu,NormalDirectory,'qcd_noniso_unweightedtagfree','uvjj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated, qcd reweighted)",[25,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_mumu,NormalDirectory,'qcd_noniso_weightedtagfree','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD)
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated)",[25,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_mumu,NormalDirectory,'qcd_noniso_unweightedPAStagfree','uvjj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated, qcd reweighted)",[25,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_mumu,NormalDirectory,'qcd_noniso_weightedPAStagfree','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD)


	sel__munu = sel_munu + '*(MT_uv>50)*(Pt_miss>55)'

	print '\nFor final selections, this gives estimates:\n'

        for plotmass in [ 200, 250, 300 , 350 , 400 , 450 , 500 , 550 , 600 , 650 , 700 , 750 , 800 , 850 , 900 , 950 , 1000 , 1050 , 1100 , 1150 , 1200 , 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000] :
	#for plotmass in [200]:
		channel='uvjj'
		fsel = ((os.popen('cat '+cutlogmunu+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+sel_munu+fsel+')'
		[Nest,Nest_err] = QuickIntegral(tn_QCD,selection+'*'+weight_munu,ScaleFactor_QCD*FakeRate)
		Nest_toterr = math.sqrt(((math.sqrt((FakeRate_err/FakeRate)**2 + (ScaleFactor_QCD_Err/ScaleFactor_QCD)**2))*Nest)**2 + Nest_err **2 ) 
		print plotmass ,'&',texentry4([Nest,Nest_toterr]),'\\\\'

	print '\n'

def texentry4(measurement):
	return '$ '+str(round(measurement[0],4))+' \\pm '+str(round(measurement[1],4))+' $'

def texentry(measurement):
	return '$ '+str(round(measurement[0],2))+' \\pm '+str(round(measurement[1],2))+' $'

def csventry(measurement):
	return str(round(measurement[0],2))+' +- '+str(round(measurement[1],2))

def QuickTableLine(treestruc,selection,scalefacs,ftex,fcsv):
	[_stree,_btrees,_dtree] = treestruc
	print 'SELECTION',selection
	_s = QuickIntegral(_stree,selection,scalefacs[0])
	_bs = [QuickIntegral(_btrees[b],selection,scalefacs[1][b]) for b in range(len(_btrees))]
	_bt = QuickMultiIntegral(_btrees,selection,scalefacs[1])
	# dselection = selection.split('*(fact')[0]
	parseselection = selection.replace('*',' ').replace(')',' ').replace('(',' ')
	parseselection = parseselection.split()
	dselection = str(selection)
	for segment in parseselection:
		if 'factor' in segment:
			dselection = dselection.replace(segment,'1')
	print 'DSELECTION',dselection
	_d = QuickEntries (_dtree,dselection+dataHLT,scalefacs[2])

	texline = ''
	for x in _bs:
		texline += ' '+texentry(x)+' &'
	texline += texentry(_bt)+' & '
	texline += texentry(_d)+' & '
	texline += texentry(_s)+' \\\\ '
	
	csvline = ''
	for x in _bs:
		csvline += ' '+csventry(x)+' ,'
	csvline += csventry(_bt)+' , '
	csvline += csventry(_d)+' , '
	csvline += csventry(_s)+'  '

	# print selection
	# print texline 

	f = open(ftex,'a')
	f.write(texline+'\n')
	f.close()

	f = open(fcsv,'a')
	f.write(csvline+'\n')
	f.close()


def QuickTableLineTTDD(treestruc,selections,scalefacs,ftex,fcsv):
	[_stree,_demutree,_mcemutrees,_btrees,_dtree] = treestruc
	[emudataselection,emumcselection,basicselection] = selections
	[signalscale,emudatascale,emumcscales,normalscales,datascale] = scalefacs

	_s = QuickIntegral(_stree,basicselection,signalscale)

	__emudat = QuickIntegral(_demutree,emudataselection,emudatascale)
	__emuBGsubtract = QuickMultiIntegral(_mcemutrees,emumcselection,emumcscales)

	# print __emudat
	# print __emuBGsubtract

	_b_ttbar = [emu_id_eff*(__emudat[0] + __emuBGsubtract[0]), emu_id_eff*(math.sqrt(__emudat[1]**2 + __emuBGsubtract[1]**2))]

	_b_other = [QuickIntegral(_btrees[b],basicselection,normalscales[b]) for b in range(len(_btrees))]

	_bs = []
	_bs.append(_b_ttbar)
	for x in _b_other:
		_bs.append(x)


	_b_tot = 0.0
	_b_tot_err = 0.0

	for b in _bs:
		_b_tot += b[0]
		_b_tot_err += b[1]**2
	_b_tot_err = math.sqrt(_b_tot_err)

	_bt = [_b_tot, _b_tot_err]

	_d = QuickEntries (_dtree,basicselection+dataHLT,datascale)



	texline = ''
	for x in _bs:
		texline += ' '+texentry(x)+' &'
	texline += texentry(_bt)+' & '
	texline += texentry(_d)+' & '
	texline += texentry(_s)+' \\\\ '
	
	csvline = ''
	for x in _bs:
		csvline += ' '+csventry(x)+' ,'
	csvline += csventry(_bt)+' , '
	csvline += csventry(_d)+' , '
	csvline += csventry(_s)+'  '

	# print selection
	print texline 

	f = open(ftex,'a')
	f.write(texline+'\n')
	f.close()

	f = open(fcsv,'a')
	f.write(csvline+'\n')
	f.close()


def QuickTable(optimlog, selection, weight,rz,rw,rt,num):
	selection = weight+'*'+selection
	texfile = optimlog.replace('.txt','_table'+str(num)+'.tex')
	csvfile = optimlog.replace('.txt','_table'+str(num)+'.csv')

	headers = ['TTBar','Z+Jets','W+Jets','sTop','VV','Tot BG','Data','Signal']


	f = open(texfile,'w')
	header = '  '
	for h in headers:
		header += h + '&'
	header = header[:-1]
	header += '\\\\'
	f.write(header+'\n')
	f.close()

	f = open(csvfile,'w')
	header = ' '
	for h in headers:
		header += h + ','
	header = header[:-1]	
	f.write(header+'\n')
	f.close()

	nline = 0
	for line in open(optimlog,'r'):

		if nline==0:

			print '  ..processing table line for optimization: ', line
			fsel = line.replace('\n','')
			masschan = fsel.split('=')[0]
			masschan = masschan.replace('\n','')
			masschan = masschan.replace(' ','')
			mass = masschan.split('jj')[-1]
			chan = 't_'+masschan.split('_')[-1]
			fsel = (fsel.split("="))[-1]
			fsel = '*'+fsel.replace(" ","")
			this_sel = '('+selection+')'

			exec('treefeed = ['+chan+']')
			#treefeed.append([t_TTBarDBin,t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson,t_ZJetsControl])
			treefeed.append([t_TTBarDBin,t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])#fixme todo no idea what zjetscontrol is...
			treefeed.append(t_DoubleMuData)
			scalefacs = [1,[rt,rz,rw,1,1],1]
			#scalefacs = [1,[rt,rz,rw,1,1,rz],1]#fixme todo added rz for ZJetsControl scale factor
			QuickTableLine(treefeed,this_sel,scalefacs,texfile,csvfile)

		print '  ..processing table line for optimization: ', line
		fsel = line.replace('\n','')
		masschan = fsel.split('=')[0]
		masschan = masschan.replace('\n','')
		masschan = masschan.replace(' ','')
		mass = masschan.split('jj')[-1]
		chan = 't_'+masschan.split('_')[-1]
		fsel = (fsel.split("="))[-1]
		fsel = fsel.replace(" ","")
		this_sel = fsel+'*'+selection

		exec('treefeed = ['+chan+']')
		treefeed.append([t_TTBarDBin,t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		treefeed.append(t_DoubleMuData)
		scalefacs = [1,[rt,rz,rw,1,1],1]
		QuickTableLine(treefeed,this_sel,scalefacs,texfile,csvfile)

		nline += 1


def QuickTableTTDD(optimlog, selection, weight,rz,rw,rt,num):
	# selection = selection+'*'+weight
	texfile = optimlog.replace('.txt','_table'+str(num)+'.tex')
	csvfile = optimlog.replace('.txt','_table'+str(num)+'.csv')

	headers = ['TTBar','Z+Jets','W+Jets','sTop','VV','Tot BG','Data','Signal']


	f = open(texfile,'w')
	header = '  '
	for h in headers:
		header += h + '&'
	header = header[:-1]
	header += '\\\\'
	f.write(header+'\n')
	f.close()

	f = open(csvfile,'w')
	header = ' '
	for h in headers:
		header += h + ','
	header = header[:-1]	
	f.write(header+'\n')
	f.close()

	nline = 0
	for line in open(optimlog,'r'):

		if nline==0:

			print '  ..processing table line for optimization: ', line
			fsel = line.replace('\n','')
			masschan = fsel.split('=')[0]
			masschan = masschan.replace('\n','')
			masschan = masschan.replace(' ','')
			mass = masschan.split('jj')[-1]
			chan = 't_'+masschan.split('_')[-1]
			fsel = (fsel.split("="))[-1]
			fsel = '*'+fsel.replace(" ","")
			this_sel = '('+selection+')'

			exec('treefeed = ['+chan+']')
			treefeed.append(te_DoubleMuData)
			treefeed.append([te_ZJetsJBin,te_WJetsJBin,te_SingleTop,te_DiBoson])
			treefeed.append([t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
			treefeed.append(t_DoubleMuData)
			scalefacs = [1,1,[-1.0*rz,-1.0*rw,-1.0,-1.0],[rz,rw,1,1],1]
			selections = [ this_sel +dataHLT+dataHLTEMUADJ, this_sel+'*'+NormalWeightEMuNoHLT, this_sel+'*'+NormalWeightMuMu ]
			QuickTableLineTTDD(treefeed,selections,scalefacs,texfile,csvfile)

		print '  ..processing table line for optimization: ', line
		fsel = line.replace('\n','')
		masschan = fsel.split('=')[0]
		masschan = masschan.replace('\n','')
		masschan = masschan.replace(' ','')
		mass = masschan.split('jj')[-1]
		chan = 't_'+masschan.split('_')[-1]
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		this_sel = '('+selection+fsel+')'

		exec('treefeed = ['+chan+']')
		treefeed.append(te_DoubleMuData)
		treefeed.append([te_ZJetsJBin,te_WJetsJBin,te_SingleTop,te_DiBoson])
		treefeed.append([t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		treefeed.append(t_DoubleMuData)

		scalefacs = [1,1,[-1.0*rz,-1.0*rw,-1.0,-1.0],[rz,rw,1,1],1]
		selections = [ this_sel +dataHLT+dataHLTEMUADJ, this_sel+'*'+NormalWeightEMuNoHLT, this_sel+'*'+NormalWeightMuMu ]		
	
		QuickTableLineTTDD(treefeed,selections,scalefacs,texfile,csvfile)

		nline += 1

def QuickSysTableLine(treestruc,selection,scalefacs,fsys,chan,rglobals,rglobalb):
	[_stree,_dtree,_btrees] = treestruc
	_s = QuickSysIntegral(_stree,selection,scalefacs[0],rglobals)
	_bs = [QuickSysIntegral(_btrees[b],selection,scalefacs[1][b],rglobalb) for b in range(len(_btrees))]
	_d = QuickSysEntries (_dtree,selection+dataHLT,scalefacs[2])

	sysline = 'L_'+chan + ' = ['
	sysline += (_s)+' , '
	sysline += (_d)+' , '
	for x in _bs:
		sysline += ' '+(x)
		sysline += ' , '
	sysline = sysline[0:-2]+' ]'

	print selection.replace('\n','')
	print ' '

	f = open(fsys,'a')
	f.write(sysline+'\n')
	f.close()


def QuickSysTableLineTTDD(treestruc,selections,scalefacs,fsys,chan,rglobals,rglobalb):
	[_stree,_demutree,_mcemutrees,_btrees,_dtree] = treestruc
	[emudataselection,emumcselection,basicselection] = selections
	[signalscale,emudatascale,emumcscales,normalscales,datascale] = scalefacs

	print 'EMU Data:', emudataselection
	print 'EMU MC:' , emumcselection
	print 'basicselection:', basicselection
	_s = QuickSysIntegral(_stree,basicselection,signalscale,rglobals)


	__emudat = QuickIntegral(_demutree,emudataselection,1.0)
	__emudat_str = QuickSysIntegral(_demutree,emudataselection,1.0,1.0)
	__emuBGsubtract = QuickMultiIntegral(_mcemutrees,emumcselection,emumcscales)

	exec('emuinfo='+__emudat_str)
	_b_ttbar = str([emudatascale*(__emudat[0] + __emuBGsubtract[0]),emuinfo[1] ])
	
	_b_other = [QuickSysIntegral(_btrees[b],basicselection,normalscales[b],rglobalb) for b in range(len(_btrees))]

	_bs = []
	_bs.append(_b_ttbar)
	for x in _b_other:
		_bs.append(x)

	# _b_tot = 0.0
	# _b_tot_err = 0.0

	# for b in _bs:
	# 	_b_tot += b[0]
	# 	_b_tot_err += b[1]**2
	# _b_tot_err = math.sqrt(_b_tot_err)

	# _bt = [_b_tot, _b_tot_err]

	_d = QuickSysEntries (_dtree,basicselection+dataHLT,datascale)

	sysline = 'L_'+chan + ' = ['
	sysline += (_s)+' , '
	sysline += (_d)+' , '
	for x in _bs:
		sysline += ' '+(x)
		sysline += ' , '
	sysline = sysline[0:-2]+' ]'


	f = open(fsys,'a')
	f.write(sysline+'\n')
	f.close()






def ModSelection(selection,sysmethod,channel_log):
	_kinematicvariables = ['Pt_muon1','Pt_muon2','Pt_ele1','Pt_ele2','Pt_jet1','Pt_jet2','Pt_miss']
	_kinematicvariables += ['Eta_muon1','Eta_muon2','Eta_ele1','Eta_ele2','Eta_jet1','Eta_jet2','Eta_miss']
	_kinematicvariables += ['Phi_muon1','Phi_muon2','Phi_ele1','Phi_ele2','Phi_jet1','Phi_jet2','Phi_miss']
	_kinematicvariables += ['St_uujj','St_uvjj']
	_kinematicvariables += ['St_eejj','St_evjj']
	_kinematicvariables += ['M_uujj1','M_uujj2','M_uujjavg','MT_uvjj1','MT_uvjj2','M_uvjj','MT_uvjj']
	_kinematicvariables += ['M_uu','MT_uv']
	_kinematicvariables += ['DR_muon1muon2','DPhi_muon1met','DPhi_jet1met']
	# _kinematicvariables += ['M_eejj1','M_eejj2','MT_evjj1','MT_evjj2','M_evjj','MT_evjj']
	# _kinematicvariables += ['JetCount','MuonCount','ElectronCount','GenJetCount']
	_weights = ['weight_nopu','weight_central', 'weight_pu_up', 'weight_pu_down']
	_variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER']	
	selsplit = []
	selchars = ''
	alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
	for s in selection:
		if s not in alphabet:
			selsplit.append(selchars)
			selchars = s
			selsplit.append(selchars)
			selchars = ''
		else:
			selchars += s
	selsplit.append(selchars)
	outsel = ''
	for v in _variations:
		if sysmethod == v:
			for sobj in selsplit:
				for k in _kinematicvariables:
					if sobj == k:
						sobj = k+sysmethod
				outsel += sobj
	if outsel != '':
		selection=outsel



	if 'weight' in selection:

		if sysmethod == 'LUMIup':
			selection = '(1.027)*'+selection
		if sysmethod == 'LUMIdown':
			selection = '(0.973)*'+selection

		if sysmethod == 'MUONIDISO':
			if 'uujj' in channel_log: 
				selection = '(1.04)*'+selection
			if 'uvjj' in channel_log: 
				selection = '(1.02)*'+selection

		if sysmethod == 'MUONHLT':
			if 'uujj' in channel_log: 
				selection = '(1.005)*'+selection
			if 'uvjj' in channel_log: 
				selection = '(1.015)*'+selection

		if sysmethod == 'PUup':
			selection = selection.replace('weight_central','weight_pu_up')
		if sysmethod == 'PUdown':
			selection = selection.replace('weight_central','weight_pu_down')

	return selection


def SysTable(optimlog, selection_uujj,selection_uvjj,NormalDirectory, weight,sysmethod):
	selection_uujj = selection_uujj+'*'+weight
	selection_uvjj = selection_uvjj+'*'+weight
	selection_uujj = ModSelection(selection_uujj,sysmethod,optimlog)
	selection_uvjj = ModSelection(selection_uvjj,sysmethod,optimlog)

	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( selection_uujj, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0)
	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( selection_uvjj, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')

	Rz_uujj_print = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
	Rtt_uujj_print = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
	Rw_uvjj_print = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
	Rtt_uvjj_print = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))	
	print sysmethod+' & ' + Rz_uujj_print+' & '+Rtt_uujj_print+' & '+Rw_uvjj_print+' & '+Rtt_uvjj_print+' \\\\'

	if 'uujj' in optimlog:
		[rz,rw,rt] = [Rz_uujj,Rw_uvjj,Rtt_uujj]
		[_e_rz,_e_rw,_e_rt] = [Rz_uujj_err,Rw_uvjj_err,Rtt_uujj_err]

		selection = selection_uujj
		alignmentcorrs = [alignmentuncs[0],alignmentuncs[1]]

	if 'uvjj' in optimlog:
		[rz,rw,rt] = [Rz_uujj,Rw_uvjj,Rtt_uvjj]
		[_e_rz,_e_rw,_e_rt] = [Rz_uujj_err,Rw_uvjj_err,Rtt_uvjj_err]	
		selection = selection_uvjj
		alignmentcorrs = [alignmentuncs[2],alignmentuncs[3]]

	rglobals = 1.0
	rglobalb = 1.0


	if sysmethod == 'ZNORMup':   
		rz *= 1.1#fixme adding this to cover discrepancy between samples
		rz += _e_rz 
	if sysmethod == 'ZNORMdown': 
		rz *= 0.9#fixme adding this to cover discrepancy between samples
		rz += -_e_rz 
	if sysmethod == 'WNORMup':     rw += _e_rw
	if sysmethod == 'WNORMdown':   rw += -_e_rw 
	if sysmethod == 'TTNORMup':  
		rt *= 1.1#fixme adding this to cover kinematic dependence of R_uu/eu
		rt += _e_rt
	if sysmethod == 'TTNORMdown':  
		rt *= 0.9#fixme adding this to cover kinematic dependence of R_uu/eu
		rt += -_e_rt 	

	#if sysmethod == 'SHAPETT' : 
		#if 'uujj' in optimlog: 
		#	rt = (1.+.01*shapesys_uujj_ttbar )*rt
		#if 'uvjj' in optimlog: 
		#	rt = (1.+.01*shapesys_uvjj_ttbar )*rt

	# if sysmethod == 'SHAPEZ'  : rz = (1.+.01*shapesys_uujj_zjets)*rz
	# if sysmethod == 'SHAPEW'  : rw = (1.+.01*shapesys_uvjj_wjets)*rw


	sysfile = optimlog.replace('.txt','_systable_'+sysmethod+'.txt')

	headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV']


	f = open(sysfile,'w')
	header = 'headers = '+str(headers)
	f.write(header+'\n')
	f.close()


	nalign = -1
	for line in open(optimlog,'r'):
		nalign =-1
		line = line.replace('\n','')
		print 'processing table line for optimization: ', line

		fsel = line.replace('\n','')
		fsel = ModSelection(fsel,sysmethod,optimlog)
		masschan = fsel.split('=')[0]
		masschan = masschan.replace('\n','')
		masschan = masschan.replace(' ','')
		mass = masschan.split('jj')[-1]
		chan = 't_'+masschan.split('_')[-1]
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		this_sel = '('+selection+fsel+')'

		print ' *'*100
		for ii in range(len(pdf_MASS)):
			pdfm = pdf_MASS[ii]
			if str(pdfm) == mass:
				nalign = ii
		print nalign

		if sysmethod == 'ALIGN':
			if 'uujj' in optimlog:
				rglobals = 1.0 + alignmentcorrs[0]*.01
				rglobalb = 1.0 + alignmentcorrs[1]*.01
			if 'uvjj' in optimlog:
				rglobals = 1.0 + alignmentcorrs[0]*.01
				rglobalb = 1.0 + alignmentcorrs[1][nalign] *.01



		rstop = 1
		rdiboson = 1
		rsig = 1
		_rt = rt
		_rw = rw
		_rz = rz

		if sysmethod == 'SHAPETT':#fixme added this for 2015 method
			if 'uujj' in optimlog:
				_rt *= (1.0+shapesysvar_uujj_ttjets[nalign]*0.01)
			if 'uvjj' in optimlog:
				_rt *= (1.0+shapesysvar_uvjj_ttjets[nalign]*0.01)

		if sysmethod == 'SHAPEZ':
			_rz *= (1.0+shapesysvar_uujj_zjets[nalign]*0.01)

		if sysmethod == 'SHAPEW':
			_rw *= (1.0+shapesysvar_uvjj_wjets[nalign]*0.01)

		if 'PDF'  in sysmethod:
			if 'uujj' in optimlog:
				_rt *= (1.0+pdf_uujj_TTBar[nalign]*0.01)
				_rw *= (1.0+pdf_uujj_WJets[nalign]*0.01)
				_rz *= (1.0+pdf_uujj_ZJets[nalign]*0.01)
				rstop *= (1.0+pdf_uujj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uujj_VV[nalign]*0.01)
				rsig *= (1.0+pdf_uujj_Signal[nalign]*0.01)

			if 'uvjj' in optimlog:
				_rt *= (1.0+pdf_uvjj_TTBar[nalign]*0.01)
				_rw *= (1.0+pdf_uvjj_WJets[nalign]*0.01)
				_rz *= (1.0+pdf_uvjj_ZJets[nalign]*0.01)
				rstop *= (1.0+pdf_uvjj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uvjj_VV[nalign]*0.01)
				rsig *= (1.0+pdf_uvjj_Signal[nalign]*0.01)

		exec('treefeed = ['+chan+']')
		treefeed.append(t_DoubleMuData)
		treefeed.append([t_TTBarDBin,t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		scalefacs = [rsig,[_rt,_rz,_rw,rstop,rdiboson],1]
		QuickSysTableLine(treefeed,this_sel,scalefacs,sysfile,chan,rglobals,rglobalb)
		# break



def SysTableTTDD(optimlog, selection_uujj,selection_uvjj,NormalDirectory, weight,sysmethod):
	selection_uujj = selection_uujj
	selection_uvjj = selection_uvjj

	selection_uujj_unmod = ModSelection(selection_uujj,"",optimlog)
	selection_uvjj_unmod = ModSelection(selection_uvjj,"",optimlog)

	selection_uujj = ModSelection(selection_uujj,sysmethod,optimlog)
	selection_uvjj = ModSelection(selection_uvjj,sysmethod,optimlog)

	weightmod = '*'+ModSelection(weight,sysmethod,optimlog)

	weightmod_uvjj = '*'+ModSelection(NormalWeightMuNu,sysmethod,optimlog)

	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( selection_uujj+weightmod, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1)
	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( selection_uvjj+weightmod_uvjj, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')

	[Rtt_uujj, Rtt_uujj_err] = [emu_id_eff, emu_id_eff_err]

	Rz_uujj_print = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
	Rtt_uujj_print = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
	Rw_uvjj_print = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
	Rtt_uvjj_print = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))	
	print sysmethod+' & ' + Rz_uujj_print+' & '+Rtt_uujj_print+' & '+Rw_uvjj_print+' & '+Rtt_uvjj_print+' \\\\'

	if 'uujj' in optimlog:
		[rz,rw,rt] = [Rz_uujj,Rw_uvjj,Rtt_uujj]
		[_e_rz,_e_rw,_e_rt] = [Rz_uujj_err,Rw_uvjj_err,Rtt_uujj_err]

		selection = selection_uujj
		selection_unmod = selection_uujj_unmod
		alignmentcorrs = [alignmentuncs[0],alignmentuncs[1]]

	if 'uvjj' in optimlog:
		[rz,rw,rt] = [Rz_uujj,Rw_uvjj,Rtt_uvjj]
		[_e_rz,_e_rw,_e_rt] = [Rz_uujj_err,Rw_uvjj_err,Rtt_uvjj_err]	
		selection = selection_uvjj
		selection_unmod = selection_uvjj_unmod
		alignmentcorrs = [alignmentuncs[2],alignmentuncs[3]]

	rglobals = 1.0
	rglobalb = 1.0


	if sysmethod == 'ZNORMup':     rz += _e_rz 
	if sysmethod == 'ZNORMdown':   rz += -_e_rz 
	if sysmethod == 'WNORMup':     rw += _e_rw
	if sysmethod == 'WNORMdown':   rw += -_e_rw 
	if sysmethod == 'TTNORMup':    rt += _e_rt
	if sysmethod == 'TTNORMdown':  rt += -_e_rt 	

	# if sysmethod == 'SHAPETT' : 
	# 	if 'uujj' in optimlog: 
	# 		rt = 1.077*rt
	# 	if 'uvjj' in optimlog: 
	# 		rt = 1.199*rt

	# if sysmethod == 'SHAPEZ'  : rz = (1.+.01*shapesys_uujj_zjets)*rz
	# if sysmethod == 'SHAPEW'  : rw = (1.+.01*shapesys_uvjj_wjets)*rw

	sysfile = optimlog.replace('.txt','_systable_'+sysmethod+'.txt')

	headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV']


	f = open(sysfile,'w')
	header = 'headers = '+str(headers)
	f.write(header+'\n')
	f.close()


	nalign = -1
	for line in open(optimlog,'r'):
		nalign = -1
		line = line.replace('\n','')
		print 'processing table line for optimization: ', line


		fsel = line.replace('\n','')
		fsel_unmod = ModSelection(fsel,"",optimlog)

		fsel = ModSelection(fsel,sysmethod,optimlog)

		masschan = fsel.split('=')[0]
		masschan = masschan.replace('\n','')
		masschan = masschan.replace(' ','')
		mass = masschan.split('jj')[-1]
		chan = 't_'+masschan.split('_')[-1]
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		this_sel = '('+selection+fsel+')'

		print ' *'*100
		for ii in range(len(pdf_MASS)):
			pdfm = pdf_MASS[ii]
			if str(pdfm) == mass:
				nalign = ii
		print nalign

		if sysmethod == 'ALIGN':
			if 'uujj' in optimlog:
				rglobals = 1.0 + alignmentcorrs[0]*.01
				rglobalb = 1.0 + alignmentcorrs[1]*.01
			if 'uvjj' in optimlog:
				rglobals = 1.0 + alignmentcorrs[0]*.01
				rglobalb = 1.0 + alignmentcorrs[1][nalign] *.01


		fsel_unmod = (fsel_unmod.split("="))[-1]
		fsel_unmod = '*'+fsel_unmod.replace(" ","")
		this_sel_unmod = '('+selection_unmod+fsel_unmod+')'

		rstop = 1
		rdiboson = 1
		rsig = 1
		_rt = rt
		_rw = rw
		_rz = rz


		if sysmethod == 'SHAPEZ':
			_rz *= (1.0+shapesysvar_uujj_zjets[nalign]*0.01)

		if sysmethod == 'SHAPEW':
			_rw *= (1.0+shapesysvar_uvjj_wjets[nalign]*0.01)


		if 'PDF'  in sysmethod:
			if 'uujj' in optimlog:
				# _rt *= (1.0+pdf_uujj_TTBar[nalign]*0.01)
				_rw *= (1.0+pdf_uujj_WJets[nalign]*0.01)
				_rz *= (1.0+pdf_uujj_ZJets[nalign]*0.01)
				rstop *= (1.0+pdf_uujj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uujj_VV[nalign]*0.01)
				rsig *= (1.0+pdf_uujj_Signal[nalign]*0.01)

			if 'uvjj' in optimlog:
				_rt *= (1.0+pdf_uvjj_TTBar[nalign]*0.01)
				_rw *= (1.0+pdf_uvjj_WJets[nalign]*0.01)
				_rz *= (1.0+pdf_uvjj_ZJets[nalign]*0.01)
				rstop *= (1.0+pdf_uvjj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uvjj_VV[nalign]*0.01)
				rsig *= (1.0+pdf_uvjj_Signal[nalign]*0.01)


		exec('treefeed = ['+chan+']')
		treefeed.append(te_DoubleMuData)
		treefeed.append([te_ZJetsJBin,te_WJetsJBin,te_SingleTop,te_DiBoson])
		treefeed.append([t_ZJetsJBin,t_WJetsJBin,t_SingleTop,t_DiBoson])
		treefeed.append(t_DoubleMuData)

		scalefacs = [rsig,_rt,[-1.0*_rz,-1.0*_rw,-1.0*rstop,-1.0*rdiboson],[_rz,_rw,rstop,rdiboson],1]
		selections = [ this_sel_unmod +dataHLT+dataHLTEMUADJ, this_sel_unmod+'*'+NormalWeightEMuNoHLT, this_sel+weightmod ]		

		QuickSysTableLineTTDD(treefeed,selections,scalefacs,sysfile,chan,rglobals,rglobalb)
		# break

def FullAnalysis(optimlog,selection_uujj,selection_uvjj,NormalDirectory,weight,usedd):
	TTDD = False
	if usedd=='TTBarDataDriven':
		TTDD=True
	_Variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','WNORMup','WNORMdown','TTNORMup','TTNORMdown','SHAPETT','SHAPEZ','SHAPEW','MUONIDISO','MUONHLT','ALIGN','PDF']	
	for v in _Variations:
		print ' -'*50
		print 'Processing table for variation: ',v
		if (optimlog.replace('.txt','_systable_'+v+'.txt')) in str(os.popen('ls '+optimlog.replace('.txt','_systable_'+v+'.txt')).readlines()):
			print 'Already present ... skipping. '
			continue
		if TTDD:
			SysTableTTDD(optimlog, selection_uujj, selection_uvjj,NormalDirectory, weight,v)
		else:
			SysTable(optimlog, selection_uujj, selection_uvjj,NormalDirectory, weight,v)




def GetScaleFactors(n1,n2,a1,a2,b1,b2,o1,o2):
	Ra = 1.0
	Rb = 1.0
	for x in range(10):
		Ra = (n1 - Rb*b1 - o1)/(a1)
		Rb = (n2 - Ra*a2 - o2)/(b2) 
	return [Ra, Rb]

def GetSimpleScaleFactors(n1,n2,a1,a2,b1,b2,o1,o2):
	Ra = 1.0
	Rb = 1.0
	for x in range(10):
		# Ra = (n1 - 1.0*b1 - o1)/(a1)
		Rb = (n2 - 1.0*a2 - o2)/(b2) 
	return [Ra, Rb]

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

def binmeanstdv(X,Y,Yrange):
	x = []
	for j in range(len(X)):
		if Y[j] > Yrange[0] and Y[j] < Yrange[1]:
			x.append(X[j])

	n, mean, std = len(x), 0, 0 

	for a in x: 
		mean = mean + a 
	if n >= 1:
		mean = mean / float(n) 
	else:
		mean = 0
	for a in x: 
		std = std + (a - mean)**2 
	if n>=1:	
		std = math.sqrt(std / float(n)) 
	elif n == 1:
		std = mean
	else:
		std = 99999999.
	print Yrange,len(x),mean,std
	return [mean, std]

def GetProfile(X,Y,binning):
	X= [1.0*xx for xx in X]
	Y= [1.0*yy for yy in Y]
	binset = ConvertBinning(binning)
	bins = []
	for b in range(len(binset)-1):
		bmin = binset[b]
		bmax = binset[b+1]
		bins.append([bmin,bmax])
	Ymeans = []
	Yerrs = []
	Xmeans = []
	Xerrs = []
	for B in bins:
		stats = binmeanstdv(X,Y,B)
		Ymeans.append(stats[0])
		Yerrs.append(stats[1])
		Xmeans.append((B[1] + B[0])/2.0)
		Xerrs.append(abs(B[1] - B[0])/2.0)
	return [Xmeans,Xerrs,Ymeans,Yerrs]



def RR(List):
	return random.gauss(List[0],List[1])

def PrintRuns():
	tmpfile = TFile("tmp.root","RECREATE")
	t_DoubleMuData2 = t_DoubleMuData.CopyTree(preselectionmunu)
	allruns = []
	NN = t_DoubleMuData2.GetEntries()
	for n in range(NN):
		if n%1000 ==0:
			print n,'of',NN
		t_DoubleMuData2.GetEntry(n)
		ev = t_DoubleMuData2.run_number
		if ev not in allruns:
			allruns.append(ev)

	allruns.sort()
	for a in allruns:
		print a

def GetMuMuScaleFactors( selection, FileDirectory, controlregion_1, controlregion_2, canUseTTDD):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_DoubleMuData,selection + '*' + controlregion_1,1.0)
	# print QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	# sys.exit()
	selection_data = selection.split('*(fact')[0]

	N1 = QuickEntries(t_DoubleMuData,selection_data + '*' + controlregion_1+dataHLT,1.0)
	print selection_data + '*' + controlregion_1+dataHLT
	N2 = QuickEntries(t_DoubleMuData,selection_data + '*' + controlregion_2+dataHLT,1.0)

	Z1 = QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBarDBin,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(t_WJetsJBin,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)
	q1 = QuickIntegral(t_QCDMu,selection   + '*' + controlregion_1,1.0)
	H1 = QuickIntegral(t_SMHiggs,selection   + '*' + controlregion_1,1.0)

	Z2 = QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBarDBin,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(t_WJetsJBin,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)
	q2 = QuickIntegral(t_QCDMu,selection   + '*' + controlregion_2,1.0)
	H2 = QuickIntegral(t_SMHiggs,selection   + '*' + controlregion_2,1.0)

	Other1 = [ s1[0]+w1[0]+v1[0]+q1[0]+H1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] + q1[1]*q1[1] + H1[1]*H1[1]) ]
	Other2 = [ s2[0]+w2[0]+v2[0]+q2[0]+H2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] + q2[1]*q2[1] + H2[1]*H2[1]) ]

	#Other1 = [ s1[0]+w1[0]+v1[0]+H1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] + H1[1]*H1[1]) ]
	#Other2 = [ s2[0]+w2[0]+v2[0]+H2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] + H2[1]*H2[1]) ]

	Other1NoH = [ s1[0]+w1[0]+v1[0]+q1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] + q1[1]*q1[1]) ]
	Other2NoH = [ s2[0]+w2[0]+v2[0]+q2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] + q2[1]*q2[1]) ]

	#Other1NoH = [ s1[0]+w1[0]+v1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1]) ]
	#Other2NoH = [ s2[0]+w2[0]+v2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1]) ]

	zvals = []
	tvals = []

	for x in range(1000):#fixme was 10000
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(Z1),RR(Z2),RR(T1),RR(T2),Other1[0],Other2[0]))
		zvals.append(variation[0])
		tvals.append(variation[1])

	zout =  GetStats(zvals)
	tout = GetStats(tvals)

	# ttbar force unity
	if useDataDrivenTTbar and canUseTTDD:
		print 'Using Data-driven TTbar'
		tout = [1.0,0.067,'1.000 +- 0.067'] #fixme todo need to understand why 0.067

        ## Force to pre-calculated values to speed things up
	#zout = [3.251,0.059,'3.251 +- 0.059']
	#tout = [2.19,0.037,'2.19  +- 0.037']
	#print 'Using pre-calculated values, rerun if you add more data!'

	print 'MuMu scale factor integrals:'
	print 'Data:',N1,N2
	print 'Z:',Z1,Z2
	print 'TT:',T1,T2
	print 'Other:',Other1NoH,Other2NoH
	print 'SMHiggs:',H1,H2

	print 'MuMu: RZ  = ', zout[-1]
	print 'MuMu: Rtt = ', tout[-1]
	return [ [ zout[0], zout[1] ] , [ tout[0],tout[1] ] ]

def GetMuMuScaleFactorsMod( selection, FileDirectory, controlregion_1, controlregion_2,samp):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_DoubleMuData,selection + '*' + controlregion_1,1.0)
	# print QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	# sys.exit()

	ScaleUpSelection = selection+'*scaleWeight_Up'
	ScaleDownSelection = selection+'*scaleWeight_Down'#fixme todo update for matching
	MatchUpSelection = selection+'*scaleWeight_Up'
	MatchDownSelection = selection+'*scaleWeight_Down'#fixme todo update for matching
	selectionMod = selection

	if 'ScaleUp' in samp:
		#t_Z = t_ZJetsScaleUp
		#t_T = t_TTJetsScaleDown
		t_Z = t_ZJetsJBin
		t_T = t_TTBarDBin	
		selectionMod=ScaleUpSelection

	elif 'ScaleDown' in samp:
		#t_Z = t_ZJetsScaleDown
		#t_T = t_TTJetsScaleDown
		t_Z = t_ZJetsJBin
		t_T = t_TTBarDBin	
		selectionMod=ScaleDownSelection

	elif 'MatchUp' in samp:
		#t_Z = t_ZJetsMatchUp
		#t_T = t_TTJetsMatchDown
		t_Z = t_ZJetsJBin
		t_T = t_TTBarDBin	
		selectionMod=ScaleUpSelection#fixme todo update for matching

	elif 'MatchDown' in samp:
		#t_Z = t_ZJetsMatchDown
		#t_T = t_TTJetsMatchDown
		t_Z = t_ZJetsJBin
		t_T = t_TTBarDBin	
		selectionMod=ScaleDownSelection#fixme todo update for matching
	else:
		t_Z = t_ZJetsJBin
		t_T = t_TTBarDBin		

	N1 = QuickEntries(t_DoubleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_DoubleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

	Z1 = QuickIntegral(t_Z,selectionMod + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBarDBin,selectionMod + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(t_WJetsJBin,selectionMod + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)

	Z2 = QuickIntegral(t_Z,selectionMod + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBarDBin,selectionMod + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(t_WJetsJBin,selectionMod + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)



	Other1 = [ s1[0]+w1[0]+v1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+w2[0]+v2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] ) ]
	zvals = []
	tvals = []

	for x in range(10000):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(Z1),RR(Z2),RR(T1),RR(T2),Other1[0],Other2[0]))
		zvals.append(variation[0])
		tvals.append(variation[1])

	zout =  GetStats(zvals)
	tout = GetStats(tvals)

	# ttbar force unity
	if useDataDrivenTTbar:
		print 'Using Data-driven TTbar'
		tout = [1.0,0.067,'1.000 +- 0.067']

	print 'MuMu: RZ  = ', zout[-1]
	print 'MuMu: Rtt = ', tout[-1]
	return [ [ zout[0], zout[1] ] , [ tout[0],tout[1] ] ]



def GetEMuScaleFactors( selection, FileDirectory):

	print '\n\n--------------\n--------------\nChecking TTBar E-Mu sample against E_Mu MC with selection:'
	print selection 
	N1 = QuickEntries(te_DoubleMuData,selection  + dataHLT,1.0)

	Z1 = QuickIntegral(te_ZJetsJBin,selection ,1.0)
	T1 = QuickIntegral(te_TTBarDBin,selection ,1.0)
	s1 = QuickIntegral(te_SingleTop,selection ,1.0)
	w1 = QuickIntegral(te_WJetsJBin,selection ,1.0)
	v1 = QuickIntegral(te_DiBoson,selection ,1.0)


	print 'This is the information for the NOTE table 6:'
	print ' Data:',N1[0]
	print '   TT:',T1[0]
	print '    Z:',Z1[0]
	print ' Stop:',s1 [0]
	print '    W:',w1[0]
	print '   VV:',v1[0]



	SF=[1.0,0.0]

	SF[0] = (N1[0] - Z1[0] - s1[0] -v1[0] - w1[0])/T1[0]

	relerror_num  = math.sqrt(N1[1]**2. + Z1[1]**2. + s1[1]**2. + v1[1]**2. + w1[1]**2.)/(N1[0] - Z1[0] - s1[0] -v1[0] - w1[0])
	relerror_denom = T1[1]/T1[0]
	SF[1] = SF[0]*math.sqrt(relerror_num**2.0 + relerror_denom**2.)

	print 'MuMu: Rtt = ', SF


	print 'Now calculating R_mumu,emu, the ratio of mumu to e,mu events in ttbar MC. '
	print 'Should be near 0.5'
	#print selection,'\n\n'
	#print selection.replace(singlemuHLTEMU,singlemuHLT).replace(MuIdScaleEMU,MuIdScale).replace(MuIsoScaleEMU,MuIsoScale),'\n\n'
	T2 = QuickIntegral(t_TTBarDBin,selection.replace(singlemuHLTEMU,singlemuHLT), 1.0)
	#T2 = QuickIntegral(t_TTBarDBin,selection.replace(singlemuHLTEMU,singlemuHLT).replace(MuIdScaleEMU,MuIdScale).replace(MuIsoScaleEMU,MuIsoScale) ,1.0)

	Ruueu = T2[0]/T1[0]
	dRuueu =  Ruueu*(math.sqrt((T1[1]/T1[0])**2.0 + (T2[1]/T2[0])**2.0))

	print 'R_uu,eu = ',Ruueu,' +- ',dRuueu

	return SF

def GetMuNuScaleFactorsMod( selection, FileDirectory, controlregion_1, controlregion_2,samp):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")

	ScaleUpSelection = selection+'*scaleWeight_Up'
	ScaleDownSelection = selection+'*scaleWeight_Down'#fixme todo update for matching
	MatchUpSelection = selection+'*scaleWeight_Up'
	MatchDownSelection = selection+'*scaleWeight_Down'#fixme todo update for matching
	selectionMod = selection

	if 'ScaleUp' in samp:
		#t_W = t_WJetsScaleUp
		#t_T = t_TTJetsScaleDown
		t_W = t_WJetsJBin
		t_T = t_TTBarDBin
		selectionMod=ScaleUpSelection

	elif 'ScaleDown' in samp:
		#t_W = t_WJetsScaleDown
		#t_T = t_TTJetsScaleDown
		t_W = t_WJetsJBin
		t_T = t_TTBarDBin
		selectionMod=ScaleDownSelection

	elif 'MatchUp' in samp:
		#t_W = t_WJetsMatchUp
		#t_T = t_TTJetsMatchDown
		t_W = t_WJetsJBin
		t_T = t_TTBarDBin
		selectionMod=ScaleUpSelection#fixme todo update for matching

	elif 'MatchDown' in samp:
		#t_W = t_WJetsMatchDown
		#t_T = t_TTJetsMatchDown
		t_W = t_WJetsJBin
		t_T = t_TTBarDBin
		selectionMod=ScaleDownSelection#fixme todo update for matching

	else:
		t_W = t_WJetsJBin
		t_T = t_TTBarDBin		

	N1 = QuickEntries(t_DoubleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_DoubleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

	W1 = QuickIntegral(t_W,selectionMod + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_T,selectionMod + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	z1 = QuickIntegral(t_ZJetsJBin,selectionMod + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)

	W2 = QuickIntegral(t_W,selectionMod + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_T,selectionMod + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	z2 = QuickIntegral(t_ZJetsJBin,selectionMod + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)

	Other1 = [ s1[0]+z1[0]+v1[0], math.sqrt( s1[1]*s1[1] + z1[1]*z1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+z2[0]+v2[0], math.sqrt( s2[1]*s2[1] + z2[1]*z2[1] + v2[1]*v2[1] ) ]

	print 'Data:',N1,N2
	print 'TT:',T1,T2
	print 'W:',W1,W2
	print 'Other:',Other1,Other2

	wvals = []
	tvals = []



	for x in range(10000):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(W1),RR(W2),RR(T1),RR(T2),Other1[0],Other2[0]))
		wvals.append(variation[0])
		tvals.append(variation[1])

	wout =  GetStats(wvals)
	tout = GetStats(tvals)

	print 'MuNu: RW  = ', wout[-1]
	print 'MuNu: Rtt = ', tout[-1]
	return [ [ wout[0], wout[1] ] , [ tout[0],tout[1] ] ]


def GetMuNuScaleFactors( selection, FileDirectory, controlregion_1, controlregion_2):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	selection_data = selection.split('*(fact')[0]

	N1 = QuickEntries(t_DoubleMuData,selection_data + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_DoubleMuData,selection_data + '*' + controlregion_2+dataHLT,1.0)

	W1 = QuickIntegral(t_WJetsJBin,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBarDBin,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	z1 = QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,  selection + '*' + controlregion_1,1.0)

	W2 = QuickIntegral(t_WJetsJBin,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBarDBin,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	z2 = QuickIntegral(t_ZJetsJBin,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,  selection + '*' + controlregion_2,1.0)

	Other1 = [ s1[0]+z1[0]+v1[0], math.sqrt( s1[1]*s1[1] + z1[1]*z1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+z2[0]+v2[0], math.sqrt( s2[1]*s2[1] + z2[1]*z2[1] + v2[1]*v2[1] ) ]
	wvals = []
	tvals = []

	for x in range(10000):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(W1),RR(W2),RR(T1),RR(T2),Other1[0],Other2[0]))
		wvals.append(variation[0])
		tvals.append(variation[1])

	print 'Here $(N_1,N_2) = (  ',
	print round(N1[0],1),',',round(N2[0],1),
	print ')$, $(N_{1,\\ttbar},N_{2,\\ttbar}) = ( ',
	print round(T1[0],1),'\\pm',round(T1[1],1),',',round(T2[0],1),'\\pm',round(T2[1],1),
	print ')$,  $(N_{1,W},N_{2,W}) = ( ',
	print round(W1[0],1),'\\pm',round(W1[1],1),',',round(W2[0],1),'\\pm',round(W2[1],1),
	print '$, and $(N_{1,0},N_{2,0}) = ( ',
	print round(Other1[0],1),'\\pm',round(Other1[1],1),',',round(Other2[0],1),'\\pm',round(Other2[1],1),
	print ')$.' 


	wout =  GetStats(wvals)
	tout = GetStats(tvals)

        #Force to pre-calculated values to speed things up
	#wout = [4.563,0.048,'4.563 +- 0.048']
	#tout = [1.9,0.037  ,'1.9   +- 0.037']
	#print 'Using pre-calculated values, rerun if you add more data!'

	print 'MuNu scale factor integrals:'
	print 'Data:',N1,N2
	print 'W:',W1,W2
	print 'TT:',T1,T2
	print 'Other:',Other1,Other2

	print 'MuNu: RW  = ', wout[-1]
	print 'MuNu: Rtt = ', tout[-1]
	return [ [ wout[0], wout[1] ] , [ tout[0],tout[1] ] ]




def MakeEfficiencyPlot(FileDirectory,weight,cutlog,channel,version_name):
	print "\n\n--------------\n--------------\nMaking signal efficiency*acceptance plot..."
	c1 = TCanvas("c1","",800,550)
	c1.cd()
	massBins=0
	lowMass=0
	ratiosFinal=[]
	ratiosFinalCTau10=[]
	ratiosFinalCTau100=[]
	ratiosFinalCTau1000=[]
	ratiosPresel=[]
	ratiosPreselCTau10=[]
	ratiosPreselCTau100=[]
	ratiosPreselCTau1000=[]
	isDisplaced = 'BL' in channel
	if isDisplaced : 
		masses   = pdf_MASS_displaced
	else : masses = pdf_MASS
	highMass = masses[-1] #fixme this is a temporary solution, need to figure out how to handle last entry in cutlog correctly
	for plotmass in masses:
		if plotmass>highMass: break #fixme this is a temporary solution, need to figure out how to handle last entry in cutlog correctly
		print 'Getting Final sel for M =',plotmass
		if cutlog !='':
		        #print 'cat '+cutlog+' | grep '+channel+str(plotmass)
			if 'LQ'in channel:
				fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
			elif 'BL' in channel:
				fsel = ((os.popen('cat '+cutlog+' | grep '+'uujj'+str(plotmass)).readlines())[0]).replace('\n','')
			if fsel=='':
				print 'No more entries in cutlog, exiting...'
				break
			else: print 'found'
			fsel = (fsel.split("="))[-1].replace(" ","")
		else : fsel = '1.0'
		selectionNoSel  = '('+weight+')'
		selectionPresel = '('+weight+'*'+preselectionmumu+')'
		selectionFinal  = '('+weight+'*'+preselectionmumu+'*'+fsel+')'
		print weight
		print selectionFinal
		if isDisplaced : exec("tree = t_"+channel+'CTau1'+'uujj'+str(plotmass))
		else : exec("tree = t_"+channel+str(plotmass))
		noSelInt  = QuickIntegral(tree,selectionNoSel,1.0)
		preselInt = QuickIntegral(tree,selectionPresel,1.0)
		finalInt  = QuickIntegral(tree,selectionFinal,1.0)
		if noSelInt[0]>0: 
			ratioFinal = finalInt[0]/noSelInt[0]
			ratioPresel = preselInt[0]/noSelInt[0]
		else:             
			ratioPresel = 0
			ratioFinal = 0
		print plotmass,ratioFinal,noSelInt,preselInt,finalInt
		if noSelInt[0]>0 and finalInt[0]>0:
			ratioFinalErr = (finalInt[0]/noSelInt[0])*math.sqrt((finalInt[1]**2)/(finalInt[0]**2)+(noSelInt[1]**2)/(noSelInt[0]**2))
			ratioPreselErr = (preselInt[0]/noSelInt[0])*math.sqrt((preselInt[1]**2)/(preselInt[0]**2)+(noSelInt[1]**2)/(noSelInt[0]**2))
		else:
			ratioFinalErr = 0
			ratioPreselErr = 0
		ratiosFinal.append([ratioFinal,ratioFinalErr])
		if isDisplaced:
			for ctau in ['10','100','1000']:
				exec("tree = t_"+channel+"CTau"+ctau+"uujj"+str(plotmass))
				noSelInt  = QuickIntegral(tree,selectionNoSel,1.0)
				preselInt = QuickIntegral(tree,selectionFinal,1.0)
				ratioFinal = preselInt[0]/noSelInt[0]
				if preselInt[0]>0:
					ratioFinalErr = (preselInt[0]/noSelInt[0])*math.sqrt((preselInt[1]**2)/(preselInt[0]**2)+(noSelInt[1]**2)/(noSelInt[0]**2))
				else : 
					ratioFinalErr = 0.0
				exec("ratiosFinalCTau"+ctau+".append([ratioFinal,ratioFinalErr])")
		ratiosPresel.append([ratioPresel,ratioPreselErr])
		if isDisplaced:
			for ctau in ['10','100','1000']:
				exec("tree = t_"+channel+"CTau"+ctau+"uujj"+str(plotmass))
				noSelInt  = QuickIntegral(tree,selectionNoSel,1.0)
				preselInt = QuickIntegral(tree,selectionPresel,1.0)
				ratioPresel = preselInt[0]/noSelInt[0]
				if preselInt[0]>0:
					ratioPreselErr = (preselInt[0]/noSelInt[0])*math.sqrt((preselInt[1]**2)/(preselInt[0]**2)+(noSelInt[1]**2)/(noSelInt[0]**2))
				else : 
					ratioPreselErr = 0.0
				exec("ratiosPreselCTau"+ctau+".append([ratioPresel,ratioPreselErr])")
		if massBins==0: lowMass=plotmass
		massBins=massBins+1
	if isDisplaced : binWidth=50
	else : binWidth=25
	ratHistFinal = TH1F("ratHistFinal","ratHistFinal",massBins,lowMass-binWidth,highMass+binWidth)
	if isDisplaced : 
		ratHistFinal.GetXaxis().SetTitle("#tilde{t} Mass [GeV]")
		ratHistFinalCtau10 = TH1F("ratHistFinalCTau10","ratHistFinalCTau10",massBins,lowMass-binWidth,highMass+binWidth)
		ratHistFinalCTau10.GetXaxis().SetTitle("#tilde{t} Mass [GeV]")
		ratHistFinalCTau10.SetLineColor(kRed)
		ratHistFinalCtau100 = TH1F("ratHistFinalCTau100","ratHistFinalCTau100",massBins,lowMass-binWidth,highMass+binWidth)
		ratHistFinalCTau100.GetXaxis().SetTitle("#tilde{t} Mass [GeV]")
		ratHistFinalCTau100.SetLineColor(kBlue)
		ratHistFinalCtau1000 = TH1F("ratHistFinalCTau1000","ratHistFinalCTau1000",massBins,lowMass-binWidth,highMass+binWidth)
		ratHistFinalCTau1000.GetXaxis().SetTitle("#tilde{t} Mass [GeV]")
		ratHistFinalCTau1000.SetLineColor(kGreen)
	else : ratHistFinal.GetXaxis().SetTitle("LQ Mass [GeV]")
	ratHistFinal.GetYaxis().SetTitle("Acceptance*Efficiency")
	ratHistPresel = TH1F("ratHistPresel","ratHistPresel",massBins,lowMass-binWidth,highMass+binWidth)
	if isDisplaced : 
		ratHistPresel.GetXaxis().SetTitle("#tilde{t} Mass [GeV]")
		ratHistPreselCTau10 = TH1F("ratHistPreselCTau10","ratHistPreselCTau10",massBins,lowMass-binWidth,highMass+binWidth)
		ratHistPreselCTau10.GetXaxis().SetTitle("#tilde{t} Mass [GeV]")
		ratHistPreselCTau10.SetLineColor(kRed)
		ratHistPreselCTau100 = TH1F("ratHistPreselCTau100","ratHistPreselCTau100",massBins,lowMass-binWidth,highMass+binWidth)
		ratHistPreselCTau100.GetXaxis().SetTitle("#tilde{t} Mass [GeV]")
		ratHistPreselCTau100.SetLineColor(kBlue)
		ratHistPreselCTau1000 = TH1F("ratHistPreselCTau1000","ratHistPreselCTau1000",massBins,lowMass-binWidth,highMass+binWidth)
		ratHistPreselCTau1000.GetXaxis().SetTitle("#tilde{t} Mass [GeV]")
		ratHistPreselCTau1000.SetLineColor(kGreen)
	else : ratHistPresel.GetXaxis().SetTitle("LQ Mass [GeV]")
	ratHistPresel.GetYaxis().SetTitle("Preselection Acceptance*Efficiency")
	for bin in range(massBins):
		ratHistFinal.SetBinContent(bin+1,ratiosFinal[bin][0])
		ratHistFinal.SetBinError(bin+1,ratiosFinal[bin][1])
		if isDisplaced : 
			ratHistFinalCTau10.SetBinContent(bin+1,ratiosFinalCTau10[bin][0])
			ratHistFinalCTau10.SetBinError(bin+1,ratiosFinalCTau10[bin][1])
			ratHistFinalCTau100.SetBinContent(bin+1,ratiosFinalCTau100[bin][0])
			ratHistFinalCTau100.SetBinError(bin+1,ratiosFinalCTau100[bin][1])
			ratHistFinalCTau1000.SetBinContent(bin+1,ratiosFinalCTau1000[bin][0])
			ratHistFinalCTau1000.SetBinError(bin+1,ratiosFinalCTau1000[bin][1])
		ratHistPresel.SetBinContent(bin+1,ratiosPresel[bin][0])
		ratHistPresel.SetBinError(bin+1,ratiosPresel[bin][1])
		if isDisplaced : 
			ratHistPreselCTau10.SetBinContent(bin+1,ratiosPreselCTau10[bin][0])
			ratHistPreselCTau10.SetBinError(bin+1,ratiosPreselCTau10[bin][1])
			ratHistPreselCTau100.SetBinContent(bin+1,ratiosPreselCTau100[bin][0])
			ratHistPreselCTau100.SetBinError(bin+1,ratiosPreselCTau100[bin][1])
			ratHistPreselCTau1000.SetBinContent(bin+1,ratiosPreselCTau1000[bin][0])
			ratHistPreselCTau1000.SetBinError(bin+1,ratiosPreselCTau1000[bin][1])
	gStyle.SetOptStat(0)
	if isDisplaced : ratHistFinal.GetYaxis().SetRangeUser(0,max(x for [x,y] in ratiosFinal)*1.1)
	else: ratHistFinal.GetYaxis().SetRangeUser(min(x for [x,y] in ratiosFinal)*.9,max(x for [x,y] in ratiosFinal)*1.1)
	ratHistFinal.Draw()
	if isDisplaced : 
		ratHistFinalCTau10.Draw("SAMES")
		ratHistFinalCTau100.Draw("SAMES")
		ratHistFinalCTau1000.Draw("SAMES")
	c1.Print('Results_'+version_name+'/signalAcceptanceTimesEfficiency_'+channel+'_FinalSel.pdf')
	print 'Saving histogram: Results_'+version_name+'/signalAcceptanceTimesEfficiency_'+channel+'_FinalSel.pdf'

	if isDisplaced : ratHistPresel.GetYaxis().SetRangeUser(0,max(x for [x,y] in ratiosPresel)*1.1)
	else : ratHistPresel.GetYaxis().SetRangeUser(min(x for [x,y] in ratiosPresel)*.9,max(x for [x,y] in ratiosPresel)*1.1)
	ratHistPresel.Draw()
	if isDisplaced : 
		ratHistPreselCTau10.Draw("SAMES")
		ratHistPreselCTau100.Draw("SAMES")
		ratHistPreselCTau1000.Draw("SAMES")
	c1.Print('Results_'+version_name+'/signalAcceptanceTimesEfficiency_'+channel+'_Presel.pdf')
	print 'Saving histogram: Results_'+version_name+'/signalAcceptanceTimesEfficiency_'+channel+'_Presel.pdf'


def MakeBasicPlot(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,cutlog,version_name,plotmass):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	# Create Canvas
	yaxismin = .13333
	perc = 0.0
	betamarker = '#beta = '
	isDisplaced=False
	#if 'cosThetaStar' in recovariable: doLog=False
	#else: doLog=True
	doLog=True
	if channel == 'uujj' or channel == 'HHres':
		syslist = totunc_uujj	
		betamarker +="1.0"
	if channel == 'uvjj':
		syslist = totunc_uvjj
		betamarker +="0.5"

	if channel == 'susy':
		plotmass = 500
		print "SUSY TESTS: Using only mass of",plotmass

	if channel == 'displaced':
		isDisplaced=True
		channel='uujj'
		#plotmass = 200
		#print "Displaced SUSY TESTS: Using only mass of",plotmass

	if 'PAS' not in tagname:
		c1 = TCanvas("c1","",800,800)
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.4, 1.0, 1.0 )#divide canvas into pads
		pad2 = TPad( 'pad2', 'pad2', 0.0, 0.26, 1.0, 0.4 )
		pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.26 )
		pad1.Draw()
		pad2.Draw()
		pad3.Draw()
		pad1.SetBottomMargin(0.0)		
		pad2.SetTopMargin(0.0)
		pad3.SetTopMargin(0.0)
		pad2.SetBottomMargin(0.0)
		pad3.SetBottomMargin(0.43)
	else:
		# if 'final' not in tagname:
		c1 = TCanvas("c1","",800,550)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		perc = 5.0
		for m in range(len(pdf_MASS)):
			if str(pdf_MASS[m]) in str(plotmass):
				perc = syslist[m]


		# else:
		# 	c1 = TCanvas("c1","",800,650)					
		# 	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.35, 1.0, 1.0 )#divide canvas into pads
		# 	pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.35 )
		# 	pad1.Draw()
		# 	pad3.Draw()
		# 	pad1.SetBottomMargin(0.0)		
		# 	pad3.SetTopMargin(0.0)
		# 	pad3.SetBottomMargin(0.43)	
		# 	perc = 30.0

	print 'Defining systematic band with percent uncertainty:',perc,'%'

	gStyle.SetOptStat(0)


	pad1.cd()
	# pad1.SetGrid()
	# These are the style parameters for certain plots - [FillStyle,MarkerStyle,MarkerSize,LineWidth,Color]
	MCRecoStyle=[0,20,.00001,1,4]
	DataRecoStyle=[0,20,1.5,1,1]
	# X and Y axis labels for plot
	Label=[xlabel,"Events / bin"]

	WStackStyle=[3007,20,.00001,1,6]
	TTStackStyle=[3005,20,.00001,1,4]
	ZStackStyle=[3004,20,.00001,1,2]
	DiBosonStackStyle=[3006,20,.00001,1,3]
	StopStackStyle=[3008,20,.00001,1,7]
	QCDStackStyle=[3013,20,.00001,1,15]
	SMHiggsStackStyle=[3008,20,.00001,1,800]


	SignalStyle=[0,22,0.7,4,28]
	SignalStyle2=[0,22,0.7,4,38]
	SignalStyle3=[0,22,0.7,4,48]
	SignalStyle4=[0,22,0.7,4,58]

	bgbandstyle=[3002,20,.00001,0,14]

	#channel = HHres
	print 'Getting Final sel '
	if 'final' in tagname:
		print 'cat '+cutlog+' | grep '+channel+str(plotmass)
 		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		print 'found'
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+selection+fsel+')'
		print 'parsed'
		# print selection

	##############################################################################
	#######      Top Left Plot - Normal Stacked Distributions              #######
	##############################################################################
	c1.cd(1)
	# print 'Projecting trees...  ',

	tt_sel_weight = selection+'*('+str(ttscale)+')*'+weight

	print 'Choosing sample...',

	t_W = t_WJetsJBin
	t_Z = t_ZJetsJBin
	t_T = t_TTBarDBin
	selectionMod=selection
	if 'ScaleUp' in tagname:
		print 'ScaleUp'
		#t_W = t_WJetsScaleUp
		#t_T = t_TTJetsScaleDown
		#t_Z = t_ZJetsScaleUp
		selectionMod=selection+'*scaleWeight_Up'

	elif 'ScaleDown' in tagname:
		print 'ScaleDown'
		#t_W = t_WJetsScaleDown
		#t_T = t_TTJetsScaleDown
		#t_Z = t_ZJetsScaleDown
		selectionMod=selection+'*scaleWeight_Down'

	elif 'MatchUp' in tagname:
		print 'MatchUp'
		#t_W = t_WJetsMatchUp
		#t_T = t_TTJetsMatchUp
		#t_Z = t_ZJetsMatchUp
		selectionMod=selection+'*scaleWeight_Up'#fixme todo update for matching

	elif 'MatchDown' in tagname:
		print "MatchDown"
		#t_W = t_WJetsMatchDown
		#t_T = t_TTJetsMatchDown	
		#t_Z = t_ZJetsMatchDown
		selectionMod=selection+'*scaleWeight_Down'#fixme todo update for matching

	else:
		print "Regular"
		t_W = t_WJetsJBin
		t_Z = t_ZJetsJBin
		print 'USING STANDARD W'
		if 'TTBarDataDriven' not in tagname:
			t_T = t_TTBarDBin
			print 'Using Decay-binned ttbar MC.'
		else:
			t_T = te_DoubleMuData
			tt_sel_weight = selection + dataHLT + dataHLTEMUADJ
			print 'Using emu data for ttbar est.'

		# t_T = t_TTPowheg

	print 'Doing Projections'
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',t_W,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',t_DoubleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',t_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',t_Z,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	print 'Doing ttbar:'
	print selection+'*('+str(ttscale)+')*'+weight
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',t_T,recovariable,presentationbinning,tt_sel_weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',t_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)
	hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD',t_QCDMu,recovariable,presentationbinning,selection+'*'+weight,QCDStackStyle,Label)
	hs_rec_SMHiggs=CreateHisto('hs_rec_SMHiggs','SM Higgs',t_SMHiggs,recovariable,presentationbinning,selection+'*'+weight,SMHiggsStackStyle,Label)

	if 'TTBarDataDriven' in tagname:

		hs_emu_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',te_WJetsJBin,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+NormalWeightEMuNoHLT,WStackStyle,Label)
		hs_emu_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,DiBosonStackStyle,Label)
		hs_emu_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',te_ZJetsJBin,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+NormalWeightEMuNoHLT,ZStackStyle,Label)
		hs_emu_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',te_SingleTop,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,StopStackStyle,Label)
		hs_emu_rec_WJets.Scale(-1.0)
		hs_emu_rec_DiBoson.Scale(-1.0)
		hs_emu_rec_ZJets.Scale(-1.0)
		hs_emu_rec_SingleTop.Scale(-1.0)
		hs_rec_TTBar.Add(hs_emu_rec_WJets)
		hs_rec_TTBar.Add(hs_emu_rec_DiBoson)
		hs_rec_TTBar.Add(hs_emu_rec_ZJets)
		hs_rec_TTBar.Add(hs_emu_rec_SingleTop)
		hs_rec_TTBar.Scale(emu_id_eff)



	sig1name = ''
	sig2name = ''

	if channel == 'uujj' or 'HH' in channel:
		sig1name = 'M_{R}=300 (1 pb)'#+betamarker
		sig2name = 'M_{R}=900 (1 pb)'#+betamarker
		#sig2name = 'LQ, M = 950 GeV, '+betamarker
		if 'final' not in tagname:
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_HHres300,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_HHres900,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
			print 'signal1,',sig1name,':',hs_rec_Signal.Integral()
			print 'signal2,',sig2name,':',hs_rec_Signal2.Integral()
			hs_rec_Signal.Scale(1000.)
			hs_rec_Signal2.Scale(1000.)
		if 'final' in tagname:
			#exec ("_stree = t_LQ"+channel+str(plotmass))
			exec ("_stree = t_HHres"+str(plotmass))
			hs_rec_Signal=CreateHisto('hs_rec_Signal','LQ, M = '+str(plotmass)+' GeV, '+betamarker,_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			print 'signal1,',sig1name,':',hs_rec_Signal.Integral()

		wErr=zErr=vvErr=ttErr=stErr=qcdErr=smHErr=Double(0.)
		wInt=hs_rec_WJets.IntegralAndError(0,-1,wErr)
		zInt=hs_rec_ZJets.IntegralAndError(0,-1,zErr)
		vvInt=hs_rec_DiBoson.IntegralAndError(0,-1,vvErr)
		ttInt=hs_rec_TTBar.IntegralAndError(0,-1,ttErr)
		stInt=hs_rec_SingleTop.IntegralAndError(0,-1,stErr)
		SMHInt=hs_rec_SMHiggs.IntegralAndError(0,-1,smHErr)
		qcdInt=hs_rec_QCD.IntegralAndError(0,-1,qcdErr)
		totBg = wInt+zInt+vvInt+ttInt+stInt+SMHInt+qcdInt
		totErr = math.sqrt(wErr**2+zErr**2+vvErr**2+ttErr**2+stErr**2+smHErr**2+qcdErr**2)

		print 'W:   ',wInt#hs_rec_WJets.Integral()
		print 'Z:   ',zInt#hs_rec_ZJets.Integral()
		print 'VV:  ',vvInt#hs_rec_DiBoson.Integral()
		print 'TT:  ',ttInt#hs_rec_TTBar.Integral()
		print 'ST:  ',stInt#hs_rec_SingleTop.Integral()
		print 'QCD: ',qcdInt#,'NOT USED'#hs_rec_SingleTop.Integral()
		print 'SM H:',SMHInt
		print 'Total Background:',totBg,'+-',totErr
		print 'Data            :',hs_rec_Data.Integral()

		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		hs_rec_DiBoson.Add(hs_rec_QCD)
		SM=[hs_rec_SMHiggs,hs_rec_DiBoson,hs_rec_ZJets,hs_rec_TTBar]

	if channel == 'susy':
		sig1name = 'LQ, M = 500 GeV'
		sig2name = 'RPV Susy, M = 500 GeV'
		if 'final' not in tagname:
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_LQuujj500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_Susy500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
		if 'final' in tagname:
			exec ("_stree = t_LQ"+channel+str(plotmass))
			hs_rec_Signal=CreateHisto('hs_rec_Signal','LQ, M = '+str(plotmass)+' GeV',_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)

		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_SMHiggs,hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets]

	if isDisplaced:
		sig1name = '#tilde{t}, M = 200 GeV, c#tau=0.1 cm'
		sig2name = '#tilde{t}, M = 500 GeV, c#tau=1 cm'
		if 'final' not in tagname:
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_BLCTau1uujj200,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_BLCTau10uujj500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
			print 'signal1,',sig1name,':',hs_rec_Signal.Integral()
			print 'signal2,',sig2name,':',hs_rec_Signal2.Integral()
		if 'final' in tagname:
			exec ("_stree  = t_BL"+channel+str(plotmass)+'CTau1')
			exec ("_stree2 = t_BL"+channel+str(plotmass)+'CTau10')
			exec ("_stree3 = t_BL"+channel+str(plotmass)+'CTau100')
			exec ("_stree4 = t_BL"+channel+str(plotmass)+'CTau1000')
			hs_rec_Signal=CreateHisto('hs_rec_Signal','#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=0.1 cm',_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2','#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=1 cm',_stree2,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
			hs_rec_Signal3=CreateHisto('hs_rec_Signal3','#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=10 cm',_stree3,recovariable,presentationbinning,selection+'*'+weight,SignalStyle3,Label)
			hs_rec_Signal4=CreateHisto('hs_rec_Signal4','#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=100 cm',_stree4,recovariable,presentationbinning,selection+'*'+weight,SignalStyle4,Label)
			print 'signal1,',sig1name,':',hs_rec_Signal.Integral()

		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets]

	if channel == 'uvjj':
		if 'final' not in tagname:	
			sig1name = 'LQ, M = 650 GeV, '+betamarker
			sig2name = 'LQ, M = 950 GeV, '+betamarker
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_LQuvjj650,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_LQuvjj950,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
		if 'final' in tagname:
			exec ("_stree = t_LQ"+channel+str(plotmass))
			hs_rec_Signal=CreateHisto('hs_rec_Signal','LQ, M = '+str(plotmass)+' GeV, '+betamarker,_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
	
		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)		
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_WJets]
	
	sigErr=Double(0.)
	sigInt = hs_rec_Signal.IntegralAndError(0,-1,sigErr)
	print 'Signal M='+str(plotmass)+'    :',sigInt,'+-',sigErr

	bgcont = []
	dcont = []
	bgconterr = []

	hs_bgband=CreateHisto('hs_bgband','bgband',t_SingleTop,recovariable,presentationbinning,'(0)',bgbandstyle,Label)
	for x in SM:
		hs_bgband.Add(x)


	# print presentationbinning
	for nn in range(SM[0].GetNbinsX()):
		n = nn + 1
		lhs = SM[0].GetBinCenter(n) - 0.5*SM[0].GetBinWidth(n)
		rhs = SM[0].GetBinCenter(n) + 0.5*SM[0].GetBinWidth(n)
		cont = 0.0
		conterr = 0.0
		for ss in SM:
			cont += ss.GetBinContent(n)
			conterr += ss.GetBinError(n)*ss.GetBinError(n)
		conterr = math.sqrt(conterr)
		# print lhs, rhs, cont
		bgcont.append(cont)
		bgconterr.append(conterr)
		dcont.append(hs_rec_Data.GetBinContent(n))


	# sysbandX = []
	# sysbandY = []
	# sysbandYaddon = []
	# sysbandXaddon = []

	# sysratbandX = []
	# sysratbandY = []
	# sysratbandYaddon = []
	# sysratbandXaddon = []


	# for c in range(len(bgcont)):
	# 	_err = math.sqrt(((perc*0.01)*bgcont[c])**2 + bgconterr[c]**2)

		# sysbandX.append(presentationbinning[c])
		# sysbandX.append(presentationbinning[c+1])
		# sysbandXaddon.append(presentationbinning[c])
		# sysbandXaddon.append(presentationbinning[c+1])

		# sysbandY.append(bgcont[c]+_err)
		# sysbandY.append(bgcont[c]+_err)
		# sysbandYaddon.append(bgcont[c]-_err)
		# sysbandYaddon.append(bgcont[c]-_err)

		# sysratbandX.append(presentationbinning[c])
		# sysratbandX.append(presentationbinning[c+1])
		# sysratbandXaddon.append(presentationbinning[c])
		# sysratbandXaddon.append(presentationbinning[c+1])

		# rat = 1.0
		# invrat = 1.0
		# if bgcont[c] > 0.0:
		# 	rat = (bgcont[c] + _err)/bgcont[c]
		# 	invrat = (bgcont[c] - _err)/bgcont[c]
		# sysratbandY.append(rat)
		# sysratbandY.append(rat)
		# sysratbandYaddon.append(invrat)
		# sysratbandYaddon.append(invrat)

	for c in range(hs_bgband.GetNbinsX()+1):
		_err = math.sqrt( (hs_bgband.GetBinError(c))**2 + (perc*0.01*hs_bgband.GetBinContent(c))**2 )
		hs_bgband.SetBinError(c,_err)
		if hs_bgband.GetBinContent(c) < 0.0001:
			hs_bgband.SetBinContent(c,0.0)
			hs_bgband.SetBinError(c,0.0)

	# print sysbandY

	# for y in range(len(sysbandY)):
	# 	if sysbandY[y] < yaxismin:
	# 		sysbandY[y] = yaxismin

	# print sysbandY


	# sysbandYaddon.reverse()
	# sysbandYaddon.reverse()
	# sysratbandYaddon.reverse()
	# sysratbandYaddon.reverse()

	# for x in sysbandYaddon:
	# 	sysbandY.append(x)

	# for x in sysbandXaddon:
	# 	sysbandX.append(x)

	# for x in sysratbandYaddon:
	# 	sysratbandY.append(x)

	# for x in sysratbandXaddon:
	# 	sysratbandX.append(x)


	# sysbandX = array("d",sysbandX)
	# sysbandY = array("d",sysbandY)
	# sysratbandX = array("d",sysratbandX)
	# sysratbandY = array("d",sysratbandY)


	# sysTop =  TPolyLine(len(sysbandY),sysbandX,sysbandY,"")
	# sysTop.SetLineColor(14)
	# sysTop.SetFillColor(14)
	# sysTop.SetFillStyle(3002)

	# sysBot =  TPolyLine(len(sysratbandY),sysratbandX,sysratbandY,"")
	# sysBot.SetLineColor(14)
	# sysBot.SetFillColor(14)
	# sysBot.SetFillStyle(3002)


	# mcdatascalepres = (1.0*(hs_rec_Data.GetEntries()))/(sum(k.Integral() for k in SM))

	MCStack = THStack ("MCStack","")
	SMIntegral = sum(k.Integral() for k in SM)
	# print SMIntegral
	# print hs_rec_Data.Integral(), hs_rec_Data.GetEntries()
	# MCStack.SetMaximum(SMIntegral*100)
	
	print 'Stacking...  ',	
	for x in SM:
		# x.Scale(mcdatascalepres)
		MCStack.Add(x)
		if doLog: x.SetMaximum(10*hs_rec_Data.GetMaximum())
		else: x.SetMaximum(SMIntegral/44.)

	if not doLog: 
		MCStack.SetMaximum(SMIntegral/44.)
		print 'Must be cosThetaStar! Setting max to ',SMIntegral/44.
	MCStack.Draw("HIST")
	c1.cd(1)
	if doLog: c1.cd(1).SetLogy()

 	# sysTop->Draw("L");


	MCStack=BeautifyStack(MCStack,Label)
	hs_rec_Signal.Draw("HISTSAME")
	if 'final' not in tagname:
		hs_rec_Signal2.Draw("HISTSAME")
 	if 'PAS' in tagname and 'final' in tagname:
		# sysTop.Draw("F")
		hs_bgband.Draw("E2SAME")
	if 'final' in tagname and isDisplaced:
		hs_rec_Signal2.Draw("HISTSAME")
		hs_rec_Signal3.Draw("HISTSAME")
		hs_rec_Signal4.Draw("HISTSAME")
	#setZeroBinErrors(hs_rec_Data,MCStack)
	#hs_rec_Data.Draw("E0PSAME")
	hs_rec_Data_tgraph = TGraphAsymmErrors(hs_rec_Data)
	if 'final' not in tagname:
		setZeroBinErrors_tgraph(hs_rec_Data,hs_rec_Data_tgraph,MCStack,hs_rec_Signal,hs_rec_Signal2)
	else:
	       	setZeroBinErrors_tgraph(hs_rec_Data,hs_rec_Data_tgraph,MCStack,hs_rec_Signal,hs_rec_Signal)

	hs_rec_Data_tgraph.Draw("ZE0PSAME")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	if 'final' not in tagname:
		leg = TLegend(0.52,0.475,0.98,0.89,"","brNDC");	
	else: 
		leg = TLegend(0.45,0.55,0.91,0.9,"","brNDC");	
	# leg = TLegend(0.53,0.52,0.89,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetFillStyle(0);
	leg.SetBorderSize(0);
	if 'final' not in tagname:
		leg.SetTextSize(.05)
	else:
		leg.SetTextSize(.045)
	leg.AddEntry(hs_rec_Data,"Data","lpe");
	leg.AddEntry(hs_rec_TTBar,'t#bar{t}' + (' (e #mu est)')*('TTBarDataDriven' in tagname))
	if channel=='uujj' or 'HH' in channel:
		leg.AddEntry(hs_rec_ZJets,'Z/^{}#gamma* + jets')
	if channel=='uvjj':
		leg.AddEntry(hs_rec_WJets,'W + jets')
	leg.AddEntry(hs_rec_DiBoson,'Other background')
	leg.AddEntry(hs_rec_SMHiggs,'SM Higgs')
	if 'final' not in tagname:
		#leg.AddEntry("", "", "");
		leg.AddEntry("", "gg#rightarrow R#rightarrow HH#rightarrow bbZZ", "");
		leg.AddEntry(hs_rec_Signal,sig1name,"l")
		leg.AddEntry(hs_rec_Signal2,sig2name,"l")
	else:
		if 'PAS' in tagname:
			leg.AddEntry(hs_bgband,'Unc. (stat + syst)')
		if isDisplaced:
			leg.AddEntry(hs_rec_Signal, '#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=0.1 cm1',"l")
			leg.AddEntry(hs_rec_Signal2,'#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=1 cm',"l")
			leg.AddEntry(hs_rec_Signal3,'#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=10 cm',"l")
			leg.AddEntry(hs_rec_Signal4,'#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=100 cm',"l")
		else:
			leg.AddEntry(hs_rec_Signal,'LQ, M = '+str(plotmass)+' GeV, '+betamarker,"l")
	leg.Draw()

	sqrts = "#sqrt{s} = 13 TeV";
	l1=TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.06)
	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(62)
	l2.SetNDC()
	l2.SetTextSize(0.08)
 
	if  'PAS' in tagname and 'tagfree' not in tagname:
		#l1.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                        35.9 fb^{-1} (13 TeV)")
		#l1.DrawLatex(0.64,0.94,"5 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	else:
		#l1.DrawLatex(0.18,0.94,"                          "+sqrts+", 225.57 pb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                        35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")


	# l1.DrawLatex(0.13,0.76,sqrts)

	# l2=TLatex()
	# l2.SetTextAlign(12)
	# l2.SetTextFont(42)
	# l2.SetNDC()
	# l2.SetTextSize(0.06)
	# # l2.SetTextAngle(45);	
	# l2.DrawLatex(0.15,0.83,"PRELIMINARY")

	gPad.Update()
	gPad.RedrawAxis()

	MCStack.SetMinimum(yaxismin)
	if doLog: MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())
	else: 
		MCStack.SetMaximum(SMIntegral/44.)

	if 'control' in tagname:
		MCStack.SetMaximum(100000*hs_rec_Data.GetMaximum())
	if 'St' in recovariable:
		MCStack.SetMaximum(250*hs_rec_Data.GetMaximum())

	resstring = ''
	if 'PAS' not in tagname:

		pad2.cd()
		# pad2.SetLogy()
		pad2.SetGrid()

		RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)

		RatHistDen.Sumw2()
		RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
		RatHistNum.Sumw2()
		for hmc in SM:
			RatHistDen.Add(hmc)

		RatHistNum.Add(hs_rec_Data)
		RatHistNum.Divide(RatHistDen)
		# for x in RatHistNum.GetNbinsX():
		# 	print RatHistNum.GetBinCenter(x), RatHistNum.GetBinContent(x)

		RatHistNum.SetMaximum(1.599)#fixme was 1.499
		RatHistNum.SetMinimum(0.401)#fixme was 0.501


		RatHistNum.GetYaxis().SetTitleFont(42);
		RatHistNum.GetXaxis().SetTitle('');
		RatHistNum.GetYaxis().SetTitle('Data/MC');
		RatHistNum.GetXaxis().SetTitle(xlabel)

		RatHistNum.GetYaxis().SetTitleFont(42);
		RatHistNum.GetXaxis().SetTitle('');
		RatHistNum.GetYaxis().SetTitle('Data/MC');
		RatHistNum.GetYaxis().SetNdivisions(308,True)

		RatHistNum.GetXaxis().SetTitleSize(0.);
		RatHistNum.GetYaxis().SetTitleSize(.20);
		RatHistNum.GetXaxis().CenterTitle();
		RatHistNum.GetYaxis().CenterTitle();		
		RatHistNum.GetXaxis().SetTitleOffset(.28);
		RatHistNum.GetYaxis().SetTitleOffset(.18);
		RatHistNum.GetYaxis().SetLabelSize(.15);
		RatHistNum.GetXaxis().SetLabelSize(.09);

		#blind(RatHistNum)#fixme
		RatHistNum.Draw()

	
		RatHistDen.SetMarkerSize(0)
		RatHistDen.SetFillColor(17)
		RatHistDen.SetFillStyle(3105)
		for bin in range(RatHistDen.GetNbinsX()+1) :
			if bin==0: continue
			x = RatHistDen.GetBinContent(bin)
			err = RatHistDen.GetBinError(bin)
			if x==0: err=0
			else: err = err/x
			RatHistDen.SetBinError(bin,err)
			RatHistDen.SetBinContent(bin,1)
		#RatHistDen.Draw("E2SAMES")
		RatHistNum.Draw("SAMES")

		unity=TLine(RatHistNum.GetXaxis().GetXmin(), 1.0 , RatHistNum.GetXaxis().GetXmax(),1.0)
		unity.Draw("SAME")	


		pad3.cd()
		# pad2.SetLogy()
		pad3.SetGrid()

		chiplot =CreateHisto('chiplot','chiplot',t_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
		chiplot.Sumw2()

		resstring = '( 0.0 '

		for n in range(chiplot.GetNbinsX()+1):
			lhs = chiplot.GetBinCenter(n) - 0.5*chiplot.GetBinWidth(n)
			rhs = chiplot.GetBinCenter(n) + 0.5*chiplot.GetBinWidth(n)
			lhs = str(round(lhs,3))
			rhs = str(round(rhs,3))

			bg = 0
			bgerr = 0
			dat = hs_rec_Data.GetBinContent(n)
			daterr = math.sqrt(1.0*dat)
			for hmc in SM:
				bg += hmc.GetBinContent(n)
				bgerr += hmc.GetBinError(n)*hmc.GetBinError(n)
			bgerr = math.sqrt(bgerr)
			total_err = math.sqrt(bgerr*bgerr+daterr*daterr)
			
			resfac = '1.0'

			if total_err>0: 
				chi = (dat - bg)/total_err
				chiplot.SetBinContent(n,chi)
				chiplot.SetBinError(n,0.0)
			if bg > 0 and dat > 0:
				resfac = str(round(dat/bg,3))
			if n != 0:
				resstring += ' + '+resfac+'*('+recovariable +'>'+lhs+')'+'*('+recovariable +'<='+rhs+')'

		resstring += ')'
		if recovariable =='Phi_miss':
			print resstring

		chiplot.SetMaximum(5.99)
		chiplot.SetMinimum(-5.99)

		chiplot.GetYaxis().SetTitleFont(42);
		# chiplot.GetXaxis().SetTitle('');
		chiplot.GetYaxis().SetTitle('#chi (Data,MC)');
		# chiplot.GetXaxis().SetTitle('#chi (Data,MC)');


		chiplot.GetXaxis().SetTitleSize(.14);
		chiplot.GetYaxis().SetTitleSize(.10);
		chiplot.GetXaxis().CenterTitle();
		chiplot.GetYaxis().CenterTitle();		
		chiplot.GetXaxis().SetTitleOffset(.8);
		chiplot.GetYaxis().SetTitleOffset(.34);
		chiplot.GetYaxis().SetLabelSize(.09);
		chiplot.GetXaxis().SetLabelSize(.09);

		#blind(chiplot)
		chiplot.Draw('EP')
		zero=TLine(RatHistNum.GetXaxis().GetXmin(), 0.0 , RatHistNum.GetXaxis().GetXmax(),0.0)
		plus2=TLine(RatHistNum.GetXaxis().GetXmin(), 2.0 , RatHistNum.GetXaxis().GetXmax(),2.0)
		minus2=TLine(RatHistNum.GetXaxis().GetXmin(), -2.0 , RatHistNum.GetXaxis().GetXmax(),-2.0)
		plus2.SetLineColor(2)
		minus2.SetLineColor(2)

		plus2.Draw("SAME")
		minus2.Draw("SAME")
		zero.Draw("SAME")	



	if 'PAS' in tagname and 'final' in tagname and False:

		pad3.cd()
		pad3.SetLogy()
		pad3.SetGrid()

		RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)

		RatHistDen.Sumw2()
		RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
		RatHistNum.Sumw2()
		for hmc in SM:
			RatHistDen.Add(hmc)

		RatHistNum.Add(hs_rec_Data)
		RatHistNum.Divide(RatHistDen)
		ratmax = 1.999
		for x in (range(RatHistNum.GetNbinsX())):
			_top = RatHistNum.GetBinContent(x+1) + RatHistNum.GetBinError(x+1)
			if _top > ratmax:
				ratmax = _top
				ratmax = 1.05*ratmax

		RatHistNum.SetMaximum(ratmax)
		RatHistNum.SetMinimum(0.1)


		RatHistNum.GetYaxis().SetTitleFont(42);
		RatHistNum.GetXaxis().SetTitle('');
		RatHistNum.GetYaxis().SetTitle('Data/MC');
		RatHistNum.GetXaxis().SetTitle(xlabel)

		RatHistNum.GetXaxis().SetTitleFont(42)
		RatHistNum.GetYaxis().SetTitleFont(42)
		RatHistNum.GetXaxis().SetLabelFont(42)
		RatHistNum.GetYaxis().SetLabelFont(42)
		RatHistNum.GetXaxis().SetLabelOffset(0.007)
		RatHistNum.GetYaxis().SetLabelOffset(0.007)
		RatHistNum.GetXaxis().SetLabelSize(0.08)
		RatHistNum.GetYaxis().SetLabelSize(0.08)

		RatHistNum.GetXaxis().SetTitleOffset(0.92)
		RatHistNum.GetYaxis().SetTitleOffset(0.52)
		RatHistNum.GetXaxis().SetTitleSize(0.12)
		RatHistNum.GetYaxis().SetTitleSize(0.10)
		RatHistNum.GetXaxis().CenterTitle(1)
		RatHistNum.GetYaxis().CenterTitle(1)

		RatHistNum.Draw("")
		# sysBot.Draw("F")		
		RatHistNum.Draw("SAME")

		unity=TLine(RatHistNum.GetXaxis().GetXmin(), 1.0 , RatHistNum.GetXaxis().GetXmax(),1.0)
		unity.Draw("SAME")	


	recovariable = recovariable.replace('/','_DIV_')
	recovariable = recovariable.replace('(','_')
	recovariable = recovariable.replace(')','_')
	
	if 'sqrt(abs(2*Pt_jet1' in recovariable: recovariable = 'M_jj'

	gPad.Update()
	l=TLine()
	#l.DrawLine(gPad.GetUxmax(), gPad.GetUymin(), gPad.GetUxmax(), gPad.GetUymax())
	if 'PAS' not in tagname:
	#	l.DrawLine(pad1.GetUxmax(), pad3.GetUymin(), pad1.GetUxmax(), pad1.GetUymax())
		x=1
	else:
		l.DrawLine(pad1.GetUxmax(), pad1.GetUymin(), pad1.GetUxmax(), pad1.GetUymax())
	print 'Saving as: ',
	if isDisplaced: channel='displaced'
	if 'final' not in tagname:
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.png')
		print 'Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.pdf',
	else:
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf')
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.png')	
		print 'Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf',
	print ' ...Done.'

	return resstring




def MakeBasicPlot2D(recovariableX,recovariableY,xlabel,ylabel,presentationbinningX,presentationbinningY,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,cutlog,version_name,plotmass):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariableY+" vs "+recovariableX+"...  "
	recovariable = recovariableY+'_vs_'+recovariableX
	# Create Canvas
	yaxismin = .13333
	perc = 0.0
	betamarker = '#beta = '
	isDisplaced=False
	if channel == 'uujj':
		syslist = totunc_uujj	
		betamarker +="1.0"

	if 'PAS' not in tagname:
		c1 = TCanvas("c1","",800,620)
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		#pad1.SetBottomMargin(0.0)
	else:
		# if 'final' not in tagname:
		c1 = TCanvas("c1","",800,800)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		perc = 5.0
		for m in range(len(pdf_MASS)):
			if str(pdf_MASS[m]) in str(plotmass):
				perc = syslist[m]

	gStyle.SetOptStat(0)

	pad1.cd()
	# pad1.SetGrid()
	# These are the style parameters for certain plots - [FillStyle,MarkerStyle,MarkerSize,LineWidth,Color]
	MCRecoStyle=[0,20,.00001,1,4]
	DataRecoStyle=[0,20,1.5,1,1]
	# X and Y axis labels for plot
	Label=[xlabel,ylabel]

	WStackStyle=[3007,20,.00001,1,6]
	TTStackStyle=[3005,20,.00001,1,4]
	ZStackStyle=[3004,20,.00001,1,2]
	DiBosonStackStyle=[1,4,.4,1,4]
	StopStackStyle=[3008,20,.00001,1,7]
	QCDStackStyle=[3013,20,.00001,1,15]

	SignalStyle=[0,22,1.2,4,kRed]

	bgbandstyle=[3002,20,.00001,0,14]


	if 'final' in tagname:
		print 'Getting Final sel '
		print 'cat '+cutlog+' | grep '+channel+str(plotmass)
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		print 'found'
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+selection+fsel+')'
		print 'parsed'
		# print selection
	else : print 'Using Preselection'

	##############################################################################
	#######      Top Left Plot - Normal Stacked Distributions              #######
	##############################################################################
	c1.cd(1)
	# print 'Projecting trees...  ',

	tt_sel_weight = selection+'*('+str(ttscale)+')*'+weight

	print 'Choosing sample...',

	t_W = t_WJetsJBin
	t_Z = t_ZJetsJBin
	t_T = t_TTBarDBin
	selectionMod=selection
	if 'ScaleUp' in tagname:
		print 'ScaleUp'
		#t_W = t_WJetsScaleUp
		#t_T = t_TTJetsScaleDown
		#t_Z = t_ZJetsScaleUp
		selectionMod=selection+'*scaleWeight_Up'

	elif 'ScaleDown' in tagname:
		print 'ScaleDown'
		#t_W = t_WJetsScaleDown
		#t_T = t_TTJetsScaleDown
		#t_Z = t_ZJetsScaleDown
		selectionMod=selection+'*scaleWeight_Down'

	elif 'MatchUp' in tagname:
		print 'MatchUp'
		#t_W = t_WJetsMatchUp
		#t_T = t_TTJetsMatchUp
		#t_Z = t_ZJetsMatchUp
		selectionMod=selection+'*scaleWeight_Up'#fixme todo update for matching

	elif 'MatchDown' in tagname:
		print "MatchDown"
		#t_W = t_WJetsMatchDown
		#t_T = t_TTJetsMatchDown	
		#t_Z = t_ZJetsMatchDown
		selectionMod=selection+'*scaleWeight_Down'#fixme todo update for matching

	else:
		print "Regular"
		t_W = t_WJetsJBin
		t_Z = t_ZJetsJBin
		print 'USING STANDARD W'
		if 'TTBarDataDriven' not in tagname:
			t_T = t_TTBarDBin
			print 'Using Decay-binned ttbar MC.'
		else:
			t_T = te_DoubleMuData
			tt_sel_weight = selection + dataHLT + dataHLTEMUADJ
			print 'Using emu data for ttbar est.'

		# t_T = t_TTPowheg

	print 'Doing Projections'
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto2D('hs_rec_WJets','W+Jets',t_W,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto2D('hs_rec_Data','Data',t_DoubleMuData,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto2D('hs_rec_DiBoson','DiBoson',t_DiBoson,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto2D('hs_rec_ZJets','Z+Jets',t_Z,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	print 'Doing ttbar:'
	print selection+'*('+str(ttscale)+')*'+weight
	hs_rec_TTBar=CreateHisto2D('hs_rec_TTBar','t#bar{t}',t_T,recovariableX,recovariableY,presentationbinningX,presentationbinningY,tt_sel_weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto2D('hs_rec_SingleTop','SingleTop',t_SingleTop,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*'+weight,StopStackStyle,Label)
	hs_rec_QCD=CreateHisto2D('hs_rec_QCD','QCD',t_QCDMu,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*'+weight+'*(TrkIso_muon1<0.1)*(TrkIso_muon2<0.1)',QCDStackStyle,Label)

	if 'TTBarDataDriven' in tagname:

		hs_emu_rec_WJets=CreateHisto2D('hs_rec_WJets','W+Jets',te_WJetsJBin,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*('+str(wscale)+')*'+NormalWeightEMuNoHLT,WStackStyle,Label)
		hs_emu_rec_DiBoson=CreateHisto2D('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*'+NormalWeightEMuNoHLT,DiBosonStackStyle,Label)
		hs_emu_rec_ZJets=CreateHisto2D('hs_rec_ZJets','Z+Jets',te_ZJetsJBin,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*('+str(zscale)+')*'+NormalWeightEMuNoHLT,ZStackStyle,Label)
		hs_emu_rec_SingleTop=CreateHisto2D('hs_rec_SingleTop','SingleTop',te_SingleTop,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*'+NormalWeightEMuNoHLT,StopStackStyle,Label)
		hs_emu_rec_WJets.Scale(-1.0)
		hs_emu_rec_DiBoson.Scale(-1.0)
		hs_emu_rec_ZJets.Scale(-1.0)
		hs_emu_rec_SingleTop.Scale(-1.0)
		hs_rec_TTBar.Add(hs_emu_rec_WJets)
		hs_rec_TTBar.Add(hs_emu_rec_DiBoson)
		hs_rec_TTBar.Add(hs_emu_rec_ZJets)
		hs_rec_TTBar.Add(hs_emu_rec_SingleTop)
		hs_rec_TTBar.Scale(emu_id_eff)



	sig1name = ''

	if channel == 'uujj':
		sig1name = '#splitline{gg#rightarrow R#rightarrow HH#rightarrow bbZZ}{M_{R}='+str(plotmass)+'}'#+betamarker
		if 'final' not in tagname:
			exec ("_stree = t_HHres"+str(plotmass))
			print 'using tree:','t_HHres'+str(plotmass)
			selection = selection.replace('*'+str(lumi)+'*weight_central','')
			hs_rec_Signal=CreateHisto2D('hs_rec_Signal',sig1name,_stree,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection,SignalStyle,Label)
			print 'signal1,',sig1name,':',hs_rec_Signal.Integral()
			#hs_rec_Signal.Scale(100.)
		elif 'final' in tagname:
			#exec ("_stree = t_LQ"+channel+str(plotmass))
			exec ("_stree = t_HHres"+str(plotmass))
			hs_rec_Signal=CreateHisto2D('hs_rec_Signal','LQ, M = '+str(plotmass)+' GeV, '+betamarker,_stree,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection,SignalStyle,Label)
			print 'signal1,',sig1name,':',hs_rec_Signal.Integral()

		wErr=zErr=vvErr=ttErr=stErr=qcdErr=Double(0.)
		wInt=hs_rec_WJets.IntegralAndError(0,-1,0,-1,wErr)
		zInt=hs_rec_ZJets.IntegralAndError(0,-1,0,-1,zErr)
		vvInt=hs_rec_DiBoson.IntegralAndError(0,-1,0,-1,vvErr)
		ttInt=hs_rec_TTBar.IntegralAndError(0,-1,0,-1,ttErr)
		stInt=hs_rec_SingleTop.IntegralAndError(0,-1,0,-1,stErr)
		qcdInt=hs_rec_QCD.IntegralAndError(0,-1,0,-1,qcdErr)
		totBg = wInt+zInt+vvInt+ttInt+stInt+qcdInt
		totErr = math.sqrt(wErr**2+zErr**2+vvErr**2+ttErr**2+stErr**2+qcdErr**2)

		print 'W:  ',wInt#hs_rec_WJets.Integral()
		print 'Z:  ',zInt#hs_rec_ZJets.Integral()
		print 'VV: ',vvInt#hs_rec_DiBoson.Integral()
		print 'TT: ',ttInt#hs_rec_TTBar.Integral()
		print 'ST: ',stInt#hs_rec_SingleTop.Integral()
		print 'QCD:',qcdInt#hs_rec_SingleTop.Integral()
		print 'Total Background:',totBg,'+-',totErr
		print 'Data            :',hs_rec_Data.Integral()

		hs_rec_DiBoson.SetTitle("Background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		hs_rec_DiBoson.Add(hs_rec_QCD)
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_TTBar)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets,hs_rec_QCD]

	sigErr=Double(0.)
	sigInt = hs_rec_Signal.IntegralAndError(0,-1,0,-1,sigErr)
	print 'Signal M='+str(plotmass)+'    :',sigInt,'+-',sigErr

	bgcont = []
	dcont = []
	bgconterr = []

	SMIntegral = sum(k.Integral() for k in SM)

	bgTmp,Sig=0.,0.
	SMx,SMy,Sigx,Sigy = 0.,0.,0.,0.
	SMhighx,SMhighy,Sighighx,Sighighy = 0.,0.,0.,0.
	bgTmp  = hs_rec_DiBoson.GetMinimumBin()
	Sig = hs_rec_Signal.GetMinimumBin()
	SMx  = hs_rec_DiBoson.GetXaxis().GetBinCenter(bgTmp)
	Sigx = hs_rec_Signal.GetXaxis().GetBinCenter(Sig)
	SMy  = hs_rec_DiBoson.GetYaxis().GetBinCenter(bgTmp)
	Sigy = hs_rec_Signal.GetYaxis().GetBinCenter(Sig)
	bgTmp  = hs_rec_DiBoson.GetMaximumBin()
	Sig = hs_rec_Signal.GetMaximumBin()
	SMhighx  = hs_rec_DiBoson.GetXaxis().GetBinCenter(bgTmp)
	Sighighx = hs_rec_Signal.GetXaxis().GetBinCenter(Sig)
	SMhighy  = hs_rec_DiBoson.GetYaxis().GetBinCenter(bgTmp)
	Sighighy = hs_rec_Signal.GetYaxis().GetBinCenter(Sig)

	SMbin = hs_rec_DiBoson.GetBinContent(bgTmp)
	hs_rec_DiBoson.GetZaxis().SetRangeUser(0,1.6*bgTmp)
	#hs_rec_DiBoson.GetXaxis().SetRangeUser(0.9*min(SMx,Sigx),1.1*max(SMx,Sigx))
	#hs_rec_DiBoson.GetYaxis().SetRangeUser(0.9*min(SMy,Sigy),1.1*max(SMy,Sigy))
	#hs_rec_DiBoson.GetYaxis().SetMinimum(0.9*min(SMy,Sigy))
	#hs_rec_DiBoson.GetXaxis().SetMaximum(1.1*max(SMx,Sigx))
	#hs_rec_DiBoson.GetYaxis().SetMaximum(1.1*max(SMy,Sigy))

        #gStyle.SetPalette(1,nullptr)
	#hs_rec_DiBoson.SetContour(50)
	hs_rec_DiBoson.Draw("colz")
	hs_rec_Signal.Draw("pSAMES")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	if 'final' not in tagname:
		leg = TLegend(0.45,0.63,0.83,0.79,"","brNDC");	
	else: 
		leg = TLegend(0.45,0.55,0.91,0.9,"","brNDC");	
	# leg = TLegend(0.53,0.52,0.89,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(kWhite);
	leg.SetFillStyle(1001);
	leg.SetBorderSize(1);
	if 'final' not in tagname:
		leg.SetTextSize(.03)
	else:
		leg.SetTextSize(.045)
	#leg.AddEntry(hs_rec_Data,"Data","lpe");
	leg.AddEntry(hs_rec_DiBoson,'SM Backgrounds',"f")
	leg.AddEntry(hs_rec_Signal,sig1name,"p")
	leg.Draw()

	sqrts = "#sqrt{s} = 13 TeV";
	l1=TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.045)
	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(62)
	l2.SetNDC()
	l2.SetTextSize(0.059)
 
	if  'PAS' in tagname and 'tagfree' not in tagname:
		#l1.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.12,0.93,"#it{Preliminary}                                       35.9 fb^{-1} (13 TeV)")
		#l1.DrawLatex(0.64,0.94,"5 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.86,"CMS")
	else:
		#l1.DrawLatex(0.18,0.94,"                          "+sqrts+", 225.57 pb^{-1}")
		l1.DrawLatex(0.125,0.93,"#it{Preliminary}                                            35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.16,0.855,"CMS")

	gPad.Update()
	gPad.RedrawAxis()

	recovariable = recovariable.replace('/','_DIV_')
	recovariable = recovariable.replace('(','_')
	recovariable = recovariable.replace(')','_')
	
	gPad.Update()

	#l=TLine()
	#l.SetLineWidth(2)
	#l.DrawLine(25,10,25,300)
	#l.DrawLine(25,10,140,10)
	#l.DrawLine(140,10,140,300)
	#l.DrawLine(25,300,140,300)

	print 'Saving as: ',
	if 'final' not in tagname:
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'_'+str(plotmass)+'.pdf')
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'_'+str(plotmass)+'.png')
		print 'Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'_'+str(plotmass)+'.pdf',
	else:
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf')
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.png')	
		print 'Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf',
	print ' ...Done.'

	return



def MakeBasicPlotQCD(recovariable,xlabel,presentationbinning,selection,qcdselection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,version_name,qcdrescale):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	# Create Canvas
	# c1 = TCanvas("c1","",800,800)
	gStyle.SetOptStat(0)

	# pad1 = TPad( 'pad1', 'pad1', 0.0, 0.47, 1.0, 1.0 )#divide canvas into pads
	# pad2 = TPad( 'pad2', 'pad2', 0.0, 0.25, 1.0, 0.44 )
	# pad3 = TPad( 'pad3', 'pad3', 0.0, 0.03, 1.0, 0.22 )
	# if tagname == 'uujj':
	# 	pad1.SetLogx()
	# 	pad2.SetLogx()
	# 	pad3.SetLogx()

	# pad1.Draw()
	# pad2.Draw()
	# pad3.Draw()

	if 'PAS' not in tagname:
		c1 = TCanvas("c1","",800,800)
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.4, 1.0, 1.0 )#divide canvas into pads
		pad2 = TPad( 'pad2', 'pad2', 0.0, 0.26, 1.0, 0.4 )
		pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.26 )
		pad1.Draw()
		pad2.Draw()
		pad3.Draw()
		pad1.SetBottomMargin(0.0)		
		pad2.SetTopMargin(0.0)
		pad3.SetTopMargin(0.0)
		pad2.SetBottomMargin(0.0)
		pad3.SetBottomMargin(0.43)
	else:
		# if 'final' not in tagname:
		c1 = TCanvas("c1","",800,550)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		perc = 5.0


	pad1.cd()
	# pad1.SetGrid()
	# These are the style parameters for certain plots - [FillStyle,MarkerStyle,MarkerSize,LineWidth,Color]
	MCRecoStyle=[0,20,.00001,1,4]
	DataRecoStyle=[0,20,1.5,1,1]
	# X and Y axis labels for plot
	Label=[xlabel,"Events / bin"]

	WStackStyle=[3007,20,.00001,1,6]
	TTStackStyle=[3005,20,.00001,1,4]
	ZStackStyle=[3004,20,.00001,1,2]
	DiBosonStackStyle=[3006,20,.00001,1,3]
	StopStackStyle=[3008,20,.00001,1,7]
	QCDStackStyle=[3013,20,.00001,1,15]

	SignalStyle=[0,22,0.7,3,28]
	SignalStyle2=[0,22,0.7,3,38]

	print 'Getting Final sel '
	if tagname == 'final':
		print 'cat '+cutlog+' | grep '+channel+str(plotmass)
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		print 'found'
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+selection+fsel+')'
		print 'parsed'
		# print selection

	##############################################################################
	#######      Top Left Plot - Normal Stacked Distributions              #######
	##############################################################################
	c1.cd(1)

	print 'Doing Projections'
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',tn_WJetsJBin,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',tn_DoubleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',tn_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',tn_ZJetsJBin,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',tn_TTBarDBin,recovariable,presentationbinning,selection+'*('+str(ttscale)+')*'+weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',tn_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)

	if channel=='uujj':
		if 'weight' in qcdselection:
			hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD #mu-enriched',tn_QCD,recovariable,presentationbinning,qcdselection,QCDStackStyle,Label)
		if 'weight' not in qcdselection:
			#hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD #mu-enriched',tn_DoubleMuData,recovariable,presentationbinning,qcdselection,QCDStackStyle,Label)
			hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD #mu-enriched',tn_DoubleMuData,recovariable,presentationbinning,qcdselection+'*('+str(qcdrescale)+')',QCDStackStyle,Label)#fixme todo adding ss non-iso scale factor

	if channel=='uvjj':
		hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD #mu-enriched',tn_QCD,recovariable,presentationbinning,qcdselection+'*('+str(qcdrescale)+')',QCDStackStyle,Label)


	if channel == 'uujj':

		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets,hs_rec_QCD]

	if channel == 'uvjj':
	
		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)		
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_WJets,hs_rec_QCD]
		


	MCStack = THStack ("MCStack","")
	SMIntegral = sum(k.Integral() for k in SM)
	print 'SM Integral: ',SMIntegral
	#print 'hs_rec_Data.Integral(): ', hs_rec_Data.Integral(), 'hs_rec_Data.GetEntries()', hs_rec_Data.GetEntries()
	
	print 'Stacking...  ',	
	for x in SM:
		# x.Scale(mcdatascalepres)
		MCStack.Add(x)
		x.SetMaximum(10*hs_rec_Data.GetMaximum())

	MCStack.Draw("HIST")
	c1.cd(1).SetLogy()

	MCStack=BeautifyStack(MCStack,Label)

	setZeroBinErrors(hs_rec_Data,MCStack)
	#hs_rec_Data.Draw("E0PSAME")
	#hs_rec_Data_tgraph = TGraphAsymmErrors(hs_rec_Data)
	#setZeroBinErrors_tgraph(hs_rec_Data,hs_rec_Data_tgraph,MCStack,hs_rec_Signal,hs_rec_Signal2)
	#hs_rec_Data_tgraph.Draw("ZE0PSAME")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	leg = TLegend(0.63,0.62,0.89,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetFillStyle(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(.04)
	leg.AddEntry(hs_rec_Data,"Data");
	if channel=='uujj':
		leg.AddEntry(hs_rec_ZJets,'Z/^{}#gamma* + jets')
	if channel=='uvjj':
		leg.AddEntry(hs_rec_WJets,'W + jets')
	leg.AddEntry(hs_rec_TTBar,'t#bar{t}')
	leg.AddEntry(hs_rec_DiBoson,'Other background')
	leg.AddEntry(hs_rec_QCD,'Multijet')
	leg.Draw()

	sqrts = "#sqrt{s} = 13 TeV";
	l1=TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.06)
 
	# l1.DrawLatex(0.37,0.94,"CMS 2012  "+sqrts+", 19.7 fb^{-1}")
	# l1.DrawLatex(0.13,0.76,sqrts)

	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(62)
	l2.SetNDC()
	l2.SetTextSize(0.06)
	# l2.SetTextAngle(45);	
	# l2.DrawLatex(0.15,0.83,"CMS #it{Preliminary}")
	if  'PAS' in tagname and 'tagfree' not in tagname:
		#l2.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                     35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	else:
		#l2.DrawLatex(0.18,0.94,"                          "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                     35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	gPad.RedrawAxis()

	MCStack.SetMinimum(1.)
	MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())

	if 'PAS' in tagname:
		print 'Saving...  ',
		c1.Print('Results_'+version_name+'/BasicLQQCD_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
		c1.Print('Results_'+version_name+'/BasicLQQCD_'+channel+'_'+recovariable+'_'+tagname+'.png')		
		print 'Done.'
		return



	pad2.cd()
	# pad2.SetLogy()
	pad2.SetGrid()

	RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)



	RatHistDen.Sumw2()
	RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
	RatHistNum.Sumw2()
	for hmc in SM:
		RatHistDen.Add(hmc)

	RatHistNum.Add(hs_rec_Data)
	RatHistNum.Divide(RatHistDen)
	# for x in RatHistNum.GetNbinsX():
	# 	print RatHistNum.GetBinCenter(x), RatHistNum.GetBinContent(x)

	RatHistNum.SetMaximum(1.5)
	RatHistNum.SetMinimum(0.5)


	RatHistNum.GetYaxis().SetTitleFont(42);
	RatHistNum.GetXaxis().SetTitle('');
	RatHistNum.GetYaxis().SetTitle('Data/MC');
	RatHistNum.GetYaxis().SetNdivisions(308,True)

	RatHistNum.GetXaxis().SetTitleSize(0.);
	RatHistNum.GetYaxis().SetTitleSize(.20);
	RatHistNum.GetXaxis().CenterTitle();
	RatHistNum.GetYaxis().CenterTitle();		
	RatHistNum.GetXaxis().SetTitleOffset(.28);
	RatHistNum.GetYaxis().SetTitleOffset(.18);
	RatHistNum.GetYaxis().SetLabelSize(.15);
	RatHistNum.GetXaxis().SetLabelSize(.09);

	RatHistNum.Draw()

	RatHistDen.SetMarkerSize(0)
	RatHistDen.SetFillColor(17)
	RatHistDen.SetFillStyle(3105)
	for bin in range(RatHistDen.GetNbinsX()+1) :
		if bin==0: continue
		x = RatHistDen.GetBinContent(bin)
		err = RatHistDen.GetBinError(bin)
		if x==0: err=0
		else: err = err/x
		RatHistDen.SetBinError(bin,err)
		RatHistDen.SetBinContent(bin,1)
	#RatHistDen.Draw("E2SAMES")
	RatHistNum.Draw("SAMES")

	unity=TLine(RatHistNum.GetXaxis().GetXmin(), 1.0 , RatHistNum.GetXaxis().GetXmax(),1.0)
	unity.Draw("SAME")	

	pad3.cd()
	# pad2.SetLogy()
	pad3.SetGrid()

	chiplot =CreateHisto('chiplot','chiplot',t_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
	chiplot.Sumw2()

	resstring = '( 0.0 '

	for n in range(chiplot.GetNbinsX()+1):
		lhs = chiplot.GetBinCenter(n) - 0.5*chiplot.GetBinWidth(n)
		rhs = chiplot.GetBinCenter(n) + 0.5*chiplot.GetBinWidth(n)
		lhs = str(round(lhs,3))
		rhs = str(round(rhs,3))

		bg = 0
		bgerr = 0
		dat = hs_rec_Data.GetBinContent(n)
		daterr = math.sqrt(1.0*dat)
		for hmc in SM:
			bg += hmc.GetBinContent(n)
			bgerr += hmc.GetBinError(n)*hmc.GetBinError(n)
		bgerr = math.sqrt(bgerr)
		total_err = math.sqrt(bgerr*bgerr+daterr*daterr)
		
		resfac = '1.0'

		if total_err>0: 
			chi = (dat - bg)/total_err
			chiplot.SetBinContent(n,chi)
			chiplot.SetBinError(n,0.0)
		if bg > 0 and dat > 0:
			resfac = str(round(dat/bg,3))
		if n != 0:
			resstring += ' + '+resfac+'*('+recovariable +'>'+lhs+')'+'*('+recovariable +'<='+rhs+')'

	resstring += ')'
	if recovariable =='Phi_miss':
		print resstring

	chiplot.SetMaximum(6)
	chiplot.SetMinimum(-6)



	chiplot.GetYaxis().SetTitleFont(42);
	# chiplot.GetXaxis().SetTitle('');
	chiplot.GetYaxis().SetTitle('#chi (Data,MC)');
	# chiplot.GetXaxis().SetTitle('#chi (Data,MC)');


	chiplot.GetXaxis().SetTitleSize(.14);
	chiplot.GetYaxis().SetTitleSize(.10);
	chiplot.GetXaxis().CenterTitle();
	chiplot.GetYaxis().CenterTitle();		
	chiplot.GetXaxis().SetTitleOffset(.8);
	chiplot.GetYaxis().SetTitleOffset(.34);
	chiplot.GetYaxis().SetLabelSize(.09);
	chiplot.GetXaxis().SetLabelSize(.09);

	chiplot.Draw('EP')
	zero=TLine(RatHistNum.GetXaxis().GetXmin(), 0.0 , RatHistNum.GetXaxis().GetXmax(),0.0)
	plus2=TLine(RatHistNum.GetXaxis().GetXmin(), 2.0 , RatHistNum.GetXaxis().GetXmax(),2.0)
	minus2=TLine(RatHistNum.GetXaxis().GetXmin(), -2.0 , RatHistNum.GetXaxis().GetXmax(),-2.0)
	plus2.SetLineColor(2)
	minus2.SetLineColor(2)

	plus2.Draw("SAME")
	minus2.Draw("SAME")
	zero.Draw("SAME")	


	print 'Saving...  ',
	c1.Print('Results_'+version_name+'/BasicLQQCD_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
	c1.Print('Results_'+version_name+'/BasicLQQCD_'+channel+'_'+recovariable+'_'+tagname+'.png')		
	print 'Done.'



def MakeBasicPlotEMu(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,cutlog,version_name,plotmass):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "te_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('te_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	# Create Canvas
	c1 = TCanvas("c1","",800,800)
	gStyle.SetOptStat(0)

	if 'PAS' not in tagname:
		c1 = TCanvas("c1","",800,800)
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.4, 1.0, 1.0 )#divide canvas into pads
		pad2 = TPad( 'pad2', 'pad2', 0.0, 0.26, 1.0, 0.4 )
		pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.26 )
		pad1.Draw()
		pad2.Draw()
		pad3.Draw()
		pad1.SetBottomMargin(0.0)		
		pad2.SetTopMargin(0.0)
		pad3.SetTopMargin(0.0)
		pad2.SetBottomMargin(0.0)
		pad3.SetBottomMargin(0.43)
	else:
		# if 'final' not in tagname:
		c1 = TCanvas("c1","",800,550)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		perc = 5.0


	pad1.cd()
	# pad1.SetGrid()
	# These are the style parameters for certain plots - [FillStyle,MarkerStyle,MarkerSize,LineWidth,Color]
	MCRecoStyle=[0,20,.00001,1,4]
	DataRecoStyle=[0,20,1.5,1,1]
	# X and Y axis labels for plot
	Label=[xlabel,"Events / bin"]

	WStackStyle=[3007,20,.00001,1,6]
	TTStackStyle=[3005,20,.00001,1,4]
	ZStackStyle=[3004,20,.00001,1,2]
	DiBosonStackStyle=[3006,20,.00001,1,3]
	StopStackStyle=[3008,20,.00001,1,7]
	QCDStackStyle=[3013,20,.00001,1,15]

	SignalStyle=[0,22,0.7,3,28]
	SignalStyle2=[0,22,0.7,3,38]

	if tagname == 'final':
		# print 'cat '+cutlog+' | grep '+channel+str(plotmass)
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+selection+fsel+')'
		# print selection

	##############################################################################
	#######      Top Left Plot - Normal Stacked Distributions              #######
	##############################################################################
	c1.cd(1)
	print 'Projecting trees...  ',
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',te_WJetsJBin,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',te_DoubleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',te_ZJetsJBin,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',te_TTBarDBin,recovariable,presentationbinning,selection+'*('+str(ttscale)+')*'+weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',te_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)

	print "THIS NUMBER --> hs_rec_TTBar.Integral():",hs_rec_TTBar.Integral(), 'hs_rec_TTBar.GetEntries():',hs_rec_TTBar.GetEntries()

	# hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD #mu-enriched [Pythia]',te_QCD,recovariable,presentationbinning,selection+'*'+weight,QCDStackStyle,Label)

	sig1name = ''
	sig2name = ''

	if channel == 'uujj':
		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_DiBoson,hs_rec_ZJets,hs_rec_TTBar]

	if channel == 'uvjj':
		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)		
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_WJets]
		

	# mcdatascalepres = (1.0*(hs_rec_Data.GetEntries()))/(sum(k.Integral() for k in SM))

	MCStack = THStack ("MCStack","")
	SMIntegral = sum(k.Integral() for k in SM)
	print 'SMIntegral:',SMIntegral
	print 'hs_rec_Data.Integral():',hs_rec_Data.Integral(), 'hs_rec_Data.GetEntries():',hs_rec_Data.GetEntries()
	# MCStack.SetMaximum(SMIntegral*100)
	
	print 'Stacking...  ',	
	for x in SM:
		# x.Scale(mcdatascalepres)
		MCStack.Add(x)
		x.SetMaximum(10*hs_rec_Data.GetMaximum())

	MCStack.Draw("HIST")
	c1.cd(1).SetLogy()

	MCStack=BeautifyStack(MCStack,Label)

	#setZeroBinErrors(hs_rec_Data,MCStack)
	hs_rec_Data_tgraph = TGraphAsymmErrors(hs_rec_Data)
	setZeroBinErrors_tgraph_emu(hs_rec_Data,hs_rec_Data_tgraph,MCStack)
	hs_rec_Data_tgraph.Draw("EPSAME")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	leg = TLegend(0.63,0.62,0.89,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetFillStyle(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(.04)
	leg.AddEntry(hs_rec_Data,"e#mu Data");
	if channel=='uujj':
		leg.AddEntry(hs_rec_ZJets,'Z/^{}#gamma* + jets')
	if channel=='uujj':
		leg.AddEntry(hs_rec_WJets,'W + jets')
	leg.AddEntry(hs_rec_TTBar,'t#bar{t} MC')
	leg.AddEntry(hs_rec_DiBoson,'Other background')
	leg.Draw()

	sqrts = "#sqrt{s} = 13 TeV";
	l1=TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.06)
 
	# l1.DrawLatex(0.37,0.94,"CMS 2012  "+sqrts+", 19.7 fb^{-1}")
	# l1.DrawLatex(0.13,0.76,sqrts)

	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(62)
	l2.SetNDC()
	l2.SetTextSize(0.06)
	# l2.SetTextAngle(45);	
	# l2.DrawLatex(0.15,0.83,"CMS #it{Preliminary} ")
	if  'PAS' in tagname and 'tagfree' not in tagname:
		#l2.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                     35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	else:
		#l2.DrawLatex(0.18,0.94,"                          "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                     35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")

	gPad.RedrawAxis()

	MCStack.SetMinimum(.03333)
	MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())

	if 'PAS' in tagname:

		print 'Saving...  ',
		if 'final' not in tagname:
			c1.Print('Results_'+version_name+'/BasicLQ_NoRatio_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
			c1.Print('Results_'+version_name+'/BasicLQ_NoRatio_'+channel+'_'+recovariable+'_'+tagname+'.png')
		else:
			c1.Print('Results_'+version_name+'/BasicLQ_NoRatio_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf')
			c1.Print('Results_'+version_name+'/BasicLQ_NoRatio_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.png')		
		print 'Done.'

		return

	pad2.cd()
	# pad2.SetLogy()
	pad2.SetGrid()

	RatHistDen =CreateHisto('RatHisDen','RatHistDen',te_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)



	RatHistDen.Sumw2()
	RatHistNum =CreateHisto('RatHisNum','RatHistNum',te_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
	RatHistNum.Sumw2()
	for hmc in SM:
		RatHistDen.Add(hmc)

	RatHistNum.Add(hs_rec_Data)
	RatHistNum.Divide(RatHistDen)
	# for x in RatHistNum.GetNbinsX():
	# 	print RatHistNum.GetBinCenter(x), RatHistNum.GetBinContent(x)

	RatHistNum.SetMaximum(1.5)
	RatHistNum.SetMinimum(0.5)


	RatHistNum.GetYaxis().SetTitleFont(42);
	RatHistNum.GetXaxis().SetTitle('');
	RatHistNum.GetYaxis().SetTitle('Data/MC');
	RatHistNum.GetYaxis().SetNdivisions(308,True)

	RatHistNum.GetXaxis().SetTitleSize(0.);
	RatHistNum.GetYaxis().SetTitleSize(.20);
	RatHistNum.GetXaxis().CenterTitle();
	RatHistNum.GetYaxis().CenterTitle();		
	RatHistNum.GetXaxis().SetTitleOffset(.28);
	RatHistNum.GetYaxis().SetTitleOffset(.18);
	RatHistNum.GetYaxis().SetLabelSize(.15);
	RatHistNum.GetXaxis().SetLabelSize(.09);

	RatHistDen.SetMarkerSize(0)
	RatHistDen.SetFillColor(17)
	RatHistDen.SetFillStyle(3105)
	for bin in range(RatHistDen.GetNbinsX()+1) :
		if bin==0: continue
		x = RatHistDen.GetBinContent(bin)
		err = RatHistDen.GetBinError(bin)
		if x==0: err=0
		else: err = err/x
		RatHistDen.SetBinError(bin,err)
		RatHistDen.SetBinContent(bin,1)
	RatHistNum.Draw()
	#RatHistDen.Draw("E2SAMES")
	RatHistNum.Draw("SAMES")
	unity=TLine(RatHistNum.GetXaxis().GetXmin(), 1.0 , RatHistNum.GetXaxis().GetXmax(),1.0)
	unity.Draw("SAME")	


	pad3.cd()
	# pad2.SetLogy()
	pad3.SetGrid()

	chiplot =CreateHisto('chiplot','chiplot',te_DoubleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
	chiplot.Sumw2()

	resstring = '( 0.0 '

	for n in range(chiplot.GetNbinsX()+1):
		lhs = chiplot.GetBinCenter(n) - 0.5*chiplot.GetBinWidth(n)
		rhs = chiplot.GetBinCenter(n) + 0.5*chiplot.GetBinWidth(n)
		lhs = str(round(lhs,3))
		rhs = str(round(rhs,3))

		bg = 0
		bgerr = 0
		dat = hs_rec_Data.GetBinContent(n)
		daterr = math.sqrt(1.0*dat)
		for hmc in SM:
			bg += hmc.GetBinContent(n)
			bgerr += hmc.GetBinError(n)*hmc.GetBinError(n)
		bgerr = math.sqrt(bgerr)
		total_err = math.sqrt(bgerr*bgerr+daterr*daterr)
		
		resfac = '1.0'

		if total_err>0: 
			chi = (dat - bg)/total_err
			chiplot.SetBinContent(n,chi)
			chiplot.SetBinError(n,0.0)
		if bg > 0 and dat > 0:
			resfac = str(round(dat/bg,3))
		if n != 0:
			resstring += ' + '+resfac+'*('+recovariable +'>'+lhs+')'+'*('+recovariable +'<='+rhs+')'

	resstring += ')'
	if recovariable =='Phi_miss':
		print resstring

	chiplot.SetMaximum(6)
	chiplot.SetMinimum(-6)


	chiplot.GetYaxis().SetTitleFont(42);
	# chiplot.GetXaxis().SetTitle('');
	chiplot.GetYaxis().SetTitle('#chi (Data,MC)');
	# chiplot.GetXaxis().SetTitle('#chi (Data,MC)');


	chiplot.GetXaxis().SetTitleSize(.14);
	chiplot.GetYaxis().SetTitleSize(.10);
	chiplot.GetXaxis().CenterTitle();
	chiplot.GetYaxis().CenterTitle();		
	chiplot.GetXaxis().SetTitleOffset(.8);
	chiplot.GetYaxis().SetTitleOffset(.34);
	chiplot.GetYaxis().SetLabelSize(.09);
	chiplot.GetXaxis().SetLabelSize(.09);


	chiplot.Draw('EP')
	zero=TLine(RatHistNum.GetXaxis().GetXmin(), 0.0 , RatHistNum.GetXaxis().GetXmax(),0.0)
	plus2=TLine(RatHistNum.GetXaxis().GetXmin(), 2.0 , RatHistNum.GetXaxis().GetXmax(),2.0)
	minus2=TLine(RatHistNum.GetXaxis().GetXmin(), -2.0 , RatHistNum.GetXaxis().GetXmax(),-2.0)
	plus2.SetLineColor(2)
	minus2.SetLineColor(2)

	plus2.Draw("SAME")
	minus2.Draw("SAME")
	zero.Draw("SAME")	


	print 'Saving...  ',
	if 'final' not in tagname:
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.png')
	else:
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf')
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.png')		
	print 'Done.'

def round_to(n, precission):
    correction = 0.5 if n >= 0 else -0.5
    return int(n/precission+correction)*precission

def TH2toCutRes(th2,thname, addon):
	res = []

	# print th2.Integral()
	nx = th2.GetNbinsX()+1
	ny = th2.GetNbinsY()+1
	for x in range(nx):
		for y in range(ny):
			if x == 0 : continue
			if y == 0 : continue
			res.append([thname,[addon, th2.GetXaxis().GetBinCenter(x) - 0.5*th2.GetXaxis().GetBinWidth(x), th2.GetYaxis().GetBinCenter(y) - 0.5*th2.GetYaxis().GetBinWidth(y)],th2.Integral(x,nx,y,ny)])

	return res


def GetRatesFromTH2(sigs,baks,_presel,_weight,_hvars,addon,scalefac):
	b1 = ConvertBinning(_hvars[0][1])
	b2 = ConvertBinning(_hvars[1][1])
	v1 = (_hvars[0][0])
	v2 = (_hvars[1][0])
	allinfo = []
	for t in sigs+baks:
		print 'Checking:',t
		h = 'h_'+t
		# print( h + ' = TH2D("'+h+'","'+h+'",len(b1)-1,array(\'d\',b1),len(b2)-1,array(\'d\',b2))')
		exec( h + ' = TH2D("'+h+'","'+h+'",len(b1)-1,array(\'d\',b1),len(b2)-1,array(\'d\',b2))')
		exec( t+'.Project("'+h+'","'+v2+':'+v1+'","'+_presel+'*('+_weight+'*'+scalefac+')")')
		exec( 'allinfo += TH2toCutRes ('+h+',"'+h+'",'+str(addon)+')')
		# break
	return allinfo


def OptimizeCuts3D(variablespace,presel,weight,tag,scalefacs,cutfile,channel):
	if 'BL' in channel:
		signalType = 'BL'
		channel = 'uujj'
	else:
		signalType = 'LQ'
	signalType = 'HH'
	channel = 'res'
	outfile = 'Results_'+tag+'/'+channel+'Cuts_new.txt'
	ftmpname = signalType+channel+'_opttmp.root'
	ftmp = TFile.Open(ftmpname,'RECREATE')
	optvars = []
	binnings = []
	for v in variablespace:
		v = v.split(':')
		var = v[0]
		v0 = float(v[1])
		v1 = float(v[3])
		vb = float(v[2])
		#bins = [int(round((v1-v0)/vb)),v0,v1]#fixme todo original
		bins = [int(round((v1-vb)/v0)),vb,v1]
		optvars.append([var,bins]) 

	minvar = ['',[9999999,0,0]]
	for v in range(len(optvars)):
		if optvars[v][1][0] < minvar[1][0]:
			minvar = optvars[v]
	hvars = []
	for v in range(len(optvars)):
		if optvars[v] != minvar:
			hvars.append(optvars[v])

	minvarcuts = ['('+minvar[0]+'>'+str(x)+')' for x in ConvertBinning(minvar[1])] 

	background =  [ 't_'+x.replace('\n','') for x in  ['QCD','DiBoson','WJetsJBin','TTBarDBin','ZJetsJBin','SingleTop']]#original 
	#background =  [ 't_'+x.replace('\n','') for x in  ['QCD','DiBoson','WJetsJBin','TTBarDBin','ZJetsJBinOpt','SingleTop']]#this is if we use the 1/5 statistics ZJets for optimization to avoid 'overtraining'
	if '/store/' in NormalDirectory:
		signals =  [ 't_'+x.replace('.root\n','') for x in  os.popen('/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls '+NormalDirectory+'| grep root | grep '+signalType+channel+' ').readlines()]
	else:
		signals =  [ 't_'+x.replace('.root\n','') for x in  os.popen('ls '+NormalDirectory+'| grep root | grep '+signalType+channel+' ').readlines()]

	[_r_z,_r_tt,_r_w] = scalefacs

	if cutfile=='':
		cutinfo = []
		logfile = 'Results_'+tag+'/Log_'+signalType+channel+'Cuts.txt'
		l = open(logfile,'w')
		for h in signals+background:
			l.write('h_'+h+' = [] \n')
		for x in range(len(minvarcuts)):
			print 'Analyzing for case',minvarcuts[x]
			scalefac = '1.0'
			if 'ZJets' in h:
				scalefac = str(_r_z)
				if 'Opt' in h:
					scalefac = scalefac+'*5.0'#this is if we use the 1/5 statistics ZJets for optimization to avoid 'overtraining'
			if 'WJets' in h:
				scalefac = str(_r_w)
			if 'TTBar' in h:
				scalefac = str(_r_tt)
		 	moreinfo = GetRatesFromTH2(signals,background,presel+'*'+minvarcuts[x],weight,hvars,(ConvertBinning(minvar[1]))[x],scalefac)
		 	for m in  moreinfo:
				l.write(m[0]+'.append(['+str(m[2])+','+str(m[1])+'])\n')
		l.close()

		os.system('rm '+ftmpname)
		cutfile = logfile
	
	print 'Getting log ... '
	# flog = open('loglog.txt','w')

	nf = os.popen('cat '+cutfile+' | wc -l').readlines()[0]
	nf = int(nf)
	nd = 0
	for c in open(cutfile):
		nd += 1
		if nd%100000==0:
			print str(100*round( (1.0*nd)/(1.0*nf),3 )), '% complete'
		# print '** ',c
		# flog.write('** '+c)
		exec(c)

	# flog.close()
	
	SIGS = []
	BAKS = []

	for h in signals:
		exec('SIGS.append(h_'+h+')')
	for h in background:
		exec('BAKS.append(h_'+h+')')

	optimlog = open('Results_'+tag+'/Opt'+signalType+'_'+channel+'Cuts.txt','w')

	valuetable = []

	for S in range(len(SIGS)):
		_ssbmax = -99999
		_bestcut = 0
		for icut in range(len(SIGS[S])):
			_s = SIGS[S][icut][0]
			_b = 0.0
			for B in BAKS:
				_b += B[icut][0]
			if _s + _b < 0.0001:
				continue
			#_ssb = _s/math.sqrt(_s+_b)#fixme original
			_ssb = math.sqrt(2.0*((_s+_b)*math.log(1.0+_s/_b)-_s))#fixme trying eq 96 from paper DOI:10.1140/epjc/s10052-011-1554-0
			if _ssb > _ssbmax:
				_ssbmax = _ssb
				_bestcut = icut
		opt = 'opt_'+signals[S].replace('t_','')+ ' = (('+minvar[0] +'>' + str(SIGS[S][_bestcut][1][0])+')*('+hvars[0][0]+'>'+str(SIGS[S][_bestcut][1][1])+')*('+hvars[1][0]+'>'+str(SIGS[S][_bestcut][1][2])+'))\n'  
		print opt
		thismass = float(((signals[S].replace('t_','')).split(channel))[-1])
		valueline = [thismass, (SIGS[S][_bestcut][1][0]), (SIGS[S][_bestcut][1][1]), (SIGS[S][_bestcut][1][2])]
		valuetable.append(valueline)
		optimlog.write(opt)

	optimlog.close()

	print 'Performing fits ...'
	cuts = MakeSmoothCuts(valuetable,[minvar[0],hvars[0][0], hvars[1][0]],tag,signalType,channel,'lin')
	cuts = MakeSmoothCuts(valuetable,[minvar[0],hvars[0][0], hvars[1][0]],tag,signalType,channel,'lintanh')
	cuts = MakeSmoothCuts(valuetable,[minvar[0],hvars[0][0], hvars[1][0]],tag,signalType,channel,'pol2')
	cuts = MakeSmoothCuts(valuetable,[minvar[0],hvars[0][0], hvars[1][0]],tag,signalType,channel,'pol2cutoff')
	cuts = MakeSmoothCuts(valuetable,[minvar[0],hvars[0][0], hvars[1][0]],tag,signalType,channel,'lincutoff')

	return cuts

def ReDoOptFits(OptFile):
	tag = OptFile.split('/')[0]
	tag = tag.replace('Results_','')
	valuetable = []
	for line in open(OptFile):
		valueline = []
		channel = line.split('jj')[0]
		if 'BL' in line : 
			signalType = 'BL'
			channel = channel.split('BL')[1]
		else: 
			signalType = 'LQ'
			channel = channel.split('LQ')[1]
		channel += 'jj'
		mass = float(line.split('jj')[1].split('=')[0].replace(' ',''))

		varnames = line.split('=')[-1]
		varnames = varnames.replace(')','')
		varnames = varnames.replace('(','')
		varnames = varnames.split('*')
		varwords = []
		varvals = []
		for v in varnames:
			v = v.split('>')
			varwords.append(v[0].replace(' ',''))
			varvals.append(float(v[1]))
		valueline = [mass]
		for v in varvals:
			valueline.append(v)
		valuetable.append(valueline)
	# print tag,channel, varwords
	# for v in valuetable:
	# 	print v

	# cuts = MakeSmoothCuts(valuetable,varwords,tag,signalType,channel,'lin')
	# cuts = MakeSmoothCuts(valuetable,varwords,tag,signalType,channel,'lintanh')
	# cuts = MakeSmoothCuts(valuetable,varwords,tag,signalType,channel,'pol2')
	cuts = MakeSmoothCuts(valuetable,varwords,tag,signalType,channel,'pol2cutoff')
	# cuts = MakeSmoothCuts(valuetable,varwords,tag,signalType,channel,'lincutoff')		

def MakeSmoothCuts(vals,vnames,versionname,signalType,chan,rawmethod):

	xnames = []
	for x in vnames:
		a = x
		if "Pt_jet1" in a :  x = "p_{T}(jet_{1})"
		if "Pt_jet2" in a :  x = "p_{T}(jet_{2})"
		if "Pt_muon1" in a :  x = "p_{T}(#mu_{1})"
		if "Pt_muon2" in a :  x = "p_{T}(#mu_{2})"
		if "St_uujj" in a :  x = "S_{T}^{#mu#mujj}"
		if "M_uu" in a :  x = "M^{#mu#mu}"
		if "M_uujj1" in a :  x = "M_{#muj}_{1}"
		if "M_uujj2" in a :  x = "M_{#muj}_{2}"
		if "GoodVertexCount" in a :  x = "N_{Vertices}"
		if "Pt_jet1" in a :  x = "p_{T}(jet_{1})"
		if "Pt_jet2" in a :  x = "p_{T}(jet_{2})"
		if "Pt_muon1" in a :  x = "p_{T}(#mu_{1})"
		if "Pt_miss" in a :  x = "E_{T}^{miss}"
		if "St_uvjj" in a :  x = "S_{T}^{#mu#nujj}"
		if "MT_uv in" in a :  x = "M_{T}^{#mu#nu}"
		if "MT_uvjj" in a :  x = "M_{T}^{#muj}"
		if "M_uvjj" in a :  x = "M_{#muj}"
		xnames.append(x)

	_allvals = sorted(vals,key=lambda vals: vals[0])


	if 'cutoff' in rawmethod:
		_vals = []
		for v in _allvals:
			if v[0] <= 1500:#fixme todo was 1000
				_vals.append(v)
	else:
		_vals=_allvals

	for v in _vals:
		print v

	yinds = []
	masses = []

	for v in range(len(_vals[0])):
		if v == 0: 
			for v in _vals:
				masses.append(v[0])
			continue
		yinds.append(v)

	allmasses = []

	for v in range(len(_allvals[0])):
		if v == 0: 
			for v in _allvals:
				allmasses.append(v[0])	

	n = len(masses)

	method = rawmethod.replace('cutoff','')
	optim_res=[masses]
	for y in yinds:

		Y = []
		for v in _vals:
			Y.append(v[y])
		print Y		
		X = array("d", masses)
		Y = array("d", Y)

		c1 = TCanvas("c1","",700,500)
		c1.cd(1).SetGrid()

		print X
		print Y
		hout = TGraph(n,X,Y)
		hout.GetYaxis().SetTitle(xnames[y-1]+' Threshold [GeV]')
		hout.GetXaxis().SetTitle('LQ Mass [GeV]')
		hout.SetTitle('')
		hout.SetMarkerStyle(21)
		hout.SetMarkerSize(1)
		hout.SetLineWidth(2)
		hout.SetLineColor(1)
		hout.GetXaxis().SetTitleFont(42)
		hout.GetYaxis().SetTitleFont(42)
		hout.GetXaxis().SetLabelFont(42)
		hout.GetYaxis().SetLabelFont(42)
		hout.GetYaxis().SetTitleFont(42);
		hout.GetXaxis().SetTitleSize(.06);
		hout.GetYaxis().SetTitleSize(.06);
		hout.GetXaxis().CenterTitle();
		hout.GetYaxis().CenterTitle();
		hout.GetXaxis().SetTitleOffset(0.8);
		hout.GetYaxis().SetTitleOffset(0.8);
		hout.GetYaxis().SetLabelSize(.05);
		hout.GetXaxis().SetLabelSize(.05);
		hout.Draw("AP")
		
		if method == 'lin':
			ft = TF1("ft","[1]*x + [0]", 150,2050 )  # linear
		if method == 'lintanh':
			ft = TF1("ft","[0] + [1]*[1]*tanh(x+[2]) + [3]*[3]*x",150,2250) 		#linear+tanh monotonic
		if method == 'pol2':
			ft = TF1("ft","[0] + [1]*x + [2]*(x*x)", 150, 2250); # second degree pol
		hout.Fit('ft')

		betterfits = []
		for m in allmasses:
			orig_val = ft.Eval(m)
			new_val = round_to(orig_val,5)
			betterfits.append(new_val)
		optim_res.append(betterfits)
		c1.Print('Results_'+versionname+'/Optimization'+signalType+'_'+chan+'_'+vnames[y-1]+'_'+rawmethod+'.pdf')
		c1.Print('Results_'+versionname+'/Optimization'+signalType+'_'+chan+'_'+vnames[y-1]+'_'+rawmethod+'.png')

	optimlog = open('Results_'+versionname+'/Opt'+signalType+'_'+chan+'Cuts_Smoothed_'+rawmethod+'.txt','w')	

	for x in range(len(optim_res[0])):
		cutstr = ''
		for y in range(len(vnames)):
			cutstr += '('+vnames[y]+ '>'+str(optim_res[y+1][x])+ ')*'
		optline =  'opt_'+signalType+chan+str(int(optim_res[0][x]))+ ' = ('+cutstr[:-1]+')'
		print optline
		optimlog.write(optline+'\n')
	optimlog.close()
	return 'Results_'+versionname+'/Opt'+signalType+'_'+chan+'Cuts_Smoothed.txt'

def CompareMeanSys(m,s1,s2):
	_m = []
	_s1 = []
	_s2 = []
	for x in range(len(m)):
		if x == 1:
			continue
		_m.append(m[x][0])
		_s1.append(s1[x][0])
		_s2.append(s2[x][0])

	systematics = []

	for x in range(len(_m)):
		syst = 1
		mavg = _m[x]
		sv1 = _s1[x]
		sv2 = _s2[x]
		d1 = abs(sv1-mavg)
		d2 = abs(sv2-mavg)
		diff = max([d1,d2])
		if diff > 0 and mavg > 0:
			syst = 1 + diff/mavg
		systematics.append(syst)
	outline = ' '
	for s in systematics:
		outline += str(s) + ' '
	return outline


def ParseFinalCards(cardcoll):
	chan = '' + 'uujj'*('uujj' in cardcoll)+ 'uvjj'*('uvjj' in cardcoll) 
	tables = glob(cardcoll)
	systypes = []
	for t in tables:
		_sys = (t.split('_')[-1]).replace('.txt','')
		systypes.append(_sys)
	variations = []
	for s in systypes:
		s = s.replace('up','')
		s = s.replace('down','')
		if s not in variations:
			variations.append(s)
	# for v in variations:
	# 	print v
	T = ''
	for n in range(len(systypes)):
		if systypes[n]=='':
			T = tables[n]
	print T
	cardnames = []
	for line in open(T,'r'):
		if 'L_' in line:
			cardname = line.split(' = ')[0]
			cardname = cardname.split('_')[-1] 
			cardnames.append(cardname)
		print ' * ',line
		exec(line)

	configlines = ['','imax 1','jmax '+str(len(headers)-2),'kmax '+str(len(headers)-1+len(variations)-1),'','bin 1','']

	nc = 0
	standardweights = []

	finalcards = cardcoll.replace('*','_ALL_')
	finalcards = finalcards.replace('systable','finalcards')
	fout = open(finalcards,'w')


	for card in cardnames:
		allcards = [line.replace('\n','') for line in os.popen('grep '+card+' '+cardcoll+' | grep -v '+str(card+'0')).readlines()]
		nc += 1
		mcard = ''
		scards = []
		for a in allcards:
			print 'here:',card,T,a
			if T in a:
				mcard = a
			else:
				scards.append(a)
			
		statlines = []

		# print headers
		#print 'mcard',mcard
		exec ('minfo = '+mcard.split('=')[-1])
		#print 'minfo',minfo
		# print ' \n '
		weights = []
		nums = []
		rates = []
		for entry in minfo:
			if entry[1] > 0.001:
				weights.append((1.0*entry[0])/(1.0*entry[1]))
			else:
				weights.append(0)
			nums.append(int(entry[1]))
			rates.append(entry[0])
		if nc ==1:
			standardweights = weights
		statlines = []
		spacers = -1
		rateline = 'rate '
		for h in range(len(headers)):
			head = headers[h]
			if 'Data' in head:
				continue
			spacers += 1
			nmc = nums[h]
			w = weights[h]
			if w <0.0000000001:
				w = standardweights[h]
			nmc = str(int(nmc))
			w = str(w)
			if rates[h]>0:
				r = str(rates[h])
			else :
				r = '0.0'
			statline = 'stat_'+head+' gmN '+nmc + (' - ')*spacers +' ' + w +' '+(' - ')*(len(headers) -2 - spacers)
			if nmc > 0:
				statlines.append(statline)
			rateline += ' '+r


		obsline = 'observation '+str(minfo[1][1])
		binline = 'bin '+(' 1 ')*(len(headers)-1)
		procline1 = 'process  '+card
		for hh in headers:
			if 'Sig' in hh or 'Data' in hh:
				continue
			procline1 += ' '+hh
		procline2 = 'process  0 '+(' 1 ')*(len(headers)-2)

		syslines = []
		for v in variations:
			if v == '':
				continue
			sysline = v + '  lnN  '
			this_sysset = []
			for ss in scards:
				if v in ss:
					this_sysset.append(ss)
			if len(this_sysset) == 1:
				this_sysset.append(this_sysset[0])
			print 'For sys',v
			print 'Looking at',this_sysset
			exec ('sys1 = '+this_sysset[0].split('=')[-1])
			exec ('sys2 = '+this_sysset[1].split('=')[-1])
			sysline += CompareMeanSys(minfo,sys1,sys2)
			syslines.append(sysline)


		fout.write( card + '.txt\n\n')
		for configline in configlines:
			fout.write( configline+'\n')
		fout.write( obsline+'\n')
		fout.write( ' '+'\n')
		fout.write( binline+'\n')
		fout.write( procline1+'\n')
		fout.write( procline2+'\n')
		fout.write( ' '+'\n')
		fout.write( rateline+'\n')
		fout.write( ' '+'\n')
		for sysline in syslines:
			fout.write( sysline+'\n')
		fout.write( ' '+'\n')
		for statline in statlines:
			fout.write( statline+'\n')
		fout.write( '\n'*3)

	fout.close()
	return finalcards

def FixFinalCards(cardsets):
	f = cardsets[0].split('/')[0]+'/FinalCardsLQ.txt'
	fout = open(f,'w')
	for c in cardsets:
		for line in open(c,'r'):
			line = line.replace('uujj','_M_')
			line = line.replace('uvjj','_BetaHalf_M_')
			fout.write(line)
	fout.close()
	return f

def ShapeSystematic(channel,normalWeight,presel,cutFile):
	print '\n\n--------------\n--------------\nRunning shape systematics for',channel,'channel.  This will take some time, be patient....'
	NoSelection = ['1.0','No selection!']
	Selection = [normalWeight,'Weight only']
	PreSelection = [normalWeight+'*'+presel,'Preselection']
	Sels = [NoSelection,Selection,PreSelection]
	for line in open(cutFile,'r'):
		if '=' in line:
			cutChannel = line.split('=')[0]
			cutSel = normalWeight+'*'+presel+'*'+line.split('=')[-1].replace('\n','').replace(' ','')
			#print cutLine
			Sels.append([cutSel, cutChannel])
	
	#scaleWeights = ['scaleWeight_Up','scaleWeight_Down']
	scaleWeights = ['scaleWeight_R1_F2','scaleWeight_R1_F0p5','scaleWeight_R2_F1','scaleWeight_Up','scaleWeight_R2_F0p5','scaleWeight_R0p5_F1','scaleWeight_R0p5_F2','scaleWeight_R0p5_F0p5']
	ZpercsUp =  []
	WpercsUp =  []
	ttpercsUp = []
	ZpercsDown =  []
	WpercsDown =  []
	ttpercsDown = []
	shapesysvar_Zjets = []
	shapesysvar_Wjets = []
	shapesysvar_TTjets = []
	
	Rz_uujj_diff = dict((x,0.) for x in scaleWeights)
	Rz_uujj_err_diff = dict((x,0.) for x in scaleWeights)
	Rtt_uujj_diff = dict((x,0.) for x in scaleWeights)
	Rtt_uujj_err_diff = dict((x,0.) for x in scaleWeights)

	#Get un-modified presel scale factors
	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0)
	#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>100)*(MT_uv<200)*(JetCount<3.5)*(((CISV_jet1>0.97)+(CISV_jet2>0.97))<1)', '(MT_uv>100)*(MT_uv<200)*(JetCount>3.5)*(((CISV_jet1>0.97)+(CISV_jet2>0.97))>=1)')#fixme todo varying control sample MT window

	#Get presel scale factors for each weight
	for weight in scaleWeights:
		[[Rz_uujj_diff[weight],Rz_uujj_err_diff[weight]],[Rtt_uujj_diff[weight],Rtt_uujj_err_diff[weight]]] = GetMuMuScaleFactors(NormalWeightMuMu+'*'+preselectionmumu+'*'+weight, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0)

	for selection in Sels :
		print '  ',selection[1]

		maxZ =[0.,0.]
		maxW =[0.,0.]
		maxTT=[0.,0.]
		for weight in scaleWeights:
			print '     ',weight
			thisSel = selection[0]+'*'+weight

			Z  = QuickIntegral(t_ZJetsJBin,selection[0]+'*'+str(Rz_uujj),1.0)
			W  = QuickIntegral(t_WJetsJBin,selection[0],1.0)
			tt = QuickIntegral(t_TTBarDBin,selection[0]+'*'+str(Rtt_uujj),1.0)

			Z_diff  = QuickIntegral(t_ZJetsJBin,thisSel+'*'+str(Rz_uujj_diff[weight]),1.0)
			W_diff  = QuickIntegral(t_WJetsJBin,thisSel,1.0)
			tt_diff = QuickIntegral(t_TTBarDBin,thisSel+'*'+str(Rtt_uujj_diff[weight]),1.0)

			if Z[0]>0 : 
				Zperc =  [100*(abs(Z_diff[0]-Z[0])/Z[0]),100*math.sqrt((math.sqrt(Z_diff[1]*Z_diff[1]+Z[1]*Z[1])/(Z[0]*Z[0]))+
								       ((Z_diff[0]-Z[0])*(Z_diff[0]-Z[0])*Z[1]*Z[1]/(Z[0]*Z[0]*Z[0]*Z[0])))]
			else : ZPerc=[0.,0.]
			if W[0]>0 : 
				Wperc =  [100*(abs(W_diff[0]-W[0])/W[0]),100*math.sqrt((math.sqrt(W_diff[1]*W_diff[1]+W[1]*W[1])/(W[0]*W[0]))+
								       ((W_diff[0]-W[0])*(W_diff[0]-W[0])*W[1]*W[1]/(W[0]*W[0]*W[0]*W[0])))]
			else : Wperc=[0.,0.]
			if tt[0]>0 : 
				TTperc =  [100*(abs(tt_diff[0]-tt[0])/tt[0]),100*math.sqrt((math.sqrt(tt_diff[1]*tt_diff[1]+tt[1]*tt[1])/(tt[0]*tt[0]))+
									   ((tt_diff[0]-tt[0])*(tt_diff[0]-tt[0])*tt[1]*tt[1]/(tt[0]*tt[0]*tt[0]*tt[0])))]
			else : TTperc=[0.,0.]
		
			print '        Z:',Zperc
			print '        W:',Wperc
			print '       tt:',TTperc
			if Zperc[0]>maxZ[0]  : maxZ = Zperc
			if Wperc[0]>maxW[0]  : maxW = Wperc
			if TTperc[0]>maxTT[0]: maxTT=TTperc
			if scaleWeights[-1] in weight:		
				print ' Final  Z:',maxZ
				print ' Final  W:',maxW
				print ' Final tt:',maxTT
	
		shapesysvar_Zjets.append (round(maxZ[0],2))
		shapesysvar_Wjets.append (round(maxW[0],2))
		shapesysvar_TTjets.append(round(maxTT[0],2))
		
	print '\n\n--------------\n--------------\nFinal systematics:'
	sys.stdout.write('shapesysvar')
	sys.stdout.write(channel)
        sys.stdout.write('_zjets = ')
        sys.stdout.write(shapesysvar_Zjets)

	sys.stdout.write('shapesysvar')
        sys.stdout.write(channel)
        sys.stdout.write('_wjets = ')
        sys.stdout.write(shapesysvar_Wjets)

	sys.stdout.write('shapesysvar')
        sys.stdout.write(channel)
        sys.stdout.write('ttjets = ')
        sys.stdout.write(shapesysvar_TTjets)

	#these have 3 extra entries before signal starts
	#shapesysvar_uujj_zjets =  [16.35, 9.46, 12.27, 17.14, 16.0, 16.53, 17.01, 16.68, 16.4, 16.34, 16.22, 16.22, 16.25, 16.09, 16.25, 16.57, 16.74, 16.88, 17.3, 17.45, 17.94, 18.16, 18.12, 19.22, 18.91, 19.42, 19.37, 19.56, 19.51, 18.3, 17.77, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24]
	#shapesysvar_uujj_wjets =  [17.24, 9.89, 29.31, 24.0, 23.73, 24.28, 24.46, 24.55, 24.32, 25.25, 25.76, 26.19, 25.6, 26.6, 26.98, 28.27, 28.01, 27.78, 27.78, 27.78, 27.78, 27.78, 27.78, 27.78, 27.78, 27.44, 27.44, 28.36, 28.36, 28.36, 28.36, 28.36, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	#shapesysvar_uujj_ttjets =  [33.0, 33.01, 35.65, 35.19, 35.24, 36.16, 37.41, 39.09, 40.03, 40.9, 41.67, 42.47, 43.18, 43.87, 44.21, 44.56, 45.91, 47.12, 47.9, 48.52, 49.2, 47.6, 47.23, 47.62, 47.73, 45.32, 43.66, 44.82, 45.28, 44.54, 45.37, 45.37, 45.37, 47.85, 47.85, 47.85, 47.85, 47.85, 47.85, 47.85]

def blind(h):
	for bin in range(h.GetNbinsX()):
		h.SetBinContent(bin+1,1.0)
		h.SetBinError(bin+1,0.0)
	h.SetMarkerSize(0.0)
	h.SetLineWidth(0)

main()
