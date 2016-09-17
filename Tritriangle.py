#### Tritriangle.py 
#### Implementation of the tri-triangle tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/tritriangle/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.09 

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
GREEN_TILE = 1; 
YELLOW_TILE = 2; 
LIME_TILE = 3;

##
 # Defines the golden ratio (or phi) constant as a Python float
##
phi = float(golden_ratio); 

## TriTriangleTile
 # A class that represents the triangular tiles in the tri-triangle tiling
##
class TriTriangleTile(object): 

     ## __init__
      # Initialization function for the TriTriangleTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of GREEN_TILE or YELLOW_TILE or LIME_TILE
      # @param pa        The vector coordinate of the vertex A in the triangle
      # @param pb        The vector coordinate of the vertex B in the triangle
      # @param pc        The vector coordinate of the vertex C in the triangle
     ##
     def __init__(self, tile_type, pa, pb, pc): 
          self.tile_type = tile_type; 
          self.pa = pa; 
          self.pb = pb; 
          self.pc = pc; 
     ## def 

     ## __str__
      # Returns a string representation of the points in the tile
     ##
     def __str__(self): 
          return "pa = " + str(self.pa) + ", pb = " + str(self.pc) + \
                 ", pc = " + str(self.pc); 
     ## def 

     ## to_points
      # Returns a list of the vertex point vectors in the tile
     ##
     def to_points(self): 
          return [self.pa, self.pb, self.pc]; 
     ## def 
     
     ## to_subtiles
      # Returns a list of golden triangle subtiles after one more 
      # substitution step
     ##
     def to_subtiles(self):      
          if self.tile_type == GREEN_TILE: 
               return [TriTriangleTile(YELLOW_TILE, self.pa, self.pb, self.pc)]; 
          elif self.tile_type == YELLOW_TILE: 
               return [TriTriangleTile(LIME_TILE, self.pa, self.pb, self.pc)]; 
          else: # LIME_TILE 
               midpthyp = 0.5 * (self.pa + self.pb)
               midptleg = 0.5 * (self.pa + self.pc)
               midpt1 = 0.5 * (midpthyp + self.pc)
               midpt2 = 0.5 * (self.pa + midpthyp)
               return [ 
                    TriTriangleTile(LIME_TILE, 
                                    pa = self.pb, 
                                    pb = self.pc, 
                                    pc = midpthyp), 
                    TriTriangleTile(GREEN_TILE, 
                                    pa = midptleg, 
                                    pb = self.pa, 
                                    pc = midpt2), 
                    TriTriangleTile(GREEN_TILE, 
                                    pa = midpthyp, 
                                    pb = midptleg, 
                                    pc = midpt2), 
                    TriTriangleTile(GREEN_TILE, 
                                    pa = midpthyp, 
                                    pb = midptleg, 
                                    pc = midpt1), 
                    TriTriangleTile(GREEN_TILE, 
                                    pa = self.pc, 
                                    pb = midptleg, 
                                    pc = midpt1), 
               ]; 
          ##           
     ## def 

## class 

## TriTriangle_Tiling
 # A Tiling subclass implementing the tri-triangle substitution tiling 
##
class TriTriangle_Tiling(Tiling): 

     ## __init__
      # Initialization function for the TriTriangle_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "TriTriangle")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "TriTriangle"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), # pa
               vector([10,0]), # pb
               vector([10, 10]), # pc
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "tri-triangle tiling"; 
     
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
          next_tiles = []; 
          for tile in prev_tiles: 
               subtiles = tile.to_subtiles(); 
               next_tiles.extend(subtiles); 
          ## for 
          return next_tiles; 
     ## def 
     
     ## get_tiles
      # Gets the polygonal GoldenTriangle tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          init_tile = self.get_initial_tile(); 
          init_gt_tile = TriTriangleTile(GREEN_TILE, init_tile[0], init_tile[2], init_tile[1]); 
          tile_list = [init_gt_tile]; 
          for n in range(1, self.N): 
               next_tiles_list = self.get_next_tiling(tile_list); 
               tile_list = next_tiles_list; 
          ## for 
          
          rtiles_list = []; 
          for (idx, gt_tile) in enumerate(tile_list): 
               rtiles_list.append(gt_tile.to_points()); 
          ## for 
          return rtiles_list; 

     ## def 

## class 

