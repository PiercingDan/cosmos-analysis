#convert is converting between pixels and arcsecs, if the original data is in arcsecs then convert = 1.0
#xvalues
cat1 = 'balogh_data2'
xvalues = []
xcol = 'zp'
xtrack = []

#yvalues
cat2 = 'ultravista'
yvalues = []
ycol = 'zp'
ytrack = []

#Importing data for efficiency
mat1 = catalogues[cat1][cat2+'_match']
xdata = catalogues[cat1][xcol].data
ydata = catalogues[cat2][ycol]

#gen = genentries(cat1, [xcol], cat2, [ycol])

#gen = (i for i in genentries(catname1, colnameslist1, catname2, colnameslist2) if data2['z'][mat1[i]] >= 0.8 and data2['z'][mat1[i]] <= 1.0)
#gen = (i for i in genentries(catname1, colnameslist1, catname2, colnameslist2, zcol=colnames1['z'], zrange=zrange1) if data2['z'][mat1[i]] >= 0.8 and data2['z'][mat1[i]] <= 1.0)

for i in range(len(balogh_data2)):
    if xdata[i] != -99.99 and catalogues[cat1][cat2+'_flag'][i] != 1:
        xvalues.append(xdata[i])
        yvalues.append(ydata[mat1[i]])
    #xvalues = np.append(xvalues, catalogues[cat1][xcol][i]) 
    #yvalues = np.append(yvalues, catalogues[cat2][ycol][mat1[i]])
    
#Convert to np array
xvalues = np.array(xvalues)
yvalues = np.array(yvalues)

fig = pl.figure(figsize=(10, 10))
subplot = pl.subplot(1, 1, 1)
pl.plot(xvalues, yvalues, 'o', ms=5.0, label = str(len(xvalues)) +' entries')
pl.xlabel(cat1 + ' ' + xcol)
pl.ylabel(cat2 + ' ' + ycol)
#pl.xlim(0.0, 4.0)
#pl.ylim(0.0, 4.0)

#lineofbestfit and plotting it
line = np.polyfit(xvalues, yvalues, 1, full=1)
myline = (1.0, 0.0)

xp = np.linspace(min(xvalues), max(xvalues), 100)

pl.plot(xp, line[0][0]*xp+line[0][1], '-', color='green', lw = 2.0, 
        label='Line of Best Fit: \n'+
        'y = '+str(np.around(line[0][0], decimals=4))+'x + '+str(np.around(line[0][1], decimals=4)))

pl.plot(xp, myline[0]*xp+myline[1], '-', color='red', lw = 2.0, 
        label='My line: \n'+ 
        'y = '+str(np.around(myline[0], decimals=4))+'x + '+str(np.around(myline[1], decimals=4)))

#subplot.set_title(cat2+' '+ycol+' vs. '+cat1+ ' ' +xcol)
pl.legend(loc='upper right')
