#convert is converting between pixels and arcsecs, if the original data is in arcsecs then convert = 1.0

#Field Catalogue========================================================
catname1 = 'morph_zurich'
colnames1 = {'radius': 'R_GIM2D', 'radius_UE': 'UE_R_GIM2D', 'radius_LE': 'LE_R_GIM2D'}
colnameslist1 = list(colnames1.values())
data1 = {namekey: np.array(catalogues[catname1][namevalue]) for namekey, namevalue in colnames1.items()}
zrange1 = [0.8, 1.0]
radconvert1 = 1.0
data1['radius'] = data1['radius']*radconvert1
data1['radius_E'] = 0.5*(data1['radius_UE']+data1['radius_LE'])*radconvert1

#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'griffith'
colnames2 = {'radius': 'RE_GALFIT_HI', 'radius_E': 'REERR_GALFIT_HI'}
colnameslist2 = list(colnames2.values())
data2 = {namekey: np.array(catalogues[catname2][namevalue]) for namekey, namevalue in colnames2.items()}
#IMPORTANT, CHANGE BELOW AS NECESSARY
radconvert2 = 0.05
data2['radius'] = data2['radius']*radconvert2
data2['radius_E'] = data2['radius_E']*radconvert2

#Creating the matching arrays
mat1 = np.array(catalogues[catname1][catname2+'_match'])

#Generating all values that are a 'good' match and have a data value
gen = genentries(catname1, colnameslist1, catname2, colnameslist2)

#for i in gen:
    #UE_AVG = (1/2)*(catalogues[cat2][col3][mat2[0][0][i]] + catalogues[cat2][col4][mat2[0][0][i]]) * convert2
    
    #values1 = np.append(values1, abs((sqrt(2)*(UE_AVG))/(catalogues[cat1][col1][mat1[0][0][i]] * convert1 - catalogues[cat2][col2][mat2[0][0][i]] * convert2)))
  
values = []  
sigma12 = []
for i in gen:
    error = np.sqrt(data1['radius_E'][i]**(2.0)+data2['radius_E'][i]**(2.0))
    values.append((data2['radius'][mat1[i]]-data1['radius'][i])/error)
    sigma12.append(error)
values = np.array(values)    
sigma12 = np.array(sigma12)
    
#plotting
pl.close()
fig = pl.figure()
subplot = pl.subplot(1, 1, 1)

n, bins, patches = pl.hist(values, np.linspace(-30, 30.0, 61, endpoint=1), normed=1, histtype='bar', label = str(len(values)) + ' entries')
pl.xlabel(r'$\frac{R_{GALFIT}-R_{GIM2D}}{\sigma_{12}}$', fontsize=20)
pl.ylabel('Frequency')

#subplot.set_title(cat2+' '+ycol+' vs. '+cat1+ ' ' +xcol)
pl.legend(loc='upper right')
subplot.set_title(colnames1['radius']+' and '+colnames2['radius']) 
