#%%time
#Field Catalogue========================================================
catname1 = 'ultravista'
colnames1 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp'}
colnameslist1 = list(colnames1.values())
data1 = {namekey: np.array(catalogues[catname1][namevalue]) for namekey, namevalue in colnames1.items()}
zrange1 = [0.8, 1.0]

#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'griffith'
colnames2 = {'radius': 'RE_GALFIT_HI', 'z': 'Z'}
colnameslist2 = list(colnames2.values())
data2 = {namekey: np.array(catalogues[catname2][namevalue]) for namekey, namevalue in colnames2.items()}
#IMPORTANT, CHANGE BELOW AS NECESSARY
radcol2convert = 0.05
data2['radius'] = radcol2convert*data2['radius']

#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
#catname2 = 'morph_zurich'
#colnames2 = {'radius': 'R_GIM2D', 'M20': 'M20', 'CC': 'CC', 'AA': 'AA'}
#colnameslist2 = list(colnames2.values())
#data2 = {namekey: np.array(catalogues[catname2][namevalue]) for namekey, namevalue in colnames2.items()}
##IMPORTANT, CHANGE BELOW AS NECESSARY
#radcol2convert = 1.0
#data2['radius'] = radcol2convert*data2['radius']

#Group Catalogue=======================================================
catname3 = 'balogh_data2'
colnames3 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp', 'gp': 'zp_prob', 'gd': 'groupdist', 'gr': 'R200'}
colnameslist3 = list(colnames3.values())
data3 = {namekey: np.array(catalogues[catname3][namevalue]) for namekey, namevalue in colnames3.items()}
zrange3 = zrange1 

#Importing the matching arrays
mat1 = np.array(catalogues[catname1][catname2+'_match'])
mat3 = np.array(catalogues[catname3][catname2+'_match'])

#Binwidth Definition, NumBins is number of point (Number of bins +1), position corresponds to different radfactor 
radfactor = [0.0, 1.0, 1.5, 2.0]
xlim = np.array([[9.0, 11.5], [8.5, 10.3], [8.0, 10.0], [7.0, 9.5]])
NumBins = 12
bins = [np.linspace(xlim[i][0], xlim[i][1], NumBins+1, endpoint=True) for i in range(len(radfactor))]
          
#2 represents two options: group or field DELETE INITIAL ENTRIES
qMRg, sfMRg, qMRf, sfMRf = [], [], [], []
#Creating all arrays=================================================

#NumBins represents total number of bins   
allbing = [np.zeros(NumBins) for i in range(len(radfactor))] 
allbinf = [np.zeros(NumBins) for i in range(len(radfactor))] 
qbing = [np.zeros(NumBins) for i in range(len(radfactor))] 
qbinf = [np.zeros(NumBins) for i in range(len(radfactor))] 
#Creating Generators

cat1gen = genentries(catname1, colnameslist1, catname2, colnameslist2, zcol=colnames1['z'], zrange=zrange1)

#Here I am selecting 0.8<=z<=1.0 by griffith matched z entries
#cat1gen = (i for i in genentries(catname1, colnameslist1, catname2, colnameslist2) if data2['z'][mat1[i]] >= 0.8 and data2['z'][mat1[i]] <= 1.0)
#Applying R200 cut: only groups with a groupdist within R200 limit will count
cat3gen = genentries(catname3, colnameslist3, catname2, colnameslist2, zcol=colnames3['z'], zrange=zrange3)

#cat3gen = (i for i in genentries(catname3, colnameslist3, catname2, colnameslist2) if data2['z'][mat3[i]] >= 0.8 and data2['z'][mat3[i]] <= 1.0)

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
    rad = data2['radius'][mat3[i]]
    gp = data3['gp'][i]
    z = data3['z'][i]
    if data3['type'][i] == 'sf':
        #starforming
        sfMRg.append([mass, rad, z, gp])
    else:    
        #quiescent
        qMRg.append([mass, rad, z, gp])
    
#Deleting Initial Entries==============================                
qMRg = np.array(qMRg)
sfMRg = np.array(sfMRg)
qMRf = np.array(qMRf)
sfMRf = np.array(sfMRf)

#Converting to actual distance (converting an entire array is faster than converting each entry one by one) I do it here after converting the data to a numpy array, which supports column indexing.
sfMRf[:, 1] = (sfMRf[:, 1]*u.arcsec).to(u.rad)*(Distance(z=sfMRf[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 
qMRf[:, 1] = (qMRf[:, 1]*u.arcsec).to(u.rad)*(Distance(z=qMRf[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad)
sfMRg[:, 1] = (sfMRg[:, 1]*u.arcsec).to(u.rad)*(Distance(z=sfMRg[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 
qMRg[:, 1] = (qMRg[:, 1]*u.arcsec).to(u.rad)*(Distance(z=qMRg[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 

#Creating Total Entries==============================================
allMRg = np.vstack((qMRg, sfMRg))
allMRf = np.vstack((qMRf, sfMRf)) 

#HISTOGRAM ANALYSIS============================                           
for i in range(len(radfactor)):
    #group
    allbing[i], bins[i] = np.histogram(allMRg[:, 0]-radfactor[i]*np.log10(allMRg[:, 1]), bins=bins[i], weights=allMRg[:, 3])
    qbing[i], bins[i] = np.histogram(qMRg[:, 0]-radfactor[i]*np.log10(qMRg[:, 1]), bins=bins[i], weights=qMRg[:, 3]) #field                               
    allbinf[i], bins[i] = np.histogram(allMRf[:, 0]-radfactor[i]*np.log10(allMRf[:, 1]), bins=bins[i])
    qbinf[i], bins[i] = np.histogram(qMRf[:, 0]-radfactor[i]*np.log10(qMRf[:, 1]), bins=bins[i])
   
   
#PLOTTING================================================================                    
#pl.close()   
fig, ax = pl.subplots(1, len(radfactor), figsize = (23, 6))#, sharey=True)
fig.suptitle(r'Quiescent Fraction vs. $\log(M/R_e^n)$ with ' + catname1 + ', ' + catname2 + ', ' + catname3 + ' ' + str(zrange1[0]) + '$ \leq z \leq $' + str(zrange1[1]), fontsize=16)
fig.subplots_adjust(left=0.04, right=0.98)

for i in range(len(radfactor)):
    x = 0.5*(bins[i][:-1] + bins[i][1:])
    ax[i].plot(x, qbing[i]/allbing[i], color='black', linestyle='-', marker='o',  markerfacecolor='black', markeredgecolor='black', label=str(allMRg.shape[0])+r' Groups within $R_{200}$')

    ax[i].plot(x, qbinf[i]/allbinf[i], color='red', linestyle='-', marker='o',  markerfacecolor='red', markeredgecolor='red', label=str(allMRf.shape[0])+' Fields')
    
    #Error Bars
    #ax[i].errorbar(x, qbing[i]/allbing[i], yerr=errg[:, i], color='black')    
    #ax[i].errorbar(x, qbinf[i]/allbinf[i], yerr=errf[:, i], color='red')

    if radfactor[i] != 0.0:
        ax[i].set_xlabel(r'$\log(M/R_e^{{%s}}\, M_*/kpc)$' % (radfactor[i]))
    else:
        ax[i].set_xlabel(r'$\log(M\, M_*)$')
    ax[i].set_ylabel(r'Quiescent Fraction')
    
    ax[i].set_xlim(bins[i][0], bins[i][-1])
    ax[i].set_ylim(0.0, 1.0)
    
    ax[i].set_yticks(np.linspace(0.0, 1.0, 11, endpoint=True))
    
    legend = ax[i].legend(loc='upper left', fontsize=12)
    
    legend.draw_frame(False)

