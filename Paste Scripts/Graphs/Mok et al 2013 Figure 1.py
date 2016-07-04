#convert is converting between pixels and arcsecs, if the original data is in arcsecs or does not need conversion then convert = 1.0
#xvalues
cat1 = 'balogh_data'
col1 = 'log10_M'

typecol = 'Class'
typecolentries = ['sf', 'int', 'p']
groupcol = 'Group_ID'
zcol = 'z'
zrange = [0.8, 1.0]        
#Values x and y
values = {'sfMg': [], 'sfMf': [], 'intMg': [], 'intMf': [], 'pMg': [],  'pMf': []}        
        
#Generating index of non-masked values and within our redshift range
def genentries():
    for i in range(len(catalogues[cat1])):
       if catalogues[cat1][col1].mask[i] == False \
       and catalogues[cat1][typecol].mask[i] == False \
       and catalogues[cat1][zcol][i] >= zrange[0] \
       and catalogues[cat1][zcol][i] <= zrange[1]:
           yield i

gen = genentries()

for i in gen:
    if catalogues[cat1][typecol][i] == 'sf':
        if catalogues[cat1][groupcol].mask[i] == False:
            #it is in a group
            values['sfMg'] = np.append(values['sfMg'], catalogues[cat1][col1][i])
            
        else:
            #it isn't in a group
            values['sfMf'] = np.append(values['sfMf'], catalogues[cat1][col1][i]) 
            
    elif catalogues[cat1][typecol][i] == 'int':
        if catalogues[cat1][groupcol].mask[i] == False:
            values['intMg'] = np.append(values['intMg'], catalogues[cat1][col1][i])        
        else: 
            values['intMf'] = np.append(values['intMf'], catalogues[cat1][col1][i]) 
        
    elif catalogues[cat1][typecol][i] == 'p':
        if catalogues[cat1][groupcol].mask[i] == False:
            values['pMg'] = np.append(values['pMg'], catalogues[cat1][col1][i])
        else:        
            values['pMf'] = np.append(values['pMf'], catalogues[cat1][col1][i])
    else: 
        pass
    
    
#Binwidth Definition, N is number of bins
xdim = [9.2, 12.0]
N = 7
bins = np.linspace(xdim[0], xdim[1], N+1, endpoint=True)
          
#Do histogram first
pl.close()
fig = pl.figure()

groupmass = np.hstack((values['sfMg'], values['intMg'], values['pMg']))
fieldmass = np.hstack((values['sfMf'], values['intMf'], values['pMf']))

ng, histbinsg, patchesg = pl.hist(groupmass, bins+1E-6, histtype='bar')
nf, histbinsf, patchesf = pl.hist(fieldmass, bins+1E-6, histtype='bar')
   
   
           
#plotting
pl.close()
fig, ax = pl.subplots(1, 3, sharey=True)

#First plot
colorarray = ['blue', 'green', 'red']

xg = 0.5*(bins[:-1] + bins[1:])
xf = 0.5*(bins[:-1] + bins[1:])

finalvalues = np.array([xg])

#Sorting into appropiate arrays
for h in range(len(typecolentries)):
    Class = typecolentries[h]
    subplot = ax[h]
    color = colorarray[h]
    
    #g, f denotes group, field
    yg = np.zeros(N, dtype=int)
    yf = np.zeros(N, dtype=int)    
    
    for j in range(len(bins)-1):
        gen = genentries()
        
        for i in gen:
            if catalogues[cat1][col1][i] > bins[j] and catalogues[cat1][col1][i] <= bins[j+1] and catalogues[cat1][typecol][i]==Class:
                if catalogues[cat1][groupcol].mask[i] == False:
                    #it is in a group!
                    yg[j]+=1
                else:
                    #nope
                    yf[j]+=1
                
                
    subplot.plot(xg, yg/ng, color=color, linestyle='-', marker='o',  markerfacecolor=color, markeredgecolor=color, label='Groups')

    subplot.plot(xf, yf/nf, color=color, linestyle='--', marker='o',  markerfacecolor='none', markeredgecolor=color, label='Fields')

    subplot.set_xlabel(col1)
    subplot.set_ylabel('Fraction of '+Class+' Galaxies')
    subplot.ylim = (0.0, 1.0)   
    
    finalvalues = np.vstack((finalvalues, yg))
    finalvalues = np.vstack((finalvalues, yf))
    
    legend = subplot.legend(loc='upper right')
    legend.draw_frame(False)
    


