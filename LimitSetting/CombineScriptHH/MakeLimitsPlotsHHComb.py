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
	#	python MakeLimitsPlotsComb.py --channel CombMuEle  --resType HHres --obslimit 1
	#	python MakeLimitsPlotsComb.py --channel CombMuEle  --resType HHBulkGrav --obslimit 1
	#
	###----------------------------------------------------------###
	###----------------------------------------------------------###
	
	whichChannel = ''
	resType = ''
	_obs_limit = 0
	draw_2l2j_limits = 1
	drawRegionSeparator = 1
	
	for x in range(len(sys.argv)):
		if sys.argv[x] == '--channel':
			whichChannel = sys.argv[x+1]
		if sys.argv[x] == '--resType':
			resType = sys.argv[x+1]
		if sys.argv[x] == '--obslimit':
			_obs_limit = int(sys.argv[x+1])
	print ' whichChannel ', whichChannel, ' resType ', resType, ' _obs_limit ', _obs_limit

	do_gg_hh_bbzz = 1
	do_noBR = 1
	if do_noBR : do_gg_hh_bbzz = 0
	##-------------------------------------------------------------##
	##-------------------------------------------------------------##

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
	
	#----- hard coded combined 2l2nu+2l2j limit at point M = 451
	# spin0
	sp0_M451_observed  = 711.8570
	sp0_M451_2sigma_dn = 283.8867
	sp0_M451_1sigma_dn = 379.7768
	sp0_M451_expected  = 534.3750
	sp0_M451_1sigma_up = 758.0294
	sp0_M451_2sigma_up = 1039.1034
	# spin2
	sp2_M451_observed  = 292.4820
	sp2_M451_2sigma_dn = 248.1934
	sp2_M451_1sigma_dn = 332.0270
	sp2_M451_expected  = 467.1875
	sp2_M451_1sigma_up = 666.4460
	sp2_M451_2sigma_up = 916.8650
	#-----

	
	xsTh=[]
	xsTh_lam1=[]
	spin = ''
	if (resType == "HHres"):
		xsTh = [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]
		xsTh_lam1 = total_Radion_RS1
		spin = 'spin0'
	elif (resType == "HHBulkGrav"):
		xsTh = [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]
		xsTh_lam1 = total_KKGraviton_RS1
		spin = 'spin2'

	# 2l2j limits
	mass_2l2j = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
	exp_2l2j_limits_sp0 = [466.7969 , 478.5156 , 449.2188 , 216.7969 , 136.2305 , 75.9277 , 55.4199 , 57.8613 , 55.9082 , 57.6172 , 58.3496 , 59.3262 , 58.5938 , 61.0352 ]
	#obs_2l2j_limits_sp0 = [699.6222 , 747.1085 , 821.7851 , 246.6537 , 103.4045 , 97.9029 , 59.8182 , 57.0078 , 33.845 , 38.1691 , 42.3573 , 30.9892 , 31.8947 , 34.1287 ]
	exp_2l2j_limits_sp2 = [398.4375 , 398.4375 , 270.5078 , 168.9453 , 106.9336 , 69.3359 , 43.8232 , 36.7432 , 32.959 , 34.5459 , 35.5225 , 41.9922 , 47.1191 , 57.373 ]
	#obs_2l2j_limits_sp2 = [563.4792 , 592.9493 , 438.8394 , 150.2542 , 97.4325 , 42.5766 , 38.8464 , 38.0121 , 25.2084 , 25.5067 , 23.3497 , 25.6571 , 22.6855 , 27.639 ]
	
	# 2l2nu limits
	# from https://github.com/RemKamal/Notebooks_SWAN/blob/master/table%20LIMITS%20dataframe%20from%20json.ipynb
	mass_2l2nu = [260.0, 270.0, 300.0, 350.0, 400.0, 450.0, 451.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 800.0, 900.0, 1000.0]
	exp_2l2nu_limits_sp0 = [410.9375, 470.3125, 496.875, 496.875, 171.09375, 82.03125, 92.1875, 54.375, 28.515625, 19.609375, 17.1875, 12.03125, 10.3515625, 9.8046875, 5.60546875, 4.53125]
	exp_2l2nu_limits_sp2 = [585.9375, 537.5, 434.375, 309.375, 119.921875, 63.28124999999999, 62.109375, 36.5625, 20.234375, 12.6953125, 11.09375, 10.078125, 8.828125, 6.54296875, 4.8046875, 4.23828125]

	if (resType == "HHres"):
		exp_2l2j_limits = exp_2l2j_limits_sp0
		exp_2l2nu_limits = exp_2l2nu_limits_sp0
	if (resType == "HHBulkGrav"):
		exp_2l2j_limits = exp_2l2j_limits_sp2
		exp_2l2nu_limits = exp_2l2nu_limits_sp2

	for i in range(len(exp_2l2j_limits)):
		exp_2l2j_limits[i] *= 0.001/(0.0043075917)


	# filename for the final plot (NB: changing the name extension changes the file format)
	fileName1 = ''
	fileName2 = ''
	fileName3 = ''
	extenFname = ''
	if do_noBR:
		extenFname = 'noBR_'
	if (whichChannel == "CombMuEle"): fileName1 = "BR_Sigma_CombMuEle"
	if (whichChannel == "muon"): fileName1 = "BR_Sigma_MuMu"
	elif (whichChannel == "ele"): fileName1 = "BR_Sigma_Ele"

	fileName2 =  fileName1 + "_" + extenFname + spin + ".pdf"
	fileName3 =  fileName1 + "_" + extenFname + spin + ".png"
	fileName1 =  fileName1 + "_" + extenFname + spin + ".eps"
	print ' output is ', fileName2

	# axes labels for the final plot
	title = ";M_{X} (GeV);#sigma (gg #rightarrow X #rightarrow HH) B(#rightarrow b#bar{b}ZZ) (fb)";
	if (do_noBR):
		if (resType == "HHres"):
			title = '95% CL limit on #sigma(pp #rightarrow X, spin 0 '
			title +='#rightarrow HH) [pb]'   # to have a full HH in pb
			#title = ";M_{X} (GeV);#sigma (gg #rightarrow X #rightarrow HH) (fb)"
		elif (resType == "HHBulkGrav"):
			title = '95% CL limit on #sigma(pp #rightarrow X, spin 2 '
			title +='#rightarrow HH) [pb]'   # to have a full HH in pb


	# integrated luminosity
	#lint = "35.9 fb^{-1}"

	mData=[]
	x_shademasses, xsUp_expected, xsUp_observed = [],[],[]
	y_1sigma, y_1sigma_1, y_1sigma_2 = [],[],[]
	y_2sigma, y_2sigma_1, y_2sigma_2 = [],[],[]

	#---- Spin 0 case
	if (resType == "HHres"):
		if (whichChannel == "CombMuEle"):
			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 451.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 451.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 451.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
			xsUp_expected = [99.2188 , 102.3438 , 98.9062 , 49.2188 , 30.3906 , 17.0312 , 17.5 , 12.5 , 11.4375 , 10.0625 , 9.675 , 6.8438 , 7.2188 , 4.3945 , 3.8594 ]
			xsUp_observed = [102.193 , 116.6816 , 163.8842 , 53.7682 , 21.4662 , 22.3192 , 23.3065 , 10.9533 , 8.6848 , 5.2512 , 9.8153 , 8.3440 , 6.8539 , 4.3675 , 3.9542 ]
			y_1sigma = [71.8222 , 74.0843 , 71.1251 , 35.2168 , 21.7097 , 12.104 , 12.4371 , 8.8535 , 8.101 , 7.0408 , 6.6043 , 5.3400 , 4.8633 , 2.736 , 2.3539 , 6.5361 , 7.2323 , 10.9882 , 12.7907 , 14.4185 , 14.5949 , 16.3613 , 17.8313 , 24.8941 , 24.2952 , 43.1101 , 69.4261 , 138.3307 , 141.9146 , 137.9768 ]
			y_1sigma_1 = [71.8222 , 74.0843 , 71.1251 , 35.2168 , 21.7097 , 12.104 , 12.4371 , 8.8535 , 8.101 , 7.0408 , 6.6043 , 5.3400 , 4.8633 , 2.736 , 2.3539 ]
			y_1sigma_2 = [137.9768 , 141.9146 , 138.3307 , 69.4261 , 43.1101 , 24.2952 , 24.8941 , 17.8313 , 16.3613 , 14.5949 , 14.4185 , 12.7907 , 10.9882 , 7.2323 , 6.5361 ]
			y_2sigma = [54.2603 , 55.9692 , 53.3167 , 26.532 , 16.145 , 9.0479 , 9.2969 , 6.5918 , 6.0315 , 5.2278 , 4.7619 , 4.2773 , 3.4966 , 1.8368 , 1.5377 , 10.5577 , 11.4951 , 16.2556 , 19.3697 , 20.6888 , 20.4087 , 22.6207 , 24.5315 , 34.0763 , 33.4242 , 59.0952 , 94.188 , 187.1862 , 189.5296 , 184.6663 ]
			y_2sigma_1 = [54.2603 , 55.9692 , 53.3167 , 26.532 , 16.145 , 9.0479 , 9.2969 , 6.5918 , 6.0315 , 5.2278 , 4.7619 , 4.2773 , 3.4966 , 1.8368 , 1.5377 ]
			y_2sigma_2 = [184.6663 , 189.5296 , 187.1862 , 94.188 , 59.0952 , 33.4242 , 34.0763 , 24.5315 , 22.6207 , 20.4087 , 20.6888 , 19.3697 , 16.2556 , 11.4951 , 10.5577 ]
	
#		if (whichChannel == "muon"):
#			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
#			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
#			xsUp_expected = [3225.0 , 3312.5 , 2906.25 , 1532.8125 , 953.125 , 535.9375 , 389.0625 , 387.5 , 362.5 , 367.5 , 316.875 , 326.25 , 241.875 , 216.75 ]
#			xsUp_observed = [4161.4975 , 4552.2726 , 5396.2357 , 1672.1335 , 684.6016 , 712.4785 , 372.9915 , 324.4364 , 192.7585 , 355.9412 , 349.6616 , 277.8588 , 209.949 , 198.6466 ]
#			y_1sigma = [2326.8264 , 2389.9575 , 2065.4526 , 1098.6217 , 680.8701 , 380.8872 , 276.5042 , 275.3937 , 256.7524 , 258.5218 , 217.0779 , 227.4829 , 156.3758 , 137.0166 , 349.8021 , 379.7448 , 477.1018 , 468.4443 , 530.1006 , 517.1086 , 549.6821 , 555.0002 , 764.5184 , 1355.8398 , 2174.3474 , 4157.3691 , 4593.2656 , 4471.9341 ]
#			y_1sigma_1 = [2326.8264 , 2389.9575 , 2065.4526 , 1098.6217 , 680.8701 , 380.8872 , 276.5042 , 275.3937 , 256.7524 , 258.5218 , 217.0779 , 227.4829 , 156.3758 , 137.0166 ]
#			y_1sigma_2 = [4471.9341 , 4593.2656 , 4157.3691 , 2174.3474 , 1355.8398 , 764.5184 , 555.0002 , 549.6821 , 517.1086 , 530.1006 , 468.4443 , 477.1018 , 379.7448 , 349.8021 ]
#			y_2sigma = [1751.0742 , 1798.584 , 1543.9453 , 820.2942 , 506.3477 , 284.7168 , 206.6895 , 205.8594 , 191.1621 , 190.9277 , 157.1997 , 168.2227 , 106.7651 , 92.2881 , 535.8672 , 571.5226 , 676.253 , 667.6553 , 738.9077 , 715.9855 , 755.9575 , 763.5431 , 1045.0289 , 1855.9388 , 2951.4448 , 5711.313 , 6155.7974 , 5993.1914 ]
#			y_2sigma_1 = [1751.0742 , 1798.584 , 1543.9453 , 820.2942 , 506.3477 , 284.7168 , 206.6895 , 205.8594 , 191.1621 , 190.9277 , 157.1997 , 168.2227 , 106.7651 , 92.2881 ]
#			y_2sigma_2 = [5993.1914 , 6155.7974 , 5711.313 , 2951.4448 , 1855.9388 , 1045.0289 , 763.5431 , 755.9575 , 715.9855 , 738.9077 , 667.6553 , 676.253 , 571.5226 , 535.8672 ]
#		if(whichChannel == "ele"):
#			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
#			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
#			xsUp_expected = [3225.0 , 3312.5 , 2906.25 , 1532.8125 , 953.125 , 535.9375 , 389.0625 , 387.5 , 362.5 , 367.5 , 316.875 , 326.25 , 241.875 , 216.75 ]
#			xsUp_observed = [4161.4975 , 4552.2726 , 5396.2357 , 1672.1335 , 684.6016 , 712.4785 , 372.9915 , 324.4364 , 192.7585 , 355.9412 , 349.6616 , 277.8588 , 209.949 , 198.6466 ]
#			y_1sigma = [2326.8264 , 2389.9575 , 2065.4526 , 1098.6217 , 680.8701 , 380.8872 , 276.5042 , 275.3937 , 256.7524 , 258.5218 , 217.0779 , 227.4829 , 156.3758 , 137.0166 , 349.8021 , 379.7448 , 477.1018 , 468.4443 , 530.1006 , 517.1086 , 549.6821 , 555.0002 , 764.5184 , 1355.8398 , 2174.3474 , 4157.3691 , 4593.2656 , 4471.9341 ]
#			y_1sigma_1 = [2326.8264 , 2389.9575 , 2065.4526 , 1098.6217 , 680.8701 , 380.8872 , 276.5042 , 275.3937 , 256.7524 , 258.5218 , 217.0779 , 227.4829 , 156.3758 , 137.0166 ]
#			y_1sigma_2 = [4471.9341 , 4593.2656 , 4157.3691 , 2174.3474 , 1355.8398 , 764.5184 , 555.0002 , 549.6821 , 517.1086 , 530.1006 , 468.4443 , 477.1018 , 379.7448 , 349.8021 ]
#			y_2sigma = [1751.0742 , 1798.584 , 1543.9453 , 820.2942 , 506.3477 , 284.7168 , 206.6895 , 205.8594 , 191.1621 , 190.9277 , 157.1997 , 168.2227 , 106.7651 , 92.2881 , 535.8672 , 571.5226 , 676.253 , 667.6553 , 738.9077 , 715.9855 , 755.9575 , 763.5431 , 1045.0289 , 1855.9388 , 2951.4448 , 5711.313 , 6155.7974 , 5993.1914 ]
#			y_2sigma_1 = [1751.0742 , 1798.584 , 1543.9453 , 820.2942 , 506.3477 , 284.7168 , 206.6895 , 205.8594 , 191.1621 , 190.9277 , 157.1997 , 168.2227 , 106.7651 , 92.2881 ]
#			y_2sigma_2 = [5993.1914 , 6155.7974 , 5711.313 , 2951.4448 , 1855.9388 , 1045.0289 , 763.5431 , 755.9575 , 715.9855 , 738.9077 , 667.6553 , 676.253 , 571.5226 , 535.8672 ]

	#---- Spin 2 case
	if (resType == "HHBulkGrav"):
		if (whichChannel == "CombMuEle"):
			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 451.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 451.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 451.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
			xsUp_expected = [88.6719 , 88.6719 , 62.1094 , 37.9688 , 23.2812 , 15.0391 , 15.3125 , 9.2578 , 7.2363 , 5.9688 , 5.8438 , 5.3906 , 4.7109 , 3.7598 , 3.4844 ]
			xsUp_observed = [107.985 , 117.1266 , 87.9631 , 31.7733 , 18.7248 , 9.4914 , 9.6063 , 6.9162 , 6.0954 , 3.9206 , 6.5643 , 5.6456 , 4.8606 , 4.2448 , 3.8187 ]
			y_1sigma = [63.9765 , 63.9765 , 44.3682 , 27.0757 , 16.6311 , 10.6519 , 10.8825 , 6.5795 , 5.1254 , 4.1988 , 4.0604 , 3.685 , 3.1505 , 2.4426 , 2.2462 , 5.6233 , 6.0078 , 7.1896 , 8.055 , 8.5691 , 8.6334 , 10.3804 , 13.2063 , 21.8434 , 21.4533 , 32.9325 , 53.2546 , 87.6091 , 122.9565 , 122.9565 ]
			y_1sigma_1 = [63.9765 , 63.9765 , 44.3682 , 27.0757 , 16.6311 , 10.6519 , 10.8825 , 6.5795 , 5.1254 , 4.1988 , 4.0604 , 3.685 , 3.1505 , 2.4426 , 2.2462 ]
			y_1sigma_2 = [122.9565 , 122.9565 , 87.6091 , 53.2546 , 32.9325 , 21.4533 , 21.8434 , 13.2063 , 10.3804 , 8.6334 , 8.5691 , 8.055 , 7.1896 , 6.0078 , 5.6233 ]
			y_2sigma = [48.1461 , 48.1461 , 32.9956 , 20.3192 , 12.3682 , 7.9308 , 8.1348 , 4.9182 , 3.816 , 3.101 , 2.9904 , 2.6953 , 2.2451 , 1.7036 , 1.5516 , 8.9251 , 9.2713 , 10.6181 , 11.6699 , 12.1272 , 12.0907 , 14.3762 , 18.1686 , 30.0511 , 29.5145 , 44.9124 , 71.964 , 119.2518 , 162.4918 , 162.4918 ]
			y_2sigma_1 = [48.1461 , 48.1461 , 32.9956 , 20.3192 , 12.3682 , 7.9308 , 8.1348 , 4.9182 , 3.816 , 3.101 , 2.9904 , 2.6953 , 2.2451 , 1.7036 , 1.5516 ]
			y_2sigma_2 = [162.4918 , 162.4918 , 119.2518 , 71.964 , 44.9124 , 29.5145 , 30.0511 , 18.1686 , 14.3762 , 12.0907 , 12.1272 , 11.6699 , 10.6181 , 9.2713 , 8.9251 ]

#		if (whichChannel == "muon"):
#			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
#			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
#			xsUp_expected = [2762.5 , 2762.5 , 1898.4375 , 1175.0 , 734.375 , 481.25 , 292.9688 , 241.25 , 220.3125 , 210.9375 , 216.4062 , 207.1875 , 200.625 , 200.0 ]
#			xsUp_observed = [3632.1524 , 3881.6039 , 2996.0379 , 1047.4742 , 635.5291 , 303.6533 , 247.01 , 220.1627 , 152.8329 , 231.9272 , 213.172 , 209.2948 , 193.2141 , 183.6267 ]
#			y_1sigma = [1986.5586 , 1993.1343 , 1360.6782 , 844.9615 , 521.9154 , 340.8609 , 208.2109 , 171.4548 , 156.0435 , 149.9119 , 151.7116 , 143.4531 , 135.1623 , 131.9336 , 311.6092 , 305.3857 , 302.9871 , 313.8806 , 300.9037 , 313.399 , 344.1447 , 416.7541 , 686.5063 , 1041.7363 , 1657.4109 , 2692.999 , 3819.5986 , 3808.5872 ]
#			y_1sigma_1 = [1986.5586 , 1993.1343 , 1360.6782 , 844.9615 , 521.9154 , 340.8609 , 208.2109 , 171.4548 , 156.0435 , 149.9119 , 151.7116 , 143.4531 , 135.1623 , 131.9336 ]
#			y_1sigma_2 = [3808.5872 , 3819.5986 , 2692.999 , 1657.4109 , 1041.7363 , 686.5063 , 416.7541 , 344.1447 , 313.399 , 300.9037 , 313.8806 , 302.9871 , 305.3857 , 311.6092 ]
#			y_2sigma = [1489.1602 , 1499.9512 , 1015.9607 , 633.3984 , 390.1367 , 253.7842 , 155.6396 , 128.1641 , 116.1804 , 112.0605 , 111.5845 , 105.2124 , 97.1777 , 93.75 , 469.1575 , 448.2071 , 432.0145 , 441.6033 , 419.2899 , 431.7812 , 473.458 , 570.473 , 944.4629 , 1418.6998 , 2248.5508 , 3679.5205 , 5054.2568 , 5046.2134 ]
#			y_2sigma_1 = [1489.1602 , 1499.9512 , 1015.9607 , 633.3984 , 390.1367 , 253.7842 , 155.6396 , 128.1641 , 116.1804 , 112.0605 , 111.5845 , 105.2124 , 97.1777 , 93.75 ]
#			y_2sigma_2 = [5046.2134 , 5054.2568 , 3679.5205 , 2248.5508 , 1418.6998 , 944.4629 , 570.473 , 473.458 , 431.7812 , 419.2899 , 441.6033 , 432.0145 , 448.2071 , 469.1575 ]
#		if(whichChannel == "ele"):
#			mData = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 ]
#			x_shademasses = [260.0 , 270.0 , 300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 750.0 , 800.0 , 900.0 , 1000.0 , 1000.0 , 900.0 , 800.0 , 750.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 , 270.0 , 260.0 ]
#			xsUp_expected = [2762.5 , 2762.5 , 1898.4375 , 1175.0 , 734.375 , 481.25 , 292.9688 , 241.25 , 220.3125 , 210.9375 , 216.4062 , 207.1875 , 200.625 , 200.0 ]
#			xsUp_observed = [3632.1524 , 3881.6039 , 2996.0379 , 1047.4742 , 635.5291 , 303.6533 , 247.01 , 220.1627 , 152.8329 , 231.9272 , 213.172 , 209.2948 , 193.2141 , 183.6267 ]
#			y_1sigma = [1986.5586 , 1993.1343 , 1360.6782 , 844.9615 , 521.9154 , 340.8609 , 208.2109 , 171.4548 , 156.0435 , 149.9119 , 151.7116 , 143.4531 , 135.1623 , 131.9336 , 311.6092 , 305.3857 , 302.9871 , 313.8806 , 300.9037 , 313.399 , 344.1447 , 416.7541 , 686.5063 , 1041.7363 , 1657.4109 , 2692.999 , 3819.5986 , 3808.5872 ]
#			y_1sigma_1 = [1986.5586 , 1993.1343 , 1360.6782 , 844.9615 , 521.9154 , 340.8609 , 208.2109 , 171.4548 , 156.0435 , 149.9119 , 151.7116 , 143.4531 , 135.1623 , 131.9336 ]
#			y_1sigma_2 = [3808.5872 , 3819.5986 , 2692.999 , 1657.4109 , 1041.7363 , 686.5063 , 416.7541 , 344.1447 , 313.399 , 300.9037 , 313.8806 , 302.9871 , 305.3857 , 311.6092 ]
#			y_2sigma = [1489.1602 , 1499.9512 , 1015.9607 , 633.3984 , 390.1367 , 253.7842 , 155.6396 , 128.1641 , 116.1804 , 112.0605 , 111.5845 , 105.2124 , 97.1777 , 93.75 , 469.1575 , 448.2071 , 432.0145 , 441.6033 , 419.2899 , 431.7812 , 473.458 , 570.473 , 944.4629 , 1418.6998 , 2248.5508 , 3679.5205 , 5054.2568 , 5046.2134 ]
#			y_2sigma_1 = [1489.1602 , 1499.9512 , 1015.9607 , 633.3984 , 390.1367 , 253.7842 , 155.6396 , 128.1641 , 116.1804 , 112.0605 , 111.5845 , 105.2124 , 97.1777 , 93.75 ]
#			y_2sigma_2 = [5046.2134 , 5054.2568 , 3679.5205 , 2248.5508 , 1418.6998 , 944.4629 , 570.473 , 473.458 , 431.7812 , 419.2899 , 441.6033 , 432.0145 , 448.2071 , 469.1575 ]
	#------------------

	br_HH_bbZZ = 0.030506112
#	if (do_noBR):
##		for i in range(len(mTh)):
##			xsTh[i] *= 0.001/(br_HH_bbZZ)
##			xsTh_lam1[i] *= 0.001/(br_HH_bbZZ)
#		for i in range(len(xsUp_expected)):
#			xsUp_expected[i] *= 0.001/(br_HH_bbZZ)
#			xsUp_observed[i] *= 0.001/(br_HH_bbZZ)
##			y_1sigma_1[i] *= 0.001/(br_HH_bbZZ)
##			y_1sigma_2[i] *= 0.001/(br_HH_bbZZ)
##			y_2sigma_1[i] *= 0.001/(br_HH_bbZZ)
##			y_2sigma_2[i] *= 0.001/(br_HH_bbZZ)
#		for i in range(len(y_1sigma)):
#			y_1sigma[i] *= 0.001/(br_HH_bbZZ)
#			y_2sigma[i] *= 0.001/(br_HH_bbZZ)


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
	if (do_gg_hh_bbzz):
		if (resType == "HHres"):
			plotLow=1
			plotHigh=100000
		if (resType == "HHBulkGrav"):
			plotLow=0.01
			plotHigh=1000000
	elif (do_noBR):
		if (resType == "HHres"):
			plotLow=0.2
			plotHigh=1400
		if (resType == "HHBulkGrav"):
			plotLow=0.2
			plotHigh=1400

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
	#xsTh_vs_m.SetLineColor(kBlue)
	xsTh_vs_m.SetLineColor(2)
	#xsTh_vs_m.SetLineStyle(8)
	#xsTh_vs_m.SetFillColor(kCyan-6)
	#xsTh_vs_m.SetMarkerSize(0.00001)
	#xsTh_vs_m.SetMarkerStyle(22)
	#xsTh_vs_m.SetMarkerColor(kBlue)

	xsTh_lam1_vs_m = TGraph(nTH, array("d",mTh), array("d",xsTh_lam1))
	xsTh_lam1_vs_m.SetLineWidth(2)
	#xsTh_lam1_vs_m.SetLineColor(kBlue)
	xsTh_lam1_vs_m.SetLineColor(2)
	#xsTh_lam1_vs_m.SetFillColor(kCyan-6)
	#xsTh_lam1_vs_m.SetMarkerSize(0.00001)
	#xsTh_lam1_vs_m.SetMarkerStyle(22)
	#xsTh_lam1_vs_m.SetMarkerColor(kBlue)

		
	xsData_vs_m_expected = TGraph(len(xsUp_expected), array("d",mData), array("d",xsUp_expected))
	xsData_vs_m_expected.SetMarkerStyle(0)
	xsData_vs_m_expected.SetMarkerColor(kBlack)
	xsData_vs_m_expected.SetLineColor(kBlack)
	xsData_vs_m_expected.SetLineWidth(2)
	xsData_vs_m_expected.SetLineStyle(7)
	xsData_vs_m_expected.SetMarkerSize(0.001)

	xsData_vs_m_observed = TGraph(len(xsUp_observed[:6]), array("d",mData[:6]), array("d",xsUp_observed[:6]))
	xsData_vs_m_observed.SetMarkerStyle(20)
	xsData_vs_m_observed.SetMarkerColor(kBlack)
	xsData_vs_m_observed.SetLineColor(kBlack)
	xsData_vs_m_observed.SetLineWidth(2)
	xsData_vs_m_observed.SetLineStyle(1)
	xsData_vs_m_observed.SetMarkerSize(1)

	xsData_vs_m_observed_high = TGraph(len(xsUp_observed[6:]), array("d",mData[6:]), array("d",xsUp_observed[6:]))
	xsData_vs_m_observed_high.SetMarkerStyle(20)
	xsData_vs_m_observed_high.SetMarkerColor(kBlack)
	xsData_vs_m_observed_high.SetLineColor(kBlack)
	xsData_vs_m_observed_high.SetLineWidth(2)
	xsData_vs_m_observed_high.SetLineStyle(1)
	xsData_vs_m_observed_high.SetMarkerSize(1)

	xsData_vs_m_observed_high_p = TGraph(len(xsUp_observed[7:]), array("d",mData[7:]), array("d",xsUp_observed[7:]))
	xsData_vs_m_observed_high_p.SetMarkerStyle(20)
	xsData_vs_m_observed_high_p.SetMarkerColor(kBlack)
	xsData_vs_m_observed_high_p.SetLineColor(kBlack)
	xsData_vs_m_observed_high_p.SetLineWidth(2)
	xsData_vs_m_observed_high_p.SetLineStyle(1)
	xsData_vs_m_observed_high_p.SetMarkerSize(1)

	# exp_2l2j_limits
	exp_2l2j_vs_m = TGraph(len(exp_2l2j_limits), array("d",mass_2l2j), array("d",exp_2l2j_limits))
	exp_2l2j_vs_m.SetLineWidth(2)
	exp_2l2j_vs_m.SetLineColor(kRed)
	exp_2l2j_vs_m.SetLineStyle(8)
	exp_2l2j_vs_m.SetMarkerSize(0.00001)
	exp_2l2j_vs_m.SetMarkerStyle(22)
	exp_2l2j_vs_m.SetMarkerColor(kRed)

	# exp_2l2nu_limits
	exp_2l2nu_vs_m = TGraph(len(exp_2l2nu_limits), array("d",mass_2l2nu), array("d",exp_2l2nu_limits))
	exp_2l2nu_vs_m.SetLineWidth(2)
	exp_2l2nu_vs_m.SetLineColor(kBlue)
	exp_2l2nu_vs_m.SetLineStyle(8)
	exp_2l2nu_vs_m.SetMarkerSize(0.00001)
	exp_2l2nu_vs_m.SetMarkerStyle(22)
	exp_2l2nu_vs_m.SetMarkerColor(kRed)


#	xsUp_observed_logY, xsUp_expected_logY = [0 for i in range(len(mData))], [0 for i in range(len(mData))]
#	xsTh_logY = [0 for i in range(len(mTh))]
#	for ii in range(len(mData)): xsUp_observed_logY[ii] = math.log10(xsUp_observed[ii])
#	for ii in range(len(mData)): xsUp_expected_logY[ii] = math.log10(xsUp_expected[ii])
#	for ii in range(len(mTh)): xsTh_logY[ii] = math.log10(xsTh[ii])
#	xsTh_vs_m_log = TGraph(nTH, array("d",mTh), array("d",xsTh_logY))
#	xsData_vs_m_expected_log = TGraph(massPoints, array("d",mData), array("d",xsUp_expected_logY))
#	xsData_vs_m_observed_log = TGraph(massPoints, array("d",mData), array("d",xsUp_observed_logY))

	exshade1 = TGraph(len(y_1sigma),array("d",x_shademasses),array("d",y_1sigma))
	exshade1.SetFillColor(kGreen)
	exshade2 = TGraph(len(y_2sigma),array("d",x_shademasses),array("d",y_2sigma))
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
		xsData_vs_m_observed_high.Draw("L")
		xsData_vs_m_observed_high_p.Draw("P")
	#grshade.SetFillStyle(1001)

	if draw_2l2j_limits:
		exp_2l2j_vs_m.Draw("L")
		exp_2l2nu_vs_m.Draw("L")

	if drawRegionSeparator:
		#yValue = 35000 if not doFullHH else 1000 if doFullHH  else 0
		yValue = 1000
		line = TLine(450, 0, 450, yValue)
		line.SetLineColor(kBlack)
		line.SetLineWidth(2)
		line.SetLineStyle(9)
		line.Draw("same")


#	legend = TLegend(.3875,.6,.91,.87);
#	legend.SetBorderSize(1);
#	legend.SetFillColor(0);
#	#legend.SetFillStyle(0);
#	legend.SetTextSize(.036);
#	legend.SetTextFont(42);
#	legend.SetMargin(0.15);



	legend = TLegend(.55, .60, .90, .90)
	if _obs_limit:
		legend.AddEntry(xsData_vs_m_observed , "Observed", "lp")
	legend.AddEntry(xsData_vs_m_expected, "Median expected", "l")
	legend.AddEntry(exp_2l2j_vs_m, "Median expected (lljj)", "l")
	legend.AddEntry(exp_2l2nu_vs_m, "Median expected (ll#nu#nu)", "l")
	legend.AddEntry(exshade1, "68 % expected", "f")
	legend.AddEntry(exshade2, "95 % expected", "f")

	legend.AddEntry(xsTh_lam1_vs_m, particleTypeFullName, "l")
	legend.SetShadowColor(0)
	legend.SetFillColor(0)
	legend.SetLineColor(0)

#	if (do_gg_hh_bbzz):
#		legend.SetHeader("gg #rightarrow HH #rightarrow b#bar{b}ZZ")
#	elif (do_noBR):
#		legend.SetHeader("gg #rightarrow HH ")
#
#	if (resType == "HHres"):
#		legend.AddEntry(xsTh_lam1_vs_m,"#sigma_{theory} (#lambda_{R}= 1 TeV)","lf")
#		legend.AddEntry(xsTh_vs_m     ,"#sigma_{theory} (#lambda_{R}= 3 TeV)","lf")
#	else:
#		legend.AddEntry(xsTh_vs_m     ,"#sigma_{theory} (#Kappa= 0.1)","lf")
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