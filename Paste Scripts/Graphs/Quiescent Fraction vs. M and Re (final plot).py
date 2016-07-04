%%time
#Field Catalogue========================================================
catname1 = 'ultravista'
colnames1 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp'}
colnameslist1 = list(colnames1.values())
#data1 = {namekey: np.array(catalogues[catname1][namevalue]) for namekey, namevalue in colnames1.items()}
zrange1 = [0.8, 1.0]

#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'griffith'
colnames2 = {'radius': 'RE_GALFIT_HI', 'raderror': 'REERR_GALFIT_HI'}
colnameslist2 = list(colnames2.values())
#data2 = {namekey: np.array(catalogues[catname2][namevalue]) for namekey, namevalue in colnames2.items()}

#Group Catalogue=======================================================
catname3 = 'balogh_data2'
colnames3 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp', 'gp': 'zp_prob', 'gd': 'groupdist', 'R200': 'R200'}
colnameslist3 = list(colnames3.values())
#data3 = {namekey: np.array(catalogues[catname3][namevalue]) for namekey, namevalue in colnames3.items()}
zrange3 = zrange1 

#Importing the matching arrays
mat1 = np.array(catalogues[catname1][catname2+'_match'])
mat3 = np.array(catalogues[catname3][catname2+'_match'])

#Binwidth Definition, NumBins is number of point (Number of bins +1), position corresponds to different radfactor 
radfactor = [0.0, 1.0, 1.5, 2.0]
xlim = np.array([[9.0, 11.5], [8.5, 10.3], [8.0, 10.0], [7.0, 9.5]])
NumBins = 12
bins = [np.linspace(xlim[i][0], xlim[i][1], NumBins+1, endpoint=True) for i in range(len(radfactor))]
          
#NumBins represents total number of bins   
allbing = np.zeros((len(radfactor), NumBins))
allbinf = np.zeros((len(radfactor), NumBins))
qbing = np.zeros((len(radfactor), NumBins))
qbinf = np.zeros((len(radfactor), NumBins))

#Creating Generators
index1 = genindex(catname1, colnameslist1, catname2, colnameslist2, zcol=colnames1['z'], zrange=zrange1)

#Applying R200 cut: only groups with a groupdist within R200 limit will count
index3 = genindex(catname3, colnameslist3, catname2, colnameslist2, zcol=colnames3['z'], zrange=zrange3)#*(catalogues[catname3][colnames3['gd']] < 0.5*catalogues[catname3][colnames3['R200']])

#Adding the data and the matched data all at once        
alldatag = dict({namekey: np.array(catalogues[catname3][namevalue][index3]) for namekey, namevalue in colnames3.items()}, **{namekey: np.array(catalogues[catname2][namevalue][mat3[index3]]) for namekey, namevalue in colnames2.items()})
alldataf = dict({namekey: np.array(catalogues[catname1][namevalue][index1]) for namekey, namevalue in colnames1.items()}, **{namekey: np.array(catalogues[catname2][namevalue][mat1[index1]]) for namekey, namevalue in colnames2.items()})    
    
#Converting Radius(TAKES THE LONGEST)====================                
alldatag['radius'] = (alldatag['radius']*0.05*u.arcsec).to(u.rad)*(Distance(z=alldatag['z'], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 
alldatag['raderror'] = (alldatag['raderror']*0.05*u.arcsec).to(u.rad)*(Distance(z=alldatag['z'], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 
alldataf['radius'] = (alldataf['radius']*0.05*u.arcsec).to(u.rad)*(Distance(z=alldataf['z'], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 
alldataf['raderror'] = (alldataf['raderror']*0.05*u.arcsec).to(u.rad)*(Distance(z=alldataf['z'], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 

#Changing 0 error, which gives bug in calculating standard distributions to arbitrary small number
alldatag['raderror'][np.where(alldatag['raderror']==0.0)] = 1E-10
alldataf['raderror'][np.where(alldataf['raderror']==0.0)] = 1E-10





#HISTOGRAM ANALYSIS============================                           
for i in range(len(radfactor)):
    #group----
    #all
    allbing[i], bins[i] = np.histogram(alldatag['mass']-radfactor[i]*np.log10(alldatag['radius']), bins=bins[i], weights=alldatag['gp'])
    #quiescent
    qbing[i], bins[i] = np.histogram(alldatag['mass'][alldatag['type']!='sf']-radfactor[i]*np.log10(alldatag['radius'][alldatag['type']!='sf']), bins=bins[i], weights=alldatag['gp'][alldatag['type']!='sf']) 
    #field-----
    #all
    allbinf[i], bins[i] = np.histogram(alldataf['mass']-radfactor[i]*np.log10(alldataf['radius']), bins=bins[i])
    #quiescent
    qbinf[i], bins[i] = np.histogram(alldataf['mass'][alldataf['type']!='sf']-radfactor[i]*np.log10(alldataf['radius'][alldataf['type']!='sf']), bins=bins[i]) 
   
#Field ERROR=========================================================================================================================================
N=100
#Varying Mass, Radius using gaussian of error
massarray = np.random.normal(loc=alldataf['mass'], scale=0.1*np.ones(len(alldataf['mass'])), size=(N, len(alldataf['mass'])))
radarray = np.log10(np.random.normal(loc=alldataf['radius'], scale=alldataf['raderror'], size=(N, len(alldataf['radius']))))
MRdata = np.dstack((massarray, radarray))

#Selecting quiescent values, choosing by 2d dimensional boolean arrays returns all chosen values in 1D arrays, without preservation of structure. This way does preserve structure
qmassarray = np.array([massarray[i][alldataf['type']!='sf'] for i in range(N)])
qradarray = np.array([radarray[i][alldataf['type']!='sf'] for i in range(N)])
qMRdata = np.dstack((qmassarray, qradarray))

#setting bins
bindata = np.empty((NumBins, len(radfactor), N))
qbindata= np.empty((NumBins, len(radfactor), N))

for i in range(len(radfactor)):
    #group
    for j in range(N):
        bindata[:, i, j], junk = np.histogram(MRdata[j][:, 0]-radfactor[i]*MRdata[j][:, 1], bins=bins[i])
        qbindata[:, i, j], junk = np.histogram(qMRdata[j][:, 0]-radfactor[i]*qMRdata[j][:, 1], bins=bins[i])

qfracarray = qbindata/bindata
meanf = np.nanmean(qfracarray, axis=2)
errf = np.nanstd(qfracarray, axis=2)

#GROUP ERROR================================================================
N=1000
#Selecting based on group probabilities
randcol = np.random.random_sample([N, len(alldatag['gp'])])
choosecol = alldatag['gp'] > randcol
#All chosen vaues and all NOT starmforming, aka quiescent
qchoosecol = choosecol * (alldatag['type'] != 'sf')

#Varying Mass, Radius using gaussian of error
massarray = np.random.normal(loc=alldatag['mass'], scale=0.1*np.ones(len(alldatag['mass'])), size=(N, len(alldatag['mass'])))

radarray = np.log10(np.random.normal(loc=alldatag['radius'], scale=alldatag['raderror'], size=(N, len(alldatag['radius']))))

#Selecting values that were chosen by realizations
MRdata = [np.array([massarray[i][choosecol[i]], radarray[i][choosecol[i]]]).T for i in range(N)]

qMRdata = [np.array([massarray[i][qchoosecol[i]], radarray[i][qchoosecol[i]]]).T for i in range(N)]

#setting bins
bindata = np.empty((NumBins, len(radfactor), N))
#allbinf = [np.zeros(i) for i in NumBins] 
qbindata= np.empty((NumBins, len(radfactor), N))
#qbinf = [np.zeros(i) for i in NumBins]

for i in range(len(radfactor)):
    #group
    for j in range(N):
        bindata[:, i, j], junk = np.histogram(MRdata[j][:, 0]-radfactor[i]*MRdata[j][:, 1], bins=bins[i])
        qbindata[:, i, j], junk = np.histogram(qMRdata[j][:, 0]-radfactor[i]*qMRdata[j][:, 1], bins=bins[i])

qfracarray = qbindata/bindata

meang = np.nanmean(qfracarray, axis=2)
errg = np.nanstd(qfracarray, axis=2)
   
#PLOTTING================================================================                    
#pl.close()   
fig, ax = pl.subplots(1, len(radfactor), figsize = (23, 6))#, sharey=True)
#fig.suptitle(r'Quiescent Fraction vs. $\log(M/R_e^n)$ with ' + catname1 + ', ' + catname2 + ', ' + catname3 + ' ' + str(zrange1[0]) + '$ \leq z \leq $' + str(zrange1[1]), fontsize=16)
fig.subplots_adjust(left=0.04, right=0.98, wspace=0.15)

ax[0].set_ylabel(r'Quiescent Fraction')

for i in range(len(radfactor)):
    x = 0.5*(bins[i][:-1] + bins[i][1:])
    ax[i].plot(x, qbing[i]/allbing[i], color='black', linestyle='-', marker='o',  markerfacecolor='black', markeredgecolor='black', label=str(len(alldatag['mass']))+r' Group Entries')

    ax[i].plot(x, qbinf[i]/allbinf[i], color='red', linestyle='-', marker='o',  markerfacecolor='red', markeredgecolor='red', label=str(len(alldataf['mass']))+' Field Entries')
    
    #Error Bars
    ax[i].errorbar(x, qbing[i]/allbing[i], yerr=errg[:, i], color='black')    
    ax[i].errorbar(x, qbinf[i]/allbinf[i], yerr=errf[:, i], color='red')

    if radfactor[i] != 0.0:
        ax[i].set_xlabel(r'$\log(M/R_e^{{%s}}\, M_*/kpc)$' % (radfactor[i]))
    else:
        ax[i].set_xlabel(r'$\log(M\, M_*)$')
    
    ax[i].set_xlim(bins[i][0], bins[i][-1])
    ax[i].set_ylim(0.0, 1.0)
    
    ax[i].set_yticks(np.linspace(0.0, 1.0, 11, endpoint=True))
    
    legend = ax[i].legend(loc='upper left', fontsize=12)
    
    legend.draw_frame(False)

