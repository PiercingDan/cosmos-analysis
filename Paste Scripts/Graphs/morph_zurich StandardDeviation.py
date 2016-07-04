%%time
#Field Catalogue========================================================
catname1 = 'morph_zurich'
colnames1 = {'radius': 'R_GIM2D', 'radius_UE': 'UE_R_GIM2D', 'radius_LE': 'LE_R_GIM2D'}
colnameslist1 = list(colnames1.values())
data1 = {namekey: np.array(catalogues[catname1][namevalue]) for namekey, namevalue in colnames1.items()}
zrange1 = [0.8, 1.0]

#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'griffith'
colnames2 = {'radius': 'RE_GALFIT_HI'}
colnameslist2 = list(colnames2.values())
data2 = {namekey: np.array(catalogues[catname2][namevalue]) for namekey, namevalue in colnames2.items()}
#IMPORTANT, CHANGE BELOW AS NECESSARY
radcol2convert = 0.05

#Creating the matching arrays
cat1 = catalogues[catname1]
mat1 = cat1[catname2+'_match']
cat2 = catalogues[catname2]

#fractional uncertainties
data1['radius_fracE'] = 0.5*(data1['radius_UE']+data1['radius_LE'])/data1['radius']

#Generating all values that are a 'good' match and have a data value
gen = genentries(catname1, colnameslist1, catname2, colnameslist2)

#Histogram parameters
N = 10
xmax = 0.10
binvalues = []
std = []

#Appending values
fracarray = []

for i in gen:
    fracarray.append(data1['radius_fracE']

#for j in range(N+1):
    #temparray = []
    #tempdiff = []
    #gen = (i for i in range(total) if mat1[1][i]==1 and mat2[1][i]==1 \
           #and catalogues[cat1][col1][mat1[0][0][i]]!=-999999.0 \
           #and catalogues[cat2][col2][mat2[0][0][i]]!=-999999.0 )  
    
    #for i in gen:
        #if fracuncert(i)>(j/N) and fracuncert(i)<=((j+1)/N): 
            ##tempdiff = np.append (tempdiff, catalogues[cat1][col1][mat1[0][0][i]]*convert1 - catalogues[cat2][col2][mat2[0][0][i]]*convert2)
            
            
    #binvalues.append(tempdiff)
    #std = np.append(std, np.std(tempdiff))
    

#plotting
pl.close()
fig = pl.figure()
subplot = pl.subplot(2, 1, 1)

subplot.bar(np.linspace(0, xmax, N+1, endpoint=1), std, width = xmax/(N), label = str(len(fracarray)) + ' total values')

#Preparing the graph
subplot.set_xlim(0, xmax)
subplot.set_xticks(np.linspace(0, xmax, N+1, endpoint=1))
subplot.set_xlabel('morph_zurich R_GIM2D Fractional Uncertainty')

subplot.set_ylabel('Scatter')

subplot.set_title('Standard Deviation of morph_zurich R_GIM2D Fractional Uncertainty')
subplot.legend (loc='upper right')

#Histogram plot
subplot2 = pl.subplot(2, 1, 2)
n, bins, patches = subplot2.hist(fracarray, np.linspace(0, xmax, N+1, endpoint=1), normed = 0, histtype='bar')
subplot2.set_title('Histogram of morph_zurich R_GIM2D Fractional Uncertainty')

subplot2.set_xticks(np.linspace(0, xmax, N+1, endpoint=1))
subplot2.set_xlabel('morph_zurich R_GIM2D Fractional Uncertainty')

subplot2.set_ylabel('Frequency')

fig.subplots_adjust(hspace = 0.38)
#n, bins, patches = pl.hist(fracarray, np.linspace(0, 1.0, 10, endpoint=1), normed=0, histtype='bar')
#subplot.plot(np.linspace(0, 1.0, N, endpoint=1), std, '.')
