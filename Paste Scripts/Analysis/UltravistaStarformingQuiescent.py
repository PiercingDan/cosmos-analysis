#generates all quiescent entries
def UminusVmag(i):
    return -2.5*np.log10(ultravista['L153'][i]/ultravista['L155'][i])
        
def VminusJmag(i):
    return -2.5*np.log10(ultravista['L155'][i]/ultravista['L161'][i])

catname1 = 'ultravista'
colnames1 = {'U': 'L153', 'V': '155', 'J': '161', 'z': 'zp'}
colnameslist1 = list(colnames1.values())
data1 = {namekey: np.array(catalogues[catname1][namevalue]) for namekey, namevalue in colnames1.items()}


tempclass = []
for i in range(len(ultravista)):
    if UminusVmag(i) > 1.3 and VminusJmag(i) < 1.5:
        if ultravista['zp'][i] >= 0.0 and ultravista['zp'][i]<=1.0 and UminusVmag(i) > VminusJmag(i)*0.88 + 0.69: 
            #it is quiescent!
            tempclass.append('q')
        elif ultravista['zp'][i] > 1.0 and ultravista['zp'][i]<=4.0 and UminusVmag(i) > VminusJmag(i)*0.88 + 0.59: 
            #it is quiescent!
            tempclass.append('q')
        else:
            #Statforming!
            tempclass.append('sf')
    else:
        #it is not quiescent, it is starforming!
        tempclass.append('sf')
        
print('There are ', np.where(np.array(tempclass)=='sf')[0].size, ' star-forming galxies')
print ('There are ', np.where(np.array(tempclass)=='q')[0].size, ' quiescent galxies')
print ('There are ', np.where(np.array(tempclass)=='nan')[0].size, ' null entries')
        
        
ultravista.add_column(Column(name='Class_2', data=tempclass))         


    