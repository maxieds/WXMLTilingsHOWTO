#### Equithirds.py 
#### Implementation of the equithirds equilateral triangle tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/equithirds/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.11 

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
ETILE = 1; 
OTILE = 2; 

## ETriangleTile
 # A class that represents the triangular tiles in the tri-triangle tiling
##
class ETriangleTile(object): 

     ## __init__
      # Initialization function for the ETriangleTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of ETILE or OTILT
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
          A, B, C = self.pa, self.pb, self.pc     
          if self.tile_type == ETILE: 
               Ax, Bx, Ay, By = X(A), X(B), Y(A), Y(B)
               Mx = (By - Ay) / 2.0 / sqrt(3) + (Ax + Bx) / 2.0
               My = (Ax - Bx) / 2.0 / sqrt(3) + (Ay + By) / 2.0
               M = vector([Mx, My])
               return[ 
                    ETriangleTile(OTILE, 
                                  pa = B, 
                                  pb = M, 
                                  pc = A), 
                    ETriangleTile(OTILE, 
                                  pa = A, 
                                  pb = M, 
                                  pc = C), 
                    ETriangleTile(OTILE, 
                                  pa = C, 
                                  pb = M, 
                                  pc = B), 
               ]; 
          else: # OTILE 
               #M1, M2 = (A + C) / 3.0, (A + C) * 2.0 / 3.0
               Ax, Cx, Ay, Cy = X(A), X(C), Y(A), Y(C)
               M1x, M2x = 2 * Ax / 3.0 + Cx / 3.0, 2 * Cx / 3.0 + Ax / 3.0
               M1y, M2y = 2 * Ay / 3.0 + Cy / 3.0, 2 * Cy / 3.0 + Ay / 3.0
               M1, M2 = vector([M1x, M1y]), vector([M2x, M2y])
               return [ 
                    ETriangleTile(OTILE, 
                                  pa = A, 
                                  pb = M1, 
                                  pc = B), 
                    ETriangleTile(ETILE, 
                                  pa = M1, 
                                  pb = B, 
                                  pc = M2), 
                    ETriangleTile(OTILE, 
                                  pa = B, 
                                  pb = M2, 
                                  pc = C), 
               ]; 
          ##           
     ## def 

## class 

## ETTriangle_Tiling
 # A Tiling subclass implementing the tri-triangle substitution tiling 
##
class ETTriangle_Tiling(Tiling): 

     ## __init__
      # Initialization function for the ETTriangle_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Equithirds")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Equithirds"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          
          s = 25
          itA, itC = vector([0, 0]), vector([s, 0])
          itBx = X(0.5 * (itA + itC)) 
          itBy = sqrt(s ** 2  - itBx ** 2)
          self.INIT_TILE = [
               itA, # pa
               vector([itBx, itBy]), # pb
               itC, # pc
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the equithirds triangular tiling"; 
     
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
          init_gt_tile = ETriangleTile(ETILE, init_tile[0], init_tile[1], init_tile[2]); 
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

