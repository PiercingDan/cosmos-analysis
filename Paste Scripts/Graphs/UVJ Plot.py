def UminusVmag(i):
    return -2.5*np.log10(ultravista_UVJ['L153'][i]/ultravista_UVJ['L155'][i])
        
def VminusJmag(i):
    return -2.5*np.log10(ultravista_UVJ['L155'][i]/ultravista_UVJ['L161'][i])

def ultravistagen (zlow=None, zupp=None):
    if zlow is None and zupp is None:
        for i in range(len(ultravista)):
            if ultravista['USE'][i] == 1:
            #ultravista['star'][i] != 0 and\
               #ultravista['K_flag'][i] <= 4 and\
               #ultravista['contamination'][i] != 1 and\
               #ultravista['nan_contam'][i] == 0 and\
               #ultravista['Ks_tot'][i] > 23.4:
                yield (i)
    else:
        for i in range(len(ultravista)):
            if ultravista['USE'][i] == 1 and\
              ultravista['zp'][i]>=zlow and\
              ultravista['zp'][i]<=zupp:
                yield (i)

xvalues, yvalues = (np.array([]), np.array([]))                

gen = genentries('ultravista', ['L155', 'L153']))



for i in gen:
    xvalues = np.concatenate((xvalues, [VminusJmag(i)]))
    yvalues = np.concatenate((yvalues, [UminusVmag(i)]))
    
    
#bin edges
xedges = np.linspace(-0.5, 2.5, 51)
yedges = np.linspace(0.0, 2.5, 36)
    
#why matplotlib, why u do this to me    
H, yedges, xedges = np.histogram2d(yvalues, xvalues, bins=(yedges, xedges))    
    
#X, Y = np.meshgrid(xedges, yedges)  

pl.close()
fig, ax = pl.subplots(1, 1)

#im=mpl.image.NonUniformImage(ax, interpolation='bilinear')
#xcenters = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
#ycenters = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
#im.set_data(xcenters, ycenters, H)
#ax.images.append(im)

#ax.set_xlim(xedges[0], xedges[-1])
#ax.set_ylim(yedges[0], yedges[-1])
X, Y = np.meshgrid(xedges, yedges)
ax.pcolormesh(X, Y, H, cmap='Greys')

#plotting cut lines
x1 = np.linspace(-0.5, 0.69318, 10)
x2 = np.linspace(0.69318, 1.5, 20)
x3 = 1.5*np.ones((15))

y1 = 1.3*np.ones((len(x1)))
y2 = x2*0.88+0.69
y3 = np.linspace(2.01, 2.5, len(x3))

ax.plot(x1, y1, 'black', lw=1.5)
ax.plot(x2, y2, 'black', lw=1.5)
ax.plot(x3, y3, 'black', lw=1.5)
ax.set_aspect('equal')

#ax.set_xlabel('V-J
