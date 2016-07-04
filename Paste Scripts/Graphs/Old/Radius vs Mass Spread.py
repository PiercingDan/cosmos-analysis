#xMvalues
cat1 = 'balogh_data'
col1 = 'log10_M'

cat2 = 'morph_zurich'
col2 = 'R_GIM2D'
mat2 = balogh_data_match[cat2]

typecol = 'Class'
typecolentries = ['sf', 'int', 'p']
groupcol = 'Group_ID'
groupprobcol = 'zp_prob'
zcol = 'z'
zrange = [0.8, 1.0]  

#Generating index of non-masked Mvalues and within our redshift range
def genentries():
    for i in range(len(catalogues[cat1])):
        if catalogues[cat1][col1].mask[i] == False \
        and catalogues[cat1][typecol].mask[i] == False \
        and catalogues[cat1][zcol][i] >= zrange[0] \
        and catalogues[cat1][zcol][i] <= zrange[1] \
        and catalogues[cat2][col2][mat2[0][0][i]] != -999999.0 \
        and mat2[1][i] == 1 :
            yield i    

#Group will be 100%, field is everything else
#x is col1, y is col2

# Figure out good way to arrange x, y pairs, placeholders

groupxy = np.empty([1, 2])
fieldxy = np.empty([1, 2])
#xvalue
#def rad (arcsec): 
    #return np.log(catalogues[cat2][col2][mat2[0][0][i]]*u.arcsec).to(u.rad)*(Distance(z=catalogues[cat1][zcol][i], cosmology=cosmology.WMAP9)).to(u.kpc))/(u.kpc*u.rad)

gen = genentries()
for i in gen:
    rad = np.log10((catalogues[cat2][col2][mat2[0][0][i]]*u.arcsec).to(u.rad)*(Distance(z=catalogues[cat1][zcol][i], cosmology=cosmology.WMAP9)).to(u.kpc)/(u.rad*u.kpc))
    mass = catalogues[cat1][col1][i]
    
    if catalogues[cat1][groupcol].mask[i] == False and catalogues[cat1][groupprobcol][i] == 1.0:
        groupxy = np.concatenate((groupxy, [[mass, rad]]))
    else:    
        fieldxy = np.concatenate((fieldxy, [[mass, rad]]))
        
#deleting placeholders       
groupxy = np.delete(groupxy, 0, axis=0)
fieldxy = np.delete(fieldxy, 0, axis=0)


#plot lines of best fit, inferred, 1.5, surface density
xlim = [9.0, 12.0]
xp = np.linspace(xlim[0], xlim[1], 100)

lines = [np.array([[1.0, 7.5], [1.0, 8.0], [1.0, 8.5]]), np.array([[1.5, 6.0], [1.5, 6.75], [1.5, 7.5]]), np.array([[2.0, 4.5], [2.0, 5.5], [2.0, 6.5]])]

markers = ['-', '-', '-']
color = ['black', 'black', 'black']
linelabels = [r'Constant $\frac{M}{R_e}$', r'Constant $\frac{M}{R_{e}^{1.5}}$', r'Constant $\frac{M}{R_{e}^{2}}$']



pl.close()    
fig, ax = pl.subplots(1, len(lines))
fig.suptitle('$\log(R_e)$ vs. $\log(M)$  of  $0.8<z<1.0$  Galaxies', fontsize=20) 
fig.subplots_adjust(top=0.85, left=0.05, right=0.98)
for i in range(len(lines)):
    ax[i].plot(fieldxy[:, 0], fieldxy[:, 1], 'o', color='red', label='Field: All Others')   
    ax[i].plot(groupxy[:, 0], groupxy[:, 1], 'o', color='blue', label='Group: Prob=100%')
     
    for j in range(len(lines[i])):
        ax[i].plot(xp, (lines[i][j][0])**(-1)*(xp-lines[i][j][1]), markers[i], color=color[i], lw=1.5)
    
    ax[i].set_xlim(xlim[0], xlim[1])

    ax[i].set_title(linelabels[i], fontsize=16)
    ax[i].set_xlabel(r'$\log(M\: (M_{\odot}))$')
    ax[i].set_ylabel('$\log(R_e\: (kpc))$')
    
    legend = ax[i].legend(loc='upper right')
            





