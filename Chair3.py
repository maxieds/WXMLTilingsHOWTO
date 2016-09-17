#### Chair3.py 
#### Implementation of the third chair tiling variant
#### See: http://tilings.math.uni-bielefeld.de/substitution_rules/chair_variant_9_tiles
#### Author: Maxie D. Schmidt
#### Created: 2016.03.28

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling 

## 
 # Python floats for constants we use as shorthand in the code below
##
one_third = float(1 / 3.0);
one_sixth = float(1 / 6.0);

## Chair3_Tiling
 # A Tiling subclass implementing the 9-tile chair substitution tiling 
 # See: http://tilings.math.uni-bielefeld.de/substitution_rules/chair_variant_9_tiles
##
class Chair3_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Chair3_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Chair3")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Chair3"): 
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
          
          # affine transformations we use to generate tiles in the 
          # substitution steps:
          self.T1OP = AffineTransformOp(one_third * matrix([[1, 0], [0, 1]]), 
                                        vector([0, 0])); 
          self.T2OP = AffineTransformOp(one_third * matrix([[1, 0], [0, 1]]), 
                                        vector([one_sixth, one_sixth]));
          self.T3OP = AffineTransformOp(one_third * matrix([[1, 0], [0, 1]]), 
                                        vector([one_third, one_third]));                              
          self.T4OP = AffineTransformOp(one_third * matrix([[0, 1], [-1, 0]]), 
                                        vector([0, 2 * one_third])); 
          self.T5OP = AffineTransformOp(one_third * matrix([[0, 1], [-1, 0]]), 
                                        vector([0, 1])); 
          self.T6OP = AffineTransformOp(one_third * matrix([[0, 1], [-1, 0]]), 
                                        vector([2 * one_third, one_third + one_sixth]));                               
          self.T7OP = AffineTransformOp(one_third * matrix([[-1, 0], [0, 1]]), 
                                        vector([2 * one_third, 0])); 
          self.T8OP = AffineTransformOp(one_third * matrix([[-1, 0], [0, 1]]), 
                                        vector([1, 0])); 
          self.T9OP = AffineTransformOp(one_third * matrix([[-1, 0], [0, 1]]), 
                                        vector([0.5, 2 * one_third])); 
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Third chair tiling variation"; 
     
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
          rpts.extend(Tiling.transform_full_points_list(init_pts, self.T5OP)); 
          rpts.extend(Tiling.transform_full_points_list(init_pts, self.T6OP)); 
          rpts.extend(Tiling.transform_full_points_list(init_pts, self.T7OP)); 
          rpts.extend(Tiling.transform_full_points_list(init_pts, self.T8OP)); 
          rpts.extend(Tiling.transform_full_points_list(init_pts, self.T9OP)); 
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




