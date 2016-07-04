#convert is converting between pixels and arcsecs, if the original data is in arcsecs then convert = 1.0
#xvalues
cat1 = 'morph_zurich'
xvalues = []
xcol = 'R_GIM2D'
xconvert = 1.0
xtrack = []

#yvalues
cat2 = 'griffith'
yvalues = []
ycol = 'RE_GALFIT_HI'
yconvert = 0.05
ytrack = []

#Importing data for efficiency
mat1 = np.array(catalogues[cat1][cat2+'_match'])
xdata = np.array(catalogues[cat1][xcol])*xconvert
ydata = np.array(catalogues[cat2][ycol])*yconvert

gen = genentries(cat1, [xcol], cat2, [ycol])

for i in gen:
    xvalues.append(xdata[i])
    yvalues.append(ydata[mat1[i]])
    #xvalues = np.append(xvalues, catalogues[cat1][xcol][i]) 
    #yvalues = np.append(yvalues, catalogues[cat2][ycol][mat1[i]])
    
#Convert to np array
xvalues = np.array(xvalues)
yvalues = np.array(yvalues)

fig = pl.figure(figsize=(12, 8))
fig.subplots_adjust(top=0.95, bottom=0.09, left=0.07, right=0.95)
subplot = pl.subplot(1, 1, 1)
pl.plot(xvalues, yvalues, 'o', ms=0.3, label = str(len(xvalues)) +' entries')
pl.xlabel(xcol + ' (arcseconds)')
pl.ylabel(ycol + ' (arcseconds)')
pl.xlim(0.0, 2.0)
pl.ylim(0.0, 4.0)

#lineofbestfit and plotting it
line = (1.15, 0.0)
myline = (1.0, 0.0)

xp = np.linspace(min(xvalues), max(xvalues), 100)

pl.plot(xp, line[0]*xp+line[1], '--', color='green', lw = 1.5, 
        label=#'Line of Best Fit: \n'+
        'y = '+str(np.around(line[0], decimals=4))+'x + '+str(np.around(line[1], decimals=4)))

pl.plot(xp, myline[0]*xp+myline[1], '--', color='red', lw = 1.5, 
        label=#'1 - 1: \n'+ 
        'y = '+str(np.around(myline[0], decimals=4))+'x + '+str(np.around(myline[1], decimals=4)))

#subplot.set_title(cat2+' '+ycol+' vs. '+cat1+ ' ' +xcol)
pl.legend(loc='upper right')
