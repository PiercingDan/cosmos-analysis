#defining data
#x colour is V-z k-corrected to z=0.9
#y colour is J-[3.6] k-corrected to z=0.9
#xcolour = (geec2['MAG_V']-geec2['KCORR09_V'])-(geec2['MAG_z']-geec2['KCORR09_z'])
#ycolour = (geec2['MAG_J']-geec2['KCORR09_J'])-(geec2['MAG_I1']-geec2['KCORR09_I1'])

xcolour = balogh_photoz['V-z']
ycolour = balogh_photoz['J-I1']

#2 indices, one for balogh2 one for geec2
g2index = []
b2index = []
for i in range(len(balogh_data2)):
    a = np.where(balogh_photoz['Galaxy_ID']==balogh_data2['Galaxy_ID'][i])[0]
    if a.size == 0:
        #no match
        b2index.append(False)
    else:
        #yes match
        b2index.append(True)
        g2index.append(a[0])
    

g2index = np.array(g2index)
b2index = np.array(b2index)

#by column
#choosecol = (balogh_data2['zp']>=0.8)*(balogh_data2['zp']<=1.0)


#Restricting by redshift
#g2index = g2index*(choosecol[b2index])
#b2index = b2index*choosecol

xdata, ydata = (xcolour[g2index], ycolour[g2index])

#PLOTTING==============================================================
pl.close()
fig, ax = pl.subplots(1, 1, figsize=(10, 10))
ms = 4.0

#ax.plot(xdata, ydata, 'o', ms=1.0, label=str(len(index))+' entries')
ax.plot(xdata[balogh_data2['Class'][b2index]=='p'], ydata[balogh_data2['Class'][b2index]=='p'], 'o', color='red', ms=ms, label='q entries')
ax.plot(xdata[balogh_data2['Class'][b2index]=='int'], ydata[balogh_data2['Class'][b2index]=='int'], 'o', color='green', ms=ms, label='int entries')
ax.plot(xdata[balogh_data2['Class'][b2index]=='sf'], ydata[balogh_data2['Class'][b2index]=='sf'], 'o', color='blue', ms=ms, label='sf entries')


#ax.plot(xdata[geec2['Type'][index]==0], ydata[geec2['Type'][index]==0], 'o', ms=4.0, color='blue', label='sf entries')
#ax.plot(xdata[geec2['Type'][index]==1], ydata[geec2['Type'][index]==1], 'o', ms=4.0, color='green', label='int entries')
#ax.plot(xdata[balogh_data1['Class']=='p'], ydata[balogh_data1['Class']=='p'], 'o', ms=4.0, color='red', label='q entries')

ax.set_xlim(0.0, 4.0)
ax.set_ylim(0.0, 4.0)

ax.set_xlabel(r'$(V-z)^{0.9}$')
ax.set_ylabel(r'$(J-[3.6])^{0.9}$')

minorLocator = mpl.ticker.AutoMinorLocator()
ax.xaxis.set_minor_locator(minorLocator)
ax.yaxis.set_minor_locator(minorLocator)

legend=ax.legend(loc='upper right')
legend.draw_frame(False)

ax.set_title('balogh_data2 '+str(len(xdata))+' entries for 0.8<zp<1.0')

#DRAW CUT LINES
#sf cuts, q cuts
qx1 = 2*np.ones(100)
qy1 = np.linspace(-150.0, 0.6311, 100)

sfx1 = 2*np.ones(100)
sfy1 = np.linspace(0.6311, 1.008, 100)

sfx2 = np.linspace(2.0, 3.0, 100)
sfy2 = 0.856*(sfx2-2)+1.008

qx2 = np.linspace(2.0, 3.0, 100)
qy2 = 0.856*(qx2-2)+0.6311

qx3 = 3*np.ones(100)
qy3 = np.linspace(1.4871, 150.0, 100)

#sf
ax.plot(sfx1, sfy1, '-', color='black', lw=2.0)
ax.plot(sfx2, sfy2, '-', color='black', lw=2.0)
ax.plot(qx1, qy1, '-', color='black', lw=2.0)
ax.plot(qx2, qy2, '-', color='black', lw=2.0)
ax.plot(qx3, qy3, '-', color='black', lw=2.0)


#producing cuts, start with int and change to q, sf
Type = np.empty(b2index.sum(), dtype='U10')
Type.fill('int')
qindex = (xdata > 3.0) + ((xdata > 2.0) * (ydata < (0.856 * (xdata - 2.0) + 0.6311)))
#Added (xdata < 3.0) AND condition to sfindex, otherwise, doesn't make sense
sfindex = (xdata < 2.0) + (ydata > (0.856 * (xdata - 2.0) + 1.008))* (xdata < 3.0)
Type[qindex]='p'
Type[sfindex]='sf'
#Checking if types are done correctly

matches = (balogh_data2['Class'][b2index]==Type).sum()
print('There are ', matches, ' matches out of ', len(xdata), ' entries')