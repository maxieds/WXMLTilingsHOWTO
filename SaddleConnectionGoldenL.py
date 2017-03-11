#### SaddleConnectionGoldenL.py
#### Based on Sage worksheet code by Jayadev Athreya
#### See: "The gap distribution of slopes on the Golden L" by J. Athreya, 
####      J. Chaika, and S. Lelievre (2013)
#### Author: Maxie D. Schmidt
#### Created: 2016.03.15

from scipy.optimize import curve_fit
from pylab import *
from scipy.stats.mstats import mquantiles
import numpy as np
from sage.all import *
from Tiling import Tiling, edist, V, X, Y

## 
 # Python float for the golden ratio
## 
#u = float(golden_ratio); 
#u = phi = var('phi')
u = golden_ratio

## 
 # Initial vector list for the iteration in compute_diagonals_first_octant
 # below
##
#V00 = [vector([1, 0]), vector([1, 1])]
V00 = [vector([1, 0]), vector([u, 1]), vector([u, u])]

## compute_diagonals_first_octant
 # Computes a list of saddle connections within a given radius, Rmax
 # @param V    An initial list of saddle connection vectors
 # @param Rmax A maxiumum radius for the computation
 # @return     A list of saddle connections within the given radius
##
def compute_diagonals_first_octant(V0, Rmax = u):
    

    # if V0 is None: V0=V00[:] #this makes a copy of V00 which holds 
    # fixed throughout instead of modifying V00 
    # ([i:j] would give a copy of just from i to j)
    #if not V: V[:] = [vector([1, 0]), vector([u, 1]), vector([u, u])]
    #if not V0: V0[:] = [vector([1, 0]), vector([1, 1])]
    if not V0: V0[:] = [vector([1, 0]), vector([u, 1]), vector([u, u])]

    #j=0
    #while j< len(V)-1:
    #    while (Rmax >= V[j][0] and Rmax >= V[j+1][0]):
    #        V[j+1:j+1] = [ u*V[j]+V[j+1], u*V[j]+u*V[j+1], V[j] + u*V[j+1]]
    #    j+=1
    j=0
    while j< len(V0)-1:
        while Rmax >= V0[j][0] and Rmax >= V0[j+1][0]:
            #V0[j+1:j+1] = [ u*V0[j]+V0[j+1], V0[j]+V0[j+1], V0[j] + u*V0[j+1]]
            V0[j+1:j+1] = [ u*V0[j]+V0[j+1], u*V0[j]+u*V0[j+1], V0[j] + u*V0[j+1]]
        j+=1
        print "j: %d, len(V0) = %d" % (j, len(V0))
    return V0;
##

## SaddleConnectionGoldenL
 # A Tiling subclass implemented to perform statistical computations on the 
 # saddle connections of the GoldenL
##
class SaddleConnectionGoldenL(Tiling): 

     ## __init__
      # Initialization function for the SaddleConnectionGoldenL class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "SaddleConnGoldenL")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "SaddleConnGoldenL"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = None;
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Implemented to perform stats on the GoldenL saddle connections"; 
     
     ## get_initial_tile
      # Returns the only tile in the tiling after zero steps
     ##
     def get_initial_tile(self): 
          return self.INIT_TILE; 
     
     ## get_tiles
      # Gets the single vertex polygonal SaddleConnGoldenL tiles after N steps
      # (we locally define the radius Rmax to be the tiling parameter N here)
      # @return A list of tiles in the computed "tiling"
     ##
     def get_tiles(self): 
          
          # we're going to define RMax to be N here: 
          tiles = compute_diagonals_first_octant(V00, Rmax = self.num_steps); 
          #rtiles = []
          #for tp in tiles: 
          #     rtiles += [tp, tp / u] # "long" and "short" vectors
          ##
          #rtiles = list(filter(lambda v: get_vector_slope(v) <= 1, tiles))
          tiles = list(filter(lambda (x, y): y <= x, tiles))
          return [tiles]; 

     ## def 

## class 

phi = golden_ratio

def ath(x): return 1 / 2.0 * log((1 + x) / (1 - x))
def r(x):   return sqrt(1 - 4.0 * x)

def f0inf(alpha): return 0
def f1inf(alpha): return (1 / (alpha**2)) * log(alpha)
def f2inf(alpha): return (1 / (alpha**2)) * (log(alpha) - 4.0 * ath(r(phi / alpha)))
def f3inf(alpha): return (1 / (alpha**2)) * (2.0 * log(1 / phi * alpha / 2.0) +\
                                             2.0 * log(1 - r(phi / alpha)))
def f0phi(alpha): return 0
def f1phi(alpha): return 1 / (alpha ** 2) * log(alpha / phi)
def f2phi(alpha): return 1 / (alpha ** 2) * (log(alpha / phi)- 4.0 * ath(r(1 / alpha)))
def f3phi(alpha): return 0

def f0one(alpha): return 0
def f1one(alpha): return 1 / (alpha ** 2) * log(alpha / phi)
def f2one(alpha): return 1 / (alpha ** 2) * (log(alpha / phi)- 2.0 * ath(r(1 / alpha / phi)))
def f3one(alpha): return 0

def finf_fitfunc(x): 
     single_var = False
     if isinstance(x, sage.symbolic.expression.Expression) or \
        isinstance(x, np.float64): 
          x = [x]
          single_var = True
     ##
     y = np.zeros(len(x))
     for (i, xi) in enumerate(x): 
          if xi <= 1: 
               y[i] = f0inf(xi)
          elif xi > 1 and xi <= 4 * phi:
               y[i] = f1inf(xi)
          elif xi > 4 * phi and xi <= phi**4:
               y[i] = f2inf(xi)
          else: 
               y[i] = f3inf(xi)
     ##
     if single_var: 
          y = y[0]
     ##
     return y
##

def fphi_fitfunc(x): 
     single_var = False
     if isinstance(x, sage.symbolic.expression.Expression) or \
        isinstance(x, np.float64): 
          x = [x]
          single_var = True
     ##
     y = np.zeros(len(x))
     for (i, xi) in enumerate(x): 
          if xi <= phi: 
               y[i] = f0phi(xi)
          elif xi > phi and xi <= 4.0:
               y[i] = f1phi(xi)
          elif xi > 4.0 and xi <= phi**3:
               y[i] = f2phi(xi)
          else: 
               y[i] = f3phi(xi)
     ##
     if single_var: 
          y = y[0]
     ##
     return y
##

def fone_fitfunc(x): 
     single_var = False
     if isinstance(x, sage.symbolic.expression.Expression) or \
        isinstance(x, np.float64): 
          x = [x]
          single_var = True
     ##
     y = np.zeros(len(x))
     for (i, xi) in enumerate(x): 
          if xi <= phi: 
               y[i] = f0one(xi)
          elif xi > phi and xi <= 4.0 / phi:
               y[i] = f1one(xi)
          elif xi > 4.0 / phi and xi <= phi**2:
               y[i] = f2one(xi)
          else: 
               y[i] = f3one(xi)
     ##
     if single_var: 
          y = y[0]
     ##
     return y
##

def sc_fitfunc(x): 
     ydata = finf_fitfunc(x) + fphi_fitfunc(x) + fone_fitfunc(x)
     return ydata
##

def SaddleConnGoldenL_finfinity(x): 
     I0, I1, I2, I3 = (0, 1), (1, 4.0 * phi), (4.0 * phi, phi ** 4), (phi ** 4, infinity)
     f0x, f1x, f2x, f3x = f0inf(x), f1inf(x), f2inf(x), f3inf(x)
     return piecewise([(I0, f0x), (I1, f1x), (I2, f2x), (I3, f3x)])
##

MAX_FIT_POINTS = 100

def fit_SaddleConnGoldenL_pdf(hist_data, xdata, ydata, hrange): 
     
     [sl, su] = hrange
     [fl, fu] = [2.3528, 8.1976]
     b = (fu - fl) / (su - sl)
     c = fu - b * su
     #if len(xdata) > 2 * MAX_FIT_POINTS: # trim to the middle 9000 x values
     #     idxl, idxu = len(xdata) / 2 - MAX_FIT_POINTS/4, len(xdata) / 2 + MAX_FIT_POINTS/4
     #     endu = len(xdata) - MAX_FIT_POINTS / 4 - 1
     #     xdata = list(xdata)[idxl:idxu+1] + list(xdata)[0:MAX_FIT_POINTS/4+1] + list(xdata)[endu:]
     #     ydata = list(ydata)[idxl:idxu+1] + list(ydata)[0:MAX_FIT_POINTS/4+1] + list(ydata)[endu:]
     ##
     # it appears that scipy has a bug, let's do an adjustment to make it go away:
     if len(ydata) - len(xdata) == 1:
          ydata = ydata[:-1]
     ##
     
     fit_func_v1 = lambda x, a, b, c, d: a * sc_fitfunc(b*x+c) + d
     fit_func = lambda x, a, d: fit_func_v1(x, a, b, c, d)
     p, pcov = curve_fit(fit_func, xdata, ydata)#, bounds = ([0,0], [10,10]))
     print p, pcov
     return lambda x: fit_func(x, p[0], p[1]), (1 - c) / b, [p[0], b, c, p[1]]
     
##
