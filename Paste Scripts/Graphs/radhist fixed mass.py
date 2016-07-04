masslim = [9.5, 10.5]
radlim = [0.0, 4.0]
#NumBins represents total number of bins   
indexf = (alldataf['mass'] > masslim[0]) * (alldataf['mass'] < masslim[1])
indexg = (alldatag['mass'] > masslim[0]) * (alldatag['mass'] < masslim[1]) #* (alldatag['gd'] < 0.5*alldatag['R200'])

#HISTOGRAM ANALYSIS============================
pl.close()
fig, ax = pl.subplots(2, 1, figsize = (8, 16))#, sharey=True)
fig.subplots_adjust(left=0.09, right=0.98, wspace=0.15, top=0.95, bottom=0.05)

meang = np.average(np.log10(alldatag['radius'][indexg]), weights = alldatag['gp'][indexg])
varg = np.average(((np.log10(alldatag['radius'][indexg]))-meang)**2)
stdg = np.sqrt(varg)
meanf = (np.log10(alldataf['radius'][indexg])).mean()
stdf = (np.log10(alldataf['radius'][indexg])).std()

allbing, binsg, patchg = ax[0].hist(np.log10(alldatag['radius'][indexg]), bins=12, weights=alldatag['gp'][indexg], label=str(indexg.sum())+' group entries \n'+'Weighted Mean: '+str(np.around(meang, decimals=4))+'\n'+r'Weighted $\sigma$: '+str(np.around(stdg, decimals=4)))
                                                  
allbinf, binsf, patchf = ax[1].hist(np.log10(alldataf['radius'][indexf]), bins=20, label=str(indexf.sum())+' field entries \n'+'Mean: '+str(np.around(meanf, decimals=4))+'\n'+r'$\sigma$: '+str(np.around(stdf, decimals=4)))

#perform K-S 2 samp test
D, p = stats.ks_2samp(np.log10(alldatag['radius'][indexg]),np.log10(alldataf['radius'][indexf]))

#fig.suptitle(str(masslim[0])+r'$ < \log(M_* \, M_{\odot}) < $'+str(masslim[1])+'\n K-S 2samp D = '+str(D)+' p-value = '+str(p), fontsize=16)

print ('K-S 2samp D = '+str(D)+' p-value = '+str(p))

ax[0].set_ylabel('Frequency')
ax[1].set_ylabel('Frequency')
ax[1].set_xlabel(r'$R_e (kpc)$')

ax[0].set_xlim(0.0, 2.5)
#ax[0].set_ylim(0.0, 30.0)
ax[1].set_xlim(0.0, 2.5)

legend = ax[0].legend(loc='upper right', fontsize=13)
legend.draw_frame(False)
legend = ax[1].legend(loc='upper right', fontsize=13)
legend.draw_frame(False)
    
