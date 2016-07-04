#%%time
#Field Catalogue========================================================
catname1 = 'ultravista'
cat1 = catalogues[catname1]
colnames1 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp'}
colnameslist1 = list(colnames1.values())
#data1 = {namekey: np.array(catalogues[catname1][namevalue]) for namekey, namevalue in colnames1.items()}
zrange1 = [0.8, 1.0]

#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'griffith'
cat2 = catalogues[catname2]
colnames2 = {'radius': 'RE_GALFIT_HI', 'raderror': 'REERR_GALFIT_HI'}
colnameslist2 = list(colnames2.values())
#data2 = {namekey: np.array(catalogues[catname2][namevalue]) for namekey, namevalue in colnames2.items()}

#Group Catalogue=======================================================
catname3 = 'balogh_data2'
cat3 = catalogues[catname3]
colnames3 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp', 'gp': 'zp_prob', 'gd': 'groupdist', 'R200': 'R200'}
colnameslist3 = list(colnames3.values())
#data3 = {namekey: np.array(catalogues[catname3][namevalue]) for namekey, namevalue in colnames3.items()}
zrange3 = zrange1 

#catname3 = 'balogh_data2'
#colnames3 = {'mass': 'log10_M', 'type': 'Class', 'z': 'zp', 'gp': 'zp_prob', 'gd': 'groupdist', 'R200': 'R200'}
#colnameslist3 = list(colnames3.values())
##data3 = {namekey: np.array(catalogues[catname3][namevalue]) for namekey, namevalue in colnames3.items()}
#zrange3 = zrange1 

#Importing the matching arrays
mat1 = np.array(catalogues[catname1][catname2+'_match'])
mat3 = np.array(catalogues[catname3][catname2+'_match'])    

#Creating Generators
index1 = genindex(catname1, colnameslist1, catname2, colnameslist2, zcol=colnames1['z'], zrange=zrange1)

#Applying R200 cut: only groups with a groupdist within R200 limit will count
index3 = genindex(catname3, colnameslist3, catname2, colnameslist2, zcol=colnames3['z'], zrange=zrange3)# *(cat3[colnames3['gd']] < 0.5*cat3[colnames3['R200']])

#Adding the data and the matched data all at once        
alldatag = dict({namekey: np.array(catalogues[catname3][namevalue][index3]) for namekey, namevalue in colnames3.items()}, **{namekey: np.array(catalogues[catname2][namevalue][mat3[index3]]) for namekey, namevalue in colnames2.items()})
alldataf = dict({namekey: np.array(catalogues[catname1][namevalue][index1]) for namekey, namevalue in colnames1.items()}, **{namekey: np.array(catalogues[catname2][namevalue][mat1[index1]]) for namekey, namevalue in colnames2.items()})    
    
#Converting Radius(TAKES THE LONGEST)====================                
alldatag['radius'] = (alldatag['radius']*0.05*u.arcsec).to(u.rad)*(Distance(z=alldatag['z'], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 
alldatag['raderror'] = (alldatag['raderror']*0.05*u.arcsec).to(u.rad)*(Distance(z=alldatag['z'], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 
alldataf['radius'] = (alldataf['radius']*0.05*u.arcsec).to(u.rad)*(Distance(z=alldataf['z'], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 
alldataf['raderror'] = (alldataf['raderror']*0.05*u.arcsec).to(u.rad)*(Distance(z=alldataf['z'], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad) 

#