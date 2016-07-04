#Field Catalogue========================================================
catname1 = 'ultravista'
magcol1 = 'Ks_tot'
zcol1 = 'zp'
typecol1 = 'Class'
columns1 = [magcol1, zcol1, typecol1]

zrange1 = []

typerequirement = 'all'
#Radius Catalogue=============a=========================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'morph_zurich'
radcol2 = 'R_GIM2D'
magcol2 = 'ACS_MAG_AUTO'
columns2 = [radcol2, magcol2]

#===================================================================
cat1 = catalogues[catname1]
cat2 = catalogues[catname2]
mat1 = cat1[catname2+'_match']

#Analysis
gen = genentries(catname2, columns2, catname2, columns2)
#tempqarray = np.empty([1, 2])
    #if groupprob is None:
        #for i in gen:
            #mass = cat['log10_M'][i]
            ##rawarad is the radius in arcsec
            #rawrad = morph_zurich['R_GIM2D'][mat[i]]
            #z = cat['zp'][i]
            #rad = np.log10((rawrad*u.arcsec).to(u.rad)*(Distance(z=z, cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
            #Type = cat['Class'][i]
            #if Type == 'sf':
                #tempsfarray = np.concatenate((tempsfarray, [[mass, rad]]))
radmag = np.empty([1, 2])                
for i in gen:
    radmag = np.concatenate((radmag, [[cat2[radcol2][i], cat2[magcol2][i]]]))
radmag = np.delete(radmag, 0, axis=0)

#ax[i].plot(sfxyg[:, 0], sfxyg[:, 1], 'o', fillstyle='full', color='blue', label='star-forming group')    
fig = pl.figure()
ax = pl.subplot(1, 1, 1)
ax.plot(radmag[:, 0], radmag[:, 1], 'o', ls='None')

ax.set_xlabel(r'$R_{GIM2D}$')
ax.set_ylabel(r'$m_{ACS}$')

ax.set_ylim(12.0, 26.0)

ax.set_title(r'ACS I-Band Magnitude vs. $R_{GIM2D}$')