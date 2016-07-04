def gendata(catname, columns, groupprob=None,zcol=None ,zrange=None):
    if zrange is None:
        gen = genentries(catname, columns, 'morph_zurich', ['R_GIM2D'], 'zp')
    else:  
        gen = genentries(catname, ['log10_M', 'zp', 'Class'],'morph_zurich', ['R_GIM2D'], 'zp', zrange)
    
    cat = catalogues[catname]
    mat = cat['morph_zurich'+'_match']    
    tempsfarray = np.empty([1, 2])
    tempqarray = np.empty([1, 2])
    if groupprob == False:
        for i in gen:
            mass = cat['log10_M'][i]
            #rawarad is the radius in arcsec
            rawrad = morph_zurich['R_GIM2D'][mat[i]]
            z = cat['zp'][i]
            rad = np.log10((rawrad*u.arcsec).to(u.rad)*(Distance(z=z, cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
            Type = cat['Class'][i]
            if Type == 'sf':
                tempsfarray = np.concatenate((tempsfarray, [[mass, rad]]))
            else:
                tempqarray = np.concatenate((tempqarray, [[mass, rad]]))
    else:
        for i in gen:
            mass = cat['log10_M'][i]
            #rawarad is the radius in arcsec
            rawrad = morph_zurich['R_GIM2D'][mat[i]]
            z = cat['zp'][i]
            rad = np.log10((rawrad*u.arcsec).to(u.rad)*(Distance(z=z, cosmology=cosmology.WMAP9).to(u.kpc))/(u.kpc*u.rad))
            Type = cat['Class'][i]
            #Group Probability Column
            if cat['zp_prob'][i] >= groupprob:
                if Type == 'sf':
                    tempsfarray = np.concatenate((tempsfarray, [[mass, rad]]))
                else:
                    tempqarray = np.concatenate((tempqarray, [[mass, rad]]))        
    #Deleting placeholder    
    tempsfarray = np.delete(tempsfarray, 0, axis=0)   
    tempqarray = np.delete(tempqarray, 0, axis=0) 
    return [tempsfarray, tempqarray]