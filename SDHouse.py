#### SDHouse.py 
#### Implementation of the semi-detached house tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/semi-detached-house/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.15 

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
RED_TILE = 1; 
BLUE_TILE = 2; 

## SDHouseTile
 # A class that represents the triangular tiles in the tiling
##
class SDHouseTile(object): 

     ## __init__
      # Initialization function for the SDHouseTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of RED_TILE or BLUE_TILE
      # @param pa        The vector coordinate of the vertex A in the quadrilateral
      # @param pb        The vector coordinate of the vertex B in the quadrilateral
      # @param pc        The vector coordinate of the vertex C in the quadrilateral
      # @param pd        The vector coordinate of the vertex D in the quadrilateral
     ##
     def __init__(self, tile_type, pa, pb, pc, pd): 
          self.tile_type = tile_type; 
          self.pa = pa; 
          self.pb = pb; 
          self.pc = pc; 
          self.pd = pd
     ## def 

     ## to_points
      # Returns a list of the vertex point vectors in the tile
     ##
     def to_points(self): 
          return [self.pa, self.pb, self.pc, self.pd]; 
     ## def 
     
     ## to_subtiles
      # Returns a list of golden triangle subtiles after one more 
      # substitution step
     ##
     def to_subtiles(self): 
          A, B, C, D = self.pa, self.pb, self.pc, self.pd
          if self.tile_type == RED_TILE: 
               return [SDHouseTile(BLUE_TILE, A, B, C, D)];
          else: # BLUE_TILE 
               M1, M3, M4 = (A + D) / 2.0, (B + C) / 2.0, (A + B) / 2.0
               M2 = (A + M1) / 2.0
               P = (M2 + M3) / 2.0
               return [ 
                    SDHouseTile(RED_TILE, 
                                pa = A, 
                                pb = M4, 
                                pc = P, 
                                pd = M1), 
                    SDHouseTile(RED_TILE, 
                                pa = B, 
                                pb = M4, 
                                pc = P, 
                                pd = C), 
                    SDHouseTile(BLUE_TILE, 
                                pa = C, 
                                pb = P, 
                                pc = M1, 
                                pd = D), 
               ]; 
          ##           
     ## def 

## class 

## SDHouse_Tiling
 # A Tiling subclass implementing the semi-detached house substitution tiling 
##
class SDHouse_Tiling(Tiling): 

     ## __init__
      # Initialization function for the SDHouse_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "SDHouse")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "SDHouse"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), # pa
               vector([10, 0]), # pb
               vector([10, 10]), # pc
               vector([0, 20]), #pd
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the semi-detached house tiling"; 
     
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
          init_gt_tile = SDHouseTile(RED_TILE, init_tile[0], init_tile[1], \
                                     init_tile[2], init_tile[3]); 
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

