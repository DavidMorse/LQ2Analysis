import os
import sys

files = []

blist = os.popen('cat BatcherResults/*txt | grep Double_t | grep beta_vals').readlines()

excom = os.popen('cat BatcherResults/*txt | grep Double_t | grep expected | grep combo').readlines()
obcom = os.popen('cat BatcherResults/*txt | grep Double_t | grep observed | grep combo').readlines()
s1com = os.popen('cat BatcherResults/*txt | grep Double_t | grep 1sigma | grep combo').readlines()
s2com = os.popen('cat BatcherResults/*txt | grep Double_t | grep 2sigma | grep combo').readlines()

exlljj = os.popen('cat BatcherResults/*txt | grep Double_t | grep expected | grep lljj').readlines()
oblljj = os.popen('cat BatcherResults/*txt | grep Double_t | grep observed | grep lljj').readlines()

exlvjj = os.popen('cat BatcherResults/*txt | grep Double_t | grep expected | grep lvjj').readlines()
oblvjj = os.popen('cat BatcherResults/*txt | grep Double_t | grep observed | grep lvjj').readlines()

def parselist(L):
	header = (L[0].split('{'))[0]
	n = str(int(len(L)))
	header = header.replace('[1]','['+n+']') + ' {'
	lastlist = []
	doublemarker = False
	for x in L:
		x = x.split('{')[-1]
		x = x.split('}')[0]
		if ',' in x:
			doublemarker=True
			lastlistx = x.split(',')[-1]
			if lastlistx=='0':
				lastlistx='300'
			lastlist.append(lastlistx)
			x = x.split(',')[0]
		if x == '0.0':
			x = '300.0'
		header += x+','
	if doublemarker == True:
		lastlist.reverse()
		lastlist = str(lastlist)
		lastlist = lastlist.replace('[','')
		lastlist = lastlist.replace(']','')
		lastlist = lastlist.replace('\'','')

		header += lastlist
		header = header.replace('[2]','['+str(2*(int(n)))+']')
		
	header += '}'
	header = header.replace(',}','}')
	header = header.replace('}','};')

	header = header.replace(' ','')
	header = header.replace('Double_t','Double_t ')

	print header
	return header

funcs = [blist,excom,obcom,s1com,s2com,exlljj,oblljj,exlvjj,oblvjj]

for x in funcs:
	parselist(x)