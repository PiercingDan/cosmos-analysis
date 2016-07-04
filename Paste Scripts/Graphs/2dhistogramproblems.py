#CORRECT!!!!

xvalues = np.array([0.5])
yvalues = np.array([1.0])
#bin edges
xedges = np.linspace(-0.5, 2.5, 51)
yedges = np.linspace(0.0, 2.5, 36)
    
#why matplotlib, why u do this to me    
H, yedges1, xedges1 = np.histogram2d(yvalues, xvalues, bins=(yedges, xedges))    
    
#X, Y = np.meshgrid(xedges, yedges)  

pl.close()
fig, ax = pl.subplots(1, 1)
im=mpl.image.NonUniformImage(ax, interpolation='bilinear')
xcenters = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
ycenters = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
im.set_data(xcenters, ycenters, H)
ax.images.append(im)
ax.set_xlim(xedges[0], xedges[-1])
ax.set_ylim(yedges[0], yedges[-1])
ax.set_aspect('equal')

#ax.set_xlabel('V-J



