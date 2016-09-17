#### SaddleConnectionGoldenL.py
#### Based on Sage worksheet code by Jayadev Athreya
#### See: "The gap distribution of slopes on the Golden L" by J. Athreya, 
####      J. Chaika, and S. Lelievre (2013)
#### Author: Maxie D. Schmidt
#### Created: 2016.03.15

from sage.all import *
from Tiling import Tiling, edist

## 
 # Python float for the golden ratio
## 
u = float(golden_ratio); 

## 
 # Initial vector list for the iteration in compute_diagonals_first_octant
 # below
##
V00 = [vector([1, 0]), vector([u, 1]), vector([u, u])]

## compute_diagonals_first_octant
 # Computes a list of saddle connections within a given radius, Rmax
 # @param V    An initial list of saddle connection vectors
 # @param Rmax A maxiumum radius for the computation
 # @return     A list of saddle connections within the given radius
##
def compute_diagonals_first_octant(V, Rmax = u):
    

    # if V0 is None: V0=V00[:] #this makes a copy of V00 which holds 
    # fixed throughout instead of modifying V00 
    # ([i:j] would give a copy of just from i to j)
    if not V: V[:] = [vector([1, 0]), vector([u, 1]), vector([u, u])]

    j=0
    while j< len(V)-1:
        while (Rmax >= V[j][0] and Rmax >= V[j+1][0]):
            V[j+1:j+1] = [ u*V[j]+V[j+1], u*V[j]+u*V[j+1], V[j] + u*V[j+1]]
        j+=1
    return V;

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
          #print V00; 
          return [tiles]; 

     ## def 

## class 
