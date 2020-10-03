import os, sys, math, random, platform, time, re
from glob import glob
from argparse import ArgumentParser

global preselectionmumu 

#fixme check on lljj excess talk variables: https://indico.cern.ch/event/588812/contributions/2374355/attachments/1374491/2086457/Update_lljj_Ping_Tan_Nov21_2016.pdf

##########################################################################
########    GLOBAL VARIABLES NEEDED FOR PLOTS AND ANALYSIS        ########
##########################################################################

# Input Options - file, cross-section, number of events
parser = ArgumentParser()
parser.add_argument("-y", "--year", dest="year", help="option to pick running year (2016,2017,2018)", metavar="YEAR")
parser.add_argument("-b", "--btags", dest="btags", help="option to pick minimum number of b-tagged jets required (0,1,2)", metavar="BTAGS", default="0")
options = parser.parse_args()
year = str(options.year)
btags = str(options.btags)


# Directory where root files are kept and the tree you want to get root files from
if year == '2016':
	NormalDirectory = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/2016/gmadigan/NTupleAnalyzer_nanoAOD_Full2016QuickTest_stockNano_2020_09_18_21_07_21/SummaryFiles'
	QCDDirectory    = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/trees/NTupleAnalyzer_nanoAOD_Full2016QCDNonIsoQuickTest_2019_10_14/SummaryFiles' #Placeholder
	EMuDirectory    = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/trees/NTupleAnalyzer_nanoAOD_Full2016EMuSwitch_2019_10_14/SummaryFiles' #Placeholder
elif year == '2017':
	NormalDirectory = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/2017/gmadigan/NTupleAnalyzer_nanoAOD_Full2017QuickTest_stockNano_2020_09_09_23_00_36/SummaryFiles'
	QCDDirectory    = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/trees/NTupleAnalyzer_nanoAOD_Full2016QCDNonIsoQuickTest_2019_10_14/SummaryFiles' #Placeholder
	EMuDirectory    = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/trees/NTupleAnalyzer_nanoAOD_Full2016EMuSwitch_2019_10_14/SummaryFiles' #Placeholder
elif year == '2018':
	NormalDirectory = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/stockNanoTrees/2018/gmadigan/NTupleAnalyzer_nanoAOD_Full2018QuickTest_stockNano_2020_07_05_00_00_41/SummaryFiles'
	QCDDirectory    = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/trees/NTupleAnalyzer_nanoAOD_Full2016QCDNonIsoQuickTest_2019_10_14/SummaryFiles' #Placeholder
	EMuDirectory    = '/eos/cms/store/group/phys_exotica/leptonsPlusJets/LQ/LQ2/trees/NTupleAnalyzer_nanoAOD_Full2016EMuSwitch_2019_10_14/SummaryFiles' #Placeholder
else:
	print "Did not enter a valid year.\nPlease use option \'-y\' to select running year (2016,2017,2018)"
	exit()

# The name of the main ttree (ntuple structure)
TreeName = "PhysicalVariables"

# Integrated luminosity for normalization
if year == '2016':
	lumi = 35920.
	lumiInvfb = '35.9'
elif year == '2017':
	lumi = 41530.
	lumiInvfb = '41.5'
elif year == '2018':
	lumi = 59740.
	lumiInvfb = '59.7'

#Muon HLT MC scale factor
#https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2

# Single-mu trigger efficiencies as a function of muon Eta. 
# This is for the case of one muon

#2016 eff - eta dependence only, HLT_Mu50 OR HLT_TkMu
singlemuHLT = '*(mu1hltSF)'
# This is for the case of two muons (i.e. the above factors, but for the case where the event has two muons)
doublemuHLT = '*(1.0-((1.0-mu1hltSF)*(1.0-mu2hltSF)))'

singlemuHLTEMUSF =  '*((IsMuon_muon1)*(0.949621*(Eta_muon1>-2.4)*(Eta_muon1<=-2.1)+0.967073*(Eta_muon1>-2.1)*(Eta_muon1<=-1.6)+1.02402*(Eta_muon1>-1.6)*(Eta_muon1<=-1.2)+0.958010*(Eta_muon1>-1.2)*(Eta_muon1<=-0.9)+0.986735*(Eta_muon1>-0.9)*(Eta_muon1<=-0.3)+0.923577*(Eta_muon1>-0.3)*(Eta_muon1<=-0.2)+0.975074*(Eta_muon1>-0.2)*(Eta_muon1<=0.0)+0.977559*(Eta_muon1>0.0)*(Eta_muon1<=0.2)+0.947337*(Eta_muon1>0.2)*(Eta_muon1<=0.3)+0.982190*(Eta_muon1>0.3)*(Eta_muon1<=0.9)+0.968889*(Eta_muon1>0.9)*(Eta_muon1<=1.2)+1.01164*(Eta_muon1>1.2)*(Eta_muon1<=1.6)+0.956268*(Eta_muon1>1.6)*(Eta_muon1<=2.1)+0.916149*(Eta_muon1>2.1)*(Eta_muon1<=2.4))+(IsMuon_muon2)*(0.949621*(Eta_muon2>-2.4)*(Eta_muon2<=-2.1)+0.967073*(Eta_muon2>-2.1)*(Eta_muon2<=-1.6)+1.02402*(Eta_muon2>-1.6)*(Eta_muon2<=-1.2)+0.958010*(Eta_muon2>-1.2)*(Eta_muon2<=-0.9)+0.986735*(Eta_muon2>-0.9)*(Eta_muon2<=-0.3)+0.923577*(Eta_muon2>-0.3)*(Eta_muon2<=-0.2)+0.975074*(Eta_muon2>-0.2)*(Eta_muon2<=0.0)+0.977559*(Eta_muon2>0.0)*(Eta_muon2<=0.2)+0.947337*(Eta_muon2>0.2)*(Eta_muon2<=0.3)+0.982190*(Eta_muon2>0.3)*(Eta_muon2<=0.9)+0.968889*(Eta_muon2>0.9)*(Eta_muon2<=1.2)+1.01164*(Eta_muon2>1.2)*(Eta_muon2<=1.6)+0.956268*(Eta_muon2>1.6)*(Eta_muon2<=2.1)+0.916149*(Eta_muon2>2.1)*(Eta_muon2<=2.4)))'

# This is for the case of the E-mu sample, where one "muon" is replaced by an electron. In that case, we check
# which muon is a real muon (IsMuon_muon1) and apply the trigger efficiency based on the muon


#These use averaged, run-dependent values - Efficiency NOT scale factor!
singlemuHLTEMU =  '*((IsMuon_muon1*(0.931484*(abs(Eta_muon1)<=0.9)*(Pt_muon1>52)*(Pt_muon1<55)+0.936389*(abs(Eta_muon1)<=0.9)*(Pt_muon1>55)*(Pt_muon1<60)+0.936215*(abs(Eta_muon1)<=0.9)*(Pt_muon1>60)*(Pt_muon1<80)+0.932935*(abs(Eta_muon1)<=0.9)*(Pt_muon1>80)*(Pt_muon1<120)+0.924966*(abs(Eta_muon1)<=0.9)*(Pt_muon1>120)*(Pt_muon1<200)+0.912550*(abs(Eta_muon1)<=0.9)*(Pt_muon1>200)*(Pt_muon1<300)+0.915244*(abs(Eta_muon1)<=0.9)*(Pt_muon1>300)*(Pt_muon1<400)+0.865542*(abs(Eta_muon1)<=0.9)*(Pt_muon1>400)+0.928172*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>52)*(Pt_muon1<55)+0.933461*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>55)*(Pt_muon1<60)+0.934581*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>60)*(Pt_muon1<80)+0.930415*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>80)*(Pt_muon1<120)+0.918477*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>120)*(Pt_muon1<200)+0.895276*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>200)*(Pt_muon1<300)+0.895417*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>300)*(Pt_muon1<400)+0.930819*(abs(Eta_muon1)>0.9)*(abs(Eta_muon1)<=1.2)*(Pt_muon1>400)+0.881011*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>52)*(Pt_muon1<55)+0.887047*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>55)*(Pt_muon1<60)+0.890108*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>60)*(Pt_muon1<80)+0.890968*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>80)*(Pt_muon1<120)+0.890131*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>120)*(Pt_muon1<200)+0.881725*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>200)*(Pt_muon1<300)+0.888385*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>300)*(Pt_muon1<400)+0.858157*(abs(Eta_muon1)>1.2)*(abs(Eta_muon1)<=2.1)*(Pt_muon1>400)+0.775304*(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<=2.4)*(Pt_muon1>52)*(Pt_muon1<55)+0.802406*(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<=2.4)*(Pt_muon1>55)*(Pt_muon1<60)+0.813275*(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<=2.4)*(Pt_muon1>60)*(Pt_muon1<80)+0.816880*(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<=2.4)*(Pt_muon1>80)*(Pt_muon1<120)+0.818516*(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<=2.4)*(Pt_muon1>120)*(Pt_muon1<200)+0.766791*(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<=2.4)*(Pt_muon1>200)*(Pt_muon1<300)+0.767369*(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<=2.4)*(Pt_muon1>300)*(Pt_muon1<400)+0.705534*(abs(Eta_muon1)>2.1)*(abs(Eta_muon1)<=2.4)*(Pt_muon1>400)))'

singlemuHLTEMU +=  '+(IsMuon_muon2*(0.931484*(abs(Eta_muon2)<=0.9)*(Pt_muon2>52)*(Pt_muon2<55)+0.936389*(abs(Eta_muon2)<=0.9)*(Pt_muon2>55)*(Pt_muon2<60)+0.936215*(abs(Eta_muon2)<=0.9)*(Pt_muon2>60)*(Pt_muon2<80)+0.932935*(abs(Eta_muon2)<=0.9)*(Pt_muon2>80)*(Pt_muon2<120)+0.924966*(abs(Eta_muon2)<=0.9)*(Pt_muon2>120)*(Pt_muon2<200)+0.912550*(abs(Eta_muon2)<=0.9)*(Pt_muon2>200)*(Pt_muon2<300)+0.915244*(abs(Eta_muon2)<=0.9)*(Pt_muon2>300)*(Pt_muon2<400)+0.865542*(abs(Eta_muon2)<=0.9)*(Pt_muon2>400)+0.928172*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>52)*(Pt_muon2<55)+0.933461*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>55)*(Pt_muon2<60)+0.934581*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>60)*(Pt_muon2<80)+0.930415*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>80)*(Pt_muon2<120)+0.918477*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>120)*(Pt_muon2<200)+0.895276*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>200)*(Pt_muon2<300)+0.895417*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>300)*(Pt_muon2<400)+0.930819*(abs(Eta_muon2)>0.9)*(abs(Eta_muon2)<=1.2)*(Pt_muon2>400)+0.881011*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>52)*(Pt_muon2<55)+0.887047*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>55)*(Pt_muon2<60)+0.890108*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>60)*(Pt_muon2<80)+0.890968*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>80)*(Pt_muon2<120)+0.890131*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>120)*(Pt_muon2<200)+0.881725*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>200)*(Pt_muon2<300)+0.888385*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>300)*(Pt_muon2<400)+0.858157*(abs(Eta_muon2)>1.2)*(abs(Eta_muon2)<=2.1)*(Pt_muon2>400)+0.775304*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4)*(Pt_muon2>52)*(Pt_muon2<55)+0.802406*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4)*(Pt_muon2>55)*(Pt_muon2<60)+0.813275*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4)*(Pt_muon2>60)*(Pt_muon2<80)+0.816880*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4)*(Pt_muon2>80)*(Pt_muon2<120)+0.818516*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4)*(Pt_muon2>120)*(Pt_muon2<200)+0.766791*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4)*(Pt_muon2>200)*(Pt_muon2<300)+0.767369*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4)*(Pt_muon2>300)*(Pt_muon2<400)+0.705534*(abs(Eta_muon2)>2.1)*(abs(Eta_muon2)<=2.4)*(Pt_muon2>400))))'

#These use averaged, run-dependent values - Efficiency NOT scale factor!
#only eta dependent, not pt 
singlemuHLTEMU  = '*((IsMuon_muon1)*(0.808813*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.840182*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.930111*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.932994*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.944875*(Eta_muon1>-0.9)*(Eta_muon1<-0.3)+0.834415*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.942008*(Eta_muon1>-0.2)*(Eta_muon1<0.)+0.945691*(Eta_muon1>0.)*(Eta_muon1<0.2)+0.852895*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.944523*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.930995*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.922036*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.850333*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.791896*(Eta_muon1>2.1)*(Eta_muon1<2.4) )'
singlemuHLTEMU += '+(IsMuon_muon2)*(0.808813*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.840182*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.930111*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.932994*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.944875*(Eta_muon2>-0.9)*(Eta_muon2<-0.3)+0.834415*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.942008*(Eta_muon2>-0.2)*(Eta_muon2<0.)+0.945691*(Eta_muon2>0.)*(Eta_muon2<0.2)+0.852895*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.944523*(Eta_muon2>0.3)*(Eta_muon2<0.9)+0.930995*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.922036*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.850333*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.791896*(Eta_muon2>2.1)*(Eta_muon2<2.4)))'


#Muon ID and Iso MC scale factors
#https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2
#eta-binned
singleMuIdScale = '*mu1idSF'
doubleMuIdScale = '*mu1idSF*mu2idSF'

singleMuIsoScale = '*mu1isoSF'
doubleMuIsoScale = '*mu1isoSF*mu2isoSF'

#eta-binned

MuIdScaleEMU = '*(IsMuon_muon1*(0.969328*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.98193*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.989731*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.975207*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.987146*(Eta_muon1>-0.9)*(Eta_muon1<-0.3)+0.965056*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.988669*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.958604*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.986526*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.972524*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.98789*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.984616*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.972038*(Eta_muon1>2.1)*(Eta_muon1<2.4))+IsMuon_muon2*(0.969328*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.98193*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.989731*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.975207*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.987146*(Eta_muon2>-0.9)*(Eta_muon2<-0.3)+0.965056*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.988669*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.958604*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.986526*(Eta_muon2>0.3)*(Eta_muon2<0.9)+0.972524*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.98789*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.984616*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.972038*(Eta_muon2>2.1)*(Eta_muon2<2.4)))'

MuIsoScaleEMU = '*(IsMuon_muon1*(0.999026*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.999513*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.999475*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.999077*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.998022*(Eta_muon1>-0.9)*(Eta_muon1<-0.3)+0.997644*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.998011*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.997196*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.997877*(Eta_muon1>0.3)*(Eta_muon1<0.9)+0.999609*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.999474*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.999761*(Eta_muon1>1.6)*(Eta_muon1<2.1)+1.00043*(Eta_muon1>2.1)*(Eta_muon1<2.4))+IsMuon_muon2*(0.999026*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.999513*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.999475*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.999077*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.998022*(Eta_muon2>-0.9)*(Eta_muon2<-0.3)+0.997644*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.998011*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.997196*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.997877*(Eta_muon2>0.3)*(Eta_muon2<0.9)+0.999609*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.999474*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.999761*(Eta_muon2>1.6)*(Eta_muon2<2.1)+1.00043*(Eta_muon2>2.1)*(Eta_muon2<2.4)))'

# This is the rescaling of the EMu data for the ttbar estimate (2 - Eff_trigger)
dataHLTEMUADJ = '*(2.0 - 1.0'+singlemuHLTEMU+')'

#This is for HIP problem https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2#Tracking_efficiency_provided_by
trackerHIP1 = '*(0.991237*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.994853*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.996413*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.997157*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.997512*(Eta_muon1>-0.9)*(Eta_muon1<-0.6)+0.99756*(Eta_muon1>-0.6)*(Eta_muon1<-0.3)+0.996745*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.996996*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.99772*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998604*(Eta_muon1>0.3)*(Eta_muon1<0.6)+0.998321*(Eta_muon1>0.6)*(Eta_muon1<0.9)+0.997682*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.995252*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.994919*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.987334*(Eta_muon1>2.1)*(Eta_muon1<2.4) )'
trackerHIP2 = '*(0.991237*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.994853*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.996413*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.997157*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.997512*(Eta_muon2>-0.9)*(Eta_muon2<-0.6)+0.99756*(Eta_muon2>-0.6)*(Eta_muon2<-0.3)+0.996745*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.996996*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.99772*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.998604*(Eta_muon2>0.3)*(Eta_muon2<0.6)+0.998321*(Eta_muon2>0.6)*(Eta_muon2<0.9)+0.997682*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.995252*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.994919*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.987334*(Eta_muon2>2.1)*(Eta_muon2<2.4) )'

trackerHIPEMU  = '*((IsMuon_muon1)*(0.991237*(Eta_muon1>-2.4)*(Eta_muon1<-2.1)+0.994853*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.996413*(Eta_muon1>-1.6)*(Eta_muon1<-1.2)+0.997157*(Eta_muon1>-1.2)*(Eta_muon1<-0.9)+0.997512*(Eta_muon1>-0.9)*(Eta_muon1<-0.6)+0.99756*(Eta_muon1>-0.6)*(Eta_muon1<-0.3)+0.996745*(Eta_muon1>-0.3)*(Eta_muon1<-0.2)+0.996996*(Eta_muon1>-0.2)*(Eta_muon1<0.2)+0.99772*(Eta_muon1>0.2)*(Eta_muon1<0.3)+0.998604*(Eta_muon1>0.3)*(Eta_muon1<0.6)+0.998321*(Eta_muon1>0.6)*(Eta_muon1<0.9)+0.997682*(Eta_muon1>0.9)*(Eta_muon1<1.2)+0.995252*(Eta_muon1>1.2)*(Eta_muon1<1.6)+0.994919*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.987334*(Eta_muon1>2.1)*(Eta_muon1<2.4) )'
trackerHIPEMU += '+(IsMuon_muon2)*(0.991237*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.994853*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.996413*(Eta_muon2>-1.6)*(Eta_muon2<-1.2)+0.997157*(Eta_muon2>-1.2)*(Eta_muon2<-0.9)+0.997512*(Eta_muon2>-0.9)*(Eta_muon2<-0.6)+0.99756*(Eta_muon2>-0.6)*(Eta_muon2<-0.3)+0.996745*(Eta_muon2>-0.3)*(Eta_muon2<-0.2)+0.996996*(Eta_muon2>-0.2)*(Eta_muon2<0.2)+0.99772*(Eta_muon2>0.2)*(Eta_muon2<0.3)+0.998604*(Eta_muon2>0.3)*(Eta_muon2<0.6)+0.998321*(Eta_muon2>0.6)*(Eta_muon2<0.9)+0.997682*(Eta_muon2>0.9)*(Eta_muon2<1.2)+0.995252*(Eta_muon2>1.2)*(Eta_muon2<1.6)+0.994919*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.987334*(Eta_muon2>2.1)*(Eta_muon2<2.4) ))'

#trackerHIPEMU = '*((IsMuon_muon2)*(0.982399*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.991747*(Eta_muon1>-2.1)*(Eta_muon1<-1.6)+0.995945*(Eta_muon1>-1.6)*(Eta_muon1<-1.1)+0.993413*(Eta_muon1>-1.1)*(Eta_muon1<-0.6)+0.991461*(Eta_muon1>-0.6)*(Eta_muon1<0)+0.99468*(Eta_muon1>0)*(Eta_muon1<0.6)+0.996666*(Eta_muon1>0.6)*(Eta_muon1<1.1)+0.994934*(Eta_muon1>1.1)*(Eta_muon1<1.6)+0.991187*(Eta_muon1>1.6)*(Eta_muon1<2.1)+0.976812*(Eta_muon1>2.1)*(Eta_muon1<2.4) )'
#trackerHIPEMU += '+(IsMuon_muon2)*(0.982399*(Eta_muon2>-2.4)*(Eta_muon2<-2.1)+0.991747*(Eta_muon2>-2.1)*(Eta_muon2<-1.6)+0.995945*(Eta_muon2>-1.6)*(Eta_muon2<-1.1)+0.993413*(Eta_muon2>-1.1)*(Eta_muon2<-0.6)+0.991461*(Eta_muon2>-0.6)*(Eta_muon2<0)+0.99468*(Eta_muon2>0)*(Eta_muon2<0.6)+0.996666*(Eta_muon2>0.6)*(Eta_muon2<1.1)+0.994934*(Eta_muon2>1.1)*(Eta_muon2<1.6)+0.991187*(Eta_muon2>1.6)*(Eta_muon2<2.1)+0.976812*(Eta_muon2>2.1)*(Eta_muon2<2.4) ))'

eleRECOScale = '*((1-IsMuon_muon1)*(((Eta_muon1>-2.5)*(Eta_muon1<-2.45)*1.3176)+((Eta_muon1>-2.45)*(Eta_muon1<-2.4)*1.11378)+((Eta_muon1>-2.4)*(Eta_muon1<-2.3)*1.02463)+((Eta_muon1>-2.3)*(Eta_muon1<-2.2)*1.01364)+((Eta_muon1>-2.2)*(Eta_muon1<-2)*1.00728)+((Eta_muon1>-2)*(Eta_muon1<-1.8)*0.994819)+((Eta_muon1>-1.8)*(Eta_muon1<-1.63)*0.994786)+((Eta_muon1>-1.63)*(Eta_muon1<-1.566)*0.991632)+((Eta_muon1>-1.566)*(Eta_muon1<-1.444)*0.963128)+((Eta_muon1>-1.444)*(Eta_muon1<-1.2)*0.989701)+((Eta_muon1>-1.2)*(Eta_muon1<-1)*0.985656)+((Eta_muon1>-1)*(Eta_muon1<-0.6)*0.981595)+((Eta_muon1>-0.6)*(Eta_muon1<-0.4)*0.984678)+((Eta_muon1>-0.4)*(Eta_muon1<-0.2)*0.981614)+((Eta_muon1>-0.2)*(Eta_muon1<0)*0.980433)+((Eta_muon1>0)*(Eta_muon1<0.2)*0.984552)+((Eta_muon1>0.2)*(Eta_muon1<0.4)*0.988764)+((Eta_muon1>0.4)*(Eta_muon1<0.6)*0.987743)+((Eta_muon1>0.6)*(Eta_muon1<1)*0.987743)+((Eta_muon1>1)*(Eta_muon1<1.2)*0.987743)+((Eta_muon1>1.2)*(Eta_muon1<1.444)*0.98768)+((Eta_muon1>1.444)*(Eta_muon1<1.566)*0.967598)+((Eta_muon1>1.566)*(Eta_muon1<1.63)*0.989627)+((Eta_muon1>1.63)*(Eta_muon1<1.8)*0.992761)+((Eta_muon1>1.8)*(Eta_muon1<2)*0.991761)+((Eta_muon1>2)*(Eta_muon1<2.2)*0.99794)+((Eta_muon1>2.2)*(Eta_muon1<2.3)*1.00104)+((Eta_muon1>2.3)*(Eta_muon1<2.4)*0.989507)+((Eta_muon1>2.4)*(Eta_muon1<2.45)*0.970519)+((Eta_muon1>2.45)*(Eta_muon1<2.5)*0.906667))+((1-IsMuon_muon2)*(((Eta_muon2>-2.5)*(Eta_muon2<-2.45)*1.3176)+((Eta_muon2>-2.45)*(Eta_muon2<-2.4)*1.11378)+((Eta_muon2>-2.4)*(Eta_muon2<-2.3)*1.02463)+((Eta_muon2>-2.3)*(Eta_muon2<-2.2)*1.01364)+((Eta_muon2>-2.2)*(Eta_muon2<-2)*1.00728)+((Eta_muon2>-2)*(Eta_muon2<-1.8)*0.994819)+((Eta_muon2>-1.8)*(Eta_muon2<-1.63)*0.994786)+((Eta_muon2>-1.63)*(Eta_muon2<-1.566)*0.991632)+((Eta_muon2>-1.566)*(Eta_muon2<-1.444)*0.963128)+((Eta_muon2>-1.444)*(Eta_muon2<-1.2)*0.989701)+((Eta_muon2>-1.2)*(Eta_muon2<-1)*0.985656)+((Eta_muon2>-1)*(Eta_muon2<-0.6)*0.981595)+((Eta_muon2>-0.6)*(Eta_muon2<-0.4)*0.984678)+((Eta_muon2>-0.4)*(Eta_muon2<-0.2)*0.981614)+((Eta_muon2>-0.2)*(Eta_muon2<0)*0.980433)+((Eta_muon2>0)*(Eta_muon2<0.2)*0.984552)+((Eta_muon2>0.2)*(Eta_muon2<0.4)*0.988764)+((Eta_muon2>0.4)*(Eta_muon2<0.6)*0.987743)+((Eta_muon2>0.6)*(Eta_muon2<1)*0.987743)+((Eta_muon2>1)*(Eta_muon2<1.2)*0.987743)+((Eta_muon2>1.2)*(Eta_muon2<1.444)*0.98768)+((Eta_muon2>1.444)*(Eta_muon2<1.566)*0.967598)+((Eta_muon2>1.566)*(Eta_muon2<1.63)*0.989627)+((Eta_muon2>1.63)*(Eta_muon2<1.8)*0.992761)+((Eta_muon2>1.8)*(Eta_muon2<2)*0.991761)+((Eta_muon2>2)*(Eta_muon2<2.2)*0.99794)+((Eta_muon2>2.2)*(Eta_muon2<2.3)*1.00104)+((Eta_muon2>2.3)*(Eta_muon2<2.4)*0.989507)+((Eta_muon2>2.4)*(Eta_muon2<2.45)*0.970519)+((Eta_muon2>2.45)*(Eta_muon2<2.5)*0.906667))))'

#eleHEEPScale = '*((1-IsMuon_muon1)*(((Eta_muon1>-2.5)*(Eta_muon1<-1.566)*0.983)+((Eta_muon1>-1.4442)*(Eta_muon1<-0.5)*0.971)+((Eta_muon1>-0.5)*(Eta_muon1<-0.0)*0.961)+((Eta_muon1>0.0)*(Eta_muon1<0.5)*0.973)+((Eta_muon1>0.5)*(Eta_muon1<1.4442)*0.978)+((Eta_muon1>1.566)*(Eta_muon1<2.5)*0.980))+(1-IsMuon_muon2)*(((Eta_muon2>-2.5)*(Eta_muon2<-1.566)*0.984)+((Eta_muon2>-1.4442)*(Eta_muon2<-0.5)*0.971)+((Eta_muon2>-0.5)*(Eta_muon2<-0.0)*0.961)+((Eta_muon2>0.0)*(Eta_muon2<0.5)*0.973)+((Eta_muon2>0.5)*(Eta_muon2<1.4442)*0.978)+((Eta_muon2>1.566)*(Eta_muon2<2.5)*0.980)))'
eleHEEPScale = '*((1-IsMuon_muon1)*(((abs(Eta_muon1)>0.0)*(abs(Eta_muon1)<0.5)*0.967)+((abs(Eta_muon1)>0.5)*(abs(Eta_muon1)<1.4442)*0.975)+((abs(Eta_muon1)>1.566)*(abs(Eta_muon1)<2.5)*0.983))+(1-IsMuon_muon2)*((abs(Eta_muon2)>0.0)*(abs(Eta_muon2)<0.5)*0.967+((abs(Eta_muon2)>0.5)*(abs(Eta_muon2)<1.4442)*0.975)+((abs(Eta_muon2)>1.566)*(abs(Eta_muon2)<2.5)*0.983)))'

#BTAG scale factors and selection
deepJetWPmedium = '1'
if year == '2016': deepJetWPmedium = '0.3093'
elif year == '2017': deepJetWPmedium = '0.3033'
elif year == '2018': deepJetWPmedium = '0.2770'

if btags == '0':
	bTagSFmedium = '*1'
	bTagSFmediumUp = '*1'
	bTagSFmediumDown = '*1'
	bTagselmedium = '*(((DeepJet_jet1>'+deepJetWPmedium+')+(DeepJet_jet2>'+deepJetWPmedium+'))==0)'
elif btags == '1':
	bTagSFmedium = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium+')*bTagSF_jet1)*(1-(DeepJet_jet2>'+deepJetWPmedium+')*bTagSF_jet2))'
	bTagSFmediumUp = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium+')*bTagSF_jet1Up)*(1-(DeepJet_jet2>'+deepJetWPmedium+')*bTagSF_jet2Up))'
	bTagSFmediumDown = '*(1-(1-(DeepJet_jet1>'+deepJetWPmedium+')*bTagSF_jet1Down)*(1-(DeepJet_jet2>'+deepJetWPmedium+')*bTagSF_jet2Down))'
	bTagselmedium = '*(((DeepJet_jet1>'+deepJetWPmedium+')+(DeepJet_jet2>'+deepJetWPmedium+'))>0)'
elif btags == '2':
	bTagSFmedium = '*(DeepJet_jet1>'+deepJetWPmedium+')*(DeepJet_jet2>'+deepJetWPmedium+')*(1-(1-bTagSF_jet1)*(1-bTagSF_jet2))'
	bTagSFmediumUp = '*(DeepJet_jet1>'+deepJetWPmedium+')*(DeepJet_jet2>'+deepJetWPmedium+')*(1-(1-bTagSF_jet1Up)*(1-bTagSF_jet2Up))'
	bTagSFmediumDown = '*(DeepJet_jet1>'+deepJetWPmedium+')*(DeepJet_jet2>'+deepJetWPmedium+')*(1-(1-bTagSF_jet1Down)*(1-bTagSF_jet2Down))'
	bTagselmedium = '*(((DeepJet_jet1>'+deepJetWPmedium+')+(DeepJet_jet2>'+deepJetWPmedium+'))>1)'
else:
	print "Did not select a valid minimum number of b-tags to require; only 2 b-tags kept in analysis trees.\n Please use option \'-b\' to select a valid number of minimum b-tagged jets (0,1,2)"
	exit()

# Weights for different MC selections, including integrated luminosity, event weight, and trigger weight
#NormalWeightMuMu = str(lumi)+'*weight_central*((pass_HLTMu50+pass_HLTTkMu50)>0)'+doublemuHLT+doubleMuIdScale+doubleMuIsoScale+trackerHIP1+trackerHIP2
#NormalWeightMuNu = str(lumi)+'*weight_central*((pass_HLTMu50+pass_HLTTkMu50)>0)'+singlemuHLT+singleMuIdScale+singleMuIsoScale+trackerHIP1
#NormalWeightEMu = str(lumi)+'*weight_central*((pass_HLTMu50+pass_HLTTkMu50)>0)'+singlemuHLTEMU+MuIdScaleEMU+MuIsoScaleEMU+eleRECOScale+eleHEEPScale+trackerHIPEMU
NormalWeightMuMu = str(lumi)+'*weight_central'+doublemuHLT+doubleMuIdScale+doubleMuIsoScale+trackerHIP1+trackerHIP2+bTagSFmedium
NormalWeightMuNu = str(lumi)+'*weight_central'+singlemuHLT+singleMuIdScale+singleMuIsoScale+trackerHIP1
#fixme checking eta restriction on muons and electrons to fix r_uu/eu
muEtaRestrict = '*((IsMuon_muon1>0)*(abs(Eta_muon1)<2.1)+(IsMuon_muon2>0)*(abs(Eta_muon2)<2.1))'
NormalWeightEMu_ttbar = str(lumi)+'*weight_central'+singlemuHLTEMU+MuIdScaleEMU+MuIsoScaleEMU+eleRECOScale+eleHEEPScale+trackerHIPEMU#+muEtaRestrict
NormalWeightEMu = str(lumi)+'*weight_central'+singlemuHLTEMU+MuIdScaleEMU+MuIsoScaleEMU+eleRECOScale+eleHEEPScale+trackerHIPEMU#+muEtaRestrict
NormalWeightEMuNoHLT = str(lumi)+'*weight_central'+MuIdScaleEMU+MuIsoScaleEMU+eleRECOScale+eleHEEPScale+trackerHIPEMU#+muEtaRestrict#fixme do we need scale factors here?

#ZptReweight = '*(0.95-0.1*TMath::Erf((Pt_mu1mu2_gen-14.0)/8.8))'

# This is the real data trigger condition
dataHLT = '*0'
if year == '2016': dataHLT = '*((pass_HLTMu50+pass_HLTTkMu50)>0)'
elif year == '2017' or year == '2018': dataHLT = '*((pass_HLTMu50+pass_HLTOldMu100+pass_HLTTkMu100)>0)'

# This is the set of event filters used
#passfilter =  '*(passDataCert*passPrimaryVertex*(GoodVertexCount>=1))' #fixme json not working
passfilter =  '*(Flag_goodVertices*(GoodVertexCount>=1))'
passfilter += '*(Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter)'
passfilter += '*(Flag_eeBadScFilter*Flag_EcalDeadCellTriggerPrimitiveFilter)'
passfilter += '*(Flag_globalSuperTightHalo2016Filter)'
passfilter += '*(Flag_BadPFMuonFilter)'#*Flag_BadChargedHadron)'
#passfilter += '*(noBadMuonsFlag*(1-duplicateMuonsFlag))'

# This defines the preselections for the mu-mu, mu-nu, and e-mu samples
preselectionmumu_single = '((Pt_muon1>53)*(Pt_muon2>53)*(Pt_jet1>50)*(St_uujj>250)*(M_uu>50)*(DR_muon1muon2>0.3)'+bTagselmedium+')'
preselectionmumu = '((Pt_muon1>53)*(Pt_muon2>53)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3)'+bTagselmedium+')'
preselectionmunu = '((Pt_muon1>53)*(Pt_muon2<53)*(Pt_miss>55)*(Pt_jet1>50)*(Pt_jet2>50)*(Pt_ele1<53)*(St_uvjj>300)*(MT_uv>50.0)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5))'
preselectionemu  = '((Pt_muon1>53)*(Pt_muon2>53)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3))'

# Add the filters to the preselections
preselectionmumu_single += passfilter
preselectionmumu += passfilter
preselectionmunu += passfilter
preselectionemu  += passfilter


munu1 = '(MT_uv>70)*(MT_uv<110)*(((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)*(2-0.887973*((1.+(0.0523821*Pt_jet1))/(1.+(0.0460876*Pt_jet1))))'
munu2 = '(MT_uv>70)*(MT_uv<110)*(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>=1)*(0.561694*((1.+(0.31439*Pt_jet1))/(1.+(0.17756*Pt_jet1))))'#*(CISV_jet1>CISV_jet2)+(0.901114+(1.40704e-05*(Pt_jet2)))*(CISV_jet2>0.8484)*(CISV_jet1<CISV_jet2))'

# https://github.com/ferencek/cms-MyAnalyzerDijetCode/blob/master/MyAnalyzer_MainAnalysis_DijetBBTag_2011.cc#L1310
# (0 btagged jets)*1 + (1 btagged jet)*w(0|1) + (2 btagged jets)*w(0|2) #fixme todo
#munu1 = '(MT_uv>70)*(MT_uv<110)*((((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)*1.0 + (((CISV_jet1>0.5426)+(CISV_jet2>0.5426))==1)*(1-(0.887973*(1.+(0.0523821*(Pt_jet1*(CISV_jet1>0.5426)+Pt_jet2*(CISV_jet1>0.5426))/(1.+(0.0460876*(Pt_jet1*(CISV_jet1>0.5426)+Pt_jet2*(CISV_jet1>0.5426)))))))) + (((CISV_jet1>0.5426)+(CISV_jet2>0.5426))>1)*(1-(0.887973*(1.+(0.0523821*Pt_jet1)/(1.+(0.0460876*Pt_jet1)))))*(1-(0.887973*(1.+(0.0523821*Pt_jet2)/(1.+(0.0460876*Pt_jet2))))))'
#munu1 = '(MT_uv>70)*(MT_uv<110)*((((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)*1.0 + (((CISV_jet1>0.5426)*(CISV_jet2<0.5426))==1)*(1-(0.887973*(1.+(0.0523821*Pt_jet1))/(1.+(0.0460876*Pt_jet1)))) + (((CISV_jet1<0.5426)*(CISV_jet2>0.5426))==1)*(1-(0.887973*(1.+(0.0523821*Pt_jet2))/(1.+(0.0460876*Pt_jet2)))) + (((CISV_jet1>0.5426)+(CISV_jet2>0.5426))>1)*(1-(0.887973*(1.+(0.0523821*Pt_jet1))/(1.+(0.0460876*Pt_jet1))))*(1-(0.887973*(1.+(0.0523821*Pt_jet2)/(1.+(0.0460876*Pt_jet2))))))'


# (1 btagged jet)*w(1|1) + (2 btagged jets)*[w(1|2)+w(2|2)]
#munu2 = '(MT_uv>70)*(MT_uv<110)*((((CISV_jet1>0.8484)+(CISV_jet2>0.8484))==1)*(0.561694*((1.+(0.31439*(Pt_jet1*(CISV_jet1>0.8484)+Pt_jet2*(CISV_jet2>0.8484))))/(1.+(0.17756*(Pt_jet1*(CISV_jet1>0.8484)+Pt_jet2*(CISV_jet2>0.8484))))))+(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>1)*((0.561694*((1.+(0.31439*Pt_jet1))/(1.+(0.17756*(Pt_jet1)))))+(0.561694*((1.+(0.31439*Pt_jet2))/(1.+(0.17756*(Pt_jet2)))))-(0.561694*((1.+(0.31439*Pt_jet1))/(1.+(0.17756*(Pt_jet1)))))*(0.561694*((1.+(0.31439*Pt_jet2))/(1.+(0.17756*(Pt_jet2)))))))'


munu1Data =  '(MT_uv>70)*(MT_uv<110)*(CISV_jet1<0.5426)*(CISV_jet2<0.5426)'
munu2Data =  '(MT_uv>70)*(MT_uv<110)*(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>0)'
#These don't have explicit btag requirements, only SF
munu1 = '(MT_uv>70)*(MT_uv<110)*((1-(CISV_jet1>0.5426)*0.887973*((1.+(0.0523821*Pt_jet1))/(1.+(0.0460876*Pt_jet1))))*(1-(CISV_jet2>0.5426)*0.887973*((1.+(0.0523821*Pt_jet2))/(1.+(0.0460876*Pt_jet2)))))'
munu2 = '(MT_uv>70)*(MT_uv<110)*(1-(1-(CISV_jet1>0.8484)*0.561694*((1.+(0.31439*Pt_jet1))/(1.+(0.17756*Pt_jet1))))*(1-(CISV_jet2>0.8484)*0.561694*((1.+(0.31439*Pt_jet2))/(1.+(0.17756*Pt_jet2)))))'



#this uses jet count splitting
#munu1Data =  '(MT_uv>70)*(MT_uv<110)*(JetCount<4)'
#munu1 =  '(MT_uv>70)*(MT_uv<110)*(JetCount<4)'
#munu2Data =  '(MT_uv>70)*(MT_uv<110)*(JetCount>=4)'
#munu2 =  '(MT_uv>70)*(MT_uv<110)*(JetCount>=4)'

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
	#emu_id_eff = 0.496644871013
	#emu_id_eff = 0.586505470035 #NLO vv
	#emu_id_eff = 0.57926678173 #eta-binned muon ID/ISO SF
	emu_id_eff = 0.607308652332 #no top-pt reweighting
#emu_id_eff_err = 0.00270930206375 #HEEP tag not cuts - NLO vv
#emu_id_eff_err = 0.00267688208321#eta-binned muon ID/ISO SF
emu_id_eff_err = 0.00276041064762
# Next are the PDF uncertainties. 
pdf_MASS   =[ 200, 250, 300 , 350 , 400 , 450 , 500 , 550 , 600 , 650 , 700 , 750 , 800 , 850 , 900 , 950 , 1000 , 1050 , 1100 , 1150 , 1200 , 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000]               
pdf_MASS_displaced = [ 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200 ]
pdf_MASS_displaced_extended = [ 100, 125, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200 ]

pdf_uvjj_QCD = [1.06,1.06,1.06,1.46,2.3,3.67,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72]
pdf_uvjj_WJets = [1.06,1.06,1.06,1.46,2.3,3.67,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72,4.72]
pdf_uvjj_sTop = [8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78,8.78]
pdf_uvjj_TTBar = [2.18,2.18,2.18,3.54,5.16,6.33,7.34,10.01,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36,14.36]
pdf_uvjj_ZJets = [2.98,2.98,2.98,3.15,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49,3.49]
pdf_uvjj_VV = [3.35,3.35,3.35,3.41,3.62,3.73,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03,4.03]

pdf_uvjj_Signal = [0.35,0.35,0.35,0.53,0.83,0.83,0.83,0.83,0.83,0.83,0.83,0.84,1.21,1.21,1.62,1.62,2.22,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35,2.35]
#pdf_uujj_Signal = [2.0 for x in pdf_MASS]               
#pdf_uvjj_Signal = [3.0 for x in pdf_MASS]               


#2016
pdf_uujj_TTBar = [1.61,1.74,2.01,2.39,2.85,3.24,3.48,4.0,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22,4.22]
pdf_uujj_ZJets = [0.51,1.08,1.47,1.78,1.86,2.3,2.67,2.77,2.77,2.97,2.97,3.5,3.5,3.56,3.57,3.57,3.86,4.01,4.2,4.2,4.7,5.14,5.14,5.14,5.14,5.14,5.14,5.14,5.14,5.14,5.14,5.14,5.14,5.14,5.14,5.14,5.14]
pdf_uujj_QCD = [0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32,0.32]
pdf_uujj_VV = [1.54,1.57,1.85,2.46,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33]
pdf_uujj_sTop = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
pdf_uujj_WJets = [8.04,8.04,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05,9.05]


pdf_uvjj_TTBar = [0.66,1.01,1.4,1.79,2.17,2.67,2.68,3.21,3.47,3.47,3.47,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55,3.55]
pdf_uvjj_WJets = [1.16,1.25,2.1,4.02,4.21,6.58,9.27,9.27,10.29,16.62,24.26,38.25,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28,55.28]#74.27,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09,88.09]
pdf_uvjj_QCD = [0.12,0.14,0.14,0.14,0.14,0.19,0.24,0.46,0.47,0.47,0.49,0.54,0.61,0.69,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71,0.71]
pdf_uvjj_sTop = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
pdf_uvjj_VV = [1.64,1.69,1.75,1.86,1.95,2.19,2.29,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54,2.54]


# These are the total background uncertainties. They are used just to make some error bands on plots. 
totunc_uujj = [5.02, 5.28, 5.42, 5.8, 6.16, 6.81, 7.74, 8.72, 9.46, 9.47, 9.83, 10.5, 11.65, 9.13, 10.39, 12.17, 11.6, 12.58, 12.27, 14.08, 16.11, 16.09, 15.8, 12.07, 11.88, 11.03, 11.75, 11.75, 12.32, 11.75, 11.75, 11.75, 11.75, 11.75, 11.75, 11.75, 11.75]
totunc_uvjj = [6.62, 6.84, 6.38, 7.96, 8.19, 9.53, 12.13, 10.11, 10.15, 10.98, 11.25, 11.88, 14.74, 14.71, 12.98, 13.2, 13.39, 13.54, 13.79, 14.2, 14.33, 14.43, 14.15, 13.91, 13.66, 14.02, 14.01, 14.02, 13.96, 14.0, 13.6, 13.99, 13.97, 14.53, 14.51, 14.48, 13.41]

# Muon alignment Uncs, [uujj sig, uujj bg, uvjj sig, [uvjj bg] ] Only uvjj BG significantly varies with mass
alignmentuncs = [0.1,1.0,1.0,[0.027,0.027,0.027,0.072,0.205,0.672,1.268,2.592,3.632,4.518,6.698,6.355,5.131,9.615,12.364,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176,16.176]]

# Shape systematics in percent

#2016
shapesysvar_uujj_zjets  = [0.54, 2.48, 2.28, 2.58, 3.8, 4.13, 2.76, 3.04, 3.18, 3.26, 4.92, 4.79, 6.01, 7.04, 6.74, 5.07, 6.35, 5.83, 7.94, 7.13, 6.72, 8.86, 8.77, 10.59, 8.37, 7.83, 8.14, 9.08, 9.08, 9.08, 9.08, 9.08, 9.08, 9.08, 9.08, 9.08, 9.08, 9.08]
shapesysvar_uujj_ttjets = [1.23, 3.08, 4.5, 7.53, 11.1, 14.59, 16.1, 17.74, 19.91, 24.51, 27.37, 27.9, 23.69, 22.78, 25.15, 34.55, 31.99, 24.91, 24.91, 8.46, 8.46, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47, 8.47]
shapesysvar_uujj_vv = [7.99, 8.94, 9.31, 11.08, 11.92, 13.12, 13.03, 15.11, 16.95, 18.41, 17.74, 17.92, 19.19, 19.65, 20.35, 19.11, 20.21, 19.49, 18.68, 20.92, 22.11, 21.14, 20.63, 21.67, 21.67, 22.91, 25.29, 26.45, 26.45, 26.45, 26.45, 26.45, 26.45, 26.45, 26.45, 26.45, 26.45, 26.45]


shapesysvar_uvjj_wjets  = [1.23, 1.54, 1.67, 3.76, 3.94, 5.6, 8.37, 7.73, 8.33, 5.19, 5.78, 5.47, 8.73, 18.11, 23.3, 12.4, 24.98, 24.79, 29.56, 14.12, 16.29, 11.8, 16.47, 35.87, 65.54, 55.04, 17.6, 18.42, 22.98, 24.6, 13.22, 7.16, 4.7, 5.11, 5.23, 3.57, 3.51, 3.42]
shapesysvar_uvjj_ttjets = [0.68, 1.13, 2.16, 3.34, 4.42, 6.39, 8.25, 9.47, 10.08, 12.29, 14.62, 15.59, 17.25, 18.12, 21.74, 24.95, 20.29, 21.35, 20.86, 20.49, 14.14, 38.26, 36.05, 36.05, 36.05, 36.05, 38.26, 38.26, 38.26, 38.26, 38.26, 38.26, 41.15, 41.15, 41.15, 41.15, 41.15, 41.15]
shapesysvar_uvjj_vv = [11.89, 12.39, 12.57, 12.6, 12.42, 12.84, 14.4, 16.64, 16.68, 20.31, 20.82, 21.56, 22.58, 19.67, 20.49, 20.44, 21.09, 22.58, 22.27, 23.2, 25.65, 26.5, 26.26, 28.7, 29.97, 30.09, 30.18, 30.18, 30.18, 30.28, 30.28, 31.56, 30.75, 30.87, 29.9, 29.59, 29.65, 29.65]

############################################################
#####  The binning (const or variable) used for plots ######
############################################################

ptbinning = [53,75,105]
ptbinning2 = [53,75,105]
metbinning2 = [0,5]

stbinning = [200,225]
bosonbinning = [50,60,70,80,90,100,110,120]
bosonzoombinning_uujj_Z = [50,70,120]
bosonzoombinning_uujj_TT = [95,100]
metzoombinning_uujj_TT = [95,100]
metzoombinning_uujj_Z = [0,5,10,15,22,30,40,55,75,100]
	
bosonzoombinning_uvjj = [50,65,115]
bosonslopebinning_uvjj = [40,70,270]
massslopebining_uvjj = [25,100,600]

lqbinning = [50,60]
etabinning = [26,-2.6,2.6]
drbinning = [70,0,7]
phibinning = [26,-3.1416,3.1416]
dphibinning = [64,0,3.2]

for x in range(40):
	if ptbinning[-1] < 2000:
       		ptbinning.append(ptbinning[-1]+(ptbinning[-1] - ptbinning[-2])*1.2)
       	if ptbinning2[-1] < 700:
       		ptbinning2.append(ptbinning2[-1]+(ptbinning2[-1] - ptbinning2[-2])*1.2)
       	if metbinning2[-1] < 900:
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
	# for this, and make use of it. e.g. For systematic variations, we can run in batch instead
	# of running serially, which speeds things up.

	version_name = 'Testing_'+year+'_stockNano' # scriptflag
	#version_name = 'Testing_noQCD_14nov' # use sf tag above if this is the real folder
	os.system('mkdir Results_'+version_name) 

	MuMuOptCutFile = 'Results_'+version_name+'/OptLQ_uujjCuts_Smoothed_pol2cutoff.txt' # scriptflag
	MuNuOptCutFile = 'Results_'+version_name+'/OptLQ_uvjjCuts_Smoothed_pol2cutoff.txt' # scriptflag

	#################################################################################
        ##############     A FEW STANDARD PLOTTING ROUTINES AND STUDIES   ###############
	#################################################################################
	global preselectionmumu 
	global preselectionmumu_single 
	global preselectionmunu 

	# ====================================================================================================================================================== #
	# These are PDF uncertainty studies.
	# ====================================================================================================================================================== #

	if False:
		PDF4LHCUncStudy(MuMuOptCutFile,MuNuOptCutFile,version_name)
		PDF4LHCPlotsFromResultDict('Results_'+version_name+'/PDFVariationsDictionary.json',version_name)

	# ====================================================================================================================================================== #
	# The ttbar e-mu data-driven study. You only need to do this once, check the validation output, and use the scale-factor as global variable "emu_id_eff"
	# The scale-factor should be near 0.5
	# ====================================================================================================================================================== #
	if False:
		# TTBar Study

		# Some modifications to the ST and LQ mass binning
		bosonbinning = [50,60,70,80,90,100,110,120]
		for x in range(40):
			if bosonbinning[-1]<1000:
				bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.2 )
		bosonbinning = [round(x) for x in bosonbinning]
		stbinning = [280 ,300]
		lqbinning = [-20,0]
		for x in range(27):
			stbinning.append(stbinning[-1]+10+stbinning[-1]-stbinning[-2])
		for x in range(15):
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


	# ============================================================================================================================================================= #
	# This is the QCD study. It will make a couple plots, and test QCD contamination at final selection. We consider QCD negligible, but is good to test this once! #
	# ============================================================================================================================================================= #
	if False :
		qcdselectionmumu = '((Pt_muon1>53)*(Pt_muon2>53)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(DR_muon1muon2>0.3))'
		qcdselectionmunu = '((Pt_muon1>53)*(Pt_muon2<53)*(Pt_jet1>50)*(Pt_jet2>50)*(Pt_ele1<53)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5))'
		qcdselectionmunuVal = '((Pt_muon1>53)*(Pt_muon2<53)*(Pt_jet1>50)*(Pt_ele1<53)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5))'

		QCDStudy(qcdselectionmumu,qcdselectionmunu,qcdselectionmunuVal,MuMuOptCutFile,MuNuOptCutFile,NormalWeightMuMu,NormalWeightMuNu,version_name)


	# ============================================================================================================================================================= #
	# This is the VV study. It will make a couple plots, and compare amc@NLO with pythia
	# ============================================================================================================================================================= #
	if False :
		VVselectionmumu = '((Pt_muon1>53)*(Pt_muon2>53)*(Pt_jet1>50)*(Pt_jet2>50)*(St_uujj>300)*(DR_muon1muon2>0.3))'
		VVselectionmunu = '((Pt_muon1>53)*(Pt_muon2<53)*(Pt_jet1>50)*(Pt_jet2>50)*(Pt_ele1<53)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5))'

		VVStudy(VVselectionmumu,VVselectionmunu,MuMuOptCutFile,MuNuOptCutFile,NormalWeightMuMu,NormalWeightMuNu,version_name)


	# ====================================================================================================================================================== #
	# This is a testing plot routine for use with the new Displaced SUSY (l+b) long-lived samples
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
		exit()
		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1,0)
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, munu1, munu2,0)#fixme todo varying control sample MT window		

		# UUJJ plots at preselection, Note that putting 'TTBarDataDriven' in the name turns on the use of data-driven ttbar e-mu sample in place of MC
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[50,0,1000],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("M_jj","M^{jj} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','displaced',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
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
	# This is a plot routine for use with the new RPV susy samples
	# ====================================================================================================================================================== #
	if False :

		# Get Scale Factors
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1,0)
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, munu1,munu2,0)
		
		# UUJJ plots at preselection, Note that putting 'TTBarDataDriven' in the name turns on the use of data-driven ttbar e-mu sample in place of MC
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[50,0,1000],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven','susy',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
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
	if False :
		#global preselectionmumu 
		# Some modifications to the ST and LQ mass binning
		bjetbinning = [0,.05]
		for x in range(20):
			bjetbinning.append(bjetbinning[-1]+.05)
		stbinning = [280 ,300]
		lqbinning = [-20,0]
		for x in range(29):#was 22 then 27
			stbinning.append(stbinning[-1]+10+stbinning[-1]-stbinning[-2])
		for x in range(28):#was 22 then 28
			lqbinning.append(lqbinning[-1]+5+lqbinning[-1]-lqbinning[-2])
		stbinningTT = stbinning[1:20]
		stbinning = stbinning[1:]
		lqbinningTT = lqbinning[1:20]
		lqbinning = lqbinning[1:]
		bjetweightbinning = [10,.8,1.4]
		##bosonbinning = [50, 70, 105, 150,200,300,425, 600, 750, 900, 1105, 1330, 1575, 1840, 2125, 2430, 2590]
		##lqbinning = [50, 75, 105, 175, 280, 405, 550, 715, 900, 1105, 1330, 1575, 1840, 2125, 2430, 2590]
		#stbinning = [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000, 3500]#added 3500	
		##stbinning = [250,300,350,400,450,500,550,600,650,710, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000, 3500]#coarser binning for now	

		bosonbinning = [50,60,70,80,90,100,110,120]
		for x in range(55):
			if bosonbinning[-1]<1800:
				bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.075 )#was 1.2	       	
		bosonbinning = [round(x) for x in bosonbinning]

		#print lqbinning,stbinning
		# Get Scale Factors
		#munu1 = '((MT_uv>70)*(MT_uv<80)+(MT_uv>90)*(MT_uv<100)+(MT_uv>110)*(MT_uv<120)+(MT_uv>130)*(MT_uv<140))*(((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)*(2-0.887973*((1.+(0.0523821*Pt_jet1))/(1.+(0.0460876*Pt_jet1))))'
		#munu2 = '((MT_uv>80)*(MT_uv<90)+(MT_uv>100)*(MT_uv<110)+(MT_uv>120)*(MT_uv<130)+(MT_uv>140)*(MT_uv<150))*(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>=1)*(0.561694*((1.+(0.31439*Pt_jet1))/(1.+(0.17756*Pt_jet1))))'
		#munu1 = '(MT_uv>70)*(MT_uv<150)*(JetCount==2)'#*(DR_muon1jet1>1.0)'#(MuonCount<3)*(ElectronCount<1)'
		#munu2 = '(MT_uv>70)*(MT_uv<10)*(JetCount==3)'#*(DR_muon1jet1<1.0)'#(((MuonCount==3)+(ElectronCount==1))>0)'
		munu1plot = munu1#'(MT_uv>70)*(MT_uv<150)*(((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)*(2-0.887973*((1.+(0.0523821*Pt_jet1))/(1.+(0.0460876*Pt_jet1))))'
		munu2plot = munu2#'(MT_uv>70)*(MT_uv<150)*(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>=1)*(0.561694*((1.+(0.31439*Pt_jet1))/(1.+(0.17756*Pt_jet1))))'#*(CISV_jet1>CISV_jet2)+(0.901114+(1.40704e-05*(Pt_jet2)))*(CISV_jet2>0.8484)*(CISV_jet1<CISV_jet2))'
		#munu1 = '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)'
		#munu2 = '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)'
		[[Rz_uuj,Rz_uuj_err],[Rtt_uuj,Rtt_uuj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu_single, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)*(M_uu<250)',0,0)
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)*(M_uu<250)',0,0)
		#exit()
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = [[1.025,0.04],[1.147,0.019]]#TTBar MC, 2016 customNano
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = [[0.925,0.005],[1.000,0.023]]#TTBarDataDriven
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = [[0.977,0.052],[0.932,0.039]]#TTBarMC
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, munu1, munu2,0)#fixme todo varying control sample MT windoq
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = [[1.0,0.0],[1.0,0.0]]#TTBarMC, eta-driven SF, no top-pt reweight
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = [[0.934,0.01],[1.028,0.008]]#TTBarMC, eta-driven SF
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = [[0.9,0.009],[1.023,0.008]]#TTBarMC
		#CSVv2L	0.5426
		#CSVv2M	0.8484
		#CSVv2T	0.9535
		# Optionally, you can make an event-count table for each selection. Useful if testing a new optimization
		# We will do this later wtih full systematics for our set of stable cuts. 
		if False:
			
			MuMuOptCutFileTable = 'Results_'+version_name+'/OptLQ_uujjCuts_LQ1400_plus_st3000.txt' # scriptflag
			##MuNuOptCutFileTable = 'Results_'+version_name+'/OptLQ_uvjjCuts_Smoothed_pol2cutoff_table.txt' # scriptflag
			QuickTableTTDD(MuMuOptCutFileTable, preselectionmumu+"*(M_uu>100)",NormalWeightMuMu,Rz_uujj, Rw_uvjj,Rtt_uujj,0)#Use data-driven TTbar
			##QuickTable(MuMuOptCutFile, preselectionmumu+"*(M_uu>100)",NormalWeightMuMu,Rz_uujj, Rw_uvjj,Rtt_uujj,0)#Use MC-driven TTbar
			#QuickTable(MuNuOptCutFile, preselectionmunu,NormalWeightMuNu,Rz_uujj, Rw_uvjj,Rtt_uvjj,0)
			exit()
                #Signal efficiency*acceptance at final selection
		#MuMuOptCutFileEff = 'Results_Testing_2016_ReRecoWithH/OptLQ_uujjCuts_Smoothed_pol2cutoff.txt'
		#MuNuOptCutFileEff = 'Results_Testing_Summer16/OptLQ_uvjjCuts_Smoothed_pol2cutoff_no1500.txt'
		
		#MakeEfficiencyPlot(NormalDirectory,NormalWeightMuMu,MuMuOptCutFile,'LQuujj',version_name,1)
		#MakeEfficiencyPlot(NormalDirectory,NormalWeightMuNu,MuNuOptCutFile,'LQuvjj',version_name,1)
		#exit()

		# Here are a few plots which are zoomed-in on control regions. 
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonzoombinning_uujj_Z,preselectionmumu,NormalWeightMuMu,NormalDirectory,'controlzoom_ZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metzoombinning_uujj_Z,preselectionmumu+'*(M_uu>80)*(M_uu<100)*(Pt_miss<100)',NormalWeightMuMu,NormalDirectory,'controlzoom_ZRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonzoombinning_uujj_TT,preselectionmumu+'*(M_uu>100)*(Pt_miss>=100)',NormalWeightMuMu,NormalDirectory,'controlzoom_TTRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",metzoombinning_uujj_TT,preselectionmumu+'*(M_uu>100)*(Pt_miss>=100)',NormalWeightMuMu,NormalDirectory,'controlzoom_TTRegion','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'linscale','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		#MakeBasicPlot("CISV_jet1","Jet1 CSV score",bjetbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		#MakeBasicPlot("CISV_jet2","Jet2 CSV score",bjetbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount<3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		#MakeBasicPlot("CISV_jet1","Jet1 CSV score",bjetbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		#MakeBasicPlot("CISV_jet2","Jet2 CSV score",bjetbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<150)*(JetCount>3.5)',NormalWeightMuNu,NormalDirectory,'controlzoom_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		
		bosonzoombinning_uvjj = [40,70,150]
		##MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)*(((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)',NormalWeightMuNu,NormalDirectory,'controlzoom_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		##MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)*(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>=1)',NormalWeightMuNu,NormalDirectory,'controlzoom_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		#MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*'+munu1plot,NormalWeightMuNu,NormalDirectory,'controlzoom_WRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		#MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*'+munu2plot,NormalWeightMuNu,NormalDirectory,'controlzoom_TTRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		#MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonslopebinning_uvjj, preselectionmunu,NormalWeightMuNu,NormalDirectory,'controlzoom_SlopeRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		#MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",massslopebining_uvjj,preselectionmunu,NormalWeightMuNu,NormalDirectory,'controlzoom_SlopeRegion','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		"""
		# TTBar comparison between emu data and mumuMC
		[[Rz_uujj_emu,Rz_uujj_err_emu],[Rtt_uujj_emu,Rtt_uujj_err_emu]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0,0)
		
		MakeBasicPlotEMuMuMu("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinningTT,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("Pt_miss","E_{T}^{miss} [GeV]",[50,0,1000],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)	
		MakeBasicPlotEMuMuMu("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		MakeBasicPlotEMuMuMu("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_EMuMuMu','uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,'',version_name,1000)
		
		for lqmass in [200,500,600,700,900] :
			MakeBasicPlotEMuMuMu("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinningTT,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			
			MakeBasicPlotEMuMuMu("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("Pt_miss","E_{T}^{miss} [GeV]",[50,0,lqmass],preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)	
			MakeBasicPlotEMuMuMu("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlotEMuMuMu("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven_EMuMuMu'+str(lqmass),'uujj',Rz_uujj, Rz_uujj_emu,Rtt_uujj_emu,MuMuOptCutFile,version_name,lqmass)
		"""	
		# UUJJ plots at preselection, Note that putting 'TTBarDataDriven' in the name turns on the use of data-driven ttbar e-mu sample in place of MC
		
		#preselectionmumu += '*(M_uu>50)*(M_uu<80)'#fixme this is for control region checks
		MakeBasicPlot("DeepJet_jet1","Jet1 DeepJet score",bjetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DeepJet_jet2","Jet2 DeepJet score",bjetbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot(bTagSFmedium[1:],"B-Tag SF Weight",bjetweightbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Pt_jet1+Pt_jet2","p_{T}(jet_{1})+p_{T}(jet_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Pt_muon1+Pt_muon2","p_{T}(#mu_{1})+p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",[50,0,1000],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Phi_miss","#phi^{miss} [GeV]",[100,-3.1416,3.1416],preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)	
		MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("Phi_muon2","#phi(#mu_{2}) [GeV]",phibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)	
		MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("M_jj","M_{jj} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("MH_uujj","M_{#muj} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("M_uujjavg","M_{#muj}_{avg} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("M_uujj","M_{#mu#mujj} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		[[Rz_uujj_muCount,Rz_uujj_muCount_err],[Rtt_uujj_muCount,Rtt_uujj_muCount_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0,0)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj_muCount, Rw_uvjj,Rtt_uujj_muCount,'',version_name,1000)#removing TTBarDataDriven cause this makes weird muon count comparison
		MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)#removing TTBarDataDriven cause this makes weird muon count comparison
		MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DR_muon2jet1","#DeltaR(#mu_{2},j_{1})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DR_muon2jet2","#DeltaR(#mu_{2},j_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DPhi_muon1met","#Delta #phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DPhi_jet1met","#Delta#phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DPhi_jet2met","#Delta#phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DPhi_muon1jet1","#Delta#phi(#mu_{1},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DPhi_muon1jet2","#Delta#phi(#mu_{1},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DPhi_muon2jet1","#Delta#phi(#mu_{2},j_{1})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
		MakeBasicPlot("DPhi_muon2jet2","#Delta#phi(#mu_{2},j_{2})",dphibinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)

		# UVJJ plots at preselection
		
		stbinning = [280 ,300]
		lqbinning = [-20,0]
		for x in range(18):
			stbinning.append(stbinning[-1]+45+stbinning[-1]-stbinning[-2])
		for x in range(20):
			lqbinning.append(lqbinning[-1]+20+lqbinning[-1]-lqbinning[-2])
		stbinning = stbinning[1:]
		lqbinning = lqbinning[1:]
		bosonbinning = [50,60,70,80,90,100,110,120]
		for x in range(55):
			if bosonbinning[-1]<1600:
				bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.3 )#was 1.2	       	
		bosonbinning = [round(x) for x in bosonbinning]
		"""
		MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Phi_jet1","#phi(jet_{1}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Phi_jet2","#phi(jet_{2}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Phi_muon1","#phi(#mu_{1}) [GeV]",phibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("Phi_miss","#phi^{miss} [GeV]",[100,-3.1416,3.1416],preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("St_uvjj","S_{T}^{#mu#nujj} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("MT_uvjj","M_{T}^{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("MH_uvjj","M_{#muj} (lead jet only) [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("GoodVertexCount","N_{Vertices}",vbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("MuonCount","N_{#mu}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("ElectronCount","N_{e}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("DPhi_muon1met","#Delta#phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("DPhi_jet1met","#Delta#phi(j_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("DPhi_jet2met","#Delta#phi(j_{2},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("DR_muon1jet1","#DeltaR(#mu_{1},j_{1})",drbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("DPhi_muon1jet1","#Delta #phi(#mu,j_{1})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		MakeBasicPlot("DPhi_muon1jet2","#Delta #phi(#mu,j_{2})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,850)
		"""

		# Full Selection Plots
		for lqmass in [650,800,1000,1100,1200,1500]:
		#for lqmass in [600]:
			"""
			MakeBasicPlot("Pt_jet1+Pt_jet2","p_{T}(jet_{1})+p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_muon1+Pt_muon2","p_{T}(#mu_{1})+p_{T}(#mu_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			"""
			MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			#MakeBasicPlot("M_uujj1","M_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uujj2","M_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			"""
			MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("DR_muon1muon2","#DeltaR(#mu_{1},#mu_{2})",drbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Eta_muon2","#eta(#mu_{2}) [GeV]",etabinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDriven','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)	
			"""

			MakeBasicPlot("St_uvjj","S_{T}^{#mu#nujj} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("M_uvjj","M_{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			"""
			MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Eta_muon1","#eta(#mu_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Eta_jet1","#eta(jet_{1}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("Eta_jet2","#eta(jet_{2}) [GeV]",etabinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("DPhi_jet1met","#Delta#phi (j_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("DPhi_jet2met","#Delta#phi (j_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			MakeBasicPlot("DPhi_muon1met","#Delta#phi (#mu_{1},E_{T}^{miss})",dphibinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'final','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
			"""
		#fixme todo removing this
		os.system('echo Combining Figures; convert -density 800 Results_'+version_name+'/*png Results_'+version_name+'/AllPlots.pdf')



	# ====================================================================================================================================================== #
	# This is a plotting routine for PAS-style publication-quality plots
	# ====================================================================================================================================================== #

	if False:

		# Some modifications to the ST and LQ mass binning
		stbinning = [280 ,300]
		lqbinning = [-20,0]
		lqbinningPaper = [-20,0]
		for x in range(29):
			stbinning.append(stbinning[-1]+10+stbinning[-1]-stbinning[-2])
		for x in range(28):
			lqbinning.append(lqbinning[-1]+5+lqbinning[-1]-lqbinning[-2])
		for x in range(29):
			lqbinningPaper.append(lqbinningPaper[-1]+5+lqbinningPaper[-1]-lqbinningPaper[-2])
		stbinning = stbinning[1:]
		lqbinning = lqbinning[1:]
		lqbinningPaper = lqbinningPaper[1:]
		#stbinning = [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000, 3500]

		bosonbinning = [50,60,70,80,90,100,110,120]
		for x in range(40):
			if bosonbinning[-1]<1800:
				bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.2 )	       	
		bosonbinning = [round(x) for x in bosonbinning]


		#munu1 = '(MT_uv>70)*(MT_uv<110)*(((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)*(2-0.887973*((1.+(0.0523821*Pt_jet1))/(1.+(0.0460876*Pt_jet1))))'
		#munu2 = '(MT_uv>70)*(MT_uv<110)*(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>=1)*(0.561694*((1.+(0.31439*Pt_jet1))/(1.+(0.17756*Pt_jet1))))'#*(CISV_jet1>CISV_jet2)+(0.901114+(1.40704e-05*(Pt_jet2)))*(CISV_jet2>0.8484)*(CISV_jet1<CISV_jet2))'
		# Get Scale Factors
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1,0)
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, munu1,munu2,0)
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = [[0.925,0.005],[1.000,0.023]]
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = [[0.9,0.009],[1.023,0.008]]

		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = [[0.983,0.006],[1.000,0.023]]#TTBarDataDriven, eta-driven SF
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = [[0.936,0.01],[1.028,0.008]]#TTBarMC, eta-driven SF
		
		# Here are a few plots which are zoomed-in on control regions. 
		#MakeBasicPlot("M_uu","M_{#mu#mu} [GeV]",[20,80,100],preselectionmumu,NormalWeightMuMu,NormalDirectory,'controlzoomPASTTBarDataDriven_ZRegiontagfree','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
		bosonzoombinning_uvjj = [20,70,110]
		#MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*'+munu1,NormalWeightMuNu,NormalDirectory,'controlzoomPAS_WRegiontagfree','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
		#MakeBasicPlot("MT_uv","M_{T}^{#mu#nu} [GeV]",bosonzoombinning_uvjj,preselectionmunu+'*'+munu2,NormalWeightMuNu,NormalDirectory,'controlzoomPAS_TTRegiontagfree','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		# The two flags are for regular plots, and tagfree plots (plots that don't say CMS Preliminary - for notes or thesis)
		#for flag in ['','tagfree']:
		
		for flag in ['tagfree']:

#			# Preselection plots in the UUJJ channel in the PAS style (no subplot)
#			MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
#			#MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
#			#MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
#			#MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
#			#MakeBasicPlot("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
#			MakeBasicPlot("M_uu","m_{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
#			#MakeBasicPlot("MH_uujj","m_{#muj} (lead jet combo) [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
#			#MakeBasicPlot("M_uujj1","m_{#muj}_{1} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
#			MakeBasicPlot("M_uujj2","m_{#muj}^{min} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
#			#MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardPAS_TTBarDataDriven'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
#
#			# Preselection plots in the UVJJ channel in the PAS style (no subplot)			
#			#MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
#			#MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
#			#MakeBasicPlot("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
#			#MakeBasicPlot("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
#			MakeBasicPlot("St_uvjj","S_{T}^{#mu#nujj} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
#			MakeBasicPlot("MT_uv","m_{T}^{#mu#nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
#			#MakeBasicPlot("MT_uvjj","m_{T}^{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			#MakeBasicPlot("M_uvjj","m_{#muj} [GeV]",lqbinningPaper,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
#			#MakeBasicPlot("MH_uvjj","m_{#muj} (lead jet only) [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
#			#MakeBasicPlot("JetCount","N_{jet}",nbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standardPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			
			# Full Selection Plots in the PAS style
			#for lqmass in [200,300,500,650,800,900,1000,1100,1200,1300,1400,1500,1600]:
			for lqmass in [1100,1400]:
				stbinningPaper = stbinning[9:]
				lqbinningPaper = lqbinning[9:]
				lqbinningPaperuujj = lqbinning[10:]
				stbinningPaper = stbinningPaper[::2]
				lqbinningPaper = lqbinningPaper[::2]
				lqbinningPaper.append(lqbinningPaper[-1]+(lqbinningPaper[-1]-lqbinningPaper[-2]))
				#MakeBasicPlot("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinningPaper,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDrivenPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
				##MakeBasicPlot("M_uu","M^{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDrivenPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uujj2","m_{#muj}^{min} [GeV]",lqbinningPaperuujj,preselectionmumu,NormalWeightMuMu,NormalDirectory,'finalTTBarDataDrivenPAS'+flag,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,MuMuOptCutFile,version_name,lqmass)
				#
				#MakeBasicPlot("St_uvjj","S_{T}^{#mu#nujj} [GeV]",stbinningPaper,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
				##MakeBasicPlot("MT_uv","m_{T}^{#mu#nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)
				MakeBasicPlot("M_uvjj","m_{#muj} [GeV]",lqbinningPaper,preselectionmunu,NormalWeightMuNu,NormalDirectory,'finalPAS'+flag,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,MuNuOptCutFile,version_name,lqmass)


	# ====================================================================================================================================================== #
	# This runs a "FullAnalysis" - i.e. produces tables with full systematics included. 
	# ====================================================================================================================================================== #

	# You can run this to make the full set of tables needed to construct the higgs card. This takes a long time!
	# Alternatively, you can run > python SysBatcher.py --launch to do each table in a separate batch job
	# When done, proceed to the next step to make higgs limit cards
	if False : 
		#FullAnalysis(MuMuOptCutFile, preselectionmumu,preselectionmunu,NormalDirectory,NormalWeightMuMu,'TTBarDataDriven') # scriptflag 
		FullAnalysis(MuMuOptCutFile, preselectionmumu,preselectionmunu,NormalDirectory,NormalWeightMuMu,'normal') # scriptflag 
		FullAnalysis(MuNuOptCutFile, preselectionmumu,preselectionmunu,NormalDirectory,NormalWeightMuNu,'normal')  # scriptflag
	if False :
 		uujjcardfiles = MuMuOptCutFile.replace('.txt','_systable*.txt')
		uvjjcardfiles = MuNuOptCutFile.replace('.txt','_systable*.txt')

		uujjcards = ParseFinalCards(uujjcardfiles)
		uvjjcards = ParseFinalCards(uvjjcardfiles)
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
			[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactorsMod( NormalWeightMuNu_mod+'*'+preselectionmunu_mod, NormalDirectory, munu1,munu2,sample,0)

			MakeBasicPlot("M_uvjj","m_{#muj} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("MT_uv","m_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2}) "+sample,drbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sample,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sysmethod in ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','PUup','PUdown']:
			preselectionmunu_mod = ModSelection(preselectionmunu,sysmethod,MuNuOptCutFile)
			NormalWeightMuNu_mod = ModSelection(NormalWeightMuNu,sysmethod,MuNuOptCutFile)

			Rz_uujj = 1.0
			[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu_mod+'*'+preselectionmunu_mod, NormalDirectory,munu1,munu2,0)
			
			MakeBasicPlot(ModSelection("M_uvjj",sysmethod,MuNuOptCutFile),"m_{#muj} [GeV]",lqbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sysmethod,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)
			MakeBasicPlot(ModSelection("MT_uv",sysmethod,MuNuOptCutFile),"m_{T}^{#mu #nu} [GeV]",bosonbinning,preselectionmunu_mod,NormalWeightMuNu_mod,NormalDirectory,'standard_sys'+sysmethod,'uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sample in ['ScaleUp','ScaleDown','MatchUp','MatchDown']:
			Rw_uvjj = 1.0
			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactorsMod( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',sample,0)

			MakeBasicPlot("Pt_jet1","p_{T}(jet_{1}) [GeV] "+sample,ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardTTBarDataDriven_sys'+sample,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot("Pt_jet2","p_{T}(jet_{2}) [GeV] "+sample,ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standardTTBarDataDriven_sys'+sample,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			rescale_string = MakeBasicPlot("DR_muon1jet2","#DeltaR(#mu_{1},j_{2})",drbinning,preselectionmunu+'*(MT_uv>70)*(MT_uv<110)',NormalWeightMuNu,NormalDirectory,'standard_rescaletest_pre','uvjj',Rz_uujj, Rw_uvjj,Rtt_uvjj,'',version_name,500)

		for sysmethod in ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','PUup','PUdown']:
			preselectionmumu_mod = ModSelection(preselectionmumu,sysmethod,MuMuOptCutFile)
			NormalWeightMuMu_mod = ModSelection(NormalWeightMuMu,sysmethod,MuMuOptCutFile)

			Rw_uvjj = 1.0

			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu_mod+'*'+preselectionmumu_mod, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1,0)

			MakeBasicPlot(ModSelection("Pt_jet1",sysmethod,MuMuOptCutFile),"p_{T}(jet_{1}) [GeV] "+sysmethod,ptbinning,preselectionmumu_mod,NormalWeightMuMu_mod,NormalDirectory,'standard_sys'+sysmethod,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)
			MakeBasicPlot(ModSelection("Pt_jet2",sysmethod,MuMuOptCutFile),"p_{T}(jet_{2}) [GeV] "+sysmethod,ptbinning,preselectionmumu_mod,NormalWeightMuMu_mod,NormalDirectory,'standard_sys'+sysmethod,'uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,500)



	# ====================================================================================================================================================== #
	# This is for Optimization of cuts
	# ====================================================================================================================================================== #

	if True :
		doLongLived = False
		# Get Scale Factors
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0,0)
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, munu1, munu2,0)#fixme todo varying control sample MT window

		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = [[1.025,0.04],[1.147,0.019]]#TTBar MC, 2016 customNano
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = [[0.934,0.01],[0.984,0.008]]#TTBarMC, eta-driven SF, no top-pt reweight
		[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = [[1.0,0.0],[1.0,0.0]]
		[[Rz_uuj,Rz_uuj_err],[Rtt_uuj,Rtt_uuj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu_single, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)*(M_uu<250)',0,0)
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)*(M_uu<250)',0,0)




		scaleFactors = [Rz_uujj,Rtt_uujj,Rw_uvjj]
		if not doLongLived :
			MuMuOptTestCutFile = 'Results_'+version_name+'/OptLQ_uujjCuts_Smoothed_pol2cutoff.txt'
			variableSpace = ['M_uu:25:100:1000','St_uujj:100:300:2500','M_uujj2:25:100:1000']
			OptimizeCuts3D(variableSpace,preselectionmumu,NormalWeightMuMu,version_name,scaleFactors,'','uujj')
                        #
                        #scaleFactors = [Rz_uuj,Rtt_uuj,Rw_uvj]
			#variableSpace = ['M_uu:25:100:1000','St_uuj:100:300:2500','M_uuj1:25:100:1000']
			#OptimizeCuts3D(variableSpace,preselectionmumu_single,NormalWeightMuMu,version_name,scaleFactors,'','uuj')
                        #
			#scaleFactors = [Rz_uujj,Rtt_uvjj,Rw_uvjj]
			#variableSpace = ['MT_uv:50:150:1200','St_uvjj:100:300:3000','M_uvjj:50:100:900',]
		    #OptimizeCuts3D(variableSpace,preselectionmunu,NormalWeightMuNu,version_name,scaleFactors,'','uvjj')
		#Now we can do it for long-lived samples
		if doLongLived :
			scaleFactors = [Rz_uujj,Rtt_uujj,Rw_uvjj]
			variableSpace = ['M_uu:15:100:500','St_uujj:15:300:1800','M_uujj2:15:100:900',]
			OptimizeCuts3D(variableSpace,preselectionmumu,NormalWeightMuMu,version_name,scaleFactors,'','BLuujj')
	if True:
 		makeOptPlotForPAS(MuMuOptCutFile,'uujj',version_name,0)
		#makeOptPlotForPAS(MuNuOptCutFile,'uvjj',version_name,1)

	# ====================================================================================================================================================== #
	# This is for shape systematics
	# ====================================================================================================================================================== #

	if False :
		MuMuOptTestCutFile = 'Results_'+version_name+'/OptLQ_uujjCuts_Smoothed_pol2cutoff.txt'
		MuNuOptTestCutFile = 'Results_'+version_name+'/OptLQ_uvjjCuts_Smoothed_pol2cutoff.txt'
		# Get Scale Factors
		#[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0,1)
		#[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory, munu1,munu2,1)#fixme todo varying control sample MT window
		
		ShapeSystematic('uujj',NormalWeightMuMu,preselectionmumu,MuMuOptTestCutFile)
		ShapeSystematic('uvjj',NormalWeightMuNu,preselectionmunu,MuNuOptTestCutFile)


	# ====================================================================================================================================================== #
	# This is for scale factor studies
	# ====================================================================================================================================================== #

	if False:
		
		mtCR = '*(MT_uv>70)*(MT_uv<110)'
		mtSR = '*(((MT_uv>50)*(MT_uv<70)+(MT_uv>110))>0)'
		preselectionmunu = '((Pt_muon1>53)*(Pt_muon2<53)*(Pt_miss>55)*(Pt_jet1>50)*(Pt_jet2>50)*(Pt_ele1<53)*(St_uvjj>300)*(DPhi_muon1met>0.8)*(DPhi_jet1met>0.5))'
		NormalWeightMuNu = str(lumi)+'*weight_central'+singlemuHLT+singleMuIdScale+singleMuIsoScale+trackerHIP1

		finalSels=['','*((M_uvjj>100)*(St_uvjj>340))','*((M_uvjj>150)*(St_uvjj>415))','*((M_uvjj>195)*(St_uvjj>490))','*((M_uvjj>240)*(St_uvjj>565))','*((M_uvjj>280)*(St_uvjj>640))','*((M_uvjj>320)*(St_uvjj>715))','*((M_uvjj>360)*(St_uvjj>790))','*((M_uvjj>400)*(St_uvjj>865))','*((M_uvjj>435)*(St_uvjj>935))','*((M_uvjj>470)*(St_uvjj>1010))','*((M_uvjj>500)*(St_uvjj>1085))','*((M_uvjj>530)*(St_uvjj>1155))','*((M_uvjj>560)*(St_uvjj>1225))','*((M_uvjj>590)*(St_uvjj>1295))','*((M_uvjj>615)*(St_uvjj>1370))','*((M_uvjj>640)*(St_uvjj>1440))','*((M_uvjj>660)*(St_uvjj>1505))','*((M_uvjj>685)*(St_uvjj>1575))','*((M_uvjj>700)*(St_uvjj>1645))','*((M_uvjj>720)*(St_uvjj>1715))','*((M_uvjj>735)*(St_uvjj>1780))','*((M_uvjj>750)*(St_uvjj>1850))','*((M_uvjj>765)*(St_uvjj>1915))','*((M_uvjj>765)*(St_uvjj>1980))','*((M_uvjj>765)*(St_uvjj>2050))','*((M_uvjj>765)*(St_uvjj>2115))','*((M_uvjj>765)*(St_uvjj>2180))','*((M_uvjj>765)*(St_uvjj>2245))','*((M_uvjj>765)*(St_uvjj>2305))','*((M_uvjj>765)*(St_uvjj>2370))','*((M_uvjj>765)*(St_uvjj>2435))','*((M_uvjj>765)*(St_uvjj>2495))','*((M_uvjj>765)*(St_uvjj>2560))','*((M_uvjj>765)*(St_uvjj>2620))','*((M_uvjj>765)*(St_uvjj>2680))','*((M_uvjj>765)*(St_uvjj>2745))','*((M_uvjj>765)*(St_uvjj>2805))']

		
		selectionsCR = [preselectionmunu+'*'+NormalWeightMuNu + mtCR + x for x in finalSels]
		selectionsSR = [preselectionmunu+'*'+NormalWeightMuNu + mtSR + x for x in finalSels]
		for x in range(len(selectionsCR)):
			if x!=0:
				print 200+float(x-1)*50
			print selectionsCR[x]
			print selectionsSR[x],'\n'
			W1 = QuickIntegral(t_WJets,selectionsCR[x],1.0)
			#T1 = QuickIntegral(t_TTBar,selectionsCR[x],1.0)
			#s1 = QuickIntegral(t_SingleTop,selectionsCR[x],1.0)
			#z1 = QuickIntegral(t_ZJets,selectionsCR[x],1.0)
			#v1 = QuickIntegral(t_DiBoson,selectionsCR[x],1.0)
			
			W2 = QuickIntegral(t_WJets,selectionsSR[x],1.0)
			#T2 = QuickIntegral(t_TTBar,selectionsSR[x],1.0)
			#s2 = QuickIntegral(t_SingleTop,selectionsSR[x],1.0)
			#z2 = QuickIntegral(t_ZJets,selectionsSR[x],1.0)
			#v2 = QuickIntegral(t_DiBoson,  selectionsSR[x],1.0)
			print 'x=',x,'CR=',W1,'SR=',W2,'CR/SR=',W2[0]/W1[0],'+-',(1/W1[0])*math.sqrt((W2[0]*W2[0]*W1[1]*W1[1]/(W1[0]*W1[0]))+(W2[1]*W2[1]))

		exit()
		print 'Nominal uujj:'
		[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1,0)
		for stRange in [['300','500'],['500','750'],['750','1250'],['1250','99999']]:
			stCut = '*(St_uujj>'+stRange[0]+')*(St_uujj<'+stRange[1]+')'
			print '*********',stCut
			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu+stCut, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1,1)
		for mujRange in [['0','250'],['250','750'],['750','99999']]:
			mujCut = '*(M_uujj2>'+mujRange[0]+')*(M_uujj2<'+mujRange[1]+')'
			print '*********',mujCut
			[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu+mujCut, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1,1)
		for stRange in [['300','500'],['500','750'],['750','99999']]:
			stCut = '*(St_uvjj>'+stRange[0]+')*(St_uvjj<'+stRange[1]+')'
			print '*********',stCut
			[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu+stCut, NormalDirectory, munu1, munu2,1)

	# ====================================================================================================================================================== #
	# This is for  spurious events
	# ====================================================================================================================================================== #

	if False:
		tmpfile = TFile("tmp.root","RECREATE")
		t_SingleMuData2 = t_SingleMuData.CopyTree(preselectionmumu)
		NN = t_SingleMuData2.GetEntries()
		for n in range(NN):
			if n%1000 ==0:
				print n,'of',NN
			t_SingleMuData2.GetEntry(n)
			st = t_SingleMuData2.St_uujj
			if st>5000:
			#if t_SingleMuData2.St_uvjj>1505 and t_SingleMuData2.MT_uv>540 and t_SingleMuData2.M_uvjj>660 and t_SingleMuData2.Pt_muon1>800:
				print 'run / lumi / event:',int(t_SingleMuData2.run_number),'/',int(t_SingleMuData2.lumi_number),'/',int(t_SingleMuData2.event_number)
				print 'St_uujj      ',t_SingleMuData2.St_uujj
				print 'St_uvjj      ',t_SingleMuData2.St_uvjj
				print 'Pt_muon1     ',t_SingleMuData2.Pt_muon1
				#print 'Pt_muon1_raw ',t_SingleMuData2.Pt_muon1_noTuneP
				#if (t_SingleMuData2.Pt_muon1>0):
				#	print 'raw/tuneP 1  ',t_SingleMuData2.Pt_muon1_noTuneP/t_SingleMuData2.Pt_muon1 
				#else: print 'raw/tuneP 1  ','n/a'
				print 'Pt_muon2     ',t_SingleMuData2.Pt_muon2
				#print 'Pt_muon2_raw ',t_SingleMuData2.Pt_muon2_noTuneP
				#if (t_SingleMuData2.Pt_muon2>0):
				#	print 'raw/tuneP 2  ',t_SingleMuData2.Pt_muon2_noTuneP/t_SingleMuData2.Pt_muon2
				#else: print 'raw/tuneP 2  ','n/a'
				print 'Eta_muon1    ',t_SingleMuData2.Eta_muon1
				print 'Eta_muon2    ',t_SingleMuData2.Eta_muon2
				print 'Phi_muon1    ',t_SingleMuData2.Phi_muon1
				print 'Phi_muon2    ',t_SingleMuData2.Phi_muon2
				print 'Pt_jet1      ',t_SingleMuData2.Pt_jet1
				print 'Pt_jet2      ',t_SingleMuData2.Pt_jet2
				print 'Eta_jet1     ',t_SingleMuData2.Eta_jet1
				print 'Eta_jet2     ',t_SingleMuData2.Eta_jet2
				print 'Phi_jet1     ',t_SingleMuData2.Phi_jet1
				print 'Phi_jet2     ',t_SingleMuData2.Phi_jet2
				print 'Pt_miss      ',t_SingleMuData2.Pt_miss
				print 'Phi_miss     ',t_SingleMuData2.Phi_miss
				print 'M_uu         ',t_SingleMuData2.M_uu
				print 'MT_uv         ',t_SingleMuData2.MT_uv
				print 'M_uujj1      ',t_SingleMuData2.M_uujj1
				print 'M_uujj2      ',t_SingleMuData2.M_uujj2
				print 'M_uvjj      ',t_SingleMuData2.M_uvjj
				print 'DR_muon1muon2',t_SingleMuData2.DR_muon1muon2
				print 'DPhi_muon1met',t_SingleMuData2.DPhi_muon1met
				print 'DPhi_jet1met ',t_SingleMuData2.DPhi_jet1met
				print 'DPhi_jet2met ',t_SingleMuData2.DPhi_jet2met


	# ====================================================================================================================================================== #
	# This is for the final event count plot
	# ====================================================================================================================================================== #
	if False:
		isPAS=True
		c1 = TCanvas("c1","",800,550)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		gStyle.SetOptStat(0)
		gStyle.SetErrorX(0);
		pad1.cd()
		pad1.SetLogy(1)
		#masses=pdf_MASS
		#print masses
		#masses.append(2025)
		sig = TH1F("sig","LQ signal;m_{LQ} [GeV];Final selection event yield",37,175,2025)
		wjets = TH1F("wjets","W+jets;m_{LQ} [GeV];Final selection event yield",37,175,2025)
		zjets = TH1F("zjets","Z+jets;m_{LQ} [GeV];Final selection event yield",37,175,2025)
		ttbar = TH1F("ttbar","t#overline{t}+jets;m_{LQ} [GeV];Final selection event yield",37,175,2025)
		VV = TH1F("vv","LQ signal;m_{LQ} [GeV];Final selection event yield",37,175,2025)
		other = TH1F("other","Other Background;m_{LQ} [GeV];Final selection event yield",37,175,2025)
		totBG = TH1F("totBG","Total Background;m_{LQ} [GeV];Final selection event yield",37,175,2025)
		data = TH1F("data","Data;m_{LQ} [GeV];Final selection event yield",37,175,2025)
		data.Sumw2()
		#data.SetBinErrorOption(TH1.kPoisson)
		data.SetLineWidth(2)
		data.SetMarkerSize(2)
                #uujj
		channel = 'uujj'
		sig.SetBinContent(1, 531700 )
		sig.SetBinError(1, 4700  )
		zjets.SetBinContent(1, 2973.2 )
		zjets.SetBinError(1, 7.4  )
		ttbar.SetBinContent(1, 5467 )
		ttbar.SetBinError(1, 56  )
		VV.SetBinContent(1, 369 )
		VV.SetBinError(1, 2.0  )
		other.SetBinContent(1, 519.4 )
		other.SetBinError(1, 9.6  )
		totBG.SetBinContent(1, 9328 )
		totBG.SetBinError(1,447.643831634)
		data.SetBinContent(1, 9317 )
		#data.SetBinError(1,96.5246082613)
		sig.SetBinContent(2, 232900 )
		sig.SetBinError(2, 1800  )
		zjets.SetBinContent(2, 1675 )
		zjets.SetBinError(2, 5.1  )
		ttbar.SetBinContent(2, 2972 )
		ttbar.SetBinError(2, 41  )
		VV.SetBinContent(2, 241.5 )
		VV.SetBinError(2, 1.7  )
		other.SetBinContent(2, 324.6 )
		other.SetBinError(2, 7.5  )
		totBG.SetBinContent(2, 5213 )
		totBG.SetBinError(2,253.503451653)
		data.SetBinContent(2, 5102 )
		#data.SetBinError(2,71.4282857137)
		sig.SetBinContent(3, 100460 )
		sig.SetBinError(3, 760  )
		zjets.SetBinContent(3, 792.9 )
		zjets.SetBinError(3, 3.0  )
		ttbar.SetBinContent(3, 1298 )
		ttbar.SetBinError(3, 26  )
		VV.SetBinContent(3, 138.9 )
		VV.SetBinError(3, 1.3  )
		other.SetBinContent(3, 189.2 )
		other.SetBinError(3, 5.7  )
		totBG.SetBinContent(3, 2419 )
		totBG.SetBinError(3,120.074976577)
		data.SetBinContent(3, 2360 )
		#data.SetBinError(3,48.579831206)
		sig.SetBinContent(4, 46160 )
		sig.SetBinError(4, 340  )
		zjets.SetBinContent(4, 387.9 )
		zjets.SetBinError(4, 1.8  )
		ttbar.SetBinContent(4, 538 )
		ttbar.SetBinError(4, 16  )
		VV.SetBinContent(4, 81.1 )
		VV.SetBinError(4, 1.0  )
		other.SetBinContent(4, 98 )
		other.SetBinError(4, 4.1  )
		totBG.SetBinContent(4, 1105 )
		totBG.SetBinError(4,59.4810894319)
		data.SetBinContent(4, 1113 )
		#data.SetBinError(4,33.3616546352)
		sig.SetBinContent(5, 22610 )
		sig.SetBinError(5, 160  )
		zjets.SetBinContent(5, 202.4 )
		zjets.SetBinError(5, 1.2  )
		ttbar.SetBinContent(5, 237 )
		ttbar.SetBinError(5, 10  )
		VV.SetBinContent(5, 51.89 )
		VV.SetBinError(5, 0.84  )
		other.SetBinContent(5, 55.2 )
		other.SetBinError(5, 3.1  )
		totBG.SetBinContent(5, 546 )
		totBG.SetBinError(5,31.0161248385)
		data.SetBinContent(5, 572 )
		#data.SetBinError(5,23.9165214862)
		sig.SetBinContent(6, 12039 )
		sig.SetBinError(6, 86  )
		zjets.SetBinContent(6, 131.72 )
		zjets.SetBinError(6, 0.92  )
		ttbar.SetBinContent(6, 120.7 )
		ttbar.SetBinError(6, 7.2  )
		VV.SetBinContent(6, 32.19 )
		VV.SetBinError(6, 0.66  )
		other.SetBinContent(6, 31.8 )
		other.SetBinError(6, 2.3  )
		totBG.SetBinContent(6, 316.4 )
		totBG.SetBinError(6,19.7618318989)
		data.SetBinContent(6, 299 )
		#data.SetBinError(6,17.2916164658)
		sig.SetBinContent(7, 6672 )
		sig.SetBinError(7, 48  )
		zjets.SetBinContent(7, 79 )
		zjets.SetBinError(7, 0.65  )
		ttbar.SetBinContent(7, 54.1 )
		ttbar.SetBinError(7, 4.6  )
		VV.SetBinContent(7, 20.92 )
		VV.SetBinError(7, 0.53  )
		other.SetBinContent(7, 20.2 )
		other.SetBinError(7, 1.9  )
		totBG.SetBinContent(7, 174.2 )
		totBG.SetBinError(7,12.1741529479)
		data.SetBinContent(7, 147 )
		#data.SetBinError(7,12.124355653)
		sig.SetBinContent(8, 3848 )
		sig.SetBinError(8, 27  )
		zjets.SetBinContent(8, 51.95 )
		zjets.SetBinError(8, 0.5  )
		ttbar.SetBinContent(8, 26.1 )
		ttbar.SetBinError(8, 3.0  )
		VV.SetBinContent(8, 14.43 )
		VV.SetBinError(8, 0.46  )
		other.SetBinContent(8, 13.1 )
		other.SetBinError(8, 1.5  )
		totBG.SetBinContent(8, 105.6 )
		totBG.SetBinError(8,8.3258633186)
		data.SetBinContent(8, 78 )
		#data.SetBinError(8,8.83176086633)
		sig.SetBinContent(9, 2328 )
		sig.SetBinError(9, 16  )
		zjets.SetBinContent(9, 34.71 )
		zjets.SetBinError(9, 0.39  )
		ttbar.SetBinContent(9, 12.9 )
		ttbar.SetBinError(9, 1.9  )
		VV.SetBinContent(9, 10.05 )
		VV.SetBinError(9, 0.38  )
		other.SetBinContent(9, 9.44 )
		other.SetBinError(9, 1.29  )
		totBG.SetBinContent(9, 67.1 )
		totBG.SetBinError(9,5.72712842531)
		data.SetBinContent(9, 44 )
		#data.SetBinError(9,6.63324958071)
		sig.SetBinContent(10, 1461 )
		sig.SetBinError(10, 10  )
		zjets.SetBinContent(10, 26.03 )
		zjets.SetBinError(10, 0.33  )
		ttbar.SetBinContent(10, 9.9 )
		ttbar.SetBinError(10, 1.8  )
		VV.SetBinContent(10, 6.55 )
		VV.SetBinError(10, 0.3  )
		other.SetBinContent(10, 6.7 )
		other.SetBinError(10, 1.1  )
		totBG.SetBinContent(10, 49.1 )
		totBG.SetBinError(10,4.42944691807)
		data.SetBinContent(10, 26 )
		#data.SetBinError(10,5.09901951359)
		sig.SetBinContent(11, 948.4 )
		sig.SetBinError(11, 6.5  )
		zjets.SetBinContent(11, 18.19 )
		zjets.SetBinError(11, 0.26  )
		ttbar.SetBinContent(11, 4.68 )
		ttbar.SetBinError(11, 1.07  )
		VV.SetBinContent(11, 4.36 )
		VV.SetBinError(11, 0.24  )
		other.SetBinContent(11, 4.53 )
		other.SetBinError(11, 0.91  )
		totBG.SetBinContent(11, 31.8 )
		totBG.SetBinError(11,2.95296461205)
		data.SetBinContent(11, 16 )
		#data.SetBinError(11,4.0)
		sig.SetBinContent(12, 630.1 )
		sig.SetBinError(12, 4.2  )
		zjets.SetBinContent(12, 12.36 )
		zjets.SetBinError(12, 0.19  )
		ttbar.SetBinContent(12, 3.47 )
		ttbar.SetBinError(12, 0.93  )
		VV.SetBinContent(12, 3.17 )
		VV.SetBinError(12, 0.2  )
		other.SetBinContent(12, 3.04 )
		other.SetBinError(12, 0.74  )
		totBG.SetBinContent(12, 22 )
		totBG.SetBinError(12,2.24722050542)
		data.SetBinContent(12, 11 )
		#data.SetBinError(12,3.31662479036)
		sig.SetBinContent(13, 424.2 )
		sig.SetBinError(13, 2.8  )
		zjets.SetBinContent(13, 9.18 )
		zjets.SetBinError(13, 0.16  )
		ttbar.SetBinContent(13, 2.62 )
		ttbar.SetBinError(13, 0.83  )
		VV.SetBinContent(13, 2.45 )
		VV.SetBinError(13, 0.19  )
		other.SetBinContent(13, 2.26 )
		other.SetBinError(13, 0.63  )
		totBG.SetBinContent(13, 16.5 )
		totBG.SetBinError(13,1.94164878389)
		data.SetBinContent(13, 8 )
		#data.SetBinError(13,2.82842712475)
		sig.SetBinContent(14, 292.7 )
		sig.SetBinError(14, 1.9  )
		zjets.SetBinContent(14, 6.93 )
		zjets.SetBinError(14, 0.13  )
		ttbar.SetBinContent(14, 3.89 )
		ttbar.SetBinError(14, 1.23  )
		VV.SetBinContent(14, 1.88 )
		VV.SetBinError(14, 0.17  )
		other.SetBinContent(14, 2.05 )
		other.SetBinError(14, 0.6  )
		totBG.SetBinContent(14, 14.8 )
		totBG.SetBinError(14,1.78044938148)
		data.SetBinContent(14, 7 )
		#data.SetBinError(14,2.64575131106)
		sig.SetBinContent(15, 205.6 )
		sig.SetBinError(15, 1.3  )
		zjets.SetBinContent(15, 5.55 )
		zjets.SetBinError(15, 0.11  )
		ttbar.SetBinContent(15, 2.34 )
		ttbar.SetBinError(15, 0.88  )
		VV.SetBinContent(15, 1.44 )
		VV.SetBinError(15, 0.15  )
		other.SetBinContent(15, 1.49 )
		other.SetBinError(15, 0.5  )
		totBG.SetBinContent(15, 10.82 )
		totBG.SetBinError(15,1.36124942608)
		data.SetBinContent(15, 6 )
		#data.SetBinError(15,2.44948974278)
		sig.SetBinContent(16, 146.75 )
		sig.SetBinError(16, 0.92  )
		zjets.SetBinContent(16, 4.405 )
		zjets.SetBinError(16, 0.097  )
		ttbar.SetBinContent(16, 0.22 )
		ttbar.SetBinError(16, 0.13  )
		VV.SetBinContent(16, 1.31 )
		VV.SetBinError(16, 0.15  )
		other.SetBinContent(16, 1.105 )
		other.SetBinError(16, 0.425  )
		totBG.SetBinContent(16, 7.04 )
		totBG.SetBinError(16,0.857029754443)
		data.SetBinContent(16, 5 )
		#data.SetBinError(16,2.2360679775)
		sig.SetBinContent(17, 103.92 )
		sig.SetBinError(17, 0.65  )
		zjets.SetBinContent(17, 3.663 )
		zjets.SetBinError(17, 0.087  )
		ttbar.SetBinContent(17, 0.72 )
		ttbar.SetBinError(17, 0.42  )
		VV.SetBinContent(17, 1.1 )
		VV.SetBinError(17, 0.13  )
		other.SetBinContent(17, 0.733 )
		other.SetBinError(17, 0.334  )
		totBG.SetBinContent(17, 6.21 )
		totBG.SetBinError(17,0.813449445264)
		data.SetBinContent(17, 4 )
		#data.SetBinError(17,2.0)
		sig.SetBinContent(18, 74.98 )
		sig.SetBinError(18, 0.46  )
		zjets.SetBinContent(18, 3.234 )
		zjets.SetBinError(18, 0.083  )
		ttbar.SetBinContent(18, 0.466 )
		ttbar.SetBinError(18, 0.33  )
		VV.SetBinContent(18, 0.93 )
		VV.SetBinError(18, 0.12  )
		other.SetBinContent(18, 0.603 )
		other.SetBinError(18, 0.311  )
		totBG.SetBinContent(18, 5.24 )
		totBG.SetBinError(18,0.737563556583)
		data.SetBinContent(18, 4 )
		#data.SetBinError(18,2.0)
		sig.SetBinContent(19, 54.86 )
		sig.SetBinError(19, 0.33  )
		zjets.SetBinContent(19, 2.712 )
		zjets.SetBinError(19, 0.074  )
		ttbar.SetBinContent(19, 0.602 )
		ttbar.SetBinError(19, 0.426  )
		VV.SetBinContent(19, 0.69 )
		VV.SetBinError(19, 0.1  )
		other.SetBinContent(19, 0.603 )
		other.SetBinError(19, 0.311  )
		totBG.SetBinContent(19, 4.6 )
		totBG.SetBinError(19,0.722495674728)
		data.SetBinContent(19, 3 )
		#data.SetBinError(19,1.73205080757)
		sig.SetBinContent(20, 40.3 )
		sig.SetBinError(20, 0.24  )
		zjets.SetBinContent(20, 2.39 )
		zjets.SetBinError(20, 0.069  )
		ttbar.SetBinContent(20, 0.036 )
		ttbar.SetBinError(20, 0.036  )
		VV.SetBinContent(20, 0.69 )
		VV.SetBinError(20, 0.1  )
		other.SetBinContent(20, 0.412 )
		other.SetBinError(20, 0.246  )
		totBG.SetBinContent(20, 3.53 )
		totBG.SetBinError(20,0.504777178565)
		data.SetBinContent(20, 3 )
		#data.SetBinError(20,1.73205080757)
		sig.SetBinContent(21, 29.65 )
		sig.SetBinError(21, 0.17  )
		zjets.SetBinContent(21, 1.859 )
		zjets.SetBinError(21, 0.058  )
		ttbar.SetBinContent(21, 0.193 )
		ttbar.SetBinError(21, 0.193  )
		VV.SetBinContent(21, 0.63 )
		VV.SetBinError(21, 0.1  )
		other.SetBinContent(21, 0.412 )
		other.SetBinError(21, 0.246  )
		totBG.SetBinContent(21, 3.1 )
		totBG.SetBinError(21,0.534134814443)
		data.SetBinContent(21, 3 )
		#data.SetBinError(21,1.73205080757)
		sig.SetBinContent(22, 22.17 )
		sig.SetBinError(22, 0.13  )
		zjets.SetBinContent(22, 1.675 )
		zjets.SetBinError(22, 0.055  )
		ttbar.SetBinContent(22, 0.223 )
		ttbar.SetBinError(22, 0.223  )
		VV.SetBinContent(22, 0.559 )
		VV.SetBinError(22, 0.099  )
		other.SetBinContent(22, 0.198 )
		other.SetBinError(22, 0.188  )
		totBG.SetBinContent(22, 2.65 )
		totBG.SetBinError(22,0.460108682813)
		data.SetBinContent(22, 2 )
		#data.SetBinError(22,1.41421356237)
		sig.SetBinContent(23, 16.425 )
		sig.SetBinError(23, 0.095  )
		zjets.SetBinContent(23, 1.129 )
		zjets.SetBinError(23, 0.04  )
		ttbar.SetBinContent(23, 0.299 )
		ttbar.SetBinError(23, 0.299  )
		VV.SetBinContent(23, 0.53 )
		VV.SetBinError(23, 0.1  )
		other.SetBinContent(23, 0.198 )
		other.SetBinError(23, 0.188  )
		totBG.SetBinContent(23, 2.15 )
		totBG.SetBinError(23,0.458039299624)
		data.SetBinContent(23, 2 )
		#data.SetBinError(23,1.41421356237)
		sig.SetBinContent(24, 12.296 )
		sig.SetBinError(24, 0.07  )
		zjets.SetBinContent(24, 1.261 )
		zjets.SetBinError(24, 0.047  )
		ttbar.SetBinContent(24, 0.46 )
		ttbar.SetBinError(24, 0.46  )
		VV.SetBinContent(24, 0.53 )
		VV.SetBinError(24, 0.1  )
		other.SetBinContent(24, 0.198 )
		other.SetBinError(24, 0.188  )
		totBG.SetBinContent(24, 2.45 )
		totBG.SetBinError(24,0.563648826842)
		data.SetBinContent(24, 2 )
		#data.SetBinError(24,1.41421356237)
		sig.SetBinContent(25, 9.238 )
		sig.SetBinError(25, 0.052  )
		zjets.SetBinContent(25, 1.144 )
		zjets.SetBinError(25, 0.044  )
		ttbar.SetBinContent(25, 0.544 )
		ttbar.SetBinError(25, 0.544  )
		VV.SetBinContent(25, 0.54 )
		VV.SetBinError(25, 0.11  )
		other.SetBinContent(25, 0.188 )
		other.SetBinError(25,0.279)
		totBG.SetBinContent(25, 2.41 )
		totBG.SetBinError(25,0.664830805544)
		data.SetBinContent(25, 2 )
		#data.SetBinError(25,1.41421356237)
		sig.SetBinContent(26, 6.899 )
		sig.SetBinError(26, 0.039  )
		zjets.SetBinContent(26, 1.057 )
		zjets.SetBinError(26, 0.044  )
		ttbar.SetBinContent(26, 0.575 )
		ttbar.SetBinError(26, 0.575  )
		VV.SetBinContent(26, 0.5 )
		VV.SetBinError(26, 0.11  )
		other.SetBinContent(26, 0.188 )
		other.SetBinError(26,0.279)
		totBG.SetBinContent(26, 2.32 )
		totBG.SetBinError(26,0.686221538572)
		data.SetBinContent(26, 2 )
		#data.SetBinError(26,1.41421356237)
		sig.SetBinContent(27, 5.243 )
		sig.SetBinError(27, 0.029  )
		zjets.SetBinContent(27, 1.054 )
		zjets.SetBinError(27, 0.045  )
		ttbar.SetBinContent(27, 0.588 )
		ttbar.SetBinError(27, 0.588  )
		VV.SetBinContent(27, 0.47 )
		VV.SetBinError(27, 0.11  )
		other.SetBinContent(27, 0.188 )
		other.SetBinError(27,0.279)
		totBG.SetBinContent(27, 2.3 )
		totBG.SetBinError(27,0.6989277502)
		data.SetBinContent(27, 2 )
		#data.SetBinError(27,1.41421356237)
		sig.SetBinContent(28, 3.985 )
		sig.SetBinError(28, 0.022  )
		zjets.SetBinContent(28, 1.054 )
		zjets.SetBinError(28, 0.045  )
		ttbar.SetBinContent(28, 0.588 )
		ttbar.SetBinError(28, 0.588  )
		VV.SetBinContent(28, 0.47 )
		VV.SetBinError(28, 0.11  )
		other.SetBinContent(28, 0.188 )
		other.SetBinError(28,0.279)
		totBG.SetBinContent(28, 2.3 )
		totBG.SetBinError(28,0.6989277502)
		data.SetBinContent(28, 2 )
		#data.SetBinError(28,1.41421356237)
		sig.SetBinContent(29, 3.062 )
		sig.SetBinError(29, 0.017  )
		zjets.SetBinContent(29, 1.054 )
		zjets.SetBinError(29, 0.045  )
		ttbar.SetBinContent(29, 0.588 )
		ttbar.SetBinError(29, 0.588  )
		VV.SetBinContent(29, 0.47 )
		VV.SetBinError(29, 0.11  )
		other.SetBinContent(29, 0.188 )
		other.SetBinError(29,0.279)
		totBG.SetBinContent(29, 2.3 )
		totBG.SetBinError(29,0.6989277502)
		data.SetBinContent(29, 2 )
		#data.SetBinError(29,1.41421356237)
		sig.SetBinContent(30, 2.346 )
		sig.SetBinError(30, 0.013  )
		zjets.SetBinContent(30, 1.054 )
		zjets.SetBinError(30, 0.045  )
		ttbar.SetBinContent(30, 0.588 )
		ttbar.SetBinError(30, 0.588  )
		VV.SetBinContent(30, 0.47 )
		VV.SetBinError(30, 0.11  )
		other.SetBinContent(30, 0.188 )
		other.SetBinError(30,0.279)
		totBG.SetBinContent(30, 2.3 )
		totBG.SetBinError(30,0.6989277502)
		data.SetBinContent(30, 2 )
		#data.SetBinError(30,1.41421356237)
		sig.SetBinContent(31, 1.7899 )
		sig.SetBinError(31, 0.0097  )
		zjets.SetBinContent(31, 1.054 )
		zjets.SetBinError(31, 0.045  )
		ttbar.SetBinContent(31, 0.588 )
		ttbar.SetBinError(31, 0.588  )
		VV.SetBinContent(31, 0.47 )
		VV.SetBinError(31, 0.11  )
		other.SetBinContent(31, 0.188 )
		other.SetBinError(31,0.279)
		totBG.SetBinContent(31, 2.3 )
		totBG.SetBinError(31,0.6989277502)
		data.SetBinContent(31, 2 )
		#data.SetBinError(31,1.41421356237)
		sig.SetBinContent(32, 1.3801 )
		sig.SetBinError(32, 0.0075  )
		zjets.SetBinContent(32, 1.054 )
		zjets.SetBinError(32, 0.045  )
		ttbar.SetBinContent(32, 0.588 )
		ttbar.SetBinError(32, 0.588  )
		VV.SetBinContent(32, 0.47 )
		VV.SetBinError(32, 0.11  )
		other.SetBinContent(32, 0.188 )
		other.SetBinError(32,0.279)
		totBG.SetBinContent(32, 2.3 )
		totBG.SetBinError(32,0.6989277502)
		data.SetBinContent(32, 2 )
		#data.SetBinError(32,1.41421356237)
		sig.SetBinContent(33, 1.0659 )
		sig.SetBinError(33, 0.0057  )
		zjets.SetBinContent(33, 1.054 )
		zjets.SetBinError(33, 0.045  )
		ttbar.SetBinContent(33, 0.588 )
		ttbar.SetBinError(33, 0.588  )
		VV.SetBinContent(33, 0.47 )
		VV.SetBinError(33, 0.11  )
		other.SetBinContent(33, 0.188 )
		other.SetBinError(33,0.279)
		totBG.SetBinContent(33, 2.3 )
		totBG.SetBinError(33,0.6989277502)
		data.SetBinContent(33, 2 )
		#data.SetBinError(33,1.41421356237)
		sig.SetBinContent(34, 0.821 )
		sig.SetBinError(34, 0.004  )
		zjets.SetBinContent(34, 1.054 )
		zjets.SetBinError(34, 0.045  )
		ttbar.SetBinContent(34, 0.588 )
		ttbar.SetBinError(34, 0.588  )
		VV.SetBinContent(34, 0.47 )
		VV.SetBinError(34, 0.11  )
		other.SetBinContent(34, 0.188 )
		other.SetBinError(34,0.279)
		totBG.SetBinContent(34, 2.3 )
		totBG.SetBinError(34,0.6989277502)
		data.SetBinContent(34, 2 )
		#data.SetBinError(34,1.41421356237)
		sig.SetBinContent(35, 0.636 )
		sig.SetBinError(35, 0.003  )
		zjets.SetBinContent(35, 1.054 )
		zjets.SetBinError(35, 0.045  )
		ttbar.SetBinContent(35, 0.588 )
		ttbar.SetBinError(35, 0.588  )
		VV.SetBinContent(35, 0.47 )
		VV.SetBinError(35, 0.11  )
		other.SetBinContent(35, 0.188 )
		other.SetBinError(35,0.279)
		totBG.SetBinContent(35, 2.3 )
		totBG.SetBinError(35,0.6989277502)
		data.SetBinContent(35, 2 )
		#data.SetBinError(35,1.41421356237)
		sig.SetBinContent(36, 0.491 )
		sig.SetBinError(36, 0.003  )
		zjets.SetBinContent(36, 1.054 )
		zjets.SetBinError(36, 0.045  )
		ttbar.SetBinContent(36, 0.588 )
		ttbar.SetBinError(36, 0.588  )
		VV.SetBinContent(36, 0.47 )
		VV.SetBinError(36, 0.11  )
		other.SetBinContent(36, 0.188 )
		other.SetBinError(36,0.279)
		totBG.SetBinContent(36, 2.3 )
		totBG.SetBinError(36,0.6989277502)
		data.SetBinContent(36, 2 )
		#data.SetBinError(36,1.41421356237)
		sig.SetBinContent(37, 0.377 )
		sig.SetBinError(37, 0.002  )
		zjets.SetBinContent(37, 1.054 )
		zjets.SetBinError(37, 0.045  )
		ttbar.SetBinContent(37, 0.588 )
		ttbar.SetBinError(37, 0.588  )
		VV.SetBinContent(37, 0.47 )
		VV.SetBinError(37, 0.11  )
		other.SetBinContent(37, 0.188 )
		other.SetBinError(37,0.279)
		totBG.SetBinContent(37, 2.3 )
		totBG.SetBinError(37,0.6989277502)
		data.SetBinContent(37, 2 )
		#data.SetBinError(37,1.41421356237)


		zjets.SetFillColor(kBlue)
		ttbar.SetFillColor(kOrange)
		VV.SetFillColor(kCyan)
		other.SetFillColor(kRed)
		totBG.SetFillColor(kGray)
		totBG.SetLineWidth(0)
		totBG.SetMarkerSize(0)
		zjets.SetLineColor(kBlue)
		ttbar.SetLineColor(kOrange)
		VV.SetLineColor(kCyan)
		other.SetLineColor(kRed)
		zjets.SetFillStyle(3013)
		ttbar.SetFillStyle(3004)
		VV.SetFillStyle(3005)
		other.SetFillStyle(3007)
		totBG.SetFillStyle(3144)
		sig.SetMarkerSize(0)
		sig.SetLineStyle(2)
		sig.SetLineWidth(2)
		#sig.SetMarkerColor(kMagenta)
		sig.SetLineColor(kMagenta)


		alpha = 1 - 0.6827
		dataTGraph = TGraphAsymmErrors(data)
		for i in range(dataTGraph.GetN()):
			N = dataTGraph.GetY()[i]
			if N>10:
				dataTGraph.SetPointEYlow(i, math.sqrt(N)/2)
				dataTGraph.SetPointEYhigh(i, math.sqrt(N)/2)
			else:
				if N==0: L = 0
				else: L = (ROOT.Math.gamma_quantile(alpha/2,N,1.))
				U =  ROOT.Math.gamma_quantile_c(alpha/2,N+1,1) 
				dataTGraph.SetPointEYlow(i, N-L)
				dataTGraph.SetPointEYhigh(i, U-N)
			#print i,N,L,U,N-L,U-N
		dataTGraph.SetMarkerStyle(20)
		dataTGraph.SetMarkerSize(1)
		dataTGraph.SetLineWidth(2)

		#for i in range(data.GetNbinsX()):
		#	print i,data.GetBinContent(i),data.GetBinError(i)


		MCStack = THStack ("MCStack",";m_{LQ} [GeV];Final selection event yield")
		for x in [other,VV,ttbar,zjets]:
			x.SetMarkerSize(0)
			x.SetLineWidth(2)
			MCStack.Add(x)
			#x.SetMaximum(*sig.GetMaximum())
			#x->SetBinErrorOption(TH1::kPoisson)
		#data.SetBinErrorOption(TH1.kPoisson)

		MCStack.SetMinimum(1)
		MCStack.SetMaximum(5*sig.GetMaximum())
		pad1.SetTicks(0,1)
		MCStack.Draw("HIST")
		MCStack.GetXaxis().SetTitleFont(42)
		MCStack.GetYaxis().SetTitleFont(42)
		MCStack.GetXaxis().SetLabelFont(42)
		MCStack.GetYaxis().SetLabelFont(42)
		MCStack.GetXaxis().SetLabelOffset(0.007)
		MCStack.GetYaxis().SetLabelOffset(0.007)
		MCStack.GetXaxis().SetLabelSize(0.053)
		MCStack.GetYaxis().SetLabelSize(0.053)
		MCStack.GetXaxis().SetTitleOffset(1.15)
		MCStack.GetYaxis().SetTitleOffset(0.92)
		MCStack.GetXaxis().SetTitleSize(0.06)
		MCStack.GetYaxis().SetTitleSize(0.06)
		#MCStack.GetXaxis().CenterTitle(1)
		#MCStack.GetYaxis().CenterTitle(1)
		totBG.Draw("e3sames")
		sig.Draw("hist same")
		dataTGraph.Draw("pesames")
		leg = TLegend(0.45,0.49,0.91,0.85,"","brNDC")	
		leg.SetTextFont(42)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetBorderSize(0)
		leg.SetTextSize(.045)
		if 'uujj' in channel:
			leg.AddEntry(dataTGraph,'Data','pe')
			leg.AddEntry(zjets,'Z+jets','f')
			leg.AddEntry(ttbar,'t#bar{t}+jets','f')
			leg.AddEntry(VV,'VV','f')
			leg.AddEntry(other,'Other background','f')
		if 'uvjj' in channel:
			leg.AddEntry(dataTGraph,'Data','pe')
			leg.AddEntry(wjets,'W+jets','f')
			leg.AddEntry(ttbar,'t#bar{t}+jets','f')
			leg.AddEntry(VV,'VV','f')
			leg.AddEntry(other,'Other background','f')
		leg.AddEntry(totBG,'stat + syst uncertainty','f')
		leg.AddEntry(sig,'LQ signal','l')
		leg.Draw()
		l1=TLatex()
		l1.SetTextAlign(12)
		l1.SetTextFont(42)
		l1.SetNDC()
		l1.SetTextSize(0.06)
		l2=TLatex()
		l2.SetTextAlign(12)
		l2.SetTextFont(62)
		l2.SetNDC()
		l2.SetTextSize(0.06)
		l3=TLatex()
		l3.SetTextAlign(12)
		l3.SetTextFont(42)
		l3.SetNDC()
		l3.SetTextSize(0.05)
		if isPAS:
			l1.DrawLatex(0.13,0.94,"                                                35.9 fb^{-1} (13 TeV)")
		else:
			l1.DrawLatex(0.13,0.94,"#it{Preliminary}                              35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.86,"CMS")
		if 'uujj' in channel:
			l3.DrawLatex(0.155,0.8,"#mu#mujj")
		if 'uvjj' in channel:
			l3.DrawLatex(0.155,0.8,"#mu#nujj")
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_finalSelectionPlot.pdf')
		print 'Saving histogram.... Results_'+version_name+'/BasicLQ_'+channel+'_finalSelectionPlot.pdf'
		
		#uvjj
		channel='uvjj'
		data.SetBinErrorOption(TH1.kPoisson)
		sig.SetBinContent(1, 116600 )
		sig.SetBinError(1, 1500  )
		wjets.SetBinContent(1, 5672 )
		wjets.SetBinError(1, 26  )
		ttbar.SetBinContent(1, 15816 )
		ttbar.SetBinError(1, 51  )
		VV.SetBinContent(1, 1049.6 )
		VV.SetBinError(1, 5.0  )
		other.SetBinContent(1, 2732 )
		other.SetBinError(1, 15  )
		totBG.SetBinContent(1, 25270 )
		totBG.SetBinError(1,1172.48539437)
		data.SetBinContent(1, 26043 )
		#err_low = data.GetBinErrorLow(1)
		#err_high = data.GetBinErrorHigh(1)
		#print err_low,err_high
		#data.SetBinError(1,161.378437221)
		sig.SetBinContent(2, 51050 )
		sig.SetBinError(2, 580  )
		wjets.SetBinContent(2, 2635 )
		wjets.SetBinError(2, 16  )
		ttbar.SetBinContent(2, 4662 )
		ttbar.SetBinError(2, 28  )
		VV.SetBinContent(2, 575.9 )
		VV.SetBinError(2, 3.7  )
		other.SetBinContent(2, 1155 )
		other.SetBinError(2, 10  )
		totBG.SetBinContent(2, 9029 )
		totBG.SetBinError(2,432.33898737)
		data.SetBinContent(2, 9519 )
		#data.SetBinError(2,97.5653627062)
		sig.SetBinContent(3, 23840 )
		sig.SetBinError(3, 250  )
		wjets.SetBinContent(3, 1259.2 )
		wjets.SetBinError(3, 9.7  )
		ttbar.SetBinContent(3, 2066 )
		ttbar.SetBinError(3, 18  )
		VV.SetBinContent(3, 346.8 )
		VV.SetBinError(3, 3.0  )
		other.SetBinContent(3, 611.7 )
		other.SetBinError(3, 7.6  )
		totBG.SetBinContent(3, 4284 )
		totBG.SetBinError(3,198.224620065)
		data.SetBinContent(3, 4669 )
		#data.SetBinError(3,68.3300812234)
		sig.SetBinContent(4, 11580 )
		sig.SetBinError(4, 120  )
		wjets.SetBinContent(4, 757.1 )
		wjets.SetBinError(4, 7.2  )
		ttbar.SetBinContent(4, 964 )
		ttbar.SetBinError(4, 13  )
		VV.SetBinContent(4, 200.7 )
		VV.SetBinError(4, 2.3  )
		other.SetBinContent(4, 335 )
		other.SetBinError(4, 5.6  )
		totBG.SetBinContent(4, 2256 )
		totBG.SetBinError(4,123.044707322)
		data.SetBinContent(4, 2379 )
		#data.SetBinError(4,48.774993593)
		sig.SetBinContent(5, 6051 )
		sig.SetBinError(5, 58  )
		wjets.SetBinContent(5, 418.2 )
		wjets.SetBinError(5, 4.8  )
		ttbar.SetBinContent(5, 461.3 )
		ttbar.SetBinError(5, 8.8  )
		VV.SetBinContent(5, 131.5 )
		VV.SetBinError(5, 1.9  )
		other.SetBinContent(5, 176 )
		other.SetBinError(5, 4.2  )
		totBG.SetBinContent(5, 1187 )
		totBG.SetBinError(5,70.8590149522)
		data.SetBinContent(5, 1279 )
		#data.SetBinError(5,35.7631094845)
		sig.SetBinContent(6, 3280 )
		sig.SetBinError(6, 32  )
		wjets.SetBinContent(6, 248.1 )
		wjets.SetBinError(6, 3.4  )
		ttbar.SetBinContent(6, 228.4 )
		ttbar.SetBinError(6, 6.2  )
		VV.SetBinContent(6, 86.4 )
		VV.SetBinError(6, 1.6  )
		other.SetBinContent(6, 108.1 )
		other.SetBinError(6, 3.4  )
		totBG.SetBinContent(6, 671 )
		totBG.SetBinError(6,47.6759897642)
		data.SetBinContent(6, 737 )
		#data.SetBinError(6,27.147743921)
		sig.SetBinContent(7, 1911 )
		sig.SetBinError(7, 18  )
		wjets.SetBinContent(7, 177.2 )
		wjets.SetBinError(7, 2.8  )
		ttbar.SetBinContent(7, 119.3 )
		ttbar.SetBinError(7, 4.4  )
		VV.SetBinContent(7, 58.8 )
		VV.SetBinError(7, 1.3  )
		other.SetBinContent(7, 67.6 )
		other.SetBinError(7, 2.7  )
		totBG.SetBinContent(7, 422.9 )
		totBG.SetBinError(7,40.46245173)
		data.SetBinContent(7, 430 )
		#data.SetBinError(7,20.7364413533)
		sig.SetBinContent(8, 1165 )
		sig.SetBinError(8, 10  )
		wjets.SetBinContent(8, 99.2 )
		wjets.SetBinError(8, 1.8  )
		ttbar.SetBinContent(8, 69.2 )
		ttbar.SetBinError(8, 3.4  )
		VV.SetBinContent(8, 44 )
		VV.SetBinError(8, 1.2  )
		other.SetBinContent(8, 42.9 )
		other.SetBinError(8, 2.1  )
		totBG.SetBinContent(8, 255.4 )
		totBG.SetBinError(8,19.4517351411)
		data.SetBinContent(8, 270 )
		#data.SetBinError(8,16.4316767252)
		sig.SetBinContent(9, 708.9 )
		sig.SetBinError(9, 6.2  )
		wjets.SetBinContent(9, 70.9 )
		wjets.SetBinError(9, 1.5  )
		ttbar.SetBinContent(9, 43.4 )
		ttbar.SetBinError(9, 2.7  )
		VV.SetBinContent(9, 31.1 )
		VV.SetBinError(9, 1.0  )
		other.SetBinContent(9, 28.6 )
		other.SetBinError(9, 1.7  )
		totBG.SetBinContent(9, 174 )
		totBG.SetBinError(9,13.5162864723)
		data.SetBinContent(9, 179 )
		#data.SetBinError(9,13.3790881603)
		sig.SetBinContent(10, 453.4 )
		sig.SetBinError(10, 3.9  )
		wjets.SetBinContent(10, 53.8 )
		wjets.SetBinError(10, 1.3  )
		ttbar.SetBinContent(10, 26.8 )
		ttbar.SetBinError(10, 2.1  )
		VV.SetBinContent(10, 22.89 )
		VV.SetBinError(10, 0.91  )
		other.SetBinContent(10, 19.7 )
		other.SetBinError(10, 1.4  )
		totBG.SetBinContent(10, 123.2 )
		totBG.SetBinError(10,10.5361283212)
		data.SetBinContent(10, 130 )
		#data.SetBinError(10,11.401754251)
		sig.SetBinContent(11, 301 )
		sig.SetBinError(11, 2.5  )
		wjets.SetBinContent(11, 36.02 )
		wjets.SetBinError(11, 0.96  )
		ttbar.SetBinContent(11, 16.7 )
		ttbar.SetBinError(11, 1.7  )
		VV.SetBinContent(11, 17.03 )
		VV.SetBinError(11, 0.78  )
		other.SetBinContent(11, 14.8 )
		other.SetBinError(11, 1.2  )
		totBG.SetBinContent(11, 84.6 )
		totBG.SetBinError(11,7.49466476902)
		data.SetBinContent(11, 93 )
		#data.SetBinError(11,9.64365076099)
		sig.SetBinContent(12, 199.2 )
		sig.SetBinError(12, 1.6  )
		wjets.SetBinContent(12, 22.73 )
		wjets.SetBinError(12, 0.68  )
		ttbar.SetBinContent(12, 11.59 )
		ttbar.SetBinError(12, 1.43  )
		VV.SetBinContent(12, 13.32 )
		VV.SetBinError(12, 0.71  )
		other.SetBinContent(12, 9.89 )
		other.SetBinError(12, 0.96  )
		totBG.SetBinContent(12, 57.5 )
		totBG.SetBinError(12,5.57135531087)
		data.SetBinContent(12, 68 )
		#data.SetBinError(12,8.24621125124)
		sig.SetBinContent(13, 136.2 )
		sig.SetBinError(13, 1.1  )
		wjets.SetBinContent(13, 13.95 )
		wjets.SetBinError(13, 0.46  )
		ttbar.SetBinContent(13, 7.6 )
		ttbar.SetBinError(13, 1.15  )
		VV.SetBinContent(13, 8.58 )
		VV.SetBinError(13, 0.52  )
		other.SetBinContent(13, 7.6 )
		other.SetBinError(13, 0.83  )
		totBG.SetBinContent(13, 37.7 )
		totBG.SetBinError(13,4.58802789878)
		data.SetBinContent(13, 57 )
		#data.SetBinError(13,7.54983443527)
		sig.SetBinContent(14, 94.69 )
		sig.SetBinError(14, 0.75  )
		wjets.SetBinContent(14, 10.49 )
		wjets.SetBinError(14, 0.37  )
		ttbar.SetBinContent(14, 4.88 )
		ttbar.SetBinError(14, 0.92  )
		VV.SetBinContent(14, 7.46 )
		VV.SetBinError(14, 0.52  )
		other.SetBinContent(14, 6.51 )
		other.SetBinError(14, 0.81  )
		totBG.SetBinContent(14, 29.3 )
		totBG.SetBinError(14,3.76961536499)
		data.SetBinContent(14, 45 )
		#data.SetBinError(14,6.7082039325)
		sig.SetBinContent(15, 65.88 )
		sig.SetBinError(15, 0.51  )
		wjets.SetBinContent(15, 8.96 )
		wjets.SetBinError(15, 0.34  )
		ttbar.SetBinContent(15, 3.43 )
		ttbar.SetBinError(15, 0.79  )
		VV.SetBinContent(15, 6.14 )
		VV.SetBinError(15, 0.48  )
		other.SetBinContent(15, 5.56 )
		other.SetBinError(15, 0.75  )
		totBG.SetBinContent(15, 24.1 )
		totBG.SetBinError(15,2.683281573)
		data.SetBinContent(15, 35 )
		#data.SetBinError(15,5.9160797831)
		sig.SetBinContent(16, 47.05 )
		sig.SetBinError(16, 0.36  )
		wjets.SetBinContent(16, 5.96 )
		wjets.SetBinError(16, 0.25  )
		ttbar.SetBinContent(16, 2.36 )
		ttbar.SetBinError(16, 0.65  )
		VV.SetBinContent(16, 4.85 )
		VV.SetBinError(16, 0.42  )
		other.SetBinContent(16, 3.7 )
		other.SetBinError(16, 0.55  )
		totBG.SetBinContent(16, 16.87 )
		totBG.SetBinError(16,1.95862196455)
		data.SetBinContent(16, 30 )
		#data.SetBinError(16,5.47722557505)
		sig.SetBinContent(17, 33.89 )
		sig.SetBinError(17, 0.25  )
		wjets.SetBinContent(17, 5.4 )
		wjets.SetBinError(17, 0.24  )
		ttbar.SetBinContent(17, 1.66 )
		ttbar.SetBinError(17, 0.55  )
		VV.SetBinContent(17, 4.3 )
		VV.SetBinError(17, 0.41  )
		other.SetBinContent(17, 3.3 )
		other.SetBinError(17, 0.52  )
		totBG.SetBinContent(17, 14.67 )
		totBG.SetBinError(17,1.7578680269)
		data.SetBinContent(17, 26 )
		#data.SetBinError(17,5.09901951359)
		sig.SetBinContent(18, 24.42 )
		sig.SetBinError(18, 0.18  )
		wjets.SetBinContent(18, 4.2 )
		wjets.SetBinError(18, 0.2  )
		ttbar.SetBinContent(18, 1.48 )
		ttbar.SetBinError(18, 0.52  )
		VV.SetBinContent(18, 3.9 )
		VV.SetBinError(18, 0.4  )
		other.SetBinContent(18, 2.54 )
		other.SetBinError(18, 0.45  )
		totBG.SetBinContent(18, 12.12 )
		totBG.SetBinError(18,1.51716841517)
		data.SetBinContent(18, 20 )
		#data.SetBinError(18,4.472135955)
		sig.SetBinContent(19, 18 )
		sig.SetBinError(19, 0.13  )
		wjets.SetBinContent(19, 4.16 )
		wjets.SetBinError(19, 0.22  )
		ttbar.SetBinContent(19, 1.29 )
		ttbar.SetBinError(19, 0.49  )
		VV.SetBinContent(19, 3.31 )
		VV.SetBinError(19, 0.38  )
		other.SetBinContent(19, 1.83 )
		other.SetBinError(19, 0.33  )
		totBG.SetBinContent(19, 10.59 )
		totBG.SetBinError(19,1.36751599625)
		data.SetBinContent(19, 15 )
		#data.SetBinError(19,3.87298334621)
		sig.SetBinContent(20, 13.413 )
		sig.SetBinError(20, 0.095  )
		wjets.SetBinContent(20, 3.05 )
		wjets.SetBinError(20, 0.17  )
		ttbar.SetBinContent(20, 0.759 )
		ttbar.SetBinError(20, 0.379  )
		VV.SetBinContent(20, 2.87 )
		VV.SetBinError(20, 0.35  )
		other.SetBinContent(20, 1.29 )
		other.SetBinError(20, 0.28  )
		totBG.SetBinContent(20, 7.97 )
		totBG.SetBinError(20,1.10385687478)
		data.SetBinContent(20, 13 )
		#data.SetBinError(20,3.60555127546)
		sig.SetBinContent(21, 9.979 )
		sig.SetBinError(21, 0.07  )
		wjets.SetBinContent(21, 3.02 )
		wjets.SetBinError(21, 0.18  )
		ttbar.SetBinContent(21, 0.559 )
		ttbar.SetBinError(21, 0.323  )
		VV.SetBinContent(21, 2.29 )
		VV.SetBinError(21, 0.31  )
		other.SetBinContent(21, 1.09 )
		other.SetBinError(21, 0.23  )
		totBG.SetBinContent(21, 6.96 )
		totBG.SetBinError(21,0.973498844375)
		data.SetBinContent(21, 11 )
		#data.SetBinError(21,3.31662479036)
		sig.SetBinContent(22, 7.417 )
		sig.SetBinError(22, 0.052  )
		wjets.SetBinContent(22, 2.68 )
		wjets.SetBinError(22, 0.17  )
		ttbar.SetBinContent(22, 0.74 )
		ttbar.SetBinError(22, 0.37  )
		VV.SetBinContent(22, 2.07 )
		VV.SetBinError(22, 0.3  )
		other.SetBinContent(22, 0.591 )
		other.SetBinError(22, 0.137  )
		totBG.SetBinContent(22, 6.08 )
		totBG.SetBinError(22,0.888144132447)
		data.SetBinContent(22, 11 )
		#data.SetBinError(22,3.31662479036)
		sig.SetBinContent(23, 5.575 )
		sig.SetBinError(23, 0.038  )
		wjets.SetBinContent(23, 1.61 )
		wjets.SetBinError(23, 0.11  )
		ttbar.SetBinContent(23, 0.74 )
		ttbar.SetBinError(23, 0.37  )
		VV.SetBinContent(23, 1.79 )
		VV.SetBinError(23, 0.28  )
		other.SetBinContent(23, 0.73 )
		other.SetBinError(23, 0.14  )
		totBG.SetBinContent(23, 4.87 )
		totBG.SetBinError(23,0.736613874428)
		data.SetBinContent(23, 9 )
		#data.SetBinError(23,3.0)
		sig.SetBinContent(24, 4.213 )
		sig.SetBinError(24, 0.028  )
		wjets.SetBinContent(24, 1.026 )
		wjets.SetBinError(24, 0.074  )
		ttbar.SetBinContent(24, 0.74 )
		ttbar.SetBinError(24, 0.37  )
		VV.SetBinContent(24, 1.5 )
		VV.SetBinError(24, 0.25  )
		other.SetBinContent(24, 0.7 )
		other.SetBinError(24, 0.14  )
		totBG.SetBinContent(24, 3.97 )
		totBG.SetBinError(24,0.644437739429)
		data.SetBinContent(24, 7 )
		#data.SetBinError(24,2.64575131106)
		sig.SetBinContent(25, 3.194 )
		sig.SetBinError(25, 0.022  )
		wjets.SetBinContent(25, 1.005 )
		wjets.SetBinError(25, 0.077  )
		ttbar.SetBinContent(25, 0.74 )
		ttbar.SetBinError(25, 0.37  )
		VV.SetBinContent(25, 1.33 )
		VV.SetBinError(25, 0.26  )
		other.SetBinContent(25, 0.69 )
		other.SetBinError(25, 0.14  )
		totBG.SetBinContent(25, 3.76 )
		totBG.SetBinError(25,0.618465843843)
		data.SetBinContent(25, 7 )
		#data.SetBinError(25,2.64575131106)
		sig.SetBinContent(26, 2.416 )
		sig.SetBinError(26, 0.016  )
		wjets.SetBinContent(26, 1.45 )
		wjets.SetBinError(26, 0.12  )
		ttbar.SetBinContent(26, 0.559 )
		ttbar.SetBinError(26, 0.323  )
		VV.SetBinContent(26, 1.32 )
		VV.SetBinError(26, 0.26  )
		other.SetBinContent(26, 0.65 )
		other.SetBinError(26, 0.14  )
		totBG.SetBinContent(26, 3.97 )
		totBG.SetBinError(26,0.629364759102)
		data.SetBinContent(26, 7 )
		#data.SetBinError(26,2.64575131106)
		sig.SetBinContent(27, 1.841 )
		sig.SetBinError(27, 0.012  )
		wjets.SetBinContent(27, 1.29 )
		wjets.SetBinError(27, 0.11  )
		ttbar.SetBinContent(27, 0.559 )
		ttbar.SetBinError(27, 0.323  )
		VV.SetBinContent(27, 1.32 )
		VV.SetBinError(27, 0.26  )
		other.SetBinContent(27, 0.584 )
		other.SetBinError(27, 0.138  )
		totBG.SetBinContent(27, 3.75 )
		totBG.SetBinError(27,0.608769250209)
		data.SetBinContent(27, 7 )
		#data.SetBinError(27,2.64575131106)
		sig.SetBinContent(28, 1.4007 )
		sig.SetBinError(28, 0.0091  )
		wjets.SetBinContent(28, 1.12 )
		wjets.SetBinError(28, 0.1  )
		ttbar.SetBinContent(28, 0.559 )
		ttbar.SetBinError(28, 0.323  )
		VV.SetBinContent(28, 1.32 )
		VV.SetBinError(28, 0.26  )
		other.SetBinContent(28, 0.491 )
		other.SetBinError(28, 0.137  )
		totBG.SetBinContent(28, 3.49 )
		totBG.SetBinError(28,0.595482997238)
		data.SetBinContent(28, 6 )
		#data.SetBinError(28,2.44948974278)
		sig.SetBinContent(29, 1.0671 )
		sig.SetBinError(29, 0.0069  )
		wjets.SetBinContent(29, 1.07 )
		wjets.SetBinError(29, 0.1  )
		ttbar.SetBinContent(29, 0.559 )
		ttbar.SetBinError(29, 0.323  )
		VV.SetBinContent(29, 1.27 )
		VV.SetBinError(29, 0.26  )
		other.SetBinContent(29, 0.457 )
		other.SetBinError(29, 0.137  )
		totBG.SetBinContent(29, 3.35 )
		totBG.SetBinError(29,0.582580466545)
		data.SetBinContent(29, 6 )
		#data.SetBinError(29,2.44948974278)
		sig.SetBinContent(30, 0.8159 )
		sig.SetBinError(30, 0.0053  )
		wjets.SetBinContent(30, 0.884 )
		wjets.SetBinError(30, 0.09  )
		ttbar.SetBinContent(30, 0.559 )
		ttbar.SetBinError(30, 0.323  )
		VV.SetBinContent(30, 1.27 )
		VV.SetBinError(30, 0.26  )
		other.SetBinContent(30, 0.442 )
		other.SetBinError(30, 0.137  )
		totBG.SetBinContent(30, 3.15 )
		totBG.SetBinError(30,0.562227711875)
		data.SetBinContent(30, 6 )
		#data.SetBinError(30,2.44948974278)
		sig.SetBinContent(31, 0.629 )
		sig.SetBinError(31, 0.004  )
		wjets.SetBinContent(31, 0.99 )
		wjets.SetBinError(31, 0.11  )
		ttbar.SetBinContent(31, 0.559 )
		ttbar.SetBinError(31, 0.323  )
		VV.SetBinContent(31, 1.05 )
		VV.SetBinError(31, 0.24  )
		other.SetBinContent(31, 0.416 )
		other.SetBinError(31, 0.137  )
		totBG.SetBinContent(31, 3.01 )
		totBG.SetBinError(31,0.544058820349)
		data.SetBinContent(31, 6 )
		#data.SetBinError(31,2.44948974278)
		sig.SetBinContent(32, 0.487 )
		sig.SetBinError(32, 0.003  )
		wjets.SetBinContent(32, 0.91 )
		wjets.SetBinError(32, 0.11  )
		ttbar.SetBinContent(32, 0.381 )
		ttbar.SetBinError(32, 0.27  )
		VV.SetBinContent(32, 0.98 )
		VV.SetBinError(32, 0.23  )
		other.SetBinContent(32, 0.384 )
		other.SetBinError(32, 0.136  )
		totBG.SetBinContent(32, 2.65 )
		totBG.SetBinError(32,0.492036584006)
		data.SetBinContent(32, 5 )
		#data.SetBinError(32,2.2360679775)
		sig.SetBinContent(33, 0.373 )
		sig.SetBinError(33, 0.002  )
		wjets.SetBinContent(33, 0.91 )
		wjets.SetBinError(33, 0.11  )
		ttbar.SetBinContent(33, 0.381 )
		ttbar.SetBinError(33, 0.27  )
		VV.SetBinContent(33, 0.96 )
		VV.SetBinError(33, 0.24  )
		other.SetBinContent(33, 0.359 )
		other.SetBinError(33, 0.136  )
		totBG.SetBinContent(33, 2.61 )
		totBG.SetBinError(33,0.494064773081)
		data.SetBinContent(33, 5 )
		#data.SetBinError(33,2.2360679775)
		sig.SetBinContent(34, 0.287 )
		sig.SetBinError(34, 0.002  )
		wjets.SetBinContent(34, 0.88 )
		wjets.SetBinError(34, 0.11  )
		ttbar.SetBinContent(34, 0.199 )
		ttbar.SetBinError(34, 0.199  )
		VV.SetBinContent(34, 0.9 )
		VV.SetBinError(34, 0.23  )
		other.SetBinContent(34, 0.321 )
		other.SetBinError(34, 0.136  )
		totBG.SetBinContent(34, 2.3 )
		totBG.SetBinError(34,0.44821869662)
		data.SetBinContent(34, 4 )
		#data.SetBinError(34,2.0)
		sig.SetBinContent(35, 0.221 )
		sig.SetBinError(35, 0.001  )
		wjets.SetBinContent(35, 0.74 )
		wjets.SetBinError(35, 0.097  )
		ttbar.SetBinContent(35, 0.199 )
		ttbar.SetBinError(35, 0.199  )
		VV.SetBinContent(35, 0.86 )
		VV.SetBinError(35, 0.24  )
		other.SetBinContent(35, 0.309 )
		other.SetBinError(35, 0.136  )
		totBG.SetBinContent(35, 2.11 )
		totBG.SetBinError(35,0.430116263352)
		data.SetBinContent(35, 3 )
		#data.SetBinError(35,1.73205080757)
		sig.SetBinContent(36, 0.17 )
		sig.SetBinError(36, 0.001  )
		wjets.SetBinContent(36, 0.685 )
		wjets.SetBinError(36, 0.096  )
		ttbar.SetBinContent(36, 0.199 )
		ttbar.SetBinError(36, 0.199  )
		VV.SetBinContent(36, 0.83 )
		VV.SetBinError(36, 0.24  )
		other.SetBinContent(36, 0.3 )
		other.SetBinError(36, 0.136  )
		totBG.SetBinContent(36, 2.02 )
		totBG.SetBinError(36,0.424381903478)
		data.SetBinContent(36, 3 )
		#data.SetBinError(36,1.73205080757)
		sig.SetBinContent(37, 0.132 )
		sig.SetBinError(37, 0.001  )
		wjets.SetBinContent(37, 0.68 )
		wjets.SetBinError(37, 0.1  )
		ttbar.SetBinContent(37, 0.199 )
		ttbar.SetBinError(37, 0.199  )
		VV.SetBinContent(37, 0.29 )
		VV.SetBinError(37, 0.088  )
		other.SetBinContent(37, 0.295 )
		other.SetBinError(37, 0.136  )
		totBG.SetBinContent(37, 1.47 )
		totBG.SetBinError(37,0.317647603485)
		data.SetBinContent(37, 2 )
		#data.SetBinError(37,1.41421356237)


		wjets.SetFillColor(kBlue)
		#zjets.SetFillColor(kBlue)
		ttbar.SetFillColor(kOrange)
		VV.SetFillColor(kCyan)
		other.SetFillColor(kRed)
		totBG.SetFillColor(kGray)
		totBG.SetLineWidth(0)
		totBG.SetMarkerSize(0)
		wjets.SetLineColor(kBlue)
		#zjets.SetLineColor(kBlue)
		ttbar.SetLineColor(kOrange)
		VV.SetLineColor(kCyan)
		other.SetLineColor(kRed)
		wjets.SetFillStyle(3013)
		#zjets.SetFillStyle(kBlue)
		ttbar.SetFillStyle(3004)
		VV.SetFillStyle(3005)
		other.SetFillStyle(3007)
		totBG.SetFillStyle(3144)
		sig.SetMarkerSize(0)
		sig.SetLineStyle(2)
		sig.SetLineWidth(2)
		sig.SetLineColor(kMagenta)

		dataTGraph = TGraphAsymmErrors(data)
		for i in range(dataTGraph.GetN()):
			N = dataTGraph.GetY()[i]
			if N>10:
				dataTGraph.SetPointEYlow(i, math.sqrt(N)/2);
				dataTGraph.SetPointEYhigh(i, math.sqrt(N)/2);
			else:
				if N==0: L = 0
				else: L = (ROOT.Math.gamma_quantile(alpha/2,N,1.))
				U =  ROOT.Math.gamma_quantile_c(alpha/2,N+1,1) 
				dataTGraph.SetPointEYlow(i, N-L);
				dataTGraph.SetPointEYhigh(i, U-N);
			#print i,N,L,U,N-L,U-N
		dataTGraph.SetMarkerStyle(20)
		dataTGraph.SetMarkerSize(1)
		dataTGraph.SetLineWidth(2)

		#for i in range(data.GetNbinsX()):
		#	print i,data.GetBinContent(i),data.GetBinError(i)
	
		#dataTGraph.Print()
			
		MCStack = THStack ("MCStack",";m_{LQ} [GeV];Final selection event yield")
		for x in [other,VV,ttbar,wjets]:
			x.SetMarkerSize(0)
			x.SetLineWidth(2)
			MCStack.Add(x)
			#x.SetMaximum(*sig.GetMaximum())
			#x->SetBinErrorOption(TH1::kPoisson)

		MCStack.SetMinimum(1)
		MCStack.SetMaximum(5*sig.GetMaximum())
		MCStack.Draw("HIST")
		MCStack.GetXaxis().SetTitleFont(42)
		MCStack.GetYaxis().SetTitleFont(42)
		MCStack.GetXaxis().SetLabelFont(42)
		MCStack.GetYaxis().SetLabelFont(42)
		MCStack.GetXaxis().SetLabelOffset(0.007)
		MCStack.GetYaxis().SetLabelOffset(0.007)
		MCStack.GetXaxis().SetLabelSize(0.053)
		MCStack.GetYaxis().SetLabelSize(0.053)
		MCStack.GetXaxis().SetTitleOffset(1.15)
		MCStack.GetYaxis().SetTitleOffset(0.92)
		MCStack.GetXaxis().SetTitleSize(0.06)
		MCStack.GetYaxis().SetTitleSize(0.06)
		#MCStack.GetXaxis().CenterTitle(1)
		#MCStack.GetYaxis().CenterTitle(1)
		totBG.Draw("e3sames")
		sig.Draw("hist same")
		dataTGraph.Draw("pesames")
		leg = TLegend(0.45,0.49,0.91,0.85,"","brNDC");	
		leg.SetTextFont(42)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetBorderSize(0)
		leg.SetTextSize(.045)
		if 'uujj' in channel:
			leg.AddEntry(dataTGraph,'Data','pe')
			leg.AddEntry(zjets,'Z+jets','f')
			leg.AddEntry(ttbar,'t#bar{t}+jets','f')
			leg.AddEntry(VV,'VV','f')
			leg.AddEntry(other,'Other background','f')
		if 'uvjj' in channel:
			leg.AddEntry(dataTGraph,'Data','pe')
			leg.AddEntry(wjets,'W+jets','f')
			leg.AddEntry(ttbar,'t#bar{t}+jets','f')
			leg.AddEntry(VV,'VV','f')
			leg.AddEntry(other,'Other background','f')
		leg.AddEntry(totBG,'stat + syst uncertainty','f')
		leg.AddEntry(sig,'LQ signal','l')
		leg.Draw()
		if isPAS:
			l1.DrawLatex(0.13,0.94,"                                                35.9 fb^{-1} (13 TeV)")
		else:
			l1.DrawLatex(0.13,0.94,"#it{Preliminary}                              35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.86,"CMS")
		if 'uujj' in channel:
			l3.DrawLatex(0.155,0.8,"#mu#mujj")
		if 'uvjj' in channel:
			l3.DrawLatex(0.155,0.8,"#mu#nujj")
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_finalSelectionPlot.pdf')
		print 'Saving histogram.... Results_'+version_name+'/BasicLQ_'+channel+'_finalSelectionPlot.pdf'

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
#ROOT.v5.TFormula.SetMaxima(100000,1000,1000000)
import numpy
import math
rnd= TRandom3()
person = (os.popen('whoami').readlines()[0]).replace("\n",'')


#if '/store' in NormalDirectory:#fixme removing since eos is hosted on /eos now
#	NormalFiles = [(x.split('/')[-1]).replace('\n','') for x in os.popen('cmsLs '+NormalDirectory+"| grep \".root\" | awk '{print $1}'").readlines()]
#else:
NormalFiles = [ff.replace('\n','') for ff in os.popen('ls '+NormalDirectory+"| grep \".root\"").readlines()]

#if '/store' in EMuDirectory:#fixme removing since eos is hosted on /eos now
#	EMuFiles = [(x.split('/')[-1]).replace('\n','') for x in os.popen('cmsLs '+EMuDirectory+"| grep \".root\" | awk '{print $1}'").readlines()]
#else:
EMuFiles = [ff.replace('\n','') for ff in os.popen('ls '+EMuDirectory+"| grep \".root\"").readlines()]

#if '/store' in QCDDirectory:	#fixme removing since eos is hosted on /eos now
#	QCDFiles = [(x.split('/')[-1]).replace('\n','') for x in os.popen('cmsLs '+QCDDirectory+"| grep \".root\" | awk '{print $1}'").readlines()]
#else:
QCDFiles = [ff.replace('\n','') for ff in os.popen('ls '+QCDDirectory+"| grep \".root\"").readlines()]

for f in NormalFiles:
	_tree = 't_'+f.split('/')[-1].replace(".root","")
	_treeTmp = _tree+"_tmp"
	_prefix = ''# +'root://eoscms//eos/cms'*('/store' in NormalDirectory)#fixme removing since eos is hosted on /eos now
	print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	#print (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	#print (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

for f in EMuFiles:
	_tree = 'te_'+f.split('/')[-1].replace(".root","")	
	_treeTmp = _tree+"_tmp"
	_prefix = ''# +'root://eoscms//eos/cms'*('/store' in EMuDirectory)#fixme removing since eos is hosted on /eos now	
	print(_tree+" = TFile.Open(\""+_prefix+EMuDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+EMuDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

for f in QCDFiles:
	_tree = 'tn_'+f.split('/')[-1].replace(".root","")
	_treeTmp = _tree+"_tmp"
	_prefix = ''# +'root://eoscms//eos/cms'*('/store' in QCDDirectory)#fixme removing since eos is hosted on /eos now	
	print(_tree+" = TFile.Open(\""+_prefix+QCDDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	exec (_treeTmp+" = TFile.Open(\""+_prefix+QCDDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")


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

	for f in NormalFiles:
		_tree = 't_'+f.split('/')[-1].replace(".root","")
		_treeTmp = _tree+"_tmp"
		_prefix = ''# +'root://eoscms//eos/cms'*('/store' in NormalDirectory)#fixme removing since eos is hosted on /eos now
		print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	        #print (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
		exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	        #print (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")
		exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

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
	nnpdfweights = [['*(factor_nnpdf_'+str(n+1)+')','*(abs(factor_nnpdf_'+str(n+1)+')<100)'] for n in range(N_nnpdf)]
	#nnpdfNoInf   = ['*((factor_nnpdf_'+str(n+1)+')<100)' for n in range(N_nnpdf)]
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
			MuNuSels.append([line.split('=')[0].replace('\n','').replace(' ','').replace('opt_LQuvjj',''),line.split('=')[-1].replace('\n','').replace(' ','')])
			


	# UUJJ CHANNEL SYSTEMATICS

	#treenames = ['ZJets','TTBar','WJets','VV','sTop','QCD','Signal']#original
	#treenames = ['ZJets','TTBar']#,'Signal']#fixme removing signal
	#treenames = ['WJets','VV','sTop','QCD']
	treenames = ['WJets','VV','sTop']
	uncnames = ['pdf_uujj_'+x for x in treenames]
	#trees  = [[t_ZJets]]
       	#trees  = [[t_ZJets],[t_TTBar],[t_WJets],[t_DiBoson],[t_SingleTop],[t_QCDMu]]#original
	#trees  = [[t_ZJets],[t_TTBar]]
	#trees = [[t_WJets],[t_DiBoson],[t_SingleTop],[t_QCDMu]]
	trees = [[t_WJets],[t_DiBoson],[t_SingleTop]]
	#treesNames = [['t_WJets'],['t_ZJets'],['t_DiBoson'],['t_SingleTop'],['t_QCDMu']]#original
	#treesNames = [['t_ZJets'],['t_TTBar']]
	#treesNames = [['t_WJets'],['t_DiBoson'],['t_SingleTop'],['t_QCDMu']]
	treesNames = [['t_WJets'],['t_DiBoson'],['t_SingleTop']]
	#trees.append([t_LQuujj200,t_LQuujj250,t_LQuujj300,t_LQuujj350,t_LQuujj400,t_LQuujj450,t_LQuujj500,t_LQuujj550,t_LQuujj600,t_LQuujj650,t_LQuujj700,t_LQuujj750,t_LQuujj800,t_LQuujj850,t_LQuujj900,t_LQuujj950,t_LQuujj1000,t_LQuujj1050,t_LQuujj1100,t_LQuujj1150,t_LQuujj1200,t_LQuujj1250,t_LQuujj1300,t_LQuujj1350,t_LQuujj1400,t_LQuujj1450,t_LQuujj1500,t_LQuujj1550,t_LQuujj1600,t_LQuujj1650,t_LQuujj1700,t_LQuujj1750,t_LQuujj1800,t_LQuujj1850,t_LQuujj1900,t_LQuujj1950,t_LQuujj2000])
	#treesNames.append(['t_LQuujj200','t_LQuujj250','t_LQuujj300','t_LQuujj350','t_LQuujj400','t_LQuujj450','t_LQuujj500','t_LQuujj550','t_LQuujj600','t_LQuujj650','t_LQuujj700','t_LQuujj750','t_LQuujj800','t_LQuujj850','t_LQuujj900','t_LQuujj950','t_LQuujj1000','t_LQuujj1050','t_LQuujj1100','t_LQuujj1150','t_LQuujj1200','t_LQuujj1250','t_LQuujj1300','t_LQuujj1350','t_LQuujj1400','t_LQuujj1450','t_LQuujj1500','t_LQuujj1550','t_LQuujj1600','t_LQuujj1650','t_LQuujj1700','t_LQuujj1750','t_LQuujj1800','t_LQuujj1850','t_LQuujj1900','t_LQuujj1950','t_LQuujj2000'])

	
	# ================================================================================================================
	# Loop over trees to consider
	for ii in range(len(trees)):
		junkfile = TFile.Open('myjunkfileforpdfanalysis_'+str(random.randint(1,999))+'.root','RECREATE')

		# Speed up by copying to new preselection tree
		ntree = 0
		systematic = '0.0'
		_t = trees[ii][ntree]
		norm_sel = '(1.0)'
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
		presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact[0]+_fact[1],1.0)[0] for _fact in nnpdfweights]
		# Loop over selections
		for _sel in MuMuSels:
			#print '   ... using tree',trees[ii][ntree]
			print '   ... using tree',treesNames[ii][ntree],'for m_LQ =',_sel[0]
			if 'Signal' in uncnames[ii]:
				_t = trees[ii][ntree]
				ntree += 1
				_tnew = _t.CopyTree(preselectionmumu + '*'+norm_sel)
				# Get the preselection values for all PDF members
				presel_central_value = QuickIntegral(_tnew,NormalWeightMuMu,1.0)[0]
				#print 'presel central:',presel_central_value
				#if 'Signal' in uncnames[ii]:
				#	presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweightsSig]#fixme update when names are uniform across samples
				#	presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in nnpdfweightsSig]
				#	presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in mmthweightsSig]
				#else:
				#presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in cteqweights]#fixme update when names are uniform across samples
				#presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact,1.0)[0] for _fact in mmthweights]
				#print [_fact[0]+_fact[1] for _fact in nnpdfweights]
				presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuMu+_fact[0]+_fact[1],1.0)[0] for _fact in nnpdfweights]
				#print NormalWeightMuMu+_fact[0]+_fact[1]
				#print 'presel varied:',presel_varied_nnpdf_values
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
			finsel_varied_nnpdf_values = [QuickIntegral(_tnewsel,NormalWeightMuMu+_fact[0]+_fact[1],1.0)[0] for _fact in nnpdfweights]
			#print 'final varied:',finsel_varied_nnpdf_values

			# Normalize Z and Signal at preselection #fixme removing signal
			if 'ZJet' in uncnames[ii] :#or 'Signal' in uncnames[ii]:
				finsel_central_value /= presel_central_value
				#finsel_varied_cteq_values = [finsel_varied_cteq_values[jj]/presel_varied_cteq_values[jj] for jj in range(len(presel_varied_cteq_values))]
				#finsel_varied_mmth_values = [finsel_varied_mmth_values[jj]/presel_varied_mmth_values[jj] for jj in range(len(presel_varied_mmth_values))]
				finsel_varied_nnpdf_values = [finsel_varied_nnpdf_values[jj]/presel_varied_nnpdf_values[jj] for jj in range(len(presel_varied_nnpdf_values))]

			if finsel_central_value >0.0:
				# Get the variations w.r.t the central member
				#finsel_varied_cteq_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_cteq_values]
				#finsel_varied_mmth_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_mmth_values]
				#finsel_varied_nnpdf_diffs =[(abs(x - finsel_central_value)*(abs(x - finsel_central_value)<5))/finsel_central_value for x in  finsel_varied_nnpdf_values]#fixme not allowing pdf differences greater than 5
				finsel_varied_nnpdf_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_nnpdf_values]

				#sfinsel_varied_cteq_diffs = [(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_cteq_values]
				#sfinsel_varied_mmth_diffs = [(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_mmth_values]
				#sfinsel_varied_nnpdf_diffs =[((x - finsel_central_value)*(abs(x - finsel_central_value)<5))/finsel_central_value for x in  finsel_varied_nnpdf_values]
				sfinsel_varied_nnpdf_diffs = [abs(x - finsel_central_value)/finsel_central_value for x in  finsel_varied_nnpdf_values]

				# Adjust cteq to 68% CL
				#finsel_varied_cteq_diffs = [xx/1.645  for xx in finsel_varied_cteq_diffs]
				#ResultDict[uncnames[ii]+'_uujj']['cteq'].append(  [100*jj for jj in sfinsel_varied_cteq_diffs])
				#ResultDict[uncnames[ii]+'_uujj']['mmth'].append(  [100*jj for jj in sfinsel_varied_mmth_diffs])
				ResultDict[uncnames[ii]+'_uujj']['nnpdf'].append( [100*jj for jj in sfinsel_varied_nnpdf_diffs])
		

				old_systematic = str(systematic)
				#systematic = str(round(100.0*max( finsel_varied_cteq_diffs + finsel_varied_mmth_diffs + finsel_varied_nnpdf_diffs ),3))
				#print finsel_varied_nnpdf_diffs
				#print finsel_varied_nnpdf_values
				systematic = str(round(100.0*max(finsel_varied_nnpdf_diffs),3))
				if float(systematic) < float(old_systematic):
					systematic = str(old_systematic)

				if float(systematic) > 100.0:
					systematic = '100.0'
			else:
				#ResultDict[uncnames[ii]+'_uujj']['cteq'].append(  ResultDict[uncnames[ii]+'_uujj']['cteq'][-1] )
				#ResultDict[uncnames[ii]+'_uujj']['mmth'].append(  ResultDict[uncnames[ii]+'_uujj']['mmth'][-1] )
				ResultDict[uncnames[ii]+'_uujj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uujj']['nnpdf'][-1] )		
			#print finsel_central_value
			print systematic+'%'
			result += systematic+','
			junkfile.Close()


		result = result[:-1]+']'
		ResultList.append(result)
	
	# ================================================================================================================
	# UVJJ CHANNEL SYSTEMATICS

	#treenames = ['TTBar','WJets']#,'Signal']#fixme removing signal
	#treenames = ['VV','sTop','QCD']
	treenames = ['VV','sTop']
	uncnames = ['pdf_uvjj_'+x for x in treenames]
	#trees  = [[t_TTBar],[t_WJets]]
	#trees = [[t_DiBoson],[t_SingleTop],[t_QCDMu]]
	trees = [[t_DiBoson],[t_SingleTop]]
	#treesNames = [['t_TTBar'],['t_WJets']]
	#treesNames = [['t_DiBoson'],['t_SingleTop'],['t_QCDMu']]
	treesNames = [['t_DiBoson'],['t_SingleTop']]
	#trees.append([t_LQuvjj200,t_LQuvjj250,t_LQuvjj300,t_LQuvjj350,t_LQuvjj400,t_LQuvjj450,t_LQuvjj500,t_LQuvjj550,t_LQuvjj600,t_LQuvjj650,t_LQuvjj700,t_LQuvjj750,t_LQuvjj800,t_LQuvjj850,t_LQuvjj900,t_LQuvjj950,t_LQuvjj1000,t_LQuvjj1050,t_LQuvjj1100,t_LQuvjj1150,t_LQuvjj1200,t_LQuvjj1250,t_LQuvjj1300,t_LQuvjj1350,t_LQuvjj1400,t_LQuvjj1450,t_LQuvjj1500,t_LQuvjj1550,t_LQuvjj1600,t_LQuvjj1650,t_LQuvjj1700,t_LQuvjj1750,t_LQuvjj1800,t_LQuvjj1850,t_LQuvjj1900,t_LQuvjj1950,t_LQuvjj2000])
	#treesNames.append(['t_LQuvjj200','t_LQuvjj250','t_LQuvjj300','t_LQuvjj350','t_LQuvjj400','t_LQuvjj450','t_LQuvjj500','t_LQuvjj550','t_LQuvjj600','t_LQuvjj650','t_LQuvjj700','t_LQuvjj750','t_LQuvjj800','t_LQuvjj850','t_LQuvjj900','t_LQuvjj950','t_LQuvjj1000','t_LQuvjj1050','t_LQuvjj1100','t_LQuvjj1150','t_LQuvjj1200','t_LQuvjj1250','t_LQuvjj1300','t_LQuvjj1350','t_LQuvjj1400','t_LQuvjj1450','t_LQuvjj1500','t_LQuvjj1550','t_LQuvjj1600','t_LQuvjj1650','t_LQuvjj1700','t_LQuvjj1750','t_LQuvjj1800','t_LQuvjj1850','t_LQuvjj1900','t_LQuvjj1950','t_LQuvjj2000'])


	
	# ================================================================================================================
	# Loop over trees to consider
	for ii in range(len(trees)):
		junkfile = TFile.Open('myjunkfileforpdfanalysis_'+str(random.randint(1,999))+'.root','RECREATE')

		# Speed up by copying to new preselection tree
		ntree = 0
		systematic = '0.0'
		_t = trees[ii][ntree]
		norm_sel = '(1)'
		print 'Analyzing',  uncnames[ii], 'in the uvjj channel. Systematics are:'
		result = uncnames[ii]+' = ['
		ResultDict[uncnames[ii]+'_uvjj'] = {}
		#ResultDict[uncnames[ii]+'_uvjj']['cteq'] = []
		#ResultDict[uncnames[ii]+'_uvjj']['mmth'] = []
		ResultDict[uncnames[ii]+'_uvjj']['nnpdf'] = []				
		result = uncnames[ii]+' = ['
		if 'WJets' in uncnames[ii]:
			norm_sel = '(MT_uv>70)*(MT_uv<110)*(JetCount<3.5)*(((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)'
		if 'TTBar' in uncnames[ii]:
			norm_sel = '(MT_uv>70)*(MT_uv<110)*(JetCount>3.5)*(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>=1)'		
		_tnew = _t.CopyTree(preselectionmunu + '*'+norm_sel)
		# Get the preselection values for all PDF members
		presel_central_value = QuickIntegral(_tnew,NormalWeightMuNu,1.0)[0]
		#presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in cteqweights]
		#presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in mmthweights]
		presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact[0]+_fact[1],1.0)[0] for _fact in nnpdfweights]
		# Loop over selections
		for _sel in MuNuSels:
			print '   ... using tree',treesNames[ii][ntree],'for m_LQ =',_sel[0]
			if 'Signal' in uncnames[ii]:
				_t = trees[ii][ntree]
				ntree += 1
				_tnew = _t.CopyTree(preselectionmunu + '*'+norm_sel)
				# Get the preselection values for all PDF members
				presel_central_value = QuickIntegral(_tnew,NormalWeightMuNu,1.0)[0]
				#presel_varied_cteq_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in cteqweights]
				#presel_varied_mmth_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact,1.0)[0] for _fact in mmthweights]
				presel_varied_nnpdf_values = [QuickIntegral(_tnew,NormalWeightMuNu+_fact[0]+_fact[1],1.0)[0] for _fact in nnpdfweights]

			# Copy tree to new final selection tree
			_tnewsel = _t.CopyTree(preselectionmunu+'*'+_sel[1])
			if _tnewsel.GetEntries()<50  and ResultDict[uncnames[ii]+'_uvjj']['nnpdf'] != []:
				#ResultDict[uncnames[ii]+'_uvjj']['cteq'].append(  ResultDict[uncnames[ii]+'_uvjj']['cteq'][-1] )
				#ResultDict[uncnames[ii]+'_uvjj']['mmth'].append(  ResultDict[uncnames[ii]+'_uvjj']['mmth'][-1] )
				ResultDict[uncnames[ii]+'_uvjj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uvjj']['nnpdf'][-1] )	
				continue				
			# Get the final-selection integrals
			finsel_central_value=QuickIntegral(_tnewsel,NormalWeightMuNu,1.0)[0]
			#finsel_varied_cteq_values = [QuickIntegral(_tnewsel,NormalWeightMuNu+_fact,1.0)[0] for _fact in cteqweights]
			#finsel_varied_mmth_values = [QuickIntegral(_tnewsel,NormalWeightMuNu+_fact,1.0)[0] for _fact in mmthweights]
			finsel_varied_nnpdf_values = [QuickIntegral(_tnewsel,NormalWeightMuNu+_fact[0]+_fact[1],1.0)[0] for _fact in nnpdfweights]

			# Normalize W, TTBar, and Z at preselection
			if 'WJet' in uncnames[ii] or 'TTBar' in uncnames[ii] or 'Signal' in uncnames[ii]:
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
				#ResultDict[uncnames[ii]+'_uvjj']['cteq'].append([100*jj for jj in sfinsel_varied_cteq_diffs])
				#ResultDict[uncnames[ii]+'_uvjj']['mmth'].append([100*jj for jj in sfinsel_varied_mmth_diffs])
				ResultDict[uncnames[ii]+'_uvjj']['nnpdf'].append([100*jj for jj in sfinsel_varied_nnpdf_diffs])

				old_systematic = str(systematic)
				#systematic = str(round(100.0*max( finsel_varied_cteq_diffs + finsel_varied_mmth_diffs + finsel_varied_nnpdf_diffs ),3))
				systematic = str(round(100.0*max(finsel_varied_nnpdf_diffs),3))
				if float(systematic) < float(old_systematic):
					systematic = str(old_systematic)

				if float(systematic) > 100.0:
					systematic = '100.0'
			else:
				#ResultDict[uncnames[ii]+'_uvjj']['cteq'].append(  ResultDict[uncnames[ii]+'_uvjj']['cteq'][-1] )
				#ResultDict[uncnames[ii]+'_uvjj']['mmth'].append(  ResultDict[uncnames[ii]+'_uvjj']['mmth'][-1] )
				ResultDict[uncnames[ii]+'_uvjj']['nnpdf'].append( ResultDict[uncnames[ii]+'_uvjj']['nnpdf'][-1] )	
			print systematic+'%'
			result += systematic+','
			junkfile.Close()

		result = result[:-1]+']'
		ResultList.append(result)
	
	json_name = 'Results_'+versionname+'/PDFVariationsDictionary.json'
	print ' -------- Creating JSON file:',json_name
	import json
	json.dump(ResultDict, open(json_name, 'wb'))
	

	#print '\n\n---------- Summary of PDF systematics as percentages --------\n'
	# for result in ResultList:
	# 	print result
	# print '\n\n'



def PDF4LHCPlotsFromResultDict(filename,versionname):
	import json
	dictionary = json.load(open(filename))
	
	mass = [200 + x*50 for x in range(37)]

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
		chan = '#mu#mu jj'*('uujj' in basename) + '#mu#nu jj'*('uvjj' in basename)
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

		cteq,mmth,nnpd = [],[],[]
		old_systematic = 0.0
		systematic = 0.0
		for imass in range(len(mass)):


			#old_cteq = list(cteq)
			#old_mmth = list(mmth)
			old_nnpd = list(nnpd)

			#cteq = data['cteq'][imass]
			#mmth = data['mmth'][imass]
			nnpd = data['nnpdf'][imass]

			#if cteq == old_cteq or old_cteq == [0]:
			#	cteq = [0]
			#if mmth == old_mmth or old_mmth == [0]:
			#	mmth = [0]
			if nnpd == old_nnpd or  old_nnpd == [0]:
				nnpd = [0]

			#C, M, N = array('d',cteq), array('d',mmth), array('d',nnpd)
			N = array('d',nnpd)
			m = mass[imass]
			#Cm = array('d',[m for x in C])
			#Mm = array('d',[m-7. for x in M])
			Nm = array('d',[m+7. for x in N])

			# print C
			#Crms.append(rms(C))
			#Mrms.append(rms(M))
			Nrms.append(rms(N))

			old_systematic = systematic
			#systematic = max([ Crms[-1],Mrms[-1],Nrms[-1] ])
			systematic = Nrms[-1]
			if systematic < old_systematic:
				systematic = old_systematic
			result += (str(round(systematic,2))) + ','
			Ms.append(1.0*m)

			#hlist.append(TGraph(len(C), Cm, C))
			#hlist[-1].SetMarkerStyle(24)
			#hlist[-1].SetMarkerColor(6)
			#hlist[-1].SetMarkerSize(0.3)

			#hlist.append(TGraph(len(M), Mm, M))
			#hlist[-1].SetMarkerStyle(24)
			#hlist[-1].SetMarkerColor(2)
			#hlist[-1].SetMarkerSize(0.3)	

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


		#Crmsclone = list(Crms)
		#Mrmsclone = list(Mrms)
		Nrmsclone = list(Nrms)
		Msclone = list(Ms)

		for xx in range(len(Nrms)):
			#Crms.append(-1.0*Crmsclone[-1-xx])
			#Mrms.append(-1.0*Mrmsclone[-1-xx])
			Nrms.append(-1.0*Nrmsclone[-1-xx])
			Ms.append(Msclone[-1-xx])

		#Crms.append(Crms[0])
		#Mrms.append(Mrms[0])
		Nrms.append(Nrms[0])
		Ms.append(Ms[0])

		#Crms = array('d',Crms)
		#Mrms = array('d',Mrms)
		Nrms = array('d',Nrms)
		Ms = array('d',Ms)

		#cwin = TPolyLine(len(Crms),Ms,Crms,"")
		#cwin.SetFillColor(6)
		#cwin.SetLineColor(6)
		#cwin.SetLineWidth(2)
		#cwin.Draw("L")

		#mwin = TPolyLine(len(Mrms),Ms,Mrms,"")
		#mwin.SetFillColor(2)
		#mwin.SetLineColor(2)
		#mwin.SetLineWidth(2)
		#mwin.Draw("L")

		nwin = TPolyLine(len(Nrms),Ms,Nrms,"")
		nwin.SetFillColor(4)
		nwin.SetLineColor(4)
		nwin.SetLineWidth(2)
		nwin.Draw("L")

		#ch=TH1F()
		#ch.SetLineColor(6)
		#ch.SetMarkerColor(6)
		#ch.SetLineWidth(2)

		#mh=TH1F()
		#mh.SetLineColor(2)
		#mh.SetMarkerColor(2)
		#mh.SetLineWidth(2)

		nh=TH1F()
		nh.SetLineColor(4)
		nh.SetMarkerColor(4)
		nh.SetLineWidth(2)

		#leg.AddEntry(ch,"CT10")
		#leg.AddEntry(mh,"MMTH")
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
		#binBG = bg.GetBinContent(bins)
		#bin = data.GetY()[bins]
		binBG = bg.GetStack().Last().GetBinContent(bins)
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
			if blinded==False:
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
	hout.GetXaxis().SetLabelSize(0.06)
	hout.GetYaxis().SetLabelSize(0.06)

	hout.GetXaxis().SetTitleOffset(0.92)
	hout.GetYaxis().SetTitleOffset(0.92)
	hout.GetXaxis().SetTitleSize(0.06)
	hout.GetYaxis().SetTitleSize(0.06)
	#hout.GetXaxis().CenterTitle(1)
	#hout.GetYaxis().CenterTitle(1)

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
	stack.GetHistogram().GetXaxis().SetLabelSize(0.0505)
	stack.GetHistogram().GetYaxis().SetLabelSize(0.0505)

	stack.GetHistogram().GetXaxis().SetTitleOffset(0.925)
	stack.GetHistogram().GetYaxis().SetTitleOffset(0.9)
	stack.GetHistogram().GetXaxis().SetTitleSize(0.07)
	stack.GetHistogram().GetYaxis().SetTitleSize(0.07)
	#stack.GetHistogram().GetXaxis().CenterTitle(1)
	#stack.GetHistogram().GetYaxis().CenterTitle(1)
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

def VVStudy(sel_mumu,sel_munu,cutlogmumu,cutlogmunu,weight_mumu,weight_munu,version_name):
	print '\n\n--------------\n--------------\nPerforming VV Study'
	#################################
	######## DIMUON CHANNEL #########
	#################################	
	print '\n------ DIMUON CHANNEL -------\n'


	stbinning = [280 ,300]
	lqbinning = [-20,0]
	for x in range(29):#was 22 then 27
		stbinning.append(stbinning[-1]+10+stbinning[-1]-stbinning[-2])
	for x in range(28):#was 22 then 28
		lqbinning.append(lqbinning[-1]+5+lqbinning[-1]-lqbinning[-2])
	stbinningTT = stbinning[1:20]
	stbinning = stbinning[1:]
	lqbinningTT = lqbinning[1:20]
	lqbinning = lqbinning[1:]
	bosonbinning = [50,60,70,80,90,100,110,120]
	for x in range(55):
		if bosonbinning[-1]<1800:
			bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.075 )#was 1.2	       	
	bosonbinning = [round(x) for x in bosonbinning]

	vvControl = sel_mumu+'*(M_jj>70)*(M_jj<110)'
	vvControlMuMu = sel_mumu+'*(M_jj>70)*(M_jj<110)'
	vvControlMuNu = sel_munu+'*(M_jj>70)*(M_jj<110)'
	vvControl3Mu  = sel_mumu+'*(MuonCount>2)'


	Rz_uujj=0.925#[0.925,0.005]
	Rtt_uujj=1.0#[1.000,0.023]
	Rw_uvjj=0.9#[0.9,0.009]
	Rtt_uvjj=1.023#[1.023,0.008]

	MakeBasicPlot("M_jj","m_{jj} [GeV]",[40,70,110],vvControlMuMu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_VVcontrol','uujj',Rz_uujj,Rw_uvjj,Rtt_uujj,'',version_name,1000)
	MakeBasicPlot("M_jj","m_{jj} [GeV]",[40,70,110],vvControlMuNu,NormalWeightMuNu,NormalDirectory,'standard_VVcontrol','uvjj',Rz_uujj,Rw_uvjj,Rtt_uujj,'',version_name,1000)
	#Checks for 3 lepton
	MakeBasicPlot("M_uu","m_{#mu#mu} [GeV]",bosonbinning,vvControl3Mu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_VVcontrol3Mu','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)
	MakeBasicPlot("M_jj","m_{jj} [GeV]",bosonbinning,vvControl3Mu,NormalWeightMuMu,NormalDirectory,'standard_TTBarDataDriven_VVcontrol3Mu','uujj',Rz_uujj, Rw_uvjj,Rtt_uujj,'',version_name,1000)

	vLO = QuickIntegral(t_DiBoson_Pythia,sel_mumu+'*'+weight_mumu,1.0)
	vNLO = QuickIntegral(t_DiBoson_amcNLO,sel_mumu+'*'+weight_mumu,1.0)

	Vscale = vNLO[0]/vLO[0]
	VscaleErr = (vNLO[0]/vLO[0])*math.sqrt(((vNLO[1]*vNLO[1])/(vNLO[0]*vNLO[0]))+((vLO[1]*vLO[1])/(vLO[0]*vLO[0])))

	print 'uujj VV NLO / LO scale factor:',Vscale,'+-',VscaleErr
	
	MakeBasicPlotVV("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',1, 1,1,version_name,Vscale)
	MakeBasicPlotVV("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',1, 1,1,version_name,Vscale)
	MakeBasicPlotVV("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',1, 1,1,version_name,Vscale)
	MakeBasicPlotVV("Pt_muon2","p_{T}(#mu_{2}) [GeV]",ptbinning2,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',1, 1,1,version_name,Vscale)
	MakeBasicPlotVV("St_uujj","S_{T}^{#mu#mujj} [GeV]",stbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',1, 1,1,version_name,Vscale)
	MakeBasicPlotVV("M_uu","m_{#mu#mu} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',1, 1,1,version_name,Vscale)
	MakeBasicPlotVV("M_uujj2","m_{#muj}_{2} [GeV]",lqbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',1, 1,1,version_name,Vscale)
	MakeBasicPlotVV("M_jj","m_{jj} [GeV]",bosonbinning,preselectionmumu,NormalWeightMuMu,NormalDirectory,'standard','uujj',1, 1,1,version_name,Vscale)
        # UVJJ plots at preselection
	

	vLO = QuickIntegral(t_DiBoson_Pythia,sel_munu+'*'+weight_munu,1.0)
	vNLO = QuickIntegral(t_DiBoson_amcNLO,sel_munu+'*'+weight_munu,1.0)

	Vscale = vNLO[0]/vLO[0]
	VscaleErr = (vNLO[0]/vLO[0])*math.sqrt(((vNLO[1]*vNLO[1])/(vNLO[0]*vNLO[0]))+((vLO[1]*vLO[1])/(vLO[0]*vLO[0])))

	print 'uvjj VV NLO / LO scale factor:',Vscale,'+-',VscaleErr
		
	stbinning = [280 ,300]
	lqbinning = [-20,0]
	for x in range(18):
		stbinning.append(stbinning[-1]+45+stbinning[-1]-stbinning[-2])
	for x in range(20):
		lqbinning.append(lqbinning[-1]+20+lqbinning[-1]-lqbinning[-2])
	stbinning = stbinning[1:]
	lqbinning = lqbinning[1:]
	bosonbinning = [50,60,70,80,90,100,110,120]
	for x in range(55):
		if bosonbinning[-1]<1600:
			bosonbinning.append(bosonbinning[-1]+ (bosonbinning[-1] - bosonbinning[-2])*1.3 )#was 1.2	       	
	bosonbinning = [round(x) for x in bosonbinning]
	MakeBasicPlotVV("MT_uv","m_{T}^{#mu#nu} [GeV]",bosonbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',1, 1,1,version_name,1)
	MakeBasicPlotVV("Pt_jet1","p_{T}(jet_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',1, 1,1,version_name,1)
	MakeBasicPlotVV("Pt_jet2","p_{T}(jet_{2}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',1, 1,1,version_name,1)
	MakeBasicPlotVV("Pt_muon1","p_{T}(#mu_{1}) [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',1, 1,1,version_name,1)
	MakeBasicPlotVV("Pt_miss","E_{T}^{miss} [GeV]",ptbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',1, 1,1,version_name,1)
	MakeBasicPlotVV("St_uvjj","S_{T}^{#mu#nujj} [GeV]",stbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',1, 1,1,version_name,1)
	MakeBasicPlotVV("M_uvjj","m_{#muj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',1, 1,1,version_name,1)
	MakeBasicPlotVV("M_jj","m_{jj} [GeV]",lqbinning,preselectionmunu,NormalWeightMuNu,NormalDirectory,'standard','uvjj',1, 1,1,version_name,1)



def QCDStudy(sel_mumu,sel_munu,sel_munuVal,cutlogmumu,cutlogmunu,weight_mumu,weight_munu,version_name):
	print '\n\n--------------\n--------------\nPerforming QCD Study'
	#################################
	######## DIMUON CHANNEL #########
	#################################	
	print '\n------ DIMUON CHANNEL -------\n'
	#intQCDMu = QuickIntegral(tn_QCDMu,sel_mumu+"*"+weight_mumu,1.0)
	#intQCDMuReweight = QuickIntegral(tn_QCDMu,sel_mumu+"*"+weight_mumu+"*(1./pow(ptHat,4.5))",1.0)
	#ptHatReweight = intQCDMu[0] / intQCDMuReweight[0]
	#ptHatReweightStr = str(ptHatReweight)
	#intQCDMuNu = QuickIntegral(tn_QCDMu,sel_munu+"*"+weight_munu,1.0)
	#intQCDMuReweightNu = QuickIntegral(tn_QCDMu,sel_munu+"*"+weight_munu+"*(1./pow(ptHat,4.5))",1.0)
	#ptHatReweightNu = intQCDMuNu[0] / intQCDMuReweightNu[0]
	#ptHatReweightStr = str(ptHatReweight)
	#ptHatReweightStrNu = str(ptHatReweightNu)
	#weight_mumu_qcd = weight_mumu+"*(1./pow(ptHat,4.5))*"+ptHatReweightStr
	#weight_munu_qcd = weight_munu+"*(1./pow(ptHat,4.5))*"+ptHatReweightStrNu
	#Q_ss = QuickIntegral(tn_QCDMu,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu_qcd,1.0)	
	#Q_os = QuickIntegral(tn_QCDMu,sel_mumu + '*(Charge_muon1*Charge_muon2 < 0)*'+weight_mumu_qcd,1.0)
	
	realnoniso = '*(TrkIso_muon1>0.1)*(TrkIso_muon2>0.1)'

	D_noniso_uujj = QuickEntries(tn_SingleMuData,sel_mumu+realnoniso+dataHLT,1.0)	
	Q_noniso_uujj = QuickIntegral(tn_QCDMu,sel_mumu+realnoniso+'*'+weight_mumu,1.0)	
	B_noniso_uujj = QuickMultiIntegral([tn_DiBoson,tn_TTBar,tn_WJets,tn_ZJets,tn_SingleTop],sel_mumu+realnoniso+'*'+weight_mumu,[1.0,1.0,1.0,1.0,1.0])
	ScaleFactor_QCD_uujj = (D_noniso_uujj[0] - B_noniso_uujj[0])/Q_noniso_uujj[0]
	ScaleFactor_QCD_uujj_Err  = (math.sqrt((math.sqrt(D_noniso_uujj[1]**2 + B_noniso_uujj[1]**2)/(D_noniso_uujj[0] - B_noniso_uujj[0]))**2 + (Q_noniso_uujj[1]/Q_noniso_uujj[0])**2))*ScaleFactor_QCD_uujj

	print'\n In the non-isolated region (TrkIso_muon1>0.1)*(TrkIso_muon2>0.1), uujj global QCD rescaling is:', texentry4([ScaleFactor_QCD_uujj,ScaleFactor_QCD_uujj_Err])


	Q_ss = QuickIntegral(tn_QCDMu,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)	
	Q_os = QuickIntegral(tn_QCDMu,sel_mumu + '*(Charge_muon1*Charge_muon2 < 0)*'+weight_mumu,1.0)


	print 'Number of events in QCD MC:'
	print 'Q_ss:',Q_ss
	print 'Q_os:',Q_os

	#D_ss = QuickIntegral(tn_QCDMu,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print 'Test: In normal Iso data, the number of same-sign events is',QuickEntries(t_SingleMuData,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)' + dataHLT,1.0)
	print 'Test: In normal Iso MC, the number of same-sign events is'
	print '    Z:',QuickIntegral(t_ZJets,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print '    W:',QuickIntegral(t_WJets,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print '    t:',QuickIntegral(t_SingleTop,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print '   VV:',QuickIntegral(t_DiBoson,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print '   tt:',QuickIntegral(t_TTBar,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,1.0)
	print 'Test: QCD Prediction in SS Isolated:', QuickIntegral(tn_QCDMu,sel_mumu + '*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu+'*(TrkIso_muon1<0.1)*(TrkIso_muon2<0.1)',1.0)

	#sys.exit()
	
	studyvals = []
	for x in range(10000):#fixme todo changed from 1,000 to 10,000
		same = RR(Q_ss)
		opp = RR(Q_os)	
		studyvals.append( (same + opp) /same )
	sameoppscale =  GetStats(studyvals)
	print "\nIn QCD MC, the conversion factor between same-sign muon events and all events is:", texentry4(sameoppscale)

	Q_ssiso = QuickIntegral(tn_QCDMu,sel_mumu+'*(TrkIso_muon1<0.1)*'+weight_mumu,1.0)
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
	MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,2.0,5.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,2.0,5.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,1.0)

	MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,2.0,5.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_noniso_weightedtagfree','uujj',1.0,1.0,1.0,version_name,ScaleFactor_QCD_uujj)
	MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,2.0,5.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_noniso_weightedtagfree','uujj',1.0,1.0,1.0,version_name,ScaleFactor_QCD_uujj)



	#MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,1.5,2.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisoPAStagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	#MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,1.5,2.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisoPAStagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	#fixme todo added SSNonIsoDataRescale for data rescale
	###MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.02,0.04,0.075,0.1,0.15,0.2,0.4,0.75,1.0,1.5,2.0,3.5],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu_qcd,weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	###MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.02,0.04,0.075,0.1,0.15,0.2,0.4,0.75,1.0,1.5,2.0,3.5],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu_qcd,weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,1.0)
	####MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",qcdBinning,sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu+'*(Charge_muon1*Charge_muon2 > 0)',weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,SSNonIsoDataRescale[0])
	####MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",qcdBinning,sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu+'*(Charge_muon1*Charge_muon2 > 0)',weight_mumu,NormalDirectory,'qcd_nonisotagfree','uujj',1.0,1.0,1.0,version_name,SSNonIsoDataRescale[0])
	#MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",[0.001,0.05,0.1,0.2,0.5,1.0,1.5,2.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisoPAStagfree','uujj',1.0,1.0,1.0,version_name,SSNonIsoDataRescale[0])
	#MakeBasicPlotQCD("TrkIso_muon2","Tracker Rel Iso Second Mu  (non-isolated)",[0.001,0.05,0.10,0.2,0.5,1.0,1.5,2.0],sel_mumu_ss,sel_mumu_ss+'*'+weight_mumu,weight_mumu,NormalDirectory,'qcd_nonisoPAStagfree','uujj',1.0,1.0,1.0,version_name,SSNonIsoDataRescale[0])


	print '\nFor final selections, this gives estimates:\n'


	#for plotmass in [ 200, 250, 300 , 350 , 400 , 450 , 500 , 550 , 600 , 650 , 700 , 750 , 800 , 850 , 900 , 950 , 1000 , 1050 , 1100 , 1150 , 1200 , 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000] :
	for plotmass in [200,250,300,350,400,450,500]:
		channel='uujj'
		fsel = ((os.popen('cat '+cutlogmumu+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0').readlines())[0]).replace('\n','')
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+sel_mumu+fsel+')'

		Nss_noniso_data = QuickEntries(tn_SingleMuData,selection + '*(Charge_muon1*Charge_muon2 > 0)',1.0)
		Nss_noniso_mc = QuickMultiIntegral([tn_DiBoson,tn_TTBar,tn_WJets,tn_ZJets,tn_SingleTop],selection+'*(Charge_muon1*Charge_muon2 > 0)*'+weight_mumu,[1.0,1.0,1.0,1.0,1.0])		
		Nss_noniso_qcdest = [Nss_noniso_data[0] - Nss_noniso_mc[0] ,  math.sqrt(Nss_noniso_data[1]**2 + Nss_noniso_mc[1]**2)]
		N_iso_qcdest = [ Nss_noniso_qcdest[0]*SSNonIsoDataRescale[0], (math.sqrt((Nss_noniso_qcdest[1]/Nss_noniso_qcdest[0])**2 + (SSNonIsoDataRescale[1]/SSNonIsoDataRescale[0])**2))*Nss_noniso_qcdest[0]*SSNonIsoDataRescale[0] ]

		print plotmass ,'&',texentry4(N_iso_qcdest),'\\\\'

	print '\n'
	
	#################################
	######## 1 MUON CHANNEL #########
	#################################	
	print '\n------ MUON+MET CHANNEL -------\n'

	sel_low_munu = sel_munu + '*(Pt_miss>5)*(Pt_miss<15)'
	sel_val_munu = sel_munuVal + '*(Pt_miss>5)*(Pt_miss<100)*(M_uu<80)'

	#print sel_low_munu

	D_noniso = QuickEntries(tn_SingleMuData,sel_low_munu+dataHLT,1.0)	
	D_iso = QuickEntries(tn_SingleMuData,sel_low_munu + '*(TrkIso_muon1<0.1)'+dataHLT,1.0)	

	Q_noniso = QuickIntegral(tn_QCDMu,sel_low_munu+'*'+weight_munu,1.0)	
	Q_iso = QuickIntegral(tn_QCDMu,sel_low_munu + '*(TrkIso_muon1<0.1)*'+weight_munu,1.0)	

	B_noniso = QuickMultiIntegral([tn_DiBoson,tn_TTBar,tn_WJets,tn_ZJets,tn_SingleTop],sel_low_munu+'*'+weight_munu,[1.0,1.0,1.0,1.0,1.0])
	B_iso = QuickMultiIntegral([tn_DiBoson,tn_TTBar,tn_WJets,tn_ZJets,tn_SingleTop],sel_low_munu+'*(TrkIso_muon1<0.1)*'+weight_munu,[1.0,1.0,1.0,1.0,1.0])

	print '  Data (noniso):',D_noniso
	print ' SM BG (noniso):',B_noniso
	print 'QCD MC (noniso):',Q_noniso

	print '  Data (iso):',D_iso
	print ' SM BG (iso):',B_iso
	print 'QCD MC (iso):',Q_iso

	ScaleFactor_QCD = (D_noniso[0] - B_noniso[0])/Q_noniso[0]
	ScaleFactor_QCD_Err  = (math.sqrt((math.sqrt(D_noniso[1]**2 + B_noniso[1]**2)/(D_noniso[0] - B_noniso[0]))**2 + (Q_noniso[1]/Q_noniso[0])**2))*ScaleFactor_QCD


	FakeRate = (D_iso[0] - B_iso[0])/(D_noniso[0]-B_noniso[0])
	FakeRate_err = (math.sqrt(( math.sqrt(D_iso[1]**2 + B_iso[1]**2) / (D_iso[0] - B_iso[0]) )**2 + ( math.sqrt(D_noniso[1]**2 + B_noniso[1]**2) / (D_noniso[0] - B_noniso[0]) )**2))*FakeRate

	MCFakeRate = Q_iso[0]/Q_noniso[0]
	MCFakeRate_err = (math.sqrt((Q_iso[1]/Q_iso[0])**2  + (Q_noniso[1]/Q_noniso[0])**2))*MCFakeRate


	print "\nIn the non_isolated low-MET region, the global QCD rescaling is:", texentry4([ScaleFactor_QCD,ScaleFactor_QCD_Err])
	print "\nThe data-driven fake-rate is:", texentry4([FakeRate,FakeRate_err])
	print "\nThe MC-driven fake-rate is:", texentry4([MCFakeRate,MCFakeRate_err])

	#uvjjQcdBins = [125,0,50]#fixme was [25,0,10]
	uvjjQcdBins = [30,0,15]
	uvjjQcdValBins = [95,5,100]
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated, qcd reweighted)",uvjjQcdValBins,sel_val_munu,sel_val_munu+'*'+weight_munu,weight_munu,NormalDirectory,'qcd_noniso_val_weightedtagfree','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD)
	
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated)",uvjjQcdBins,sel_low_munu,sel_low_munu+'*'+weight_munu,weight_munu,NormalDirectory,'qcd_noniso_unweightedtagfree','uvjj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated, qcd reweighted)",uvjjQcdBins,sel_low_munu,sel_low_munu+'*'+weight_munu,weight_munu,NormalDirectory,'qcd_noniso_weightedtagfree','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD)
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated)",uvjjQcdBins,sel_low_munu,sel_low_munu+'*'+weight_munu,weight_munu,NormalDirectory,'qcd_noniso_unweightedPAStagfree','uvjj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated, qcd reweighted)",uvjjQcdBins,sel_low_munu,sel_low_munu+'*'+weight_munu,weight_munu,NormalDirectory,'qcd_noniso_weightedPAStagfree','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD)
	MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",qcdBinning,sel_low_munu,sel_low_munu+'*'+weight_munu,weight_munu,NormalDirectory,'qcd_noniso_unweightedtagfree','uvjj',1.0,1.0,1.0,version_name,1.0)
	MakeBasicPlotQCD("TrkIso_muon1","Tracker Rel Iso Lead Mu  (non-isolated)",qcdBinning,sel_low_munu,sel_low_munu+'*'+weight_munu,weight_munu,NormalDirectory,'qcd_noniso_weightedtagfree','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD)
        
	#MakeBasicPlotQCD("Pt_miss","E_{T}^{miss} [GeV] (muon non-isolated)",uvjjQcdValBins,sel_val_munu,sel_val_munu,weight_munu,NormalDirectory,'qcd_noniso_DataVALtagfree','uvjj',1.0,1.0,1.0,version_name,ScaleFactor_QCD*FakeRate)

	sel_munu = sel_munu + '*(MT_uv>50)*(Pt_miss>55)'#fixme this was not on???? otherwise you dont get presel correct

	print '\nFor final selections, this gives estimates:\n'

        for plotmass in [ 200, 250, 300 , 350 , 400 , 450 , 500 , 550 , 600 , 650 , 700 , 750 , 800 , 850 , 900 , 950 , 1000 , 1050 , 1100 , 1150 , 1200 , 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000] :
		channel='uvjj'
		fsel = ((os.popen('cat '+cutlogmunu+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0').readlines())[0]).replace('\n','')
		fsel = (fsel.split("="))[-1]
		fsel = '*'+fsel.replace(" ","")
		selection = '('+sel_munu+fsel+')'
		[Nobs,Nobs_err] = QuickIntegral(tn_SingleMuData,selection+'*'+dataHLT,1.0)
		B_obs = QuickMultiIntegral([tn_DiBoson,tn_TTBar,tn_WJets,tn_ZJets,tn_SingleTop],selection+'*'+weight_munu,[1.0,1.0,1.0,1.0,1.0])
		Nobs = (Nobs - B_obs[0])*FakeRate
		Nobs_err = math.sqrt(Nobs_err**2 + B_obs[1]**2 + FakeRate_err**2)
		[Nest,Nest_err] = QuickIntegral(tn_QCDMu,selection+'*'+weight_munu,ScaleFactor_QCD*FakeRate)
		Nobs_toterr = math.sqrt((FakeRate_err/FakeRate)**2 + Nobs_err **2)
		Nest_toterr = math.sqrt(((math.sqrt((FakeRate_err/FakeRate)**2 + (ScaleFactor_QCD_Err/ScaleFactor_QCD)**2))*Nest)**2 + Nest_err **2 ) 
		#print plotmass ,'&',texentry4([Nobs,Nobs_toterr]),'\\\\'
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
	#print 'SELECTION',selection
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
	#print 'DSELECTION',dselection
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
	print texline 

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

	#Number of MC events
       	_b_ttbar_nMC = QuickSysIntegral(_demutree,emudataselection,emudatascale,1.0)
	_b_other_nMC = [QuickSysIntegral(_btrees[b],basicselection,normalscales[b],1.0) for b in range(len(_btrees))]

	#print _b_other_nMC

	_b_ttbar = [emu_id_eff*(__emudat[0] + __emuBGsubtract[0]), emu_id_eff*(math.sqrt(__emudat[1]**2 + __emuBGsubtract[1]**2))]
	_Nb_ttbar =  _b_ttbar_nMC[1]
	_b_other = [QuickIntegral(_btrees[b],basicselection,normalscales[b]) for b in range(len(_btrees))]
	_Nb_other = [_b_other_nMC[b] for b in range(len(_btrees))]


	_bs = []
	_bs.append(_b_ttbar)
	for x in _b_other:
		_bs.append(x)

	_Nbs = []
	_Nbs.append(_Nb_ttbar)
	for x in _Nb_other:
		_Nbs.append(x)


	_b_tot = 0.0
	_b_tot_err = 0.0

	for b in _bs:
		_b_tot += b[0]
		_b_tot_err += b[1]**2
	_b_tot_err = math.sqrt(_b_tot_err)

	_bt = [_b_tot, _b_tot_err]

	_d = QuickEntries (_dtree,basicselection+dataHLT,datascale)



	texline = ''
	for x,Nx in zip(_bs,_Nbs):
		#texline += ' '+texentry(x)+' &' # prediction + error only
		texline += ' '+texentry(x)+' ['+Nx+'] &' # prediction + error + N_MC
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
	for f in NormalFiles:
		_tree = 't_'+f.split('/')[-1].replace(".root","")
		_treeTmp = _tree+"_tmp"
		_prefix = ''# +'root://eoscms//eos/cms'*('/store' in NormalDirectory)#fixme removing since eos is hosted on /eos now
		#print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	        #print (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
		exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	        #print (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")
		exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

	selection = weight+'*'+selection
	texfile = optimlog.replace('.txt','_table'+str(num)+'.tex')
	csvfile = optimlog.replace('.txt','_table'+str(num)+'.csv')

	#headers = ['TTBar','Z+Jets','W+Jets','sTop','VV','QCD','Tot BG','Data','Signal']
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

			print '  ..processing table line for preselection: '
			fsel = line.replace('\n','')
			masschan = fsel.split('=')[0]
			masschan = masschan.replace('\n','')
			masschan = masschan.replace(' ','')
			mass = masschan.split('jj')[-1]
			chan = 't_'+masschan.split('_')[-1]
			fsel = (fsel.split("="))[-1]
			fsel = '*'+fsel.replace(" ","")
			this_sel = '('+selection+')'

			#print this_sel

			exec('treefeed = ['+chan+']')
			#treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson,t_ZJetsControl])
			#treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson,t_QCDMu])#fixme todo no idea what zjetscontrol is...
			treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson])
			treefeed.append(t_SingleMuData)
			scalefacs = [1,[rt,rz,rw,1,1,1],1]
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
		#treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson,t_QCDMu])
		treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson])
		treefeed.append(t_SingleMuData)
		scalefacs = [1,[rt,rz,rw,1,1,1],1]
		QuickTableLine(treefeed,this_sel,scalefacs,texfile,csvfile)

		nline += 1


def QuickTableTTDD(optimlog, selection, weight,rz,rw,rt,num):
	# selection = selection+'*'+weight
	texfile = optimlog.replace('.txt','_table'+str(num)+'.tex')
	csvfile = optimlog.replace('.txt','_table'+str(num)+'.csv')

	#headers = ['TTBar','Z+Jets','W+Jets','sTop','VV','QCD','Tot BG','Data','Signal']
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
			continue
			print '  ..processing table line for preselection: '
			fsel = line.replace('\n','')
			masschan = fsel.split('=')[0]
			masschan = masschan.replace('\n','')
			masschan = masschan.replace(' ','')
			mass = masschan.split('jj')[-1]
			chan = 't_'+masschan.split('_')[-1]
			fsel = (fsel.split("="))[-1]
			fsel = '*'+fsel.replace(" ","")
			this_sel = '('+selection+')'

			#this_sel = this_sel.replace('*(M_uu>100)','').replace('*(St_uujj>300)*(M_uu>50)*(DR_muon1muon2>0.3)','*(M_uu>10)').replace('*(Pt_muon2>53)','').replace('(Pt_muon1>53)*(Pt_jet1>50)*(Pt_jet2>50)*','')
			#print this_sel

			exec('treefeed = ['+chan+']')
			treefeed.append(te_SingleMuData)
			#treefeed.append([te_ZJets,te_WJets,te_SingleTop,te_DiBoson,te_QCDMu])
			#treefeed.append([t_ZJets,t_WJets,t_SingleTop,t_DiBoson,t_QCDMu])
			treefeed.append([te_ZJets,te_WJets,te_SingleTop,te_DiBoson])
			treefeed.append([t_ZJets,t_WJets,t_SingleTop,t_DiBoson])
			treefeed.append(t_SingleMuData)
			scalefacs = [1,1,[-1.0*rz,-1.0*rw,-1.0,-1.0,-1.0],[rz,rw,1,1,1],1]
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
		treefeed.append(te_SingleMuData)
		#treefeed.append([te_ZJets,te_WJets,te_SingleTop,te_DiBoson,te_QCDMu])
		#treefeed.append([t_ZJets,t_WJets,t_SingleTop,t_DiBoson,t_QCDMu])
		treefeed.append([te_ZJets,te_WJets,te_SingleTop,te_DiBoson])
		treefeed.append([t_ZJets,t_WJets,t_SingleTop,t_DiBoson])
		treefeed.append(t_SingleMuData)

		scalefacs = [1,1,[-1.0*rz,-1.0*rw,-1.0,-1.0,-1.0],[rz,rw,1,1,1],1]
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
	_kinematicvariables  = ['Pt_muon1','Pt_muon2','Pt_ele1','Pt_ele2','Pt_jet1','Pt_jet2','Pt_miss']
	_kinematicvariables += ['Eta_muon1','Eta_muon2','Eta_ele1','Eta_ele2','Eta_jet1','Eta_jet2','Eta_miss']
	_kinematicvariables += ['Phi_muon1','Phi_muon2','Phi_ele1','Phi_ele2','Phi_jet1','Phi_jet2','Phi_miss']
	_kinematicvariables += ['St_uujj','St_uvjj']
	_kinematicvariables += ['St_eejj','St_evjj']
	_kinematicvariables += ['M_uujj1','M_uujj2','M_uujjavg','MT_uvjj1','MT_uvjj2','M_uvjj','MT_uvjj']
	_kinematicvariables += ['M_uu','MT_uv']
	_kinematicvariables += ['DR_muon1muon2','DPhi_muon1met','DPhi_jet1met']
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
		#Some updates:
		#https://indico.cern.ch/event/675475/contributions/2764498/subcontributions/240732/attachments/1547347/2429001/Wprime-muon-Approvalv1.pdf
		if sysmethod == 'LUMIup':
			selection = '(1.025)*'+selection
		if sysmethod == 'LUMIdown':
			selection = '(0.975)*'+selection
		if sysmethod == 'MUONIDISOup':
			if 'uujj' in channel_log:
				selection = '(1.04)*'+selection
			if 'uvjj' in channel_log: 
				selection = '(1.02)*'+selection
		if sysmethod == 'MUONIDISOdown':
			if 'uujj' in channel_log:
				#selection = '(1.05)*'+selection #normally 1% for ID and 0.5% for ISO, why 5%?
				#selection = '((1.05)*((Pt_muon1*cosh(Eta_muon1))<100)*((Pt_muon2*cosh(Eta_muon2))<100) + (0.9936-3.71e-06*(Pt_muon1*cosh(Eta_muon1)))*(abs(Eta_muon1)<1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*(1.025)*((Pt_muon2*cosh(Eta_muon2))<100) + (0.9936-3.71e-06*(Pt_muon1*cosh(Eta_muon1)))*(abs(Eta_muon1)<1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon2*cosh(Eta_muon2))>100)*(0.9936-3.71e-06*(Pt_muon2*cosh(Eta_muon2)))*(abs(Eta_muon2)<1.6) + (0.9936-3.71e-06*(Pt_muon1*cosh(Eta_muon1)))*(abs(Eta_muon1)<1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon2*cosh(Eta_muon2))>100)*((Pt_muon2*cosh(Eta_muon2))<200)*(1.025)*(abs(Eta_muon2)>1.6) + (0.9936-3.71e-06*(Pt_muon1*cosh(Eta_muon1)))*(abs(Eta_muon1)<1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon2*cosh(Eta_muon2))>200)*((0.9784-4.73e-5*(Pt_muon2*cosh(Eta_muon2)))/(0.9908-1.26e-5*(Pt_muon2*cosh(Eta_muon2))))*(abs(Eta_muon2)>1.6) + (1.025)*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon1*cosh(Eta_muon1))<200)*(1.025)*((Pt_muon2*cosh(Eta_muon2))<100) + (1.025)*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon1*cosh(Eta_muon1))<200)*((Pt_muon2*cosh(Eta_muon2))>100)*(0.9936-3.71e-06*(Pt_muon2*cosh(Eta_muon2)))*(abs(Eta_muon2)<1.6) + (1.025)*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon1*cosh(Eta_muon1))<200)*((Pt_muon2*cosh(Eta_muon2))>100)*((Pt_muon2*cosh(Eta_muon2))<200)*(1.025)*(abs(Eta_muon2)>1.6) + (1.025)*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon1*cosh(Eta_muon1))<200)*((Pt_muon2*cosh(Eta_muon2))>200)*((0.9784-4.73e-5*(Pt_muon2*cosh(Eta_muon2)))/(0.9908-1.26e-5*(Pt_muon2*cosh(Eta_muon2))))*(abs(Eta_muon2)>1.6) + ((0.9784-4.73e-5*(Pt_muon1*cosh(Eta_muon1)))/(0.9908-1.26e-5*(Pt_muon1*cosh(Eta_muon1))))*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>200)*(1.025)*((Pt_muon2*cosh(Eta_muon2))<100) + ((0.9784-4.73e-5*(Pt_muon1*cosh(Eta_muon1)))/(0.9908-1.26e-5*(Pt_muon1*cosh(Eta_muon1))))*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>200)*((Pt_muon2*cosh(Eta_muon2))>100)*(0.9936-3.71e-06*(Pt_muon2*cosh(Eta_muon2)))*(abs(Eta_muon2)<1.6) + ((0.9784-4.73e-5*(Pt_muon1*cosh(Eta_muon1)))/(0.9908-1.26e-5*(Pt_muon1*cosh(Eta_muon1))))*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>200)*((Pt_muon2*cosh(Eta_muon2))>100)*((Pt_muon2*cosh(Eta_muon2))<200)*(1.025)*(abs(Eta_muon2)>1.6) + ((0.9784-4.73e-5*(Pt_muon1*cosh(Eta_muon1)))/(0.9908-1.26e-5*(Pt_muon1*cosh(Eta_muon1))))*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>200)*((Pt_muon2*cosh(Eta_muon2))>200)*((0.9784-4.73e-5*(Pt_muon2*cosh(Eta_muon2)))/(0.9908-1.26e-5*(Pt_muon2*cosh(Eta_muon2))))*(abs(Eta_muon2)>1.6))*'+selection
				selection = '(0.96)*((1.0)*((Pt_muon1*cosh(Eta_muon1))<100)*((Pt_muon2*cosh(Eta_muon2))<100) + ((Pt_muon1*cosh(Eta_muon1))<100)*((Pt_muon2*cosh(Eta_muon2))>100)*(0.9936-3.71e-06*(Pt_muon2*cosh(Eta_muon2)))*(abs(Eta_muon2)<1.6) + ((Pt_muon1*cosh(Eta_muon1))<100)*((Pt_muon2*cosh(Eta_muon2))>100)*((Pt_muon2*cosh(Eta_muon2))<200)*(abs(Eta_muon2)>1.6) + ((Pt_muon1*cosh(Eta_muon1))<100)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon2*cosh(Eta_muon2))>200)*((0.9784-4.73e-5*(Pt_muon2*cosh(Eta_muon2)))/(0.9908-1.26e-5*(Pt_muon2*cosh(Eta_muon2))))*(abs(Eta_muon2)>1.6)+ (0.9936-3.71e-06*(Pt_muon1*cosh(Eta_muon1)))*(abs(Eta_muon1)<1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon2*cosh(Eta_muon2))<100) + (0.9936-3.71e-06*(Pt_muon1*cosh(Eta_muon1)))*(abs(Eta_muon1)<1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon2*cosh(Eta_muon2))>100)*(0.9936-3.71e-06*(Pt_muon2*cosh(Eta_muon2)))*(abs(Eta_muon2)<1.6) + (0.9936-3.71e-06*(Pt_muon1*cosh(Eta_muon1)))*(abs(Eta_muon1)<1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon2*cosh(Eta_muon2))>100)*((Pt_muon2*cosh(Eta_muon2))<200)*(abs(Eta_muon2)>1.6) + (0.9936-3.71e-06*(Pt_muon1*cosh(Eta_muon1)))*(abs(Eta_muon1)<1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon2*cosh(Eta_muon2))>200)*((0.9784-4.73e-5*(Pt_muon2*cosh(Eta_muon2)))/(0.9908-1.26e-5*(Pt_muon2*cosh(Eta_muon2))))*(abs(Eta_muon2)>1.6) + (abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon1*cosh(Eta_muon1))<200)*((Pt_muon2*cosh(Eta_muon2))<100) + (abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon1*cosh(Eta_muon1))<200)*((Pt_muon2*cosh(Eta_muon2))>100)*(0.9936-3.71e-06*(Pt_muon2*cosh(Eta_muon2)))*(abs(Eta_muon2)<1.6) + (abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon1*cosh(Eta_muon1))<200)*((Pt_muon2*cosh(Eta_muon2))>100)*((Pt_muon2*cosh(Eta_muon2))<200)*(abs(Eta_muon2)>1.6) + (abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon1*cosh(Eta_muon1))<200)*((Pt_muon2*cosh(Eta_muon2))>200)*((0.9784-4.73e-5*(Pt_muon2*cosh(Eta_muon2)))/(0.9908-1.26e-5*(Pt_muon2*cosh(Eta_muon2))))*(abs(Eta_muon2)>1.6) + ((0.9784-4.73e-5*(Pt_muon1*cosh(Eta_muon1)))/(0.9908-1.26e-5*(Pt_muon1*cosh(Eta_muon1))))*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>200)*((Pt_muon2*cosh(Eta_muon2))<100) + ((0.9784-4.73e-5*(Pt_muon1*cosh(Eta_muon1)))/(0.9908-1.26e-5*(Pt_muon1*cosh(Eta_muon1))))*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>200)*((Pt_muon2*cosh(Eta_muon2))>100)*(0.9936-3.71e-06*(Pt_muon2*cosh(Eta_muon2)))*(abs(Eta_muon2)<1.6) + ((0.9784-4.73e-5*(Pt_muon1*cosh(Eta_muon1)))/(0.9908-1.26e-5*(Pt_muon1*cosh(Eta_muon1))))*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>200)*((Pt_muon2*cosh(Eta_muon2))>100)*((Pt_muon2*cosh(Eta_muon2))<200)*(abs(Eta_muon2)>1.6) + ((0.9784-4.73e-5*(Pt_muon1*cosh(Eta_muon1)))/(0.9908-1.26e-5*(Pt_muon1*cosh(Eta_muon1))))*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>200)*((Pt_muon2*cosh(Eta_muon2))>200)*((0.9784-4.73e-5*(Pt_muon2*cosh(Eta_muon2)))/(0.9908-1.26e-5*(Pt_muon2*cosh(Eta_muon2))))*(abs(Eta_muon2)>1.6))*'+selection
			if 'uvjj' in channel_log: 
				#selection = '(1.025)*'+selection
				#selection = '((1.025)*((Pt_muon1*cosh(Eta_muon1))<100) + (0.9936-3.71e-06*(Pt_muon1*cosh(Eta_muon1)))*(abs(Eta_muon1)<1.6)*((Pt_muon1*cosh(Eta_muon1))>100) + (1.025)*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon1*cosh(Eta_muon1))<200) + ((0.9784-4.73e-5*(Pt_muon1*cosh(Eta_muon1)))/(0.9908-1.26e-5*(Pt_muon1*cosh(Eta_muon1))))*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>200))*'+selection
				selection = '(0.98)*(((Pt_muon1*cosh(Eta_muon1))<100) + (0.9936-3.71e-06*(Pt_muon1*cosh(Eta_muon1)))*(abs(Eta_muon1)<1.6)*((Pt_muon1*cosh(Eta_muon1))>100) + (abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>100)*((Pt_muon1*cosh(Eta_muon1))<200) + ((0.9784-4.73e-5*(Pt_muon1*cosh(Eta_muon1)))/(0.9908-1.26e-5*(Pt_muon1*cosh(Eta_muon1))))*(abs(Eta_muon1)>1.6)*((Pt_muon1*cosh(Eta_muon1))>200))*'+selection

		#if sysmethod == 'MUONHLT':
		#	if 'uujj' in channel_log: 
		#		selection = '(1.02)*'+selection#was 1.005? AN says 1% per muon
		#	if 'uvjj' in channel_log: 
		#		selection = '(1.01)*'+selection# was 1.015?
		# Per-muon 2% below 300 GeV and +2% -6% above 300 GeV. On top of this, 2% is added resulting from the impact of pre-triggering.
		if sysmethod == 'MUONHLTup':
			if 'uujj' in channel_log: #2% pretrigger, +-2% per muon below 300, +2-6% per muon above 300  uujj: x(SF1+SF2-xSF1SF2)
				selection = '(1.02)*(2-1.02)*1.02*(2-1.02)*'+selection #fixme todo
			if 'uvjj' in channel_log: 
				selection = '(1.02)*(1.02)*'+selection
		if sysmethod == 'MUONHLTdown':
			if 'uujj' in channel_log: 
				selection = '(0.98)*(2-0.98)*(0.98*(2-0.98)*(Pt_muon1<300)+0.94*(2-0.94)*(Pt_muon1>300))*(0.98*(2-0.98)*(Pt_muon2<300)+0.94*(2-0.94)*(Pt_muon2>300))*'+selection
			if 'uvjj' in channel_log: 
				selection = '(0.98)*(0.98*(Pt_muon1<300)+0.94*(Pt_muon1>300))*'+selection
		#https://indico.cern.ch/event/675475/contributions/2764498/subcontributions/240732/attachments/1547347/2429001/Wprime-muon-Approvalv1.pdf
		if sysmethod == 'HIPup ':#Per-muon uncertainty: 0.5% (pT < 300 GeV), 1% (pT > 300 GeV)
			if 'uujj' in channel_log: 
				selection = '((1.005*(Pt_muon1<300)+1.01*(Pt_muon1>300))*(1.005*(Pt_muon2<300)+1.01*(Pt_muon2>300)))*'+selection
			if 'uvjj' in channel_log: 
				selection = '(1.005*(Pt_muon1<300)+1.01*(Pt_muon1>300))*'+selection
		if sysmethod == 'HIPdown':
			if 'uujj' in channel_log: 
				selection = '((0.995*(Pt_muon1<300)+0.99*(Pt_muon1>300))*(0.995*(Pt_muon2<300)+0.99*(Pt_muon2>300)))*'+selection
			if 'uvjj' in channel_log: 
				selection = '(0.995*(Pt_muon1<300)+0.99*(Pt_muon1>300))*'+selection

		if sysmethod == 'PUup':
			selection = selection.replace('weight_central','weight_pu_up')
		if sysmethod == 'PUdown':
			selection = selection.replace('weight_central','weight_pu_down')

	return selection


def SysTable(optimlog, selection_uujj,selection_uvjj,NormalDirectory, weight,sysmethod):
	global munu1
	global munu2
	for f in NormalFiles:
		_tree = 't_'+f.split('/')[-1].replace(".root","")
		_treeTmp = _tree+"_tmp"
		_prefix = ''# +'root://eoscms//eos/cms'*('/store' in NormalDirectory)#fixme removing since eos is hosted on /eos now
		exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
		exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")
	selection_uujj = selection_uujj+'*'+weight
	selection_uvjj = selection_uvjj+'*'+weight
	selection_uujj = ModSelection(selection_uujj,sysmethod,optimlog)
	selection_uvjj = ModSelection(selection_uvjj,sysmethod,optimlog)


	if sysmethod == 'BTAGup':
		if 'uvjj' in optimlog:
			munu1 = '(((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)*(MT_uv>70)*(MT_uv<110)*(1-((CISV_jet1>0.5426)*(0.887973*((1.+(0.0523821*Pt_jet1))/(1.+(0.0460876*Pt_jet1)))+(0.02891194075345993*(Pt_jet1>50)*(Pt_jet1<70)+0.028121808543801308*(Pt_jet1>70)*(Pt_jet1<100)+0.027028990909457207*(Pt_jet1>100)*(Pt_jet1<140)+0.027206243947148323*(Pt_jet1>140)*(Pt_jet1<200)+0.033642303198575974*(Pt_jet1>200)*(Pt_jet1<300)+0.04273652657866478*(Pt_jet1>300)*(Pt_jet1<600)+0.054665762931108475*(Pt_jet1>600)))))*(1-((CISV_jet2>0.5426)*(0.887973*((1.+(0.0523821*Pt_jet2))/(1.+(0.0460876*Pt_jet2)))+(0.02891194075345993*(Pt_jet2>50)*(Pt_jet2<70)+0.028121808543801308*(Pt_jet2>70)*(Pt_jet2<100)+0.027028990909457207*(Pt_jet2>100)*(Pt_jet2<140)+0.027206243947148323*(Pt_jet2>140)*(Pt_jet2<200)+0.033642303198575974*(Pt_jet2>200)*(Pt_jet2<300)+0.04273652657866478*(Pt_jet2>300)*(Pt_jet2<600)+0.054665762931108475*(Pt_jet2>600)))))'
			munu2 = '(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>=1)*(MT_uv>70)*(MT_uv<110)*(1-(1-((CISV_jet1>0.8484)*(0.561694*((1.+(0.31439*Pt_jet1))/(1.+(0.17756*Pt_jet1)))+(0.03711806982755661*(Pt_jet1>50)*(Pt_jet1<70)+0.036822021007537842*(Pt_jet1>70)*(Pt_jet1<100)+0.034397732466459274*(Pt_jet1>100)*(Pt_jet1<140)+0.0362386554479599*(Pt_jet1>140)*(Pt_jet1<200)+0.044985830783843994*(Pt_jet1>200)*(Pt_jet1<300)+0.064243391156196594*(Pt_jet1>300)*(Pt_jet1<600)+0.097131341695785522*(Pt_jet1>600)))))*(1-((CISV_jet2>0.8484)*(0.561694*((1.+(0.31439*Pt_jet2))/(1.+(0.17756*Pt_jet2)))+(0.03711806982755661*(Pt_jet1>50)*(Pt_jet1<70)+0.036822021007537842*(Pt_jet1>70)*(Pt_jet1<100)+0.034397732466459274*(Pt_jet1>100)*(Pt_jet1<140)+0.0362386554479599*(Pt_jet1>140)*(Pt_jet1<200)+0.044985830783843994*(Pt_jet1>200)*(Pt_jet1<300)+0.064243391156196594*(Pt_jet1>300)*(Pt_jet1<600)+0.097131341695785522*(Pt_jet1>600))))))'
	if sysmethod == 'BTAGdown':
		if 'uvjj' in optimlog:
			munu1 = '(((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)*(MT_uv>70)*(MT_uv<110)*(1-((CISV_jet1>0.5426)*(0.887973*((1.+(0.0523821*Pt_jet1))/(1.+(0.0460876*Pt_jet1)))-(0.02891194075345993*(Pt_jet1>50)*(Pt_jet1<70)+0.028121808543801308*(Pt_jet1>70)*(Pt_jet1<100)+0.027028990909457207*(Pt_jet1>100)*(Pt_jet1<140)+0.027206243947148323*(Pt_jet1>140)*(Pt_jet1<200)+0.033642303198575974*(Pt_jet1>200)*(Pt_jet1<300)+0.04273652657866478*(Pt_jet1>300)*(Pt_jet1<600)+0.054665762931108475*(Pt_jet1>600)))))*(1-((CISV_jet2>0.5426)*(0.887973*((1.+(0.0523821*Pt_jet2))/(1.+(0.0460876*Pt_jet2)))-(0.02891194075345993*(Pt_jet2>50)*(Pt_jet2<70)+0.028121808543801308*(Pt_jet2>70)*(Pt_jet2<100)+0.027028990909457207*(Pt_jet2>100)*(Pt_jet2<140)+0.027206243947148323*(Pt_jet2>140)*(Pt_jet2<200)+0.033642303198575974*(Pt_jet2>200)*(Pt_jet2<300)+0.04273652657866478*(Pt_jet2>300)*(Pt_jet2<600)+0.054665762931108475*(Pt_jet2>600)))))'
			munu2 = '(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>=1)*(MT_uv>70)*(MT_uv<110)*(1-(1-((CISV_jet1>0.8484)*(0.561694*((1.+(0.31439*Pt_jet1))/(1.+(0.17756*Pt_jet1)))-(0.03711806982755661*(Pt_jet1>50)*(Pt_jet1<70)+0.036822021007537842*(Pt_jet1>70)*(Pt_jet1<100)+0.034397732466459274*(Pt_jet1>100)*(Pt_jet1<140)+0.0362386554479599*(Pt_jet1>140)*(Pt_jet1<200)+0.044985830783843994*(Pt_jet1>200)*(Pt_jet1<300)+0.064243391156196594*(Pt_jet1>300)*(Pt_jet1<600)+0.097131341695785522*(Pt_jet1>600)))))*(1-((CISV_jet2>0.8484)*(0.561694*((1.+(0.31439*Pt_jet2))/(1.+(0.17756*Pt_jet2)))-(0.03711806982755661*(Pt_jet1>50)*(Pt_jet1<70)+0.036822021007537842*(Pt_jet1>70)*(Pt_jet1<100)+0.034397732466459274*(Pt_jet1>100)*(Pt_jet1<140)+0.0362386554479599*(Pt_jet1>140)*(Pt_jet1<200)+0.044985830783843994*(Pt_jet1>200)*(Pt_jet1<300)+0.064243391156196594*(Pt_jet1>300)*(Pt_jet1<600)+0.097131341695785522*(Pt_jet1>600))))))'

	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( selection_uujj, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0,0)
	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( selection_uvjj, NormalDirectory, munu1,munu2,0)

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
		rz *= 1.1#fixme adding this to cover st/muj kinematic difference
		rz += _e_rz 
	if sysmethod == 'ZNORMdown': 
		rz *= 0.9#fixme adding this to cover st/muj kinematic difference
		rz += -_e_rz 
	if sysmethod == 'WNORMup':     
		rw += _e_rw
	if sysmethod == 'WNORMdown':  
		rw += -_e_rw 
	if sysmethod == 'TTNORMup':  
		rt += _e_rt
	if sysmethod == 'TTNORMdown':  
		rt += -_e_rt 	

	#if sysmethod == 'SHAPETT' : 
		#if 'uujj' in optimlog: 
		#	rt = (1.+.01*shapesys_uujj_ttbar )*rt
		#if 'uvjj' in optimlog: 
		#	rt = (1.+.01*shapesys_uvjj_ttbar )*rt

	# if sysmethod == 'SHAPEZ'  : rz = (1.+.01*shapesys_uujj_zjets)*rz
	# if sysmethod == 'SHAPEW'  : rw = (1.+.01*shapesys_uvjj_wjets)*rw


	sysfile = optimlog.replace('.txt','_systable_'+sysmethod+'.txt')

	#headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV','QCD']
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
		#rqcd = 1
		rsig = 1
		_rt = rt
		_rw = rw
		_rz = rz
                #for shape, do nalign+1 because the first entry is preselection
		if sysmethod == 'SHAPETT':#fixme added this for 2015 method
			#if 'uujj' in optimlog:
			#	_rt *= (1.0+shapesysvar_uujj_ttjets[nalign+1]*0.01)#fixme check - do we need? ttbar is from data.....
			if 'uvjj' in optimlog:
				_rt *= (1.0+shapesysvar_uvjj_ttjets[nalign+1]*0.01)

		if sysmethod == 'SHAPEZ':
			if 'uujj' in optimlog:
				#_rz *= (1.0+shapesysvar_uujj_zjets[nalign+1]*0.01)
				#fixme adding this to cover pt-binned vs inclusive shape difference
				_rz *= (1.0 + math.sqrt(.04*.04+shapesysvar_uujj_zjets[nalign+1]*0.01*shapesysvar_uujj_zjets[nalign+1]*0.01))
                        #if 'uvjj' in optimlog:
			#	_rz *= (1.0+shapesysvar_uvjj_zjets[nalign+1]*0.01)

		if sysmethod == 'SHAPEW':
			#if 'uujj' in optimlog:
			#	_rw *= (1.0)+shapesysvar_uujj_wjets[nalign+1]*0.01)
			if 'uvjj' in optimlog:
				#_rw *= (1.0+shapesysvar_uvjj_wjets[nalign+1]*0.01)
				#fixme adding this to cover pt-binned vs inclusive shape difference
				_rw *= (1.0 + math.sqrt(.07*.07+shapesysvar_uvjj_wjets[nalign+1]*0.01*shapesysvar_uvjj_wjets[nalign+1]*0.01))

		if sysmethod == 'SHAPEVV':
			if 'uujj' in optimlog:
				rdiboson *= (1.0+shapesysvar_uujj_vv[nalign+1]*0.01)

			if 'uvjj' in optimlog:
				rdiboson *= (1.0+shapesysvar_uvjj_vv[nalign+1]*0.01)

		if 'PDF'  in sysmethod:
			if 'uujj' in optimlog:
				_rt      *= (1.0+pdf_uujj_TTBar[nalign]*0.01)
				_rz      *= (1.0+pdf_uujj_ZJets[nalign]*0.01)
				_rw      *= (1.0+pdf_uujj_WJets[nalign]*0.01)
				rstop    *= (1.0+pdf_uujj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uujj_VV[nalign]*0.01)
				#rqcd     *= (1.0+pdf_uujj_QCD[nalign]*0.01)
				rsig     *= (1.0+pdf_uujj_Signal[nalign]*0.01)

			if 'uvjj' in optimlog:
				_rt      *= (1.0+pdf_uvjj_TTBar[nalign]*0.01)
				_rw      *= (1.0+pdf_uvjj_WJets[nalign]*0.01)
				_rz      *= (1.0+pdf_uvjj_ZJets[nalign]*0.01)
				rstop    *= (1.0+pdf_uvjj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uvjj_VV[nalign]*0.01)
				#rqcd     *= (1.0+pdf_uvjj_QCD[nalign]*0.01)
				rsig     *= (1.0+pdf_uvjj_Signal[nalign]*0.01)

		exec('treefeed = ['+chan+']')
		treefeed.append(t_SingleMuData)
		#treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson,t_QCDMu])
		treefeed.append([t_TTBar,t_ZJets,t_WJets,t_SingleTop,t_DiBoson])
		#scalefacs = [rsig,[_rt,_rz,_rw,rstop,rdiboson,rqcd],1]
		scalefacs = [rsig,[_rt,_rz,_rw,rstop,rdiboson],1]
		QuickSysTableLine(treefeed,this_sel,scalefacs,sysfile,chan,rglobals,rglobalb)
		# break



def SysTableTTDD(optimlog, selection_uujj,selection_uvjj,NormalDirectory, weight,sysmethod):
	for f in NormalFiles:
		_tree = 't_'+f.split('/')[-1].replace(".root","")
		_treeTmp = _tree+"_tmp"
		_prefix = ''# +'root://eoscms//eos/cms'*('/store' in NormalDirectory)#fixme removing since eos is hosted on /eos now
		exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
		exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")
	selection_uujj = selection_uujj
	selection_uvjj = selection_uvjj

	selection_uujj_unmod = ModSelection(selection_uujj,"",optimlog)
	selection_uvjj_unmod = ModSelection(selection_uvjj,"",optimlog)

	selection_uujj = ModSelection(selection_uujj,sysmethod,optimlog)
	selection_uvjj = ModSelection(selection_uvjj,sysmethod,optimlog)

	weightmod = '*'+ModSelection(weight,sysmethod,optimlog)

	weightmod_uvjj = '*'+ModSelection(NormalWeightMuNu,sysmethod,optimlog)

	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( selection_uujj+weightmod, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',1,0)
	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( selection_uvjj+weightmod_uvjj, NormalDirectory,munu1,munu2,0)

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


	if sysmethod == 'ZNORMup':  
		rz *= 1.1#fixme adding this to cover st/muj kinematic difference
		rz += _e_rz 
	if sysmethod == 'ZNORMdown': 
		rz *= 0.9#fixme adding this to cover st/muj kinematic difference
		rz += -_e_rz 
	if sysmethod == 'WNORMup':     rw += _e_rw
	if sysmethod == 'WNORMdown':   rw += -_e_rw 
	if sysmethod == 'TTNORMup':    rt += _e_rt
	if sysmethod == 'TTNORMdown':  rt += -_e_rt 	

	sysfile = optimlog.replace('.txt','_systable_'+sysmethod+'.txt')

	#headers = ['Signal','Data','TTBar','ZJets','WJets','sTop','VV','QCD']
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
		#rqcd = 1
		rsig = 1
		_rt = rt
		_rw = rw
		_rz = rz


		if sysmethod == 'SHAPEZ':
			if 'uujj' in optimlog:
				#_rz *= (1.0+shapesysvar_uujj_zjets[nalign+1]*0.01)
				#fixme adding this to cover pt-binned vs inclusive shape difference
				_rz *= (1.0 + math.sqrt(.04*.04+shapesysvar_uujj_zjets[nalign+1]*0.01*shapesysvar_uujj_zjets[nalign+1]*0.01))
			#if 'uvjj' in optimlog:
			#	_rz *= (1.0+shapesysvar_uvjj_zjets[nalign+1]*0.01)

		if sysmethod == 'SHAPEW':
			#if 'uujj' in optimlog:
			#	_rw *= (1.0+shapesysvar_uujj_wjets[nalign+1]*0.01)
			if 'uvjj' in optimlog:
				#_rw *= (1.0+shapesysvar_uvjj_wjets[nalign+1]*0.01)
				#fixme adding this to cover pt-binned vs inclusive shape difference
				_rw *= (1.0 + math.sqrt(.07*.07+shapesysvar_uvjj_wjets[nalign+1]*0.01*shapesysvar_uvjj_wjets[nalign+1]*0.01))

		if sysmethod == 'SHAPEVV':
			if 'uujj' in optimlog:
				rdiboson *= (1.0+shapesysvar_uujj_vv[nalign+1]*0.01)
			if 'uvjj' in optimlog:
				rdiboson *= (1.0+shapesysvar_uvjj_vv[nalign+1]*0.01)

		if 'PDF'  in sysmethod:
			if 'uujj' in optimlog:
				# _rt *= (1.0+pdf_uujj_TTBar[nalign]*0.01)
				_rz      *= (1.0+pdf_uujj_ZJets[nalign]*0.01)
				_rw      *= (1.0+pdf_uujj_WJets[nalign]*0.01)
				rstop    *= (1.0+pdf_uujj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uujj_VV[nalign]*0.01)
				#rqcd     *= (1.0+pdf_uujj_QCD[nalign]*0.01)
				rsig     *= (1.0+pdf_uujj_Signal[nalign]*0.01)

			if 'uvjj' in optimlog:
				_rt      *= (1.0+pdf_uvjj_TTBar[nalign]*0.01)
				_rw      *= (1.0+pdf_uvjj_WJets[nalign]*0.01)
				_rz      *= (1.0+pdf_uvjj_ZJets[nalign]*0.01)
				rstop    *= (1.0+pdf_uvjj_sTop[nalign]*0.01)
				rdiboson *= (1.0+pdf_uvjj_VV[nalign]*0.01)
				#rqcd     *= (1.0+pdf_uvjj_QCD[nalign]*0.01)
				rsig     *= (1.0+pdf_uvjj_Signal[nalign]*0.01)


		exec('treefeed = ['+chan+']')
		treefeed.append(te_SingleMuData)
		#treefeed.append([te_ZJets,te_WJets,te_SingleTop,te_DiBoson,te_QCDMu])
		#treefeed.append([t_ZJets,t_WJets,t_SingleTop,t_DiBoson,t_QCDMu])
		treefeed.append([te_ZJets,te_WJets,te_SingleTop,te_DiBoson])
		treefeed.append([t_ZJets,t_WJets,t_SingleTop,t_DiBoson])
		treefeed.append(t_SingleMuData)

		#scalefacs = [rsig,_rt,[-1.0*_rz,-1.0*_rw,-1.0*rstop,-1.0*rdiboson,-1.0*rqcd],[_rz,_rw,rstop,rdiboson,rqcd],1]
		scalefacs = [rsig,_rt,[-1.0*_rz,-1.0*_rw,-1.0*rstop,-1.0*rdiboson],[_rz,_rw,rstop,rdiboson],1]
		selections = [ this_sel_unmod +dataHLT+dataHLTEMUADJ, this_sel_unmod+'*'+NormalWeightEMuNoHLT, this_sel+weightmod ]		

		QuickSysTableLineTTDD(treefeed,selections,scalefacs,sysfile,chan,rglobals,rglobalb)
		# break

def FullAnalysis(optimlog,selection_uujj,selection_uvjj,NormalDirectory,weight,usedd):
	TTDD = False
	if usedd=='TTBarDataDriven':
		TTDD=True
	#_Variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','WNORMup','WNORMdown','TTNORMup','TTNORMdown','SHAPETT','SHAPEZ','SHAPEW','MUONIDISO','MUONHLT','ALIGN','PDF']	
        #fixme removing align
	#_Variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','WNORMup','WNORMdown','TTNORMup','TTNORMdown','SHAPETT','SHAPEZ','SHAPEW','SHAPEVV','MUONIDISO','MUONHLT','PDF','HIPup','HIPdown']	
	#Splitting MUONIDISO and MUONHLT into up and down to account for asymmetric high pt corrections
	_Variations = ['','JESup','JESdown','MESup','MESdown','JERup','JERdown','MER','LUMIup','LUMIdown','PUup','PUdown','ZNORMup','ZNORMdown','WNORMup','WNORMdown','TTNORMup','TTNORMdown','SHAPETT','SHAPEZ','SHAPEW','SHAPEVV','MUONIDISOup','MUONIDISOdown','MUONHLTup','MUONHLTdown','PDF','HIPup','HIPdown','BTAGup','BTAGdown']	
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
	t_SingleMuData2 = t_SingleMuData.CopyTree(preselectionmunu)
	allruns = []
	NN = t_SingleMuData2.GetEntries()
	for n in range(NN):
		if n%1000 ==0:
			print n,'of',NN
		t_SingleMuData2.GetEntry(n)
		ev = t_SingleMuData2.run_number
		if ev not in allruns:
			allruns.append(ev)

	allruns.sort()
	for a in allruns:
		print a

def GetMuMuScaleFactors( selection, FileDirectory, controlregion_1, controlregion_2, canUseTTDD, isQuick):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_SingleMuData,selection + '*' + controlregion_1,1.0)
	# print QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	# sys.exit()
	selection_data = selection.split('*(fact')[0]

	N1 = QuickEntries(t_SingleMuData,selection_data + '*' + controlregion_1+dataHLT,1.0)
	print selection_data + '*' + controlregion_1+dataHLT
	N2 = QuickEntries(t_SingleMuData,selection_data + '*' + controlregion_2+dataHLT,1.0)

	Z1 = QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBar,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(t_WJets,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)
	ttv1 = QuickIntegral(t_TTV,selection + '*' + controlregion_1,1.0)
	#q1 = QuickIntegral(t_QCDMu,selection   + '*' + controlregion_1,1.0)

	Z2 = QuickIntegral(t_ZJets,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBar,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(t_WJets,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)
	ttv2 = QuickIntegral(t_TTV,selection + '*' + controlregion_2,1.0)
	#q2 = QuickIntegral(t_QCDMu,selection   + '*' + controlregion_2,1.0)

	if useDataDrivenTTbar and canUseTTDD:
		selection = preselectionmumu
		selectionData =  selection + dataHLT + dataHLTEMUADJ
		#emuTrees = [te_ZJets,te_WJets,te_SingleTop,te_DiBoson,te_QCDMu]
		emuTrees = [te_ZJets,te_WJets,te_SingleTop,te_DiBoson]
		#T3 = QuickEntries(te_SingleMuData,selection + '*' + controlregion_1,1.0)
		T3 = QuickIntegral(te_SingleMuData,selectionData + '*' + controlregion_1,1.0)
		B3 = QuickMultiIntegral(emuTrees,selection+'*'+NormalWeightEMuNoHLT+'*'+ controlregion_1,[-1.0,-1.0,-1.0,-1.0,-1.0])
		T1 = [emu_id_eff*(T3[0]-B3[0]),emu_id_eff*math.sqrt(T3[1]**2+B3[1]**2)]

	#Other1 = [ s1[0]+w1[0]+v1[0]+q1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] + q1[1]*q1[1] ) ]
	#Other2 = [ s2[0]+w2[0]+v2[0]+q2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] + q2[1]*q2[1] ) ]
	Other1 = [ s1[0]+w1[0]+v1[0]+ttv1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] + ttv1[1]*ttv1[1]) ]
	Other2 = [ s2[0]+w2[0]+v2[0]+ttv2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] + ttv2[1]*ttv2[1]) ]
	zvals = []
	tvals = []

	if isQuick: loops=50
	else: loops=10000
	for x in range(loops):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(Z1),RR(Z2),RR(T1),RR(T2),Other1[0],Other2[0]))
		zvals.append(variation[0])
		tvals.append(variation[1])

	zout =  GetStats(zvals)
	tout = GetStats(tvals)

	# ttbar force unity
	if useDataDrivenTTbar and canUseTTDD:
		print 'Using Data-driven TTbar'
		tout = [1.0,0.023,'1.000 +- 0.023'] #set to emu_id_eff_err

        ## Force to pre-calculated values to speed things up
	#zout = [3.251,0.059,'3.251 +- 0.059']
	#tout = [2.19,0.037,'2.19  +- 0.037']
	#print 'Using pre-calculated values, rerun if you add more data!'

	print 'MuMu scale factor integrals:'
	print 'Data:',N1,N2
	print 'Z:',Z1,Z2
	print 'TT:',T1,T2
	print 'ST:',s1,s2
	print 'W:',w1,w2
	print 'VV:',v1,v2
	print 'TTV:',ttv1,ttv2
	print 'Other:',Other1,Other2


	print 'MuMu: RZ  = ', zout[-1]
	print 'MuMu: Rtt = ', tout[-1]
	return [ [ zout[0], zout[1] ] , [ tout[0],tout[1] ] ]

def GetMuMuScaleFactorsData( selection, FileDirectory, controlregion_1, controlregion_2, canUseTTDD, isQuick):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_SingleMuData,selection + '*' + controlregion_1,1.0)
	# print QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	# sys.exit()
	selection_data = selection.split('*(fact')[0]
	
	_muu=selection.split('M_uu')[1].split('*')[0]
	
	selection_Zpeak = selection.replace('(M_uu'+_muu,'(M_uu>80)*(M_uu<100)')

	N1 = QuickEntries(t_SingleMuData,selection_data + '*' + controlregion_1+dataHLT,1.0)
	print selection_data + '*' + controlregion_1+dataHLT
	N2 = QuickEntries(t_SingleMuData,selection_data + '*' + controlregion_2+dataHLT,1.0)

	Z1 = QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBar,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(t_WJets,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)
	#q1 = QuickIntegral(t_QCDMu,selection   + '*' + controlregion_1,1.0)

	Z2 = QuickIntegral(t_ZJets,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBar,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(t_WJets,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)
	#q2 = QuickIntegral(t_QCDMu,selection   + '*' + controlregion_2,1.0)

	#Other1 = [ s1[0]+w1[0]+v1[0]+q1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] + q1[1]*q1[1] ) ]
	#Other2 = [ s2[0]+w2[0]+v2[0]+q2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] + q2[1]*q2[1] ) ]
	Other1 = [ s1[0]+w1[0]+v1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+w2[0]+v2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] ) ]
	zvals = []
	tvals = []

	if isQuick: loops=50
	else: loops=10000
	for x in range(loops):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(Z1),RR(Z2),RR(T1),RR(T2),Other1[0],Other2[0]))
		zvals.append(variation[0])
		tvals.append(variation[1])

	zout =  GetStats(zvals)
	tout = GetStats(tvals)

	# ttbar force unity
	if useDataDrivenTTbar and canUseTTDD:
		print 'Using Data-driven TTbar'
		tout = [1.0,0.023,'1.000 +- 0.023'] #set to emu_id_eff_err

        ## Force to pre-calculated values to speed things up
	#zout = [3.251,0.059,'3.251 +- 0.059']
	#tout = [2.19,0.037,'2.19  +- 0.037']
	#print 'Using pre-calculated values, rerun if you add more data!'

	print 'MuMu scale factor integrals:'
	print 'Data:',N1,N2
	print 'Z:',Z1,Z2
	print 'TT:',T1,T2
	print 'Other:',Other1,Other2


	print 'MuMu: RZ  = ', zout[-1]
	print 'MuMu: Rtt = ', tout[-1]
	return [ [ zout[0], zout[1] ] , [ tout[0],tout[1] ] ]

def GetMuMuScaleFactorsMod( selection, FileDirectory, controlregion_1, controlregion_2,samp,isQuick):
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	# print QuickEntries(t_SingleMuData,selection + '*' + controlregion_1,1.0)
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

	N1 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

	Z1 = QuickIntegral(t_Z,selectionMod + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBar,selectionMod + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	w1 = QuickIntegral(t_WJets,selectionMod + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)
	#q1 = QuickIntegral(t_QCDMu,selection     + '*' + controlregion_1,1.0)

	Z2 = QuickIntegral(t_Z,selectionMod + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBar,selectionMod + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	w2 = QuickIntegral(t_WJets,selectionMod + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)
	#q2 = QuickIntegral(t_QCDMu,selection     + '*' + controlregion_2,1.0)

	#Other1 = [ s1[0]+w1[0]+v1[0]+q1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] + q1[1]*q1[1] ) ]
	#Other2 = [ s2[0]+w2[0]+v2[0]+q2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] + q2[1]*q2[1] ) ]
	Other1 = [ s1[0]+w1[0]+v1[0], math.sqrt( s1[1]*s1[1] + w1[1]*w1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+w2[0]+v2[0], math.sqrt( s2[1]*s2[1] + w2[1]*w2[1] + v2[1]*v2[1] ) ]
	zvals = []
	tvals = []

	if isQuick: loops=1000
	else: loops=10000
	for x in range(loops):
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
	#dataselection = selection.replace(singlemuHLTEMUSF,'').replace(MuIdScaleEMU,'').replace(MuIsoScaleEMU,'').replace(trackerHIPEMU,'').replace(eleRECOScale,'').replace(eleHEEPScale,'')
	dataselection = selection.replace(singlemuHLTEMU,'').replace(MuIdScaleEMU,'').replace(MuIsoScaleEMU,'').replace(trackerHIPEMU,'').replace(eleRECOScale,'').replace(eleHEEPScale,'')
	N1 = QuickEntries(te_SingleMuData,dataselection  + dataHLT,1.0)

	Z1 = QuickIntegral(te_ZJets,selection ,1.0)
	T1 = QuickIntegral(te_TTBar,selection ,1.0)
	s1 = QuickIntegral(te_SingleTop,selection ,1.0)
	w1 = QuickIntegral(te_WJets,selection ,1.0)
	v1 = QuickIntegral(te_DiBoson,selection   ,1.0)
	#q1 = QuickIntegral(te_QCDMu,selection     ,1.0)


	print 'This is the information for the NOTE table 6:'
	print ' Data:',N1[0]
	print '   TT:',T1[0]
	print '    Z:',Z1[0]
	print ' Stop:',s1[0]
	print '    W:',w1[0]
	print '   VV:',v1[0]
	#print '  QCD:',q1[0]

	SF=[1.0,0.0]

	#SF[0] = (N1[0] - Z1[0] - s1[0] - v1[0] - w1[0] - q1[0])/T1[0]
	SF[0] = (N1[0] - Z1[0] - s1[0] - v1[0] - w1[0] )/T1[0]

	#relerror_num  = math.sqrt(N1[1]**2. + Z1[1]**2. + s1[1]**2. + v1[1]**2. + w1[1]**2. + q1[1]**2)/(N1[0] - Z1[0] - s1[0] - v1[0] - w1[0] - q1[0])
	relerror_num  = math.sqrt(N1[1]**2. + Z1[1]**2. + s1[1]**2. + v1[1]**2. + w1[1]**2.)/(N1[0] - Z1[0] - s1[0] - v1[0] - w1[0])
	relerror_denom = T1[1]/T1[0]
	SF[1] = SF[0]*math.sqrt(relerror_num**2. + relerror_denom**2.)

	print 'MuMu: Rtt = ', SF


	print 'Now calculating R_mumu,emu, the ratio of mumu to e,mu events in ttbar MC. '
	print 'Should be near 0.5'
	#print selection,'\n\n'
	#T2 = QuickIntegral(t_TTBar,selection.replace(singlemuHLTEMUSF,singlemuHLT).replace(trackerHIPEMU,trackerHIP1), 1.0)
	#T2 = QuickIntegral(t_TTBar,selection.replace(singlemuHLTEMUSF,singlemuHLT).replace(MuIdScaleEMU,singleMuIdScale).replace(MuIsoScaleEMU,singleMuIsoScale).replace(trackerHIPEMU,trackerHIP1) ,1.0)
	#T2 = QuickIntegral(t_TTBar,selection.replace(singlemuHLTEMUSF,singlemuHLT).replace(MuIdScaleEMU,doubleMuIdScale).replace(MuIsoScaleEMU,doubleMuIsoScale).replace(trackerHIPEMU,trackerHIP1+trackerHIP2).replace(eleRECOScale,'').replace(eleHEEPScale,'') ,1.0)
	T2 = QuickIntegral(t_TTBar,selection.replace(singlemuHLTEMU,singlemuHLT).replace(MuIdScaleEMU,doubleMuIdScale).replace(MuIsoScaleEMU,doubleMuIsoScale).replace(trackerHIPEMU,trackerHIP1+trackerHIP2).replace(eleRECOScale,'').replace(eleHEEPScale,''),1.0)
	#T2 = QuickIntegral(t_TTBar,selection.replace(singlemuHLTEMU,singlemuHLT).replace(MuIdScaleEMU,doubleMuIdScale).replace(MuIsoScaleEMU,doubleMuIsoScale).replace(trackerHIPEMU,trackerHIP1+trackerHIP2).replace(eleRECOScale,'').replace(eleHIPScale,'').replace(muEtaRestrict,'*(abs(Eta_muon1)<2.1)*(abs(Eta_muon2)<2.1)') ,1.0)

	T3 = QuickIntegral(te_TTBar,selection+'*(2.0 - 1.0'+singlemuHLTEMU+')' ,1.0)
	
	Ruueu = T2[0]/T1[0]
	dRuueu =  Ruueu*(math.sqrt((T1[1]/T1[0])**2.0 + (T2[1]/T2[0])**2.0))

	print 'R_uu,eu = ',Ruueu,' +- ',dRuueu

	return SF

def GetMuNuScaleFactorsMod( selection, FileDirectory, controlregion_1, controlregion_2,samp,isQuick):
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

	N1 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_1+dataHLT,1.0)
	N2 = QuickEntries(t_SingleMuData,selection + '*' + controlregion_2+dataHLT,1.0)

	W1 = QuickIntegral(t_W,selectionMod + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_T,selectionMod + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	z1 = QuickIntegral(t_ZJets,selectionMod + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_1,1.0)
	#q1 = QuickIntegral(t_QCDMu,selection + '*' + controlregion_1,1.0)

	W2 = QuickIntegral(t_W,selectionMod + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_T,selectionMod + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	z2 = QuickIntegral(t_ZJets,selectionMod + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,selection + '*' + controlregion_2,1.0)
	#q2 = QuickIntegral(t_QCDMu,selection + '*' + controlregion_2,1.0)

	#Other1 = [ s1[0]+z1[0]+v1[0]+q1[0], math.sqrt( s1[1]*s1[1] + z1[1]*z1[1] + v1[1]*v1[1] + q1[1]*q1[1] ) ]
	#Other2 = [ s2[0]+z2[0]+v2[0]+q2[0], math.sqrt( s2[1]*s2[1] + z2[1]*z2[1] + v2[1]*v2[1] + q1[1]*q1[1] ) ]
	Other1 = [ s1[0]+z1[0]+v1[0], math.sqrt( s1[1]*s1[1] + z1[1]*z1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+z2[0]+v2[0], math.sqrt( s2[1]*s2[1] + z2[1]*z2[1] + v2[1]*v2[1] ) ]

	print 'Data:',N1,N2
	print 'TT:',T1,T2
	print 'W:',W1,W2
	print 'Other:',Other1,Other2

	wvals = []
	tvals = []


	if isQuick: loops=1000
	else: loops=10000
	for x in range(loops):
		variation = (GetScaleFactors(RR(N1),RR(N2),RR(W1),RR(W2),RR(T1),RR(T2),Other1[0],Other2[0]))
		wvals.append(variation[0])
		tvals.append(variation[1])

	wout =  GetStats(wvals)
	tout = GetStats(tvals)

	print 'MuNu: RW  = ', wout[-1]
	print 'MuNu: Rtt = ', tout[-1]
	return [ [ wout[0], wout[1] ] , [ tout[0],tout[1] ] ]


def GetMuNuScaleFactors( selection, FileDirectory, controlregion_1, controlregion_2,isQuick):
	global munu1Data
	global munu2Data
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	selection_data = selection.split('*(fact')[0]

	N1 = QuickEntries(t_SingleMuData,selection_data + '*' + munu1Data+dataHLT,1.0)
	N2 = QuickEntries(t_SingleMuData,selection_data + '*' + munu2Data+dataHLT,1.0)

	W1 = QuickIntegral(t_WJets,selection + '*' + controlregion_1,1.0)
	T1 = QuickIntegral(t_TTBar,selection + '*' + controlregion_1,1.0)
	s1 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_1,1.0)
	z1 = QuickIntegral(t_ZJets,selection + '*' + controlregion_1,1.0)
	v1 = QuickIntegral(t_DiBoson,  selection + '*' + controlregion_1,1.0)
	#q1 = QuickIntegral(t_QCDMu,    selection + '*' + controlregion_1,1.0)

	W2 = QuickIntegral(t_WJets,selection + '*' + controlregion_2,1.0)
	T2 = QuickIntegral(t_TTBar,selection + '*' + controlregion_2,1.0)
	s2 = QuickIntegral(t_SingleTop,selection + '*' + controlregion_2,1.0)
	z2 = QuickIntegral(t_ZJets,selection + '*' + controlregion_2,1.0)
	v2 = QuickIntegral(t_DiBoson,  selection + '*' + controlregion_2,1.0)
	#q2 = QuickIntegral(t_QCDMu,    selection + '*' + controlregion_2,1.0)

	#Other1 = [ s1[0]+z1[0]+v1[0]+q1[0], math.sqrt( s1[1]*s1[1] + z1[1]*z1[1] + v1[1]*v1[1] + q1[1]*q1[1] ) ]
	#Other2 = [ s2[0]+z2[0]+v2[0]+q2[0], math.sqrt( s2[1]*s2[1] + z2[1]*z2[1] + v2[1]*v2[1] + q2[1]*q2[1] ) ]
	Other1 = [ s1[0]+z1[0]+v1[0], math.sqrt( s1[1]*s1[1] + z1[1]*z1[1] + v1[1]*v1[1] ) ]
	Other2 = [ s2[0]+z2[0]+v2[0], math.sqrt( s2[1]*s2[1] + z2[1]*z2[1] + v2[1]*v2[1] ) ]
	wvals = []
	tvals = []

	###
        #fixme adding inc/pt-binned scale factor in 70-110 window
	#W1=[W1[0]*1.175, W1[1]*1.175]
        ###

	if isQuick: loops=1000
	else: loops=10000
	for x in range(loops):
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

	print '\\ttbar control region & ',round(N2[0],1),' & ',round(T2[0],1),'$\\pm$',round(T2[1],1),' & ',round(W2[0],1),'$\\pm$',round(W2[1],1),' & ',round(Other2[0],1),'$\\pm$',round(Other2[1],1),' & ',round(T2[0]+W2[0]+Other2[0],1),'$\\pm$',round(math.sqrt(T2[1]**2+W2[1]**2+Other2[1]**2),1),'\\\\ \\hline'
	print 'W control region & ',round(N1[0],1),' & ',round(T1[0],1),'$\\pm$',round(T1[1],1),' & ',round(W1[0],1),'$\\pm$',round(W1[1],1),' & ',round(Other1[0],1),'$\\pm$',round(Other1[1],1),' & ',round(T1[0]+W1[0]+Other1[0],1),'$\\pm$',round(math.sqrt(T1[1]**2+W1[1]**2+Other1[1]**2),1),'\\\\ \\hline'

	wout =  GetStats(wvals)
	tout = GetStats(tvals)

        #Force to pre-calculated values to speed things up
	#wout = [1.053,0.044 ,'1.053 +- 0.044']
	#tout = [0.954,0.030 ,'0.954 +- 0.030']
	#print "----------------------------\nUsing pre-calculated values, rerun if you add more data!\n----------------------------"

	print 'MuNu scale factor integrals:'
	print 'Data:',N1,N2
	print 'W:',W1,W2
	print 'TT:',T1,T2
	print 'Other:',Other1,Other2

	print 'MuNu: RW  = ', wout[-1]
	print 'MuNu: Rtt = ', tout[-1]
	return [ [ wout[0], wout[1] ] , [ tout[0],tout[1] ] ]




def MakeEfficiencyPlot(FileDirectory,weight,cutlog,channel,version_name,isPAS):
	print "\n\n--------------\n--------------\nMaking signal efficiency*acceptance plot..."
	print "Getting files again so it doesn't fail....."

	gStyle.SetErrorX(0)

	for f in NormalFiles:
		_tree = 't_'+f.split('/')[-1].replace(".root","")
		_treeTmp = _tree+"_tmp"
		_prefix = ''# +'root://eoscms//eos/cms'*('/store' in NormalDirectory)#fixme removing since eos is hosted on /eos now
		#print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	        #print (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
		exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	        #print (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")
		exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

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
	if isDisplaced : 
		xsecs=[64.5085,8.51615,1.83537,0.51848,0.174599,0.0670476,0.0283338,0.0128895,0.00615134,0.00307413,0.00159844]
		xsecsErr=[9.29555,1.18564,0.251418,0.0693711,0.02306,0.00894609,0.00401518,0.00195954,0.00100238,0.000532983,0.000296045]
	elif 'uujj' in channel :
		xsecs = [6.06E+01,2.03E+01,8.04E+00,3.59E+00,1.74E+00,9.06E-01,4.96E-01,2.84E-01,1.69E-01,1.03E-01,6.48E-02,4.16E-02,2.73E-02,1.82E-02,1.23E-02,8.45E-03,5.86E-03,4.11E-03,2.91E-03,2.08E-03,1.50E-03,1.09E-03,7.95E-04,5.85E-04,4.33E-04,3.21E-04,2.40E-04,1.80E-04,1.35E-04,1.02E-04,7.74E-05,5.88E-05,4.48E-05,3.43E-05,2.62E-05,2.01E-05,1.55E-05]#this assumes 200-2000
		xsecsErr = [2.50E+00,1.09E+00,5.35E-01,2.85E-01,1.61E-01,9.52E-02,5.78E-02,3.69E-02,2.37E-02,1.57E-02,1.06E-02,7.27E-03,5.03E-03,3.55E-03,2.53E-03,1.83E-03,1.33E-03,9.82E-04,7.25E-04,5.41E-04,4.07E-04,3.09E-04,2.34E-04,1.79E-04,1.38E-04,1.06E-04,8.24E-05,6.43E-05,5.01E-05,3.92E-05,3.08E-05,2.43E-05,1.92E-05,1.52E-05,1.20E-05,9.55E-06,7.59E-06]
	elif 'uvjj' in channel :
		xsecs = [30.3,10.15,4.02,1.795,0.87,0.453,0.248,0.142,0.0845,0.0515,0.0324,0.0208,0.01365,0.0091,0.00615,0.004225,0.00293,0.002055,0.001455,0.00104,0.00075,0.000545,0.0003975,0.0002925,0.0002165,0.0001605,0.00012,9e-05,6.75e-05,5.1e-05,3.87e-05,2.94e-05,2.24e-05,1.715e-05,1.31e-05,1.005e-05,7.75e-06]
		xsecsErr=[1.25,0.545,0.2675,0.1425,0.0805,0.0476,0.0289,0.01845,0.01185,0.00785,0.0053,0.003635,0.002515,0.001775,0.001265,0.000915,0.000665,0.000491,0.0003625,0.0002705,0.0002035,0.0001545,0.000117,8.95e-05,6.9e-05,5.3e-05,4.12e-05,3.215e-05,2.505e-05,1.96e-05,1.54e-05,1.215e-05,9.6e-06,7.6e-06,6e-06,4.775e-06,3.795e-06]
	xsecCounter,xsecCounter10,xsecCounter100,xsecCounter1000 = 0,0,0,0
	for plotmass in masses:
		if plotmass>highMass: break #fixme this is a temporary solution, need to figure out how to handle last entry in cutlog correctly
		print 'Getting Final sel for M =',plotmass
		if cutlog !='':
		        #print 'cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0'
			if 'LQ'in channel:
				fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0').readlines())[0]).replace('\n','')
			elif 'BL' in channel:
				fsel = ((os.popen('cat '+cutlog+' | grep '+'uujj'+str(plotmass)+' | grep -v '+'uujj'+str(plotmass)+'0').readlines())[0]).replace('\n','')
			if fsel=='':
				print 'No more entries in cutlog, exiting...'
				break
			else: print 'found'
			fsel = (fsel.split("="))[-1].replace(" ","")
		else : fsel = '1.0'
		selectionNoSel  = '('+weight+')'
		selectionFinal=selectionPresel=''
		if 'uujj' in channel or 'BL' in channel:
			selectionPresel = '('+weight+'*'+preselectionmumu+')'
			selectionFinal  = '('+weight+'*'+preselectionmumu+'*'+fsel+')'
		if 'uvjj' in channel:
			selectionPresel = '('+weight+'*'+preselectionmunu+')'
			selectionFinal  = '('+weight+'*'+preselectionmunu+'*'+fsel+')'
		print weight
		print selectionFinal
		if isDisplaced : exec("tree = t_"+channel+'CTau1uujj'+str(plotmass))
		else : exec("tree = t_"+channel+str(plotmass))
		#noSelInt = [lumi*xsecs[xsecCounter],lumi*xsecsErr[xsecCounter]]
		noSelInt = [lumi*xsecs[xsecCounter],0]
		xsecCounter = xsecCounter+1
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
		ratiosPresel.append([ratioPresel,ratioPreselErr])
		ratiosFinal.append([ratioFinal,ratioFinalErr])
		if isDisplaced:
			for ctau in ['10','100','1000']:
				exec("tree = t_"+channel+"CTau"+ctau+"uujj"+str(plotmass))
				#noSelInt = [lumi*xsecs[xsecCounter],lumi*xsecsErr[xsecCounter]]
				if ctau=='10':
					noSelInt = [lumi*xsecs[xsecCounter10],0.]
					xsecCounter10 = xsecCounter10+1
				if ctau=='100':
					noSelInt = [lumi*xsecs[xsecCounter100],0.]
					xsecCounter100 = xsecCounter100+1
				if ctau=='1000':
					noSelInt = [lumi*xsecs[xsecCounter1000],0.]
					xsecCounter1000 = xsecCounter1000+1
				preselInt = QuickIntegral(tree,selectionPresel,1.0)
				finalInt = QuickIntegral(tree,selectionFinal,1.0)
				if noSelInt[0]>0: 
					ratioFinal = finalInt[0]/noSelInt[0]
					ratioPresel = preselInt[0]/noSelInt[0]
				else:
					ratioFinal = 0.0
					ratioPresel = 0.0
				if noSelInt[0]>0 and finalInt[0]>0:
					ratioFinalErr = (finalInt[0]/noSelInt[0])*math.sqrt((finalInt[1]**2)/(finalInt[0]**2)+(noSelInt[1]**2)/(noSelInt[0]**2))
					ratioPreselErr = (preselInt[0]/noSelInt[0])*math.sqrt((preselInt[1]**2)/(preselInt[0]**2)+(noSelInt[1]**2)/(noSelInt[0]**2))
				else : 
					ratioFinalErr = 0.0
					ratioPreselErr = 0.0
				exec("ratiosFinalCTau"+ctau+".append([ratioFinal,ratioFinalErr])")
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
	else : 
		ratHistFinal.GetXaxis().SetTitle("m_{LQ} [GeV]")
		ratHistFinal.SetMarkerStyle(20)
		ratHistFinal.SetMarkerColor(kBlue)
		ratHistFinal.SetLineColor(kBlue)
		ratHistFinal.SetLineWidth(2)
		ratHistFinal.SetMarkerSize(1)

	ratHistFinal.GetYaxis().SetTitle("Acceptance #times efficiency")
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
	else :
		ratHistPresel.GetXaxis().SetTitle("m_{LQ} [GeV]")
		ratHistPresel.SetMarkerColor(kBlue)
		ratHistPresel.SetLineColor(kBlue)
		ratHistPresel.SetLineWidth(2)
		ratHistPresel.SetMarkerSize(2)
	ratHistPresel.GetYaxis().SetTitle("Preselection acc. times eff.")
	ratHistFinal.GetXaxis().SetTitleFont(42)
	ratHistFinal.GetYaxis().SetTitleFont(42)
	ratHistFinal.GetXaxis().SetLabelFont(42)
	ratHistFinal.GetYaxis().SetLabelFont(42)
	ratHistFinal.GetXaxis().SetTitleOffset(0.92)
	ratHistFinal.GetYaxis().SetTitleOffset(0.92)
	ratHistFinal.GetXaxis().SetTitleSize(0.06)
	ratHistFinal.GetYaxis().SetTitleSize(0.06)
	ratHistFinal.GetXaxis().SetLabelOffset(0.006)
	ratHistFinal.GetYaxis().SetLabelOffset(0.006)
	ratHistFinal.GetXaxis().SetLabelSize(0.045)
	ratHistFinal.GetYaxis().SetLabelSize(0.045)
	#ratHistFinal.GetXaxis().CenterTitle();
	#ratHistFinal.GetYaxis().CenterTitle();

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
	ratHistFinal.Draw("P")
	l1=TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.06)
	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(62)
	l2.SetNDC()
	l2.SetTextSize(0.06)
	l3=TLatex()
	l3.SetTextAlign(12)
	l3.SetTextFont(42)
	l3.SetNDC()
	l3.SetTextSize(0.06)
	if isPAS:
		l1.DrawLatex(0.13,0.94,"                                                35.9 fb^{-1} (13 TeV)")
	else:
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                              35.9 fb^{-1} (13 TeV)")
	l2.DrawLatex(0.15,0.84,"CMS")
	l1.DrawLatex(0.25,0.84,"#it{Simulation}")
	#l2.SetTextSize(0.05)
	if 'uujj' in channel: l3.DrawLatex(0.155,0.76,"#mu#mujj")
	if 'uvjj' in channel: l3.DrawLatex(0.155,0.76,"#mu#nujj")
	if isDisplaced : 
		ratHistFinalCTau10.Draw("SAMES")
		ratHistFinalCTau100.Draw("SAMES")
		ratHistFinalCTau1000.Draw("SAMES")
	c1.Print('Results_'+version_name+'/signalAcceptanceTimesEfficiency_'+channel+'_FinalSel.pdf')
	print 'Saving histogram: Results_'+version_name+'/signalAcceptanceTimesEfficiency_'+channel+'_FinalSel.pdf'

	if isDisplaced : ratHistPresel.GetYaxis().SetRangeUser(0,max(x for [x,y] in ratiosPresel)*1.1)
	else : ratHistPresel.GetYaxis().SetRangeUser(min(x for [x,y] in ratiosPresel)*.9,max(x for [x,y] in ratiosPresel)*1.1)
	ratHistPresel.Draw()
	if isPAS:
		l1.DrawLatex(0.13,0.94,"                                                35.9 fb^{-1} (13 TeV)")
	else:
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                              35.9 fb^{-1} (13 TeV)")
	l2.DrawLatex(0.15,0.84,"CMS")
	#l2.SetTextSize(0.07)
	l3.DrawLatex(0.15,0.75,channel)
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
	if channel == 'uujj':
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
		#pad1 = TPad( 'pad1', 'pad1', 0.0, 0.4, 1.0, 1.0 )#divide canvas into pads
		#pad2 = TPad( 'pad2', 'pad2', 0.0, 0.26, 1.0, 0.4 )
		#pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.26 )
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.3, 1.0, 1.0 )
		pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 1.0, 0.3 )
		pad1.Draw()
		#pad2.Draw()
		pad3.Draw()
		pad1.SetBottomMargin(0.0)		
		#pad2.SetTopMargin(0.0)
		pad3.SetTopMargin(0.0)
		#pad2.SetBottomMargin(0.0)
		pad3.SetBottomMargin(0.43)
		if 'final' not in tagname:
			perc = syslist[0]
	else:
		# if 'final' not in tagname:
		c1 = TCanvas("c1","",800,550)		
		pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )#divide canvas into pads
		pad1.Draw()
		perc = 5.0
		for m in range(len(pdf_MASS)):
			if str(pdf_MASS[m]) in str(plotmass):
				perc = syslist[m]
		if 'final' not in tagname:
			perc = syslist[0]


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
	TTVStackStyle=[3015,20,.00001,1,28]

	SignalStyle=[0,22,0.7,4,28]
	SignalStyle2=[0,22,0.7,4,38]
	SignalStyle3=[0,22,0.7,4,48]
	SignalStyle4=[0,22,0.7,4,58]

	bgbandstyle=[3002,20,.00001,0,14]


	print 'Getting Final sel '
	if 'final' in tagname:
		print 'cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0'
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0').readlines())[0]).replace('\n','')
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
			t_T = te_SingleMuData
			tt_sel_weight = selection + dataHLT + dataHLTEMUADJ
			print 'Using emu data for ttbar est.'

		# t_T = t_TTPowheg

	print 'Doing Projections'
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',t_W,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',t_SingleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',t_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',t_Z,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	print 'Doing ttbar:'
	#print selection+'*('+str(ttscale)+')*'+weight
	print tt_sel_weight
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',t_T,recovariable,presentationbinning,tt_sel_weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',t_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)
	hs_rec_TTV=CreateHisto('hs_rec_TTV','t#bar{t}V',t_TTV,recovariable,presentationbinning,selection+'*'+weight,TTVStackStyle,Label)
	#hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD',t_QCDMu,recovariable,presentationbinning,selection+'*'+weight,QCDStackStyle,Label)

	if 'TTBarDataDriven' in tagname:

		hs_emu_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',te_WJets,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+NormalWeightEMuNoHLT,WStackStyle,Label)
		hs_emu_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,DiBosonStackStyle,Label)
		hs_emu_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',te_ZJets,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+NormalWeightEMuNoHLT,ZStackStyle,Label)
		hs_emu_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',te_SingleTop,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,StopStackStyle,Label)
		#hs_emu_rec_QCD=CreateHisto('hs_rec_QCD','QCD',te_QCDMu,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,QCDStackStyle,Label)
		hs_emu_rec_WJets.Scale(-1.0)
		hs_emu_rec_DiBoson.Scale(-1.0)
		hs_emu_rec_ZJets.Scale(-1.0)
		hs_emu_rec_SingleTop.Scale(-1.0)
		#hs_emu_rec_QCD.Scale(-1.0)
		hs_rec_TTBar.Add(hs_emu_rec_WJets)
		hs_rec_TTBar.Add(hs_emu_rec_DiBoson)
		hs_rec_TTBar.Add(hs_emu_rec_ZJets)
		hs_rec_TTBar.Add(hs_emu_rec_SingleTop)
		#hs_rec_TTBar.Add(hs_emu_rec_QCD)
		hs_rec_TTBar.Scale(emu_id_eff)



	sig1name = ''
	sig2name = ''

	if channel == 'uujj':
		sig1name = 'm_{LQ} = 1500 GeV, '+betamarker
		sig2name = 'm_{LQ} = 2000 GeV, '+betamarker
		if 'final' not in tagname:
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_LQuujj1500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_LQuujj2000,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
			print 'signal1,',sig1name,':',hs_rec_Signal.Integral()
			print 'signal2,',sig2name,':',hs_rec_Signal2.Integral()
		if 'final' in tagname:
			exec ("_stree = t_LQ"+channel+str(plotmass))
			hs_rec_Signal=CreateHisto('hs_rec_Signal','m_{LQ} = '+str(plotmass)+' GeV, '+betamarker,_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			print 'signal1,',sig1name,':',hs_rec_Signal.Integral()

		wErr=zErr=vvErr=ttErr=stErr=ttvErr=qcdErr=Double(0.)
		wInt=hs_rec_WJets.IntegralAndError(0,-1,wErr)
		zInt=hs_rec_ZJets.IntegralAndError(0,-1,zErr)
		vvInt=hs_rec_DiBoson.IntegralAndError(0,-1,vvErr)
		ttInt=hs_rec_TTBar.IntegralAndError(0,-1,ttErr)
		stInt=hs_rec_SingleTop.IntegralAndError(0,-1,stErr)
		ttvInt=hs_rec_TTV.IntegralAndError(0,-1,ttvErr)
		#qcdInt=hs_rec_QCD.IntegralAndError(0,-1,qcdErr)
		#totBg = wInt+zInt+vvInt+ttInt+stInt+qcdInt
		#totErr = math.sqrt(wErr**2+zErr**2+vvErr**2+ttErr**2+stErr**2+qcdErr**2)
		totBg = wInt+zInt+vvInt+ttInt+stInt
		totErr = math.sqrt(wErr**2+zErr**2+vvErr**2+ttErr**2+stErr**2+ttvErr**2)

		print 'W:  ',wInt#hs_rec_WJets.Integral()
		print 'Z:  ',zInt#hs_rec_ZJets.Integral()
		print 'VV: ',vvInt#hs_rec_DiBoson.Integral()
		print 'TT: ',ttInt#hs_rec_TTBar.Integral()
		print 'ST: ',stInt#hs_rec_SingleTop.Integral()
		print 'TTV: ',ttvInt
		#print 'QCD:',qcdInt#hs_rec_QCD.Integral()
		print 'Total Background:',totBg,'+-',totErr
		print 'Data            :',hs_rec_Data.Integral(0,-1)

		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		hs_rec_DiBoson.Add(hs_rec_TTV)
		#hs_rec_DiBoson.Add(hs_rec_QCD)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets]

	if channel == 'susy':
		sig1name = 'm_{LQ} = 500 GeV'
		sig2name = 'RPV Susy, M = 500 GeV'
		if 'final' not in tagname:
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_LQuujj500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_Susy500,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
		if 'final' in tagname:
			exec ("_stree = t_LQ"+channel+str(plotmass))
			hs_rec_Signal=CreateHisto('hs_rec_Signal','m_{LQ} = '+str(plotmass)+' GeV',_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)

		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		#hs_rec_DiBoson.Add(hs_rec_QCD)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets]

	if isDisplaced:
		sig1name = '#tilde{t}, M = 200 GeV, c#tau=0.1 cm'
		sig2name = '#tilde{t}, M = 500 GeV, c#tau=1 cm'
		if 'final' not in tagname:
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_BLuujj200CTau1,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_BLuujj500CTau10,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
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
		#hs_rec_DiBoson.Add(hs_rec_QCD)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets]

	if channel == 'uvjj':
		if 'final' not in tagname:	
			sig1name = 'm_{LQ} = 850 GeV, '+betamarker
			sig2name = 'm_{LQ} = 1000 GeV, '+betamarker
			hs_rec_Signal=CreateHisto('hs_rec_Signal',sig1name,t_LQuvjj850,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			hs_rec_Signal2=CreateHisto('hs_rec_Signal2',sig2name,t_LQuvjj1000,recovariable,presentationbinning,selection+'*'+weight,SignalStyle2,Label)
		if 'final' in tagname:
			exec ("_stree = t_LQ"+channel+str(plotmass))
			hs_rec_Signal=CreateHisto('hs_rec_Signal','m_{LQ} = '+str(plotmass)+' GeV, '+betamarker,_stree,recovariable,presentationbinning,selection+'*'+weight,SignalStyle,Label)
			
		wErr=zErr=vvErr=ttErr=stErr=qcdErr=Double(0.)
		wInt=hs_rec_WJets.IntegralAndError(0,-1,wErr)
		zInt=hs_rec_ZJets.IntegralAndError(0,-1,zErr)
		vvInt=hs_rec_DiBoson.IntegralAndError(0,-1,vvErr)
		ttInt=hs_rec_TTBar.IntegralAndError(0,-1,ttErr)
		stInt=hs_rec_SingleTop.IntegralAndError(0,-1,stErr)
		#qcdInt=hs_rec_QCD.IntegralAndError(0,-1,qcdErr)
		#totBg = wInt+zInt+vvInt+ttInt+stInt+qcdInt
		#totErr = math.sqrt(wErr**2+zErr**2+vvErr**2+ttErr**2+stErr**2+qcdErr**2)
		totBg = wInt+zInt+vvInt+ttInt+stInt
		totErr = math.sqrt(wErr**2+zErr**2+vvErr**2+ttErr**2+stErr**2)

		print 'W:  ',wInt#hs_rec_WJets.Integral()
		print 'Z:  ',zInt#hs_rec_ZJets.Integral()
		print 'VV: ',vvInt#hs_rec_DiBoson.Integral()
		print 'TT: ',ttInt#hs_rec_TTBar.Integral()
		print 'ST: ',stInt#hs_rec_SingleTop.Integral()
		#print 'QCD:',qcdInt#hs_rec_QCD.Integral()
		print 'Total Background:',totBg,'+-',totErr
		print 'Data            :',hs_rec_Data.Integral()

		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)		
		#hs_rec_DiBoson.Add(hs_rec_QCD)
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
		x.SetMaximum(10*hs_rec_Data.GetMaximum())

	MCStack.Draw("HIST")
	c1.cd(1).SetLogy()
	if 'GoodVertex' in recovariable and 'linscale' in tagname: c1.cd(1).SetLogy(0)
	if 'DPhi' in recovariable or ('MT' in recovariable and 'control' in tagname): c1.cd(1).SetLogy(0)

 	# sysTop->Draw("L");


	MCStack=BeautifyStack(MCStack,Label)
	hs_rec_Signal.Draw("HISTSAME")
	if 'final' not in tagname:
		hs_rec_Signal2.Draw("HISTSAME")
 	if 'PAS' in tagname and 'final' in tagname:
		# sysTop.Draw("F")
		hs_bgband.Draw("E2SAME")
	#fixme adding syst band for now - only works because presel and M200 final sel are the same
	hs_bgband.Draw("E2SAME")
	if 'final' in tagname and isDisplaced:
		hs_rec_Signal2.Draw("HISTSAME")
		hs_rec_Signal3.Draw("HISTSAME")
		hs_rec_Signal4.Draw("HISTSAME")
	#setZeroBinErrors(hs_rec_Data,MCStack)
	blinded=True
	if blinded: blind(hs_rec_Data,recovariable,1,tagname,channel)#fixme
        #hs_rec_Data.Draw("E0PSAME")
	hs_rec_Data_tgraph = TGraphAsymmErrors(hs_rec_Data)
	blinded=True
	if 'BDT' in tagname: blinded=True
	if 'final' not in tagname:
		setZeroBinErrors_tgraph(hs_rec_Data,hs_rec_Data_tgraph,MCStack,hs_rec_Signal,hs_rec_Signal2,blinded)
	else:
	       	setZeroBinErrors_tgraph(hs_rec_Data,hs_rec_Data_tgraph,MCStack,hs_rec_Signal,hs_rec_Signal,blinded)

	hs_rec_Data_tgraph.Draw("ZE0PSAME")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	if 'final' not in tagname:
		if 'PAS' not in tagname:
			leg = TLegend(0.43,0.53,0.89,0.89,"","brNDC");	
		else:
			leg = TLegend(0.4,0.53,0.88,0.89,"","brNDC");	
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
	if channel=='uujj':
		leg.AddEntry(hs_rec_ZJets,'Z/^{}#gamma* + jets')
	if channel=='uvjj':
		leg.AddEntry(hs_rec_WJets,'W + jets')
	leg.AddEntry(hs_rec_TTBar,'t#bar{t}' + (' (e #mu est)')*('TTBarDataDrivena' in tagname))

	leg.AddEntry(hs_rec_DiBoson,'Other background')
	if 'final' not in tagname:
		if 'PAS' in tagname:
			leg.AddEntry(hs_bgband,'Unc. (stat + syst)')
		leg.AddEntry(hs_rec_Signal,sig1name,"l")
		leg.AddEntry(hs_rec_Signal2,sig2name,"l")
	else:
		if 'PAS' in tagname:
			leg.AddEntry(hs_bgband,'Unc. (stat + syst)')
		if isDisplaced:
			leg.AddEntry(hs_rec_Signal, '#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=0.1 cm',"l")
			leg.AddEntry(hs_rec_Signal2,'#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=1   cm',"l")
			leg.AddEntry(hs_rec_Signal3,'#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=10  cm',"l")
			leg.AddEntry(hs_rec_Signal4,'#tilde{t}, M = '+str(plotmass)+' GeV, c#tau=100 cm',"l")
		else:
			leg.AddEntry(hs_rec_Signal,'m_{LQ} = '+str(plotmass)+' GeV, '+betamarker,"l")
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
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                "+lumiInvfb+" fb^{-1} (13 TeV)")
		#l1.DrawLatex(0.64,0.94,"5 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	elif  'PAS' in tagname and 'tagfree' in tagname:
		#l1.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"                                                "+lumiInvfb+" fb^{-1} (13 TeV)")
		#l1.DrawLatex(0.64,0.94,"5 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
		if channel=='uujj':
			l1.DrawLatex(0.155,0.77,"#mu#mujj")
		if channel=='uvjj':
			l1.DrawLatex(0.155,0.77,"#mu#nujj")
	else:
		#l1.DrawLatex(0.18,0.94,"                          "+sqrts+", 225.57 pb^{-1}")
		l1.DrawLatex(0.12,0.94,"#it{Preliminary}                           "+lumiInvfb+" fb^{-1} (13 TeV)")
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
	if 'final' in tagname:
		MCStack.SetMaximum(75*hs_rec_Data.GetMaximum())
	else:
		MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())
	if 'control' in tagname:
		MCStack.SetMaximum(100000*hs_rec_Data.GetMaximum())
	if 'St' in recovariable or 'GoodVertex' in recovariable:
		MCStack.SetMaximum(250*hs_rec_Data.GetMaximum())
	if 'GoodVertex' in recovariable and 'linscale' in tagname:
		MCStack.SetMaximum(2.0*hs_rec_Data.GetMaximum())
	if 'St' in recovariable and 'final' in tagname:
		#MCStack.SetMaximum(50*hs_rec_Data.GetMaximum())
		MCStack.SetMaximum(50*hs_rec_Signal.GetMaximum())
	if 'DPhi' in recovariable or ('MT' in recovariable and 'control' in tagname):
		MCStack.SetMaximum(2.0*hs_rec_Data.GetMaximum())
	if blinded==True and 'final' in tagname:
		MCStack.SetMaximum(100*MCStack.GetMaximum())
	resstring = ''
	if 'PAS' not in tagname:
		pad3.cd()
		# pad2.SetLogy()
		pad3.SetGrid()

		RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)

		RatHistDen.Sumw2()
		RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
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

		RatHistNum.GetXaxis().SetTitleSize(0.14);
		RatHistNum.GetYaxis().SetTitleSize(.12);
		#RatHistNum.GetXaxis().CenterTitle();
		#RatHistNum.GetYaxis().CenterTitle();		
		RatHistNum.GetXaxis().SetTitleOffset(0.);
		RatHistNum.GetYaxis().SetTitleOffset(.45);
		RatHistNum.GetYaxis().SetLabelSize(.1);
		RatHistNum.GetXaxis().SetLabelSize(.09);
		

		if blinded: blind(RatHistNum,recovariable,2,tagname,channel)#fixme
		RatHistNum.Draw("PE0")

	
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
		RatHistNum.Draw("PE0SAMES")

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

		chiplot =CreateHisto('chiplot','chiplot',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
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
		        #fixme syst errors for presel
			bgerr = hs_bgband.GetBinError(n)*hs_bgband.GetBinError(n)
			#
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
		#chiplot.GetXaxis().CenterTitle();
		#chiplot.GetYaxis().CenterTitle();		
		chiplot.GetXaxis().SetTitleOffset(.8);
		chiplot.GetYaxis().SetTitleOffset(.34);
		chiplot.GetYaxis().SetLabelSize(.09);
		chiplot.GetXaxis().SetLabelSize(.09);

		if blinded: blind(chiplot,recovariable,3,tagname,channel)
		chiplot.Draw('EP')
		zero=TLine(RatHistNum.GetXaxis().GetXmin(), 0.0 , RatHistNum.GetXaxis().GetXmax(),0.0)
		plus2=TLine(RatHistNum.GetXaxis().GetXmin(), 2.0 , RatHistNum.GetXaxis().GetXmax(),2.0)
		minus2=TLine(RatHistNum.GetXaxis().GetXmin(), -2.0 , RatHistNum.GetXaxis().GetXmax(),-2.0)
		plus2.SetLineColor(2)
		minus2.SetLineColor(2)

		#plus2.Draw("SAME")
		#minus2.Draw("SAME")
		zero.Draw("SAME")	
		"""


	if 'PAS' in tagname and 'final' in tagname and False:

		pad3.cd()
		pad3.SetLogy()
		pad3.SetGrid()

		RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)

		RatHistDen.Sumw2()
		RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
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
		#RatHistNum.GetXaxis().CenterTitle(1)
		#RatHistNum.GetYaxis().CenterTitle(1)

		RatHistNum.Draw("")
		# sysBot.Draw("F")		
		RatHistNum.Draw("SAME")

		unity=TLine(RatHistNum.GetXaxis().GetXmin(), 1.0 , RatHistNum.GetXaxis().GetXmax(),1.0)
		unity.Draw("SAME")	


	recovariable = recovariable.replace('/','_DIV_')
	
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



def MakeBasicPlotEMuMuMu(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,cutlog,version_name,plotmass):
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	# Create Canvas
	yaxismin = .13333
	perc = 0.0
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

	gStyle.SetOptStat(0)


	pad1.cd()
	# pad1.SetGrid()
	# These are the style parameters for certain plots - [FillStyle,MarkerStyle,MarkerSize,LineWidth,Color]
	MCRecoStyle=[0,20,.00001,1,4]
	DataRecoStyle=[0,20,1.5,1,1]
	# X and Y axis labels for plot
	Label=[xlabel,"Events / bin"]

	WStackStyle=[3007,20,.00001,1,6]
	TTStackStyle=[0,20,1.4,1,1]
	TTStackStyleMuMu=[0,20,1.4,1,2]
	ZStackStyle=[3004,20,.00001,1,2]
	DiBosonStackStyle=[3006,20,.00001,1,3]
	StopStackStyle=[3008,20,.00001,1,7]
	QCDStackStyle=[3013,20,.00001,1,15]

	bgbandstyle=[3002,20,.00001,0,14]


	print 'Getting Final sel '
	if 'final' in tagname:
		print 'cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0'
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0').readlines())[0]).replace('\n','')
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
	print "Regular"
	t_W = t_WJets
	t_Z = t_ZJets
	if 'TTBarDataDriven' not in tagname:
		t_T = t_TTBar
		print 'Using Decay-binned ttbar MC.'
	else:
		t_T = te_SingleMuData
		tt_sel_weight = selection + dataHLT + dataHLTEMUADJ
		print 'Using emu data for ttbar est.'

	print 'Doing Projections'
	### Make the plots without variable bins!
	hs_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',t_W,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+weight,WStackStyle,Label)
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',t_SingleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',t_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',t_Z,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	print 'Doing ttbar:'
	#print selection+'*('+str(ttscale)+')*'+weight
	print tt_sel_weight
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',t_T,recovariable,presentationbinning,tt_sel_weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',t_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)
	#hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD',t_QCDMu,recovariable,presentationbinning,selection+'*'+weight,QCDStackStyle,Label)
	hs_rec_TTBarMuMu=CreateHisto('hs_rec_TTBarMuMu','t#bar{t}',t_TTBar,recovariable,presentationbinning,selection+'*('+str(ttscale)+')*'+weight,TTStackStyleMuMu,Label)

	if 'TTBarDataDriven' in tagname:

		hs_emu_rec_WJets=CreateHisto('hs_rec_WJets','W+Jets',te_WJets,recovariable,presentationbinning,selection+'*('+str(wscale)+')*'+NormalWeightEMuNoHLT,WStackStyle,Label)
		hs_emu_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,DiBosonStackStyle,Label)
		hs_emu_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',te_ZJets,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+NormalWeightEMuNoHLT,ZStackStyle,Label)
		hs_emu_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',te_SingleTop,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,StopStackStyle,Label)
		#hs_emu_rec_QCD=CreateHisto('hs_rec_QCD','QCD',te_QCDMu,recovariable,presentationbinning,selection+'*'+NormalWeightEMuNoHLT,QCDStackStyle,Label)
		hs_emu_rec_WJets.Scale(-1.0)
		hs_emu_rec_DiBoson.Scale(-1.0)
		hs_emu_rec_ZJets.Scale(-1.0)
		hs_emu_rec_SingleTop.Scale(-1.0)
		#hs_emu_rec_QCD.Scale(-1.0)
		hs_rec_TTBar.Add(hs_emu_rec_WJets)
		hs_rec_TTBar.Add(hs_emu_rec_DiBoson)
		hs_rec_TTBar.Add(hs_emu_rec_ZJets)
		hs_rec_TTBar.Add(hs_emu_rec_SingleTop)
		#hs_rec_TTBar.Add(hs_emu_rec_QCD)
		hs_rec_TTBar.Scale(emu_id_eff)

	if channel == 'uujj':
		wErr=zErr=vvErr=ttErr=ttErrMuMu=stErr=qcdErr=Double(0.)
		wInt=hs_rec_WJets.IntegralAndError(0,-1,wErr)
		zInt=hs_rec_ZJets.IntegralAndError(0,-1,zErr)
		vvInt=hs_rec_DiBoson.IntegralAndError(0,-1,vvErr)
		ttInt=hs_rec_TTBar.IntegralAndError(0,-1,ttErr)
		ttIntMuMu=hs_rec_TTBarMuMu.IntegralAndError(0,-1,ttErrMuMu)
		stInt=hs_rec_SingleTop.IntegralAndError(0,-1,stErr)
		#qcdInt=hs_rec_QCD.IntegralAndError(0,-1,qcdErr)
		#totBg = wInt+zInt+vvInt+ttInt+stInt+qcdInt
		#totErr = math.sqrt(wErr**2+zErr**2+vvErr**2+ttErr**2+stErr**2+qcdErr**2)
		totBg = wInt+zInt+vvInt+ttInt+stInt
		totErr = math.sqrt(wErr**2+zErr**2+vvErr**2+ttErr**2+stErr**2)
		
		print 'TT e#mu: ',ttInt
		print 'TT #mu#mu: ',ttIntMuMu

	bgcont = []
	dcont = []
	bgconterr = []

	SM=[hs_rec_TTBarMuMu]
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
		dcont.append(hs_rec_TTBar.GetBinContent(n))

	for c in range(hs_bgband.GetNbinsX()+1):
		_err = math.sqrt( (hs_bgband.GetBinError(c))**2 + (perc*0.01*hs_bgband.GetBinContent(c))**2 )
		hs_bgband.SetBinError(c,_err)
		if hs_bgband.GetBinContent(c) < 0.0001:
			hs_bgband.SetBinContent(c,0.0)
			hs_bgband.SetBinError(c,0.0)

	MCStack = THStack ("MCStack","")
	SMIntegral = sum(k.Integral() for k in SM)
	
	print 'Stacking...  ',	
	for x in SM:
		MCStack.Add(x)
		x.SetMaximum(10*hs_rec_TTBar.GetMaximum())

	MCStack.Draw("ze0p")
	c1.cd(1).SetLogy()

	MCStack=BeautifyStack(MCStack,Label)
	blinded=True
	hs_rec_TTBar_tgraph = TGraphAsymmErrors(hs_rec_TTBar)
	#setZeroBinErrors_tgraph(hs_rec_TTBar,hs_rec_TTBar_tgraph,MCStack,hs_rec_Signal,hs_rec_Signal2,blinded)
	hs_rec_TTBar_tgraph.Draw("ZE0PSAME")

	print 'Legend...  ',
	# Create Legend
	leg = TLegend(0.43,0.53,0.89,0.89,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetFillStyle(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(.05)
	leg.AddEntry(hs_rec_TTBar,'t#bar{t}' + (' (e#mu Data est)')*('TTBarDataDriven' in tagname))

	leg.AddEntry(hs_rec_TTBarMuMu,'t#bar{t} (#mu#mu MC est)')
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
 
	l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                       35.9 fb^{-1} (13 TeV)")
	l2.DrawLatex(0.15,0.84,"CMS")

	gPad.Update()
	gPad.RedrawAxis()

	MCStack.SetMinimum(yaxismin)
	MCStack.SetMaximum(100*hs_rec_TTBar.GetMaximum())
	if 'St' in recovariable or 'GoodVertex' in recovariable:
		MCStack.SetMaximum(250*hs_rec_TTBar.GetMaximum())
	if 'DPhi' in recovariable:
		MCStack.SetMaximum(2.0*hs_rec_TTBar.GetMaximum())
	resstring = ''
	if 'PAS' not in tagname:

		pad2.cd()
		# pad2.SetLogy()
		pad2.SetGrid()

		RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_SingleMuData,recovariable,presentationbinning,'0',TTStackStyle,Label)

		RatHistDen.Sumw2()
		RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_SingleMuData,recovariable,presentationbinning,'0',TTStackStyle,Label)
		RatHistNum.Sumw2()
		for hmc in SM:
			RatHistDen.Add(hmc)

		RatHistNum.Add(hs_rec_TTBar)
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
		#RatHistNum.GetXaxis().CenterTitle();
		#RatHistNum.GetYaxis().CenterTitle();		
		RatHistNum.GetXaxis().SetTitleOffset(.28);
		RatHistNum.GetYaxis().SetTitleOffset(.18);
		RatHistNum.GetYaxis().SetLabelSize(.15);
		RatHistNum.GetXaxis().SetLabelSize(.09);

		#blind(RatHistNum,recovariable,2,tagname,channel)#fixme
		RatHistNum.Draw("PE0")

	
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
		RatHistNum.Draw("PE0SAMES")

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

		pad3.cd()
		# pad2.SetLogy()
		pad3.SetGrid()

		chiplot =CreateHisto('chiplot','chiplot',t_TTBar,recovariable,presentationbinning,'0',TTStackStyle,Label)
		chiplot.Sumw2()

		for n in range(chiplot.GetNbinsX()+1):
			lhs = chiplot.GetBinCenter(n) - 0.5*chiplot.GetBinWidth(n)
			rhs = chiplot.GetBinCenter(n) + 0.5*chiplot.GetBinWidth(n)
			lhs = str(round(lhs,3))
			rhs = str(round(rhs,3))

			bg = 0
			bgerr = 0
			dat = max(0.,hs_rec_TTBar.GetBinContent(n))
			daterr = math.sqrt(1.0*dat)
			for hmc in SM:
				bg += hmc.GetBinContent(n)
				bgerr += hmc.GetBinError(n)*hmc.GetBinError(n)
			bgerr = math.sqrt(bgerr)
			total_err = math.sqrt(bgerr*bgerr+daterr*daterr)
			
			if total_err>0: 
				chi = (dat - bg)/total_err
				chiplot.SetBinContent(n,chi)
				chiplot.SetBinError(n,0.0)

		chiplot.SetMaximum(5.99)
		chiplot.SetMinimum(-5.99)

		chiplot.GetYaxis().SetTitleFont(42);
		# chiplot.GetXaxis().SetTitle('');
		chiplot.GetYaxis().SetTitle('#chi (Data,MC)');
		# chiplot.GetXaxis().SetTitle('#chi (Data,MC)');


		chiplot.GetXaxis().SetTitleSize(.14);
		chiplot.GetYaxis().SetTitleSize(.10);
		#chiplot.GetXaxis().CenterTitle();
		#chiplot.GetYaxis().CenterTitle();		
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

		#plus2.Draw("SAME")
		#minus2.Draw("SAME")
		zero.Draw("SAME")	
	
	gPad.Update()
	l=TLine()
	#l.DrawLine(gPad.GetUxmax(), gPad.GetUymin(), gPad.GetUxmax(), gPad.GetUymax())
	if 'PAS' not in tagname:
	#	l.DrawLine(pad1.GetUxmax(), pad3.GetUymin(), pad1.GetUxmax(), pad1.GetUymax())
		x=1
	else:
		l.DrawLine(pad1.GetUxmax(), pad1.GetUymin(), pad1.GetUxmax(), pad1.GetUymax())
	print 'Saving as: ',
	c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
	c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.png')
	print 'Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.pdf',
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
		print 'cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0'
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0').readlines())[0]).replace('\n','')
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
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',tn_SingleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',tn_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',tn_ZJets,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',tn_TTBar,recovariable,presentationbinning,selection+'*('+str(ttscale)+')*'+weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',tn_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)

	if channel=='uujj':
		if 'weight' in qcdselection:
			hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched',tn_QCDMu,recovariable,presentationbinning,qcdselection+'*('+str(qcdrescale)+')',QCDStackStyle,Label)
		if 'weight' not in qcdselection:
			#hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched',tn_SingleMuData,recovariable,presentationbinning,qcdselection,QCDStackStyle,Label)
			hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched',tn_SingleMuData,recovariable,presentationbinning,qcdselection+'*('+str(qcdrescale)+')',QCDStackStyle,Label)#fixme todo adding ss non-iso scale factor

	if channel=='uvjj':
		hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched',tn_QCDMu,recovariable,presentationbinning,qcdselection+'*('+str(qcdrescale)+')',QCDStackStyle,Label)
		#fixme add validation region, take qcd from non-iso data, subtract non-qcd MC

	print 'Data:',selection+dataHLT
	print 'Other:',selection+weight
	print 'QCD:',qcdselection+'*('+str(qcdrescale)+')'
	
	if channel == 'uujj':

		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_ZJets,hs_rec_QCDMu]

	if channel == 'uvjj':
		if 'VAL' not in tagname:
			hs_rec_DiBoson.SetTitle("Other background")
			hs_rec_DiBoson.Add(hs_rec_ZJets)
			hs_rec_DiBoson.Add(hs_rec_SingleTop)		
			SM=[hs_rec_DiBoson,hs_rec_TTBar,hs_rec_WJets,hs_rec_QCDMu]
		if 'VAL'in tagname:
			hs_rec_DiBoson.Scale(-1.0)
			hs_rec_ZJets.Scale(-1.0)
			hs_rec_SingleTop.Scale(-1.0)
			hs_rec_WJets.Scale(-1.0)
			hs_rec_TTBar.Scale(-1.0)
			hs_rec_Data.Add(hs_rec_DiBoson)
			hs_rec_Data.Add(hs_rec_ZJets)
			hs_rec_Data.Add(hs_rec_SingleTop)
			hs_rec_Data.Add(hs_rec_WJets)
			hs_rec_Data.Add(hs_rec_TTBar)
			SM=[hs_rec_QCDMu]

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

	setZeroBinErrors(hs_rec_Data,MCStack)
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
	if channel=='uujj':
		leg.AddEntry(hs_rec_ZJets,'Z/^{}#gamma* + jets')
	if channel=='uvjj':
		leg.AddEntry(hs_rec_WJets,'W + jets')
	leg.AddEntry(hs_rec_TTBar,'t#bar{t}')
	leg.AddEntry(hs_rec_DiBoson,'Other background')
	leg.AddEntry(hs_rec_QCDMu,'Multijet')
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
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                 35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	else:
		#l2.DrawLatex(0.18,0.94,"                          "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                 35.9 fb^{-1} (13 TeV)")
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

	RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)



	RatHistDen.Sumw2()
	RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
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
	#RatHistNum.GetXaxis().CenterTitle();
	#RatHistNum.GetYaxis().CenterTitle();		
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

	chiplot =CreateHisto('chiplot','chiplot',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
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
	#chiplot.GetXaxis().CenterTitle();
	#chiplot.GetYaxis().CenterTitle();		
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

	#plus2.Draw("SAME")
	#minus2.Draw("SAME")
	zero.Draw("SAME")	


	print 'Saving...  ',
	c1.Print('Results_'+version_name+'/BasicLQQCD_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
	c1.Print('Results_'+version_name+'/BasicLQQCD_'+channel+'_'+recovariable+'_'+tagname+'.png')		
	print 'Done.'


def MakeBasicPlotVV(recovariable,xlabel,presentationbinning,selection,weight,FileDirectory,tagname,channel, zscale, wscale, ttscale,version_name,VVrescale):

	# Load all root files as trees - e.g. file "DiBoson.root" will give you tree called "t_DiBoson"
	# for f in os.popen('ls '+FileDirectory+"| grep \".root\"").readlines():
	# 	exec('t_'+f.replace(".root\n","")+" = TFile.Open(\""+FileDirectory+"/"+f.replace("\n","")+"\")"+".Get(\""+TreeName+"\")")
	tmpfile = TFile("tmpbin.root","RECREATE")
	print "  Preparing basic histo for "+channel+":"+recovariable+"...  "
	# Create Canvas
	# c1 = TCanvas("c1","",800,800)
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

	LOStackStyle=[3007,20,.00001,1,6]
	NLOStackStyle=[3005,20,.00001,1,4]

	print 'Getting Final sel '
	if tagname == 'final':
		print 'cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0'
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0').readlines())[0]).replace('\n','')
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
	hs_rec_DiBoson_LO=CreateHisto('hs_rec_DiBoson_LO','DiBoson (Pythia)',t_DiBoson_Pythia,recovariable,presentationbinning,selection+'*'+weight+'*'+str(VVrescale),LOStackStyle,Label)
	hs_rec_DiBoson_NLO=CreateHisto('hs_rec_DiBoson_NLO','DiBoson (aMC@NLO)',t_DiBoson_amcNLO,recovariable,presentationbinning,selection+'*'+weight,NLOStackStyle,Label)


	plotmax = max(hs_rec_DiBoson_LO.GetMaximum(),hs_rec_DiBoson_NLO.GetMaximum())
	hs_rec_DiBoson_LO.SetMaximum(plotmax)

	hs_rec_DiBoson_LO.Draw("EP")
	c1.cd(1).SetLogy()
	hs_rec_DiBoson_NLO.Draw("EPSAME")

	print 'Legend...  ',
	# Create Legend
	# FixDrawLegend(c1.cd(1).BuildLegend())
	leg = TLegend(0.63,0.62,0.89,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetFillStyle(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(.04)
	leg.AddEntry(hs_rec_DiBoson_LO,"DiBoson (Pythia)");
	leg.AddEntry(hs_rec_DiBoson_NLO,"DiBoson (aMC@NLO)");
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
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                 35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	else:
		#l2.DrawLatex(0.18,0.94,"                          "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                 35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	gPad.RedrawAxis()

	#MCStack.SetMinimum(1.)
	#MCStack.SetMaximum(100*hs_rec_Data.GetMaximum())

	if 'PAS' in tagname:
		print 'Saving...  ',
		c1.Print('Results_'+version_name+'/BasicLQVV_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
		c1.Print('Results_'+version_name+'/BasicLQVV_'+channel+'_'+recovariable+'_'+tagname+'.png')		
		print 'Done.'
		return



	pad2.cd()
	# pad2.SetLogy()
	pad2.SetGrid()

	RatHistDen =CreateHisto('RatHisDen','RatHistDen',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)



	RatHistDen.Sumw2()
	RatHistNum =CreateHisto('RatHisNum','RatHistNum',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
	RatHistNum.Sumw2()
	RatHistDen.Add(hs_rec_DiBoson_LO)

	RatHistNum.Add(hs_rec_DiBoson_NLO)
	RatHistNum.Divide(RatHistDen)
	# for x in RatHistNum.GetNbinsX():
	# 	print RatHistNum.GetBinCenter(x), RatHistNum.GetBinContent(x)

	RatHistNum.SetMaximum(1.5)
	RatHistNum.SetMinimum(0.5)


	RatHistNum.GetYaxis().SetTitleFont(42);
	RatHistNum.GetXaxis().SetTitle('');
	RatHistNum.GetYaxis().SetTitle('NLO / LO');
	RatHistNum.GetYaxis().SetNdivisions(308,True)

	RatHistNum.GetXaxis().SetTitleSize(0.);
	RatHistNum.GetYaxis().SetTitleSize(.20);
	#RatHistNum.GetXaxis().CenterTitle();
	#RatHistNum.GetYaxis().CenterTitle();		
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

	chiplot =CreateHisto('chiplot','chiplot',t_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
	chiplot.Sumw2()

	resstring = '( 0.0 '

	for n in range(chiplot.GetNbinsX()+1):
		lhs = chiplot.GetBinCenter(n) - 0.5*chiplot.GetBinWidth(n)
		rhs = chiplot.GetBinCenter(n) + 0.5*chiplot.GetBinWidth(n)
		lhs = str(round(lhs,3))
		rhs = str(round(rhs,3))

		bg = 0
		bgerr = 0
		dat = hs_rec_DiBoson_NLO.GetBinContent(n)
		daterr = hs_rec_DiBoson_NLO.GetBinError(n)*hs_rec_DiBoson_NLO.GetBinError(n)
		bg += hs_rec_DiBoson_LO.GetBinContent(n)
		bgerr += hs_rec_DiBoson_LO.GetBinError(n)*hs_rec_DiBoson_LO.GetBinError(n)
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
	chiplot.GetYaxis().SetTitle('#chi (NLO,LO)');
	# chiplot.GetXaxis().SetTitle('#chi (Data,MC)');


	chiplot.GetXaxis().SetTitleSize(.14);
	chiplot.GetYaxis().SetTitleSize(.10);
	#chiplot.GetXaxis().CenterTitle();
	#chiplot.GetYaxis().CenterTitle();		
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

	#plus2.Draw("SAME")
	#minus2.Draw("SAME")
	zero.Draw("SAME")	


	print 'Saving...  ',
	c1.Print('Results_'+version_name+'/BasicLQVV_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
	c1.Print('Results_'+version_name+'/BasicLQVV_'+channel+'_'+recovariable+'_'+tagname+'.png')		
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
		# print 'cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0'
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0').readlines())[0]).replace('\n','')
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
	hs_rec_Data=CreateHisto('hs_rec_Data','Data',te_SingleMuData,recovariable,presentationbinning,selection+dataHLT,DataRecoStyle,Label)
	hs_rec_DiBoson=CreateHisto('hs_rec_DiBoson','DiBoson',te_DiBoson,recovariable,presentationbinning,selection+'*'+weight,DiBosonStackStyle,Label)
	hs_rec_ZJets=CreateHisto('hs_rec_ZJets','Z+Jets',te_ZJets,recovariable,presentationbinning,selection+'*('+str(zscale)+')*'+weight,ZStackStyle,Label)
	hs_rec_TTBar=CreateHisto('hs_rec_TTBar','t#bar{t}',te_TTBar,recovariable,presentationbinning,selection+'*('+str(ttscale)+')*'+weight,TTStackStyle,Label)
	hs_rec_SingleTop=CreateHisto('hs_rec_SingleTop','SingleTop',te_SingleTop,recovariable,presentationbinning,selection+'*'+weight,StopStackStyle,Label)
	#hs_rec_QCD=CreateHisto('hs_rec_QCD','QCD',te_QCDMu,recovariable,presentationbinning,selection+'*'+weight,QCDStackStyle,Label)

	print "THIS NUMBER --> hs_rec_TTBar.Integral():",hs_rec_TTBar.Integral(), 'hs_rec_TTBar.GetEntries():',hs_rec_TTBar.GetEntries()

	# hs_rec_QCDMu=CreateHisto('hs_rec_QCDMu','QCD #mu-enriched [Pythia]',te_QCDMu,recovariable,presentationbinning,selection+'*'+weight,QCDStackStyle,Label)

	sig1name = ''
	sig2name = ''

	if channel == 'uujj':
		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_WJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)
		#hs_rec_DiBoson.Add(hs_rec_QCD)
		SM=[hs_rec_DiBoson,hs_rec_ZJets,hs_rec_TTBar]

	if channel == 'uvjj':
		hs_rec_DiBoson.SetTitle("Other background")
		hs_rec_DiBoson.Add(hs_rec_ZJets)
		hs_rec_DiBoson.Add(hs_rec_SingleTop)		
		#hs_rec_DiBoson.Add(hs_rec_QCD)		
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
	leg = TLegend(0.55,0.58,0.81,0.86,"","brNDC");
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
	if  'PAS' in tagname:# and 'tagfree' not in tagname:
		#l2.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                             35.9 fb^{-1} (13 TeV)")
		l2.DrawLatex(0.15,0.84,"CMS")
	else:
		#l2.DrawLatex(0.18,0.94,"                          "+sqrts+", 19.7 fb^{-1}")
		l1.DrawLatex(0.13,0.94,"#it{Preliminary}                                      35.9 fb^{-1} (13 TeV)")
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

	RatHistDen =CreateHisto('RatHisDen','RatHistDen',te_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)



	RatHistDen.Sumw2()
	RatHistNum =CreateHisto('RatHisNum','RatHistNum',te_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
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
	#RatHistNum.GetXaxis().CenterTitle();
	#RatHistNum.GetYaxis().CenterTitle();		
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

	chiplot =CreateHisto('chiplot','chiplot',te_SingleMuData,recovariable,presentationbinning,'0',DataRecoStyle,Label)
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
	#chiplot.GetXaxis().CenterTitle();
	#chiplot.GetYaxis().CenterTitle();		
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

	#plus2.Draw("SAME")
	#minus2.Draw("SAME")
	zero.Draw("SAME")	


	print 'Saving...  ',
	if 'final' not in tagname:
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.pdf')
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.png')
		print 'Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+'.pdf',
	else:
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf')
		c1.Print('Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.png')		
		print 'Results_'+version_name+'/BasicLQ_'+channel+'_'+recovariable+'_'+tagname+str(plotmass)+'.pdf',
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
			if th2.Integral(x,nx,y,ny)>0:
				res.append([thname,[addon, th2.GetXaxis().GetBinCenter(x) - 0.5*th2.GetXaxis().GetBinWidth(x), th2.GetYaxis().GetBinCenter(y) - 0.5*th2.GetYaxis().GetBinWidth(y)],th2.Integral(x,nx,y,ny)])
			else:
				res.append([thname,[addon, th2.GetXaxis().GetBinCenter(x) - 0.5*th2.GetXaxis().GetBinWidth(x), th2.GetYaxis().GetBinCenter(y) - 0.5*th2.GetYaxis().GetBinWidth(y)],0])#fixme avoiding negative integrals because it goes into a log calculation

	return res


def GetRatesFromTH2(sigs,baks,_presel,_weight,_hvars,addon,scalefac):
	for f in NormalFiles:
		_tree = 't_'+f.split('/')[-1].replace(".root","")
		_treeTmp = _tree+"_tmp"
		_prefix = ''# +'root://eoscms//eos/cms'*('/store' in NormalDirectory)#fixme removing since eos is hosted on /eos now
		#print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	        #print (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
		exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	        #print (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")
		exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

	b1 = ConvertBinning(_hvars[0][1])
	b2 = ConvertBinning(_hvars[1][1])
	v1 = (_hvars[0][0])
	v2 = (_hvars[1][0])
	allinfo = []
	for t in sigs+baks:
		print 'Checking:',t
		h = 'h_'+t
		#print( h + ' = TH2D("'+h+'","'+h+'",len(b1)-1,array(\'d\',b1),len(b2)-1,array(\'d\',b2))')
		exec(  h + ' = TH2D("'+h+'","'+h+'",len(b1)-1,array(\'d\',b1),len(b2)-1,array(\'d\',b2))')
		#print( t+'.Project("'+h+'","'+v2+':'+v1+'","'+_presel+'*('+_weight+'*'+scalefac+')")')
		exec(  t+'.Project("'+h+'","'+v2+':'+v1+'","'+_presel+'*('+_weight+'*'+scalefac+')")')
		exec( 'allinfo += TH2toCutRes ('+h+',"'+h+'",'+str(addon)+')')
		# break
	return allinfo


def OptimizeCuts3D(variablespace,presel,weight,tag,scalefacs,cutfile,channel):

	for f in NormalFiles:
		_tree = 't_'+f.split('/')[-1].replace(".root","")
		_treeTmp = _tree+"_tmp"
		_prefix = ''# +'root://eoscms//eos/cms'*('/store' in NormalDirectory)#fixme removing since eos is hosted on /eos now
		print(_tree+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")"+".Get(\""+TreeName+"\")")
	        #print (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
		exec (_treeTmp+" = TFile.Open(\""+_prefix+NormalDirectory+"/"+f.replace("\n","")+"\",\"READ\")")
	        #print (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")
		exec (_tree+" = "+_treeTmp+".Get(\""+TreeName+"\")")

	if 'BL' in channel:
		signalType = 'BL'
		channel = 'uujj'
	else:
		signalType = 'LQ'
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

	background =  [ 't_'+x.replace('\n','') for x in  ['DiBoson','WJets','TTBar','ZJets','SingleTop','TTV']]#original 
	#background =  [ 't_'+x.replace('\n','') for x in  ['QCDMu','DiBoson','WJets','TTBar','ZJetsOpt','SingleTop']]#fixme this is if we use the 1/5 statistics ZJets for optimization to avoid 'overtraining'
	#background =  [ 't_'+x.replace('\n','') for x in  ['QCDMu','DiBoson','WJets','TTBar','ZJets','SingleTop']]
	#if '/store/' in NormalDirectory:#fixme removing since eos is hosted on /eos now
	#	signals =  [ x.replace('.root\n','') for x in  os.popen('/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls '+NormalDirectory+'| grep root | grep '+signalType+channel+' ').readlines()]
	#else:
	signals =  [ (x.replace('.root','').replace('\n','').replace(' ','').replace('\t',''),int(x.replace('.root','').replace('\n','').replace(signalType+channel,''))) for x in  os.popen('ls '+NormalDirectory+'| grep root | grep '+signalType+channel+' ').readlines()]

	#now sort the signals by mass
	signals = ['t_'+x for (x,y) in sorted(signals, key = lambda element : element[1])]

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

	# Get LQ cross sections from ntuple info csv files 
	channelDict = {'uujj':'pair','uuj':'single','1':'BMu','2':'BMu','0':'SMu'}
	with open('NTupleInfo'+year+'Full_stockNano.csv','read') as NTupleInfocsv:
		xsecs = [float(line.split(',')[1]) for line in NTupleInfocsv if 'LQTo'+channelDict[btags] in line and channelDict[channel] in line]
	NTupleInfocsv.close()

	for S in range(len(SIGS)):
		_ssbmax = -99999
		_bestcut = 0
		for icut in range(len(SIGS[S])):
			#print SIGS[S],'\n'
			_s = SIGS[S][icut][0]
			_b = 0.0
			_sOrig = xsecs[S]*lumi
			for B in BAKS:
				_b += B[icut][0]
			if _s + _b < 0.001: #was 0.0001
				continue
			_sEff  = _s / _sOrig
			#_ssb = _s/math.sqrt(_s+_b)#fixme original
			#if (1.0+_s/_b)>0 and (2.0*((_s+_b)*math.log(1.0+_s/_b)-_s))>0:#fixme why are we getting negative #s in the first place?
			_ssb=0#fixme avoiding division by 0 and negative backgrounds from amc@NLO
			#if _b<0.: 
			#	_b=0.
			if _b>1.0 :
				#_ssb = math.sqrt(2.0*((_s+_b)*math.log(1.0+_s/_b)-_s))#fixme trying eq 96 from paper DOI:10.1140/epjc/s10052-011-1554-0
			        #fixme trying Punzi significance
			        _ssb = _sEff/(2.5+math.sqrt(_b))
			#else: _ssb=0
			if _ssb > _ssbmax :
				_ssbmax = _ssb
				_bestcut = icut
		opt = 'opt_'+signals[S].replace('t_','')+ ' = (('+minvar[0] +'>' + str(SIGS[S][_bestcut][1][0])+')*('+hvars[0][0]+'>'+str(SIGS[S][_bestcut][1][1])+')*('+hvars[1][0]+'>'+str(SIGS[S][_bestcut][1][2])+'))\n'  
		print opt
		thismass = float(((signals[S].replace('t_','')).split('jj'))[-1])
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
		if "M_uu" in a :  x = "m_{#mu#mu}"
		if "M_uujj1" in a :  x = "m_{#muj}_{1}"
		if "M_uujj2" in a :  x = "m_{#muj}_{2}"
		if "GoodVertexCount" in a :  x = "N_{Vertices}"
		if "Pt_jet1" in a :  x = "p_{T}(jet_{1})"
		if "Pt_jet2" in a :  x = "p_{T}(jet_{2})"
		if "Pt_muon1" in a :  x = "p_{T}(#mu_{1})"
		if "Pt_miss" in a :  x = "E_{T}^{miss}"
		if "St_uvjj" in a :  x = "S_{T}^{#mu#nujj}"
		if "MT_uv in" in a :  x = "m_{T}^{#mu#nu}"
		if "MT_uvjj" in a :  x = "m_{T}^{#muj}"
		if "M_uvjj" in a :  x = "m_{#muj}"
		xnames.append(x)

	_allvals = sorted(vals,key=lambda vals: vals[0])


	if 'cutoff' in rawmethod:
		_vals = []
		if 'uujj' in chan: cutoffVal=1250
		elif 'uvjj' in chan: cutoffVal=1300
		for v in _allvals:
			if v[0] <= cutoffVal :
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
		#hout.GetXaxis().CenterTitle();
		#hout.GetYaxis().CenterTitle();
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
	print 'here',m,s1,s2
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
		mavg = _m[x]#*(_m[x]>0)+0.0*(_m[x]<0)#fixme this is for negative integrals in amcNLO
		sv1 = _s1[x]#*(_s1[x]>0)+0.0*(_s1[x]<0)#fixme this is for negative integrals in amcNLO
		sv2 = _s2[x]#*(_s2[x]>0)+0.0*(_s2[x]<0)#fixme this is for negative integrals in amcNLO
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

	syslinesMax=[]#used in case we need to hold systematics constant after a certain mass value
	sys1uvjj300, sys2uvjj300=[],[]#used in case we need to hold an individual systematic constant after a certain mass value

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
		LQmass = mcard.split('=')[0].split(':')[-1].split('LQ')[-1]
		channel = LQmass.split('jj')[0]+'jj'
		LQmass = LQmass.split('jj')[-1]
		#print 'LQmass',channel,LQmass
		# print ' \n '
		weights = []
		nums = []
		rates = []
		amcNlo0 =[]
		for entry in minfo:
			if entry[1] > 0.0001 and entry[0] >= 0:#fixme this is for negative integrals in amcNLO
				weights.append((1.0*entry[0])/(1.0*entry[1]))
				nums.append(int(entry[1]))#fixme this is for negative integrals in amcNLO
				rates.append(entry[0])#fixme this is for negative integrals in amcNLO
				amcNlo0.append(1)
			else:
				weights.append(0.0)
				nums.append(int(entry[1]))#fixme this is for negative integrals in amcNLO - sets neg. number to 0
				rates.append(0.0)#fixme this is for negative integrals in amcNLO
				amcNlo0.append(0)
			#original
			#if entry[1] > 0.001:
			#	weights.append((1.0*entry[0])/(1.0*entry[1]))
			#else:
			#	weights.append(0)
			#nums.append(int(entry[1]))
			#rates.append(entry[0])

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
			#z=amcNlo0[h]
			if w <0.0000000001:# and z>0:#fixme for neg integrals in amcnlo - check
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
			if 'uvjj' in channel and ('MES' in v):
				if int(LQmass)==550: sys1uvjjMES = sysline
				if int(LQmass)>550: sysline = sys1uvjjMES
			if 'uvjj' in channel and ('PDF' in v):
				if int(LQmass)==550: sys1uvjjPDF = sysline
				if int(LQmass)>550: sysline = sys1uvjjPDF
			if 'uvjj' in channel and ('JER' in v):
				if int(LQmass)==550: sys1uvjjJER = sysline
				if int(LQmass)>550: sysline = sys1uvjjJER
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
		
		#if channel=='uujj' and int(LQmass)==1500:
		#	syslinesMax = syslines
		if channel=='uvjj' and int(LQmass)==900:
			syslinesMax = syslines

		#if channel=='uujj' and int(LQmass)>1500:
		#	syslines = syslinesMax
		if channel=='uvjj' and int(LQmass)>900:
			syslines = syslinesMax
		
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
	#Sels = [NoSelection,Selection,PreSelection]
	Sels = [PreSelection]
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
	VVpercsUp = []
	ZpercsDown =  []
	WpercsDown =  []
	ttpercsDown = []
	VVpercsDown = []
	shapesysvar_Zjets = []
	shapesysvar_Wjets = []
	shapesysvar_TTjets = []
	shapesysvar_VVjets = []
	
	Rz_diff = dict((x,0.) for x in scaleWeights)
	Rz_err_diff = dict((x,0.) for x in scaleWeights)
	Rw_diff = dict((x,0.) for x in scaleWeights)
	Rw_err_diff = dict((x,0.) for x in scaleWeights)
	Rtt_diff = dict((x,0.) for x in scaleWeights)
	Rtt_err_diff = dict((x,0.) for x in scaleWeights)
	RVV_diff = dict((x,0.) for x in scaleWeights)
	RVV_err_diff = dict((x,0.) for x in scaleWeights)

	#Get un-modified presel scale factors
	#munu1 = '(MT_uv>70)*(MT_uv<110)*(((CISV_jet1>0.5426)+(CISV_jet2>0.5426))<1)*(2-0.887973*((1.+(0.0523821*Pt_jet1))/(1.+(0.0460876*Pt_jet1))))'
	#munu2 = '(MT_uv>70)*(MT_uv<110)*(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>=1)*(0.561694*((1.+(0.31439*Pt_jet1))/(1.+(0.17756*Pt_jet1))))'#*(CISV_jet1>CISV_jet2)+(0.901114+(1.40704e-05*(Pt_jet2)))*(CISV_jet2>0.8484)*(CISV_jet1<CISV_jet2))'
	#munu1 = '(MT_uv>100)*(MT_uv<150)*(((CISV_jet1>0.5)+(CISV_jet2>0.5))<1)'
	#munu2 = '(MT_uv>100)*(MT_uv<150)*(((CISV_jet1>0.8484)+(CISV_jet2>0.8484))>=1)*((0.901114+(1.32145e-05*(Pt_jet1))))'#*(CISV_jet1>CISV_jet2)+(0.901114+(1.40704e-05*(Pt_jet2)))*(CISV_jet2>0.8484)*(CISV_jet1<CISV_jet2))'
	[[Rz_uujj,Rz_uujj_err],[Rtt_uujj,Rtt_uujj_err]] = GetMuMuScaleFactors( NormalWeightMuMu+'*'+preselectionmumu, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0,1)
	[[Rw_uvjj,Rw_uvjj_err],[Rtt_uvjj,Rtt_uvjj_err]] = GetMuNuScaleFactors( NormalWeightMuNu+'*'+preselectionmunu, NormalDirectory,munu1,munu2,1)

	#Get presel scale factors for each weight
	for weight in scaleWeights:
		if 'uujj' in channel:
			[[Rz_diff[weight],Rz_err_diff[weight]],[Rtt_diff[weight],Rtt_err_diff[weight]]] = GetMuMuScaleFactors(NormalWeightMuMu+'*'+preselectionmumu+'*'+weight, NormalDirectory, '(M_uu>80)*(M_uu<100)', '(M_uu>100)',0,1)
		elif 'uvjj' in channel:
			[[Rw_diff[weight],Rw_err_diff[weight]],[Rtt_diff[weight],Rtt_err_diff[weight]]] = GetMuNuScaleFactors(NormalWeightMuNu+'*'+preselectionmunu+'*'+weight, NormalDirectory, munu1, munu2,1)
	for selection in Sels :
		print '  ',selection[1]

		maxZ =[0.,0.]
		maxW =[0.,0.]
		maxTT=[0.,0.]
		maxVV=[0.,0.]
		for weight in scaleWeights:
			print '     ',weight
			thisSel = selection[0]+'*'+weight

			if 'uujj' in channel:
				Z  = QuickIntegral(t_ZJets,selection[0]+'*'+str(Rz_uujj),1.0)
				W  = QuickIntegral(t_WJets,selection[0],1.0)
				tt = QuickIntegral(t_TTBar,selection[0]+'*'+str(Rtt_uujj),1.0)
				VV = QuickIntegral(t_DiBoson,selection[0],1.0)
				Z_diff  = QuickIntegral(t_ZJets,thisSel+'*'+str(Rz_diff[weight]),1.0)
				W_diff  = W
				tt_diff = QuickIntegral(t_TTBar,thisSel+'*'+str(Rtt_diff[weight]),1.0)
				VV_diff = QuickIntegral(t_DiBoson,thisSel,1.0)
			
			elif 'uvjj' in channel:
				Z  = QuickIntegral(t_ZJets,selection[0],1.0)
				W  = QuickIntegral(t_WJets,selection[0]+'*'+str(Rw_uvjj),1.0)
				tt = QuickIntegral(t_TTBar,selection[0]+'*'+str(Rtt_uvjj),1.0)
				VV = QuickIntegral(t_DiBoson,selection[0],1.0)
				Z_diff  = Z
				W_diff  = QuickIntegral(t_WJets,thisSel+'*'+str(Rw_diff[weight]),1.0)
				tt_diff = QuickIntegral(t_TTBar,thisSel+'*'+str(Rtt_diff[weight]),1.0)
				VV_diff = QuickIntegral(t_DiBoson,thisSel,1.0)
	                        #print Z, Z_diff
				#print W, W_diff

			Zperc=Wperc=TTperc=VVperc=[0.0,0.0]
			if Z[0]>0 and abs(Z_diff[0]-Z[0])>0 : 
				Zperc =  [100*(abs(Z_diff[0]-Z[0])/Z[0]),100*math.sqrt((math.sqrt(Z_diff[1]*Z_diff[1]+Z[1]*Z[1])/(Z[0]*Z[0]))+
								       ((Z_diff[0]-Z[0])*(Z_diff[0]-Z[0])*Z[1]*Z[1]/(Z[0]*Z[0]*Z[0]*Z[0])))]
			else : ZPerc=[0.,0.]
			if W[0]>0  and abs(W_diff[0]-W[0])>0 : 
				Wperc =  [100*(abs(W_diff[0]-W[0])/W[0]),100*math.sqrt((math.sqrt(W_diff[1]*W_diff[1]+W[1]*W[1])/(W[0]*W[0]))+
								       ((W_diff[0]-W[0])*(W_diff[0]-W[0])*W[1]*W[1]/(W[0]*W[0]*W[0]*W[0])))]
			else : Wperc=[0.,0.]
			if tt[0]>0 : 
				TTperc =  [100*(abs(tt_diff[0]-tt[0])/tt[0]),100*math.sqrt((math.sqrt(tt_diff[1]*tt_diff[1]+tt[1]*tt[1])/(tt[0]*tt[0]))+
									   ((tt_diff[0]-tt[0])*(tt_diff[0]-tt[0])*tt[1]*tt[1]/(tt[0]*tt[0]*tt[0]*tt[0])))]
			else : TTperc=[0.,0.]
			if VV[0]>0 : 
				VVperc =  [100*(abs(VV_diff[0]-VV[0])/VV[0]),100*math.sqrt((math.sqrt(VV_diff[1]*VV_diff[1]+VV[1]*VV[1])/(VV[0]*VV[0]))+
									   ((VV_diff[0]-VV[0])*(VV_diff[0]-VV[0])*VV[1]*VV[1]/(VV[0]*VV[0]*VV[0]*VV[0])))]
			else : VVperc=[0.,0.]
		
			print '        Z:',Zperc
			print '        W:',Wperc
			print '       tt:',TTperc
			print '       VV:',VVperc
			if Zperc[0]>maxZ[0]  : maxZ = Zperc
			if Wperc[0]>maxW[0]  : maxW = Wperc
			if TTperc[0]>maxTT[0]: maxTT=TTperc
			if VVperc[0]>maxVV[0]: maxVV=VVperc
			if scaleWeights[-1] in weight:		
				print ' Final  Z:',maxZ
				print ' Final  W:',maxW
				print ' Final tt:',maxTT
				print ' Final VV:',maxVV
	
		shapesysvar_Zjets.append (round(maxZ[0],2))
		shapesysvar_Wjets.append (round(maxW[0],2))
		shapesysvar_TTjets.append(round(maxTT[0],2))
		shapesysvar_VVjets.append(round(maxVV[0],2))
		
	print '\n\n--------------\n--------------\nFinal systematics (Presel then final selections):'

	print 'shapesysvar_'+channel+'_zjets  =',shapesysvar_Zjets
	print 'shapesysvar_'+channel+'_wjets  =',shapesysvar_Wjets
	print 'shapesysvar_'+channel+'_ttjets =',shapesysvar_TTjets
	print 'shapesysvar_'+channel+'_vvjets =',shapesysvar_VVjets

	
	#sys.stdout.write('shapesysvar')
	#sys.stdout.write(channel)
        #sys.stdout.write('_zjets = ')
        #sys.stdout.write(shapesysvar_Zjets)

	#sys.stdout.write('shapesysvar')
        #sys.stdout.write(channel)
        #sys.stdout.write('_wjets = ')
        #sys.stdout.write(shapesysvar_Wjets)

	#sys.stdout.write('shapesysvar')
        #sys.stdout.write(channel)
        #sys.stdout.write('ttjets = ')
        #sys.stdout.write(shapesysvar_TTjets)

def blind(h,name,num,tag,chan):
	#print name
	#name = h.GetName()
	blindstart = 9999
	if name == 'M_uu':
		blindstart = 300
	elif 'St' in name and 'uujj' in chan:
		blindstart = 1500
	elif 'uujj2' in name:
		blindstart = 800
	elif ('M_uu' in name and 'uujj2' not in name) or 'Pt_muon1' in name or 'Pt_miss' in name or 'MT_uv' in name:
		blindstart = 800
	elif 'Pt_muon2' in name:
		blindstart=300
	if 'final' in tag:
		blindstart=0
	for bin in range(h.GetNbinsX()):
		if h.GetBinLowEdge(bin+1)>blindstart:
			if num==1:
				h.SetBinContent(bin+1,0.0)
				h.SetBinError(bin+1,0.0)
			if num==2 or num==3:
				h.SetBinContent(bin+1,-50.0)
				h.SetBinError(bin+1,0.0)
			if 'final' in tag:
				h.SetBinContent(bin+1,.0001)
				h.SetBinError(bin+1,0.0)
	#h.SetMarkerSize(0.0)
	#h.SetLineWidth(0)

def makeOptPlotForPAS(cutlog, channel, version_name, isPAS):
	c1 = TCanvas("c1","",800,600)		
	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 1.0, 1.0 )
	pad1.Draw()
	gStyle.SetOptStat(0)

	with open(cutlog,'read') as cutlogfile:
		masses = [int(re.search('[0-9]+',line).group(0)) for line in cutlogfile]
	cutlogfile.close()

	#if channel == 'uujj':
	#	uujj=1

	n = len(masses)-1
	mass,var1Name,var1,var2Name,var2,var3Name,var3 = [],[],[],[],[],[],[]
	for plotmass in masses:
		#print plotmass
		#print 'cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0'
		fsel = ((os.popen('cat '+cutlog+' | grep '+channel+str(plotmass)+' | grep -v '+channel+str(plotmass)+'0').readlines())[0]).replace('\n','')
		#print 'found'
		fsel = fsel.replace('(',' ').replace('*',' ').replace(')',' ').replace('opt_LQ'+channel,' ').replace('>',' ')
		fsel=fsel.split()
		#print fsel
		#print float(fsel[0]),fsel[2],float(fsel[3]),fsel[4], float(fsel[5]),fsel[6],float(fsel[7])
		mass.append(float(fsel[0]))
		var1Name.append(fsel[2])
		var1.append(float(fsel[3]))
		var2Name.append(fsel[4])
		var2.append(float(fsel[5]))
		var3Name.append(fsel[6])
		var3.append(float(fsel[7]))
	#print 	mass
	#print var1Name
	#print var1
	#print var2Name
	#print var2
	#print var3Name
	print var3


	hout1= TH1D('hout1',';m_{LQ} [GeV];Final selection value [GeV]',n,array('d',masses))
	hout1.Sumw2()
	hout1.SetFillStyle(0)
	hout1.SetMarkerStyle(8)
	hout1.SetMarkerSize(1)
	hout1.SetLineWidth(3)
	hout1.SetMarkerColor(kBlack)
	hout1.SetLineColor(kBlack)
	hout1.SetFillColor(0)
	hout1.SetFillColor(0)
	hout1.GetXaxis().SetTitleFont(42)
	hout1.GetYaxis().SetTitleFont(42)
	hout1.GetXaxis().SetLabelFont(42)
	hout1.GetYaxis().SetLabelFont(42)
	#hout1.GetXaxis().CenterTitle(1)
	#hout1.GetYaxis().CenterTitle(1)
	hout1.GetXaxis().SetLabelOffset(0.008)
	hout1.GetYaxis().SetLabelOffset(0.008)
	hout1.GetXaxis().SetLabelSize(0.045)
	hout1.GetYaxis().SetLabelSize(0.045)
	hout1.GetXaxis().SetTitleOffset(1.1)
	hout1.GetYaxis().SetTitleOffset(1.07)
	hout1.GetXaxis().SetTitleSize(0.058)
	hout1.GetYaxis().SetTitleSize(0.058)

	hout2= TH1D('hout2',';m_{LQ} [GeV];Final selection value [GeV]',n,array('d',masses))
	hout2.Sumw2()
	hout2.SetFillStyle(0)
	hout2.SetMarkerStyle(21)
	hout2.SetMarkerSize(1)
	hout2.SetLineWidth(3)
	hout2.SetMarkerColor(kBlue)
	hout2.SetLineColor(kBlue)
	hout2.SetFillColor(0)
	hout2.SetFillColor(0)

	hout3= TH1D('hout3',';m_{LQ} [GeV];Final selection value [GeV]',n,array('d',masses))
	hout3.Sumw2()
	hout3.SetFillStyle(0)
	hout3.SetMarkerStyle(22)
	hout3.SetMarkerSize(1)
	hout3.SetLineWidth(3)
	hout3.SetMarkerColor(kRed)
	hout3.SetLineColor(kRed)
	hout3.SetFillColor(0)
	hout3.SetFillColor(0)

	for x in range(len(masses)):
		hout1.SetBinContent(x+1,var1[x])
		hout2.SetBinContent(x+1,var2[x])
		hout3.SetBinContent(x+1,var3[x])

	if channel=='uujj':
		hout1.GetYaxis().SetRangeUser(0,2000)
	if channel=='uvjj':
		hout1.GetYaxis().SetRangeUser(0,3000)
		#hout1.SetMarkerColor(k)
		#hout1.SetLineColor(k)
		hout1.SetMarkerColor(kRed)
		hout1.SetLineColor(kRed)
		hout3.SetMarkerColor(kBlack)
		hout3.SetLineColor(kBlack)
		hout1.SetMarkerStyle(22)
		hout3.SetMarkerStyle(8)

	hout1.Draw("lp")
	hout2.Draw("lpsames")
	hout3.Draw("lpsames")
	
	l1=TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.045)
	l2=TLatex()
	l2.SetTextAlign(12)
	l2.SetTextFont(62)
	l2.SetNDC()
	l2.SetTextSize(0.06)
	l3=TLatex()
	l3.SetTextAlign(12)
	l3.SetTextFont(42)
	l3.SetNDC()
	l3.SetTextSize(0.05)
	if isPAS:
		l1.DrawLatex(0.13,0.93,"                                                               35.9 fb^{-1} (13 TeV)")
	else:
		l1.DrawLatex(0.13,0.93,"#it{Preliminary}                                             35.9 fb^{-1} (13 TeV)")
	l2.DrawLatex(0.15,0.85,"CMS")

	if channel=='uujj':
		l3.DrawLatex(.15,.79,"#mu#mujj")
	if channel=='uvjj':
		l3.DrawLatex(.15,.79,"#mu#nujj")

	#leg = TLegend(0.15,0.48,0.25,0.75,"","brNDC");
	leg = TLegend(0.27,0.6,0.37,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetFillStyle(0);
	leg.SetBorderSize(0);
	names = {'St_uujj':'S_{T}^{#mu#mujj}','St_uvjj':'S_{T}^{#mu#nujj}','M_uu':'m_{#mu#mu}','M_uujj2':'m_{#muj}^{min}','M_uvjj':'m_{#muj}','MT_uv':'m_{T}^{#mu#nu}'}
	if channel=='uujj':
		leg.AddEntry(hout1,names[var1Name[0]],"lp")
		leg.AddEntry(hout3,names[var3Name[0]],"lp")
		leg.AddEntry(hout2,names[var2Name[0]],"lp")
	if channel=='uvjj':
		leg.AddEntry(hout3,names[var3Name[0]],"lp")
		leg.AddEntry(hout1,names[var1Name[0]],"lp")
		leg.AddEntry(hout2,names[var2Name[0]],"lp")
	leg.Draw()
	c1.Print('Results_'+version_name+'/optPlot'+channel+'_FinalSel.pdf')
	print 'Saving histogram: Results_'+version_name+'/optPlot'+channel+'_FinalSel.pdf'

main()

