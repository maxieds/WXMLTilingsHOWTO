#### AmmannChair.py 
#### Implementation of the first (A2) Amann chair tiling
#### Author: Maxie D. Schmidt
#### Created: 2016.02.23 

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling 

##
 # Python constants to denote the individual tile types in the 
 # substitution tiling
##
LA3_TILE = 1; 
SA3_TILE = 2

## gamma
 # A python float of the square root of the golden ratio
##
#gamma = float(golden_ratio ** 0.5); 
#gamma = var('gamma')
#gamma = sqrt(golden_ratio)

## AmmannChair_Tiling
 # A Tiling subclass implementing the Ammann Chair tiling 
 # See: http://demonstrations.wolfram.com/AmmannChair/
##
class AmmannChair_Tiling(Tiling): 

     ## __init__ 
      # Initialization function for the AmmannChair_Tiling class
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "AmmannChair")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "AmmannChair", 
                  gamma = float(golden_ratio ** 0.5)): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               (gamma ** 5) * vector([1, 0]), 
               (gamma ** 5) * vector([1, 0]) + (gamma ** 4) * vector([0, 1]), 
               ((gamma ** 5) - gamma) * vector([1, 0]) + \
               (gamma ** 4) * vector([0, 1]), 
               ((gamma ** 5) - gamma) * vector([1, 0]) + \
               (gamma ** 6) * vector([0, 1]), 
               (gamma ** 6) * vector([0, 1]), 
          ]; 
          self.LOP = AffineTransformOp((gamma ** -1) * matrix([[0, -1], [1, 0]]), \
                                       (gamma ** 5) * vector([1, 0])); 
          self.SOP = AffineTransformOp((gamma ** -2) * matrix([[1, 0], [0, -1]]), \
                                       (gamma**6) * vector([0, 1])); 
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Ammann A2 chair tiling"; 
     
     ## get_initial_tile 
      # Returns a tile of points in the Golden L
     ##
     def get_initial_tile(self): 
          return self.INIT_TILE; 
     
     ## get_next_tiling
      # Gets the next list of tiles after one subsequent substitution step
      # @param prev_tiles        A list of the tiles after one step back
      # @param second_prev_tiles A list of the tiles two steps back
      # @return                  A list of tiles after one more step
     ##
     def get_next_tiling(self, prev_tiles, second_prev_tiles = []): 
          rpts = Tiling.transform_full_points_list(prev_tiles, self.LOP); 
          rpts.extend(Tiling.transform_full_points_list(second_prev_tiles, self.SOP));
          return rpts;  
     ## def 
     
     ## get_tiles
      # Gets the polygonal Ammann Chair tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          init_tile = self.INIT_TILE; 
          prev_tiles = [init_tile];
          pprev_tiles = [init_tile]; 
          for n in range(1, self.N): 
               next_tiles = self.get_next_tiling(prev_tiles, pprev_tiles); 
               pprev_tiles = prev_tiles; 
               prev_tiles = next_tiles; 
          ## for 
          return prev_tiles; 
     ## def 

## class 

