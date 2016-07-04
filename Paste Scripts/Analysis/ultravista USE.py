temparray = np.array([])
cat = ultravista_Main

for i in range(len(cat)):
    if cat['star'][i] != 1 and\
       cat['K_flag'][i] <= 3 and\
       cat['contamination'][i] != 1 and\
       cat['nan_contam'][i] < 3 and\
       -2.5*np.log10(cat['Ks'][i]) +25 < 23.4: 
        temparray = np.append(temparray, 1)
    else:
        temparray = np.append(temparray, 0)
        
print(temparray.sum())    

gen = (i for i in range(len(cat)) if cat['USE'][i]==1)
tempmag = np.array([])
tempmag2 = np.array([])
tempflag = np.empty([1, 4])

for i in gen:
    tempmag = np.append(tempmag, -2.5*np.log10(cat['Ks_tot'][i])+25)
    tempmag2 = np.append(tempmag2, -2.5*np.log10(cat['Ks'][i])+25)
    tempflag = np.concatenate((tempflag, [[cat['star'][i], cat['K_flag'][i], cat['contamination'][i], cat['nan_contam'][i]]]))
    
tempflag = np.delete(tempflag, 0, axis=0)    