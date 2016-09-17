#### Domino9Tile.py 
#### Implementation of the 9-tile domino tiling variant
#### See: http://tilings.math.uni-bielefeld.de/substitution/domino-variant-9-tiles/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.25

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling 

## Domino9Tile_Tiling
 # A Tiling subclass implementing the domino variant substitution tiling 
##
class Domino9Tile_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Pentomino_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Domino-9Tile")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Domino-9Tile"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([3, 0]), 
               vector([3, 6]), 
               vector([0, 6]), 
          ];
          
          atop1 = lambda xo, yo: \
                  AffineTransformOp(1 / 3.0 * matrix([[1, 0], [0, 1]]), \
                                    1 / 3.0 * vector([xo, yo]))
          atop2 = lambda xo, yo: \
                  AffineTransformOp(1 / 3.0 * matrix([[0, 1], [-1, 0]]), \
                                    1 / 6.0 * vector([xo, yo]))
          
          # affine transformations we use to generate tiles in the 
          # substitution steps:
          self.T1OP = atop1(6, 0)
          self.T2OP = atop1(0, 6)
          self.T3OP = atop1(6, 12)                              
          self.T4OP = atop2(0, 6)  
          self.T5OP = atop2(0, 12) 
          self.T6OP = atop2(6, 18)  
          self.T7OP = atop2(6, 24)
          self.T8OP = atop2(0, 30)  
          self.T9OP = atop2(0, 36)
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "9-tile domino tiling"; 
     
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

