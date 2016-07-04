#convert is converting between pixels and arcsecs, if the original data is in arcsecs then convert = 1.0
#xvalues
cat1 = 'morph_2005'
values1 = []
col1 = 'halflightrad'
convert1 = 0.03
xtrack = []

#yvalues
cat2 = 'morph_zurich'
values2 = []
col2 = 'R_GIM2D'
convert2 = 1.0
ytrack = []

#additional
col3 = 'LE_R_GIM2D'
col4 = 'UE_R_GIM2D'

#matching
mat1 = balogh_data1_match[cat1]
mat2 = balogh_data1_match[cat2]

#all mat[0][0] have same length
gen = (i for i in range(len(mat1[0][0])) if mat1[1][i]==1 and mat2[1][i]==1 \
       and catalogues[cat1][col1][mat1[0][0][i]]!=-999999.0 \
       and catalogues[cat2][col2][mat2[0][0][i]]!=-999999.0 )

for i in gen:
    UE_AVG = (1/2)*(catalogues[cat2][col3][mat2[0][0][i]] + catalogues[cat2][col4][mat2[0][0][i]]) * convert2
    
    values1 = np.append(values1, abs((sqrt(2)*(UE_AVG))/(catalogues[cat1][col1][mat1[0][0][i]] * convert1 - catalogues[cat2][col2][mat2[0][0][i]] * convert2)))
    
#plotting
pl.close()
fig = pl.figure()
subplot = pl.subplot(1, 1, 1)

n, bins, patches = pl.hist(values1, np.linspace(0.0, 100.0, 20, endpoint=1), normed=0, histtype='bar')
pl.xlabel(r'$\left|\frac{R_{2005}-R_{GIM2D}}{\sigma_{12}}\right|$')
pl.ylabel('Frequency')
##pl.ylim(0.0, 4.0)

#subplot.set_title(cat2+' '+ycol+' vs. '+cat1+ ' ' +xcol)
pl.legend(loc='upper right')
