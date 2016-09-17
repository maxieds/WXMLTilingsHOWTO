#### Armchair.py 
#### Implementation of the pentomino tiling 
#### See:http://tilings.math.uni-bielefeld.de/substitution/pentomino/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.15

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling 

## 
 # Python floats for constants we use as shorthand in the code below
##

## Pentomino_Tiling
 # A Tiling subclass implementing the pentomino substitution tiling 
 # See: http://tilings.math.uni-bielefeld.de/substitution/pentomino/
##
class Pentomino_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Pentomino_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Pentomino")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Pentomino"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([10, 0]), 
               vector([10, 10]), 
               vector([5, 10]), 
               vector([5, 15]), 
               vector([0, 15]), 
          ];
          
          # affine transformations we use to generate tiles in the 
          # substitution steps:
          self.T1OP = AffineTransformOp(0.5 * matrix([[1, 0], [0, 1]]), 
                                        vector([0, 0])); 
          self.T2OP = AffineTransformOp(0.5 * matrix([[-1, 0], [0, 1]]), 
                                        vector([10, 0]));
          self.T3OP = AffineTransformOp(0.5 * matrix([[0, 1], [-1, 0]]), 
                                        vector([2.5, 10]));                              
          self.T4OP = AffineTransformOp(0.5 * matrix([[1, 0], [0, -1]]), 
                                        vector([0, 15]));  
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "A pentomino tiling"; 
     
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
      # Gets the polygonal Chair3 tiles after N steps
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

