#convert is converting between pixels and arcsecs, if the original data is in arcsecs then convert = 1.0

#xyvalues
catname1 = 'griffith'
colnames1 = {'radius': 'RE_GALFIT_HI', 'I-Band': 'MAG_BEST_HI', 'mu': 'MU_HI', 'z': 'Z'}
colnameslist1 = list(colnames1.values())
data1 = {namekey: np.array(catalogues[catname1][namevalue]) for namekey, namevalue in colnames1.items()}
#IMPORTANT, CHANGE BELOW AS NECESSARY
radcol1convert = 0.05
data1['radius'] = radcol1convert*data1['radius']

gen = genentries(catname1, colnameslist1)
array1 = []
#array 2 is our redshift range
array2= []


for i in gen:
    if data1['z'][i] >= 0.8 and data1['z'][i] <= 1.0:
        array2.append([data1['I-Band'][i], data1['radius'][i]])
    else:
        array1.append([data1['I-Band'][i], data1['radius'][i]])

#Convert to np array
array1 = np.array(array1)
array2 = np.array(array2)

#PLOTTING===============================================================
fig = pl.figure(figsize=(11, 11))
ax = pl.subplot(1, 1, 1)

ax.plot(array1[:, 0], array1[:, 1], 'o', color='black', fillstyle='none', ms=0.1)#, label = str(len(extendedxy)) +' extended entries')
ax.plot(array2[:, 0], array2[:, 1], 'o', color='red', fillstyle='none', ms=0.2)#, label = r'$0.8 \leq z \leq 1.0$')

ax.set_ylabel(colnames1['radius'])
ax.set_xlabel(colnames1['I-Band'])
ax.set_xlim(12.0, 26.0)

xp = np.linspace(23.618944, 26.0, 100)
yp = np.linspace(10**(-2), 10**2, 100)
yp2 = yp = np.linspace(0.03, 10**2, 100)
xp26 = 26 - 2.5*np.log10(2*np.pi*(yp**2))
xp18 = 18 - 2.5*np.log10(2*np.pi*(yp**2))

ax.plot(xp26, yp, '-', color='green', lw=1.5, label=r'$\mu = 26.0$')
ax.plot(xp18, yp, '-', color='purple', lw=1.5, label=r'$\mu = 18.0$')
ax.plot(xp, 0.03*np.ones(100), '--', color='purple', lw=1.5, label=r'$r_{e} = 0.03$')

minorLocator = mpl.ticker.AutoMinorLocator()

ax.xaxis.set_minor_locator(minorLocator)
ax.set_yscale('log')
ax.set_ylim(10**(-2), 10**2)
#pl.ylim(0.0, 4.0)

legend = ax.legend(loc='upper left')
legend.draw_frame(False)
#lineofbestfit and plotting it

#LINES of mu = 26 and mu = 18 and re = 0.03
