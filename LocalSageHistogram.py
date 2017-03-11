import numpy as np
import matplotlib.pyplot as plt
from sage.all import *

class LocalHistogram(object):

     def __init__(self, hdata, bins, xran = None, cumulative = False, probability = True, 
                  rgbcolor = 'darkorange', legend_label = "", thickness = 1.0, 
                  aspect_ratio = 'automatic'): 
                  
          histy, histx = np.histogram(np.array(hdata), bins = bins, 
                                      density = True, #density = not probability, 
                                      range = xran)
          histx, histy = map(list, [histx, histy])
          if probability: 
               total_points = sum(histy)
               histy = list(np.array(histy) / float(total_points))
          ##
          if cumulative: 
               yd = np.array(histy)
               yd = [yd[0:idx+1] for idx in range(0, len(histy))]
               histy = map(sum, yd)
          ##
          
          self._histx = histx
          self._histy = histy
          self._hist_points = zip(histx, histy)
          
          if xran != None: 
               xmin, xmax = xran
               self._hist_points = \
                    list(filter(lambda (x, y): x>=xmin and x<=xmax, self._hist_points))
               self._histx = np.array(self._hist_points)[:,0]
               self._histy = np.array(self._hist_points)[:,1]
          ##      
          self._plthist = plot_step_function(self._hist_points, vertical_lines = True, 
                                            thickness = thickness, rgbcolor = rgbcolor, 
                                            aspect_ratio = aspect_ratio, 
                                            legend_label = legend_label)
     ##
     
     def get_histogram_plot(self):
          return self._plthist
     ##
     
     @property
     def histx(self):
          return self._histx
     ##
     
     @property
     def histy(self):
          return self._histy
     ##
     
     @property
     def hist_points(self):
          return self._hist_points
     ##
     
     def compute_derivative_list(self): 
          plot_points = self.hist_points
          deriv_points = []
          for i in range(1, len(plot_points), 3): 
               (x1, y1), (x2, y2) = plot_points[i-1], plot_points[i]
               deriv_approx = (y2 - y1) / (x2 - x1)
               deriv_points += [((x1 + x2) / 2.0, deriv_approx)]
          ##
          return deriv_points     
     ##
     
##

