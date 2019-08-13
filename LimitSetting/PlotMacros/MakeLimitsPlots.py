import os
import sys, getopt
import ROOT
from ROOT import *
import random
import time
import datetime
from array import array
import math


def main():
	###----------------------------------------------------------###
	###------------------ USAGE ---------------------------------###
	###----------------------------------------------------------###
	#
	#	python MakeLimitsPlots.py --channel CombMuEle  --resType HHres --obslimit 1
	#
	###----------------------------------------------------------###
	###----------------------------------------------------------###
	
	whichChannel = ''
	resType = ''
	_obs_limit = 0
	
	for x in range(len(sys.argv)):
		if sys.argv[x] == '--channel':
			whichChannel = sys.argv[x+1]
		if sys.argv[x] == '--resType':
			resType = sys.argv[x+1]
		if sys.argv[x] == '--obslimit':
			_obs_limit = int(sys.argv[x+1])
	print ' whichChannel ', whichChannel, ' resType ', resType, ' _obs_limit ', _obs_limit

	do_noBR = 1
	do_bbuujj = 0
	if (whichChannel == "CombMuEle"):
		do_noBR = 1
		do_bbuujj = 0
	elif (whichChannel == "muon"):
		do_noBR = 1
		do_bbuujj = 0
	elif (whichChannel == "ele"):
		do_noBR = 1
		do_bbuujj = 0
	if (do_noBR): do_bbuujj = 0

	nTH=11
	mTh = [200, 260, 300, 400, 500, 600, 700, 750, 800, 900, 1000]
	
	###############THIS IS THE PARTICLE TO USE FOR SPIN 0 ###############################
	# need to multiply these numbers by 9 to get to LR 1TeV scenario, according to Xanda
	Radion_RS1_GF_NLO_13TeV_LR_3TeV = [12.6708, 7.00006, 4.84338, 2.203, 1.288, 0.815, 0.532, 0.434, 0.36, 0.246941, 0.1729559]
	# even though it is bulk, Xanda says numbers also work for RS1 radion
	Radion_Bulk_Decay_long_kl_35_arxiv11106452 = [0, 0.242876, 0.324309, 0.284102, 0.250955, 0.240894, 0.237688, 0.23708, 0.236795, 0.236731, 0.236958]
	total_Radion_RS1 = [x*y for x, y in zip(Radion_RS1_GF_NLO_13TeV_LR_3TeV, Radion_Bulk_Decay_long_kl_35_arxiv11106452)]
	total_Radion_RS1 = [x*9 for x in total_Radion_RS1]
	# the difference with HIG-17-006 is that they use Bulk Radion, while we try to be consistent and use RS1 Radion, the difference is about x2
	# at 260 gev we will have for 2b2l2nu (7*0.2428* (0.0012 + 0.0266)*1000*9) = 425, while bbWW has (10.31*0.2428* (0.0012 + 0.0266)*1000*9)=626.3176536

	###############THIS IS THE PARTICLE TO USE FOR SPIN 2 ###############################
	#https://github.com/CrossSectionsLHC/WED/blob/master/KKGraviton_RS1/GF_NLO_13TeV_ktilda_0p1.txt
	#https://github.com/CrossSectionsLHC/WED/blob/master/KKGraviton_RS1/Decay_long.txt
	KKGraviton_RS1_GF_NLO_13TeV_xsecs = [39275.98, 14445.39, 8033.67, 2481.79, 937.05, 415.62, 205.6, 146.43, 105.82, 60.5, 36.13]
	KKGraviton_RS1_Decay_long_toHH = [0., 7.875333606243e-6, 0.0002609363907507743, 0.0014748453016228675, 0.002474422167974112, 0.0031442653849825413, 0.0035917787224510177, 0.003759423688146883, 0.0038997130095538993,0.004118727164348575, 0.00427930100894505]
	total_KKGraviton_RS1 = [x*y for x, y in zip(KKGraviton_RS1_GF_NLO_13TeV_xsecs, KKGraviton_RS1_Decay_long_toHH)]
	
#	############### Bulk RS ###############
#	# for bblljj ( xec pp->R->HH->bblljj ), lambda=3TeV, kL=35
#	Radion_Bulk_bblljj_LR_3TeV_kl_35 = [10.7916, 10.0599, 4.1241, 2.1212, 1.2826, 0.8235, 0.6697, 0.5543, 0.3809, 0.2673]
#	
#	# for bblljj ( xec pp->R->HH->bblljj ), lambda=1TeV, kL=35
#	Radion_Bulk_bblljj_LR_1TeV_kl_35 = [10.7916*9., 10.0599*9., 4.1241*9., 2.1212*9., 1.2826*9., 0.8235*9., 0.6697*9., 0.5543*9., 0.3809*9., 0.2673*9.]
#	
#	# for bblljj ( xec pp->G->HH->bblljj ), kL=35
#	KKGraviton_Bulk_bblljj_LR_3TeV_kl_35 = [0.00348859705791891, 0.0690614885863187, 0.118022211131053, 0.062398403022778, 0.0291177444067983, 0.0144132736061965, 0.010371214086094, 0.00762994497426704, 0.00414633289345529, 0.00240858873106233]
#	#######################################

	xsTh=[]
	xsTh_lam1=[]
	spin = ''
	if (resType == "HHres"):
		xsTh = [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]
		xsTh_lam1 = total_Radion_RS1
		spin = 'spin0'
	elif (resType == "HHBulkGrav"):
		xsTh = [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]
		xsTh_lam1 = total_KKGraviton_RS1
		spin = 'spin2'

	# filename for the final plot (NB: changing the name extension changes the file format)
	fileName1 = ''
	fileName2 = ''
	fileName3 = ''
	if (whichChannel == "CombMuEle"):
		fileName1 = "BR_Sigma_CombMuEle"
	if (whichChannel == "muon"):
		fileName1 = "BR_Sigma_MuMu"
	elif (whichChannel == "ele"):
		fileName1 = "BR_Sigma_Ele"
	fileName2 =  fileName1 + "_" + spin + ".pdf"
	fileName3 =  fileName1 + "_" + spin + ".png"
	fileName1 =  fileName1 + "_" + spin + ".eps"
	print ' output is ', fileName2

	# axes labels for the final plot
	title = ";M_{X} (GeV);#sigma/#sigma_{theory}"
	if (do_noBR):
		if (resType == "HHres"):
			title = '95% CL limit on #sigma(pp #rightarrow X, spin 0 '
			title +='#rightarrow HH) [pb]'   # to have a full HH in pb
			#title = ";M_{X} (GeV);#sigma (gg #rightarrow X #rightarrow HH) (fb)"
		elif (resType == "HHBulkGrav"):
			title = '95% CL limit on #sigma(pp #rightarrow X, spin 2 '
			title +='#rightarrow HH) [pb]'   # to have a full HH in pb
	elif (do_bbuujj):
		if (whichChannel == "muon"):
			title = ";M_{X} (GeV);#sigma (gg #rightarrow X #rightarrow HH) B(#rightarrow b#bar{b}ZZ #rightarrow b#bar{b}#mu#mujj) (fb)"
		elif (whichChannel == "ele"):
			title = ";M_{X} (GeV);#sigma (gg #rightarrow X #rightarrow HH) B(#rightarrow b#bar{b}ZZ #rightarrow b#bar{b}eejj) (fb)"
	else:
		title = ";M_{X} (GeV);#sigma (gg #rightarrow X #rightarrow HH) B(#rightarrow b#bar{b}ZZ #rightarrow b#bar{b}lljj) (fb)";

	# integrated luminosity
	#lint = "35.9 fb^{-1}"

	massPoints=14
	mData=[]
	x_shademasses, xsUp_expected, xsUp_observed = [],[],[]
	y_1sigma, y_1sigma_1, y_1sigma_2 = [],[],[]
	y_2sigma, y_2sigma_1, y_2sigma_2 = [],[],[]

	#---- Spin 0 case
	if (resType == "HHres"):
		if (whichChannel == "CombMuEle"):
			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
			xsUp_expected = [466.7969 , 478.5156 , 449.2188 , 216.7969 , 136.2305 , 75.9277 , 55.4199 , 57.8613 , 55.9082 , 57.6172 , 58.3496 , 59.3262 , 58.5938 , 61.0352 ]
			xsUp_observed = [699.6222 , 747.1085 , 821.7851 , 246.6537 , 103.4045 , 97.9029 , 59.8182 , 57.0078 , 33.845 , 38.1691 , 42.3573 , 30.9892 , 31.8947 , 34.1287 ]
			y_1sigma = [336.7924 , 345.2474 , 324.1098 , 154.5988 , 97.317 , 53.9613 , 39.253 , 41.3336 , 39.7336 , 40.9482 , 41.4687 , 42.2388 , 41.3597 , 43.083 , 88.2835 , 84.285 , 85.1021 , 83.7013 , 81.9616 , 79.9763 , 82.3089 , 78.6151 , 107.7061 , 193.2476 , 307.5338 , 628.2793 , 663.5319 , 647.2821 ]
			y_1sigma_1 = [336.7924 , 345.2474 , 324.1098 , 154.5988 , 97.317 , 53.9613 , 39.253 , 41.3336 , 39.7336 , 40.9482 , 41.4687 , 42.2388 , 41.3597 , 43.083 ]
			y_1sigma_2 = [647.2821 , 663.5319 , 628.2793 , 307.5338 , 193.2476 , 107.7061 , 78.6151 , 82.3089 , 79.9763 , 81.9616 , 83.7013 , 85.1021 , 84.285 , 88.2835 ]
			y_2sigma = [253.4561 , 259.819 , 243.9117 , 116.0202 , 72.3724 , 40.3366 , 29.2253 , 30.7388 , 29.7012 , 30.6091 , 30.9982 , 31.2853 , 30.6702 , 31.9481 , 123.6364 , 117.66 , 118.2338 , 115.9214 , 112.9215 , 110.5732 , 113.4 , 107.7652 , 147.6431 , 263.1764 , 416.0705 , 844.4109 , 889.2513 , 864.4575 ]
			y_2sigma_1 = [253.4561 , 259.819 , 243.9117 , 116.0202 , 72.3724 , 40.3366 , 29.2253 , 30.7388 , 29.7012 , 30.6091 , 30.9982 , 31.2853 , 30.6702 , 31.9481 ]
			y_2sigma_2 = [864.4575 , 889.2513 , 844.4109 , 416.0705 , 263.1764 , 147.6431 , 107.7652 , 113.4 , 110.5732 , 112.9215 , 115.9214 , 118.2338 , 117.66 , 123.6364 ]

		if (whichChannel == "muon"):
			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
			xsUp_expected = [575.0 , 577.0 , 563.0 , 282.0 , 180.75 , 98.875 , 72.25 , 76.25 , 74.25 , 80.0 , 84.25 , 76.0 , 73.5 , 76.5 ]
			xsUp_observed = [865.2993 , 886.8665 , 834.2917 , 357.8595 , 173.7834 , 138.3238 , 88.8182 , 107.8635 , 70.1593 , 91.6086 , 105.109 , 57.6911 , 55.4719 , 57.6818 ]
			y_1sigma = [414.8605 , 416.3035 , 406.2026 , 199.0558 , 128.0221 , 70.0314 , 51.2682 , 54.0065 , 52.411 , 56.6626 , 59.4697 , 53.6462 , 51.7044 , 53.8147 , 111.5672 , 106.6061 , 109.6263 , 123.5414 , 114.1205 , 106.806 , 108.7711 , 103.6411 , 141.44 , 257.8411 , 401.1508 , 789.6583 , 804.6947 , 801.9055 ]
			y_1sigma_1 = [414.8605 , 416.3035 , 406.2026 , 199.0558 , 128.0221 , 70.0314 , 51.2682 , 54.0065 , 52.411 , 56.6626 , 59.4697 , 53.6462 , 51.7044 , 53.8147 ]
			y_1sigma_2 = [801.9055 , 804.6947 , 789.6583 , 401.1508 , 257.8411 , 141.44 , 103.6411 , 108.7711 , 106.806 , 114.1205 , 123.5414 , 109.6263 , 106.6061 , 111.5672 ]
			y_2sigma = [312.207 , 313.293 , 305.6914 , 147.6094 , 95.3174 , 52.1411 , 37.8184 , 40.21 , 38.8652 , 42.1875 , 44.0996 , 39.7812 , 38.1855 , 39.7441 , 160.2742 , 153.1821 , 154.7062 , 174.3217 , 162.5509 , 148.634 , 151.5655 , 143.9903 , 195.5514 , 354.7256 , 549.1145 , 1067.0817 , 1075.5583 , 1075.5278 ]
			y_2sigma_1 = [312.207 , 313.293 , 305.6914 , 147.6094 , 95.3174 , 52.1411 , 37.8184 , 40.21 , 38.8652 , 42.1875 , 44.0996 , 39.7812 , 38.1855 , 39.7441 ]
			y_2sigma_2 = [1075.5278 , 1075.5583 , 1067.0817 , 549.1145 , 354.7256 , 195.5514 , 143.9903 , 151.5655 , 148.634 , 162.5509 , 174.3217 , 154.7062 , 153.1821 , 160.2742 ]

		if(whichChannel == "ele"):
			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
			xsUp_expected = [732.0 , 780.0 , 672.0 , 334.5 , 205.5 , 126.5 , 88.5 , 93.0 , 95.0 , 91.75 , 89.5 , 105.5 , 106.5 , 113.5 ]
			xsUp_observed = [1118.6326 , 1245.252 , 1317.7821 , 359.5622 , 148.9074 , 130.4379 , 79.1695 , 64.8187 , 46.7273 , 46.3474 , 51.8619 , 50.9741 , 56.0905 , 62.1694 ]
			y_1sigma = [526.3931 , 560.9106 , 481.6465 , 238.9519 , 145.0566 , 89.5977 , 62.4696 , 66.2137 , 67.0578 , 64.9849 , 63.1755 , 74.4695 , 74.9186 , 79.4167 , 166.4327 , 155.3191 , 152.1786 , 129.0993 , 131.6134 , 136.6541 , 133.4065 , 126.9514 , 181.4615 , 294.7854 , 475.8331 , 953.2552 , 1094.0205 , 1026.6962 ]
			y_1sigma_1 = [526.3931 , 560.9106 , 481.6465 , 238.9519 , 145.0566 , 89.5977 , 62.4696 , 66.2137 , 67.0578 , 64.9849 , 63.1755 , 74.4695 , 74.9186 , 79.4167 ]
			y_1sigma_2 = [1026.6962 , 1094.0205 , 953.2552 , 475.8331 , 294.7854 , 181.4615 , 126.9514 , 133.4065 , 136.6541 , 131.6134 , 129.0993 , 152.1786 , 155.3191 , 166.4327 ]
			y_2sigma = [394.5938 , 420.4688 , 359.625 , 177.7031 , 107.5664 , 66.709 , 46.3242 , 49.043 , 49.7266 , 48.3838 , 46.8477 , 55.2227 , 55.3301 , 58.9668 , 236.9371 , 219.8352 , 213.4392 , 181.0693 , 182.8527 , 190.1714 , 184.1768 , 176.3756 , 252.1075 , 406.9712 , 651.3433 , 1310.9766 , 1448.423 , 1359.2893 ]
			y_2sigma_1 = [394.5938 , 420.4688 , 359.625 , 177.7031 , 107.5664 , 66.709 , 46.3242 , 49.043 , 49.7266 , 48.3838 , 46.8477 , 55.2227 , 55.3301 , 58.9668 ]
			y_2sigma_2 = [1359.2893 , 1448.423 , 1310.9766 , 651.3433 , 406.9712 , 252.1075 , 176.3756 , 184.1768 , 190.1714 , 182.8527 , 181.0693 , 213.4392 , 219.8352 , 236.9371 ]

	#---- Spin 2 case
	if (resType == "HHBulkGrav"):
		if (whichChannel == "CombMuEle"):
			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
			xsUp_expected = [398.4375 , 398.4375 , 270.5078 , 168.9453 , 106.9336 , 69.3359 , 43.8232 , 36.7432 , 32.959 , 34.5459 , 35.5225 , 41.9922 , 47.1191 , 57.373 ]
			xsUp_observed = [563.4792 , 592.9493 , 438.8394 , 150.2542 , 97.4325 , 42.5766 , 38.8464 , 38.0121 , 25.2084 , 25.5067 , 23.3497 , 25.6571 , 22.6855 , 27.639 ]
			y_1sigma = [286.5229 , 287.4713 , 192.2481 , 120.4756 , 75.997 , 49.2766 , 31.1449 , 26.1131 , 23.5444 , 24.5515 , 25.1599 , 29.6411 , 33.2601 , 40.498 , 82.7578 , 67.967 , 60.4043 , 50.9562 , 49.4177 , 46.7535 , 52.4144 , 62.3395 , 98.9082 , 151.689 , 238.3079 , 383.7247 , 550.9036 , 549.3154 ]
			y_1sigma_1 = [286.5229 , 287.4713 , 192.2481 , 120.4756 , 75.997 , 49.2766 , 31.1449 , 26.1131 , 23.5444 , 24.5515 , 25.1599 , 29.6411 , 33.2601 , 40.498 ]
			y_1sigma_2 = [549.3154 , 550.9036 , 383.7247 , 238.3079 , 151.689 , 98.9082 , 62.3395 , 52.4144 , 46.7535 , 49.4177 , 50.9562 , 60.4043 , 67.967 , 82.7578 ]
			y_2sigma = [214.7827 , 216.3391 , 143.7073 , 90.4121 , 56.8085 , 36.8347 , 23.2811 , 19.5198 , 17.5095 , 18.3525 , 18.7325 , 21.9803 , 24.6639 , 30.0312 , 116.0726 , 95.3277 , 84.323 , 71.2401 , 68.3236 , 64.0894 , 72.1092 , 85.3333 , 136.0732 , 207.9346 , 323.3039 , 522.5796 , 728.9793 , 727.8192 ]
			y_2sigma_1 = [214.7827 , 216.3391 , 143.7073 , 90.4121 , 56.8085 , 36.8347 , 23.2811 , 19.5198 , 17.5095 , 18.3525 , 18.7325 , 21.9803 , 24.6639 , 30.0312 ]
			y_2sigma_2 = [727.8192 , 728.9793 , 522.5796 , 323.3039 , 207.9346 , 136.0732 , 85.3333 , 72.1092 , 64.0894 , 68.3236 , 71.2401 , 84.323 , 95.3277 , 116.0726 ]

		if (whichChannel == "muon"):
			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
			xsUp_expected = [506.5 , 490.0 , 318.5 , 264.5 , 166.25 , 115.5 , 57.875 , 44.625 , 44.375 , 45.125 , 47.25 , 48.375 , 58.25 , 70.5 ]
			xsUp_observed = [732.5991 , 726.5603 , 436.7411 , 325.1878 , 229.1635 , 91.725 , 76.9111 , 66.7221 , 44.3697 , 37.1242 , 49.7558 , 35.902 , 38.863 , 46.525 ]
			y_1sigma = [364.2324 , 352.3669 , 225.588 , 189.5766 , 119.1573 , 83.0579 , 41.3433 , 31.7147 , 31.537 , 31.8525 , 33.3524 , 34.1465 , 40.9001 , 49.594 , 102.8168 , 84.7193 , 69.9714 , 68.1558 , 64.7309 , 63.3012 , 63.3021 , 82.0977 , 161.9992 , 233.1806 , 370.9851 , 459.4206 , 687.2693 , 710.412 ]
			y_1sigma_1 = [364.2324 , 352.3669 , 225.588 , 189.5766 , 119.1573 , 83.0579 , 41.3433 , 31.7147 , 31.537 , 31.8525 , 33.3524 , 34.1465 , 40.9001 , 49.594 ]
			y_1sigma_2 = [710.412 , 687.2693 , 459.4206 , 370.9851 , 233.1806 , 161.9992 , 82.0977 , 63.3021 , 63.3012 , 64.7309 , 68.1558 , 69.9714 , 84.7193 , 102.8168 ]
			y_2sigma = [273.0352 , 264.1406 , 167.959 , 141.5488 , 88.9697 , 62.2617 , 30.7461 , 23.707 , 23.5742 , 23.6201 , 24.7324 , 25.3213 , 30.4902 , 36.627 , 145.9605 , 119.7342 , 98.5938 , 95.0024 , 90.498 , 87.0868 , 87.3398 , 112.9059 , 218.9128 , 312.974 , 497.9346 , 632.4321 , 909.9067 , 940.5464 ]
			y_2sigma_1 = [273.0352 , 264.1406 , 167.959 , 141.5488 , 88.9697 , 62.2617 , 30.7461 , 23.707 , 23.5742 , 23.6201 , 24.7324 , 25.3213 , 30.4902 , 36.627 ]
			y_2sigma_2 = [940.5464 , 909.9067 , 632.4321 , 497.9346 , 312.974 , 218.9128 , 112.9059 , 87.3398 , 87.0868 , 90.498 , 95.0024 , 98.5938 , 119.7342 , 145.9605 ]
		if(whichChannel == "ele"):
			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
			xsUp_expected = [576.0 , 607.0 , 513.0 , 221.5 , 139.0 , 89.25 , 70.25 , 63.625 , 53.875 , 53.625 , 56.5 , 66.875 , 84.25 , 103.5 ]
			xsUp_observed = [770.1378 , 839.411 , 914.7414 , 161.0232 , 94.5301 , 61.2045 , 52.4679 , 42.8619 , 35.5285 , 39.6365 , 28.1252 , 41.8178 , 41.555 , 51.7587 ]
			y_1sigma = [412.1367 , 435.0587 , 364.5857 , 158.2297 , 98.1161 , 62.3004 , 49.4181 , 44.9111 , 38.0288 , 37.8524 , 39.5334 , 47.0439 , 59.0634 , 72.167 , 152.1815 , 123.5414 , 97.5302 , 82.3993 , 77.3514 , 77.712 , 91.5223 , 101.8922 , 129.806 , 200.5007 , 314.2054 , 731.7979 , 856.2114 , 812.4839 ]
			y_1sigma_1 = [412.1367 , 435.0587 , 364.5857 , 158.2297 , 98.1161 , 62.3004 , 49.4181 , 44.9111 , 38.0288 , 37.8524 , 39.5334 , 47.0439 , 59.0634 , 72.167 ]
			y_1sigma_2 = [812.4839 , 856.2114 , 731.7979 , 314.2054 , 200.5007 , 129.806 , 101.8922 , 91.5223 , 77.712 , 77.3514 , 82.3993 , 97.5302 , 123.5414 , 152.1815 ]
			y_2sigma = [310.5 , 324.8398 , 272.5312 , 117.6719 , 72.7578 , 44.4507 , 36.4971 , 33.3037 , 28.2002 , 28.0693 , 29.3535 , 34.7437 , 43.4414 , 53.3672 , 218.8511 , 176.9125 , 138.042 , 116.6262 , 108.4898 , 108.3229 , 127.7631 , 143.3537 , 182.9023 , 279.478 , 427.904 , 993.8329 , 1161.5917 , 1094.932 ]
			y_2sigma_1 = [310.5 , 324.8398 , 272.5312 , 117.6719 , 72.7578 , 44.4507 , 36.4971 , 33.3037 , 28.2002 , 28.0693 , 29.3535 , 34.7437 , 43.4414 , 53.3672 ]
			y_2sigma_2 = [1094.932 , 1161.5917 , 993.8329 , 427.904 , 279.478 , 182.9023 , 143.3537 , 127.7631 , 108.3229 , 108.4898 , 116.6262 , 138.042 , 176.9125 , 218.8511 ]
	#------------------

	if (do_noBR):
		#for i in range(len(mTh)):
			#xsTh[i] *= 0.001/(0.0043075917)
			#xsTh_lam1[i] *= 0.001/(0.0043075917)
		for i in range(len(mData)):
			xsUp_expected[i] *= 0.001/(0.0043075917)
			xsUp_observed[i] *= 0.001/(0.0043075917)
			y_1sigma_1[i] *= 0.001/(0.0043075917)
			y_1sigma_2[i] *= 0.001/(0.0043075917)
			y_2sigma_1[i] *= 0.001/(0.0043075917)
			y_2sigma_2[i] *= 0.001/(0.0043075917)
		for i in range(2*len(mData)):
			y_1sigma[i] *= 0.001/(0.0043075917)
			y_2sigma[i] *= 0.001/(0.0043075917)
#	elif (do_bbuujj):
#		#--- AH: for bbuujj I have to scale the values of r with 0.333300327
#		for i in range(len(mTh)):
#			xsTh[i] *= 0.333300327
#			xsTh_lam1[i] *= 0.333300327
#		for i in range(len(mData)):
#			xsUp_expected[i] *= 0.333300327
#			xsUp_observed[i] *= 0.333300327
#			y_1sigma_1[i] *= 0.333300327
#			y_1sigma_2[i] *= 0.333300327
#			y_2sigma_1[i] *= 0.333300327
#			y_2sigma_2[i] *= 0.333300327
#		for i in range(2*len(mData)):
#			y_1sigma[i] *= 0.333300327
#			y_2sigma[i] *= 0.333300327

	#turn on/off batch mode
	gROOT.SetBatch(kTRUE)
	#set ROOT style
	setTDRStyle()
	gStyle.SetPadLeftMargin(0.14)
	gROOT.ForceStyle()

	c = TCanvas("c","",800,800)
	c.SetRightMargin(0.06)
	c.SetLeftMargin(0.2)
	c.cd()
	plotLow=0.07
	plotHigh=2000
	if (do_noBR):
		if (resType == "HHres"):
			plotLow=0.2; plotHigh=1400
		if (resType == "HHBulkGrav"):
			plotLow=0.2; plotHigh=1400
	else:
		plotLow=0.07; plotHigh=50000;
	
	bg = TH2F("bg","", 1, 240, 1050, 1, plotLow, plotHigh)
	#bg.GetXaxis().CenterTitle()
	#bg.GetYaxis().CenterTitle()
	if (resType == "HHres"): bg.GetXaxis().SetTitle('m_{X, spin 0} [GeV]')
	elif (resType == "HHBulkGrav"): bg.GetXaxis().SetTitle('m_{X, spin 2} [GeV]')
	bg.GetYaxis().SetTitle(title)
	bg.GetYaxis().CenterTitle()

	bg.GetYaxis().SetLabelSize(0.035)
	bg.GetXaxis().SetLabelSize(0.03)
	bg.SetTitleSize(0.03, "Y")
	bg.SetTitleSize(0.04, "X")
	bg.SetTitleOffset(2.45, "Y")
	bg.SetStats(kFALSE)
	#bg.SetTitleOffset(1.,"X")
	#bg.SetTitleOffset(1.15,"Y")
	bg.Draw()

	xsTh_vs_m = TGraph(nTH, array("d",mTh), array("d",xsTh))
	xsTh_vs_m.SetLineWidth(2)
#	xsTh_vs_m.SetLineColor(kBlue)
	xsTh_vs_m.SetLineColor(2)
#	xsTh_vs_m.SetLineStyle(8)
#	xsTh_vs_m.SetFillColor(kCyan-6)
#	xsTh_vs_m.SetMarkerSize(0.00001)
#	xsTh_vs_m.SetMarkerStyle(22)
#	xsTh_vs_m.SetMarkerColor(kBlue)

	xsTh_lam1_vs_m = TGraph(nTH, array("d",mTh), array("d",xsTh_lam1))
	xsTh_lam1_vs_m.SetLineWidth(2)
	#xsTh_lam1_vs_m.SetLineColor(kBlue)
	xsTh_lam1_vs_m.SetLineColor(2)
#	xsTh_lam1_vs_m.SetFillColor(kCyan-6)
#	xsTh_lam1_vs_m.SetMarkerSize(0.00001)
#	xsTh_lam1_vs_m.SetMarkerStyle(22)
#	xsTh_lam1_vs_m.SetMarkerColor(kBlue)

		
	xsData_vs_m_expected = TGraph(massPoints, array("d",mData), array("d",xsUp_expected))
	xsData_vs_m_expected.SetMarkerStyle(0)
	xsData_vs_m_expected.SetMarkerColor(kBlack)
	xsData_vs_m_expected.SetLineColor(kBlack)
	xsData_vs_m_expected.SetLineWidth(2)
	xsData_vs_m_expected.SetLineStyle(7)
	xsData_vs_m_expected.SetMarkerSize(0.001)

	xsData_vs_m_observed = TGraph(massPoints, array("d",mData), array("d",xsUp_observed))
	xsData_vs_m_observed.SetMarkerStyle(21)
	xsData_vs_m_observed.SetMarkerColor(kBlack)
	xsData_vs_m_observed.SetLineColor(kBlack)
	xsData_vs_m_observed.SetLineWidth(2)
	xsData_vs_m_observed.SetLineStyle(1)
	xsData_vs_m_observed.SetMarkerSize(1)

#	xsUp_observed_logY, xsUp_expected_logY = [0 for i in range(len(mData))], [0 for i in range(len(mData))]
#	xsTh_logY = [0 for i in range(len(mTh))]
#	for ii in range(len(mData)): xsUp_observed_logY[ii] = math.log10(xsUp_observed[ii])
#	for ii in range(len(mData)): xsUp_expected_logY[ii] = math.log10(xsUp_expected[ii])
#	for ii in range(len(mTh)): xsTh_logY[ii] = math.log10(xsTh[ii])
#	xsTh_vs_m_log = TGraph(nTH, array("d",mTh), array("d",xsTh_logY))
#	xsData_vs_m_expected_log = TGraph(massPoints, array("d",mData), array("d",xsUp_expected_logY))
#	xsData_vs_m_observed_log = TGraph(massPoints, array("d",mData), array("d",xsUp_observed_logY))

	exshade1 = TGraph(2*massPoints,array("d",x_shademasses),array("d",y_1sigma))
	exshade1.SetFillColor(kGreen)
	exshade2 = TGraph(2*massPoints,array("d",x_shademasses),array("d",y_2sigma))
	exshade2.SetFillColor(kYellow);
	exshade2.Draw("f")
	exshade1.Draw("f")
	gPad.RedrawAxis()


	if (resType == "HHres") :
		xsTh_lam1_vs_m.Draw("C")
		#particleTypeFullName = "Bulk Radion"
		particleTypeFullName = "RS1 Radion"
	else:
		xsTh_lam1_vs_m.Draw("C")
		#particleTypeFullName = "Bulk Graviton"
		particleTypeFullName = "RS1 KK graviton"
	xsData_vs_m_expected.Draw("LP")
	if (_obs_limit):
		xsData_vs_m_observed.Draw("LP")
	#grshade.SetFillStyle(1001)

	legend = TLegend(.3875,.6,.91,.87);
	legend.SetBorderSize(1);
	legend.SetFillColor(0);
	#legend.SetFillStyle(0);
	legend.SetTextSize(.036);
	legend.SetTextFont(42);
	legend.SetMargin(0.15);

	legend = TLegend(.60, .70, .90, .90)
	if _obs_limit:
		legend.AddEntry(xsData_vs_m_observed , "Observed", "lp")
	legend.AddEntry(xsData_vs_m_expected, "Median expected", "l")
	legend.AddEntry(exshade1, "68 % expected", "f")
	legend.AddEntry(exshade2, "95 % expected", "f")

	legend.AddEntry(xsTh_vs_m, particleTypeFullName, "l")
	legend.SetShadowColor(0)
	legend.SetFillColor(0)
	legend.SetLineColor(0)

#	if (do_noBR):
#		legend.SetHeader("gg #rightarrow HH ")
#		if (resType == "HHres"):
#			legend.AddEntry(xsTh_lam1_vs_m,"#sigma_{theory} (#lambda_{R}= 1 TeV)","lf")
#			legend.AddEntry(xsTh_vs_m     ,"#sigma_{theory} (#lambda_{R}= 3 TeV)","lf")
#
#		else:
#			legend.AddEntry(xsTh_vs_m     ,"#sigma_{theory} (#Kappa= 0.1)","lf")
#	elif (do_bbuujj):
#		if (whichChannel == "muon"):
#			legend.SetHeader("gg #rightarrow HH #rightarrow b#bar{b}#mu#mujj")
#			legend.AddEntry(xsTh_lam1_vs_m,"#sigma_{theory} #times BR (#lambda_{R}= 1 TeV)","lf")
#			legend.AddEntry(xsTh_vs_m     ,"#sigma_{theory} #times BR (#lambda_{R}= 3 TeV)","lf")
#
#		elif (whichChannel == "ele"):
#			legend.SetHeader("gg #rightarrow HH #rightarrow b#bar{b}eejj")
#			legend.AddEntry(xsTh_lam1_vs_m,"#sigma_{theory} #times BR (#lambda_{R}= 1 TeV)","lf")
#			legend.AddEntry(xsTh_vs_m     ,"#sigma_{theory} #times BR (#lambda_{R}= 3 TeV)","lf")
#	else:
#		legend.SetHeader("gg #rightarrow HH #rightarrow b#bar{b}lljj")
#		legend.AddEntry(xsTh_lam1_vs_m,"#sigma_{theory} #times BR (#lambda_{R}= 1 TeV)","lf")
#		legend.AddEntry(xsTh_vs_m     ,"#sigma_{theory} #times BR (#lambda_{R}= 3 TeV)","lf")
#
#	legend.AddEntry(xsData_vs_m_expected, "Expected 95% CL upper limit","lp")
#	legend.AddEntry(xsData_vs_m_observed, "Observed 95% CL upper limit","lp")
	legend.Draw()

	l1 = TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.04)
	#l1.DrawLatex(0.14,0.93,"CMS #it{Preliminary}                              35.9 fb^{-1} (13 TeV)")
	#// l1.DrawLatex(0.14,0.93,"CMS Work In Progress      #sqrt{s} = 8 TeV         19.6 fb^{-1}");
	#// l1.DrawLatex(0.76,0.53,"Preliminary");
	#// l1.DrawLatex(0.76,0.48,"#sqrt{s} = 8 TeV");
	#// l1.DrawLatex(0.76,0.43,"19.6 fb^{-1}");

	latex2 = TLatex()
	latex2.SetNDC()
	latex2.SetTextSize(0.5 * c.GetTopMargin())
	latex2.SetTextFont(42)
	latex2.SetTextAlign(11)
	latex2.DrawLatex(0.2, 0.95, "#bf{CMS} #it{preliminary}")
	latex2.DrawLatex(0.7, 0.95, "35.9 fb^{-1} (13 TeV)")

	c.SetGridx()
	c.SetGridy()
	c.RedrawAxis()
	legend.Draw()
	c.SetLogy()
	#c.SaveAs(fileName1)
	c.SaveAs(fileName2)
	#c.SaveAs(fileName3)

	del xsTh_vs_m
	del bg
	del c



def setTDRStyle():
	tdrStyle = TStyle("tdrStyle","Style for P-TDR")
	# For the canvas:
	tdrStyle.SetCanvasBorderMode(0)
	tdrStyle.SetCanvasColor(kWhite)
	tdrStyle.SetCanvasDefH(600) #//Height of canvas
	tdrStyle.SetCanvasDefW(600) #//Width of canvas
	tdrStyle.SetCanvasDefX(0)   #//POsition on screen
	tdrStyle.SetCanvasDefY(0)

	# For the Pad:
	tdrStyle.SetPadBorderMode(0)
	# tdrStyle.SetPadBorderSize(Width_t size = 1)
	tdrStyle.SetPadColor(kWhite)
	tdrStyle.SetPadGridX(False)
	tdrStyle.SetPadGridY(False)
	tdrStyle.SetGridColor(0)
	tdrStyle.SetGridStyle(3)
	tdrStyle.SetGridWidth(1)

	# For the frame:
	tdrStyle.SetFrameBorderMode(0)
	tdrStyle.SetFrameBorderSize(1)
	tdrStyle.SetFrameFillColor(0)
	tdrStyle.SetFrameFillStyle(0)
	tdrStyle.SetFrameLineColor(1)
	tdrStyle.SetFrameLineStyle(1)
	tdrStyle.SetFrameLineWidth(1)

	# For the histo:
	tdrStyle.SetHistFillColor(63)
	# tdrStyle.SetHistFillStyle(0)
	tdrStyle.SetHistLineColor(1)
	tdrStyle.SetHistLineStyle(0)
	tdrStyle.SetHistLineWidth(1)


	tdrStyle.SetMarkerStyle(20)

	#For the fit/function :
	tdrStyle.SetOptFit(1)
	tdrStyle.SetFitFormat("5.4g")
	tdrStyle.SetFuncColor(2)
	tdrStyle.SetFuncStyle(1)
	tdrStyle.SetFuncWidth(1)

	#For the date:
	tdrStyle.SetOptDate(0)

	#For the statistics box:
	tdrStyle.SetOptFile(0)
	tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
	tdrStyle.SetStatColor(kWhite)
	tdrStyle.SetStatFont(42)
	tdrStyle.SetStatFontSize(0.025)
	tdrStyle.SetStatTextColor(1)
	tdrStyle.SetStatFormat("6.4g")
	tdrStyle.SetStatBorderSize(1)
	tdrStyle.SetStatH(0.1)
	tdrStyle.SetStatW(0.15)


	# Margins:
	tdrStyle.SetPadTopMargin(0.07)
	tdrStyle.SetPadBottomMargin(0.13)
	tdrStyle.SetPadLeftMargin(0.13)
	tdrStyle.SetPadRightMargin(0.05)

	# For the Global title:

	#  tdrStyle.SetOptTitle(0)
	tdrStyle.SetTitleFont(42)
	tdrStyle.SetTitleColor(1)
	tdrStyle.SetTitleTextColor(1)
	tdrStyle.SetTitleFillColor(10)
	tdrStyle.SetTitleFontSize(0.05)

	# For the axis titles:

	tdrStyle.SetTitleColor(1, "XYZ")
	tdrStyle.SetTitleFont(42, "XYZ")
	#tdrStyle.SetTitleSize(0.06, "XYZ")
	tdrStyle.SetTitleSize(0.048, "XYZ")
	tdrStyle.SetTitleXOffset(0.9)
	tdrStyle.SetTitleYOffset(1.05)

	# For the axis labels:

	tdrStyle.SetLabelColor(1, "XYZ")
	tdrStyle.SetLabelFont(42, "XYZ")
	tdrStyle.SetLabelOffset(0.007, "XYZ")
	tdrStyle.SetLabelSize(0.04, "XYZ")

	# For the axis:

	tdrStyle.SetAxisColor(1, "XYZ")
	tdrStyle.SetStripDecimals(kTRUE)
	tdrStyle.SetTickLength(0.03, "XYZ")
	tdrStyle.SetNdivisions(510, "XYZ")
	tdrStyle.SetPadTickX(1) # To get tick marks on the opposite side of the frame
	tdrStyle.SetPadTickY(1)

	# Change for log plots:
	tdrStyle.SetOptLogx(0)
	tdrStyle.SetOptLogy(0)
	tdrStyle.SetOptLogz(0)

	tdrStyle.cd()



if __name__ == "__main__":
	main()