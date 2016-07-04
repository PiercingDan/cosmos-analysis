#convert is converting between pixels and arcsecs, if the original data is in arcsecs then convert = 1.0
#xvalues

cat1 = 'balogh_data1'
xvalues = []
xcol1 = 'MAG_J'
xcol2 = 'MAG_I1'

#yvalues
cat2 = 'ultravista_Main'
yvalues = []
ycol1 = 'J'
ycol2 = 'ch1'

#=================================================
g2index = []
b2index = []
for i in range(len(balogh_data2)):
    a = np.where(geec2['ID_1']==catalogues[cat1]['Galaxy_ID'][i])[0]
    if a.size == 0:
        #no match
        b2index.append(False)
    else:
        #yes match
        b2index.append(True)
        g2index.append(a[0])

g2index = np.array(g2index)
b2index = np.array(b2index)

#Importing data for efficiency
mat1 = catalogues[cat1]['ultravista_match'][b2index]
xdata = np.array(geec2[xcol1][g2index])-np.array(geec2[xcol2][g2index])
ydata = -2.5*np.log10(np.array(catalogues[cat2][ycol1]))-(-2.5*np.log10(np.array(catalogues[cat2][ycol2])))
Type = np.array(catalogues[cat1]['Class'])
#
goodcol = (np.array(geec2[xcol1][g2index])>-98.0)*(np.array(geec2[xcol2][g2index])>-98.0)

#gen = genentries(cat1, [xcol], cat2, [ycol])
choosecol = goodcol*(catalogues[cat1]['ultravista_flag'][b2index]!=1)*(np.isnan(ydata[mat1])==False)

#Convert to np array
xvalues = xdata[choosecol]
yvalues = ydata[mat1][choosecol]
typevalues = Type[choosecol]

fig = pl.figure(figsize=(10, 10))
ax = pl.subplot(1, 1, 1)
ms = 3.0
ax.plot(xvalues, yvalues, 'o', ms=ms, label = str(len(xvalues)) +' entries')

#ax.plot(xvalues[typevalues=='sf'], yvalues[typevalues=='sf'], 'o', color='blue', ms=ms, label = 'star-forming entries')
#ax.plot(xvalues[typevalues=='int'], yvalues[typevalues=='int'], 'o', color='green', ms=ms, label = 'intermediate entries')
#ax.plot(xvalues[typevalues=='p'], yvalues[typevalues=='p'], 'o', color='red', ms=ms, label = 'quiescent entries')
pl.xlabel('geec2' + ' ' + xcol1 + ' - ' + xcol2)
pl.ylabel(cat2 + ' ' + ycol1 + ' - ' + ycol2)
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

ax.set_title(str(len(xvalues))+' entries')
pl.legend(loc='upper left')
