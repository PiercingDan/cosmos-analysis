#Field Catalogue========================================================
catname1 = 'ultravista'
masscol1 = 'log10_M'
typecol1 = 'Class'
zcol1 = 'zp'
columns1 = [masscol1, typecol1, zcol1]

zrange1 = [0.8, 1.0]

#Radius Catalogue======================================================
#Conversion is 1.0, since it is already in arssecs
catname2 = 'morph_zurich'
radcol2 = 'R50'
#IMPORTANT, CHANGE BELOW AS NECESSARY
radcol2convert = 0.03
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

zrange3 = zrange1 

#to shorten names
cat1 = catalogues[catname1]
mat1 = cat1[catname2+'_match']
cat2 = catalogues[catname2]
cat3 = catalogues[catname3]
mat3 = cat3[catname2+'_match']

#Binwidth Definition, N is number of point (Number of bins +1), position corresponds to different radfactor 
radfactor = [0.0, 1.0, 1.5, 2.0]
xlim = np.array([[9.5, 11.5], [8.5, 10.5], [8.0, 10.0], [7.0, 9.5]])
N = np.array([12, 12, 12, 12], dtype=int)
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


#Creating Generators

cat1gen = genentries(catname1, columns1, catname2, columns2, zcol1, zrange1)
#Applying R200 cut: only groups with a groupdist within R200 limit will count
cat3gen = genentries(catname3, columns3, catname2, columns2, zcol3, zrange3)
#(i for i in genentries(catname3, columns3, catname2, columns2, zcol3, zrange3) if cat3[groupdistcol3][i] < cat3[groupradiuscol3][i])
xvalues = [np.array([]), np.array([]), np.array([]), np.array([])]

#Field
len1 = 0
for i in cat1gen:
    len1 += 1
    #defining radius, logmass
    logmass = cat1[masscol1][i]
    radius = cat2[radcol2][mat1[i]]*radcol2convert
    z = cat1[zcol1][i]
    
    for j in range(len(radfactor)):
        val = xvalue(logmass, radius, z, radfactor[j])
        xvalues[j] = np.append(xvalues[j], val)
        for k in range(len(bins[j])-1):
            if val > bins[j][k] and val <= bins[j][k+1]:
                totalvalues[j][k]+=1
                fieldtotalvalues[j][k]+=1 
                if cat1[typecol1][i] != 'sf':
                    fieldquiescentvalues[j][k]+=1
#Group  
len3 = 0
for i in cat3gen:
    len3 += 1
    #defining radius, logmass, GROUP PROBABILITY (gp)
    logmass = cat3[masscol3][i]
    radius = cat2[radcol2][mat3[i]]*radcol2convert
    gp = cat3[groupprobcol3][i]
    z = cat3[zcol3][i]
    
    for j in range(len(radfactor)):
        val = xvalue(logmass, radius, z, radfactor[j])
        xvalues[j] = np.append(xvalues[j], val)
        for k in range(len(bins[j])-1):
            if val > bins[j][k] and val <= bins[j][k+1]:
                totalvalues[j][k]+=1
                grouptotalvalues[j][k]+=gp 
                if cat3[typecol3][i] != 'sf':
                    groupquiescentvalues[j][k]+=gp
                    
pl.close()   
fig, ax = pl.subplots(1, len(radfactor), figsize = (23, 6))# sharey=True)
fig.suptitle(r'Quiescent Fraction vs. $\log(M/R_e^n)$ with ' + catname1 + ', ' + catname2 + ', ' + catname3 + ' ' + str(zrange1[0]) + '$ \leq z \leq $' + str(zrange1[1]), fontsize=16)
fig.subplots_adjust(left=0.04, right=0.98)

for i in range(len(radfactor)):
    x = 0.5*(bins[i][:-1] + bins[i][1:])
    ax[i].plot(x, groupquiescentvalues[i]/grouptotalvalues[i], color='black', linestyle='-', marker='o',  markerfacecolor='black', markeredgecolor='black', label=str(len3)+r' Groups')# within $R_{200}$')

    ax[i].plot(x, fieldquiescentvalues[i]/fieldtotalvalues[i], color='red', linestyle='--', marker='o',  markerfacecolor='none', markeredgecolor='red', label=str(len1)+' Fields')

    if radfactor[i] != 0.0:
        ax[i].set_xlabel(r'$\log(M/R_e^{{%s}}\, M_*/kpc)$' % (radfactor[i]))
    else:
        ax[i].set_xlabel(r'$\log(M\, M_*)$')
    ax[i].set_ylabel(r'Quiescent Fraction')
    
    ax[i].set_xlim(bins[i][0], bins[i][-1])
    ax[i].set_ylim(0.0, 1.1)
    
    ax[i].set_yticks(np.linspace(0.0, 1.0, 11, endpoint=True))
    
    legend = ax[i].legend(loc='upper left')
    legend.draw_frame(False)

