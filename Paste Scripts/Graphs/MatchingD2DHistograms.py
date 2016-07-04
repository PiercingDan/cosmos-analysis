catname1 = 'morph_zurich'
matcatname2 = 'griffith'

d2dvalues = np.array(catalogues[catname1][matcatname2+'_d2d'])

fig = pl.figure()
#Hists.subplots_adjust(left=0.07, bottom=0.10, right=0.95, top=0.90, wspace=0.32, hspace=0.32)
ax = pl.subplot(1, 1, 1)
bins = np.linspace(0.0, 5.0, 101)

n, bins, patches = pl.hist(d2dvalues, bins=bins)
ax.set_xlabel("Distance in 2D (arcsec)")
ax.set_xticks(np.linspace(0.0, 5.0, 11))
ax.set_ylabel("Frequency (out of) "+str(len(catalogues[catname1])))  
ax.set_title(catname2+' matched to '+catname1+' d2d Histogram')