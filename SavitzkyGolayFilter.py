from scipy.signal import savgol_filter as sgf
from matplotlib import pyplot as plt
import numpy as np
#plt.rc(usetex = True)

# masses
masses = np.array([300.0 , 400.0 , 500.0 , 600.0 , 700.0 , 800.0 , 900.0 , 1000.0 , 1100.0 , 1200.0 , 1300.0 , 1400.0 , 1500.0 , 1600.0 , 1700.0 , 1800.0 , 1900.0 , 2000.0 , 2100.0 , 2200.0 , 2300.0 , 2400.0 , 2500.0])
# data x
# 2017 expected upper limits
x = np.array([0.0025206 , 0.0009065 , 0.0004509 , 0.00032414 , 0.000477226 , 0.00021172 , 0.0001904 , 0.000335312 , 0.00014154 , 0.0001331194 , 0.00013457675 , 0.000271656 , 0.00012630484 , 0.0001381305 , 0.00013051533 , 0.000126910224 , 0.000114617428 , 0.000125449506 , 0.0001533328005 , 0.0002496909818 , 0.0001309580117 , 0.00026120573 , 0.0002424988665])
# order
order = [1,2,3,4,5]
window = [(2*m)+1 for m in order] 

#filter
filtered1 = sgf(x,window[0],order[0])
filtered2 = sgf(x,window[1],order[1])
filtered3 = sgf(x,window[2],order[2])
filtered4 = sgf(x,window[3],order[3])
filtered5 = sgf(x,window[4],order[4])

print "filtered1 = ",filtered1
print "filtered2 = ",filtered2
print "filtered3 = ",filtered3
print "filtered4 = ",filtered4
print "filtered5 = ",filtered5

# plot to check
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(masses,x, label='unfiltered')
ax.plot(masses,filtered1, label='poly order: '+str(order[0])+', window length: '+str(window[0]))
ax.plot(masses,filtered2, label='poly order: '+str(order[1])+', window length: '+str(window[1]))
ax.plot(masses,filtered3, label='poly order: '+str(order[2])+', window length: '+str(window[2]))
ax.plot(masses,filtered4, label='poly order: '+str(order[3])+', window length: '+str(window[3]))
ax.plot(masses,filtered5, label='poly order: '+str(order[4])+', window length: '+str(window[4]))

ax.set_ylabel(r"$\sigma\, \beta^2$ [pb]")
ax.set_xlabel('LQ mass [GeV]')

ax.set_yscale('log')
ax.legend()
plt.savefig("SavitzkyGolayFilterStudy2017.pdf")