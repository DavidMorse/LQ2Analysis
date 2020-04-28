#!/usr/bin/python
import sys
import os
sys.argv.append( '-b True' )
from ROOT import *
import math
from optparse import OptionParser


##########################################################################################
#################      SETUP OPTIONS - File, Normalization, etc    #######################
##########################################################################################

# Input Options - file, cross-section, number of vevents
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="input root file", metavar="FILE")
parser.add_option("-b", "--batch", dest="dobatch", help="run in batch mode", metavar="BATCH")
parser.add_option("-s", "--sigma", dest="crosssection", help="specify the process cross-section", metavar="SIGMA")
parser.add_option("-n", "--ntotal", dest="ntotal", help="total number of MC events for the sample", metavar="NTOTAL")
parser.add_option("-l", "--lumi", dest="lumi", help="integrated luminosity for data taking", metavar="LUMI")
parser.add_option("-j", "--json", dest="json", help="json file for certified run:lumis", metavar="JSON")
parser.add_option("-d", "--dir", dest="dir", help="output directory", metavar="DIR")
parser.add_option("-p", "--pdf", dest="pdf", help="option to produce pdf uncertainties", metavar="PDF")
parser.add_option("-y", "--year", dest="year", help="option to pick running year (2016,2017,2018)", metavar="YEAR")

(options, args) = parser.parse_args()


# Here we get the file name, and adjust it accordingly for EOS, castor, or local directory
name = options.filename

if '/store' in name:
	name = 'root://eoscms//eos/cms'+name

# Get the file, tree, and number of entries
fin = TFile.Open(name,"READ")

hev = fin.Get('EventCounter')
#Now we always use the 3rd bin, so that the genWeight will be canceled out later.
NORIG = hev.GetBinContent(3)
#if 'amcnlo' in name or 'amcatnlo' in name:
#	NORIG = hev.GetBinContent(3)
#else:
#	NORIG = hev.GetBinContent(1)
outname = options.dir+'/'+(name.split('/')[-5]+'__'+name.split('/')[-1].replace('.root','_count.txt'))#changed -2 to -5 to get dataset name instead of 0000
print outname

os.system("echo "+str(NORIG) + " > "+outname)
