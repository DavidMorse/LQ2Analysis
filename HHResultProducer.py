import os, sys, math, random, platform
from glob import glob


#global preselectionmumu

##########################################################################
########    GLOBAL VARIABLES NEEDED FOR PLOTS AND ANALYSIS        ########
##########################################################################

# Directory where root files are kept and the tree you want to get root files from

if 'cmsneu' in platform.node():
	#NormalDirectory = '/media/dataPlus/dmorse/hhNtuples/NTupleAnalyzerHH_newBDTs_2018_02_27/SummaryFiles'
	#QCDDirectory = '/media/dataPlus/dmorse/hhNtuples/NTupleAnalyzerHH_newBDTs_QCDNonIsoQuickTest_2018_02_27/SummaryFiles'
	NormalDirectory = '/media/dataPlus/dmorse/hhNtuples/NTupleAnalyzerHH_hhFullV2310_QuickTest_2018_05_29/SummaryFiles'
	QCDDirectory = '/media/dataPlus/dmorse/hhNtuples/NTupleAnalyzerHH_hhFullV2310_QCDNonIsoQuickTest_2018_05_29/SummaryFiles'
	EMuDirectory = 'emu'

else:
	print 'Not running on cmsneu!'
	#exit()
	NormalDirectory = '/eos/cms/store/user/dmorse/diHiggs_HHToZZbb/NTupleAnalyzerHH_newBDTs_2018_02_27/SummaryFiles'
	QCDDirectory = '/eos/cms/store/user/dmorse/diHiggs_HHToZZbb/NTupleAnalyzerHH_newBDTs_QCDNonIsoQuickTest_2018_02_27/SummaryFiles'
	EMuDirectory = 'emu'

# The name of the main ttree (ntuple structure)
TreeName = "PhysicalVariables"

# Integrated luminosity for normalization
#lumi =  2318.348
#lumi = 2690.707
#lumi = 40000.0
#lumi = 21780.339
#lumi = 35863.308
lumi = 35860.066

#HLT_Ele17_Ele12...DZ
##lumi=20809.806

#HLT_Ele23_Ele12...DZ
#lumi=27213.867

#Muon HLT MC scale factor
#https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2

# Single-mu trigger efficiencies as a function of muon Eta. 
# This is for the case of one muon
#2012#singleMuonHLT =  '*( 0.93*(abs(Eta_muon1)<=0.9) + 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) + 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) )'
singleMuonHLT =  '*( 0.9494*(abs(Eta_muon1)<=0.9)*(Pt_muon1>50)*(Pt_muon1<60) + 0.9460*(abs(Eta_muon1)<=0.9)*(Pt_muon1>60) + 0.9030*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>50)*(Pt_muon1<60) + 0.8968*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>60) + 0.9153*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>50)*(Pt_muon1<60) + 0.9175*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>60) )'
# This is for the case of two muons (i.e. the above factors, but for the case where the event has two muons)
#2012#doubleMuonHLT =  '*(1.0-(( 1.0 - 0.93*(abs(Eta_muon1)<=0.9) - 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) - 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) )'
#2012#doubleMuonHLT += '*( 1.0 - 0.93*(abs(Eta_muon2)<=0.9) - 0.83*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2) - 0.80*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1) )))'
#doubleMuonHLT =  '*(1.0-(( 1.0 - 0.9494*(abs(Eta_muon1)<=0.9)*(Pt_muon1>50)*(Pt_muon1<60) - 0.9460*(abs(Eta_muon1)<=0.9)*(Pt_muon1>60) - 0.9030*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>50)*(Pt_muon1<60) - 0.8968*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>60) - 0.9153*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>50)*(Pt_muon1<60) - 0.9175*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>60) )'
#doubleMuonHLT += '*( 1.0 - 0.9494*(abs(Eta_muon2)<=0.9)*(Pt_muon2>50)*(Pt_muon2<60) - 0.9460*(abs(Eta_muon2)<=0.9)*(Pt_muon2>60) - 0.9030*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>50)*(Pt_muon2<60) - 0.8968*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>60) - 0.9153*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>50)*(Pt_muon2<60) - 0.9175*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>60) )))'


#fixme todo this is applying a weight of .995 for two central muons, which is 1-(1-eff1)*(1-eff2)= eff1+eff2 - eff1*eff2.  Using now instead just eff1*eff2
#doubleMuonHLT =  '*((( 0.93*(abs(Eta_muon1)<=0.9) + 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) + 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) ))'
#doubleMuonHLT += '*( 0.93*(abs(Eta_muon2)<=0.9) + 0.83*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2) + 0.80*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1) ))'

#2015 values, taken from AN2016_021_v6.pdf
doubleMuonHLT = '*((abs(Eta_muon1)<=0.9)*(0.9490*(abs(Eta_muon2)<=0.9)+0.9490*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.4)+0.9376*(abs(Eta_muon2)>1.4)*(abs(Eta_muon2)<=2.1)+0.9207*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4))+(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.4)*(0.9628*(abs(Eta_muon2)<=0.9)+0.9576*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.4)+0.9288*(abs(Eta_muon2)>1.4)*(abs(Eta_muon2)<=2.1)+0.9684*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4))+(abs(Eta_muon1)>1.4)*(abs(Eta_muon1)<=2.1)*(0.9477*(abs(Eta_muon2)<=0.9)+0.9493*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.4)+0.9216*(abs(Eta_muon2)>1.4)*(abs(Eta_muon2)<=2.1)+0.9333*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4))+(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<=2.4)*(0.9420*(abs(Eta_muon2)<=0.9)+0.9142*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.4)+0.9470*(abs(Eta_muon2)>1.4)*(abs(Eta_muon2)<=2.1)+0.9252*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4)))'

#No longer using HLT SF
doubleMuonHLT = '*(1.0)'



doubleElectronHLTAndId = '*(ele1hltSF*ele2hltSF*ele1IDandIsoSF*ele2IDandIsoSF)'


# This is for the case of the E-mu sample, where one "muon" is replaced by an electron. In that case, we check
# which muon is a real muon (IsMuon_muon1) and apply the trigger efficiency based on the muon
#2012#singleMuonHLTEMU = '*((IsMuon_muon1*( 0.93*(abs(Eta_muon1)<=0.9) + 0.83*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2) + 0.80*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1) ))'
#2012#singleMuonHLTEMU += '+(IsMuon_muon2*( 0.93*(abs(Eta_muon2)<=0.9) + 0.83*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2) + 0.80*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1) )))'
singleMuonHLTEMU = '*((IsMuon_muon1*( 0.9494*(abs(Eta_muon1)<=0.9)*(Pt_muon1>50)*(Pt_muon1<60) + 0.9460*(abs(Eta_muon1)<=0.9)*(Pt_muon1>60) + 0.9030*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>50)*(Pt_muon1<60) + 0.8968*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>60) + 0.9153*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>50)*(Pt_muon1<60) + 0.9175*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>60) ))'
singleMuonHLTEMU += '+(IsMuon_muon2*( 0.9494*(abs(Eta_muon2)<=0.9)*(Pt_muon2>50)*(Pt_muon2<60) + 0.9460*(abs(Eta_muon2)<=0.9)*(Pt_muon2>60) + 0.9030*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>50)*(Pt_muon2<60) + 0.8968*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>60) + 0.9153*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>50)*(Pt_muon2<60) + 0.9175*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>60) )))'

#Muon ID and Iso MC scale factors
#https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2


#doubleMuonIdAndIsoScale = '*((0.9837160408450394*(Eta_muon1>-2.4)*(Eta_muon1>-2.1)+0.9945438368059955*(Eta_muon1>-2.1)*(Eta_muon1>-1.6)+0.9970378022168973*(Eta_muon1>-1.6)*(Eta_muon1>-1.2)+0.9956615088416513*(Eta_muon1>-1.2)*(Eta_muon1>-0.9)+0.9978576536660979*(Eta_muon1>-0.9)*(Eta_muon1>-0.3)+0.9924072276003321*(Eta_muon1>-0.0)*(Eta_muon1>-0.2)+0.9966624814619885*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.9940334796698915*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998044399081353*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.9952984093114865*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.9967601541976385*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.9959660681513732*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.9858520897236493*(Eta_muon1>2.1)*(Eta_muon1<2.4))*(0.9837160408450394*(Eta_muon1>-2.4)*(Eta_muon1>-2.1)+0.9945438368059955*(Eta_muon1>-2.1)*(Eta_muon1>-1.6)+0.9970378022168973*(Eta_muon1>-1.6)*(Eta_muon1>-1.2)+0.9956615088416513*(Eta_muon1>-1.2)*(Eta_muon1>-0.9)+0.9978576536660979*(Eta_muon1>-0.9)*(Eta_muon1>-0.3)+0.9924072276003321*(Eta_muon1>-0.0)*(Eta_muon1>-0.2)+0.9966624814619885*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.9940334796698915*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998044399081353*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.9952984093114865*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.9967601541976385*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.9959660681513732*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.9858520897236493*(Eta_muon1>2.1)*(Eta_muon1<2.4)))'

# AH:
#doubleMuonIdAndIsoScale = '*((0.9837*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.9945*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.9970*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.9957*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.9979*(Eta_muon1>-0.9)*(Eta_muon1<-0.3)+0.9924*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.9967*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.9940*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.9980*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.9953*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.9968*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.9960*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.9859*(Eta_muon1>2.1)*(Eta_muon1<2.4))*(0.9837*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.9945*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.9970*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.9957*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.9979*(Eta_muon2>-0.9)*(Eta_muon2<-0.3)+0.9924*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.9967*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.9940*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.9980*(Eta_muon2>0.3)*(Eta_muon2<0.9)+0.9953*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.9968*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.9960*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.9859*(Eta_muon2>2.1)*(Eta_muon2<2.4)))'

#DM -Update mixing Medium2016 for BCDEF and Medium for GH
doubleMuonIdAndIsoScale = '*((0.9675*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.9891*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.9941*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.9913*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.9957*(Eta_muon1>-0.9)*(Eta_muon1<-0.3)+0.9848*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.9933*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.9881*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.9961*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.9906*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.9935*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.9919*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.9717*(Eta_muon1>2.1)*(Eta_muon1<2.4))*(0.9675*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.9891*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.9941*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.9913*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.9957*(Eta_muon2>-0.9)*(Eta_muon2<-0.3)+0.9848*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.9933*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.9881*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.9961*(Eta_muon2>0.3)*(Eta_muon2<0.9)+0.9906*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.9935*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.9919*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.9717*(Eta_muon2>2.1)*(Eta_muon2<2.4)))'

doubleMuonIdScale = '*(0.9682423360434217*(Eta_muon1<-2.4)*(Eta_muon1>-2.1)+0.9893833099668479*(Eta_muon1<-2.1)*(Eta_muon1>-1.6)+0.9943077120257308*(Eta_muon1<-1.6)*(Eta_muon1>-1.2)+0.9916914851938796*(Eta_muon1<-1.2)*(Eta_muon1>-0.9)+0.995621634743804*(Eta_muon1<-0.9)*(Eta_muon1>-0.3)+0.9852246225934387*(Eta_muon1<-0.0)*(Eta_muon1>-0.2)+0.9939788646593908*(Eta_muon1<-0.2)*(Eta_muon1>0.2)+0.9885359568100729*(Eta_muon1<0.2)*(Eta_muon1>0.3)+0.9958132831910403*(Eta_muon1<0.3)*(Eta_muon1>0.9)+0.9902529688519877*(Eta_muon1<0.9)*(Eta_muon1>1.2)+0.9934874686188648*(Eta_muon1<1.2)*(Eta_muon1>1.6)+0.9923028170743358*(Eta_muon1<1.6)*(Eta_muon1>2.1)+0.9724438481770842*(Eta_muon1<2.1)*(Eta_muon1>2.4))*(0.9682423360434217*(Eta_muon2<-2.4)*(Eta_muon2>-2.1)+0.9893833099668479*(Eta_muon2<-2.1)*(Eta_muon2>-1.6)+0.9943077120257308*(Eta_muon2<-1.6)*(Eta_muon2>-1.2)+0.9916914851938796*(Eta_muon2<-1.2)*(Eta_muon2>-0.9)+0.995621634743804*(Eta_muon2<-0.9)*(Eta_muon2>-0.3)+0.9852246225934387*(Eta_muon2<-0.0)*(Eta_muon2>-0.2)+0.9939788646593908*(Eta_muon2<-0.2)*(Eta_muon2>0.2)+0.9885359568100729*(Eta_muon2<0.2)*(Eta_muon2>0.3)+0.9958132831910403*(Eta_muon2<0.3)*(Eta_muon2>0.9)+0.9902529688519877*(Eta_muon2<0.9)*(Eta_muon2>1.2)+0.9934874686188648*(Eta_muon2<1.2)*(Eta_muon2>1.6)+0.9923028170743358*(Eta_muon2<1.6)*(Eta_muon2>2.1)+0.9724438481770842*(Eta_muon2<2.1)*(Eta_muon2>2.4))'

#doubleMuonIdScale = '*((0.9813326964101629*(Pt_muon1>50)*(Pt_muon1<55)+0.9811215588407185*(Pt_muon1>55)*(Pt_muon1<60)+0.9888030350742609*(Pt_muon1>60)*(Pt_muon1<120)+1.0179598732419621*(Pt_muon1>120))*(0.9813326964101629*(Pt_muon2>50)*(Pt_muon2<55)+0.9811215588407185*(Pt_muon2>55)*(Pt_muon2<60)+0.9888030350742609*(Pt_muon2>60)*(Pt_muon2<120)+1.0179598732419621*(Pt_muon2>120)))'

doubleMuonIsoScale = '*(0.999189745646657*(Eta_muon1<-2.4)*(Eta_muon1>-2.1)+0.999704363645143*(Eta_muon1<-2.1)*(Eta_muon1>-1.6)+0.9997678924080637*(Eta_muon1<-1.6)*(Eta_muon1>-1.2)+0.9996315324894229*(Eta_muon1<-1.2)*(Eta_muon1>-0.9)+1.0000936725883918*(Eta_muon1<-0.9)*(Eta_muon1>-0.3)+0.9995898326072254*(Eta_muon1<-0.0)*(Eta_muon1>-0.2)+0.9993460982645863*(Eta_muon1<-0.2)*(Eta_muon1>0.2)+0.9995310025297102*(Eta_muon1<0.2)*(Eta_muon1>0.3)+1.0002755149716656*(Eta_muon1<0.3)*(Eta_muon1>0.9)+1.0003438497709853*(Eta_muon1<0.9)*(Eta_muon1>1.2)+1.0000328397764122*(Eta_muon1<1.2)*(Eta_muon1>1.6)+0.9996293192284107*(Eta_muon1<1.6)*(Eta_muon1>2.1)+0.9992603312702144*(Eta_muon1<2.1)*(Eta_muon1>2.4))*(0.999189745646657*(Eta_muon2<-2.4)*(Eta_muon2>-2.1)+0.999704363645143*(Eta_muon2<-2.1)*(Eta_muon2>-1.6)+0.9997678924080637*(Eta_muon2<-1.6)*(Eta_muon2>-1.2)+0.9996315324894229*(Eta_muon2<-1.2)*(Eta_muon2>-0.9)+1.0000936725883918*(Eta_muon2<-0.9)*(Eta_muon2>-0.3)+0.9995898326072254*(Eta_muon2<-0.0)*(Eta_muon2>-0.2)+0.9993460982645863*(Eta_muon2<-0.2)*(Eta_muon2>0.2)+0.9995310025297102*(Eta_muon2<0.2)*(Eta_muon2>0.3)+1.0002755149716656*(Eta_muon2<0.3)*(Eta_muon2>0.9)+1.0003438497709853*(Eta_muon2<0.9)*(Eta_muon2>1.2)+1.0000328397764122*(Eta_muon2<1.2)*(Eta_muon2>1.6)+0.9996293192284107*(Eta_muon2<1.6)*(Eta_muon2>2.1)+0.9992603312702144*(Eta_muon2<2.1)*(Eta_muon2>2.4))'

#doubleMuonIsoScale = '*((0.9985465327438463*(Pt_muon1>50)*(Pt_muon1<55)+0.9988891755735836*(Pt_muon1>55)*(Pt_muon1<60)+0.9989480835906359*(Pt_muon1>60)*(Pt_muon1<120)+1.0006806854046033*(Pt_muon1>120))*(0.9985465327438463*(Pt_muon2>50)*(Pt_muon2<55)+0.9988891755735836*(Pt_muon2>55)*(Pt_muon2<60)+0.9989480835906359*(Pt_muon2>60)*(Pt_muon2<120)+1.0006806854046033*(Pt_muon2>120)))'

#fracBCDEF2016 = '(0.542239493)'
#fracGH2016    = '(0.457760507)'

doubleMuonIdAndIsoScale = '*((0.542239493)*medID2016mu1*((abs(Eta_muon1)<0.9)*(0.987*(Pt_muon1<25)+0.987*(Pt_muon1>25)*(Pt_muon1<30)+0.998*(Pt_muon1>30)*(Pt_muon1<40)+0.992*(Pt_muon1>40)*(Pt_muon1<50)+0.985*(Pt_muon1>50)*(Pt_muon1<60)+1.010*(Pt_muon1>60))+(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<1.2)*(0.975*(Pt_muon1<25)+0.969*(Pt_muon1>25)*(Pt_muon1<30)+0.979*(Pt_muon1>30)*(Pt_muon1<40)+0.983*(Pt_muon1>40)*(Pt_muon1<50)+0.982*(Pt_muon1>50)*(Pt_muon1<60)+0.981*(Pt_muon1>60))+(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<2.1)*(0.986*(Pt_muon1<25)+0.982*(Pt_muon1>25)*(Pt_muon1<30)+0.987*(Pt_muon1>30)*(Pt_muon1<40)+0.991*(Pt_muon1>40)*(Pt_muon1<50)+0.985*(Pt_muon1>50)*(Pt_muon1<60)+0.993*(Pt_muon1>60))+(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<2.4)*(0.945*(Pt_muon1<25)+0.942*(Pt_muon1>25)*(Pt_muon1<30)+0.940*(Pt_muon1>30)*(Pt_muon1<40)+0.943*(Pt_muon1>40)*(Pt_muon1<50)+0.941*(Pt_muon1>50)*(Pt_muon1<60)+0.942*(Pt_muon1>60))) + (0.457760507)*medIDmu1*((abs(Eta_muon1)<0.9)*(0.993*(Pt_muon1<25)+0.994*(Pt_muon1>25)*(Pt_muon1<30)+1.000*(Pt_muon1>30)*(Pt_muon1<40)+0.998*(Pt_muon1>40)*(Pt_muon1<50)+0.993*(Pt_muon1>50)*(Pt_muon1<60)+1.000*(Pt_muon1>60))+(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<1.2)*(0.998*(Pt_muon1<25)+0.999*(Pt_muon1>25)*(Pt_muon1<30)+0.998*(Pt_muon1>30)*(Pt_muon1<40)+0.997*(Pt_muon1>40)*(Pt_muon1<50)+0.993*(Pt_muon1>50)*(Pt_muon1<60)+0.999*(Pt_muon1>60))+(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<2.1)*(0.998*(Pt_muon1<25)+0.999*(Pt_muon1>25)*(Pt_muon1<30)+0.999*(Pt_muon1>30)*(Pt_muon1<40)+0.996*(Pt_muon1>40)*(Pt_muon1<50)+0.991*(Pt_muon1>50)*(Pt_muon1<60)+0.995*(Pt_muon1>60))+(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<2.4)*(0.984*(Pt_muon1<25)+0.983*(Pt_muon1>25)*(Pt_muon1<30)+0.975*(Pt_muon1>30)*(Pt_muon1<40)+0.975*(Pt_muon1>40)*(Pt_muon1<50)+0.970*(Pt_muon1>50)*(Pt_muon1<60)+0.971*(Pt_muon1>60))))*((0.542239493)*medID2016mu2*((abs(Eta_muon2)<0.9)*(0.987*(Pt_muon2<25)+0.987*(Pt_muon2>25)*(Pt_muon2<30)+0.998*(Pt_muon2>30)*(Pt_muon2<40)+0.992*(Pt_muon2>40)*(Pt_muon2<50)+0.985*(Pt_muon2>50)*(Pt_muon2<60)+1.010*(Pt_muon2>60))+(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<1.2)*(0.975*(Pt_muon2<25)+0.969*(Pt_muon2>25)*(Pt_muon2<30)+0.979*(Pt_muon2>30)*(Pt_muon2<40)+0.983*(Pt_muon2>40)*(Pt_muon2<50)+0.982*(Pt_muon2>50)*(Pt_muon2<60)+0.981*(Pt_muon2>60))+(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<2.1)*(0.986*(Pt_muon2<25)+0.982*(Pt_muon2>25)*(Pt_muon2<30)+0.987*(Pt_muon2>30)*(Pt_muon2<40)+0.991*(Pt_muon2>40)*(Pt_muon2<50)+0.985*(Pt_muon2>50)*(Pt_muon2<60)+0.993*(Pt_muon2>60))+(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<2.4)*(0.945*(Pt_muon2<25)+0.942*(Pt_muon2>25)*(Pt_muon2<30)+0.940*(Pt_muon2>30)*(Pt_muon2<40)+0.943*(Pt_muon2>40)*(Pt_muon2<50)+0.941*(Pt_muon2>50)*(Pt_muon2<60)+0.942*(Pt_muon2>60))) + (0.457760507)*medIDmu1*((abs(Eta_muon2)<0.9)*(0.993*(Pt_muon2<25)+0.994*(Pt_muon2>25)*(Pt_muon2<30)+1.000*(Pt_muon2>30)*(Pt_muon2<40)+0.998*(Pt_muon2>40)*(Pt_muon2<50)+0.993*(Pt_muon2>50)*(Pt_muon2<60)+1.000*(Pt_muon2>60))+(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<1.2)*(0.998*(Pt_muon2<25)+0.999*(Pt_muon2>25)*(Pt_muon2<30)+0.998*(Pt_muon2>30)*(Pt_muon2<40)+0.997*(Pt_muon2>40)*(Pt_muon2<50)+0.993*(Pt_muon2>50)*(Pt_muon2<60)+0.999*(Pt_muon2>60))+(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<2.1)*(0.998*(Pt_muon2<25)+0.999*(Pt_muon2>25)*(Pt_muon2<30)+0.999*(Pt_muon2>30)*(Pt_muon2<40)+0.996*(Pt_muon2>40)*(Pt_muon2<50)+0.991*(Pt_muon2>50)*(Pt_muon2<60)+0.995*(Pt_muon2>60))+(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<2.4)*(0.984*(Pt_muon2<25)+0.983*(Pt_muon2>25)*(Pt_muon2<30)+0.975*(Pt_muon2>30)*(Pt_muon2<40)+0.975*(Pt_muon2>40)*(Pt_muon2<50)+0.970*(Pt_muon2>50)*(Pt_muon2<60)+0.971*(Pt_muon2>60))))'


singleMuonIdScale = '*(0.9813326964101629*(Pt_muon1>50)*(Pt_muon1<55)+0.9811215588407185*(Pt_muon1>55)*(Pt_muon1<60)+0.9888030350742609*(Pt_muon1>60)*(Pt_muon1<120)+1.0179598732419621*(Pt_muon1>120))'

singleMuonIsoScale = '*(0.9985465327438463*(Pt_muon1>50)*(Pt_muon1<55)+0.9988891755735836*(Pt_muon1>55)*(Pt_muon1<60)+0.9989480835906359*(Pt_muon1>60)*(Pt_muon1<120)+1.0006806854046033*(Pt_muon1>120))'

MuIdScaleEMU = '*(IsMuon_muon1*(0.9813326964101629*(Pt_muon1>50)*(Pt_muon1<55)+0.9811215588407185*(Pt_muon1>55)*(Pt_muon1<60)+0.9888030350742609*(Pt_muon1>60)*(Pt_muon1<120)+1.0179598732419621*(Pt_muon1>120))+IsMuon_muon2*(0.9813326964101629*(Pt_muon2>50)*(Pt_muon2<55)+0.9811215588407185*(Pt_muon2>55)*(Pt_muon2<60)+0.9888030350742609*(Pt_muon2>60)*(Pt_muon2<120)+1.0179598732419621*(Pt_muon2>120)))'

MuIsoScaleEMU = '*(IsMuon_muon1*(0.9985465327438463*(Pt_muon1>50)*(Pt_muon1<55)+0.9988891755735836*(Pt_muon1>55)*(Pt_muon1<60)+0.9989480835906359*(Pt_muon1>60)*(Pt_muon1<120)+1.0006806854046033*(Pt_muon1>120))+IsMuon_muon2*(0.9985465327438463*(Pt_muon2>50)*(Pt_muon2<55)+0.9988891755735836*(Pt_muon2>55)*(Pt_muon2<60)+0.9989480835906359*(Pt_muon2>60)*(Pt_muon2<120)+1.0006806854046033*(Pt_muon2>120)))'


# This is the rescaling of the EMu data for the ttbar estimate (2 - Eff_trigger)
dataHLTEMUADJ = '*(2.0 - 1.0'+singleMuonHLTEMU+')'


# bTag scale factors: https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#1c_Event_reweighting_using_scale

# For case of >=1 bTag: w(>= 1|n) = 1 - w(0|n), where  w(0|n) = \prod_{i=1}^n (1-SF_i)
bTag1SFloose = '*(1-(1-(CMVA_bjet1>-0.5884)*Hjet1BsfLoose)*(1-(CMVA_bjet2>-0.5884)*Hjet2BsfLoose)*(1-(CMVA_Zjet1>-0.5884)*Zjet1BsfLoose)*(1-(CMVA_Zjet2>-0.5884)*Zjet2BsfLoose))'

#bTag1SFmedium = '*(1-(1-(CMVA_bjet1>-0.5884)*0.600657*((1.+(0.753343*Pt_Hjet1))/(1.+(0.472587*Pt_Hjet1))))*(1-(CMVA_bjet2>-0.5884)*0.600657*((1.+(0.753343*Pt_Hjet2))/(1.+(0.472587*Pt_Hjet2))))*(1-(CMVA_Zjet1>-0.5884)*0.600657*((1.+(0.753343*Pt_Zjet1))/(1.+(0.472587*Pt_Zjet1))))*(1-(CMVA_Zjet2>-0.5884)*0.600657*((1.+(0.753343*Pt_Zjet2))/(1.+(0.472587*Pt_Zjet2)))))'
bTag1SFmedium = '*(1-(1-(CMVA_bjet1>0.4432)*Hjet1BsfMedium)*(1-(CMVA_bjet2>0.4432)*Hjet2BsfMedium)*(1-(CMVA_Zjet1>0.4432)*Zjet1BsfMedium)*(1-(CMVA_Zjet2>0.4432)*Zjet2BsfMedium))'
bTag1SFmediumUp = '*(1-(1-(CMVA_bjet1>0.4432)*Hjet1BsfMediumUp)*(1-(CMVA_bjet2>0.4432)*Hjet2BsfMediumUp)*(1-(CMVA_Zjet1>0.4432)*Zjet1BsfMediumUp)*(1-(CMVA_Zjet2>0.4432)*Zjet2BsfMediumUp))'
bTag1SFmediumDown = '*(1-(1-(CMVA_bjet1>0.4432)*Hjet1BsfMediumDown)*(1-(CMVA_bjet2>0.4432)*Hjet2BsfMediumDown)*(1-(CMVA_Zjet1>0.4432)*Zjet1BsfMediumDown)*(1-(CMVA_Zjet2>0.4432)*Zjet2BsfMediumDown))'



# For case of >=2 bTag: w(>= 2|n) = 1 - w(0|n) - w(1|n), where  w(1|n) = \sum_{j=1}^n [ \prod_{i=1, i!=j}^n (1-SF_i) ]*SF_j
#bTag2SFloose = '*(1-(1-(CMVA_bjet1>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Hjet1))))*(1-(CMVA_bjet2>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Hjet2))))*(1-(CMVA_Zjet1>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Zjet1))))*(1-(CMVA_Zjet2>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Zjet2))))-((CMVA_bjet1>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Hjet1))))*(1-(CMVA_bjet2>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Hjet2))))*(1-(CMVA_Zjet1>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Zjet1))))*(1-(CMVA_Zjet2>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Zjet2))))-(1-(CMVA_bjet1>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Hjet1))))*((CMVA_bjet2>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Hjet2))))*(1-(CMVA_Zjet1>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Zjet1))))*(1-(CMVA_Zjet2>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Zjet2))))-(1-(CMVA_bjet1>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Hjet1))))*(1-(CMVA_bjet2>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Hjet2))))*((CMVA_Zjet1>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Zjet1))))*(1-(CMVA_Zjet2>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Zjet2))))-(1-(CMVA_bjet1>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Hjet1))))*(1-(CMVA_bjet2>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Hjet2))))*(1-(CMVA_Zjet1>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Zjet1))))*((CMVA_Zjet2>-0.5884)*(0.976111+(-(4.37632e-05*Pt_Zjet2)))))'

#This is for HIP problem https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2#Tracking_efficiency_provided_by
trackerHIP1 = '*(0.991237*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.994853*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.996413*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.997157*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.997512*(Eta_muon1>-0.9)*(Eta_muon1<-0.6)+0.99756*(Eta_muon1>-0.6)*(Eta_muon1<-0.3)+0.996745*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.996996*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.99772*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998604*(Eta_muon1>0.3)*(Eta_muon1<0.6)+0.998321*(Eta_muon1>0.6)*(Eta_muon1<0.9)+0.997682*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.995252*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.994919*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.987334*(Eta_muon1>2.1)*(Eta_muon1<2.4) )'
trackerHIP2 = '*(0.991237*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.994853*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.996413*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.997157*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.997512*(Eta_muon2>-0.9)*(Eta_muon2<-0.6)+0.99756*(Eta_muon2>-0.6)*(Eta_muon2<-0.3)+0.996745*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.996996*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.99772*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.998604*(Eta_muon2>0.3)*(Eta_muon2<0.6)+0.998321*(Eta_muon2>0.6)*(Eta_muon2<0.9)+0.997682*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.995252*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.994919*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.987334*(Eta_muon2>2.1)*(Eta_muon2<2.4) )'

trackerHIPEMU  = '*((IsMuon_muon1)*(0.991237*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.994853*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.996413*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.997157*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.997512*(Eta_muon1>-0.9)*(Eta_muon1<-0.6)+0.99756*(Eta_muon1>-0.6)*(Eta_muon1<-0.3)+0.996745*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.996996*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.99772*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998604*(Eta_muon1>0.3)*(Eta_muon1<0.6)+0.998321*(Eta_muon1>0.6)*(Eta_muon1<0.9)+0.997682*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.995252*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.994919*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.987334*(Eta_muon1>2.1)*(Eta_muon1<2.4) )'
trackerHIPEMU += '+(IsMuon_muon2)*(0.991237*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.994853*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.996413*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.997157*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.997512*(Eta_muon2>-0.9)*(Eta_muon2<-0.6)+0.99756*(Eta_muon2>-0.6)*(Eta_muon2<-0.3)+0.996745*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.996996*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.99772*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.998604*(Eta_muon2>0.3)*(Eta_muon2<0.6)+0.998321*(Eta_muon2>0.6)*(Eta_muon2<0.9)+0.997682*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.995252*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.994919*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.987334*(Eta_muon2>2.1)*(Eta_muon2<2.4) ))'

eleRECOScale = '*((1.3176*(Eta_ele1>-2.5)*(Eta_ele1<-2.45)+1.11378*(Eta_ele1>-2.45)*(Eta_ele1<-2.4)+1.02463*(Eta_ele1>-2.4)*(Eta_ele1<-2.3)+1.01364*(Eta_ele1>-2.3)*(Eta_ele1<-2.2)+1.00728*(Eta_ele1>-2.2)*(Eta_ele1<-2)+0.994819*(Eta_ele1>-2)*(Eta_ele1<-1.8)+0.994786*(Eta_ele1>-1.8)*(Eta_ele1<-1.63)+0.991632*(Eta_ele1>-1.63)*(Eta_ele1<-1.566)+0.963129*(Eta_ele1>-1.566)*(Eta_ele1<-1.444)+0.989701*(Eta_ele1>-1.444)*(Eta_ele1<-1.2)+0.985656*(Eta_ele1>-1.2)*(Eta_ele1<-1)+0.981595*(Eta_ele1>-1)*(Eta_ele1<-0.6)+0.984678*(Eta_ele1>-0.6)*(Eta_ele1<-0.4)+0.981614*(Eta_ele1>-0.4)*(Eta_ele1<-0.2)+0.980433*(Eta_ele1>-0.2)*(Eta_ele1<0)+0.984552*(Eta_ele1>0)*(Eta_ele1<0.2)+0.988764*(Eta_ele1>0.2)*(Eta_ele1<0.4)+0.987743*(Eta_ele1>0.4)*(Eta_ele1<0.6)+0.987743*(Eta_ele1>0.6)*(Eta_ele1<1)+0.987743*(Eta_ele1>1)*(Eta_ele1<1.2)+0.98768*(Eta_ele1>1.2)*(Eta_ele1<1.444)+0.967598*(Eta_ele1>1.444)*(Eta_ele1<1.566)+0.989627*(Eta_ele1>1.566)*(Eta_ele1<1.63)+0.992761*(Eta_ele1>1.63)*(Eta_ele1<1.8)+0.991761*(Eta_ele1>1.8)*(Eta_ele1<2)+0.99794*(Eta_ele1>2)*(Eta_ele1<2.2)+1.00104*(Eta_ele1>2.2)*(Eta_ele1<2.3)+0.989507*(Eta_ele1>2.3)*(Eta_ele1<2.4)+0.970519*(Eta_ele1>2.4)*(Eta_ele1<2.45)+0.906667*(Eta_ele1>2.45)*(Eta_ele1<2.5))'
eleRECOScale += '*(1.3176*(Eta_ele2>-2.5)*(Eta_ele2<-2.45)+1.11378*(Eta_ele2>-2.45)*(Eta_ele2<-2.4)+1.02463*(Eta_ele2>-2.4)*(Eta_ele2<-2.3)+1.01364*(Eta_ele2>-2.3)*(Eta_ele2<-2.2)+1.00728*(Eta_ele2>-2.2)*(Eta_ele2<-2)+0.994819*(Eta_ele2>-2)*(Eta_ele2<-1.8)+0.994786*(Eta_ele2>-1.8)*(Eta_ele2<-1.63)+0.991632*(Eta_ele2>-1.63)*(Eta_ele2<-1.566)+0.963129*(Eta_ele2>-1.566)*(Eta_ele2<-1.444)+0.989701*(Eta_ele2>-1.444)*(Eta_ele2<-1.2)+0.985656*(Eta_ele2>-1.2)*(Eta_ele2<-1)+0.981595*(Eta_ele2>-1)*(Eta_ele2<-0.6)+0.984678*(Eta_ele2>-0.6)*(Eta_ele2<-0.4)+0.981614*(Eta_ele2>-0.4)*(Eta_ele2<-0.2)+0.980433*(Eta_ele2>-0.2)*(Eta_ele2<0)+0.984552*(Eta_ele2>0)*(Eta_ele2<0.2)+0.988764*(Eta_ele2>0.2)*(Eta_ele2<0.4)+0.987743*(Eta_ele2>0.4)*(Eta_ele2<0.6)+0.987743*(Eta_ele2>0.6)*(Eta_ele2<1)+0.987743*(Eta_ele2>1)*(Eta_ele2<1.2)+0.98768*(Eta_ele2>1.2)*(Eta_ele2<1.444)+0.967598*(Eta_ele2>1.444)*(Eta_ele2<1.566)+0.989627*(Eta_ele2>1.566)*(Eta_ele2<1.63)+0.992761*(Eta_ele2>1.63)*(Eta_ele2<1.8)+0.991761*(Eta_ele2>1.8)*(Eta_ele2<2)+0.99794*(Eta_ele2>2)*(Eta_ele2<2.2)+1.00104*(Eta_ele2>2.2)*(Eta_ele2<2.3)+0.989507*(Eta_ele2>2.3)*(Eta_ele2<2.4)+0.970519*(Eta_ele2>2.4)*(Eta_ele2<2.45)+0.906667*(Eta_ele2>2.45)*(Eta_ele2<2.5)))'

#https://github.com/cp3-llbb/HHAnalysis/blob/master/data/ScaleFactors/Electron_MediumPlusHLTSafeID_moriond17.json
#doubleEleMedIdScale = '*(((Eta_ele1>-2.5)*(Eta_ele1<-2.0)*(0.7290*(Pt_ele1>10)*(Pt_ele1<20)+0.8077*(Pt_ele1>20)*(Pt_ele1<35)+0.8479*(Pt_ele1>35)*(Pt_ele1<50)+0.8685*(Pt_ele1>50)*(Pt_ele1<90)+0.9598*(Pt_ele1>90)*(Pt_ele1<150)+0.9463*(Pt_ele1>150))+(Eta_ele1>-2.0)*(Eta_ele1<-1.566)*(0.7845*(Pt_ele1>10)*(Pt_ele1<20)+0.8764*(Pt_ele1>20)*(Pt_ele1<35)+0.9074*(Pt_ele1>35)*(Pt_ele1<50)+0.9149*(Pt_ele1>50)*(Pt_ele1<90)+0.8977*(Pt_ele1>90)*(Pt_ele1<150)+0.8722*(Pt_ele1>150))+(Eta_ele1>-1.556)*(Eta_ele1<-1.444)*(0.7433*(Pt_ele1>10)*(Pt_ele1<20)+0.9792*(Pt_ele1>20)*(Pt_ele1<35)+0.9677*(Pt_ele1>35)*(Pt_ele1<50)+0.9706*(Pt_ele1>50)*(Pt_ele1<90)+1.0613*(Pt_ele1>90)*(Pt_ele1<150)+1.0465*(Pt_ele1>150))+(Eta_ele1>-1.444)*(Eta_ele1<-0.8)*(0.9809*(Pt_ele1>10)*(Pt_ele1<20)+0.9635*(Pt_ele1>20)*(Pt_ele1<35)+0.9705*(Pt_ele1>35)*(Pt_ele1<50)+0.9601*(Pt_ele1>50)*(Pt_ele1<90)+0.9329*(Pt_ele1>90)*(Pt_ele1<150)+0.9470*(Pt_ele1>150))+(Eta_ele1>-0.8)*(Eta_ele1<0.0)*(0.9356*(Pt_ele1>10)*(Pt_ele1<20)+0.9446*(Pt_ele1>20)*(Pt_ele1<35)+0.9490*(Pt_ele1>35)*(Pt_ele1<50)+0.9525*(Pt_ele1>50)*(Pt_ele1<90)+0.9506*(Pt_ele1>90)*(Pt_ele1<150)+0.9691*(Pt_ele1>150))+(Eta_ele1>0.0)*(Eta_ele1<0.8)*(0.9620*(Pt_ele1>10)*(Pt_ele1<20)+0.9706*(Pt_ele1>20)*(Pt_ele1<35)+0.9757*(Pt_ele1>35)*(Pt_ele1<50)+0.9764*(Pt_ele1>50)*(Pt_ele1<90)+0.9876*(Pt_ele1>90)*(Pt_ele1<150)+1.0066*(Pt_ele1>150))+(Eta_ele1>0.8)*(Eta_ele1<1.4444)*(0.9632*(Pt_ele1>10)*(Pt_ele1<20)+0.9532*(Pt_ele1>20)*(Pt_ele1<35)+0.9687*(Pt_ele1>35)*(Pt_ele1<50)+0.9759*(Pt_ele1>50)*(Pt_ele1<90)+0.9718*(Pt_ele1>90)*(Pt_ele1<150)+0.9574*(Pt_ele1>150))+(Eta_ele1>1.444)*(Eta_ele1<1.566)*(0.6824*(Pt_ele1>10)*(Pt_ele1<20)+0.9296*(Pt_ele1>20)*(Pt_ele1<35)+0.9477*(Pt_ele1>35)*(Pt_ele1<50)+0.9597*(Pt_ele1>50)*(Pt_ele1<90)+0.9450*(Pt_ele1>90)*(Pt_ele1<150)+0.8444*(Pt_ele1>150))+(Eta_ele1>1.566)*(Eta_ele1<2.0)*(0.8103*(Pt_ele1>10)*(Pt_ele1<20)+0.8592*(Pt_ele1>20)*(Pt_ele1<35)+0.9004*(Pt_ele1>35)*(Pt_ele1<50)+0.9140*(Pt_ele1>50)*(Pt_ele1<90)+0.9271*(Pt_ele1>90)*(Pt_ele1<150)+0.9074*(Pt_ele1>150))+(Eta_ele1>2.0)*(Eta_ele1<2.5)*(0.7256*(Pt_ele1>10)*(Pt_ele1<20)+0.7962*(Pt_ele1>20)*(Pt_ele1<35)+0.8453*(Pt_ele1>35)*(Pt_ele1<50)+0.8687*(Pt_ele1>50)*(Pt_ele1<90)+0.9123*(Pt_ele1>90)*(Pt_ele1<150)+0.9505*(Pt_ele1>150)))'
#doubleEleMedIdScale += '*((Eta_ele2>-2.5)*(Eta_ele2<-2.0)*(0.7290*(Pt_ele2>10)*(Pt_ele2<20)+0.8077*(Pt_ele2>20)*(Pt_ele2<35)+0.8479*(Pt_ele2>35)*(Pt_ele2<50)+0.8685*(Pt_ele2>50)*(Pt_ele2<90)+0.9598*(Pt_ele2>90)*(Pt_ele2<150)+ 0.9463*(Pt_ele2>150))+(Eta_ele2>-2.0)*(Eta_ele2<-1.566)*(0.7845*(Pt_ele2>10)*(Pt_ele2<20)+0.8764*(Pt_ele2>20)*(Pt_ele2<35)+0.9074*(Pt_ele2>35)*(Pt_ele2<50)+0.9149*(Pt_ele2>50)*(Pt_ele2<90)+0.8977*(Pt_ele2>90)*(Pt_ele2<150)+0.8722*(Pt_ele2>150))+(Eta_ele2>-1.556)*(Eta_ele2<-1.444)*(0.7433*(Pt_ele2>10)*(Pt_ele2<20)+0.9792*(Pt_ele2>20)*(Pt_ele2<35)+0.9677*(Pt_ele2>35)*(Pt_ele2<50)+0.9706*(Pt_ele2>50)*(Pt_ele2<90)+1.0613*(Pt_ele2>90)*(Pt_ele2<150)+1.0465*(Pt_ele2>150))+(Eta_ele2>-1.444)*(Eta_ele2<-0.8)*(0.9809*(Pt_ele2>10)*(Pt_ele2<20)+0.9635*(Pt_ele2>20)*(Pt_ele2<35)+0.9705*(Pt_ele2>35)*(Pt_ele2<50)+0.9601*(Pt_ele2>50)*(Pt_ele2<90)+0.9329*(Pt_ele2>90)*(Pt_ele2<150)+0.9470*(Pt_ele2>150))+(Eta_ele2>-0.8)*(Eta_ele2<0.0)*(0.9356*(Pt_ele2>10)*(Pt_ele2<20)+0.9446*(Pt_ele2>20)*(Pt_ele2<35)+0.9490*(Pt_ele2>35)*(Pt_ele2<50)+0.9525*(Pt_ele2>50)*(Pt_ele2<90)+0.9506*(Pt_ele2>90)*(Pt_ele2<150)+0.9691*(Pt_ele2>150))+(Eta_ele2>0.0)*(Eta_ele2<0.8)*(0.9620*(Pt_ele2>10)*(Pt_ele2<20)+ 0.9706*(Pt_ele2>20)*(Pt_ele2<35)+ 0.9757*(Pt_ele2>35)*(Pt_ele2<50)+0.9764*(Pt_ele2>50)*(Pt_ele2<90)+0.9876*(Pt_ele2>90)*(Pt_ele2<150)+1.0066*(Pt_ele2>150))+(Eta_ele2>0.8)*(Eta_ele2<1.4444)*(0.9632*(Pt_ele2>10)*(Pt_ele2<20)+0.9532*(Pt_ele2>20)*(Pt_ele2<35)+0.9687*(Pt_ele2>35)*(Pt_ele2<50)+0.9759*(Pt_ele2>50)*(Pt_ele2<90)+0.9718*(Pt_ele2>90)*(Pt_ele2<150)+0.9574*(Pt_ele2>150))+(Eta_ele2>1.444)*(Eta_ele2<1.566)*(0.6824*(Pt_ele2>10)*(Pt_ele2<20)+0.9296*(Pt_ele2>20)*(Pt_ele2<35)+0.9477*(Pt_ele2>35)*(Pt_ele2<50)+0.9597*(Pt_ele2>50)*(Pt_ele2<90)+0.9450*(Pt_ele2>90)*(Pt_ele2<150)+0.8444*(Pt_ele2>150))+(Eta_ele2>1.566)*(Eta_ele2<2.0)*(0.8103*(Pt_ele2>10)*(Pt_ele2<20)+0.8592*(Pt_ele2>20)*(Pt_ele2<35)+0.9004*(Pt_ele2>35)*(Pt_ele2<50)+0.9140*(Pt_ele2>50)*(Pt_ele2<90)+0.9271*(Pt_ele2>90)*(Pt_ele2<150)+0.9074*(Pt_ele2>150))+(Eta_ele2>2.0)*(Eta_ele2<2.5)*(0.7256*(Pt_ele2>10)*(Pt_ele2<20)+0.7962*(Pt_ele2>20)*(Pt_ele2<35)+0.8453*(Pt_ele2>35)*(Pt_ele2<50)+0.8687*(Pt_ele2>50)*(Pt_ele2<90)+0.9123*(Pt_ele2>90)*(Pt_ele2<150)+0.9505*(Pt_ele2>150))))'

# This is the real data trigger condition
dataHLTMuon = '*(pass_HLT_Mu17_Mu8)'
dataHLTElectron = '*(pass_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)'

# This is the set of event filters used
passfilter =  '*(passDataCert*passPrimaryVertex*(GoodVertexCount>=1))'
passfilter += '*(passHBHENoiseFilter*passHBHENoiseIsoFilter)'
passfilter += '*(passBadEESuperCrystal*passEcalDeadCellTP)'
passfilter += '*(passBeamHalo2016)'
passfilter += '*(passBadMuon*passBadChargedHadron)'
#passfilter += '*(noBadMuonsFlag*(1-duplicateMuonsFlag))'

# This defines the preselections for the mu-mu, mu-nu, and e-mu samples
#preselection_Muon_nos = '((Pt_muon1>20)*(Pt_muon2>10)*(Pt_Hjet1>20)*(Pt_Hjet2>20)*(Pt_Zjet1>20)*(Pt_Zjet2>20)*(M_uu>12)*(isMuonEvent))'
preselection_Muon_nos = '((pass_HLT_Mu17_Mu8)*(Pt_muon1>20)*(Pt_muon2>10)*(Pt_Hjet1>20)*(Pt_Hjet2>20)*(Pt_Zjet1>20)*(Pt_Zjet2>20)*(M_uu>12)*(isMuonEvent))'#*(1-(run_number==276950)*(lumi_number==22)*(event_number==34039924))*(1-(run_number==1)*(lumi_number==447098)*(event_number==71625048)))'
#preselection_Electron_nos = '((pass_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)*(Pt_ele1>25)*(Pt_ele2>15)*(Pt_Hjet1>20)*(Pt_Hjet2>20)*(Pt_Zjet1>20)*(Pt_Zjet2>20)*(M_ee>12)*(isElectronEvent))'#*(1-(run_number==276950)*(lumi_number==22)*(event_number==34039924))*(1-(run_number==1)*(lumi_number==447098)*(event_number==71625048)))'
#removing HLT
preselection_Electron_nos = '((pass_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)*(Pt_ele1>25)*(Pt_ele2>15)*(Pt_Hjet1>20)*(Pt_Hjet2>20)*(Pt_Zjet1>20)*(Pt_Zjet2>20)*(M_ee>12)*(isElectronEvent)*(1-isMuonEvent))'#*(1-(run_number==276950)*(lumi_number==22)*(event_number==34039924))*(1-(run_number==1)*(lumi_number==447098)*(event_number==71625048)))'
#Require at least one loose MVA bTag
bTagsel1loose = '*(((CMVA_bjet1>-0.5884)+(CMVA_bjet2>-0.5884)+(CMVA_Zjet1>-0.5884)+(CMVA_Zjet2>-0.5884))>0)'
bTagsel1medium = '*(((CMVA_bjet1>0.4432)+(CMVA_bjet2>0.4432)+(CMVA_Zjet1>0.4432)+(CMVA_Zjet2>0.4432))>0)'
bTagsel2loose = '*(((CMVA_bjet1>-0.5884)+(CMVA_bjet2>-0.5884)+(CMVA_Zjet1>-0.5884)+(CMVA_Zjet2>-0.5884))>1)'

#This defines the preselection and final selection bTag requirements
bTagPresel   = bTagsel1loose
bTagFinalsel = bTagsel1medium

bTagPreselSF = bTag1SFloose
bTagFinalSF  = bTag1SFmedium
bTagFinalSFup    = bTag1SFmediumUp
bTagFinalSFdown  = bTag1SFmediumDown


preselection_Muon_nos = preselection_Muon_nos+bTagPresel
preselection_Electron_nos = preselection_Electron_nos+bTagPresel
preselectionMuon = preselection_Muon_nos + '*(Charge_muon1*Charge_muon2 < 0)'
preselectionElectron = preselection_Electron_nos + '*(Charge_ele1*Charge_ele2 < 0)'
#preselectionMuon = '((Pt_muon1>20)*(Pt_muon2>10)*(Pt_Hjet1>25)*(Pt_Hjet2>25)*(Pt_Zjet1>20)*(Pt_Zjet2>20)*(Charge_muon1*Charge_muon2<0)*(CISV_bjet1>0.8)*(CISV_bjet2>0.46)*(abs(cosThetaStarMu)<0.9)*(M_uu>10)*(DPhi_uu_jj_Z<2.75)*(Pt_miss<150)*(M_uu<105)*(isMuonEvent>0))'

preselectionmunu = '((Pt_muon1>50)*(Pt_muon2<50.0)*(Pt_miss>55)*(Pt_jet1>200)*(Pt_jet2>50)*(Pt_ele1<50.0)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5)*(MT_uv>50.0))'
preselectionemu  = '((Pt_muon1>50)*(Pt_muon2>50)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3))'

# Add the filters to the preselections
preselectionemu  += passfilter
preselectionMuon += passfilter
preselectionElectron += passfilter
preselectionmunu += passfilter

#These are the Z and TTbar control regions, hard-coded to avoid mistakes in multiple functions
dyControlRegion_Muon = '(M_uu>80)*(M_uu<100)'
ttControlRegion_Muon = '(M_uu>100)*(Pt_miss>100)'
dyControlRegion_Electron = '(M_ee>80)*(M_ee<100)'
ttControlRegion_Electron = '(M_ee>100)*(Pt_miss>100)'
#dyControlRegion = '(M_uu>86)*(M_uu<96)'
#ttControlRegion = '((((M_uu>50)*(M_uu<70))+(M_uu>100))>0)*(Pt_miss>100)'

# Weights for different MC selections, including integrated luminosity, event weight, and trigger weight
#NormalWeightMuon = str(lumi)+'*weight_central'+trackerHIP1+trackerHIP2+doubleMuonHLT+doubleMuonIdAndIsoScale+bTagPreselSF
NormalWeightMuon     = str(lumi)+'*weight_central'+trackerHIP1+trackerHIP2+doubleMuonHLT+doubleMuonIdAndIsoScale+bTagPreselSF
NormalWeightElectron = str(lumi)+'*weight_central'+bTagPreselSF+eleRECOScale+doubleElectronHLTAndId#+doubleElectronHLT+doubleEleMedIdScale+trackerHIP1+trackerHIP2
NormalWeightMuNu = str(lumi)+'*weight_central'+singleMuonHLT+singleMuonIdScale+singleMuonIsoScale+trackerHIP1
#NormalWeightEMu = str(lumi)+'*weight_central'+singleMuonHLTEMU+MuIdScaleEMU+MuIsoScaleEMU+eleRECOScale+eleHEEPScale+trackerHIPEMU
#NormalWeightEMuNoHLT = str(lumi)+'*weight_central'+MuIdScaleEMU+MuIsoScaleEMU+eleRECOScale+eleHEEPScale+trackerHIPEMU#fixme do we need scale factors here?


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

# QCD data-driven scale factor
useDataDrivenQCD = True
fbd_Muon     = [1.449, 0.03] # Apr 18, 2018
fbd_Electron = [1.449, 0.1] # Feb 2018

# tt, z SF calculated using Data with NEW method (Apr 18, 2018)
Rz_data_muon  = [1.152, 0.013]
Rtt_data_muon = [1.016, 0.062]
Rz_data_electron  = [1.127, 0.011]
Rtt_data_electron = [0.915, 0.023]


analysisChannel = 'muon'
#analysisChannel = 'electron'
if (analysisChannel == 'muon'):
 	NormalWeight=NormalWeightMuon
	preselection_nos=preselection_Muon_nos
	preselection=preselectionMuon
	dataHLT=dataHLTMuon
	fbd=fbd_Muon
	charge1 = 'Charge_muon1'
	charge2 = 'Charge_muon2'
	dyControlRegion = dyControlRegion_Muon
	ttControlRegion = ttControlRegion_Muon
	ell='u'
	latexEll='#mu'
	cosThetaStar="cosThetaStarMu"
	Rz_data=Rz_data_muon
	Rtt_data=Rtt_data_muon
if (analysisChannel == 'electron'):
	NormalWeight=NormalWeightElectron
	preselection_nos=preselection_Electron_nos
	preselection=preselectionElectron
	dataHLT=dataHLTElectron
	fbd=fbd_Electron
	charge1 = 'Charge_ele1'
	charge2 = 'Charge_ele2'
	dyControlRegion = dyControlRegion_Electron
	ttControlRegion = ttControlRegion_Electron
	ell='e'
	latexEll='e'
	cosThetaStar="cosThetaStarEle"
	Rz_data=Rz_data_electron
	Rtt_data=Rtt_data_electron

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

totunc_Muon = [6.75]
totunc_Electron = [6.75]



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
#bosonzoombinning_uujj_TT = [95,100]
bosonzoombinning_uujj_TT = [45,50]
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
bdtbinning = [50,-0.7,0.8]

for x in range(40):
	if ptbinning[-1] < 1000:
       		ptbinning.append(ptbinning[-1]+(ptbinning[-1] - ptbinning[-2])*1.2)
       	if ptbinning2[-1] < 500:
       		ptbinning2.append(ptbinning2[-1]+(ptbinning2[-1] - ptbinning2[-2])*1.2)
       	if metbinning2[-1] < 500:
       		metbinning2.append(metbinning2[-1]+(metbinning2[-1] - metbinning2[-2])*1.2)		
       	if stbinning[-1] < 2500:
       		stbinning.append(stbinning[-1]+(stbinning[-1] - stbinning[-2])*1.2)
       	if bosonbinning[-1]<9000:
       		bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.2 )
       	if lqbinning[-1]<1500:
       		lqbinning.append(lqbinning[-1]+(lqbinning[-1] - lqbinning[-2])*1.1)
       	if bosonzoombinning_uujj_TT[-1] < 700:
       		bosonzoombinning_uujj_TT.append(bosonzoombinning_uujj_TT[-1] + (bosonzoombinning_uujj_TT[-1] - bosonzoombinning_uujj_TT[-2])*1.25)	       	
	if metzoombinning_uujj_TT[-1] < 800:
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
	global analysisChannel
	global preselection 
	global ell
	global latexEll
	global cosThetaStar

	#######################################################################################
    ######  The output directories, and the files that define final selection cuts  #######
	#######################################################################################

	# Please retain the "script flag" comment. Some python scripts are available which search
	# for this, and make use of it. e.g. For systematic variations, we can in batch instead
	# of running serially, which speeds things up.


	version_name = 'Testing_diHiggs_newNtuples_MuCutsMC0p49_'+analysisChannel # scriptflag
	os.system('mkdir Results_'+version_name) 

	MuonOptCutFile = 'Results_'+version_name+'/OptHH_resCuts_Smoothed_pol2cutoff.txt' # scriptflag
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
		PDF4LHCUncStudy(MuonOptCutFile,MuNuOptCutFile,version_name)
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
		
		qcdselection = preselection_nos
		qcdselectionmunu = preselection_nos
		qcdselection += passfilter # AH: do we need also the passfilters ?
		qcdselectionmunu += passfilter
		
		QCDStudy(qcdselection,qcdselection,MuonOptCutFile,MuNuOptCutFile,NormalWeight,NormalWeightMuNu,version_name)

	if False:
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err],[Fbd_uujj,Fbd_uujj_err]] = GetNormalizationScaleFactorsAndFbd(NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion, ttControlRegion,0)
		exit()

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

		MakeEfficiencyPlot(NormalDirectory,NormalWeight,'Results_'+version_name+'/OptBLCTau1_uujjCuts_Smoothed_pol2cutoff.txt','BL',version_name)

		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuonScaleFactors( NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion, ttControlRegion,1)
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))<1)', '(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))>=1)')#fixme todo varying control sample MT window
		

		# UUJJ plots at preselection, Note that putting 'TTBarDataDriven' in the name turns on the use of data-driven ttbar e-mu sample in place of MC
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[60,0,600],preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		#MakeBasicPlot("M_jj","M^{jj} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)

		# Full Selection Plots
		for lqmass in [200,300,400,500,600,750,800,900,1000]:
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
                        MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("CISV_jet1","Jet1 CSV score",bjetbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("CISV_jet2","Jet2 CSV score",bjetbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuonOptCutFile,version_name,lqmass)

	# ====================================================================================================================================================== #
	# This is a testing plot routine for use with the new RPV susy samples
	# ====================================================================================================================================================== #
	if False :

		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuonScaleFactors( NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion, ttControlRegion,1)
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
		
		# UUJJ plots at preselection, Note that putting 'TTBarDataDriven' in the name turns on the use of data-driven ttbar e-mu sample in place of MC
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[60,0,600],preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)	
		MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MH_uujj","M_{#muj} (lead jet combo) [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon2jet1","#DeltaR(#mu_{2},j_{1})",drbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DR_muon2jet2","#DeltaR(#mu_{2},j_{2})",drbinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_jet1met","#Delta#phi(j_{1},E_{T}^{miss})",dphibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_jet2met","#Delta#phi(j_{2},E_{T}^{miss})",dphibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1jet1","#Delta#phi(#mu_{1},j_{1})",dphibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon1jet2","#Delta#phi(#mu_{1},j_{2})",dphibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon2jet1","#Delta#phi(#mu_{2},j_{1})",dphibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("DPhi_muon2jet2","#Delta#phi(#mu_{2},j_{2})",dphibinning,preselection,NormalWeight,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)


	# ====================================================================================================================================================== #
	# This is a basic plotting routine to make Analysis Note style plots with ratio plots. AN Analysis-Note
makeba	# ====================================================================================================================================================== #
	if True :
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
			if bosonbinning[-1]<750:
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

		print '\n  NormalWeight plus preselection  is : ', str(NormalWeight+'*'+preselection) , '\n' # AH:
		#print lqbinning,stbinning

		#Scale Factor Study
		if False:
			for x in [['',''],['*(Pt_muon1<30)','*(Pt_miss>90)'],['*(Pt_muon1>30)*(Pt_muon1<50)','*(Pt_miss>80)'],['*(Pt_muon1>50)*(Pt_muon1<75)','*(Pt_miss>70)'],['*(Pt_muon1>75)*(Pt_muon1<100)','*(Pt_miss>70)'],['*(Pt_muon1>100)','*(Pt_miss>50)']]:
			#for x in [['*(Pt_muon1>100)*(Pt_muon1<150)','*(Pt_miss>80)'],['*(Pt_muon1>150)*(Pt_muon1<200)',''],['*(Pt_muon1>200)','']]:
				print '--------------\n'
				print x
				[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactors( NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion+x[0], '(M_uu>100)'+x[1],0)
			exit()
		# Get Scale Factors
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactors( NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion, ttControlRegion,0)
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = [Rz_data,Rtt_data]
		# AH: To speed things up when debugging

		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]]=[[1.,0.],[1.,0.]]
		#CSVv2L	0.460
		#CSVv2M	0.8
		#CSVv2T	0.935

		#preselection = preselection+'*('+charge1+'<0)*('+charge2+'<0)'#FIXME checking same sign

		# Optionally, you can make an event-count table for each selection. Useful if testing a new optimization
		# We will do this later wtih full systematics for our set of stable cuts. 
		if False:
			QuickTableTTDD(MuonOptCutFile, preselection+"*(M_uu>100)",NormalWeight,Rz_uujj, Rw_uvjj,Rtt_uujj,0)#Use data-driven TTbar
			#QuickTable(MuonOptCutFile, preselection+"*(M_uu>100)",NormalWeight,Rz_uujj, Rw_uvjj,Rtt_uujj,0)#Use MC-driven TTbar
			#QuickTable(MuNuOptCutFile, preselectionmunu,NormalWeightMuNu,Rz_uujj, Rw_uvjj,Rtt_uvjj,0)

		#MakeBasicPlot("sqrt(abs(2*Pt_jet1*Pt_jet2*(cosh(Eta_jet1-Eta_jet2) - (((Phi_jet1-Phi_jet2)<-1*pi)*cos(Phi_jet1-Phi_jet2+2*pi)) - (((Phi_jet1-Phi_jet2)>-1*pi)*((Phi_jet1-Phi_jet2)<1*pi)*cos(Phi_jet1-Phi_jet2)) - (((Phi_jet1-Phi_jet2)> 1*pi)*cos(Phi_jet1-Phi_jet2-2*pi)) )))","M_{jj} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)

                #Signal efficiency*acceptance at final selection
		#MuonOptCutFile = 'Results_Testing_Feb21_tmp/OptLQ_uujjCuts_Smoothed_pol2cutoff.txt'
		#MakeEfficiencyPlot(NormalDirectory,NormalWeight,MuonOptCutFile,'LQuujj',version_name)
		
		
		# Here are a few plots which are zoomed-in on control regions. 
		
		MakeBasicPlot("M_"+ell+ell,"M^{"+latexEll+latexEll+"} [GeV] (DY control region)",bosonzoombinning_uujj_Z,preselection,NormalWeight,NormalDirectory,'controlzoom_ZRegion',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV] (DY control region)",metzoombinning_uujj_Z,preselection+'*(M_'+ell+ell+'>80)*(M_'+ell+ell+'<100)',NormalWeight,NormalDirectory,'controlzoomZRegion',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("M_"+ell+ell,"M^{"+latexEll+latexEll+"} [GeV] (TT control region)",bosonzoombinning_uujj_TT,preselection+'*'+ttControlRegion,NormalWeight,NormalDirectory,'controlzoom_TTRegion',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV] (TT control region)",metzoombinning_uujj_TT,preselection+'*'+ttControlRegion,NormalWeight,NormalDirectory,'controlzoomTTRegion',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		
		#Here are some 2D plots
		
		#MakeBasicPlot2D("M_uu","Mjj_Z","M_{uu} [GeV]","M_{(Z)jj} [GeV]",binning2D,binning2D,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot2D("M_uu","Mjj_Z","M_{uu} [GeV]","M_{(Z)jj} [GeV]",binning2D,binning2D,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,900)
		#MakeBasicPlot2D("Mbb_H","Mjj_Z","M_{(H)bb} [GeV]","M_{(Z)jj} [GeV]",binning2D,binning2D,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot2D("Mbb_H","Mjj_Z","M_{(H)bb} [GeV]","M_{(Z)jj} [GeV]",binning2D,binning2D,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,900)
		#MakeBasicPlot2D("Mbb_H-125","Mjj_Z-91","M_{bb}-125 [GeV]","M_{jj}-91 [GeV]",MassMinusbinning,MassMinusbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot2D("Mbb_H-125","Mjj_Z-91","M_{bb}-125 [GeV]","M_{jj}-91 [GeV]",MassMinusbinning,MassMinusbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,900)
		#MakeBasicPlot2D("abs(cosThetaStarMu)","M_uu4j","|cos(#Theta*)|","M_{uu4j} [GeV]",costhetastarbinning,lqbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot2D("abs(cosThetaStarMu)","M_uu4j","|cos(#Theta*)|","M_{uu4j} [GeV]",costhetastarbinning,lqbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,900)
		

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
		
		# putting 'QCDDataDriven' will also turns on the use of data-driven QCD if not already set at default
		for lqmass in [260,270,300,350,400,450,500,550,600,650,750,800,900,1000]:
			MakeBasicPlot("bdt_discrim_M"+str(lqmass),"BDT output at M"+str(lqmass),bdtbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,lqmass)
		MakeBasicPlot("bdt_discrims3_low","BDT output combined M260-350",bdtbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("bdt_discrims3_high","BDT output combined M400-1000",bdtbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,900)
		MakeBasicPlot("cosTheta_hbb_"+ell+ell,"cos(#Theta) (H->bb) "+latexEll+latexEll,costhetastarbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("cosTheta_z"+ell+ell+"_hzz","cos(#Theta) (Z->"+latexEll+latexEll+", H->ZZ)",costhetastarbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		if ell=='mu': MakeBasicPlot(cosThetaStarMu,"cos(#Theta*) ("+latexEll+")",costhetastarbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		if ell=='e': MakeBasicPlot(cosThetaStarEle,"cos(#Theta*) ("+latexEll+")",costhetastarbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("phi0_"+ell+ell,"#phi0_"+latexEll+latexEll,phi0binning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("phi0_zz_"+ell+ell,"#phi0_zz_"+latexEll+latexEll,phi0binning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("phi1_"+ell+ell,"#phi1_"+latexEll+latexEll,phi0binning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("phi1_z"+ell+ell,"#phi1_z"+latexEll+latexEll,phi0binning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("phi1_zjj_"+ell+ell,"#phi1_zjj+"+latexEll+latexEll,phi0binning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("CMVA_bjet1","Jet1(H->bb) CMVA score",bjetbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("CMVA_bjet2","Jet2(H->bb) CMVA score",bjetbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("CMVA_Zjet1","Jet1(Z->jj) CMVA score",bjetbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("CMVA_Zjet2","Jet2(Z->jj) CMVA score",bjetbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Hjet1","p_{T}(bjet_{1}) (H) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Hjet2","p_{T}(bjet_{2}) (H) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Zjet1","p_{T}(jet_{1}) (Z) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Zjet2","p_{T}(jet_{2}) (Z) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Hjets","p_{T}(bb) (H) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_Zjets","p_{T}(jj) (Z) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_"+ell+ell,"p_{T}("+latexEll+latexEll+") [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_ele1","p_{T}(e_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_ele2","p_{T}(e_{2}) [GeV]",ptbinning2,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[60,0,600],preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Eta_Hjet1","#eta(bjet_{1}) (H) [GeV]",etabinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Eta_Hjet2","#eta(bjet_{2}) (Z) [GeV]",etabinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Eta_Zjet1","#eta(jet_{1}) (H) [GeV]",etabinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Eta_Zjet2","#eta(jet_{2}) (Z) [GeV]",etabinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)		
		MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)	
		MakeBasicPlot("Phi_Hjet1","#phi(bjet_{1}) (H) [GeV]",phibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Phi_Hjet2","#phi(bjet_{2}) (H) [GeV]",phibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)	
		MakeBasicPlot("Phi_Zjet1","#phi(jet_{1}) (Z) [GeV]",phibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Phi_Zjet2","#phi(jet_{2}) (Z) [GeV]",phibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)	
		#MakeBasicPlot("M_uu4j-Mbb_H+125","M_{X} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("M_uu4j-Mbb_H+125-M_uujj+125","M_{X2} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("M_jj","M_{jj} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("M_"+ell+ell,"M^{"+latexEll+latexEll+"} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Mbb_H","M^{bb} from H [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("Mbb_H-125","(M^{bb}-125) from H [GeV]",MassMinusbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Mjj_Z","M^{jj} from Z [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("Mjj_Z-91","(M^{jj-91)} from Z [GeV]",MassMinusbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("MH_uujj","M_{#muj} (lead jet combo) [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("M_uujjavg","M_{#muj}_{avg} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("M_"+ell+ell+"jj","M_{"+latexEll+latexEll+"jj} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("M_"+ell+ell+"4j","M_{"+latexEll+latexEll+"4j} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("JetCount","N_{jet}",njetbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)#removing TTBarDataDriven cause this makes weird muon count comparison
		MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)#removing TTBarDataDriven cause this makes weird muon count comparison
		MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_ele1ele2","#DeltaR(e_{1},e_{2})",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_"+ell+"1Hj1","#DeltaR("+latexEll+"_{1},Hj_{1})",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_"+ell+"1Hj2","#DeltaR("+latexEll+"_{1},Hj_{2})",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_"+ell+"2Hj1","#DeltaR("+latexEll+"_{2},Hj_{1})",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_"+ell+"2Hj2","#DeltaR("+latexEll+"_{2},Hj_{2})",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_"+ell+"1Zj1","#DeltaR("+latexEll+"_{1},Zj_{1})",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_"+ell+"1Zj2","#DeltaR("+latexEll+"_{1},Zj_{2})",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_"+ell+"2Zj1","#DeltaR("+latexEll+"_{2},Zj_{1})",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_"+ell+"2Zj2","#DeltaR("+latexEll+"_{2},Zj_{2})",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_jj_Z","#DeltaR(j_{1},j_{2}) (Z)",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_bb_H","#DeltaR(b_{1},b_{2}) (H)",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_"+ell+ell+"_bb_H","#DeltaR("+latexEll+latexEll+",bb(H))",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DR_"+ell+ell+"_jj_Z","#DeltaR("+latexEll+latexEll+",jj(Z))",drbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_ele1met","#Delta #phi (e_{1},E_{T}^{miss})",dphibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_"+ell+ell+"_jj_Z","#Delta#phi("+latexEll+latexEll+",jj(Z))",dphibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_"+ell+ell+"_bb_H","#Delta#phi("+latexEll+latexEll+",bb(H))",dphibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_bb_H","#Delta#phi(bb) (H)",dphibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("DPhi_jj_Z","#Delta#phi(jj) (Z)",dphibinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Hjet1BsfLoose","Hjet1 Btag SF",[120,0,1.5],preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Hjet2BsfLoose","Hjet2 Btag SF",[120,0,1.5],preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Zjet1BsfLoose","Zjet1 Btag SF",[120,0,1.5],preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("Zjet2BsfLoose","Zjet2 Btag SF",[120,0,1.5],preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		MakeBasicPlot("(1-(1-(CMVA_bjet1>-0.5884)*Hjet1BsfLoose)*(1-(CMVA_bjet2>-0.5884)*Hjet2BsfLoose)*(1-(CMVA_Zjet1>-0.5884)*Zjet1BsfLoose)*(1-(CMVA_Zjet2>-0.5884)*Zjet2BsfLoose))","Btag Total SF",[200,0,2],preselection,NormalWeight,NormalDirectory,'standard',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,300)
		#if analysisChannel=='electron' : exit()
		#fixme turning off final selection
		# Full Selection Plots
		for lqmass in [260,270,300,350,400,450,500,550,600,650,750,800,900,1000]:
		#for lqmass in [300,900]: # AH
			MakeBasicPlot("bdt_discrim_M"+str(lqmass),"BDT output at M"+str(lqmass),bdtbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			#MakeBasicPlot("bdt_discrims2_M300","BDT output (no 6-object mass) at M300",bdtbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			#MakeBasicPlot("bdt_discrims2_M550","BDT output (no 6-object mass) at M550",bdtbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("bdt_discrims3_low","BDT output combined M260-350",bdtbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("bdt_discrims3_high","BDT output combined M400-1000",bdtbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_uu","M^{#mu#mu} [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uu4j","M_{#mu#mu4j} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("DR_bb_H","#DeltaR(b_{1},b_{2}) (H)",drbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			if ell=="mu": MakeBasicPlot("cosThetaStarMu","cos(#Theta*)(#mu)",costhetastarbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			if ell=="e"MakeBasicPlot("cosThetaStarEle","cos(#Theta*)(e)",costhetastarbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			
			MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("CMVA_bjet1","Jet1(H->bb) CMVA score",bjetbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("CMVA_bjet2","Jet2(H->bb) CMVA score",bjetbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("CMVA_Zjet1","Jet1(Z->bb) CMVA score",bjetbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			MakeBasicPlot("CMVA_Zjet2","Jet2(Z->bb) CMVA score",bjetbinning,preselection,NormalWeight,NormalDirectory,'final',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			print '------- Done with final selection plots'

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
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactors( NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion, ttControlRegion,0)
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))<1)', '(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))>=1)')#fixme todo varying control sample MT window
		

		# Here are a few plots which are zoomed-in on control regions. 
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",[20,80,100],preselection,NormalWeight,NormalDirectory,'controlzoomPASTTBarDataDriven_ZRegiontagfree',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		# MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonzoombinning_uujj_Z,preselection,NormalWeight,NormalDirectory,'controlzoomPAS_ZRegion',ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		bosonzoombinning_uvjj = [20,70,110]
		MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))<1)',NormalWeightMuNu,NormalDirectory,'controlzoomPAS_WRegiontagfree','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))>=1)',NormalWeightMuNu,NormalDirectory,'controlzoomPAS_TTRegiontagfree','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		# The two flags are for regular plots, and tagfree plots (plots that don't say CMS Preliminary - for notes or thesis)
		for flag in ['','tagfree']:

			# Preselection plots in the UUJJ channel in the PAS style (no subplot)
			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselection,NormalWeight,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselection,NormalWeight,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("MH_uujj","M_{#muj} (lead jet combo) [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uujj2","M_{#muj}^{min} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("JetCount","N_{jet}",nbinning,preselection,NormalWeight,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			#fixme todo added version with MC based ttbar background
			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standardPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standardPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselection,NormalWeight,NormalDirectory,'standardPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselection,NormalWeight,NormalDirectory,'standardPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselection,NormalWeight,NormalDirectory,'standardPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'standardPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("MH_uujj","M_{#muj} (lead jet combo) [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standardPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standardPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("M_uujj2","M_{#muj}^{min} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'standardPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("JetCount","N_{jet}",nbinning,preselection,NormalWeight,NormalDirectory,'standardPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)

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
				MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDrivenPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDrivenPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uujj2","M_{#muj}^{min} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'finalTTBarDataDrivenPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
			        #fixme todo added version with MC based ttbar background
				MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselection,NormalWeight,NormalDirectory,'finalPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselection,NormalWeight,NormalDirectory,'finalPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uujj2","M_{#muj}^{min} [GeV]",lqbinning,preselection,NormalWeight,NormalDirectory,'finalPAS'+flag,ell+ell+'jj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuonOptCutFile,version_name,lqmass)
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
		#FullAnalysis(MuonOptCutFile, preselection,preselectionmunu,NormalDirectory,NormalWeight,'TTBarDataDriven')  # scriptflag
		#FullAnalysis(MuNuOptCutFile, preselection,preselectionmunu,NormalDirectory,NormalWeightMuNu,'normal')  # scriptflag
		
		finalSelectionMuon = preselection.replace(bTagPresel,bTagFinalsel)
		finalWeightMuon = NormalWeight.replace(bTagPreselSF,bTagFinalSF)
		#finalSelectionMuon = preselection.replace(bTagsel1loose,bTagsel2loose)
		#finalWeightMuon = NormalWeight.replace(bTag1SF,bTag2SF)
		#FullAnalysis(MuonOptCutFile, preselection,preselection,preselectionmunu,NormalDirectory,NormalWeight,NormalWeight'normal')  # scriptflag #preselection (1 loose bTag)
		FullAnalysis(MuonOptCutFile, preselection,finalSelectionMuon,preselectionmunu,NormalDirectory,NormalWeight,finalWeightMuon,'normal')  # scriptflag #final selection

	if False :
		uujjcardfiles = MuonOptCutFile.replace('.txt','_systable*.txt')
		#uvjjcardfiles = MuNuOptCutFile.replace('.txt','_systable*.txt')

		uujjcards = ParseFinalCards(uujjcardfiles)
		#uvjjcards = ParseFinalCards(uvjjcardfiles)#fixme using uujj for now for speed
		#finalcards = FixFinalCards([uujjcards,uvjjcards])
		finalcards = FixFinalCards([uujjcards])

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
			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactorsMod( NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion, ttControlRegion,sample)
			# MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			# MakeBasicPlot("MT_uv","M_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV] "+sample,ptbinning,preselection,NormalWeight,NormalDirectory,'standardTTBarDataDriven_sys'+sample,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV] "+sample,ptbinning,preselection,NormalWeight,NormalDirectory,'standardTTBarDataDriven_sys'+sample,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			rescale_string = MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)',NormalWeightMuNu,NormalDirectory,'standard_rescaletest_pre','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sysmethod in ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','PUup','PUdown']:
			preselection_mod = ModSelection(preselection,sysmethod,MuonOptCutFile)
			NormalWeight_mod = ModSelection(NormalWeight,sysmethod,MuonOptCutFile)

			Rw_uvjj = 1.0

			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactors( NormalWeight_mod+'*'+preselection_mod, NormalDirectory, dyControlRegion, ttControlRegion,1)

			MakeBasicPlot(ModSelection("Pt_jet1",sysmethod,MuonOptCutFile),"p_{T}(jet_{1}) [GeV] "+sysmethod,ptbinning,preselection_mod,NormalWeight_mod,NormalDirectory,'standard_sys'+sysmethod,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot(ModSelection("Pt_jet2",sysmethod,MuonOptCutFile),"p_{T}(jet_{2}) [GeV] "+sysmethod,ptbinning,preselection_mod,NormalWeight_mod,NormalDirectory,'standard_sys'+sysmethod,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)



	# ====================================================================================================================================================== #
	# This is for Optimization of cuts
	# ====================================================================================================================================================== #

	if False :
		doLongLived = False
		# Get Scale Factors
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactors( NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion, ttControlRegion,0)
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))<1)', '(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)*(((CISV_jet1>0.8)+(CISV_jet2>0.8))>=1)')#fixme todo varying control sample MT window
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]]=[[1.,0.],[1.,0,]]
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]]=[[1.,0.],[1.,0,]]
		scaleFactors = [Rz_uujj,Rtt_uujj,Rw_uvjj]
		if not doLongLived :
			MuonOptTestCutFile = 'Results_'+version_name+'/OptLQ_uujjCuts_Smoothed_pol2cutoff.txt'
	          	#variableSpace = ['Pt_jet1:10:0:1000']
			variableSpace = ['Pt_uu:50:0:1000','St_uujj:50:0:4000','M_uu4j:50:100:2500',]
			OptimizeCuts3D(variableSpace,preselection,NormalWeight,version_name,scaleFactors,'','uujj')
			#scaleFactors = [Rz_uujj,Rtt_uvjj,Rw_uvjj]
			#variableSpace = ['MT_uv:25:120:1200','St_uvjj:25:300:2000','M_uvjj:25:100:1000',]
		        #OptimizeCuts3D(variableSpace,preselectionmunu,NormalWeightMuNu,version_name,scaleFactors,'','uvjj')#FIXME turned off uvjj for now
		#Now we can do it for long-lived samples
		if doLongLived :
			scaleFactors = [Rz_uujj,Rtt_uujj,Rw_uvjj]
		        #variableSpace = ['Pt_jet1:10:0:1000']
			variableSpace = ['M_uu:15:100:500','St_uujj:15:300:1800','M_uujj2:15:100:900',]
			OptimizeCuts3D(variableSpace,preselection,NormalWeight,version_name,scaleFactors,'','BLuujj')


	# ====================================================================================================================================================== #
	# This is for shape systematics
	# ====================================================================================================================================================== #

	if False :
		#MuonOptTestCutFile = 'Results_'+version_name+'/OptLQ_uujjCuts_Smoothed_pol2cutoff_1150On.txt'
		#MuNuOptTestCutFile = 'Results_'+version_name+'/OptLQ_uvjjCuts_Smoothed_pol2cutoff.txt'
		# Get Scale Factors
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactors( NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion, ttControlRegion,0)
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>100)*(MT_uv<200)*(JetCount<3.5)*(((CISV_jet1>0.97)+(CISV_jet2>0.97))<1)', '(MT_uv>100)*(MT_uv<200)*(JetCount>3.5)*(((CISV_jet1>0.97)+(CISV_jet2>0.97))>=1)')#fixme todo varying control sample MT window
		
		finalSelectionMuon = preselection.replace(bTagPresel,bTagFinalsel)
		finalWeightMuon = NormalWeight.replace(bTagPreselSF,bTagFinalSF)
	
		ShapeSystematic('uujj',NormalWeight,preselection,finalWeightMuon,finalSelectionMuon)
		#ShapeSystematic('uvjj',NormalWeightMuNu,preselectionmunu,MuNuOptTestCutFile)

	# ====================================================================================================================================================== #
	# This is for  spurious events
	# ====================================================================================================================================================== #

	if False:
		tmpfile = TFile("tmp.root","RECREATE")
		t_DoubleMuData2 = t_TTBar.CopyTree(preselection)
		NN = t_DoubleMuData2.GetEntries()
		for n in range(NN):
			if n%1000 ==0:
				print n,'of',NN
			t_DoubleMuData2.GetEntry(n)
			#st = t_DoubleMuData2.St_uujj
			#if st>5000:
			#if t_DoubleMuData2.St_uvjj>1505 and t_DoubleMuData2.MT_uv>540 and t_DoubleMuData2.M_uvjj>660 and t_DoubleMuData2.Pt_muon1>800:
			if t_DoubleMuData2.Pt_miss>145 and t_DoubleMuData2.Pt_miss<160 and  t_DoubleMuData2.Phi_muon2>1.3 and t_DoubleMuData2.Phi_muon2<1.8 and t_DoubleMuData2.bdt_discrim_M260>0.05 and t_DoubleMuData2.bdt_discrim_M260<0.15 and t_DoubleMuData2.bdt_discrims3_low>0.04 and t_DoubleMuData2.bdt_discrims3_low<0.1 and t_DoubleMuData2.cosThetaStarMu>-0.7 and t_DoubleMuData2.cosThetaStarMu<-0.6:			
				print 'run / lumi / event:',int(t_DoubleMuData2.run_number),'/',int(t_DoubleMuData2.lumi_number),'/',int(t_DoubleMuData2.event_number)
				print 'Pt_muon1     ',t_DoubleMuData2.Pt_muon1
				#print 'Pt_muon1_raw ',t_DoubleMuData2.Pt_muon1_noTuneP
				#if (t_DoubleMuData2.Pt_muon1>0):
				#	print 'raw/tuneP 1  ',t_DoubleMuData2.Pt_muon1_noTuneP/t_DoubleMuData2.Pt_muon1 
				#else: print 'raw/tuneP 1  ','n/a'
				print 'Pt_muon2     ',t_DoubleMuData2.Pt_muon2
				#print 'Pt_muon2_raw ',t_DoubleMuData2.Pt_muon2_noTuneP
				#if (t_DoubleMuData2.Pt_muon2>0):
				#	print 'raw/tuneP 2  ',t_DoubleMuData2.Pt_muon2_noTuneP/t_DoubleMuData2.Pt_muon2
				#else: print 'raw/tuneP 2  ','n/a'
				print 'Eta_muon1    ',t_DoubleMuData2.Eta_muon1
				print 'Eta_muon2    ',t_DoubleMuData2.Eta_muon2
				print 'Phi_muon1    ',t_DoubleMuData2.Phi_muon1
				print 'Phi_muon2    ',t_DoubleMuData2.Phi_muon2
				print 'Pt_Hjet1      ',t_DoubleMuData2.Pt_Hjet1
				print 'Pt_Hjet2      ',t_DoubleMuData2.Pt_Hjet2
				print 'Pt_Zjet1      ',t_DoubleMuData2.Pt_Zjet1
				print 'Pt_Zjet2      ',t_DoubleMuData2.Pt_Zjet2
				print 'Eta_Hjet1     ',t_DoubleMuData2.Eta_Hjet1
				print 'Eta_Hjet2     ',t_DoubleMuData2.Eta_Hjet2
				print 'Phi_Hjet1     ',t_DoubleMuData2.Phi_Hjet1
				print 'Phi_Hjet2     ',t_DoubleMuData2.Phi_Hjet2
				print 'Eta_Zjet1     ',t_DoubleMuData2.Eta_Zjet1
				print 'Eta_Zjet2     ',t_DoubleMuData2.Eta_Zjet2
				print 'Phi_Zjet1     ',t_DoubleMuData2.Phi_Zjet1
				print 'Phi_Zjet2     ',t_DoubleMuData2.Phi_Zjet2
				print 'Pt_miss      ',t_DoubleMuData2.Pt_miss
				print 'Phi_miss     ',t_DoubleMuData2.Phi_miss
				print 'M_uu         ',t_DoubleMuData2.M_uu
				print 'DR_muon1muon2',t_DoubleMuData2.DR_muon1muon2
				print 'DPhi_muon1met',t_DoubleMuData2.DPhi_muon1met
				print 'CMVA Hjet1   ',t_DoubleMuData2.CMVA_bjet1
				print 'CMVA Hjet2   ',t_DoubleMuData2.CMVA_bjet2
				print 'CMVA Zjet1   ',t_DoubleMuData2.CMVA_Zjet1
				print 'CMVA Zjet2   ',t_DoubleMuData2.CMVA_Zjet2
				print 'weight_central',t_DoubleMuData2.weight_central


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
TTreeFormula.SetMaxima(100000,1000,1000000)
import numpy
import math
rnd= TRandom3()
person = (os.popen('whoami').readlines()[0]).replace("\n",'')


#if '/store' in NormalDirectory:
#	NormalFiles = [(x.split('/')[-1]).replace('\n','') for x in os.popen('cmsLs '+NormalDirectory+"| grep \".root\" | awk '{print $1}'").readlines()]
#else:
NormalFiles = [ff.replace('\n','') for ff in os.popen('ls '+NormalDirectory+"| grep \".root\"").readlines()]

#if '/store' in EMuDirectory:
#	EMuFiles = [(x.split('/')[-1]).replace('\n','') for x in os.popen('cmsLs '+EMuDirectory+"| grep \".root\" | awk '{print $1}'").readlines()]
#else:
EMuFiles = [ff.replace('\n','') for ff in os.popen('ls '+EMuDirectory+"| grep \".root\"").readlines()]

#if '/store' in QCDDirectory:	
#	QCDFiles = [(x.split('/')[-1]).replace('\n','') for x in os.popen('cmsLs '+QCDDirectory+"| grep \".root\" | awk '{print $1}'").readlines()]
#else:
QCDFiles = [ff.replace('\n','') for ff in os.popen('ls '+QCDDirectory+"| grep \".root\"").readlines()]

for f in NormalFiles:
	_tree = 't_'+f.split('/')[-1].replace(".root","")
	_treeTmp = _tree+"_tmp"
	_prefix = ''# +'root://eoscms//eos/cms'*('/store' in NormalDirectory)
	print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

for f in EMuFiles:
	_tree = 'te_'+f.split('/')[-1].replace(".root","")	
	_treeTmp = _tree+"_tmp"
	_prefix = ''# +'root://eoscms//eos/cms'*('/store' in EMuDirectory)	
	print(_tree+" = TFile.Open(\""+_prefix+EMuDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+EMuDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

for f in QCDFiles:
	_tree = 'tn_'+f.split('/')[-1].replace(".root","")
	_treeTmp = _tree+"_tmp"
	_prefix = ''# +'root://eoscms//eos/cms'*('/store' in QCDDirectory)	
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


def PDF4LHCUncStudy(MuonOptCutFile,MuNuOptCutFile,versionname):
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
	MuonSels = []
	MuNuSels = []

	# Get selections
	for line in open(MuonOptCutFile,'r'):
		if '=' in line:
			MuonSels.append([line.split('=')[0].replace('\n','').replace(' ','').replace('opt_LQuujj',''),line.split('=')[-1].replace('\n','').replace(' ','')])
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
	# trees  = [[t_ZJets]]
	#trees  = [[t_ZJets],[t_TTBar],[t_WJets],[t_DiBoson],[t_SingleTop]]#original
	#treesNames = [['t_ZJets'],['t_TTBar'],['t_WJets'],['t_DiBoson'],['t_SingleTop']]#original
	trees  = [[t_ZJets],[t_WJets]]
	treesNames = [['t_ZJets'],['t_WJets']]
	#trees  = [[t_ZJets],[t_WJets]]
	#trees  = [[t_TTBar]]
	#trees  = [[t_WJets],[t_DiBoson],[t_SingleTop],[t_TTBar]]
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
			norm_sel = dyControlRegion
		_tnew = _t.CopyTree(preselection + '*'+norm_sel)
		# Get the preselection values for all PDF members
		presel_central_value = QuickIntegral(_tnew,NormalWeight,1.0)[0]
		#if 'Signal' in uncnames[ii]:
		#	presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in cteqweightsSig]#fixme update when names are uniform across samples
		#	presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in nnpdfweightsSig]
		#	presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in mmthweightsSig]
		#else:
		#presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in cteqweights]#fixme update when names are uniform across samples
		#presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in mmthweights]
		presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in nnpdfweights]
		# Loop over selections
		for _sel in MuonSels:
			#print '   ... using tree',trees[ii][ntree]
			print '   ... using tree',treesNames[ii][ntree],'for M_LQ =',_sel[0]
			if 'Signal' in uncnames[ii]:
				_t = trees[ii][ntree]
				ntree += 1
				_tnew = _t.CopyTree(preselection + '*'+norm_sel)
				# Get the preselection values for all PDF members
				presel_central_value = QuickIntegral(_tnew,NormalWeight,1.0)[0]
				#if 'Signal' in uncnames[ii]:
				#	presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in cteqweightsSig]#fixme update when names are uniform across samples
				#	presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in nnpdfweightsSig]
				#	presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in mmthweightsSig]
				#else:
				#presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in cteqweights]#fixme update when names are uniform across samples
				#presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in mmthweights]
				presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeight+_fact,1.0)[0] for _fact in nnpdfweights]

			# Copy tree to new final selection tree
			_tnewsel = _t.CopyTree(preselection+'*'+_sel[1])
			if _tnewsel.GetEntries()<50 and ResultDict[uncnames[ii]+'_uujj']['nnpdf'] != []:#fixme changed 100 to 50
				#ResultDict[uncnames[ii]+'_uujj']['cteq'].append(  ResultDict[uncnames[ii]+'_uujj']['cteq'][-1] )
				#ResultDict[uncnames[ii]+'_uujj']['mmth'].append(  ResultDict[uncnames[ii]+'_uujj']['mmth'][-1] )
				ResultDict[uncnames[ii]+'_uujj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uujj']['nnpdf'][-1] )					
				continue
			# Get the final-selection integrals
			finsel_central_value=QuickIntegral(_tnewsel,NormalWeight,1.0)[0]
			#if 'Signal' in uncnames[ii]:
			#	finsel_varied_cteq_values = [QuickIntegral(_tnewsel,NormalWeight+_fact,1.0)[0] for _fact in cteqweightsSig]#fixme update when names are uniform across samples
			#	finsel_varied_nnpdf_values = [QuickIntegral(_tnewsel,NormalWeight+_fact,1.0)[0] for _fact in nnpdfweightsSig]
			#	finsel_varied_mmth_values = [QuickIntegral(_tnewsel,NormalWeight+_fact,1.0)[0] for _fact in mmthweightsSig]
			#else:
				#finsel_varied_cteq_values = [QuickIntegral(_tnewsel,NormalWeight+_fact,1.0)[0] for _fact in cteqweights]#fixme update when names are uniform across samples
				#finsel_varied_mmth_values = [QuickIntegral(_tnewsel,NormalWeight+_fact,1.0)[0] for _fact in mmthweights]
			finsel_varied_nnpdf_values = [QuickIntegral(_tnewsel,NormalWeight+_fact,1.0)[0] for _fact in nnpdfweights]
					

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
#	# trees  = [[t_TTBar],[t_WJets]]
#	trees  = [[t_ZJets],[t_TTBar],[t_WJets],[t_DiBoson],[t_SingleTop]]
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

def setZeroBinErrors_tgraph(data_hist,data, bg, sig_hist1, sig_hist2, blinded):
	start = False
	nBins = data.GetN()
	blindstart=0.1
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
			if blinded==False :#or (blinded==True and (data_hist.GetBinLowEdge(bins)+data_hist.GetBinWidth(bins))<blindstart):
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
	#print '\n AH: I am in QuickSysEntries(): selection is ', selection, '\n'
	h = TH1D('h','h',1,-1,3)
	h.Sumw2()
	tree.Project('h','1.0',selection)
	I = h.GetEntries()
	return str([int(1.0*I*scalefac),int(1.0*I*scalefac)]) 

def QCDStudy(sel_Muon,sel_munu,cutlogMuon,cutlogmunu,weight_Muon,weight_munu,version_name):
	global analysisChannel
	if analysisChannel=='muon' : 
		t_data  = t_DoubleMuData
		tn_data = tn_DoubleMuData
		t_QCD   = t_QCDMu
		tn_QCD  = tn_QCDMu
	if analysisChannel=='electron' : 
		t_data  = t_DoubleEleData
		tn_data = tn_DoubleEleData
		t_QCD   = t_QCDEle
		tn_QCD  = tn_QCDEle
	print 'Get DY & TTbar Data/MC normalization scale factors'
	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactors( NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion, ttControlRegion,1)
	#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = [Rz_data, Rtt_data]
	print '[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]]=',[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]]

	print '\n\n--------------\n--------------\nPerforming QCD Study'
	#################################
	######## DIMUON CHANNEL #########
	#################################	
	print '\n------ DI-'+analysisChannel+' CHANNEL -------\n'
	#intQCD = QuickIntegral(tn_QCD,sel_Muon+"*"+weight_Muon,1.0)
	#intQCDReweight = QuickIntegral(tn_QCD,sel_Muon+"*"+weight_Muon+"*(1./pow(ptHat,4.5))",1.0)
	#ptHatReweight = intQCD[0] / intQCDReweight[0]
	#ptHatReweightStr = str(ptHatReweight)
	#intQCDNu = QuickIntegral(tn_QCD,sel_munu+"*"+weight_munu,1.0)
	#intQCDReweightNu = QuickIntegral(tn_QCD,sel_munu+"*"+weight_munu+"*(1./pow(ptHat,4.5))",1.0)
	#ptHatReweightNu = intQCDNu[0] / intQCDReweightNu[0]
	#ptHatReweightStr = str(ptHatReweight)
	#ptHatReweightStrNu = str(ptHatReweightNu)
	#weight_Muon_qcd = weight_Muon+"*(1./pow(ptHat,4.5))*"+ptHatReweightStr
	#weight_munu_qcd = weight_munu+"*(1./pow(ptHat,4.5))*"+ptHatReweightStrNu
	#Q_ss = QuickIntegral(tn_QCD,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon_qcd,1.0)	
	#Q_os = QuickIntegral(tn_QCD,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon_qcd,1.0)
	Q_ss = QuickIntegral(tn_QCD,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon,1.0)
	Q_os = QuickIntegral(tn_QCD,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon,1.0)
	
	print 'Number of events in QCD MC:'
	print 'Q_ss:',Q_ss
	print 'Q_os:',Q_os

	print '\n'
	#D_ss = QuickIntegral(tn_QCD,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon,1.0)
	print 'Test: In normal Iso data, the number of same-sign events is',QuickEntries(t_data,sel_Muon + '*('+charge1+'*'+charge2+' > 0)',1.0)
	print 'Test: In normal Iso MC, the number of same-sign events is'
	print '        Z:',QuickIntegral(t_ZJets,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+'*('+str(Rz_uujj)+')',1.0)
	print '        W:',QuickIntegral(t_WJets,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon,1.0)
	print '        t:',QuickIntegral(t_SingleTop,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon,1.0)
	print '       VV:',QuickIntegral(t_DiBoson,sel_Muon +   '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon,1.0)
	print '       tt:',QuickIntegral(t_TTBar,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+'*('+str(Rtt_uujj)+')',1.0)
	print ' SMHigggs:',QuickIntegral(t_SMHiggs,sel_Muon +   '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon,1.0)
	print '      QCD:',QuickIntegral(t_QCD,sel_Muon +     '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon,1.0)
	#print 'Test: QCD Prediction in SS Isolated (using tn_ sample):', QuickIntegral(tn_QCD,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+'*(TrkIso_muon1<0.25)*(TrkIso_muon2<0.25)',1.0)

	#############################################
	data_ss_iso = QuickEntries(tn_data,sel_Muon + '*('+charge1+'*'+charge2+' > 0)'+               '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	zjet_ss_iso = QuickIntegral(tn_ZJets,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+   '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))'+'*('+str(Rz_uujj)+')',1.0)
	wjet_ss_iso = QuickIntegral(tn_WJets,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+   '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	stop_ss_iso = QuickIntegral(tn_SingleTop,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+    '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	vv_ss_iso   = QuickIntegral(tn_DiBoson,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+      '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	tt_ss_iso   = QuickIntegral(tn_TTBar,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+ '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))'+'*('+str(Rtt_uujj)+')',1.0)
	smh_ss_iso  = QuickIntegral(tn_SMHiggs,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+      '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	qcd_ss_iso_val = data_ss_iso[0]-(zjet_ss_iso[0] + wjet_ss_iso[0] + stop_ss_iso[0] + vv_ss_iso[0] + tt_ss_iso[0] + smh_ss_iso[0])
	qcd_ss_iso_err = math.sqrt(data_ss_iso[1]**2 + zjet_ss_iso[1]**2 + wjet_ss_iso[1]**2 + stop_ss_iso[1]**2 + vv_ss_iso[1]**2 + tt_ss_iso[1]**2 + smh_ss_iso[1]**2)
	qcd_ss_iso = [qcd_ss_iso_val,qcd_ss_iso_err]
	oth_ss_iso = [wjet_ss_iso[0] + stop_ss_iso[0] + vv_ss_iso[0] + smh_ss_iso[0], math.sqrt(wjet_ss_iso[1]**2 + stop_ss_iso[1]**2 + vv_ss_iso[1]**2 + smh_ss_iso[1]**2)]
	print 'data_ss_iso: ', data_ss_iso
	print 'zjet_ss_iso: ', zjet_ss_iso
	print 'tt_ss_iso: ', tt_ss_iso
	print 'oth_ss_iso: ', oth_ss_iso
	print '		wjet_ss_iso: ', wjet_ss_iso
	print '		stop_ss_iso: ', stop_ss_iso
	print '		vv_ss_iso: ', vv_ss_iso
	print '		smh_ss_iso: ', smh_ss_iso
	print 'qcd_ss_iso: ', qcd_ss_iso
	wjet_ss_iso_ent = QuickEntries(tn_WJets,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+   '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	print 'Wjets entries in ss_iso :', wjet_ss_iso_ent

	data_op_iso = QuickEntries(tn_data,sel_Muon + '*('+charge1+'*'+charge2+' < 0)'+               '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	zjet_op_iso = QuickIntegral(tn_ZJets,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+   '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))'+'*('+str(Rz_uujj)+')',1.0)
	wjet_op_iso = QuickIntegral(tn_WJets,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+   '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	stop_op_iso = QuickIntegral(tn_SingleTop,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+    '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	vv_op_iso   = QuickIntegral(tn_DiBoson,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+      '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	tt_op_iso   = QuickIntegral(tn_TTBar,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+ '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))'+'*('+str(Rtt_uujj)+')',1.0)
	smh_op_iso  = QuickIntegral(tn_SMHiggs,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+      '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	qcd_op_iso_val = data_op_iso[0]-(zjet_op_iso[0] + wjet_op_iso[0] + stop_op_iso[0] + vv_op_iso[0] + tt_op_iso[0] + smh_op_iso[0])
	qcd_op_iso_err = math.sqrt(data_op_iso[1]**2 + zjet_op_iso[1]**2 + wjet_op_iso[1]**2 + stop_op_iso[1]**2 + vv_op_iso[1]**2 + tt_op_iso[1]**2 + smh_op_iso[1]**2)
	qcd_op_iso = [qcd_op_iso_val,qcd_op_iso_err]
	oth_op_iso = [wjet_op_iso[0] + stop_op_iso[0] + vv_op_iso[0] + smh_op_iso[0], math.sqrt(wjet_op_iso[1]**2 + stop_op_iso[1]**2 + vv_op_iso[1]**2 + smh_op_iso[1]**2)]
	print 'data_op_iso: ', data_op_iso
	print 'zjet_op_iso: ', zjet_op_iso
	print 'tt_op_iso: ', tt_op_iso
	print 'oth_op_iso: ', oth_op_iso
	print '		wjet_op_iso: ', wjet_op_iso
	print '		stop_op_iso: ', stop_op_iso
	print '		vv_op_iso: ', vv_op_iso
	print '		smh_op_iso: ', smh_op_iso
	print 'qcd_op_iso: ', qcd_op_iso
	wjet_op_iso_ent = QuickEntries(tn_WJets,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+   '*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))',1.0)
	print 'Wjets entries in op_iso :', wjet_op_iso_ent

	data_ss_inv = QuickEntries(tn_data,sel_Muon + '*('+charge1+'*'+charge2+' > 0)'+               '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	zjet_ss_inv = QuickIntegral(tn_ZJets,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+   '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))'+'*('+str(Rz_uujj)+')',1.0)
	wjet_ss_inv = QuickIntegral(tn_WJets,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+   '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	stop_ss_inv = QuickIntegral(tn_SingleTop,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+    '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	vv_ss_inv   = QuickIntegral(tn_DiBoson,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+      '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	tt_ss_inv   = QuickIntegral(tn_TTBar,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+ '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))'+'*('+str(Rtt_uujj)+')',1.0)
	smh_ss_inv  = QuickIntegral(tn_SMHiggs,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+      '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	qcd_ss_inv_val = data_ss_inv[0]-(zjet_ss_inv[0] + wjet_ss_inv[0] + stop_ss_inv[0] + vv_ss_inv[0] + tt_ss_inv[0] + smh_ss_inv[0])
	qcd_ss_inv_err = math.sqrt(data_ss_inv[1]**2 + zjet_ss_inv[1]**2 + wjet_ss_inv[1]**2 + stop_ss_inv[1]**2 + vv_ss_inv[1]**2 + tt_ss_inv[1]**2 + smh_ss_inv[1]**2)
	qcd_ss_inv = [qcd_ss_inv_val,qcd_ss_inv_err]
	oth_ss_inv = [wjet_ss_inv[0] + stop_ss_inv[0] + vv_ss_inv[0] + smh_ss_inv[0], math.sqrt(wjet_ss_inv[1]**2 + stop_ss_inv[1]**2 + vv_ss_inv[1]**2 + smh_ss_inv[1]**2)]
	print 'data_ss_inv: ', data_ss_inv
	print 'zjet_ss_inv: ', zjet_ss_inv
	print 'tt_ss_inv: ', tt_ss_inv
	print 'oth_ss_inv: ', oth_ss_inv
	print '		wjet_ss_inv: ', wjet_ss_inv
	print '		stop_ss_inv: ', stop_ss_inv
	print '		vv_ss_inv: ', vv_ss_inv
	print '		smh_ss_inv: ', smh_ss_inv
	print 'qcd_ss_inv: ', qcd_ss_inv
	wjet_ss_inv_ent = QuickEntries(tn_WJets,sel_Muon + '*('+charge1+'*'+charge2+' > 0)*'+weight_Muon+   '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	print 'Wjets entries in ss_inv :', wjet_ss_inv_ent

	data_op_inv = QuickEntries(tn_data,sel_Muon + '*('+charge1+'*'+charge2+' < 0)'+               '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	zjet_op_inv = QuickIntegral(tn_ZJets,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+   '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))'+'*('+str(Rz_uujj)+')',1.0)
	wjet_op_inv = QuickIntegral(tn_WJets,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+   '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	stop_op_inv = QuickIntegral(tn_SingleTop,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+    '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	vv_op_inv   = QuickIntegral(tn_DiBoson,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+      '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	tt_op_inv   = QuickIntegral(tn_TTBar,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+ '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))'+'*('+str(Rtt_uujj)+')',1.0)
	smh_op_inv  = QuickIntegral(tn_SMHiggs,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+      '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	qcd_op_inv_val = data_op_inv[0]-(zjet_op_inv[0] + wjet_op_inv[0] + stop_op_inv[0] + vv_op_inv[0] + tt_op_inv[0] + smh_op_inv[0])
	qcd_op_inv_err = math.sqrt(data_op_inv[1]**2 + zjet_op_inv[1]**2 + wjet_op_inv[1]**2 + stop_op_inv[1]**2 + vv_op_inv[1]**2 + tt_op_inv[1]**2 + smh_op_inv[1]**2)
	qcd_op_inv = [qcd_op_inv_val,qcd_op_inv_err]
	oth_op_inv = [wjet_op_inv[0] + stop_op_inv[0] + vv_op_inv[0] + smh_op_inv[0], math.sqrt(wjet_op_inv[1]**2 + stop_op_inv[1]**2 + vv_op_inv[1]**2 + smh_op_inv[1]**2)]
	print 'data_op_inv: ', data_op_inv
	print 'zjet_op_inv: ', zjet_op_inv
	print 'tt_op_inv: ', tt_op_inv
	print 'oth_op_inv: ', oth_op_inv
	print '		wjet_op_inv: ', wjet_op_inv
	print '		stop_op_inv: ', stop_op_inv
	print '		vv_op_inv: ', vv_op_inv
	print '		smh_op_inv: ', smh_op_inv
	print 'qcd_op_inv: ', qcd_op_inv
	wjet_op_inv_ent = QuickEntries(tn_WJets,sel_Muon + '*('+charge1+'*'+charge2+' < 0)*'+weight_Muon+   '*((TrkIso_muon1>0.25) || (TrkIso_muon2>0.25))',1.0)
	print 'Wjets entries in op_inv :', wjet_op_inv_ent
	
	f_bd = [(qcd_op_inv[0]/qcd_ss_inv[0]), (qcd_op_inv[0]/qcd_ss_inv[0])* math.sqrt((qcd_op_inv[1]/qcd_op_inv[0])**2 +  (qcd_ss_inv[1]/qcd_ss_inv[0])**2)]
	data_qcd_op_iso = [(f_bd[0] * qcd_ss_iso[0]), (f_bd[0] * qcd_ss_iso[0])* math.sqrt((f_bd[1]/f_bd[0])**2 +  (qcd_ss_iso[1]/qcd_ss_iso[0])**2) ]
	print ' f_bd : ', f_bd
	print 'data_qcd_op_iso: ', data_qcd_op_iso


	#sys.exit()
        """
	studyvals = []
	for x in range(10000):#fixme todo changed from 1,000 to 10,000
		same = RR(Q_ss)
		opp = RR(Q_os)	
		studyvals.append( (same + opp) /same )
	sameoppscale =  GetStats(studyvals)
	print "\nIn QCD MC, the conversion factor between same-sign muon events and all events is:", texentry4(sameoppscale)

	Q_ssiso = QuickIntegral(tn_QCD,sel_Muon+'*(TrkIso_muon1<0.1)*('+charge1+'*'+charge2+' > 0)*'+weight_Muon,1.0)
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
        """
	#qcdBinning = [0.001,0.04,0.1,0.25,0.5,1.0,1.5,2.0]
	qcdBinning=[0.001,0.05,0.1,0.25,0.75,1.5,2.5,5.0]

	sel_Muon_ss = sel_Muon+'*('+charge1+'*'+charge2+' > 0)'
	#sel_Muon_ss = sel_Muon+'*('+charge1+'*'+charge2+' > 0)'#fixme todo put same sign back in
	#MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,2.0,5.0],sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon,weight_Muon,NormalDirectory,'qcd_nonisotagfree',ell+ell+'jj',1.0,1.0,1.0,version_name,1.0)
	#MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,2.0,5.0],sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon,weight_Muon,NormalDirectory,'qcd_nonisotagfree',ell+ell+'jj',1.0,1.0,1.0,version_name,1.0)
	#MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,1.5,2.0],sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon,weight_Muon,NormalDirectory,'qcd_nonisoPAStagfree',ell+ell+'jj',1.0,1.0,1.0,version_name,1.0)
	#MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,1.5,2.0],sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon,weight_Muon,NormalDirectory,'qcd_nonisoPAStagfree',ell+ell+'jj',1.0,1.0,1.0,version_name,1.0)
	#fixme todo added SSNonIsoDataRescale for data rescale
	###MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.02,0.04,0.075,0.1,0.15,0.2,0.4,0.75,1.0,1.5,2.0,3.5],sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon_qcd,weight_Muon,NormalDirectory,'qcd_nonisotagfree',ell+ell+'jj',1.0,1.0,1.0,version_name,1.0)
	###MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.02,0.04,0.075,0.1,0.15,0.2,0.4,0.75,1.0,1.5,2.0,3.5],sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon_qcd,weight_Muon,NormalDirectory,'qcd_nonisotagfree',ell+ell+'jj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu SS (non-isolated)",qcdBinning,sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon+'*('+charge1+'*'+charge2+' > 0)',weight_Muon,NormalDirectory,'qcd_nonisotagfree',ell+ell+'jj',Rz_uujj,1.0,Rtt_uujj,version_name,SSNonIsoDataRescale[0])
	MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu SS (non-isolated)",qcdBinning,sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon+'*('+charge1+'*'+charge2+' > 0)',weight_Muon,NormalDirectory,'qcd_nonisotagfree',ell+ell+'jj',Rz_uujj,1.0,Rtt_uujj,version_name,SSNonIsoDataRescale[0])
	MakeBasicPlotQCD("Pt_muon1","p_{T}(#mu_{1})[GeV] SS (non-isolated)",ptbinning,sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon+'*('+charge1+'*'+charge2+' > 0)',weight_Muon,NormalDirectory,'qcd_nonisotagfree',ell+ell+'jj',Rz_uujj,1.0,Rtt_uujj,version_name,SSNonIsoDataRescale[0])
	MakeBasicPlotQCD("Pt_muon2","p_{T}(#mu_{2})[GeV] SS (non-isolated)",ptbinning2,sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon+'*('+charge1+'*'+charge2+' > 0)',weight_Muon,NormalDirectory,'qcd_nonisotagfree',ell+ell+'jj',Rz_uujj,1.0,Rtt_uujj,version_name,SSNonIsoDataRescale[0])

	#MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,1.5,2.0],sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon,weight_Muon,NormalDirectory,'qcd_nonisoPAStagfree',ell+ell+'jj',1.0,1.0,1.0,version_name,SSNonIsoDataRescale[0])
	#MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,1.5,2.0],sel_Muon_ss,sel_Muon_ss+'*'+weight_Muon,weight_Muon,NormalDirectory,'qcd_nonisoPAStagfree',ell+ell+'jj',1.0,1.0,1.0,version_name,SSNonIsoDataRescale[0])

"""
	print '\nFor final selections, this gives estimates:\n'


	#for plotmass in [ 200, 250, 300 , 350 , 400 , 450 , 500 , 550 , 600 , 650 , 700 , 750 , 800 , 850 , 900 , 950 , 1000 , 1050 , 1100 , 1150 , 1200 , 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000] :
	for plotmass in [300]:
		#channel=ell+ell+'jj'
		channel='HHres'
		fsel = ((os.popen('cat '+cutlogMuon+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+sel_Muon+fsel+')'

		Nss_noniso_data = QuickEntries(tn_DoubleMuData,selection + '*('+charge1+'*'+charge2+' > 0)',1.0)
		Nss_noniso_mc = QuickMultiIntegral([tn_DiBoson,tn_TTBar,tn_WJets,tn_ZJets,tn_SingleTop,tn_SMHiggs],selection+'*('+charge1+'*'+charge2+' > 0)*'+weight_Muon,[1.0,Rtt_uujj,1.0,Rz_uujj,1.0,1.0])
		Nss_noniso_qcdest = [Nss_noniso_data[0] - Nss_noniso_mc[0] ,  math.sqrt(Nss_noniso_data[1]**2 + Nss_noniso_mc[1]**2)]
		N_iso_qcdest = [ Nss_noniso_qcdest[0]*SSNonIsoDataRescale[0], (math.sqrt((Nss_noniso_qcdest[1]/Nss_noniso_qcdest[0])**2 + (SSNonIsoDataRescale[1]/SSNonIsoDataRescale[0])**2))*Nss_noniso_qcdest[0]*SSNonIsoDataRescale[0] ]
		print 'Nss_noniso_data[0]: ', Nss_noniso_data[0] , 'Nss_noniso_mc[0]: ', Nss_noniso_mc[0]
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

	Q_noniso = QuickIntegral(tn_QCDMu,sel_low_munu+'*'+weight_munu,1.0)
	Q_iso = QuickIntegral(tn_QCDMu,sel_low_munu + '*(TrkIso_muon1<0.1)*'+weight_munu,1.0)

	B_noniso = QuickMultiIntegral([tn_DiBoson,tn_TTBar,tn_WJets,tn_ZJets,tn_SingleTop],sel_low_munu+'*'+weight_munu,[1.0,1.0,1.0,1.0,1.0])
	B_iso = QuickMultiIntegral([tn_DiBoson,tn_TTBar,tn_WJets,tn_ZJets,tn_SingleTop],sel_low_munu+'*(TrkIso_muon1<0.1)*'+weight_munu,[1.0,1.0,1.0,1.0,1.0])

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

	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated)",[25,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_Muon,NormalDirectory,'qcd_noniso_unweightedtagfree','uvjj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated, qcd reweighted)",[25,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_Muon,NormalDirectory,'qcd_noniso_weightedtagfree','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD)
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated)",[25,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_Muon,NormalDirectory,'qcd_noniso_unweightedPAStagfree','uvjj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated, qcd reweighted)",[25,0,10],sel_low_munu,sel_low_munu+'*'+weight_munu,weight_Muon,NormalDirectory,'qcd_noniso_weightedPAStagfree','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD)


	sel__munu = sel_munu + '*(MT_uv>50)*(Pt_miss>55)'

	print '\nFor final selections, this gives estimates:\n'

	#for plotmass in [ 200, 250, 300 , 350 , 400 , 450 , 500 , 550 , 600 , 650 , 700 , 750 , 800 , 850 , 900 , 950 , 1000 , 1050 , 1100 , 1150 , 1200 , 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000] :
	for plotmass in [300]:
		channel='uvjj'
		fsel = ((os.popen('cat '+cutlogmunu+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+sel_munu+fsel+')'
		[Nest,Nest_err] = QuickIntegral(tn_QCDMu,selection+'*'+weight_munu,ScaleFactor_QCD*FakeRate)
		Nest_toterr = math.sqrt(((math.sqrt((FakeRate_err/FakeRate)**2 + (ScaleFactor_QCD_Err/ScaleFactor_QCD)**2))*Nest)**2 + Nest_err **2 ) 
		print plotmass ,'&',texentry4([Nest,Nest_toterr]),'\\\\'

	print '\n'
"""


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
			#treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson,t_ZJetsControl])
			treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson])#fixme todo no idea what zjetscontrol is...
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
		treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson])
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
			treefeed.append([te_ZJets,te_WJets,te_SingleTop,te_DiBoson])
			treefeed.append([t_ZJets,t_WJets,t_SingleTop,t_DiBoson])
			treefeed.append(t_DoubleMuData)
			scalefacs = [1,1,[-1.0*rz,-1.0*rw,-1.0,-1.0],[rz,rw,1,1],1]
			selections = [ this_sel +dataHLT+dataHLTEMUADJ, this_sel+'*'+NormalWeightEMuNoHLT, this_sel+'*'+NormalWeight ]
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
		treefeed.append([te_ZJets,te_WJets,te_SingleTop,te_DiBoson])
		treefeed.append([t_ZJets,t_WJets,t_SingleTop,t_DiBoson])
		treefeed.append(t_DoubleMuData)

		scalefacs = [1,1,[-1.0*rz,-1.0*rw,-1.0,-1.0],[rz,rw,1,1],1]
		selections = [ this_sel +dataHLT+dataHLTEMUADJ, this_sel+'*'+NormalWeightEMuNoHLT, this_sel+'*'+NormalWeight ]		
	
		QuickTableLineTTDD(treefeed,selections,scalefacs,texfile,csvfile)

		nline += 1

def QuickSysTableLine(treestruc,selection,inp_weight,scalefacs,fsys,chan,rglobals,rglobalb,plotmass,sysmethod):
	[_stree,_dtree,_btrees] = treestruc
#	old_s = QuickSysIntegral(_stree,selection,scalefacs[0],rglobals)
#	old_bs = [QuickSysIntegral(_btrees[b],selection,scalefacs[1][b],rglobalb) for b in range(len(_btrees))]
#	old_d = QuickSysEntries (_dtree,selection+dataHLT,scalefacs[2])
#	print 'old_s is ' , old_s
#	print 'old_bs is ' , old_bs
#	print 'old_d is ' , old_d

	# AH:-----------------------------
	#plotmass = 300
	channel = 'HHres'
#	recovariableFileName = ''
#	if int(plotmass) > 400:
#		recovariableFileName = 'bdt_discrim_M550'
#	elif int(plotmass) <= 400:
#		recovariableFileName = 'bdt_discrim_M300'
#	recovariableFileName = ''
#	if int(plotmass) > 400:
#		recovariableFileName = 'bdt_discrims3_high'
#	elif int(plotmass) <= 400:
#		recovariableFileName = 'bdt_discrims3_low'

	recovariableFileName = 'bdt_discrim_M' + plotmass
	_nonWeightVary = ['JESup','JESdown','MESup','MESdown','JERup','JERdown','MER'] # AH: this is just a holder to specify the variations that need the corresponding branches
	recovariable = recovariableFileName
	for vary in _nonWeightVary:
		if sysmethod == vary:
			recovariable += sysmethod
	print '\n AH: I am in QuickSysTableLine(): plotmass is ', plotmass, ' discriminant is ', recovariable, 'recovariableFileName ', recovariableFileName,'\n'
	presentationbinning = [100,-0.7,0.7]
	DataRecoStyle=[0,20,1.5,1,1]
	Label=["tmp","Events / bin"]
	
	# AH: Todo: I have to check this again !
	#selec_1 = selection[1:selection.find("weight_")-11] # AH: fixme: if using PU_syst the string "weight_central" will not appear here ! >> use "weight_" instead ?
	#weight = selection[selection.find("weight_")-10:len(selection)]
	#selec_2 = weight[weight.find('Pt_muon1')-2:len(weight)-1]
	#weight_new = weight[0:weight.find('Pt_muon1')-3]
	#selec_new = selec_1 + '*' + selec_2
	#print '\n AH: I am in QuickSysTableLine(): selection is ', selection, '\n'
	##print '\n AH: I am in QuickSysTableLine(): selec_1 is ', selec_1, '\n'
	##print '\n AH: I am in QuickSysTableLine(): selec_2 is ', selec_2, '\n'

	selec_new = selection
	weight_new = inp_weight
	print '\n AH: I am in QuickSysTableLine(): selec_new is \n', selec_new, '\n'
	print '\n AH: I am in QuickSysTableLine(): weight_new is \n', weight_new, '\n'
	
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',_dtree,recovariable,presentationbinning,selec_new+dataHLT,DataRecoStyle,Label)
	hs_rec_Signal=CreateHisto('hs_rec_Signal','M_{R} = '+str(plotmass)+' GeV, ',_stree,recovariable,presentationbinning,selec_new+'*('+str(scalefacs[0]*rglobals)+')*'+weight_new,DataRecoStyle,Label)
	print 'Doing ttbar:'
	tt_sel_weight = selec_new+'*('+str(scalefacs[1][0])+')*'+weight_new
	#print '\n AH: I am in QuickSysTableLine(): tt_sel_weight is ', tt_sel_weight, '\n'
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',_btrees[0],recovariable,presentationbinning,selec_new+'*('+str(scalefacs[1][0]*rglobalb)+')*'+weight_new,DataRecoStyle,Label)
	print 'Doing ZJets:'
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',_btrees[1],recovariable,presentationbinning,selec_new+'*('+str(scalefacs[1][1]*rglobalb)+')*'+weight_new,DataRecoStyle,Label)
	print 'Doing WJets:'
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',_btrees[2],recovariable,presentationbinning,selec_new+'*('+str(scalefacs[1][2]*rglobalb)+')*'+weight_new,DataRecoStyle,Label)
	print 'Doing SingleTop:'
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',_btrees[3],recovariable,presentationbinning,selec_new+'*'+weight_new,DataRecoStyle,Label) ## AH: fixme : add rglobalb
	print 'Doing DiBoson:'
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',_btrees[4],recovariable,presentationbinning,selec_new+'*'+weight_new,DataRecoStyle,Label)
	print 'Doing SMHiggs:'
	hs_rec_SMHiggs=CreateHisto('hs_rec_SMHiggs','SM Higgs',_btrees[6],recovariable,presentationbinning,selec_new+'*'+weight_new,DataRecoStyle,Label)
	print 'Doing QCD:'
	if (not useDataDrivenQCD):
		hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD',_btrees[5],recovariable,presentationbinning,selec_new+'*'+weight_new,DataRecoStyle,Label)
	else:
		#--- using normal directory with ss requirement
		qcd_sel = selec_new.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' > 0)')
		hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD'              ,_btrees[5],recovariable,presentationbinning,qcd_sel+dataHLT,DataRecoStyle,Label) # + dataHLT ??
		print '   Doing 2nd:'
		hs_ss_rec_TTBar=CreateHisto('hs_ss_rec_TTBar','TTBar'  ,_btrees[0],recovariable,presentationbinning,qcd_sel+'*'+weight_new+'*('+str(scalefacs[1][0]*rglobalb)+')',DataRecoStyle,Label)
		print '   Doing :'
		hs_ss_rec_ZJets=CreateHisto('hs_ss_rec_ZJets','Z+Jets' ,_btrees[1],recovariable,presentationbinning,qcd_sel+'*'+weight_new+'*('+str(scalefacs[1][1]*rglobalb)+')',DataRecoStyle,Label)
		print '   Doing :'
		hs_ss_rec_WJets=CreateHisto('hs_ss_rec_WJets','W+Jets' ,_btrees[2],recovariable,presentationbinning,qcd_sel+'*'+weight_new+'*('+str(scalefacs[1][2]*rglobalb)+')',DataRecoStyle,Label)
		print '   Doing :'
		hs_ss_rec_SingleTop=CreateHisto('hs_ss_rec_STop','STop',_btrees[3],recovariable,presentationbinning,qcd_sel+'*'+weight_new                      ,DataRecoStyle,Label)
		print '   Doing :'
		hs_ss_rec_DiBoson=CreateHisto('hs_ss_rec_VV','VV'      ,_btrees[4],recovariable,presentationbinning,qcd_sel+'*'+weight_new                      ,DataRecoStyle,Label)
		print '   Doing last:'
		hs_ss_rec_SMHiggs=CreateHisto('hs_ss_rec_SMH','SMH'    ,_btrees[6],recovariable,presentationbinning,qcd_sel+'*'+weight_new                      ,DataRecoStyle,Label)
		##
		hs_ss_rec_TTBar.Scale(-1.0)
		hs_ss_rec_ZJets.Scale(-1.0)
		hs_ss_rec_WJets.Scale(-1.0)
		hs_ss_rec_SingleTop.Scale(-1.0)
		hs_ss_rec_DiBoson.Scale(-1.0)
		hs_ss_rec_SMHiggs.Scale(-1.0)
		hs_rec_QCD.Add(hs_ss_rec_WJets)
		hs_rec_QCD.Add(hs_ss_rec_DiBoson)
		hs_rec_QCD.Add(hs_ss_rec_ZJets)
		hs_rec_QCD.Add(hs_ss_rec_TTBar)
		hs_rec_QCD.Add(hs_ss_rec_SingleTop)
		hs_rec_QCD.Add(hs_ss_rec_SMHiggs)
		for k in range(hs_rec_QCD.GetNbinsX()):
			if (hs_rec_QCD.GetBinContent(k+1) <= 0):
				hs_rec_QCD.SetBinContent(k+1, 0.)
				hs_rec_QCD.SetBinError(k+1, 0.)
		hs_rec_QCD.Scale(fbd[0])
	
	# AH: create output root file to store histogram
	if sysmethod == '':
		outHistRootFile = TFile(channel+str(plotmass)+'_'+recovariableFileName+'_13TeV_new.root', "RECREATE")
		dirThis = outHistRootFile.mkdir(channel+ell+ell+'jj')
		dirThis.cd()
		print '\n AH: I am in QuickSysTableLine(): sysmethod is ', sysmethod, '\n'
		hs_rec_Data.Write("data_obs")
		hs_rec_Signal.Write("HHres")
		hs_rec_TTBar.Write("TTBar")
		hs_rec_ZJets.Write("ZJets")
		hs_rec_WJets.Write("WJets")
		hs_rec_SingleTop.Write("sTop")
		hs_rec_DiBoson.Write("VV")
		hs_rec_QCD.Write("QCD")
		hs_rec_SMHiggs.Write("SMH")
	else:
		outHistRootFile = TFile(channel+str(plotmass)+'_'+recovariableFileName+'_13TeV_new.root', "UPDATE")
		dirValid = outHistRootFile.cd(channel+ell+ell+'jj')
		if (not dirValid):
			dirThis = outHistRootFile.mkdir(channel+ell+ell+'jj')
			dirThis.cd()
		outHistRootFile.cd(channel+ell+ell+'jj')
		sysmethod = sysmethod.replace('up','Up')
		sysmethod = sysmethod.replace('down','Down')
		print '\n AH: I am in QuickSysTableLine(): sysmethod is ', sysmethod, '\n'
		hs_rec_Data.Write("data_obs"+"_"+sysmethod)
		hs_rec_Signal.Write("HHres"+"_"+sysmethod)
		hs_rec_TTBar.Write("TTBar"+"_"+sysmethod)
		hs_rec_ZJets.Write("ZJets"+"_"+sysmethod)
		hs_rec_WJets.Write("WJets"+"_"+sysmethod)
		hs_rec_SingleTop.Write("sTop"+"_"+sysmethod)
		hs_rec_DiBoson.Write("VV"+"_"+sysmethod)
		hs_rec_QCD.Write("QCD"+"_"+sysmethod)
		hs_rec_SMHiggs.Write("SMH"+"_"+sysmethod)

	outHistRootFile.Close()

	_data = str([int(1.0*hs_rec_Data.GetEntries()*scalefacs[2]),int(1.0*hs_rec_Data.GetEntries()*scalefacs[2])])
	_sg = str([hs_rec_Signal.Integral(),int(hs_rec_Signal.GetEntries())])
	_tt = str([hs_rec_TTBar.Integral(),int(hs_rec_TTBar.GetEntries())])
	_zj = str([hs_rec_ZJets.Integral(),int(hs_rec_ZJets.GetEntries())])
	_wj = str([hs_rec_WJets.Integral(),int(hs_rec_WJets.GetEntries())])
	_st = str([hs_rec_SingleTop.Integral(),int(hs_rec_SingleTop.GetEntries())])
	_db = str([hs_rec_DiBoson.Integral(),int(hs_rec_DiBoson.GetEntries())])
	_qc = str([hs_rec_QCD.Integral(),int(hs_rec_QCD.GetEntries())])
	_sh = str([hs_rec_SMHiggs.Integral(),int(hs_rec_SMHiggs.GetEntries())])
	
	_s = _sg
	_bs = [_tt,_zj,_wj,_st,_db,_qc,_sh]
	_d = _data
	print '_s is ' , _s
	print '_bs is ' , _bs
	print '_d is ' , _d
	# AH:-----------------------------


	sysline = 'L_'+chan + ' = ['
	sysline += (_s)+' , '
	sysline += (_d)+' , '
	for x in _bs:
		sysline += ' '+(x)
		sysline += ' , '
	sysline = sysline[0:-2]+' ]'

	#print selection.replace('\n','')
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
	#print '\n AH: I am in ModSelection(): selection is ', selection, '\n'
	# variables used in final selections have to be present here
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
	_kinematicvariables += ['Pt_Hjet1','Pt_Hjet2','Pt_Zjet1','Pt_Zjet2','CISV_bjet1','CISV_bjet2','CMVA_bjet1','CMVA_bjet2']
	_kinematicvariables += ['CMVA_Zjet1','CMVA_Zjet2']

	_weights = ['weight_nopu','weight_central', 'weight_pu_up', 'weight_pu_down'] # AH: this is not used, can be commented out?
	_variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER'] # AH: this is just a holder to specify the variations that need the corresponding branches
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
			selection = '(1.025)*'+selection
		if sysmethod == 'LUMIdown':
			selection = '(0.975)*'+selection

		if sysmethod == 'MUONIDISOup':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = '(1.04)*'+selection
			if 'uvjj' in channel_log: 
				selection = '(1.02)*'+selection

		if sysmethod == 'MUONIDISOdown':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = '(0.96)*'+selection
			if 'uvjj' in channel_log: 
				selection = '(0.98)*'+selection

		if sysmethod == 'MUONHLTup':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = '(1.01)*'+selection
			if 'uvjj' in channel_log: 
				selection = '(1.015)*'+selection

		if sysmethod == 'MUONHLTdown':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = '(0.99)*'+selection
			if 'uvjj' in channel_log: 
				selection = '(0.985)*'+selection

		if sysmethod == 'PUup':
			selection = selection.replace('weight_central','weight_pu_up')
		if sysmethod == 'PUdown':
			selection = selection.replace('weight_central','weight_pu_down')

		if sysmethod == 'HIPup ':#Per-muon uncertainty: 0.5% (pT < 300 GeV), 1% (pT > 300 GeV)
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = '((1.005*(Pt_muon1<300)+1.01*(Pt_muon1>300))*(1.005*(Pt_muon2<300)+1.01*(Pt_muon2>300)))*'+selection
			if 'uvjj' in channel_log: 
				selection = '(1.005*(Pt_muon1<300)+1.01*(Pt_muon1>300))*'+selection
		if sysmethod == 'HIPdown':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = '((0.995*(Pt_muon1<300)+0.99*(Pt_muon1>300))*(0.995*(Pt_muon2<300)+0.99*(Pt_muon2>300)))*'+selection
			if 'uvjj' in channel_log: 
				selection = '(0.995*(Pt_muon1<300)+0.99*(Pt_muon1>300))*'+selection
		if sysmethod == 'BTAGup':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = selection.replace(bTagFinalSF,bTagFinalSFup)
		if sysmethod == 'BTAGdown':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = selection.replace(bTagFinalSF,bTagFinalSFdown)

		if sysmethod == 'QCDscaleR1F2':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = selection+'*(scaleWeight_R1_F2/scaleWeight_R1_F1)'

		if sysmethod == 'QCDscaleR2F1':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = selection+'*(scaleWeight_R2_F1/scaleWeight_R1_F1)'

		if sysmethod == 'QCDscaleR2F2':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = selection+'*(scaleWeight_Up/scaleWeight_R1_F1)'

		if sysmethod == 'QCDscaleR1F0p5':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = selection+'*(scaleWeight_R1_F0p5/scaleWeight_R1_F1)'

		if sysmethod == 'QCDscaleR0p5F1':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = selection+'*(scaleWeight_R0p5_F1/scaleWeight_R1_F1)'

		if sysmethod == 'QCDscaleR0p5F0p5':
			if 'uujj' in channel_log or 'HH' in channel_log:
				selection = selection+'*(scaleWeight_R0p5_F0p5/scaleWeight_R1_F1)'

	return selection


def SysTable(optimlog, PreSelection_uujj, selection_uujj,selection_uvjj,NormalDirectory, NormalWeight, weight,sysmethod):
	print '\n AH: I am in SysTable(): selection_uujj is ', selection_uujj, '\n'
	#AH:selection_uujj = selection_uujj+'*'+weight
	#AH:selection_uvjj = selection_uvjj+'*'+weight
	NormalWeight      = ModSelection(NormalWeight,sysmethod,optimlog)
	PreSelection_uujj = ModSelection(PreSelection_uujj,sysmethod,optimlog)
	weight            = ModSelection(weight,sysmethod,optimlog)
	selection_uujj    = ModSelection(selection_uujj,sysmethod,optimlog)
	selection_uvjj = ModSelection(selection_uvjj,sysmethod,optimlog)
	print '\n AH: I am in SysTable(): after ModSelection, selection_uujj is ', selection_uujj, '\n'
	print '\n AH: I am in SysTable(): after ModSelection, weight is ', weight, '\n'
	
	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactors( PreSelection_uujj+'*'+NormalWeight, NormalDirectory, dyControlRegion, ttControlRegion,0)
	#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = [Rz_data, Rtt_data]
	# AH: To speed things up when debugging
	
	#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( selection_uvjj, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)')
	# AH: I set these factors to 1
	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]]=[[1.,0.],[1.,0,]]

	Rz_uujj_print = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
	Rtt_uujj_print = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
	Rw_uvjj_print = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
	Rtt_uvjj_print = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))
	print '\n AH: I am in SysTable(): sysmethod is ', sysmethod, '\n'
	print sysmethod+' & ' + Rz_uujj_print+' & '+Rtt_uujj_print+' & '+Rw_uvjj_print+' & '+Rtt_uvjj_print+' \\\\'

	if 'uujj' in optimlog or 'HH' in optimlog: # AH:
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
		#rz *= 1.1#fixme adding this to cover discrepancy between samples
		rz += _e_rz 
	if sysmethod == 'ZNORMdown': 
		#rz *= 0.9#fixme adding this to cover discrepancy between samples
		rz += -_e_rz 
	if sysmethod == 'WNORMup':     rw += _e_rw
	if sysmethod == 'WNORMdown':   rw += -_e_rw 
	if sysmethod == 'TTNORMup':  
		#rt *= 1.1#fixme adding this to cover kinematic dependence of R_uu/eu
		rt += _e_rt
	if sysmethod == 'TTNORMdown':  
		#rt *= 0.9#fixme adding this to cover kinematic dependence of R_uu/eu
		rt += -_e_rt 	

	#if sysmethod == 'SHAPETT' : 
		#if 'uujj' in optimlog: 
		#	rt = (1.+.01*shapesys_uujj_ttbar )*rt
		#if 'uvjj' in optimlog: 
		#	rt = (1.+.01*shapesys_uvjj_ttbar )*rt

	# if sysmethod == 'SHAPEZ'  : rz = (1.+.01*shapesys_uujj_zjets)*rz
	# if sysmethod == 'SHAPEW'  : rw = (1.+.01*shapesys_uvjj_wjets)*rw


	sysfile = optimlog.replace('.txt','_systable_'+sysmethod+'.txt')
	print '\n AH: I am in SysTable(): sysfile is ', sysfile, '\n'
	#headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV'] # AH
	headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV', 'QCD', 'SMH']  # AH


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
		#mass = masschan.split('jj')[-1] # AH
		mass = masschan.split('HHres')[-1]
		chan = 't_'+masschan.split('_')[-1]
		print '\n AH: I am in SysTable(): masschan is ', masschan, '\n'
		print '\n AH: I am in SysTable(): chan is ', chan, '\n'
		print '\n AH: I am in SysTable(): mass is ', mass, '\n'
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		this_sel = '('+selection+fsel+')'

		print ' *'*100
		#print '\n AH: I am in SysTable(): pdf_MASS is ', pdf_MASS, '\n'
		for ii in range(len(pdf_MASS)):
			pdfm = pdf_MASS[ii]
			if str(pdfm) == mass:
				nalign = ii
		#print nalign
		print '\n AH: I am in SysTable(): nalign is ', nalign, '\n'


		if sysmethod == 'ALIGN':
			if 'uujj' in optimlog or 'HH' in optimlog:
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
			if 'uujj' in optimlog or 'HH' in optimlog:
				_rt *= (1.0+shapesysvar_uujj_ttjets[nalign]*0.01)
			if 'uvjj' in optimlog:
				_rt *= (1.0+shapesysvar_uvjj_ttjets[nalign]*0.01)

		if sysmethod == 'SHAPEZ':
			_rz *= (1.0+shapesysvar_uujj_zjets[nalign]*0.01)

		if sysmethod == 'SHAPEW':
			_rw *= (1.0+shapesysvar_uvjj_wjets[nalign]*0.01)

		if 'PDF'  in sysmethod:
			if 'uujj' in optimlog or 'HH' in optimlog:
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
		
		if (useDataDrivenQCD):
			#--- using normal directory with ss requirement
			t_estQCD = t_DoubleMuData
			print 'Using data-driven for QCD est.'
		else:
			t_estQCD = t_QCDMu
			print 'Using QCD MC.'
		
		treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson,t_estQCD,t_SMHiggs]) # AH
		scalefacs = [rsig,[_rt,_rz,_rw,rstop,rdiboson,1,1],1]	# AH
		#print '\n AH: I am in SysTable(): this_sel is ', this_sel, '\n'
		print '\n AH: I am in SysTable(): rglobals is ', rglobals, '\n'
		print '\n AH: I am in SysTable(): rglobalb is ', rglobalb, '\n'
		print '\n AH: I am in SysTable(): scalefacs is ', scalefacs, '\n'
		QuickSysTableLine(treefeed,this_sel,weight,scalefacs,sysfile,chan,rglobals,rglobalb,mass,sysmethod)
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

	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactors( selection_uujj+weightmod, NormalDirectory, dyControlRegion, ttControlRegion,1)
#	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( selection_uvjj+weightmod_uvjj, NormalDirectory, '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)', '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)') # AH
	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]]=[[1.,0.],[1.,0,]]


	[Rtt_uujj, Rtt_uujj_err] = [emu_id_eff, emu_id_eff_err]

	Rz_uujj_print = str(round(Rz_uujj,3)) + ' $\\pm$ ' + str(round(Rz_uujj_err,3))	
	Rtt_uujj_print = str(round(Rtt_uujj,3)) + ' $\\pm$ ' + str(round(Rtt_uujj_err,3))	
	Rw_uvjj_print = str(round(Rw_uvjj,3)) + ' $\\pm$ ' + str(round(Rw_uvjj_err,3))	
	Rtt_uvjj_print = str(round(Rtt_uvjj,3)) + ' $\\pm$ ' + str(round(Rtt_uvjj_err,3))	
	print sysmethod+' & ' + Rz_uujj_print+' & '+Rtt_uujj_print+' & '+Rw_uvjj_print+' & '+Rtt_uvjj_print+' \\\\'

#	if 'uujj' in optimlog:
	if 'uujj' in optimlog or 'HH' in optimlog: # AH:
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

#	headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV']
	headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV', 'QCD', 'SMH']  # AH


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
#		mass = masschan.split('jj')[-1]
		mass = masschan.split('HHres')[-1] # AH
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
#		treefeed.append([te_ZJets,te_WJets,te_SingleTop,te_DiBoson])
		treefeed.append([te_ZJets,te_WJets,te_SingleTop,te_DiBoson,te_QCDMu,te_SMHiggs]) # AH
#		treefeed.append([t_ZJets,t_WJets,t_SingleTop,t_DiBoson])
		treefeed.append([t_ZJets,t_WJets,t_SingleTop,t_DiBoson,t_QCDMu,t_SMHiggs]) # AH
		treefeed.append(t_DoubleMuData)


		#scalefacs = [rsig,_rt,[-1.0*_rz,-1.0*_rw,-1.0*rstop,-1.0*rdiboson,-1,-1],[_rz,_rw,rstop,rdiboson],1,1,1] # AH:
		scalefacs = [rsig,_rt,[-1.0*_rz,-1.0*_rw,-1.0*rstop,-1.0*rdiboson],[_rz,_rw,rstop,rdiboson],1]
		selections = [ this_sel_unmod +dataHLT+dataHLTEMUADJ, this_sel_unmod+'*'+NormalWeightEMuNoHLT, this_sel+weightmod ]		

		QuickSysTableLineTTDD(treefeed,selections,scalefacs,sysfile,chan,rglobals,rglobalb)
		# break

def FullAnalysis(optimlog,PreSelection_uujj,selection_uujj,selection_uvjj,NormalDirectory,NormalWeight,weight,usedd):
	#print '\n AH: I am in FullAnalysis(): optimlog is ', optimlog, '\n'
	#print '\n AH: I am in FullAnalysis(): selection_uujj is ', selection_uujj, '\n'
	TTDD = False
	if usedd=='TTBarDataDriven':
		TTDD=True

	_Variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','WNORMup','WNORMdown','TTNORMup','TTNORMdown','MUONIDISOup','MUONIDISOdown','HIPup','HIPdown','MUONHLTup','MUONHLTdown','BTAGup','BTAGdown','PDF','SHAPETT','SHAPEZ','SHAPEW','QCDscaleR1F2','QCDscaleR2F1','QCDscaleR2F2','QCDscaleR1F0p5','QCDscaleR0p5F1','QCDscaleR0p5F0p5']

	#_Variations = ['']

	for v in _Variations:
		print ' -'*50
		print 'Processing table for variation: ',v
		if (optimlog.replace('.txt','_systable_'+v+'.txt')) in str(os.popen('ls '+optimlog.replace('.txt','_systable_'+v+'.txt')).readlines()):
			print 'Already present ... skipping. '
			continue
		if TTDD:
			SysTableTTDD(optimlog, selection_uujj, selection_uvjj,NormalDirectory, weight,v)
		else:
			SysTable(optimlog, PreSelection_uujj, selection_uujj, selection_uvjj,NormalDirectory, NormalWeight, weight,v)




def GetScaleFactors(n1,n2,a1,a2,b1,b2,o1,o2):
	Ra = 1.0
	Rb = 1.0
	for x in range(10):
		Ra = (n1 - Rb*b1 - o1)/(a1)
		Rb = (n2 - Ra*a2 - o2)/(b2) 
	return [Ra, Rb]

def GetScaleFactorsAndFbd(n1,n2,z1,z2,t1,t2,o1,o2,n1c,n2c,z1c,z2c,t1c,t2c,o1c,o2c,nb,zb,tb,ob,nd,zd,td,od):
	#	print ' I am in GetScaleFactorsAndFbd() '
	#	print ' printing all input '
	#	print ' n1  n2  z1  z2  t1  t2  o1  o2  ', n1,n2,z1,z2,t1,t2,o1,o2
	#	print ' n1c n2c z1c z2c t1c t2c o1c o2c ', n1c,n2c,z1c,z2c,t1c,t2c,o1c,o2c
	#	print ' nb, zb, tb, ob, nd, zd, td, od  ', nb,zb,tb,ob,nd,zd,td,od
	
	fbd = 1.0
	Rz = 1.0
	Rt = 1.0
	for x in range(10):
		q1c = n1c - Rz*z1c - Rt*t1c - o1c
		q2c = n2c - Rz*z2c - Rt*t2c - o2c
		Rz = (n1 - Rt*t1 - fbd*q1c - o1)/(z1)
		Rt = (n2 - Rz*z2 - fbd*q2c - o2)/(t2)
		fbd = (nb - Rz*zb - Rt*tb - ob)/(nd - Rz*zd - Rt*td - od)
		#print 'iter_th', x, 'Rz', Rz, 'Rt', Rt, 'fbd', fbd
	return [Rz, Rt, fbd]

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

def GetNormalizationScaleFactors( selection, FileDirectory, controlregion_1, controlregion_2, canUseTTDD):
	global analysisChannel
	print 'getting '+analysisChannel+' scale factors :'
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_DoubleMuData,selection + '*' + controlregion_1,1.0)
	# print QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	# sys.exit()
	selection_data = selection.split('*(fact')[0]
	if analysisChannel=='muon'     :
		t_data  = t_DoubleMuData
		tn_data = tn_DoubleMuData
		t_QCD  = t_QCDMu
		tn_QCD = tn_QCDMu
	if analysisChannel=='electron' :
		t_data  = t_DoubleEleData
		tn_data = tn_DoubleEleData
		t_QCD  = t_QCDEle
		tn_QCD = tn_QCDEle

	N1 = QuickEntries(t_data,selection_data + '*' + controlregion_1+dataHLT,1.0)
	#print selection_data + '*' + controlregion_1+dataHLT
	N2 = QuickEntries(t_data,selection_data + '*' + controlregion_2+dataHLT,1.0)

	Z1 = QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBar,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(t_WJets,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)
	H1 = QuickIntegral(t_SMHiggs,selection   + '*' + controlregion_1,1.0)
	
	Z2 = QuickIntegral(t_ZJets,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBar,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(t_WJets,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)
	H2 = QuickIntegral(t_SMHiggs,selection   + '*' + controlregion_2,1.0)
	
	if (not useDataDrivenQCD):
		print ' using QCD MC when calculating '+analysisChannel+' scale factors'
		q1 = QuickIntegral(t_QCD,selection   + '*' + controlregion_1,1.0)
		q2 = QuickIntegral(t_QCD,selection   + '*' + controlregion_2,1.0)		
	else:
		print ' using QCD data-driven when calculating '+analysisChannel+' scale factors'
		print ' QCD fake rate is ', fbd
		selec_qcd_data = selection_data.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' > 0)*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))')
		selec_qcd = selection.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' > 0)*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))')
		
		#---- using QCD noniso directory
		ssiso_n1 = QuickEntries(tn_data          ,selec_qcd_data + '*' + controlregion_1+dataHLT,1.0) # + dataHLT ??
		ssiso_z1 = QuickIntegral(tn_ZJets        ,selec_qcd + '*' + controlregion_1,Rz_data[0])
		ssiso_t1 = QuickIntegral(tn_TTBar        ,selec_qcd + '*' + controlregion_1,Rtt_data[0])
		ssiso_s1 = QuickIntegral(tn_SingleTop    ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_w1 = QuickIntegral(tn_WJets        ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_v1 = QuickIntegral(tn_DiBoson      ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_h1 = QuickIntegral(tn_SMHiggs      ,selec_qcd + '*' + controlregion_1,1.0)
		dataq1_val = fbd[0] * (ssiso_n1[0] - (ssiso_z1[0]+ssiso_t1[0]+ssiso_s1[0]+ssiso_w1[0]+ssiso_v1[0]+ssiso_h1[0]))
		dataq1_err = fbd[0] * math.sqrt(ssiso_n1[1]**2 + ssiso_z1[1]**2 + ssiso_t1[1]**2 + ssiso_s1[1]**2 + ssiso_w1[1]**2 + ssiso_v1[1]**2 + ssiso_h1[1]**2)
		q1 = [dataq1_val,dataq1_err]
		
		ssiso_n2 = QuickEntries(tn_data          ,selec_qcd_data + '*' + controlregion_2+dataHLT,1.0) # + dataHLT ??
		ssiso_z2 = QuickIntegral(tn_ZJets        ,selec_qcd + '*' + controlregion_2,Rz_data[0])
		ssiso_t2 = QuickIntegral(tn_TTBar        ,selec_qcd + '*' + controlregion_2,Rtt_data[0])
		ssiso_s2 = QuickIntegral(tn_SingleTop    ,selec_qcd + '*' + controlregion_2,1.0)
		ssiso_w2 = QuickIntegral(tn_WJets        ,selec_qcd + '*' + controlregion_2,1.0)
		ssiso_v2 = QuickIntegral(tn_DiBoson      ,selec_qcd + '*' + controlregion_2,1.0)
		ssiso_h2 = QuickIntegral(tn_SMHiggs      ,selec_qcd + '*' + controlregion_2,1.0)
		dataq2_val = fbd[0] * (ssiso_n2[0] - (ssiso_z2[0]+ssiso_t2[0]+ssiso_s2[0]+ssiso_w2[0]+ssiso_v2[0]+ssiso_h2[0]))
		dataq2_err = fbd[0] * math.sqrt(ssiso_n2[1]**2 + ssiso_z2[1]**2 + ssiso_t2[1]**2 + ssiso_s2[1]**2 + ssiso_w2[1]**2 + ssiso_v2[1]**2 + ssiso_h2[1]**2)
		q2 = [dataq2_val,dataq2_err]

#		#---- using Normal directory
#		ssiso_n1 = QuickEntries(t_data          ,selec_qcd_data + '*' + controlregion_1+dataHLT,1.0) # + dataHLT ??
#		ssiso_z1 = QuickIntegral(t_ZJets        ,selec_qcd + '*' + controlregion_1,Rz_data[0])
#		ssiso_t1 = QuickIntegral(t_TTBar        ,selec_qcd + '*' + controlregion_1,Rtt_data[0])
#		ssiso_s1 = QuickIntegral(t_SingleTop    ,selec_qcd + '*' + controlregion_1,1.0)
#		ssiso_w1 = QuickIntegral(t_WJets        ,selec_qcd + '*' + controlregion_1,1.0)
#		ssiso_v1 = QuickIntegral(t_DiBoson      ,selec_qcd + '*' + controlregion_1,1.0)
#		ssiso_h1 = QuickIntegral(t_SMHiggs      ,selec_qcd + '*' + controlregion_1,1.0)
#		dataq1_val = fbd[0] * (ssiso_n1[0] - (ssiso_z1[0]+ssiso_t1[0]+ssiso_s1[0]+ssiso_w1[0]+ssiso_v1[0]+ssiso_h1[0]))
#		dataq1_err = fbd[0] * math.sqrt(ssiso_n1[1]**2 + ssiso_z1[1]**2 + ssiso_t1[1]**2 + ssiso_s1[1]**2 + ssiso_w1[1]**2 + ssiso_v1[1]**2 + ssiso_h1[1]**2)
#		q1 = [dataq1_val,dataq1_err]
#		
#		ssiso_n2 = QuickEntries(t_data          ,selec_qcd_data + '*' + controlregion_2+dataHLT,1.0) # + dataHLT ??
#		ssiso_z2 = QuickIntegral(t_ZJets        ,selec_qcd + '*' + controlregion_2,Rz_data[0])
#		ssiso_t2 = QuickIntegral(t_TTBar        ,selec_qcd + '*' + controlregion_2,Rtt_data[0])
#		ssiso_s2 = QuickIntegral(t_SingleTop    ,selec_qcd + '*' + controlregion_2,1.0)
#		ssiso_w2 = QuickIntegral(t_WJets        ,selec_qcd + '*' + controlregion_2,1.0)
#		ssiso_v2 = QuickIntegral(t_DiBoson      ,selec_qcd + '*' + controlregion_2,1.0)
#		ssiso_h2 = QuickIntegral(t_SMHiggs      ,selec_qcd + '*' + controlregion_2,1.0)
#		dataq2_val = fbd[0] * (ssiso_n2[0] - (ssiso_z2[0]+ssiso_t2[0]+ssiso_s2[0]+ssiso_w2[0]+ssiso_v2[0]+ssiso_h2[0]))
#		dataq2_err = fbd[0] * math.sqrt(ssiso_n2[1]**2 + ssiso_z2[1]**2 + ssiso_t2[1]**2 + ssiso_s2[1]**2 + ssiso_w2[1]**2 + ssiso_v2[1]**2 + ssiso_h2[1]**2)
#		q2 = [dataq2_val,dataq2_err]


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

	print 'Muon scale factor integrals:'
	print 'Data:',N1,N2
	print 'Z:',Z1,Z2
	print 'TT:',T1,T2
	print 'Other:',Other1NoH,Other2NoH
	print 'SMHiggs:',H1,H2

	print 'Muon: RZ  = ', zout[-1], zout[0], zout[1]
	print 'Muon: Rtt = ', tout[-1], tout[0], tout[1]
	return [ [ zout[0], zout[1] ] , [ tout[0],tout[1] ] ]

def GetNormalizationScaleFactorsAndFbd( selection, FileDirectory, controlregion_1, controlregion_2, canUseTTDD):
	global analysisChannel
	print 'I am in GetNormalizationScaleFactorsAndFbd()'
	print 'getting '+analysisChannel+' scale factors :'
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_DoubleMuData,selection + '*' + controlregion_1,1.0)
	# print QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	# sys.exit()
	selection_data = selection.split('*(fact')[0]
	if analysisChannel=='muon'     :
		t_data  = t_DoubleMuData
		tn_data = tn_DoubleMuData
		doubleIso         = '((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))'
		invertedDoubleIso = '(((TrkIso_muon1>0.25) + (TrkIso_muon2>0.25))>0)'
	if analysisChannel=='electron' :
		t_data  = t_DoubleEleData
		tn_data = tn_DoubleEleData
		doubleIso         = '(((abs(Eta_ele1)<1.442)*(TrkIso_ele1<0.0695)+(abs(Eta_ele1)>1.56)*(TrkIso_ele1<0.0821))*((abs(Eta_ele2)<1.442)*(TrkIso_ele2<0.0695)+(abs(Eta_ele2)>1.56)*(TrkIso_ele2<0.0821)))'
		invertedDoubleIso = '((((abs(Eta_ele1)<1.442)*(TrkIso_ele1>0.0695)+(abs(Eta_ele1)>1.56)*(TrkIso_ele1>0.0821)) + ((abs(Eta_ele2)<1.442)*(TrkIso_ele2>0.0695)+(abs(Eta_ele2)>1.56)*(TrkIso_ele2>0.0821)))>0)'
	
	N1 = QuickEntries(t_data,selection_data + '*' + controlregion_1+dataHLT,1.0)
	#print selection_data + '*' + controlregion_1+dataHLT
	N2 = QuickEntries(t_data,selection_data + '*' + controlregion_2+dataHLT,1.0)
	
	Z1 = QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBar,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(t_WJets,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)
	H1 = QuickIntegral(t_SMHiggs,selection   + '*' + controlregion_1,1.0)
	
	Z2 = QuickIntegral(t_ZJets,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBar,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(t_WJets,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)
	H2 = QuickIntegral(t_SMHiggs,selection   + '*' + controlregion_2,1.0)
	
	O1 = [ s1[0]+w1[0]+v1[0]+H1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] + H1[1]*H1[1]) ]
	O2 = [ s2[0]+w2[0]+v2[0]+H2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] + H2[1]*H2[1]) ]
	
	w1ent = QuickEntries(t_WJets,selection + '*' + controlregion_1,1.0)
	w2ent = QuickEntries(t_WJets,selection + '*' + controlregion_2,1.0)
	z1ent = QuickEntries(t_ZJets,selection + '*' + controlregion_1,1.0)
	z2ent = QuickEntries(t_ZJets,selection + '*' + controlregion_2,1.0)
	
	if (not useDataDrivenQCD):
		print ' Please set useDataDrivenQCD to True'
		exit()
	else:
		print ' using QCD data-driven when calculating '+analysisChannel+' scale factors'
		selec_qcd_data = selection_data.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' > 0)*'+doubleIso)
		selec_qcd = selection.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' > 0)*'+doubleIso)
		
		#---- using QCD noniso directory
		print ' doing ss iso in region 1 '
		ssiso_n1 = QuickEntries(tn_data          ,selec_qcd_data + '*' + controlregion_1+dataHLT,1.0) # + dataHLT ??
		ssiso_z1 = QuickIntegral(tn_ZJets        ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_t1 = QuickIntegral(tn_TTBar        ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_s1 = QuickIntegral(tn_SingleTop    ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_w1 = QuickIntegral(tn_WJets        ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_v1 = QuickIntegral(tn_DiBoson      ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_h1 = QuickIntegral(tn_SMHiggs      ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_o1 = [ssiso_s1[0]+ssiso_w1[0]+ssiso_v1[0]+ssiso_h1[0], math.sqrt(ssiso_s1[1]**2 + ssiso_w1[1]**2 + ssiso_v1[1]**2 + ssiso_h1[1]**2)]
		#ssiso_q1 = [(ssiso_n1[0] - (ssiso_z1[0]+ssiso_t1[0]+ssiso_o1[0])), math.sqrt(ssiso_n1[1]**2 + ssiso_z1[1]**2 + ssiso_t1[1]**2 + ssiso_o1[1]**2)]
		
		print ' doing ss iso in region 2 '
		ssiso_n2 = QuickEntries(tn_data  ,selec_qcd_data + '*' + controlregion_2+dataHLT,1.0) # + dataHLT ??
		ssiso_z2 = QuickIntegral(tn_ZJets        ,selec_qcd + '*' + controlregion_2,1.0)
		ssiso_t2 = QuickIntegral(tn_TTBar        ,selec_qcd + '*' + controlregion_2,1.0)
		ssiso_s2 = QuickIntegral(tn_SingleTop    ,selec_qcd + '*' + controlregion_2,1.0)
		ssiso_w2 = QuickIntegral(tn_WJets        ,selec_qcd + '*' + controlregion_2,1.0)
		ssiso_v2 = QuickIntegral(tn_DiBoson      ,selec_qcd + '*' + controlregion_2,1.0)
		ssiso_h2 = QuickIntegral(tn_SMHiggs      ,selec_qcd + '*' + controlregion_2,1.0)
		ssiso_o2 = [ssiso_s2[0]+ssiso_w2[0]+ssiso_v2[0]+ssiso_h2[0], math.sqrt(ssiso_s2[1]**2 + ssiso_w2[1]**2 + ssiso_v2[1]**2 + ssiso_h2[1]**2)]
		#ssiso_q2 = [(ssiso_n2[0] - (ssiso_z2[0]+ssiso_t2[0]+ssiso_o2[0])), math.sqrt(ssiso_n2[1]**2 + ssiso_z2[1]**2 + ssiso_t2[1]**2 + ssiso_o2[1]**2)]
		
		#		#---- using Normal directory
		#		ssiso_n1 = QuickEntries(t_data          ,selec_qcd_data + '*' + controlregion_1+dataHLT,1.0) # + dataHLT ??
		#		ssiso_z1 = QuickIntegral(t_ZJets        ,selec_qcd + '*' + controlregion_1,1.0)
		#		ssiso_t1 = QuickIntegral(t_TTBar        ,selec_qcd + '*' + controlregion_1,1.0)
		#		ssiso_s1 = QuickIntegral(t_SingleTop    ,selec_qcd + '*' + controlregion_1,1.0)
		#		ssiso_w1 = QuickIntegral(t_WJets        ,selec_qcd + '*' + controlregion_1,1.0)
		#		ssiso_v1 = QuickIntegral(t_DiBoson      ,selec_qcd + '*' + controlregion_1,1.0)
		#		ssiso_h1 = QuickIntegral(t_SMHiggs      ,selec_qcd + '*' + controlregion_1,1.0)
		#
		#		ssiso_n2 = QuickEntries(t_data          ,selec_qcd_data + '*' + controlregion_2+dataHLT,1.0) # + dataHLT ??
		#		ssiso_z2 = QuickIntegral(t_ZJets        ,selec_qcd + '*' + controlregion_2,1.0)
		#		ssiso_t2 = QuickIntegral(t_TTBar        ,selec_qcd + '*' + controlregion_2,1.0)
		#		ssiso_s2 = QuickIntegral(t_SingleTop    ,selec_qcd + '*' + controlregion_2,1.0)
		#		ssiso_w2 = QuickIntegral(t_WJets        ,selec_qcd + '*' + controlregion_2,1.0)
		#		ssiso_v2 = QuickIntegral(t_DiBoson      ,selec_qcd + '*' + controlregion_2,1.0)
		#		ssiso_h2 = QuickIntegral(t_SMHiggs      ,selec_qcd + '*' + controlregion_2,1.0)
		
		ssiso_w1ent = QuickEntries(tn_WJets        ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_w2ent = QuickEntries(tn_WJets        ,selec_qcd + '*' + controlregion_2,1.0)
		ssiso_z1ent = QuickEntries(tn_ZJets        ,selec_qcd + '*' + controlregion_1,1.0)
		ssiso_z2ent = QuickEntries(tn_ZJets        ,selec_qcd + '*' + controlregion_2,1.0)
		
		print 'ssiso_cr_n:', ssiso_n1, ssiso_n2
		print 'ssiso_cr_z:', ssiso_z1, ssiso_z2
		print 'ssiso_cr_t:', ssiso_t1, ssiso_t2
		print 'ssiso_cr_o:', ssiso_o1, ssiso_o2
		print '    ssiso_cr_w:', ssiso_w1, ssiso_w2
		print '   ssiso_cr_vv:', ssiso_v1, ssiso_v2
		print '   ssiso_cr_st:', ssiso_s1, ssiso_s2
		print '  ssiso_cr_smh:', ssiso_h1, ssiso_h2
		#print 'ssiso_cr_q:', ssiso_q1, ssiso_q2
		print 'Wjets entries in ss iso CR1 CR2 :', ssiso_w1ent, ssiso_w2ent
		print 'Zjets entries in ss iso CR1 CR2 :', ssiso_z1ent, ssiso_z2ent
		
		#----- invert isolation in nominal region for f_bd
		print ' doing invert iso in nominal region for f_bd '
		selec_ssinv_data = selection_data.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' > 0)*'+invertedDoubleIso)
		selec_ssinv      =      selection.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' > 0)*'+invertedDoubleIso)
		selec_opinv_data = selection_data.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' < 0)*'+invertedDoubleIso)
		selec_opinv      =      selection.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' < 0)*'+invertedDoubleIso)
		
		data_ss_inv = QuickEntries(tn_data         ,selec_ssinv_data+dataHLT, 1.0)
		zjet_ss_inv = QuickIntegral(tn_ZJets       ,selec_ssinv, 1.0)
		tt_ss_inv   = QuickIntegral(tn_TTBar       ,selec_ssinv, 1.0)
		wjet_ss_inv = QuickIntegral(tn_WJets       ,selec_ssinv, 1.0)
		stop_ss_inv = QuickIntegral(tn_SingleTop   ,selec_ssinv, 1.0)
		vv_ss_inv   = QuickIntegral(tn_DiBoson     ,selec_ssinv, 1.0)
		smh_ss_inv  = QuickIntegral(tn_SMHiggs     ,selec_ssinv, 1.0)
		other_ss_inv = [wjet_ss_inv[0] + stop_ss_inv[0] + vv_ss_inv[0] + smh_ss_inv[0], math.sqrt(wjet_ss_inv[1]**2 + stop_ss_inv[1]**2 + vv_ss_inv[1]**2 + smh_ss_inv[1]**2)]
		
		data_op_inv = QuickEntries(tn_data         ,selec_opinv_data+dataHLT,1.0)
		zjet_op_inv = QuickIntegral(tn_ZJets       ,selec_opinv, 1.0)
		tt_op_inv   = QuickIntegral(tn_TTBar       ,selec_opinv, 1.0)
		wjet_op_inv = QuickIntegral(tn_WJets       ,selec_opinv, 1.0)
		stop_op_inv = QuickIntegral(tn_SingleTop   ,selec_opinv, 1.0)
		vv_op_inv   = QuickIntegral(tn_DiBoson     ,selec_opinv, 1.0)
		smh_op_inv  = QuickIntegral(tn_SMHiggs     ,selec_opinv, 1.0)
		other_op_inv = [wjet_op_inv[0] + stop_op_inv[0] + vv_op_inv[0] + smh_op_inv[0], math.sqrt(wjet_op_inv[1]**2 + stop_op_inv[1]**2 + vv_op_inv[1]**2 + smh_op_inv[1]**2)]
		
		wjet_ss_inv_ent = QuickEntries(tn_WJets       ,selec_ssinv, 1.0)
		wjet_op_inv_ent = QuickEntries(tn_WJets       ,selec_opinv, 1.0)
		zjet_ss_inv_ent = QuickEntries(tn_ZJets       ,selec_ssinv, 1.0)
		zjet_op_inv_ent = QuickEntries(tn_ZJets       ,selec_opinv, 1.0)
		
		print 'data_inv : ss, os:', data_ss_inv , data_op_inv
		print 'zjet_inv : ss, os:', zjet_ss_inv , zjet_op_inv
		print 'tt_inv   : ss, os:', tt_ss_inv   , tt_op_inv
		print 'wjet_inv : ss, os:', wjet_ss_inv , wjet_op_inv
		print 'stop_inv : ss, os:', stop_ss_inv , stop_op_inv
		print 'vv_inv   : ss, os:', vv_ss_inv   , vv_op_inv
		print 'smh_inv  : ss, os:', smh_ss_inv  , smh_op_inv
		print 'other_inv: ss, os:', other_ss_inv, other_op_inv
		print 'Wjets entries in the inv iso: ss, os :', wjet_ss_inv_ent, wjet_op_inv_ent
		print 'Zjets entries in the inv iso: ss, os :', zjet_ss_inv_ent, zjet_op_inv_ent
		
		#vals = GetScaleFactorsAndFbd(N1[0],N2[0],Z1[0],Z2[0],T1[0],T2[0],O1[0],O2[0],ssiso_n1[0],ssiso_n2[0],ssiso_z1[0],ssiso_z2[0],ssiso_t1[0],ssiso_t2[0],ssiso_o1[0],ssiso_o2[0],data_op_inv[0],zjet_op_inv[0],tt_op_inv[0],other_op_inv[0],data_ss_inv[0],zjet_ss_inv[0],tt_ss_inv[0],other_ss_inv[0])
		#print ' vals ', vals
		
		print ' Getting avg and uncer of Rz Rt Fbd '
		zvals = []
		tvals = []
		fbdvals = []
		for x in range(1000):#fixme was 10000
			variation = (GetScaleFactorsAndFbd(RR(N1),RR(N2),RR(Z1),RR(Z2),RR(T1),RR(T2),RR(O1),RR(O2),RR(ssiso_n1),RR(ssiso_n2),RR(ssiso_z1),RR(ssiso_z2),RR(ssiso_t1),RR(ssiso_t2),RR(ssiso_o1),RR(ssiso_o2),RR(data_op_inv),RR(zjet_op_inv),RR(tt_op_inv),RR(other_op_inv),RR(data_ss_inv),RR(zjet_ss_inv),RR(tt_ss_inv),RR(other_ss_inv)))
			zvals.append(variation[0])
			tvals.append(variation[1])
			fbdvals.append(variation[2])
		
		zout   = GetStats(zvals)
		tout   = GetStats(tvals)
		fbdout = GetStats(fbdvals)
#		zout = vals[0]
#		tout = vals[1]
#		fbdout = vals[2]
	
#	# ttbar force unity
#	if useDataDrivenTTbar and canUseTTDD:
#		print 'Using Data-driven TTbar'
#		tout = [1.0,0.067,'1.000 +- 0.067'] #fixme todo need to understand why 0.067
#	# Force to pre-calculated values to speed things up
#	#zout = [3.251,0.059,'3.251 +- 0.059']
#	#tout = [2.19,0.037,'2.19  +- 0.037']
#	#print 'Using pre-calculated values, rerun if you add more data!'
	
	ssiso_q1 = [(ssiso_n1[0] - (ssiso_z1[0]*zout[0] + ssiso_t1[0]*tout[0] + ssiso_o1[0])), math.sqrt(ssiso_n1[1]**2 + (ssiso_z1[1]*zout[0])**2 + (ssiso_t1[1]*tout[0])**2 + ssiso_o1[1]**2)]
	dataq1_val = fbdout[0] * ssiso_q1[0]
	dataq1_err = fbdout[0] * ssiso_q1[1]
	q1 = [dataq1_val,dataq1_err]
	
	ssiso_q2 = [(ssiso_n2[0] - (ssiso_z2[0]*zout[0] + ssiso_t2[0]*tout[0] + ssiso_o2[0])), math.sqrt(ssiso_n2[1]**2 + (ssiso_z2[1]*zout[0])**2 + (ssiso_t2[1]*tout[0])**2 + ssiso_o2[1]**2)]
	dataq2_val = fbdout[0] * ssiso_q2[0]
	dataq2_err = fbdout[0] * ssiso_q2[1]
	q2 = [dataq2_val,dataq2_err]
	
	print 'MuMu scale factor integrals: CR1, CR2 '
	print 'Data:',N1,N2
	print 'Z:',Z1,Z2
	print 'TT:',T1,T2
	print 'Other:',O1,O2
	print '       W:',w1,w2
	print '      VV:',v1,v2
	print '      ST:',s1,s2
	print '     SMH:',H1,H2
	print 'QCD:',q1,q2
	print 'Wjets entries in CR1 CR2 :', w1ent, w2ent
	print 'Zjets entries in CR1 CR2 :', z1ent, z2ent
	
	print '\n'
	print 'MuMu: RZ  = ', zout[-1], zout[0], zout[1]
	print 'MuMu: Rtt = ', tout[-1], tout[0], tout[1]
	print 'MuMu: fbd = ', fbdout[-1], fbdout[0], fbdout[1]
	return [ [ zout[0], zout[1] ] , [ tout[0], tout[1] ], [ fbdout[0], fbdout[1] ] ]

def GetNormalizationScaleFactorsMod( selection, FileDirectory, controlregion_1, controlregion_2,samp):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_DoubleMuData,selection + '*' + controlregion_1,1.0)
	# print QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	# sys.exit()

	ScaleUpSelection = selection+'*scaleWeight_Up'
	ScaleDownSelection = selection+'*scaleWeight_Down'#fixme todo update for matching
	MatchUpSelection = selection+'*scaleWeight_Up'
	MatchDownSelection = selection+'*scaleWeight_Down'#fixme todo update for matching
	selectionMod = selection

	if 'ScaleUp' in samp:
		#t_Z = t_ZJetsScaleUp
		#t_T = t_TTJetsScaleDown
		t_Z = t_ZJets
		t_T = t_TTBar	
		selectionMod=ScaleUpSelection

	elif 'ScaleDown' in samp:
		#t_Z = t_ZJetsScaleDown
		#t_T = t_TTJetsScaleDown
		t_Z = t_ZJets
		t_T = t_TTBar	
		selectionMod=ScaleDownSelection

	elif 'MatchUp' in samp:
		#t_Z = t_ZJetsMatchUp
		#t_T = t_TTJetsMatchDown
		t_Z = t_ZJets
		t_T = t_TTBar	
		selectionMod=ScaleUpSelection#fixme todo update for matching

	elif 'MatchDown' in samp:
		#t_Z = t_ZJetsMatchDown
		#t_T = t_TTJetsMatchDown
		t_Z = t_ZJets
		t_T = t_TTBar	
		selectionMod=ScaleDownSelection#fixme todo update for matching
	else:
		t_Z = t_ZJets
		t_T = t_TTBar		

	N1 = QuickEntries(t_DoubleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_DoubleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

	Z1 = QuickIntegral(t_Z,selectionMod + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBar,selectionMod + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(t_WJets,selectionMod + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)

	Z2 = QuickIntegral(t_Z,selectionMod + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBar,selectionMod + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(t_WJets,selectionMod + '*' + controlregion_2,1.0)
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

	print 'Muon: RZ  = ', zout[-1]
	print 'Muon: Rtt = ', tout[-1]
	return [ [ zout[0], zout[1] ] , [ tout[0],tout[1] ] ]



def GetEMuScaleFactors( selection, FileDirectory):

	print '\n\n--------------\n--------------\nChecking TTBar E-Mu sample against E_Mu MC with selection:'
	print selection 
	N1 = QuickEntries(te_DoubleMuData,selection  + dataHLT,1.0)

	Z1 = QuickIntegral(te_ZJets,selection ,1.0)
	T1 = QuickIntegral(te_TTBar,selection ,1.0)
	s1 = QuickIntegral(te_SingleTop,selection ,1.0)
	w1 = QuickIntegral(te_WJets,selection ,1.0)
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

	print 'Muon: Rtt = ', SF


	print 'Now calculating R_Muon,emu, the ratio of mu,mu to e,mu events in ttbar MC. '
	print 'Should be near 0.5'
	#print selection,'\n\n'
	#print selection.replace(singleMuonHLTEMU,singleMuonHLT).replace(MuIdScaleEMU,MuIdScale).replace(MuIsoScaleEMU,MuIsoScale),'\n\n'
	T2 = QuickIntegral(t_TTBar,selection.replace(singleMuonHLTEMU,singleMuonHLT), 1.0)
	#T2 = QuickIntegral(t_TTBar,selection.replace(singleMuonHLTEMU,singleMuonHLT).replace(MuIdScaleEMU,MuIdScale).replace(MuIsoScaleEMU,MuIsoScale) ,1.0)

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
		t_W = t_WJets
		t_T = t_TTBar
		selectionMod=ScaleUpSelection

	elif 'ScaleDown' in samp:
		#t_W = t_WJetsScaleDown
		#t_T = t_TTJetsScaleDown
		t_W = t_WJets
		t_T = t_TTBar
		selectionMod=ScaleDownSelection

	elif 'MatchUp' in samp:
		#t_W = t_WJetsMatchUp
		#t_T = t_TTJetsMatchDown
		t_W = t_WJets
		t_T = t_TTBar
		selectionMod=ScaleUpSelection#fixme todo update for matching

	elif 'MatchDown' in samp:
		#t_W = t_WJetsMatchDown
		#t_T = t_TTJetsMatchDown
		t_W = t_WJets
		t_T = t_TTBar
		selectionMod=ScaleDownSelection#fixme todo update for matching

	else:
		t_W = t_WJets
		t_T = t_TTBar		

	N1 = QuickEntries(t_DoubleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_DoubleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

	W1 = QuickIntegral(t_W,selectionMod + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_T,selectionMod + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	z1 = QuickIntegral(t_ZJets,selectionMod + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)

	W2 = QuickIntegral(t_W,selectionMod + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_T,selectionMod + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	z2 = QuickIntegral(t_ZJets,selectionMod + '*' + controlregion_2,1.0)
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

	W1 = QuickIntegral(t_WJets,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBar,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	z1 = QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,  selection + '*' + controlregion_1,1.0)

	W2 = QuickIntegral(t_WJets,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBar,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	z2 = QuickIntegral(t_ZJets,selection + '*' + controlregion_2,1.0)
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
		selectionPresel = '('+weight+'*'+preselection+')'
		selectionFinal  = '('+weight+'*'+preselection+'*'+fsel+')'
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
	global ell
	global latexEll
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	print '\n AH: I am in MakeBasicPlot(): selection is \n'
	print selection, '\n'
	
	# Create Canvas
	yaxismin = .13333
	perc = totunc_Muon[0]
	betamarker = '#beta = '
	isDisplaced=False
	#if 'cosThetaStar' in recovariable: doLog=False
	#else: doLog=True
	doLog=True
	syslist=[0]
	if channel == 'uujj' or channel == 'HHres':
		syslist = totunc_Muon	
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
		#pad1 = TPad( 'pad1', 'pad1', 0.0, 0.4, 1.0, 1.0 )#divide canvas into pads
		#pad2 = TPad( 'pad2', 'pad2', 0.0, 0.26, 1.0, 0.4 )
		#pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.26 )
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.3, 1.0, 1.0 )#divide canvas into pads
		pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.3 )
		pad1.Draw()
		#pad2.Draw()
		pad3.Draw()
		pad1.SetBottomMargin(0.0)		
		#pad2.SetTopMargin(0.0)
		pad3.SetTopMargin(0.0)
		#pad2.SetBottomMargin(0.0)
		pad3.SetBottomMargin(0.43)
	else:
		# if 'final' not in tagname:
		c1 = TCanvas("c1","",800,550)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		#perc = 5.0
		#for m in range(len(pdf_MASS)):
		#	if str(pdf_MASS[m]) in str(plotmass):
		#		perc = syslist[m]


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
		"""
		print 'cat '+cutlog+' | grep '+channel+str(plotmass)
 		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)).readlines())[0]).replace('\n','')
		print 'found'
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+selection+fsel+')'
		print 'parsed'
		"""
		selection = selection.replace(bTagPresel,bTagFinalsel)
		weight = weight.replace(bTagPreselSF,bTagFinalSF)
		print '\n', selection , '\n'

	##############################################################################
	#######      Top Left Plot - Normal Stacked Distributions              #######
	##############################################################################
	c1.cd(1)
	# print 'Projecting trees...  ',

	tt_sel_weight = selection+'*('+str(ttscale)+')*'+weight
	qcd_sel_weight= selection+'*'+weight

	print 'Choosing sample...',

	t_W = t_WJets
	t_Z = t_ZJets
	t_T = t_TTBar
	if analysisChannel=='muon'     :
		t_data = t_DoubleMuData
	if analysisChannel=='electron' :
		t_data = t_DoubleEleData
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
		t_W = t_WJets
		t_Z = t_ZJets
		print 'USING STANDARD W'
		if 'TTBarDataDriven' not in tagname:
			t_T = t_TTBar
			print 'Using Decay-binned ttbar MC.'
		else:
			t_T = te_DoubleMuData
			tt_sel_weight = selection + dataHLT + dataHLTEMUADJ
			print 'Using emu data for ttbar est.'

		# t_T = t_TTPowheg
		
		if (useDataDrivenQCD or 'QCDDataDriven' in tagname):
#			#--- using qcd directory
#			t_estQCD = tn_DoubleMuData
#			qcd_sel_weight = selection.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' > 0)*((TrkIso_muon1<0.25)*(TrkIso_muon2<0.25))'+dataHLT) # + dataHLT ??
			#--- using normal directory with ss requirement
			if analysisChannel=='muon'     :
				t_estQCD = t_DoubleMuData
			if analysisChannel=='electron' :
				t_estQCD = t_DoubleEleData
			qcd_sel_weight = selection.replace('*('+charge1+'*'+charge2+' < 0)', '*('+charge1+'*'+charge2+' > 0)'+dataHLT)
			print 'Using data-driven for QCD est.'
		else:
			if analysisChannel=='muon'     :
				t_estQCD = t_QCDMu
			if analysisChannel=='electron' :
				t_estQCD = t_QCDEle
			print 'Using QCD MC.'

	print 'Doing Projections'
	print '\n AH: I am in MakeBasicPlot(): selection is ',selection , '\n'
	print '\n AH: I am in MakeBasicPlot(): zscale is ', zscale, '\n'
	print '\n AH: I am in MakeBasicPlot(): wscale is ', wscale, '\n'
	print '\n AH: I am in MakeBasicPlot(): ttscale is ', ttscale, '\n'
	print '\n AH: I am in MakeBasicPlot(): dataHLT is ', dataHLT, '\n'
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',t_W,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',t_data,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',t_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',t_Z,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	print 'Doing ttbar:'
	#print selection+'*('+str(ttscale)+')*'+weight
	print '\n AH: I am in MakeBasicPlot(): tt_sel_weight is ', tt_sel_weight, '\n'
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',t_T,recovariable,presentationbinning,tt_sel_weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',t_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)
	print 'Doing QCD:'
	print '\n AH: I am in MakeBasicPlot(): qcd_sel_weight is ', qcd_sel_weight, '\n'
	hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD',t_estQCD,recovariable,presentationbinning,qcd_sel_weight,QCDStackStyle,Label)
	hs_rec_SMHiggs=CreateHisto('hs_rec_SMHiggs','SM Higgs',t_SMHiggs,recovariable,presentationbinning,selection+'*'+weight,SMHiggsStackStyle,Label)


	if 'TTBarDataDriven' in tagname:

		hs_emu_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',te_WJets,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+NormalWeightEMuNoHLT,WStackStyle,Label)
		hs_emu_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,DiBosonStackStyle,Label)
		hs_emu_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',te_ZJets,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+NormalWeightEMuNoHLT,ZStackStyle,Label)
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

	if (useDataDrivenQCD or 'QCDDataDriven' in tagname):
		#--- using qcd directory
#		hs_ss_rec_WJets=CreateHisto('hs_ss_rec_WJets','W+Jets'            ,tn_WJets   ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight+'*('+str(wscale)+')' ,WStackStyle,Label)
#		hs_ss_rec_DiBoson=CreateHisto('hs_ss_rec_DiBoson','DiBoson'       ,tn_DiBoson      ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight                      ,DiBosonStackStyle,Label)
#		hs_ss_rec_ZJets=CreateHisto('hs_ss_rec_ZJets','Z+Jets'            ,tn_ZJets   ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight+'*('+str(zscale)+')' ,ZStackStyle,Label)
#		hs_ss_rec_TTBar=CreateHisto('hs_ss_rec_TTBar','TTBar'             ,tn_TTBar ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight+'*('+str(ttscale)+')',TTStackStyle,Label)
#		hs_ss_rec_SingleTop=CreateHisto('hs_ss_rec_SingleTop','SingleTop' ,tn_SingleTop    ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight                      ,StopStackStyle,Label)
#		hs_ss_rec_SMHiggs=CreateHisto('hs_ss_rec_SMHiggs','SMHiggs'       ,tn_SMHiggs      ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight                      ,SMHiggsStackStyle,Label)

		#--- using normal directory with ss requirement
		hs_ss_rec_WJets=CreateHisto('hs_ss_rec_WJets','W+Jets'            ,t_W         ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight+'*('+str(wscale)+')' ,WStackStyle,Label)
		hs_ss_rec_DiBoson=CreateHisto('hs_ss_rec_DiBoson','DiBoson'       ,t_DiBoson   ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight                      ,DiBosonStackStyle,Label)
		hs_ss_rec_ZJets=CreateHisto('hs_ss_rec_ZJets','Z+Jets'            ,t_Z         ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight+'*('+str(zscale)+')' ,ZStackStyle,Label)
		hs_ss_rec_TTBar=CreateHisto('hs_ss_rec_TTBar','TTBar'             ,t_T         ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight+'*('+str(ttscale)+')',TTStackStyle,Label)
		hs_ss_rec_SingleTop=CreateHisto('hs_ss_rec_SingleTop','SingleTop' ,t_SingleTop ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight                      ,StopStackStyle,Label)
		hs_ss_rec_SMHiggs=CreateHisto('hs_ss_rec_SMHiggs','SMHiggs'       ,t_SMHiggs   ,recovariable,presentationbinning,qcd_sel_weight+'*'+weight                      ,SMHiggsStackStyle,Label)
		
		
		print ' Looking at ss iso : Integral : Entries'
		print 'W:   ', hs_ss_rec_WJets.Integral(), hs_ss_rec_WJets.GetEntries()
		print 'VV:  ', hs_ss_rec_DiBoson.Integral(), hs_ss_rec_DiBoson.GetEntries()
		print 'Z:   ', hs_ss_rec_ZJets.Integral(), hs_ss_rec_ZJets.GetEntries()
		print 'TT:  ', hs_ss_rec_TTBar.Integral(), hs_ss_rec_TTBar.GetEntries()
		print 'ST:  ', hs_ss_rec_SingleTop.Integral(), hs_ss_rec_SingleTop.GetEntries()
		print 'SM H:', hs_ss_rec_SMHiggs.Integral(), hs_ss_rec_SMHiggs.GetEntries()
		#print 'Total Background:',totBg,'+-',totErr
		print 'Data            :',hs_rec_QCD.Integral(), hs_rec_QCD.GetEntries()

		
		hs_ss_rec_WJets.Scale(-1.0)
		hs_ss_rec_DiBoson.Scale(-1.0)
		hs_ss_rec_ZJets.Scale(-1.0)
		hs_ss_rec_TTBar.Scale(-1.0)
		hs_ss_rec_SingleTop.Scale(-1.0)
		hs_ss_rec_SMHiggs.Scale(-1.0)
		hs_rec_QCD.Add(hs_ss_rec_WJets)
		hs_rec_QCD.Add(hs_ss_rec_DiBoson)
		hs_rec_QCD.Add(hs_ss_rec_ZJets)
		hs_rec_QCD.Add(hs_ss_rec_TTBar)
		hs_rec_QCD.Add(hs_ss_rec_SingleTop)
		hs_rec_QCD.Add(hs_ss_rec_SMHiggs)
		#SetNegBinZero(hs_rec_QCD)
		for k in range(hs_rec_QCD.GetNbinsX()):
			if (hs_rec_QCD.GetBinContent(k+1) <= 0):
				hs_rec_QCD.SetBinContent(k+1, 0.)
				hs_rec_QCD.SetBinError(k+1, 0.)
		hs_rec_QCD.Scale(fbd[0])



	sig1name = ''
	sig2name = ''

	if channel == ell+ell+'jj' or 'HH' in channel:
		sig1name = 'M_{R}=300 (1 pb)'#+betamarker
		sig2name = 'M_{R}=900 (1 pb)'#+betamarker
		#sig1name = 'M_{R}=300 x 1000'#+betamarker # AH:
		#sig2name = 'M_{R}=900 x 1000'#+betamarker # AH:
		#sig2name = 'LQ, M = 950 GeV, '+betamarker
		if 'final' not in tagname:
			if 'bdt' not in recovariable:
				hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_HHres300,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
				hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_HHres900,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
			else:
				exec ("_stree = t_HHres"+str(plotmass))
				sig1name = 'M_{R} = '+str(plotmass)+' GeV (1 pb)'
				sig2name = 'M_{R} = 900 GeV (1 pb)'
				hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
				hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_HHres900,'bdt_discrim_M900',presentationbinning,selection+'*'+weight,SignalStyle2,Label)
			print 'signal1,',sig1name,':',hs_rec_Signal.Integral()
			print 'signal2,',sig2name,':',hs_rec_Signal2.Integral()
			hs_rec_Signal.Scale(1000.)
			hs_rec_Signal2.Scale(1000.)
		if 'final' in tagname:
			#exec ("_stree = t_LQ"+channel+str(plotmass))
			exec ("_stree = t_HHres"+str(plotmass))
			# AH: hs_rec_Signal=CreateHisto('hs_rec_Signal','M_{R} = '+str(plotmass)+' GeV, '+betamarker,_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal=CreateHisto('hs_rec_Signal','M_{R} = '+str(plotmass)+' GeV',_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			print 'signal1,',sig1name,':',hs_rec_Signal.Integral()
			# ------- AH: ---------------------------------
			hs_rec_Signal.Scale(1000.) # AH I have to scale it after writing histogram to files

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

		print 'W:   ',wInt, hs_rec_WJets.Integral(), hs_rec_WJets.GetEntries()
		print 'Z:   ',zInt, hs_rec_ZJets.Integral(), hs_rec_ZJets.GetEntries()
		print 'VV:  ',vvInt, hs_rec_DiBoson.Integral(), hs_rec_DiBoson.GetEntries()
		print 'TT:  ',ttInt, hs_rec_TTBar.Integral(), hs_rec_TTBar.GetEntries()
		print 'ST:  ',stInt, hs_rec_SingleTop.Integral(), hs_rec_SingleTop.GetEntries()
		print 'QCD: ',qcdInt, hs_rec_QCD.Integral(), hs_rec_QCD.GetEntries()#,'NOT USED'#hs_rec_SingleTop.Integral()
		print 'SM H:',SMHInt, hs_rec_SMHiggs.Integral(), hs_rec_SMHiggs.GetEntries()
		print 'Total Background:',totBg,'+-',totErr
		print 'Data            :',hs_rec_Data.Integral(), hs_rec_Data.GetEntries()

		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_SMHiggs,hs_rec_DiBoson,hs_rec_QCD,hs_rec_ZJets,hs_rec_TTBar]

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
		if 'bdt' not in recovariable:
			hs_rec_Signal2.Draw("HISTSAME")
 	if 'PAS' in tagname and 'final' in tagname:
		# sysTop.Draw("F")
		hs_bgband.Draw("E2SAME")
	#adding syst band
	hs_bgband.Draw("E2SAME")
	if 'final' in tagname and isDisplaced:
		hs_rec_Signal2.Draw("HISTSAME")
		hs_rec_Signal3.Draw("HISTSAME")
		hs_rec_Signal4.Draw("HISTSAME")
	#setZeroBinErrors(hs_rec_Data,MCStack)
	#hs_rec_Data.Draw("E0PSAME")
	blinded=False
	#fixme this blinds the BDTs above 0.15
	if 'bdt' in recovariable: 
		blind(hs_rec_Data,1)
		#blinded=True
	hs_rec_Data_tgraph = TGraphAsymmErrors(hs_rec_Data)
	if 'final' not in tagname:
		setZeroBinErrors_tgraph(hs_rec_Data,hs_rec_Data_tgraph,MCStack,hs_rec_Signal,hs_rec_Signal2,blinded)
	else:
	       	setZeroBinErrors_tgraph(hs_rec_Data,hs_rec_Data_tgraph,MCStack,hs_rec_Signal,hs_rec_Signal,blinded)

	hs_rec_Data_tgraph.Draw("ZE0PSAME")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	if 'final' not in tagname:
		leg = TLegend(0.52,0.475,0.98,0.89,"","brNDC");	
	else: 
		leg = TLegend(0.55,0.55,0.91,0.9,"","brNDC");	
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
	if channel==ell+ell+'jj' or 'HH' in channel:
		leg.AddEntry(hs_rec_ZJets,'Z/^{}#gamma* + jets')
	if channel=='uvjj':
		leg.AddEntry(hs_rec_WJets,'W + jets')
	leg.AddEntry(hs_rec_QCD,'QCD')
	leg.AddEntry(hs_rec_DiBoson,'Other background')
	leg.AddEntry(hs_rec_SMHiggs,'SM Higgs')

	if 'final' not in tagname:
		#leg.AddEntry("", "", "");
		leg.AddEntry("", "gg#rightarrow R#rightarrow HH#rightarrow bbZZ", "");
		leg.AddEntry(hs_rec_Signal,sig1name,"l")
		if 'bdt' not in recovariable:
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
			#leg.AddEntry(hs_rec_Signal,'LQ, M = '+str(plotmass)+' GeV, '+betamarker,"l")
			#leg.AddEntry(hs_rec_Signal,'M_{R} = '+str(plotmass)+' GeV',"l") # AH:
			leg.AddEntry(hs_rec_Signal,'M_{R} = '+str(plotmass)+' GeV (1 pb)',"l") # AH:
	leg.AddEntry(hs_bgband,'Unc. (stat + syst)')

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
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                35.9 fb^{-1} (13 TeV)")
		#l1.DrawLatex(0.64,0.94,"5 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	else:
		#l1.DrawLatex(0.18,0.94,"                          "+sqrts+", 225.57 pb^{-1}")
		l1.DrawLatex(0.12,0.94,"#it{Preliminary}                             35.9 fb^{-1} (13 TeV)")
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

		pad3.cd()
		# pad2.SetLogy()
		pad3.SetGrid()

		RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_data,recovariable,presentationbinning,'0',DataRecoStyle,Label)

		RatHistDen.Sumw2()
		RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_data,recovariable,presentationbinning,'0',DataRecoStyle,Label)
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
		#RatHistNum.GetXaxis().SetTitle('');
		RatHistNum.GetYaxis().SetTitle('Data/MC');
		RatHistNum.GetYaxis().SetNdivisions(308,True)

		RatHistNum.GetXaxis().SetTitleSize(0.12);
		RatHistNum.GetYaxis().SetTitleSize(.12);
		RatHistNum.GetXaxis().CenterTitle();
		RatHistNum.GetYaxis().CenterTitle();		
		RatHistNum.GetXaxis().SetTitleOffset(1.);
		RatHistNum.GetYaxis().SetTitleOffset(.45);
		RatHistNum.GetYaxis().SetLabelSize(.1);
		RatHistNum.GetXaxis().SetLabelSize(.09);

		if 'bdt' in recovariable: blind(RatHistNum,2)#fixme this is to blind data for BDTs
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

		#fixme syst errors for presel
		hs_bgbandRat = hs_bgband.Clone()
		for c in range(hs_bgbandRat.GetNbinsX()+1):
			if hs_bgbandRat.GetBinContent(c)>0:
				newErr = hs_bgbandRat.GetBinError(c)/hs_bgbandRat.GetBinContent(c)
			else : newErr = hs_bgbandRat.GetBinError(c)
			hs_bgbandRat.SetBinContent(c,1.0)
			hs_bgbandRat.SetBinError(c,newErr)
		hs_bgbandRat.Draw("E2SAMES")

		"""
		pad3.cd()
		# pad2.SetLogy()
		pad3.SetGrid()

		chiplot =CreateHisto('chiplot','chiplot',t_data,recovariable,presentationbinning,'0',DataRecoStyle,Label)
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

		if blinded :blind(chiplot)
		chiplot.Draw('EP')
		zero=TLine(RatHistNum.GetXaxis().GetXmin(), 0.0 , RatHistNum.GetXaxis().GetXmax(),0.0)
		plus2=TLine(RatHistNum.GetXaxis().GetXmin(), 2.0 , RatHistNum.GetXaxis().GetXmax(),2.0)
		minus2=TLine(RatHistNum.GetXaxis().GetXmin(), -2.0 , RatHistNum.GetXaxis().GetXmax(),-2.0)
		plus2.SetLineColor(2)
		minus2.SetLineColor(2)

		plus2.Draw("SAME")
		minus2.Draw("SAME")
		zero.Draw("SAME")	
		"""


	if 'PAS' in tagname and 'final' in tagname and False:

		pad3.cd()
		pad3.SetLogy()
		pad3.SetGrid()

		RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_data,recovariable,presentationbinning,'0',DataRecoStyle,Label)

		RatHistDen.Sumw2()
		RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_data,recovariable,presentationbinning,'0',DataRecoStyle,Label)
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
	
	if 'sqrt(abs(2*Pt_jet1' in recovariable : recovariable = 'M_jj'
	if '(1-(1-(CMVA_bjet1>-0.5884)*Hjet1BsfLoose)*(1-(CMVA_bjet2>-0.5884)*Hjet2BsfLoose)*(1-(CMVA_Zjet1>-0.5884)*Zjet1BsfLoose)*(1-(CMVA_Zjet2>-0.5884)*Zjet2BsfLoose))' in recovariable : recovariable = 'BTagSF'

	recovariable = recovariable.replace('/','_DIV_')
	#recovariable = recovariable.replace('*','_TIM_')
	recovariable = recovariable.replace('(','_')
	recovariable = recovariable.replace(')','_')
	#recovariable = recovariable.replace('-','_MIN_')
	#recovariable = recovariable.replace('+','_PL_')
	#recovariable = recovariable.replace('>','_GT_')

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
		syslist = totunc_Muon	
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

	t_W = t_WJets
	t_Z = t_ZJets
	t_T = t_TTBar
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
		t_W = t_WJets
		t_Z = t_ZJets
		print 'USING STANDARD W'
		if 'TTBarDataDriven' not in tagname:
			t_T = t_TTBar
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

		hs_emu_rec_WJets=CreateHisto2D('hs_rec_WJets','W+Jets',te_WJets,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*('+str(wscale)+')*'+NormalWeightEMuNoHLT,WStackStyle,Label)
		hs_emu_rec_DiBoson=CreateHisto2D('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*'+NormalWeightEMuNoHLT,DiBosonStackStyle,Label)
		hs_emu_rec_ZJets=CreateHisto2D('hs_rec_ZJets','Z+Jets',te_ZJets,recovariableX,recovariableY,presentationbinningX,presentationbinningY,selection+'*('+str(zscale)+')*'+NormalWeightEMuNoHLT,ZStackStyle,Label)
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

	if channel == ell+ell+'jj':
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
		l1.DrawLatex(0.12,0.93,"#it{Preliminary}                              35.9 fb^{-1} (13 TeV)")
		#l1.DrawLatex(0.64,0.94,"5 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.86,"CMS")
	else:
		#l1.DrawLatex(0.18,0.94,"                          "+sqrts+", 225.57 pb^{-1}")
		l1.DrawLatex(0.1,0.93,"#it{Preliminary}                          35.9 fb^{-1} (13 TeV)")
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
	# if tagname == ell+ell+'jj':
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
	SMHiggsStackStyle=[3008,20,.00001,1,800]

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
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',tn_WJets,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	#hs_rec_Data=CreateHisto('hs_rec_Data','Data',tn_DoubleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label) # AH: why do we put HLT here
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',tn_DoubleMuData,recovariable,presentationbinning,selection,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',tn_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',tn_ZJets,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',tn_TTBar,recovariable,presentationbinning,selection+'*('+str(ttscale)+')*'+weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',tn_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)
	hs_rec_SMHiggs  =CreateHisto('hs_rec_SMHiggs','SM Higgs',tn_SMHiggs,recovariable,presentationbinning,selection+'*'+weight,SMHiggsStackStyle,Label)
	
	if channel==ell+ell+'jj':
		#print ' qcdselection :', qcdselection
		if 'weight' in qcdselection:
			# here we plot QCD MC in the ss region. 'weight_central' is present.
			hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD #mu-enriched',tn_QCDMu,recovariable,presentationbinning,qcdselection,QCDStackStyle,Label)
		if 'weight' not in qcdselection:
			#hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD #mu-enriched',tn_DoubleMuData,recovariable,presentationbinning,qcdselection,QCDStackStyle,Label)
			# here we plot QCD datadriven in the ss region, so we need special treatment to scale data
			# fixme todo adding ss non-iso scale factor # AH: but other BGs should be subtracted before scaling ? >> we can have a SF that applies to Data directly?
			hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD #mu-enriched',tn_DoubleMuData,recovariable,presentationbinning,qcdselection+'*('+str(qcdrescale)+')',QCDStackStyle,Label)

	if channel=='uvjj':
		hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD #mu-enriched',tn_QCDMu,recovariable,presentationbinning,qcdselection+'*('+str(qcdrescale)+')',QCDStackStyle,Label)
	
	if channel == ell+ell+'jj':
		
		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		hs_rec_DiBoson.Add(hs_rec_SMHiggs)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets,hs_rec_QCD]

	if channel == 'uvjj':
		
		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_WJets,hs_rec_QCD]


	MCStack = THStack ("MCStack","")
	SMIntegral = sum(k.Integral() for k in SM)
	print 'SM Integral: ',SMIntegral
	print 'hs_rec_Data.Integral(): ', hs_rec_Data.Integral(), 'hs_rec_Data.GetEntries()', hs_rec_Data.GetEntries()
	
	print 'Stacking...  ',	
	for x in SM:
		# x.Scale(mcdatascalepres)
		MCStack.Add(x)
		x.SetMaximum(10*hs_rec_Data.GetMaximum())

	MCStack.Draw("HIST")
	c1.cd(1).SetLogy()

	MCStack=BeautifyStack(MCStack,Label)

	#setZeroBinErrors(hs_rec_Data,MCStack)
	hs_rec_Data.Draw("E0PSAME")
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
	if channel==ell+ell+'jj':
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
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                            35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	else:
		#l2.DrawLatex(0.18,0.94,"                          "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                            35.9 fb^{-1} (13 TeV)")
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
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',te_WJets,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',te_DoubleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',te_ZJets,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',te_TTBar,recovariable,presentationbinning,selection+'*('+str(ttscale)+')*'+weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',te_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)

	print "THIS NUMBER --> hs_rec_TTBar.Integral():",hs_rec_TTBar.Integral(), 'hs_rec_TTBar.GetEntries():',hs_rec_TTBar.GetEntries()

	# hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD #mu-enriched [Pythia]',te_QCD,recovariable,presentationbinning,selection+'*'+weight,QCDStackStyle,Label)

	sig1name = ''
	sig2name = ''

	if channel == ell+ell+'jj':
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
	if channel==ell+ell+'jj':
		leg.AddEntry(hs_rec_ZJets,'Z/^{}#gamma* + jets')
	if channel==ell+ell+'jj':
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
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                            35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	else:
		#l2.DrawLatex(0.18,0.94,"                          "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                            35.9 fb^{-1} (13 TeV)")
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

	background =  [ 't_'+x.replace('\n','') for x in  ['QCD','DiBoson','WJets','TTBar','ZJets','SingleTop']]#original 
	#background =  [ 't_'+x.replace('\n','') for x in  ['QCD','DiBoson','WJets','TTBar','ZJetsOpt','SingleTop']]#this is if we use the 1/5 statistics ZJets for optimization to avoid 'overtraining'
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
	print '\n AH: I am in ParseFinalCards(): cardcoll is ', cardcoll, '\n'
	chan = '' + ell+ell+'jj'*(ell+ell+'jj' in cardcoll)+ 'uvjj'*('uvjj' in cardcoll) + 'HH_res'*('HH_res' in cardcoll)
	print '\n AH: I am in ParseFinalCards(): chan is ', chan, '\n'
	tables = glob(cardcoll)
	print '\n AH: I am in ParseFinalCards(): tables is ', tables, '\n'
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
	print '\n AH: I am in ParseFinalCards(): systypes is ', systypes, '\n'
	T = ''
	for n in range(len(systypes)):
		if systypes[n]=='':
			T = tables[n]
	#print T
	print '\n AH: I am in ParseFinalCards(): T is ', T, '\n'
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

	print '\n AH: I am in ParseFinalCards(): cardnames is ', cardnames, '\n'
	for card in cardnames:
		print '\n AH: I am in ParseFinalCards(): card is ', card, '\n'
		allcards = [line.replace('\n','') for line in os.popen('grep '+card+' '+cardcoll+' | grep -v '+str(card+'0')).readlines()]
		print '\n AH: I am in ParseFinalCards(): allcards is ', allcards, '\n'
		nc += 1
		mcard = ''
		scards = []
		for a in allcards:
			print 'here:',card,'\n',T,'\n',a, '\n' # AH:
			if T in a:
				mcard = a
			else:
				scards.append(a)
		print '\n AH: I am in ParseFinalCards(): mcard is ', mcard, '\n'
		print '\n AH: I am in ParseFinalCards(): scards is ', scards, '\n'
		statlines = []

		print headers
		print 'mcard',mcard
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
		procline2 = 'process  0 ' # AH:
		proc_num = 0
		for hh in headers:
			if 'Sig' in hh or 'Data' in hh:
				continue
			proc_num += 1
			procline1 += ' '+hh
			procline2 += ' ' + str(proc_num) + ' '
		#procline2 = 'process  0 '+(' 1 ')*(len(headers)-2) # AH:

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
			line = line.replace(ell+ell+'jj','_M_')
			line = line.replace('uvjj','_BetaHalf_M_')
			fout.write(line)
	fout.close()
	return f

def ShapeSystematic(channel,normalWeight,presel,finalWeight,finalSel):
	print '\n\n--------------\n--------------\nRunning shape systematics for',channel,'channel.  This will take some time, be patient....'
	NoSelection = ['1.0','No selection!']
	Selection = [normalWeight,'Weight only']
	PreSelection = [normalWeight+'*'+presel,'Preselection']
	FinalSelection = [finalWeight+'*'+finalSel,'Final Selection']
	Sels = [PreSelection,FinalSelection]
	"""
	for line in open(cutFile,'r'):
		if '=' in line:
			cutChannel = line.split('=')[0]
			cutSel = normalWeight+'*'+presel+'*'+line.split('=')[-1].replace('\n','').replace(' ','')
			#print cutLine
			Sels.append([cutSel, cutChannel])
	"""
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
	#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetNormalizationScaleFactors( NormalWeight+'*'+preselection, NormalDirectory, dyControlRegion, ttControlRegion,0)
	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = [[0.974561303332, 0.00553],[1.11001331611, 0.01308]]

	#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, '(MT_uv>100)*(MT_uv<200)*(JetCount<3.5)*(((CISV_jet1>0.97)+(CISV_jet2>0.97))<1)', '(MT_uv>100)*(MT_uv<200)*(JetCount>3.5)*(((CISV_jet1>0.97)+(CISV_jet2>0.97))>=1)')#fixme todo varying control sample MT window

	#Get presel scale factors for each weight
	for weight in scaleWeights:
		[[Rz_uujj_diff[weight],Rz_uujj_err_diff[weight]],[Rtt_uujj_diff[weight],Rtt_uujj_err_diff[weight]]] = GetNormalizationScaleFactors(NormalWeight+'*'+preselection+'*'+weight, NormalDirectory, dyControlRegion, ttControlRegion,0)

	for selection in Sels :
		print '  ',selection[1]

		maxZ =[0.,0.]
		maxW =[0.,0.]
		maxTT=[0.,0.]
		for weight in scaleWeights:
			print '     ',weight
			thisSel = selection[0]+'*'+weight

			Z  = QuickIntegral(t_ZJets,selection[0]+'*'+str(Rz_uujj),1.0)
			#W  = QuickIntegral(t_WJets,selection[0],1.0)
			tt = QuickIntegral(t_TTBar,selection[0]+'*'+str(Rtt_uujj),1.0)

			Z_diff  = QuickIntegral(t_ZJets,thisSel+'*'+str(Rz_uujj_diff[weight]),1.0)
			#W_diff  = QuickIntegral(t_WJets,thisSel,1.0)
			tt_diff = QuickIntegral(t_TTBar,thisSel+'*'+str(Rtt_uujj_diff[weight]),1.0)

			if Z[0]>0 : 
				Zperc =  [100*(abs(Z_diff[0]-Z[0])/Z[0]),100*math.sqrt((math.sqrt(Z_diff[1]*Z_diff[1]+Z[1]*Z[1])/(Z[0]*Z[0]))+
								       ((Z_diff[0]-Z[0])*(Z_diff[0]-Z[0])*Z[1]*Z[1]/(Z[0]*Z[0]*Z[0]*Z[0])))]
			else : ZPerc=[0.,0.]
			#if W[0]>0 : 
			#	Wperc =  [100*(abs(W_diff[0]-W[0])/W[0]),100*math.sqrt((math.sqrt(W_diff[1]*W_diff[1]+W[1]*W[1])/(W[0]*W[0]))+
			#					       ((W_diff[0]-W[0])*(W_diff[0]-W[0])*W[1]*W[1]/(W[0]*W[0]*W[0]*W[0])))]
			#else : Wperc=[0.,0.]
			if tt[0]>0 : 
				TTperc =  [100*(abs(tt_diff[0]-tt[0])/tt[0]),100*math.sqrt((math.sqrt(tt_diff[1]*tt_diff[1]+tt[1]*tt[1])/(tt[0]*tt[0]))+
									   ((tt_diff[0]-tt[0])*(tt_diff[0]-tt[0])*tt[1]*tt[1]/(tt[0]*tt[0]*tt[0]*tt[0])))]
			else : TTperc=[0.,0.]
		
			print '        Z:',Zperc
			#print '        W:',Wperc
			print '       tt:',TTperc
			if Zperc[0]>maxZ[0]  : maxZ = Zperc
			#if Wperc[0]>maxW[0]  : maxW = Wperc
			if TTperc[0]>maxTT[0]: maxTT=TTperc
			if scaleWeights[-1] in weight:		
				print ' Final  Z:',maxZ
				#print ' Final  W:',maxW
				print ' Final tt:',maxTT
	
		shapesysvar_Zjets.append (round(maxZ[0],2))
		#shapesysvar_Wjets.append (round(maxW[0],2))
		shapesysvar_TTjets.append(round(maxTT[0],2))
		
	print '\n\n--------------\n--------------\nFinal systematics:'
	sys.stdout.write('shapesysvar')
	sys.stdout.write(channel)
        sys.stdout.write('_zjets = ')
        sys.stdout.write(shapesysvar_Zjets)
	"""
	sys.stdout.write('shapesysvar')
        sys.stdout.write(channel)
        sys.stdout.write('_wjets = ')
        sys.stdout.write(shapesysvar_Wjets)
	"""
	sys.stdout.write('shapesysvar')
        sys.stdout.write(channel)
        sys.stdout.write('ttjets = ')
        sys.stdout.write(shapesysvar_TTjets)

	#these have 3 extra entries before signal starts
	#shapesysvar_uujj_zjets =  [16.35, 9.46, 12.27, 17.14, 16.0, 16.53, 17.01, 16.68, 16.4, 16.34, 16.22, 16.22, 16.25, 16.09, 16.25, 16.57, 16.74, 16.88, 17.3, 17.45, 17.94, 18.16, 18.12, 19.22, 18.91, 19.42, 19.37, 19.56, 19.51, 18.3, 17.77, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24, 17.24]
	#shapesysvar_uujj_wjets =  [17.24, 9.89, 29.31, 24.0, 23.73, 24.28, 24.46, 24.55, 24.32, 25.25, 25.76, 26.19, 25.6, 26.6, 26.98, 28.27, 28.01, 27.78, 27.78, 27.78, 27.78, 27.78, 27.78, 27.78, 27.78, 27.44, 27.44, 28.36, 28.36, 28.36, 28.36, 28.36, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	#shapesysvar_uujj_ttjets =  [33.0, 33.01, 35.65, 35.19, 35.24, 36.16, 37.41, 39.09, 40.03, 40.9, 41.67, 42.47, 43.18, 43.87, 44.21, 44.56, 45.91, 47.12, 47.9, 48.52, 49.2, 47.6, 47.23, 47.62, 47.73, 45.32, 43.66, 44.82, 45.28, 44.54, 45.37, 45.37, 45.37, 47.85, 47.85, 47.85, 47.85, 47.85, 47.85, 47.85]

def blind(h,pad):
	blindstart=0.1
	for bin in range(h.GetNbinsX()):
		if h.GetBinLowEdge(bin+1)>blindstart:
			if pad==1:
				h.SetBinContent(bin+1,0.00001)
				h.SetBinError(bin+1,0.0)
			if pad==2:
				h.SetBinContent(bin+1,1.0)
				h.SetBinError(bin+1,0.0)
	#h.SetMarkerSize(0.0)
	#h.SetLineWidth(0)

main()
