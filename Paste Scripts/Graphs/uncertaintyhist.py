#convert is converting between pixels and arcsecs, if the original data is in arcsecs then convert = 1.0
#xvalues
cat1 = 'morph_2005'
values1 = []
col1 = 'halflightrad'
convert1 = 0.07
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
tempvalues = []
tempUE = []

total = (len(mat1[0][0]))
#all mat[0][0] have same length
gen = (i for i in range(total) if mat1[1][i]==1 and mat2[1][i]==1 \
       and catalogues[cat1][col1][mat1[0][0][i]]!=-999999.0 \
       and catalogues[cat2][col2][mat2[0][0][i]]!=-999999.0 )

for i in gen:
    UE_AVG = (0.5)*(catalogues[cat2][col3][mat2[0][0][i]] + catalogues[cat2][col4][mat2[0][0][i]]) * convert2
    
    tempUE = np.append(tempUE, UE_AVG)
    
    tempvalues = np.append(tempvalues, (catalogues[cat1][col1][mat1[0][0][i]] * convert1 - catalogues[cat2][col2][mat2[0][0][i]] * convert2))
    
    values1 = np.append(values1, (catalogues[cat1][col1][mat1[0][0][i]] * convert1 - catalogues[cat2][col2][mat2[0][0][i]] * convert2)/(np.sqrt(2)*(UE_AVG)))
    
#plotting
pl.close()
fig = pl.figure()
subplot = pl.subplot(1, 1, 1)

#Histogram
N=30
binsize = np.linspace(-N, N, 2*N+1, endpoint=1)
n, bins, patches = pl.hist(values1, binsize, normed=0, histtype='bar')

#best fitting data
(mu1, sigma) = norm.fit(values1)


#Histogram Curve
ynorm = mlab.normpdf(bins, mu, sigma)
#subplot.plot(bins, ynorm*len(values1), 'r--', lw = 2.0)

subplot.set_xticks(np.linspace(-N, N, N/2.5+1, endpoint=1))
subplot.set_xlim(-N, N)
subplot.set_xlabel(r'$\frac{R_{2005}-R_{GIM2D}}{\sigma_{12}}$')
subplot.set_ylabel('Frequency (Out of ' +str(len(values1))+ ' Values)')
#subplot.set_ylim(0.0, 1000.0)



subplot.set_title('Histogram of '+ r'$\frac{R_{2005}-R_{GIM2D}}{\sigma_{12}}$')
#pl.legend(loc='upper right')
