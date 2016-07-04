%%time
#Field Catalogue========================================================
catname1 = 'balogh_data2'
colnames1 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp', 'gp': 'zp_prob', 'gd': 'groupdist', 'gr': 'R200'}
colnameslist1 = list(colnames3.values())
data1 = {namekey: np.array(catalogues[catname3][namevalue]) for namekey, namevalue in colnames3.items()}
zrange1 = [0.8, 1.0]

#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'griffith'
colnames2 = {'radius': 'RE_GALFIT_HI'}
colnameslist2 = list(colnames2.values())
data2 = {namekey: np.array(catalogues[catname2][namevalue]) for namekey, namevalue in colnames2.items()}
#IMPORTANT, CHANGE BELOW AS NECESSARY
radcol2convert = 0.05

#Creating the matching arrays
cat1 = catalogues[catname1]
mat1 = cat1[catname2+'_match']
cat2 = catalogues[catname2]
cat3 = catalogues[catname3]
mat3 = cat3[catname2+'_match']

#Binwidth Definition, N is number of point (Number of bins +1), position corresponds to different radfactor 
radfactor = [0.0, 1.0, 1.5, 2.0]
xlim = np.array([[9.5, 11.5], [8.5, 10.5], [8.0, 10.0], [7.0, 9.5]])
N = np.array([12, 12, 12, 12], dtype=int)
bins = [np.linspace(xlim[i][0], xlim[i][1], N[i]+1, endpoint=True) for i in range(len(radfactor))]
          
#2 represents two options: group or field DELETE INITIAL ENTRIES
qMRg, sfMRg, qMRf, sfMRf = [], [], [], []
#Creating all arrays=================================================

#N represents total number of bins   
allbing = [np.zeros(i) for i in N] 
allbinf = [np.zeros(i) for i in N] 
qbing = [np.zeros(i) for i in N]
qbinf = [np.zeros(i) for i in N]

#Creating Generators
cat1gen = (i for i in genentries(catname1, colnameslist1, catname2, colnameslist2, zcol=colnames1['z'], zrange=zrange1) if data1['gp'][i] < data1['gr'][i])
#Applying R200 cut: only groups with a groupdist within R200 limit will count
cat3gen = (i for i in genentries(catname1, colnameslist1, catname2, colnameslist2, zcol=colnames1['z'], zrange=zrange1) if data1['gp'][i] >= data1['gr'][i])

#Adding Entries
#Field================================================================
for i in cat1gen:
    #defining radius, logmass
    mass = data1['mass'][i]
    rad = data2['radius'][mat1[i]]
    z = data1['z'][i]
    if data1['type'][i] == 'sf':
        #starforming
        sfMRf.append([mass, rad, z])
    else:    
        #quiescent
        qMRf.append([mass, rad, z])
        
#Group================================================================
for i in cat3gen:
    #defining radius, logmass, GROUP PROBABILITY (gp)
    mass = data3['mass'][i]
    rad = 0
    rad = (data2['radius'][mat3[i]]*radcol2convert*u.arcsec).to(u.rad)*(Distance(z=data3['z'][i], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad)
    gp = data3['gp'][i]
    if data3['type'][i] == 'sf':
        #starforming
        sfMRg.append([mass, rad, gp])
    else:    
        #quiescent
        qMRg.append([mass, rad, gp])
    
#Deleting Initial Entries==============================                
qMRg = np.array(qMRg)
sfMRg = np.array(sfMRg)
qMRf = np.array(qMRf)
sfMRf = np.array(sfMRf)

#Converting to actual distance (converting an entire array is faster than converting each entry one by one) I do it here after converting the data to a numpy array, which supports column indexing.
sfMRf[:, 1] = (sfMRf[:, 1]*radcol2convert*u.arcsec).to(u.rad)*(Distance(z=sfMRf[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 
qMRf[:, 1] = (qMRf[:, 1]*radcol2convert*u.arcsec).to(u.rad)*(Distance(z=qMRf[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad)
sfMRg[:, 1] = (sfMRg[:, 1]*radcol2convert*u.arcsec).to(u.rad)*(Distance(z=sfMRg[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 
qMRg[:, 1] = (qMRg[:, 1]*radcol2convert*u.arcsec).to(u.rad)*(Distance(z=qMRg[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 

#Creating Total Entries==============================================
allMRg = np.vstack((qMRg, sfMRg))
allMRf = np.vstack((qMRf, sfMRf)) 

#HISTOGRAM ANALYSIS============================                           
for i in range(len(radfactor)):
    allbing[i], bins[i] = np.histogram(allMRg[:, 0]-radfactor[i]*np.log10(allMRg[:, 1]), bins=bins[i], weights=allMRg[:, 2])
    qbing[i], bins[i] = np.histogram(qMRg[:, 0]-radfactor[i]*np.log10(qMRg[:, 1]), bins=bins[i], weights=qMRg[:, 2])                                
    allbinf[i], bins[i] = np.histogram(allMRf[:, 0]-radfactor[i]*np.log10(allMRf[:, 1]), bins=bins[i])
    qbinf[i], bins[i] = np.histogram(qMRf[:, 0]-radfactor[i]*np.log10(qMRf[:, 1]), bins=bins[i])
                    
#pl.close()   
fig, ax = pl.subplots(1, len(radfactor), figsize = (23, 6))# sharey=True)
fig.suptitle(r'Quiescent Fraction vs. $\log(M/R_e^n)$ with ' + catname1 + ', ' + catname2 + ', ' + catname3 + ' ' + str(zrange1[0]) + '$ \leq z \leq $' + str(zrange1[1]), fontsize=16)
fig.subplots_adjust(left=0.04, right=0.98)

for i in range(len(radfactor)):
    x = 0.5*(bins[i][:-1] + bins[i][1:])
    ax[i].plot(x, qbing[i]/allbing[i], color='black', linestyle='-', marker='o',  markerfacecolor='black', markeredgecolor='black', label=str(allMRg.shape[0])+r' Groups within $R_{200}$')

    ax[i].plot(x, qbinf[i]/allbinf[i], color='red', linestyle='--', marker='o',  markerfacecolor='none', markeredgecolor='red', label=str(allMRf.shape[0])+' Fields')

    if radfactor[i] != 0.0:
        ax[i].set_xlabel(r'$\log(M/R_e^{{%s}}\, M_*/kpc)$' % (radfactor[i]))
    else:
        ax[i].set_xlabel(r'$\log(M\, M_*)$')
    ax[i].set_ylabel(r'Quiescent Fraction')
    
    ax[i].set_xlim(bins[i][0], bins[i][-1])
    ax[i].set_ylim(0.0, 1.1)
    
    ax[i].set_yticks(np.linspace(0.0, 1.0, 11, endpoint=True))
    
    legend = ax[i].legend(loc='upper left')
    legend.draw_frame(False)

