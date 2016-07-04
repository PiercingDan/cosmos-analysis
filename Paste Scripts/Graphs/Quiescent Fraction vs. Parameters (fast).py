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

#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'morph_zurich'
colnames2 = {'radius': 'R_GIM2D', 'GG': 'GG', 'M20': 'M20', 'CC': 'CC', 'AA': 'AA'}
colnameslist2 = list(colnames2.values())
data2 = {namekey: np.array(catalogues[catname2][namevalue]) for namekey, namevalue in colnames2.items()}
#IMPORTANT, CHANGE BELOW AS NECESSARY
radcol2convert = 1.0
data2['radius'] = radcol2convert*data2['radius']

#Group Catalogue=======================================================
catname3 = 'balogh_data2'
colnames3 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp', 'gp': 'zp_prob', 'gd': 'groupdist', 'gr': 'R200'}
colnameslist3 = list(colnames3.values())
data3 = {namekey: np.array(catalogues[catname3][namevalue]) for namekey, namevalue in colnames3.items()}
zrange3 = zrange1 

#Importing the matching arrays
mat1 = np.array(catalogues[catname1][catname2+'_match'])
mat3 = np.array(catalogues[catname3][catname2+'_match'])

#Binwidth Definition, N is number of point (Number of bins +1), position corresponds to different radfactor 
xlim = np.array([[9.0, 11.5], [8.5, 10.5], [8.0, 10.0], [7.0, 9.5], [7.0, 9.5]])
N = np.array([12, 12, 12, 12, 12], dtype=int)
bins = [np.linspace(xlim[i][0], xlim[i][1], N[i]+1, endpoint=True) for i in range(len(parameters))]
          
#2 represents two options: group or field DELETE INITIAL ENTRIES
qMRg, sfMRg, qMRf, sfMRf = [], [], [], []
#Creating all arrays=================================================

#N represents total number of bins   
allbing = [np.zeros(i) for i in N] 
allbinf = [np.zeros(i) for i in N] 
qbing = [np.zeros(i) for i in N]
qbinf = [np.zeros(i) for i in N]
#Creating Generators

cat1gen = genentries(catname1, colnameslist1, catname2, colnameslist2, zcol=colnames1['z'], zrange=zrange1)
#Applying R200 cut: only groups with a groupdist within R200 limit will count
cat3gen = (i for i in genentries(catname3, colnameslist3, catname2, colnameslist2, zcol=colnames3['z'], zrange=zrange3) if data3['gd'][i] < data3['gr'][i])#

#Adding Entries
#Field================================================================
for i in cat1gen:
    #defining radius, logmass
    mass = data1['mass'][i]
    rad = data2['radius'][mat1[i]]
    z = data1['z'][i]
    GG = data2['GG'][mat1[i]]
    M20 = data2['M20'][mat1[i]]
    CC = data2['CC'][mat1[i]]
    AA = data2['AA'][mat1[i]]
    if data1['type'][i] == 'sf':
        #starforming
        sfMRf.append([mass, GG, M20, CC, AA])
    else:    
        #quiescent
        qMRf.append([mass, GG, M20, CC, AA])
        
#Group================================================================
for i in cat3gen:
    #defining radius, logmass, GROUP PROBABILITY (gp)
    mass = data3['mass'][i]
    rad = data2['radius'][mat3[i]]
    gp = data3['gp'][i]
    z = data3['z'][i]
    GG = data2['GG'][mat3[i]]
    M20 = data2['M20'][mat3[i]]
    CC = data2['CC'][mat3[i]]
    AA = data2['AA'][mat3[i]]    
    if data3['type'][i] == 'sf':
        #starforming
        sfMRg.append([mass, GG, M20, CC, AA, gp])
    else:    
        #quiescent
        qMRg.append([mass, GG, M20, CC, AA, gp])
    
#Deleting Initial Entries==============================                
qMRg = np.recarray(qMRg, format=['f8', 'f8', 'f8','f8','f8'], names=('mass', 'GG', 'M20', 'CC', 'AA'))
sfMRg = np.array(sfMRg)
qMRf = np.array(qMRf)
sfMRf = np.array(sfMRf)

#Creating Total Entries==============================================
allMRg = np.vstack((qMRg, sfMRg))
allMRf = np.vstack((qMRf, sfMRf)) 

parameters = [0, 1, 2, 3, 4]
#HISTOGRAM ANALYSIS============================                           
for i in range(len(parameters)):
    j = parameters[i]
    #group
    allbing[i], bins[i] = np.histogram(allMRg[:, j], bins=bins[i], weights=allMRg[:, -1])
    qbing[i], bins[i] = np.histogram(qMRg[:, j], bins=bins[i], weights=qMRg[:, -1]) 
    #field                               
    allbinf[i], bins[i] = np.histogram(allMRf[:, j], bins=bins[i])
    qbinf[i], bins[i] = np.histogram(qMRf[:, j], bins=bins[i])
                    
#pl.close()   

fig, ax = pl.subplots(1, len(radfactor), figsize = (23, 6))# sharey=True)
fig.suptitle(r'Quiescent Fraction vs. ' + ', '.join(parameters) + str(zrange1[0]) + '$ \leq z \leq $' + str(zrange1[1]), fontsize=16)
fig.subplots_adjust(left=0.04, right=0.98)

for i in range(len(parameters)):
    x = 0.5*(bins[i][:-1] + bins[i][1:])
    ax[i].plot(x, qbing[i]/allbing[i], color='black', linestyle='-', marker='o',  markerfacecolor='black', markeredgecolor='black', label=str(allMRg.shape[0])+r' Groups within $R_{200}$')

    ax[i].plot(x, qbinf[i]/allbinf[i], color='red', linestyle='--', marker='o',  markerfacecolor='none', markeredgecolor='red', label=str(allMRf.shape[0])+' Fields')

   
    ax[i].set_xlabel(r'$\log(M/R_e^{{%s}}\, M_*/kpc)$' % (radfactor[i]))
    
    ax[i].set_ylabel(r'Quiescent Fraction')
    
    ax[i].set_xlim(bins[i][0], bins[i][-1])
    ax[i].set_ylim(0.0, 1.1)
    
    ax[i].set_yticks(np.linspace(0.0, 1.0, 11, endpoint=True))
    
    legend = ax[i].legend(loc='upper left')
    
    legend.draw_frame(False)

