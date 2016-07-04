Hists = pl.figure()
ax = pl.subplot(1, 1, 1)
n, bins, patches = pl.hist(tempmatch[1].to(u.arcsec), normed=0, bins=np.linspace(0.0, 15.0, 51), histtype='bar')
pl.xlabel("Distance in 2D to closest match in Zurich Catalog (arcsec)")
pl.ylabel("Frequency")  
ax.set_title('Ultravista Matching Distance Histogram')