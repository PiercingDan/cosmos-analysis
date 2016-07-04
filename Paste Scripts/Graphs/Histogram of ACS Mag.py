#Field Catalogue========================================================
catname1 = 'ultravista'
masscol1 = 'log10_M'
typecol1 = 'Class'
zcol1 = 'zp'
columns1 = [masscol1, typecol1, zcol1]

zrange = [0.8, 1.0]

typerequirement = 'all'
#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'morph_zurich'
radcol2 = 'R_GIM2D'
magcol2 = 'ACS_MAG_AUTO'
columns2 = [radcol2]

#Group Catalogue=======================================================
catname3 = 'balogh_data2'
masscol3 = 'log10_M'
typecol3 = 'Class'
groupprobcol3 = 'zp_prob'
zcol3 = 'zp'
groupdistcol3 = 'groupdist'
groupradiuscol3 = 'R200'
columns3 = [masscol3, typecol3, groupprobcol3, zcol3, groupdistcol3, groupradiuscol3]


#to shorten names
cat1 = catalogues[catname1]
mat1 = cat1[catname2+'_match']
cat2 = catalogues[catname2]
cat3 = catalogues[catname3]
mat3 = cat3[catname2+'_match']

#========================================================================
gen = genentries(catname2, ['R_GIM2D'])
bins = 20
Range = [14.0, 24.0]
binedges = np.linspace(Range[0], Range[1], bins, endpoint=0)
wid = (Range[1]-Range[0])/bins

description = 'All Zurich Galaxies with Good Entry and Good R_GIM2D Entry'
xlabel = r'ACS I-Band $m_{AB}$'
ylabel = 'Fraction'

#Analysis===========================================================
mag = np.array([])
maglen = 0
for i in gen:
    mag = np.append(mag, cat2[magcol2][i])
    maglen += 1
    
binvalues, garbage = np.histogram(mag, bins, Range)    

#Plotting===========================================================
pl.close()
fig = pl.figure(figsize=(10,7))
ax = pl.subplot(1, 1, 1)
fig.subplots_adjust(top=0.85)

ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.bar(left=binedges, height=binvalues/maglen, width=wid, label='Fraction of '+str(maglen)+' entries')
ax.set_title(description)
fig.suptitle('z: '+str(zrange)+'; type: ' +typerequirement, fontsize=16)
legend = ax.legend(loc='upper left', fontsize=12.5)
legend.draw_frame(False)