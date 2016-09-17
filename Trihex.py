#### Trihex.py 
#### Implementation of the trihex 30-60-90 triangle tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/trihex/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.25

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
WTILE = 1; 
BTILE = 2; 

## THTriangleTile
 # A class that represents the triangular tiles in the triangle tiling
##
class THTriangleTile(object): 

     ## __init__
      # Initialization function for the THTriangleTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of WTILE or BTILT
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

     ## to_points
      # Returns a list of the vertex point vectors in the tile
     ##
     def to_points(self): 
          return [self.pa, self.pb, self.pc]; 
     ## def 
     
     ## to_subtiles
      # Returns a list of triangular subtiles after one more 
      # substitution step
     ##
     def to_subtiles(self): 
          A, B, C = self.pa, self.pb, self.pc     
          if self.tile_type == WTILE: 
               M1 = (A + C) / 2.0
               M2 = (B + C) / 2.0
               M3 = (A + M2) / 2.0
               return[ 
                    THTriangleTile(WTILE, 
                                   pa = M1, 
                                   pb = M2, 
                                   pc = C), 
                    THTriangleTile(BTILE, 
                                   pa = M1, 
                                   pb = M2, 
                                   pc = A), 
                    THTriangleTile(WTILE, 
                                   pa = M3, 
                                   pb = A, 
                                   pc = B), 
                    THTriangleTile(BTILE, 
                                   pa = M3, 
                                   pb = M2, 
                                   pc = B), 
               ]; 
          else: # BTILE 
               M1 = (A + C) / 2.0
               M2 = (B + C) / 2.0
               M3 = (A + M2) / 2.0
               return[ 
                    THTriangleTile(BTILE, 
                                   pa = M1, 
                                   pb = M2, 
                                   pc = C), 
                    THTriangleTile(WTILE, 
                                   pa = M1, 
                                   pb = M2, 
                                   pc = A), 
                    THTriangleTile(BTILE, 
                                   pa = M3, 
                                   pb = A, 
                                   pc = B), 
                    THTriangleTile(WTILE, 
                                   pa = M3, 
                                   pb = M2, 
                                   pc = B),
               ]; 
          ##           
     ## def 

## class 

## Trihex_Tiling
 # A Tiling subclass implementing the trihex substitution tiling 
##
class Trihex_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Trihex_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Trihex")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Trihex"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          
          sidex = 10
          self.INIT_TILE = [
               vector([0, 0]), # pa
               vector([sidex, 0]), # pb
               vector([0, 2 * sidex]), # pc
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the trihex triangular tiling"; 
     
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
          init_gt_tile = THTriangleTile(WTILE, init_tile[0], init_tile[1], init_tile[2]); 
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

