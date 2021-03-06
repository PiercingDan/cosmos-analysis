#Field Catalogue========================================================
catname1 = 'ultravista'
masscol1 = 'log10_M'
zcol1 = 'zp'
typecol1 = 'Class'
columns1 = [masscol1, zcol1, typecol1]

zrange1 = [0.8, 1.0]

typerequirement = 'q'
#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'morph_zurich'
radcol2 = 'R_GIM2D'
columns2 = [radcol2]

#===================================================================
cat1 = catalogues[catname1]
cat2 = catalogues[catname2]
mat1 = cat1[catname2+'_match']

gen = []
#Complete List of All Good Galaxies (USE2=1)
gen.append(genentries(catname1, columns1, zcol=zcol1, zrange=zrange1))

#List of Galaxies that have a Good Match to Zurich
sparegen = genentries(catname1, columns1, zcol=zcol1, zrange=zrange1)
gen.append((i for i in sparegen if cat1[catname2+'_flag'][i]==1))
    
#List of Galaxies that have a Good Match to Zurich, Good Entry (Pass Flag Check)
gen.append(genentries(catname1, columns1, catname2, [], zcol=zcol1, zrange=zrange1))

#List of Galaxies that have a Good Match to Zurich, Good Entry, and have a good R_GIM2D Entry
gen.append(genentries(catname1, columns1, catname2, columns2, zcol=zcol1, zrange=zrange1))

#For only starforming or for only quiescent
if typerequirement != 'all':
    for i in range(len(gen)):
        gen[i] = (j for j in gen[i] if cat1[typecol1][j]==typerequirement)
    
#Analysis: First create an array of all the masses for each generator
mass = [] 
for generator in gen:
    temparray = np.array([])
    for i in generator:
        temparray = np.append(temparray, cat1[masscol1][i])
    mass.append(temparray)

#Histrogram Parameters
bins = 20
Range = [8.0, 11.0]
binedges = np.linspace(Range[0], Range[1], bins, endpoint=0)
wid = (Range[1]-Range[0])/bins

#binvalues is the number of mass[i] in each bin
binvalues = []
    
#Then use np.histogram (no plotting yet!) to calculate the histogram parameters based solely on frequency of each mass[i]
for i in range(len(gen)):
    (tempbinvalues, garbage) = np.histogram(mass[i], bins, Range)
    binvalues.append(tempbinvalues)
    
#=======================================================================
#Plotting==============================================================
#pl.close()
fig, ax = pl.subplots(1, len(gen)-1, figsize=(20, 6))
fig.subplots_adjust(left=0.08, right=0.96, top=0.86)

#Since there's just two plots, no need for iterating loop
fig.suptitle('z: '+str(zrange1)+'; type: ' +typerequirement, fontsize=16)
title = ('Good Match in Zurich', r'Good Match in Zurich, Good Entry', r"""Good Match in Zurich, Good Entry, 
and Good Value in $R_{GIM2D}$""")

for i in range(len(gen)-1):
    ax[i].bar(left=binedges, height=binvalues[i+1]/binvalues[0], width=wid, label=str(len(mass[i+1]))+' entries out of '+str(len(mass[0])))
    ax[i].set_xlabel(r'$\log(M\, M_{\odot})$')
    ax[i].set_ylabel('Fraction')
    ax[i].set_title(title[i])
    ax[i].set_ylim(0.0, 1.0)
    ax[i].set_yticks((np.linspace(0.0, 1.0, 11, endpoint=True)))
    
    legend=ax[i].legend(loc='upper right')
    legend.draw_frame(False)