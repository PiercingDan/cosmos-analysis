#Field Catalogue========================================================
catname1 = 'ultravista'
magcol1 = 'Ks_tot'
zcol1 = 'zp'
typecol1 = 'Class'
columns1 = [magcol1, zcol1, typecol1]

zrange1 = []

typerequirement = 'all'
#Radius Catalogue=============a=========================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'morph_zurich'
radcol2 = 'R_GIM2D'
magcol2 = 'ACS_MAG_AUTO'
columns2 = [radcol2, magcol2]

#===================================================================
cat1 = catalogues[catname1]
cat2 = catalogues[catname2]
mat1 = cat1[catname2+'_match']

#Analysis
gen = genentries(catname1, columns1, catname2, columns2)

ACSmagKmag = np.empty([1, 2])                
for i in gen:
    ACSmagKmag = np.concatenate((ACSmagKmag, [[-2.5*np.log10(cat1[magcol1][i])+25, cat2[magcol2][mat1[i]]]]))
ACSmagKmag = np.delete(ACSmagKmag, 0, axis=0)
  
fig = pl.figure()
ax = pl.subplot(1, 1, 1)
ax.plot(ACSmagKmag[:, 0], ACSmagKmag[:, 1], 'o', ls='None')

ax.set_xlabel(r'$m_{Ks}$')
ax.set_ylabel(r'$m_{ACS}$')

ax.set_ylim(12.0, 26.0)

ax.set_xticks(np.linspace(14.0, 24.0, 11, endpoint=1))
ax.set_yticks(np.linspace(12.0, 26.0, 15, endpoint=1))

ax.set_title(r'ACS Total I-Band Magnitude vs. UltraVISTA Total K-Band Magnitude')