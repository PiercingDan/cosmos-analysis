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
colnames3 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp', 'gp': 'zp_prob', 'gd': 'groupdist', 'gr': 'R200'}
colnameslist3 = list(colnames3.values())
data3 = {namekey: np.array(catalogues[catname3][namevalue]) for namekey, namevalue in colnames3.items()}
zrange3 = zrange1 
R200 = True

#Importing the matching arrays
mat1 = np.array(catalogues[catname1][catname2+'_match'])
mat3 = np.array(catalogues[catname3][catname2+'_match'])

#2 represents two options: group or field DELETE INITIAL ENTRIES
qMRg, sfMRg, qMRf, sfMRf = [], [], [], []

#Creating Generators

cat1gen = genentries(catname1, colnameslist1, catname2, colnameslist2, zcol=colnames1['z'], zrange=zrange1)
#Applying R200 cut: only groups with a groupdist within R200 limit will count
if R200 == True:
    cat3gen = (i for i in genentries(catname3, colnameslist3, catname2, colnameslist2, zcol=colnames3['z'], zrange=zrange3) if data3['gd'][i] < data3['gr'][i])#
    GroupLabel = r'within $R_{200}$'
else:   
    cat3gen = genentries(catname3, colnameslist3, catname2, colnameslist2, zcol=colnames3['z'], zrange=zrange3)
    GroupLabel = ''    

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
#Adding log to the radius!
sfMRf[:, 1] = np.log10((sfMRf[:, 1]*u.arcsec).to(u.rad)*(Distance(z=sfMRf[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
qMRf[:, 1] = np.log10((qMRf[:, 1]*u.arcsec).to(u.rad)*(Distance(z=qMRf[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
sfMRg[:, 1] = np.log10((sfMRg[:, 1]*u.arcsec).to(u.rad)*(Distance(z=sfMRg[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
qMRg[:, 1] = np.log10((qMRg[:, 1]*u.arcsec).to(u.rad)*(Distance(z=qMRg[:, 2], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))

#Creating Total Entries==============================================
allMRg = np.vstack((qMRg, sfMRg))
allMRf = np.vstack((qMRf, sfMRf)) 
    
#bin edges
xedges = np.linspace(8.0, 12.0, 31)
yedges = np.linspace(0.0, 2.5, 19)
    
#For Field
#For Field Quiescent REMEMBER, funny np.histogram2d notation yvalues first!
qHf, yedges, xedges = np.histogram2d(qMRf[:, 1], qMRf[:, 0], bins=(yedges, xedges)) 
#For Field All
allHf, yedges, xedges = np.histogram2d(allMRf[:, 1], allMRf[:, 0], bins=(yedges, xedges)) 
#======================================================================
#For Group
#For Group Quiescent
qHg, yedges, xedges = np.histogram2d(qMRg[:, 1], qMRg[:, 0], bins=(yedges, xedges), weights=qMRg[:, 3]) 
#For Group All
allHg, yedges, xedges = np.histogram2d(allMRg[:, 1], allMRg[:, 0], bins=(yedges, xedges), weights=allMRg[:, 3]) 

#Quiescent fraction
qfracHg = qHg/allHg
qfracHf = qHf/allHf
qfd = qfracHg -qfracHf
qfe = (qfracHg-qfracHf)/(1-qfracHf)

#PLOTTING================================================================
#========================================================================

xlim = [9.0, 11.5]
ylim = [0.0, 2.0]

pl.close()
fig, ax = plt.subplots(1, 2, figsize=(20, 6))
fig.subplots_adjust(left=0.06, right=1.00, wspace=0.10)
#fig.suptitle(str(len(allMRf))+' Field Galaxies  '+str(len(allMRg))+' Group Galaxies '+GroupLabel)
    
#Adjusting colorbar
# define the colormap
cmap = pl.cm.jet
# extract all colors from the .jet map
cmaplist = [cmap(i) for i in range(cmap.N)]
# force the first color entry to be grey
cmaplist[0] = (.5,.5,.5,1.0)
# create the new map
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

# define the bins and normalize
bounds0 = [-1.0, -0.3, -0.2 ,-0.1 ,0.0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8]
norm0 = mpl.colors.BoundaryNorm(bounds0, cmap.N)

bounds1 = [-24.0, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]
norm1 = mpl.colors.BoundaryNorm(bounds1, cmap.N)
#Field==============================================================
#bounds0 = np.linspace(0.0, 1.0, 11)
#norm0 = mpl.colors.BoundaryNorm(bounds0, cmap.N)

xcenters = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
ycenters = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
im = ax[0].contourf(xcenters, ycenters, qfd, 20, levels=bounds0, norm=norm0, alpha=1.0, cmap=pl.cm.jet)
ax[0].contour(xcenters, ycenters, qfd, levels=bounds0, colors='black', linestyles='-', lw=0.5)

ax[0].set_xlim(xlim)
ax[0].set_ylim(ylim)

ax[0].set_xlabel(r'$\log(M \, (M_{\odot}))$')
ax[0].set_ylabel(r'$\log(R_e \, (kpc))$')
#ax[0].set_title(r'$QF_{Group} - QF_{Field}$', fontsize=16)
legend = ax[0].legend(loc='upper right')
cbar0=pl.colorbar(im, ax=ax[0])
cbar0.set_ticks(bounds0)
cbar0.set_ticklabels(bounds0)

##Lines 
#lines = np.array([[1.5, 9.0]])
#xp = np.linspace(8.0, 12.0, 100)
#for i in range(len(lines)):
    #ax[0].plot(xp, lines[i][0]**(-1)*(xp-lines[i][1]), '-', color='black', lw=2.0)

#Group==============================================================
im = ax[1].contourf(xcenters, ycenters, qfe, 20, levels=bounds1, norm=norm1, cmap=pl.cm.jet)
ax[1].contour(xcenters, ycenters, qfe, levels=bounds1, colors='black', linestyles='-', lw=0.5)

ax[1].set_xlim(xlim)
ax[1].set_ylim(ylim)

ax[1].set_xlabel(r'$\log(M \, (M_{\odot}))$')
ax[1].set_ylabel(r'$\log(R_e \, (kpc))$')
#ax[1].set_title(r'$\frac{QF_{Group} - QF_{Field}}{1 - QF_{Field}}$', fontsize=16)
#ax[1].set_title(r'Quenching Efficiency', fontsize=16)
legend = ax[1].legend(loc='upper right')
cbar1 = pl.colorbar(im, ax=ax[1])
cbar1.set_ticks(bounds1)
cbar1.set_ticklabels(bounds1)