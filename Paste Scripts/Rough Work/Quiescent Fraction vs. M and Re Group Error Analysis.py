#%%time
#import numpy as np

#gen = genentries(catname3, colnameslist3, catname2, colnameslist2, zcol=colnames3['z'], zrange=zrange3)

gen = (i for i in genentries(catname3, colnameslist3, catname2, colnameslist2) if data2['z'][mat3[i]] >= 0.8 and data2['z'][mat3[i]] <= 1.0)

N = 1000

indexcol = []
for i in gen: 
    indexcol.append(i)
indexcol = np.array(indexcol)

probcol = balogh_data2['zp_prob'][indexcol].data
typecol = balogh_data2['Class'][indexcol].data
masscol = balogh_data2['log10_M'][indexcol].data
#Assuming error on mass is 0.1 dex
masserrcol = 0.1*np.ones(len(masscol))
#zcol = data3['z'][indexcol].data
zcol = griffith['Z'][mat3[indexcol]].data

#USING GRIFFITH REDSHIFT HERE
radcol = ((griffith['RE_GALFIT_HI'][mat3[indexcol]]*0.05*u.arcsec).to(u.rad)*(Distance(z=zcol, cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad)).value
raderrcol = ((griffith['REERR_GALFIT_HI'][mat3[indexcol]]*0.05*u.arcsec).to(u.rad)*(Distance(z=zcol, cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad)).value

#radcol2 = (griffith['RE_GALFIT_HI'][mat3[indexcol]]*0.05*u.arcsec).to(u.rad)*(Distance(z=balogh_data2['zp'][indexcol], cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad)

#Selecting based on group probabilities
randcol = np.random.random_sample([N, len(indexcol)])
choosecol = probcol > randcol
#All chosen vaues and all NOT starmforming, aka quiescent
qchoosecol = choosecol * (typecol != 'sf')

#Varying Mass, Radius using gaussian of error
massarray = np.random.normal(loc=masscol, scale=masserrcol, size=(N, len(masscol)))

#applying the log10 to the radius here
#Some rad errors are 0.0, which triggers a big, we set them to some small value

raderrcol[np.where(raderrcol==0.0)] = 1E-10

radarray = np.log10(np.random.normal(loc=radcol, scale=raderrcol, size=(N, len(radcol))))
#np.log10(np.random.normal(loc=radcol, scale=raderrcol, size=(N, len(radcol))))

#Selecting values that were chosen by realizations
MRdata = [np.array([massarray[i][choosecol[i]], radarray[i][choosecol[i]]]).T for i in range(N)]

qMRdata = [np.array([massarray[i][qchoosecol[i]], radarray[i][qchoosecol[i]]]).T for i in range(N)]

#setting bins
bindata = np.empty((NumBins, len(radfactor), N))
#allbinf = [np.zeros(i) for i in NumBins] 
qbindata= np.empty((NumBins, len(radfactor), N))
#qbinf = [np.zeros(i) for i in NumBins]

for i in range(len(radfactor)):
    #group
    for j in range(N):
        bindata[:, i, j], junk = np.histogram(MRdata[j][:, 0]-radfactor[i]*MRdata[j][:, 1], bins=bins[i])
        qbindata[:, i, j], junk = np.histogram(qMRdata[j][:, 0]-radfactor[i]*qMRdata[j][:, 1], bins=bins[i])

qfracarray = qbindata/bindata

meang = np.nanmean(qfracarray, axis=2)
errg = np.nanstd(qfracarray, axis=2)

#PLOTTING=================================================================
fig, ax = pl.subplots(1, len(radfactor), figsize = (23, 6))# sharey=True)
fig.suptitle(r'Quiescent Fraction vs. $\log(M/R_e^n)$ with ' + catname1 + ', ' + catname2 + ', ' + catname3 + ' ' + str(zrange1[0]) + '$ \leq z \leq $' + str(zrange1[1]), fontsize=16)
fig.subplots_adjust(left=0.04, right=0.98)

for i in range(len(radfactor)):
    x = 0.5*(bins[i][:-1] + bins[i][1:])
    
    ax[i].plot(x, meang[:, i], color='blue', linestyle='--', marker='o',  markerfacecolor='black', markeredgecolor='b', label=str(allMRg.shape[0])+r' Mean of '+str(N)+' Realizations')
    ax[i].errorbar(x, meang[:, i], yerr=errg[:, i], color='blue')
    
    ax[i].plot(x, qbing[i]/allbing[i], color='black', linestyle='-', marker='o',  markerfacecolor='black', markeredgecolor='black', label=str(allMRg.shape[0])+r' Groups within $R_{200}$')

    #ax[i].plot(x, qfracarray[:, i], color='red', linestyle='--', marker='o',  markerfacecolor='none', markeredgecolor='red', label=str(allMRf.shape[0])+' Fields')

    if radfactor[i] != 0.0:
        ax[i].set_xlabel(r'$\log(M/R_e^{{%s}}\, M_*/kpc)$' % (radfactor[i]))
    else:
        ax[i].set_xlabel(r'$\log(M\, M_*)$')
    ax[i].set_ylabel(r'Quiescent Fraction')
    
    ax[i].set_xlim(bins[i][0], bins[i][-1])
    ax[i].set_ylim(0.0, 1.0)
    
    ax[i].set_yticks(np.linspace(0.0, 1.0, 11, endpoint=True))
    
    legend = ax[i].legend(loc='upper left', fontsize=12)
    
    legend.draw_frame(False)


