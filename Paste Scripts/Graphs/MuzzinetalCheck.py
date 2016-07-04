#Field Catalogue========================================================
catname1 = 'balogh_data2'
masscol1 = 'log10_M'
typecol1 = 'Class'
zcol1 = 'zp'
columns1 = [masscol1, typecol1, zcol1]

zrange1 = [0.8, 1.0]


#to shorten names
cat1 = catalogues[catname1]

#Binwidth Definition, N is number of point (Number of bins +1), position corresponds to different radfactor 
radfactor = [0.0, 0.0]#1.0, 1.5, 2.0]
xlim = np.array([[8.0, 12.0], [8.0, 12.0], [7.5, 10.0], [6.5, 9.5]])
N = np.array([15, 30, 10, 10], dtype=int)
bins = [np.linspace(xlim[i][0], xlim[i][1], N[i]+1, endpoint=True) for i in range(len(radfactor))]

#xvalue
def xvalue (log10M, rad, z, factor): 
    return log10M - factor*np.log10((rad*u.arcsec).to(u.rad)*(Distance(z=z, cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
          
#Total values for each graph, contains the array by which contains the total number of group or field galaxies in each bin for certain log(M/R^n)
#len(radfactor) means there are three of (2, N) arrays, each corresponding to a different factor n (different graph)
#2 represents two options: group or field
#N represents total number of bins
totalvalues = [np.zeros(i, dtype=int) for i in N]       
grouptotalvalues = [np.zeros(i) for i in N] 
fieldtotalvalues = [np.zeros(i, dtype=int) for i in N] 
groupquiescentvalues = [np.zeros(i) for i in N]
fieldquiescentvalues = [np.zeros(i, dtype=int) for i in N]


#Creating Generator
cat1gen = (i for i in range(len(cat1))\
           if ultravista['star'][i] != 1 and\
            ultravista['K_flag'][i] <= 4 and\
            ultravista['contamination'][i] != 1 and\
            ultravista['nan_contam'][i] <= 3 and\
            ultravista['zp'][i] >= zrange1[0] and\
            ultravista['zp'][i] <= zrange1[1] and\
            -2.5*np.log10(ultravista['Ks_tot'][i]) +25 < 23.4)# and\
            #ultravista['morph_zurich_flag'][i] == 1 and\
            #flag('morph_zurich', ['R_GIM2D'], ultravista['morph_zurich_match'][i])==False)

#xvalues = np.array([])
#Field
mass = np.array([])
for i in cat1gen:
    #defining radius, logmass
    logmass = cat1[masscol1][i]
    z = cat1[zcol1][i]
    mass = np.concatenate((mass, [logmass]))
    for j in range(len(radfactor)):
        #val = xvalue(logmass, radius, z, radfactor[j])
        val = logmass
       # xvalues[j] = np.append(xvalues[j], val)
        for k in range(len(bins[j])-1):
            if val > bins[j][k] and val <= bins[j][k+1]:
                totalvalues[j][k]+=1
                fieldtotalvalues[j][k]+=1 
                if cat1[typecol1][i] != 'sf':
                    fieldquiescentvalues[j][k]+=1
#pl.close()   
fig, ax = pl.subplots(1, len(radfactor), figsize = (23, 6))# sharey=True)
fig.suptitle(r'Quiescent Fraction vs. $\log(M/R_e^n)$ with ' + catname1 +' '+ str(zrange1[0]) + '$ \leq z \leq $' + str(zrange1[1]), fontsize=16)
fig.subplots_adjust(left=0.04, right=0.98)

for i in range(len(radfactor)):
    x = 0.5*(bins[i][:-1] + bins[i][1:])

    ax[i].plot(x, fieldquiescentvalues[i]/fieldtotalvalues[i], color='red', linestyle='--', marker='o',  markerfacecolor='none', markeredgecolor='red', label='Field')

    if radfactor[i] != 0.0:
        ax[i].set_xlabel(r'$\log(M/R_e^{{%s}}\, M_*/kpc)$' % (radfactor[i]))
    else:
        ax[i].set_xlabel(r'$\log(M\, M_*)$')
    ax[i].set_ylabel(r'Quiescent Fraction')
    
    ax[i].set_xlim(bins[i][0], bins[i][-1])
    ax[i].set_ylim(0.0, 1.1)
    
    ax[i].set_yticks(np.linspace(0.0, 1.0, 11, endpoint=True))
    
    #legend = ax[i].legend(loc='upper right')
    #legend.draw_frame(False)

