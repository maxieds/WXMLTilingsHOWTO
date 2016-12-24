#### SaddleConnectionGoldenL.py
#### Based on Sage worksheet code by Jayadev Athreya
#### See: "The gap distribution of slopes on the Golden L" by J. Athreya, 
####      J. Chaika, and S. Lelievre (2013)
#### Author: Maxie D. Schmidt
#### Created: 2016.03.15

from sage.all import *
from Tiling import Tiling, edist, V, X, Y

## 
 # Python float for the golden ratio
## 
u = float(golden_ratio); 
u = phi = var('phi')
u = golden_ratio

## 
 # Initial vector list for the iteration in compute_diagonals_first_octant
 # below
##
V00 = [vector([1, 0]), vector([0, 1])]
V00_v2 = [vector([1, 0]), vector([u, 1]), vector([u, u])]

def get_vector_slope(v): 
     if X(v) == 0: 
          return Y(v)
     else: 
          return float(Y(v) / X(v))
##

def vector_slope_cmp(v1, v2): 
     [slope1, slope2] = map(get_vector_slope, [v1, v2])
     if slope1 == slope2: 
          return 0
     elif slope1 < slope2:
          return -1
     else: 
          return 1
##

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
    if not V0: V0[:] = [vector([1, 0]), vector([0, 1])]

    #j=0
    #while j< len(V)-1:
    #    while (Rmax >= V[j][0] and Rmax >= V[j+1][0]):
    #        V[j+1:j+1] = [ u*V[j]+V[j+1], u*V[j]+u*V[j+1], V[j] + u*V[j+1]]
    #    j+=1
    j=0
    while j< len(V0)-1:
        while (Rmax >= edist(V0[j], V(0, 0)) and Rmax >= edist(V0[j+1], V(0, 0))):
            V0[j+1:j+1] = [ u*V0[j]+V0[j+1], V0[j]+V0[j+1], V0[j] + u*V0[j+1]]
        j+=1
    return V0;
    
def compute_diagonals_first_octant2(V0, Rmax = u):
    

    # if V0 is None: V0=V00[:] #this makes a copy of V00 which holds 
    # fixed throughout instead of modifying V00 
    # ([i:j] would give a copy of just from i to j)
    #if not V: V[:] = [vector([1, 0]), vector([u, 1]), vector([u, u])]
    if not V0: V0[:] = [vector([1, 0]), vector([0, 1])]

    originv, exit_loop = V(0, 0), False
    while not exit_loop:
         j = 0
         while j < len(V0) - 1:
              v, vnext = V0[j], V0[j+1]
              if Rmax < edist(v, originv) or Rmax < edist(vnext, originv):
                   exit_loop = True
                   break
              ##
              next_three = [u*v + vnext, v + vnext, v + u*vnext]
              v0[j:j] = next_three
              j += 3
         ##
         V0 = sorted(V0, cmp = vector_slope_cmp)
    ##
    
    return V0;
    
def compute_diagonals_first_octant_V2(V0, Rmax = u):
    

    # if V0 is None: V0=V00[:] #this makes a copy of V00 which holds 
    # fixed throughout instead of modifying V00 
    # ([i:j] would give a copy of just from i to j)
    if not V0: V[:] = [vector([1, 0]), vector([u, 1]), vector([u, u])]

    j=0
    while j< len(V0)-1:
        while (Rmax >= edist(V0[j], V(0, 0)) and Rmax >= edist(V0[j+1], V(0, 0))):
            V0[j+1:j+1] = [ u*V0[j]+V0[j+1], u*V0[j]+u*V0[j+1], V0[j] + u*V0[j+1]]
        j+=1
    return V0;
    
def compute_diagonals_first_octant2_V2(V0, Rmax = u):
    

    # if V0 is None: V0=V00[:] #this makes a copy of V00 which holds 
    # fixed throughout instead of modifying V00 
    # ([i:j] would give a copy of just from i to j)
    if not V0: V[:] = [vector([1, 0]), vector([u, 1]), vector([u, u])]
    V0 += map(lambda v: v / u, V0)

    originv, exit_loop = V(0, 0), False
    while not exit_loop:
         j = 0
         while j < len(V0) - 1:
              v, vnext = V0[j], V0[j+1]
              if Rmax < edist(v, originv) or Rmax < edist(vnext, originv):
                   exit_loop = True
                   break
              ##
              next_three = [u*v + vnext, u*v + u*vnext, v + u*vnext]
              next_six = next_three + [u + vnext / u, v + vnext, v / u + vnext]
              v0[j:j] = next_six
              j += 6
         ##
         V0 = sorted(V0, cmp = vector_slope_cmp)
    ##

    return V0;

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
          tiles = compute_diagonals_first_octant_V2(V00_v2, Rmax = self.num_steps); 
          #print V00; 
          return [tiles]; 

     ## def 
     
     def get_tiles_V2(self): 
          
          # we're going to define RMax to be N here: 
          #tiles = compute_diagonals_first_octant_V2(V00_v2, Rmax = self.num_steps); 
          tiles = compute_diagonals_first_octant2_V2(V00_v2, Rmax = self.num_steps); 
          #print V00; 
          return [tiles]; 

     ## def 

## class 
