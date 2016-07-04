#Field Catalogue========================================================
catname1 = 'geec2'
masscol1 = 'log10_M'
zcol1 = 'zp'
typecol1 = 'Class'
columns1 = []

zrange1 = [0.8, 1.0]

typerequirement = 'q'
#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'balogh_data1'
radcol2 = 'R_GIM2D'
columns2 = []

#=====================================================================
cat1 = catalogues[catname1]
cat2 = catalogues[catname2]
#======================================================================
#RADEC = np.empty([1, 2])
#for i in genentries(catname1, [], catname2, []):
    #RADEC = np.concatenate((RADEC, [[cat1['RA'][i], cat1['DEC'][i]]]))
#RADEC = np.delete(RADEC, 0, axis=0) 

#PLOTTING==============================================================    
pl.close()
fig = pl.figure()
ax = pl.subplot(1, 1, 1)

    

#All Ultravista points
ax.plot(cat2['RA'], cat2['DEC'], marker='o', color='red', label=catname2, ls='None')
ax.plot(cat1['RA'], cat1['DEC'], marker='o', color='blue', label=catname1, ls='None')
#All Zurich points

#ax.plot(RADEC[:, 0], RADEC[:, 1], color='green', marker='o', mfc='green', label='Good Ultravista and Good Zurich and Good Match', fillstyle='none', ls='None')   

ax.set_ylim(1.4, 3.4)
ax.set_xlim(149.2, 151.2)
legend = ax.legend(loc='upper right')
legend.draw_frame(False)



#All common points, d2d<1.0 arcsec