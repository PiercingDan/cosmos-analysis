#convert is converting between pixels and arcsecs, if the original data is in arcsecs then convert = 1.0
#xvalues
cat1 = 'morph_zurich'
xvalues = []
ycol1 = 'R_GIM2D'
yconvert1 = 1.0
xcol1 = 'ACS_MAG_AUTO'
xtrack = []

#yvalues
cat2 = 'griffith'
yvalues = []
xcol2 = 'MU_HI'
ycol2 = 'RE_GALFIT_HI'

yconvert2 = 0.05

#Importing data for efficiency
mat1 = np.array(catalogues[cat1][cat2+'_match'])
ydata1 = np.log(np.array(catalogues[cat1][ycol1])*yconvert1)
ydata2 = np.log(np.array(catalogues[cat2][ycol2])*yconvert2)
xdata2 = np.array(catalogues[cat2][xcol2])
xdata1 = np.array(catalogues[cat1][xcol1])

gen = genentries(cat1, [ycol1], cat2, [ycol2, xcol2])

for i in gen:
    xvalues.append(xdata2[mat1[i]])
    yvalues.append(ydata2[mat1[i]]-ydata1[i])
    #xvalues = np.append(xvalues, catalogues[cat1][xcol][i]) 
    #yvalues = np.append(yvalues, catalogues[cat2][ycol][mat1[i]])
    
#Convert to np array
xvalues = np.array(xvalues)
yvalues = np.array(yvalues)

fig = pl.figure(figsize=(14, 8))
ax = pl.subplot(1, 1, 1)
ax.plot(xvalues, yvalues, 'o', ms=0.5, label = str(len(xvalues)) +' entries')
#pl.ylabel('log ('+ ycol2 + ' / ' + ycol1 + ')', fontsize=14)
ax.set_ylabel(r'$\log (\frac{R_{GALFIT}}{R_{GIM2D}})$', fontsize=16)
ax.set_xlabel(xcol2, fontsize=14)
#ax.set_xlabel(r'$\mu$', fontsize=16)
pl.xlim(15.0, 30.0)
pl.ylim(-1.0, 4.0)
minorLocator = mpl.ticker.AutoMinorLocator()
ax.xaxis.set_minor_locator(minorLocator)
minorLocator = mpl.ticker.AutoMinorLocator()
ax.yaxis.set_minor_locator(minorLocator)

#lineofbestfit and plotting it
line = np.polyfit(xvalues, yvalues, 1, full=1)
myline = (1.0, 0.0)

xp = np.linspace(min(xvalues), max(xvalues), 100)

#represents 22.5 cut
xmag = 22.5*np.ones(100)
ymag = np.linspace(min(yvalues), max(yvalues), 100)

#pl.plot(xp, line[0][0]*xp+line[0][1], '-', color='green', lw = 3.0, 
        #label='Line of Best Fit: \n'+
        #'y = '+str(np.around(line[0][0], decimals=4))+'x + '+str(np.around(line[0][1], decimals=4)))

#pl.plot(xmag, ymag, '-', color='red', lw = 3.0, label='I = 22.5')

#pl.plot(xp, myline[0]*xp+myline[1], '-', color='red', lw = 2.0, 
        #label='My line: \n'+ 
        #'y = '+str(np.around(myline[0], decimals=4))+'x + '+str(np.around(myline[1], decimals=4)))

#subplot.set_title(cat2+' '+ycol+' vs. '+cat1+ ' ' +xcol)
legend=ax.legend(loc='upper left')
legend.draw_frame(False)
