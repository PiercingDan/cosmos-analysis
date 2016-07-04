#Field Catalogue========================================================
catname1 = 'ultravista'
masscol1 = 'log10_M'
zcol1 = 'zp'
typecol1 = 'Class'
columns1 = [masscol1, zcol1, typecol1]

zrange = []

typerequirement = 'all'
#Radius Catalogue=============a=========================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'morph_zurich'
radcol2 = 'R50'
magcol2 = 'ACS_MAG_AUTO'
columns2 = [magcol2]
#describing what values are generated
if radcol2 in columns2:
    description = 'Matched, with good entries, good '+radcol2+' entries'
else:
    description = 'Matched, with good entries'
#===================================================================
cat1 = catalogues[catname1]
cat2 = catalogues[catname2]
mat1 = cat1[catname2+'_match']

#Analysis
gen = genentries(catname1, columns1, catname2, columns2, zcol=zcol1, zrange=zrange)
#Analysing by type if needed
if typerequirement != 'all':
    gen = (i for i in gen if cat1[typecol1][i]==typerequirement)

xyvalues = np.empty([1, 2])                
for i in gen:
    xyvalues = np.concatenate((xyvalues, [[cat2[magcol2][mat1[i]], cat1[masscol1][i]]]))
xyvalues = np.delete(xyvalues, 0, axis=0)

#PLOTTING=====================================================================================================================================  
fig = pl.figure()
fig.suptitle('z: '+str(zrange)+'; type: ' +typerequirement, fontsize=16)
ax = pl.subplot(1, 1, 1)
ax.plot(xyvalues[:, 0], xyvalues[:, 1], 'o', ls='None', label=str(xyvalues.shape[0])+' total values')

ax.set_xlabel(r'ACS I-Band $m_{AB}$')
ax.set_ylabel(r'$\log(M\, M_{\odot})$')
ax.set_title(description)
ax.set_ylim(7.5, 12.0)

legend = ax.legend(loc='upper right')
legend.draw_frame(False)
