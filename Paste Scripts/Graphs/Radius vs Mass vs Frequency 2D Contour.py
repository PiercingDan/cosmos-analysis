   
#bin edges
xedges = np.linspace(9.5, 12.0, 31)
yedges = np.linspace(0.0, 2.5, 19)
    
#Cutting Field Galaxies at M=10^9.5 to match galaxy cut    
index = alldataf['mass']>=9.5
    
#For Field All
allHf, yedges, xedges = np.histogram2d(np.log10(alldataf['radius'][index]), alldataf['mass'][index], bins=(yedges, xedges)) 
#======================================================================
#For Group All
allHg, yedges, xedges = np.histogram2d(np.log10(alldatag['radius']), alldatag['mass'], bins=(yedges, xedges), weights=alldatag['gp'])

#PLOTTING================================================================
#pl.close()
fig, ax = plt.subplots(1, 2, figsize=(20, 6))
fig.subplots_adjust(left=0.06, right=1.00, wspace=0.10)

xcenters = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
ycenters = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
im = ax[0].contourf(xcenters, ycenters, allHf, 10, alpha=1.0, cmap=pl.cm.jet)
ax[0].contour(xcenters, ycenters, allHf, 10, colors='black', lw=0.5)

ax[0].set_xlim(xedges[0], xedges[-1])
ax[0].set_ylim(yedges[0], yedges[-1])

ax[0].set_xlabel(r'$\log(M \, (M_{\odot}))$')
ax[0].set_ylabel(r'$\log(R_e \, (kpc))$')
#ax[0].set_title('Frequency of ' + str(len(alldataf['radius'])) + ' Field Galaxies')
legend = ax[0].legend(loc='upper right')
cbar0 = pl.colorbar(im, ax=ax[0])
    
##Lines 
#lines = np.array([[1.5, 10.5]])
#xp = np.linspace(8.0, 12.0, 100)
#for i in range(len(lines)):
    #ax[0].plot(xp, lines[i][0]**(-1)*(xp-lines[i][1]), '--', color='black', lw=2.0)

#Group==============================================================
im = ax[1].contourf(xcenters, ycenters, allHg, 10, alpha=1.0, cmap=pl.cm.jet)
ax[1].contour(xcenters, ycenters, allHg, 5, colors='black', lw=0.5)

ax[1].set_xlim(xedges[0], xedges[-1])
ax[1].set_ylim(yedges[0], yedges[-1])

ax[1].set_xlabel(r'$\log(M \, (M_{\odot}))$')
ax[1].set_ylabel(r'$\log(R_e \, (kpc))$')
#ax[1].set_title(r'Frequency of ' + str(len(alldatag['radius'])) + ' Group Galaxies ')
legend = ax[1].legend(loc='upper right')
cbar0 = pl.colorbar(im, ax=ax[1])
    
    