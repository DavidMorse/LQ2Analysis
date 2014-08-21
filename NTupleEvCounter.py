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

(options, args) = parser.parse_args()


# Here we get the file name, and adjust it accordingly for EOS, castor, or local directory
name = options.filename
if '/store' in name:
	name = 'root://eoscms//eos/cms'+name
if '/castor/cern.ch' in name:
	name = 'rfio://'+name

# Get the file, tree, and number of entries
fin = TFile.Open(name,"READ")

hev = fin.Get('LJFilter/EventCount/EventCounter')
NORIG = hev.GetBinContent(1)
outname = options.dir+'/'+(name.split('/')[-2]+'__'+name.split('/')[-1].replace('.root','_count.txt'))
print outname

os.system("echo "+str(NORIG) + " > "+outname)