#defining data
#x colour is V-z k-corrected to z=0.9
#y colour is J-[3.6] k-corrected to z=0.9
catname = 'balogh_photoz'
cat = catalogues[catname]
redshift = 'zp'
#bands = {'J': 'J', '3.6': 'ch1', 'V': 'V', 'z+': 'zp'} 
#kcorr = {'J': 'kc_J_'+redshift, '3.6':'kc_ch1_'+redshift, 'V':'kc_V_'+redshift, 'z+': 'kc_zp_'+redshift}
mat = cat['griffith_match']

#V - z kcorrected to z=0.9
#data = {key: -2.5*np.log10(np.array(ultravista_Main[bands[key]][mat])*np.array(ultravista_Main['Ks_tot'][mat])/np.array(ultravista_Main['Ks'][mat]))+25-np.array(cat[kcorr[key]]) for key in bands.keys()}
#
#xcolour = data['V']-data['z+']
#ycolour = data['J']-data['3.6']

xcolour = balogh_photoz['V-z']
ycolour = balogh_photoz['J-I1']

#index = []
#for i in range(len(balogh_data1)):
    #index.append(np.where(geec2['ID_1']==balogh_data1['Galaxy_ID'][i])[0][0])

#index = np.array(index)

#Kcorr is set up so that if one band is -99.99, all kcorrections are bad, because we are fitting profil to these bands, one bad value most likely will mess up all of the others
#choosecol = (cat['zp']>=0.8)*(cat['zp']<=1.0)#*(cat[kcorr['J']]!=-99.99)
xdata, ydata = (xcolour, ycolour)

#calculating Type
Type = np.empty(len(xdata), dtype='U10')
Type.fill('int')
qindex = (xdata > 3.0) + ((xdata > 2.0) * (ydata < (0.856 * (xdata - 2.0) + 0.6311)))
#Added (xdata < 3.0) AND condition to sfindex, otherwise, doesn't make sense
sfindex = (xdata < 2.0) + (ydata > (0.856 * (xdata - 2.0) + 1.008))* (xdata < 3.0)
Type[qindex]='p'
Type[sfindex]='sf'


#PLOTTING==============================================================
#pl.close()
ms = 1.5
fig, ax = pl.subplots(1, 1, figsize=(10, 10))
#ax.plot(xdata, ydata, 'o', ms=1.0, label=str(len(xdata))+' entries')
ax.plot(xdata[Type=='p'], ydata[Type=='p'], 'o', ms=ms, mfc='none', mec='red', label='q entries')
ax.plot(xdata[Type=='int'], ydata[Type=='int'], 'o', ms=ms, mfc='none', mec='green', label='int entries')
ax.plot(xdata[Type=='sf'], ydata[Type=='sf'], 'o', ms=ms, mfc='none', mec='blue', label='sf entries')

#ax.set_xlim(0.0, 4.0)
#ax.set_ylim(-1.0, 4.0)

ax.set_xlabel(r'$(V-z)^{0.9}$')
ax.set_ylabel(r'$(J-[3.6])^{0.9}$')

minorLocator = mpl.ticker.AutoMinorLocator()
ax.xaxis.set_minor_locator(minorLocator)
ax.yaxis.set_minor_locator(minorLocator)

ax.set_title(catname+' 0.8<'+redshift+'<1.0 : '+str(len(xdata))+' entries')

legend=ax.legend(loc='upper right')
legend.draw_frame(False)

#DRAW CUT LINES
#sf cuts, q cuts
qx1 = 2*np.ones(100)
qy1 = np.linspace(-5.0, 0.6311, 100)

sfx1 = 2*np.ones(100)
sfy1 = np.linspace(0.6311, 1.008, 100)

sfx2 = np.linspace(2.0, 3.0, 100)
sfy2 = 0.856*(sfx2-2)+1.008

qx2 = np.linspace(2.0, 3.0, 100)
qy2 = 0.856*(qx2-2)+0.6311

qx3 = 3*np.ones(100)
qy3 = np.linspace(1.4871, 6.0, 100)


#sf
ax.plot(sfx1, sfy1, '-', color='black', lw=2.0)
ax.plot(sfx2, sfy2, '-', color='black', lw=2.0)
ax.plot(qx1, qy1, '-', color='black', lw=2.0)
ax.plot(qx2, qy2, '-', color='black', lw=2.0)
ax.plot(qx3, qy3, '-', color='black', lw=2.0)


##producing cuts, start with int and change to q, sf

##Checking if types are done correctly

#matches = (balogh_data1['Class'][choosecol]==Type).sum()
#print('There are ', matches, ' matches out of ', len(xdata), ' entries')
