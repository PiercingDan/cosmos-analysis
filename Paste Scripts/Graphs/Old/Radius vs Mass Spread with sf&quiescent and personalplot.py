##Field Catalogue========================================================
#catname1 = 'ultravista'
#masscol1 = 'log10_M'
#typecol1 = 'Class'
#zcol1 = 'zp'
#columns1 = [masscol1, typecol1, zcol1]

#zrange1 = [0.8, 1.0]

##Radius Catalogue======================================================
##Conversion is 1.0, since it is already in arssecs
#catname2 = 'morph_zurich'
#radcol2 = 'R_GIM2D'
#columns2 = [radcol2]

##Group Catalogue=======================================================
#catname3 = 'balogh_data2'
#masscol3 = 'log10_M'
#typecol3 = 'Class'
#groupprobcol3 = 'zp_prob'
#zcol3 = 'zp'
#columns3 = [masscol3, typecol3, groupprobcol3, zcol3]

#zrange3 = [0.8, 1.0]  

##to shorten names
#cat1 = catalogues[catname1]
#cat2 = catalogues[catname2]
#cat3 = catalogues[catname3]

#mat1 = cat1[catname2+'_match']
#mat3 = cat3[catname2+'_match']

##group star forming
#sfxyg = np.empty([1, 2])
##group quiescent
#qxyg = np.empty([1, 2])
##field star forming
#sfxyf = np.empty([1, 2])
##field quiescent
#qxyf = np.empty([1, 2])

##xvalue
##def rad (arcsec): 
    ##return np.log(catalogues[cat2][col2][mat2[0][0][i]]*u.arcsec).to(u.rad)*(Distance(z=catalogues[cat1][zcol][i], cosmology=cosmology.WMAP9)).to(u.kpc))/(u.kpc*u.rad)

#cat1gen = genentries(catname1, columns1, catname2, columns2, zcol1, zrange1)
#cat3gen = genentries(catname3, columns3, catname2, columns2, zcol3, zrange3)

##Cat1 - Field
#for i in cat1gen:
    #rad = np.log10((cat2[radcol2][mat1[i]]*u.arcsec).to(u.rad)*(Distance(z=cat1[zcol1][i], cosmology=cosmology.WMAP9)).to(u.kpc)/(u.rad*u.kpc))
    #mass = cat1[masscol1][i]
    
    #if cat1[typecol1][i] == 'sf':
        #sfxyf = np.concatenate((sfxyf, [[mass, rad]]))
    #else:    
        #qxyf = np.concatenate((qxyf, [[mass, rad]]))
        
##Cat3 - Group
#for i in cat3gen:
    #rad = np.log10((cat2[radcol2][mat3[i]]*u.arcsec).to(u.rad)*(Distance(z=cat3[zcol3][i], cosmology=cosmology.WMAP9)).to(u.kpc)/(u.rad*u.kpc))
    #mass = cat3[masscol3][i]
    ##If it 100% a group
    #if cat3[groupprobcol3][i] == 1.0:
        #if cat3[typecol3][i] == 'sf':
            #sfxyg = np.concatenate((sfxyg, [[mass, rad]]))
        #else:    
            #qxyg = np.concatenate((qxyg, [[mass, rad]]))
        
##deleting placeholders       
#sfxyf = np.delete(sfxyf, 0, axis=0)
#qxyf = np.delete(qxyf, 0, axis=0)
#sfxyg = np.delete(sfxyg, 0, axis=0)
#qxyg = np.delete(qxyg, 0, axis=0)


#Setting data
sfxyf = ultravistamassrad[0]
qxyf = ultravistamassrad[1]
sfxyg = balogh2massrad[0]
qxyg = balogh2massrad[1]

#PLOTING================================================================
xlim = [9.0, 12.0]
xp = np.linspace(xlim[0], xlim[1], 100)
#sffit = np.polyfit(sfxy[:, 0], sfxy[:, 1], 1, full=1)
#qfit = np.polyfit(qxy[:, 0], qxy[:, 1], 1, full=1)
#separline = [2.0, -(9.5*2.0)]

lines = [np.array([[1.0, 9.0], [1.0, 9.5], [1.0, 10.0]]), np.array([[1.5, 8.5], [1.5, 9.0], [1.5, 9.5]]), np.array([[2.0, 8.5], [2.0, 9.0]])]#, np.array([sffit[0], qfit[0], separline])]
markers = ['-', '-', '-']
color = ['black', 'black', 'black']
linelabels = [r'Constant $\frac{M}{R_e}$', r'Constant $\frac{M}{R_{e}^{1.5}}$', r'Constant $\frac{M}{R_{e}^{2}}$']

#=======================================================================


#ACTUAL PLOTTING================================================================================================================================
#pl.close()    
fig, ax = pl.subplots(1, len(lines), figsize = (23, 6))
fig.suptitle(r'$\log(R_e)$ vs. $\log(M)$  of  $0.8<z<1.0$  Galaxies', fontsize=20) 
fig.subplots_adjust(top=0.85, left=0.05, right=0.98)
for i in range(len(lines)):
    ax[i].plot(sfxyf[:, 0], sfxyf[:, 1], 'o', fillstyle='none', color='blue', label='star-forming field')    
    ax[i].plot(qxyf[:, 0], qxyf[:, 1], 'o', fillstyle='none', color='red', label='quiescent field')   
    ax[i].plot(sfxyg[:, 0], sfxyg[:, 1], 'o', fillstyle='full', color='blue', label='star-forming group')    
    ax[i].plot(qxyg[:, 0], qxyg[:, 1], 'o', fillstyle='full', color='red', label='quiescent group')       
  
    for j in range(len(lines[i])):
        ax[i].plot(xp, (lines[i][j][0])**(-1)*(xp-lines[i][j][1]), markers[i], color=color[i], lw=1.5)
    
    
    ax[i].set_xlim(xlim[0], xlim[1])
    ax[i].set_ylim(0.0, 4.0)

    ax[i].set_title(linelabels[i], fontsize=16)
    
    ax[i].set_xlabel(r'$\log(M \, (M_{\odot}))$')
    ax[i].set_ylabel(r'$\log(R_e \, (kpc))$')
    
    legend = ax[i].legend(loc='upper right')
            





