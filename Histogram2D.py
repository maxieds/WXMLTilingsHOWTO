import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sage.all import *
from sage.plot.histogram import Histogram

def DensityHistogram(xypoints, numbins):

     xpoints = map(lambda (x, y): x, xypoints)
     ypoints = map(lambda (x, y): y, xypoints)
     minx, maxx, miny, maxy = min(xpoints), max(xpoints), \
                              min(ypoints), max(ypoints)
     xedges = np.arange(minx, maxx, (maxx - minx) / float(numbins))
     yedges = np.arange(miny, maxy, (maxy - miny) / float(numbins))
     H, xedges, yedges = np.histogram2d(ypoints, xpoints, bins = (xedges, yedges))
     
     fig = plt.figure(figsize=(7, 3))
     ax = fig.add_subplot(132)
     ax.set_title('pcolormesh: exact bin edges')
     X, Y = np.meshgrid(xedges, yedges)
     ax.pcolormesh(X, Y, H)
     ax.set_aspect('equal')
     #plt.savefig('./output/foo.png', bbox_inches='tight')
     #plt.show()

     g = histogram([xpoints, ypoints])
     g.save('./output/foo2.png')

## def

def get_xybin_value(x, y, xedges, yedges, hist_data): 
     xbin_idx = np.digitize([x], xedges, right = False)
     ybin_idx = np.digitize([y], yedges, right = False)
     if xbin_idx <= len(xedges) - 1 and ybin_idx <= len(yedges) - 1 and \
        xbin_idx < len(hist_data) and ybin_idx < len(hist_data[xbin_idx - 1]): 
          return hist_data[ybin_idx - 1][xbin_idx - 1]
     else: 
          return 0.0
##

def Histogram3D(xypoints, numbins):

     xpoints = map(lambda (x, y): x, xypoints)
     ypoints = map(lambda (x, y): y, xypoints)
     minx, maxx, miny, maxy = min(xpoints), max(xpoints), \
                              min(ypoints), max(ypoints)
     dx, dy = (maxx - minx) / float(numbins), (maxy - miny) / float(numbins)
     xedges = [0.0] + np.arange(minx, maxx + dx, dx)
     yedges = [0.0] + np.arange(miny, maxy + dy, dy)
     H, xedges, yedges = np.histogram2d(ypoints, xpoints, 
                                        bins = (xedges, yedges), 
                                        normed = False)
     
     print H, len(H), len(H[0]), type(H)
     print xedges, len(xedges)
     print yedges, len(yedges)

     plt.figure(1)
     plt.subplot(211)
     extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
     plt.imshow(H, extent = extent, interpolation = 'nearest')
     plt.colorbar()
     plt.savefig('./output/foo-density-hist3d.png')

     plt.subplot(212)
     xidx = np.clip(np.digitize(xpoints, xedges), 0, H.shape[0]-1)
     yidx = np.clip(np.digitize(ypoints, yedges), 0, H.shape[1]-1)
     c = H[xidx, yidx]
     print c
     plt.scatter(xpoints, ypoints, c=c, alpha = 0.5)
     plt.colorbar()
     plt.savefig('./output/foo-density-scatter.png')

     plt.figure(2)
     plt.hexbin(xpoints, ypoints)
     plt.colorbar()
     plt.savefig('./output/foo-mpl-combined.png')

     hist_fxy = lambda x, y: get_xybin_value(x, y, xedges, yedges, H)
     P = plot3d(hist_fxy, (minx, maxx), (miny, maxy), adaptive = True, 
                color = rainbow(60, 'rgbtuple'), max_bend = 0.1, 
                max_depth = 15, mesh = False, aspect_ratio = 1)
     P.save('./output/foo-hist3d.png')
     
     list_plot3d_data = []
     for x in xedges: 
          for y in yedges:
               list_plot3d_data += [(x, y, get_xybin_value(x, y, xedges, yedges, H))]
          ##
     ##
     LP = list_plot3d(list_plot3d_data)
     LP.save('./output/foo-listplot3d-hist3d.png')


## def





