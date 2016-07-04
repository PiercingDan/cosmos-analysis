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
colnames2 = {'radius': 'RE_GALFIT_HI'}
colnameslist2 = list(colnames2.values())
data2 = {namekey: np.array(catalogues[catname2][namevalue]) for namekey, namevalue in colnames2.items()}
#IMPORTANT, CHANGE BELOW AS NECESSARY
radcol2convert = 0.05
data2['radius'] = radcol2convert*data2['radius']

#Group Catalogue=======================================================
catname3 = 'balogh_data2'
colnames3 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp'}#, 'gp': 'zp_prob', 'gd': 'groupdist', 'gr': 'R200'}
colnameslist3 = list(colnames3.values())
data3 = {namekey: np.array(catalogues[catname3][namevalue]) for namekey, namevalue in colnames3.items()}
zrange3 = zrange1 

#Importing the matching arrays
mat1 = np.array(catalogues[catname1][catname2+'_match'])
mat3 = np.array(catalogues[catname3][catname2+'_match'])

#Binwidth Definition, N is number of point (Number of bins +1), position corresponds to different radfactor 
radfactor = [0.0, 1.0, 1.5, 2.0]
xlim = np.array([[9.0, 11.5], [8.5, 10.5], [8.0, 10.0], [7.0, 9.5]])
N = np.array([12, 12, 12, 12], dtype=int)
bins = [np.linspace(xlim[i][0], xlim[i][1], N[i]+1, endpoint=True) for i in range(len(radfactor))]
          
#2 represents two options: group or field DELETE INITIAL ENTRIES
qMRg, sfMRg, qMRf, sfMRf = [], [], [], []
intMRg, intMRf = [], []

#Creating Generators

cat1gen = genentries(catname1, colnameslist1, catname2, colnameslist2, zcol=colnames1['z'], zrange=zrange1)
#Applying R200 cut: only groups with a groupdist within R200 limit will count
cat3gen = genentries(catname3, colnameslist3, catname2, colnameslist2, zcol=colnames3['z'], zrange=zrange3)
#(i for i in genentries(catname3, colnameslist3, catname2, colnameslist2, zcol=colnames3['z'], zrange=zrange3) if data3['gd'][i] < data3['gr'][i])#

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
    #elif data1['type'][i] == 'int':
        #intermediate
        #intMRf.append([mass, rad, z])
    else:    
        #quiescent
        qMRf.append([mass, rad, z])
        
#Group================================================================
for i in cat3gen:
    #defining radius, logmass, GROUP PROBABILITY (gp)
    mass = data3['mass'][i]
    rad = data2['radius'][mat3[i]]
    #gp = data3['gp'][i]
    gp = 0
    z = data3['z'][i]
    if data3['type'][i] == 'sf':
        #starforming
        sfMRg.append([mass, rad, z, gp])
    #elif data3['type'][i] == 'int':
        ##intermediate
        #intMRg.append([mass, rad, z, gp])
    else:    
        #quiescent
        qMRg.append([mass, rad, z, gp])
    
#Deleting Initial Entries==============================                
qMRg = np.array(qMRg)
intMRg = np.array(intMRg)
sfMRg = np.array(sfMRg)
qMRf = np.array(qMRf)
sfMRf = np.array(sfMRf)
intMRf = np.array(intMRf)

#Converting to actual distance (converting an entire array is faster than converting each entry one by one) I do it here after converting the data to a numpy array, which supports column indexing.
#Adding log to the radius!
sfMRf[:, 1] = np.log10((sfMRf[:, 1]*u.arcsec).to(u.rad)*(Distance(z=sfMRf[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
qMRf[:, 1] = np.log10((qMRf[:, 1]*u.arcsec).to(u.rad)*(Distance(z=qMRf[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
#intMRf[:, 1] = np.log10((intMRf[:, 1]*u.arcsec).to(u.rad)*(Distance(z=intMRf[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
#intMRg[:, 1] = np.log10((intMRg[:, 1]*u.arcsec).to(u.rad)*(Distance(z=intMRg[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
sfMRg[:, 1] = np.log10((sfMRg[:, 1]*u.arcsec).to(u.rad)*(Distance(z=sfMRg[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
qMRg[:, 1] = np.log10((qMRg[:, 1]*u.arcsec).to(u.rad)*(Distance(z=qMRg[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
#PLOTING================================================================
xlim = [8.0, 12.0]
xp = np.linspace(xlim[0], xlim[1], 100)
#sffit = np.polyfit(sfxy[:, 0], sfxy[:, 1], 1, full=1)
#qfit = np.polyfit(qxy[:, 0], qxy[:, 1], 1, full=1)
#separline = [2.0, -(9.5*2.0)]

#lines = [np.array([[1.0, 9.0], [1.0, 9.5], [1.0, 10.0]]), np.array([[1.5, 8.5], [1.5, 9.0], [1.5, 9.5]]), np.array([[2.0, 8.5], [2.0, 9.0]])]#, np.array([sffit[0], qfit[0], separline])]
lines = [np.array([[1.5, 8.5], [1.5, 9.0], [1.5, 9.5]])]
markers = ['-', '--', '-']
color = ['black', 'black', 'black']
linelabels = [r'Constant $\frac{M}{R_e}$', r'Constant $\frac{M}{R_{e}^{1.5}}$', r'Constant $\frac{M}{R_{e}^{2}}$']


#ACTUAL PLOTTING================================================================================================================================
pl.close()    
fig, ax = pl.subplots(1, len(lines), figsize = (10, 6))
#fig.suptitle(r'$\log(R_e)$ vs. $\log(M)$  of  $0.8<z<1.0$  Galaxies', fontsize=20) 
fig.subplots_adjust(top=0.90, left=0.08, right=0.98)
msize = 6.0
for i in range(len(lines)):
    #ax.plot(sfMRf[:, 0], sfMRf[:, 1], 'o', fillstyle='none', color='blue', ms=1.0, label=str(len(sfMRf)) + ' star-forming field')    
    ax.plot(sfMRg[:, 0], sfMRg[:, 1], 'o', fillstyle='full', color='blue', ms=msize, label=str(len(sfMRg)) +' star-forming group')  
    ##ax.plot(intMRg[:, 0], intMRg[:, 1], 'o', fillstyle='none', color='green', ms=msize, label=str(len(intMRg)) +' intermediate group')
    #ax.plot(qMRf[:, 0], qMRf[:, 1], 'o', fillstyle='none', color='red', ms=1.0, label=str(len(qMRf)) + ' quiescent field')
    ax.plot(qMRg[:, 0], qMRg[:, 1], 'o', fillstyle='full', color='red', ms=msize, label=str(len(qMRg)) + ' quiescent group')     
    #ax.plot(intMRf[:, 0], intMRf[:, 1], 'o', fillstyle='full', color='green', ms=3.5, label=str(len(intMRf)) +' intermediate field')
  
    #for j in range(len(lines[i])):
       # ax.plot(xp, (lines[i][j][0])**(-1)*(xp-lines[i][j][1]), markers[i], color=color[i], lw=1.0)
    
    
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_ylim(0.0, 4.0)

    #ax.set_title(linelabels[i], fontsize=16)
    
    ax.set_xlabel(r'$\log(M \, (M_{\odot}))$')
    ax.set_ylabel(r'$\log(R_e \, (kpc))$')
    
    legend = ax.legend(loc='upper right')
            





