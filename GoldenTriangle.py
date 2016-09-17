#### GoldenTriangle.py 
#### Implementation of the golden triangle tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution_rules/golden_triangles
#### Author: Maxie D. Schmidt
#### Created: 2016.02.25 

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
G1_TILE = 1; 
G2_TILE = 2; 

##
 # Defines the golden ratio (or phi) constant as a Python float
##
phi = float(golden_ratio); 

## GoldenTriangleTile
 # A class that represents the triangular tiles in the golden triangle tiling
##
class GoldenTriangleTile(object): 

     ## __init__
      # Initialization function for the GoldenTriangleTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of G1_TILE or G2_TILE
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
          if self.tile_type == G1_TILE: 
               return [GoldenTriangleTile(G2_TILE, phi * self.pa, 
                                          phi * self.pb, phi * self.pc)]; 
          else: # G2_TILE 
               midpoint = phi * self.pa + (self.pb - self.pa); 
               return [ 
                    GoldenTriangleTile(G1_TILE, 
                                       pa = phi * self.pc, 
                                       pb = phi * self.pb, 
                                       pc = midpoint), 
                    GoldenTriangleTile(G2_TILE, 
                                       pa = phi * self.pa, 
                                       pb = phi * self.pc, 
                                       pc = midpoint), 
               ]; 
          ##           
     ## def 

## class 

## GoldenTriangle_Tiling
 # A Tiling subclass implementing the golden triangle substitution tiling 
 # See: http://tilings.math.uni-bielefeld.de/substitution_rules/golden_triangles
##
class GoldenTriangle_Tiling(Tiling): 

     ## __init__
      # Initialization function for the GoldenTriangle_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "GoldenTriangle")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "GoldenTriangle"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 1]), # pa
               vector([phi / float(sqrt(2)), -float(sqrt(abs(1 - (phi ** 2) / 2)))]), # pb
               vector([0, 0]), # pc
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Golden triangle tiling"; 
     
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
          init_gt_tile = GoldenTriangleTile(G1_TILE, init_tile[0], init_tile[1], init_tile[2]); 
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

