   
#bin edges
xedges = np.linspace(8.0, 12.0, 31)
yedges = np.linspace(0.0, 2.5, 19)
    
#For Field All
allHf, yedges, xedges = np.histogram2d(np.log10(alldataf['radius']), alldataf['mass'], bins=(yedges, xedges)) 
#======================================================================
#For Group All
allHg, yedges, xedges = np.histogram2d(np.log10(alldatag['radius']), alldatag['mass'], bins=(yedges, xedges), weights=alldatag['gp'])


#PLOTTING================================================================
#pl.close()
fig, ax = plt.subplots(1, 2, figsize=(23, 5))

#Field==============================================================
im=mpl.image.NonUniformImage(ax[0], interpolation='nearest', label=str(len(alldataf['radius']))+' Field')
xcenters = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
ycenters = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
im.set_data(xcenters, ycenters, allHf)
ax[0].images.append(im)
ax[0].set_xlim(xedges[0], xedges[-1])
ax[0].set_ylim(yedges[0], yedges[-1])
ax[0].set_aspect('equal')

ax[0].set_xlabel(r'$\log(M \, (M_{\odot}))$')
ax[0].set_ylabel(r'$\log(R_e \, (kpc))$')
ax[0].set_title('Frequency of ' + str(len(alldataf['radius'])) + ' Field Galaxies')
legend = ax[0].legend(loc='upper right')
pl.colorbar(im, ax=ax[0])
    
#Lines 
#lines = np.array([[1.5, 8.5], [1.5, 9.0], [1.5, 9.5]])
#xp = np.linspace(8.0, 12.0, 100)
#for i in range(len(lines)):
    #ax[0].plot(xp, lines[i][0]**(-1)*(xp-lines[i][1]), '-', color='black', lw=2.0)

#Group==============================================================
im=mpl.image.NonUniformImage(ax[1], interpolation='nearest', label=str(len(alldatag['radius']))+' Group')
xcenters = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
ycenters = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
im.set_data(xcenters, ycenters, allHg)
ax[1].images.append(im)
ax[1].set_xlim(xedges[0], xedges[-1])
ax[1].set_ylim(yedges[0], yedges[-1])
ax[1].set_aspect('equal')
ax[1].set_title(r'Frequency of ' + str(len(alldatag['radius'])) + ' Group Galaxies ')
ax[1].set_xlabel(r'$\log(M \, (M_{\odot}))$')
ax[1].set_ylabel(r'$\log(R_e \, (kpc))$')
legend = ax[1].legend(loc='upper right')
pl.colorbar(im, ax=ax[1])
    