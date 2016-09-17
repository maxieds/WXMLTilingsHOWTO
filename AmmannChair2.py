#### AmmannChair2.py 
#### Implementation of the second Amann chair tiling
#### Author: Maxie D. Schmidt
#### Created: 2016.02.23 

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling 

## AmmannChair2_Tiling
 # A Tiling subclass implementing the 4-tile chair substitution tiling 
 # See: http://tilings.math.uni-bielefeld.de/substitution_rules/chair
##
class AmmannChair2_Tiling(Tiling): 

     ## __init__
      # Initialization function for the AmmannChair2_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "AmmannChair2")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "AmmannChair2"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([1, 0]), 
               vector([1, 0.5]), 
               vector([0.5, 0.5]), 
               vector([0.5, 1]), 
               vector([0, 1]), 
          ]; 
          
          # affine transformations we use in the substitution steps to 
          # transform previous tiles in to the next subtiles:
          self.T1OP = AffineTransformOp(0.5 * matrix([[1, 0], [0, 1]]), 
                                        vector([0, 0])); 
          self.T2OP = AffineTransformOp(0.5 * matrix([[1, 0], [0, 1]]), 
                                        vector([0.25, 0.25])); 
          self.T3OP = AffineTransformOp(0.5 * matrix([[0, 1], [-1, 0]]), 
                                        vector([0, 1])); 
          self.T4OP = AffineTransformOp(0.5 * matrix([[-1, 0], [0, 1]]), 
                                        vector([1, 0])); 
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Second chair tiling variation"; 
     
     ## get_initial_tile
      # Returns the only tile in the tiling after zero steps
     ##
     def get_initial_tile(self): 
          return self.INIT_TILE; 
     
     ## get_next_tiling
      # Gets the next list of tiles after one subsequent substitution step
      # @param prev_tiles        A list of the tiles after one step back
      # @return                  A list of tiles after one more step
     ##
     def get_next_tiling(self, prev_tiles): 
          init_pts = prev_tiles; 
          rpts = Tiling.transform_full_points_list(init_pts, self.T1OP); 
          rpts.extend(Tiling.transform_full_points_list(init_pts, self.T2OP)); 
          rpts.extend(Tiling.transform_full_points_list(init_pts, self.T3OP)); 
          rpts.extend(Tiling.transform_full_points_list(init_pts, self.T4OP)); 
          return rpts; 
     ## def 
     
     ## get_tiles
      # Gets the polygonal AmmannChair2 tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          init_tile = self.get_initial_tile(); 
          tile_list = [init_tile]; 
          for n in range(1, self.N): 
               next_tiles_list = self.get_next_tiling(tile_list); 
               tile_list = next_tiles_list; 
          ## for 
          return tile_list; 
     ## def 

## class 

