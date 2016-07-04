#xMvalues
cat1 = 'balogh_data'
col1 = 'log10_M'

cat2 = 'morph_zurich'
col2 = 'R_GIM2D'
matchcol = 'morph_zurich_match'

typecol = 'Class'
typecolentries = ['sf', 'int', 'p']
groupcol = 'group_ID'
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

#sf will be 100%, q is everything else
#x is col1, y is col2

# Figure out good way to arrange x, y pairs, placeholders

sfxy = np.empty([1, 2])
qxy = np.empty([1, 2])
#xvalue
#def rad (arcsec): 
    #return np.log(catalogues[cat2][col2][mat2[0][0][i]]*u.arcsec).to(u.rad)*(Distance(z=catalogues[cat1][zcol][i], cosmology=cosmology.WMAP9)).to(u.kpc))/(u.kpc*u.rad)

gen = genentries()
for i in gen:
    rad = np.log10((catalogues[cat2][col2][mat2[0][0][i]]*u.arcsec).to(u.rad)*(Distance(z=catalogues[cat1][zcol][i], cosmology=cosmology.WMAP9)).to(u.kpc)/(u.rad*u.kpc))
    mass = catalogues[cat1][col1][i]
    
    if catalogues[cat1][typecol][i] == 'sf':
        sfxy = np.concatenate((sfxy, [[mass, rad]]))
    else:    
        qxy = np.concatenate((qxy, [[mass, rad]]))
        
#deleting placeholders       
sfxy = np.delete(sfxy, 0, axis=0)
qxy = np.delete(qxy, 0, axis=0)


#plot lines of best fit, inferred, 1.5, surface density
xlim = [9.0, 12.0]
xp = np.linspace(xlim[0], xlim[1], 100)
sffit = np.polyfit(sfxy[:, 0], sfxy[:, 1], 1, full=1)
qfit = np.polyfit(qxy[:, 0], qxy[:, 1], 1, full=1)
separline = [2.0, -(9.5*2.0)]

lines = [np.array([[1.0, 7.5], [1.0, 8.0], [1.0, 8.5]]), np.array([[1.5, 6.0], [1.5, 6.75], [1.5, 7.5]]), np.array([[2.0, 4.5], [2.0, 5.5], [2.0, 6.5]]), np.array([sffit[0], qfit[0], separline])]

#Regular Plots
markers = ['-', '-', '-']
color = ['black', 'black', 'black']
linelabels = [r'Constant $\frac{M}{R_e}$', r'Constant $\frac{M}{R_{e}^{1.5}}$', r'Constant $\frac{M}{R_{e}^{2}}$']

#My Plot np.around(line[0][0], decimals=4)
mycolor = ['black', 'black', 'cyan']
mymarkers = ['-', '--', '-']
mylinelabels = ['sf: n = ' + str(np.around(sffit[0][0]**(-1), decimals=4)) + ', xint = ' +str (np.around(-sffit[0][1]/sffit[0][0], decimals=4)),\
                'q: n = ' + str(np.around(qfit[0][0]**(-1), decimals=4)) + ', xint = ' +str (np.around(-qfit[0][1]/qfit[0][0], decimals=4)),\
                'separation: n = ' + str(np.around(separline[0]**(-1), decimals=4)) + ', xint = ' +str(np.around(-separline[1]/ separline[0], decimals=4))]


pl.close()    
fig1, ax1 = pl.subplots(1, len(lines))
fig1.suptitle('$\log(R_e)$ vs. $\log(M)$  of  $0.8<z<1.0$  Galaxies', fontsize=20) 
fig1.subplots_adjust(top=0.85, left=0.05, right=0.98)

for i in range(len(lines)):
    ax1[i].plot(sfxy[:, 0], sfxy[:, 1], 'o', color='blue')# label=' starforming')    
    ax1[i].plot(qxy[:, 0], qxy[:, 1], 'o', color='red')#, label='quiescent')   
  
    #plotting regular plots
    if i != 3:
        for j in range(len(lines[i])):
            ax1[i].plot(xp, (lines[i][j][0])**(-1)*(xp-lines[i][j][1]), markers[i], color=color[i], lw=1.5)
            ax1[i].set_xlim(xlim[0], xlim[1])
            ax1[i].set_title(linelabels[i], fontsize=16)
            ax1[i].set_xlabel(r'$\log(M\: (M_{\odot}))$')
            ax1[i].set_ylabel('$\log(R_e\: (kpc))$')
            legend = ax1[i].legend(loc='upper right', fontsize=10)
    #plotting my fits    
    else:
        for j in range(len(lines[i])):    
            ax1[i].plot(xp, (lines[i][j][0])*xp+lines[i][j][1], mymarkers[j], color=mycolor[j], lw=2.0, label=mylinelabels[j])
            
            ax1[i].set_xlim(xlim[0], xlim[1])
            ax1[i].set_ylim(0.0, 4.5)
            legend = ax1[i].legend(loc='upper right', fontsize=10)
            
            






