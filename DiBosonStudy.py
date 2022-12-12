from matplotlib import pyplot as plt

######################################## Here is where all the event yield data is stored ########################################

################# 2016 #################

#### No lepton veto ####

# 2016 Enhanced selection (no lepton veto)
vv_2016_EnhancedSel_noVeto = [14.23, 14.31, 13.57, 12.11, 10.62, 8.04, 7.17, 5.93, 5.2, 4.49, 3.13, 2.28, 1.71, 0.832, 0.723, 0.83, 0.626, 0.587, 0.442, 0.394, 0.348, 0.303, 0.287, 0.266, 0.319, 0.319, 0.332, 0.264, 0.168, 0.0]

#### mu pt > 45 GeV ####

# 2016 Enhanced selection (mu pT > 45)
vv_2016_EnhancedSel_pt45 = [12.52, 12.61, 11.94, 10.6, 9.29, 6.85, 6.17, 5.05, 4.49, 3.86, 2.65, 1.93, 1.45, 0.663, 0.542, 0.674, 0.503, 0.464, 0.341, 0.293, 0.252, 0.208, 0.187, 0.167, 0.219, 0.219, 0.233, 0.165, 0.113, 0.0]

#### mu pt > 20 GeV ####

# 2016 Enhanced selection (mu pT > 20)
vv_2016_EnhancedSel_pt20 = [10.49, 10.58, 10.08, 8.97, 7.97, 5.87, 5.29, 4.41, 3.93, 3.37, 2.33, 1.72, 1.22, 0.462, 0.405, 0.549, 0.4, 0.407, 0.309, 0.264, 0.231, 0.208, 0.187, 0.167, 0.219, 0.219, 0.233, 0.165, 0.113, 0.0]


################# 2017 #################

#### No lepton veto ####

# 2017 Enhanced selection (no lepton veto)
vv_2017_EnhancedSel_noVeto = [25.44, 25.39, 24.04, 20.31, 16.81, 13.04, 10.73, 9.24, 8.12, 7.19, 6.92, 5.21, 4.99, 4.47, 2.47, 2.17, 1.91, 1.59, 1.37, 0.555, 0.54, 0.454, 0.377, 0.39, 0.339, 0.296, 0.278, 0.177, 0.177, 0.0]

#### mu pt > 45 GeV ####

# 2017 Enhanced selection (mu pT > 45)
vv_2017_EnhancedSel_pt45 = [24.1, 24.05, 22.77, 19.06, 15.71, 12.12, 10, 8.55, 7.63, 6.85, 6.6, 4.93, 4.76, 4.25, 2.31, 2.05, 1.8, 1.49, 1.27, 0.481, 0.47, 0.403, 0.329, 0.341, 0.291, 0.27, 0.252, 0.151, 0.151, 0.0]

#### mu pt > 20 GeV ####

# 2017 Enhanced selection (mu pT > 20)
vv_2017_EnhancedSel_pt20 = [23.1, 23.05, 21.72, 18.26, 15.07, 11.62, 9.58, 8.19, 7.38, 6.78, 6.58, 4.91, 4.68, 4.21, 2.27, 2.01, 1.75, 1.45, 1.23, 0.437, 0.426, 0.361, 0.311, 0.323, 0.273, 0.252, 0.252, 0.151, 0.151, 0.0]

################# 2018 #################

#### No lepton veto ####

# 2018 Enhanced selection (no lepton veto)
vv_2018_EnhancedSel_noVeto = [41.59, 41.69, 37.96, 33.14, 28.8, 28.9, 23.12, 16.87, 13.1, 7.97, 5.05, 4.06, 3.08, 2.65, 3.5, 3.2, 2.32, 2.04, 2.08, 0.89, 0.75, 0.87, 0.84, 0.83, 0.416, 0.331, 0.284, 0.284, 0.185, 0.034]

#### mu pt > 45 GeV ####

# 2018 Enhanced selection (mu pT > 45)
vv_2018_EnhancedSel_pt45 = [39.85, 39.95, 36.21, 31.65, 27.51, 27.97, 22.2, 16.13, 12.56, 7.55, 4.72, 3.83, 2.88, 2.45, 3.3, 2.99, 2.12, 1.91, 1.94, 0.81, 0.72, 0.8, 0.8, 0.78, 0.373, 0.291, 0.27, 0.27, 0.185, 0.034]

#### mu pt > 20 GeV ####

# 2018 Enhanced selection (mu pT > 20)
vv_2018_EnhancedSel_pt20 = [37.64, 37.75, 34.23, 30.06, 26.16, 26.86, 21.35, 15.54, 12.19, 7.22, 4.52, 3.6, 2.77, 2.35, 3.16, 2.88, 2.03, 1.84, 1.88, 0.74, 0.65, 0.76, 0.77, 0.76, 0.349, 0.275, 0.254, 0.254, 0.169, 0.018]

######################################## Calculations are done here ########################################

LQmasses = ['300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000','2100','2200','2300','2400','2500']#,'2600','2700','2800','2900','3000','3500','4000']
x = [300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500]#,2600,2700,2800,2900,3000,3500,4000]

y_2016_EnhancedSel_noVeto = []
y_2016_EnhancedSel_pt45 = []
y_2016_EnhancedSel_pt20 = []

y_2017_EnhancedSel_noVeto = []
y_2017_EnhancedSel_pt45 = []
y_2017_EnhancedSel_pt20 = []

y_2018_EnhancedSel_noVeto = []
y_2018_EnhancedSel_pt45 = []
y_2018_EnhancedSel_pt20 = []

for i, mass in enumerate(LQmasses):

    y_2016_EnhancedSel_noVeto.append(vv_2016_EnhancedSel_noVeto[i])
    y_2016_EnhancedSel_pt45.append(vv_2016_EnhancedSel_pt45[i])
    y_2016_EnhancedSel_pt20.append(vv_2016_EnhancedSel_pt20[i])

    y_2017_EnhancedSel_noVeto.append(vv_2017_EnhancedSel_noVeto[i])
    y_2017_EnhancedSel_pt45.append(vv_2017_EnhancedSel_pt45[i])
    y_2017_EnhancedSel_pt20.append(vv_2017_EnhancedSel_pt20[i])

    y_2018_EnhancedSel_noVeto.append(vv_2018_EnhancedSel_noVeto[i])
    y_2018_EnhancedSel_pt45.append(vv_2018_EnhancedSel_pt45[i])
    y_2018_EnhancedSel_pt20.append(vv_2018_EnhancedSel_pt20[i])



######################################## Do plotting here ########################################

############# 2016 Enhanced Selection #############

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

print 'x=',x

plt_2016_EnhancedSel_noVeto = ax.plot(x,y_2016_EnhancedSel_noVeto,'-',linewidth=1, label="no lepton veto",color='tab:red')
plt_2016_EnhancedSel_pt45 = ax.plot(x,y_2016_EnhancedSel_pt45,'-',linewidth=1, label="pT>45 lepton veto",color='tab:blue')
plt_2016_EnhancedSel_pt20 = ax.plot(x,y_2016_EnhancedSel_pt20,'-',linewidth=1, label="pT>20 lepton veto",color='tab:green')

ax.set_ylabel("DiBoson Events",fontsize=16)
ax.set_xlabel(r"$M_{LQ}$ [GeV]",fontsize=16)

all_2016_EnhancedSel = plt_2016_EnhancedSel_noVeto+plt_2016_EnhancedSel_pt45+plt_2016_EnhancedSel_pt20
labels = [l.get_label() for l in all_2016_EnhancedSel]
ax.legend(title = "2016 DiBoson MC")#all_2016_EnhancedSel, labels, loc=9)
ax.set_yscale('log')

plt.savefig("DiBosonStudy2016EnhancedSel.pdf")
plt.close(fig)

############# 2017 Enhanced Selection #############

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

print 'x=',x

plt_2017_EnhancedSel_noVeto = ax.plot(x,y_2017_EnhancedSel_noVeto,'-',linewidth=1, label="no lepton veto",color='tab:red')
plt_2017_EnhancedSel_pt45 = ax.plot(x,y_2017_EnhancedSel_pt45,'-',linewidth=1, label="pT>45 lepton veto",color='tab:blue')
plt_2017_EnhancedSel_pt20 = ax.plot(x,y_2017_EnhancedSel_pt20,'-',linewidth=1, label="pT>20 lepton veto",color='tab:green')

ax.set_ylabel("DiBoson Events",fontsize=16)
ax.set_xlabel(r"$M_{LQ}$ [GeV]",fontsize=16)

all_2017_EnhancedSel = plt_2017_EnhancedSel_noVeto+plt_2017_EnhancedSel_pt45+plt_2017_EnhancedSel_pt20
labels = [l.get_label() for l in all_2017_EnhancedSel]
ax.legend(title = "2017 DiBoson MC")#all_2017_EnhancedSel, labels, loc=9)
ax.set_yscale('log')

plt.savefig("DiBosonStudy2017EnhancedSel.pdf")
plt.close(fig)

############# 2018 Enhanced Selection #############

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

print 'x=',x

plt_2018_EnhancedSel_noVeto = ax.plot(x,y_2018_EnhancedSel_noVeto,'-',linewidth=1, label="no lepton veto",color='tab:red')
plt_2018_EnhancedSel_pt45 = ax.plot(x,y_2018_EnhancedSel_pt45,'-',linewidth=1, label="pT>45 lepton veto",color='tab:blue')
plt_2018_EnhancedSel_pt20 = ax.plot(x,y_2018_EnhancedSel_pt20,'-',linewidth=1, label="pT>20 lepton veto",color='tab:green')

ax.set_ylabel("DiBoson Events",fontsize=16)
ax.set_xlabel(r"$M_{LQ}$ [GeV]",fontsize=16)

all_2018_EnhancedSel = plt_2018_EnhancedSel_noVeto+plt_2018_EnhancedSel_pt45+plt_2018_EnhancedSel_pt20
labels = [l.get_label() for l in all_2018_EnhancedSel]
ax.legend(title = "2018 DiBoson MC")#all_2018_EnhancedSel, labels, loc=9)
ax.set_yscale('log')

plt.savefig("DiBosonStudy2018EnhancedSel.pdf")
plt.close(fig)
