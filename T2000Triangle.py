#### T2000Triangle.py 
#### Implementation of the T2000 triangle tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/t2000/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.25

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y, solve_system

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
BTILE = 1; 
LBTILE = 2; 

## See: http://stackoverflow.com/questions/5922027/how-to-determine-if-a-point-is-within-a-quadrilateral
def contained_in_triangle(P, A, B, C):
     v0 = C - A
     v1 = B - A
     v2 = P - A
     dot00, dot01, dot02, dot11, dot12 = v0.inner_product(v0), \
            v0.inner_product(v1), v0.inner_product(v2), v1.inner_product(v1), \
            v1.inner_product(v2)
     invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
     u = (dot11 * dot02 - dot01 * dot12) * invDenom
     v = (dot00 * dot12 - dot01 * dot02) * invDenom
     return u >= 0 and v >= 0 and 1 >= u + v 
## def

## THTriangleTile
 # A class that represents the triangular tiles in the triangle tiling
##
class T2000TriangleTile(object): 

     ## __init__
      # Initialization function for the THTriangleTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of WTILE or BTILE
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
          if self.tile_type == LBTILE: 
               return[ 
                    T2000TriangleTile(BTILE, 
                                      pa = A, 
                                      pb = B, 
                                      pc = C), 
               ]; 
          else: # BTILE 
               M1 = A * 2.0 / 3.0 + B / 3.0
               M2 = A / 3.0 + B * 2.0 / 3.0
               mp12 = (M1 + M2) / 2.0
               M3 = mp12 * 2.0 / 3.0 + C / 3.0
               return[ 
                    T2000TriangleTile(BTILE, 
                                      pa = C, 
                                      pb = A, 
                                      pc = M1), 
                    T2000TriangleTile(LBTILE, 
                                      pa = M1, 
                                      pb = M2, 
                                      pc = M3), 
                    T2000TriangleTile(LBTILE, 
                                      pa = C, 
                                      pb = M1, 
                                      pc = M3), 
                    T2000TriangleTile(LBTILE, 
                                      pa = M2, 
                                      pb = C, 
                                      pc = M3), 
                    T2000TriangleTile(BTILE, 
                                      pa = B, 
                                      pb = C, 
                                      pc = M2),
               ]; 
          ##           
     ## def 

## class 

## T2000Triangle_Tiling
 # A Tiling subclass implementing the T2000 substitution tiling 
##
class T2000Triangle_Tiling(Tiling): 

     ## __init__
      # Initialization function for the T2000Triangle_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "T2000Triangle")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "T2000Triangle"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          
          sidex = 10
          self.INIT_TILE = [
               vector([0, 0]), # pa
               vector([4 * sidex, 0]), # pb
               vector([2 * sidex, sidex]), # pc
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the T2000 triangular tiling"; 
     
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
          init_gt_tile = T2000TriangleTile(LBTILE, init_tile[0], init_tile[1], init_tile[2]); 
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

