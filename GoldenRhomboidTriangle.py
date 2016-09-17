#### GoldenRhomboidTriangle.py 
#### Implementation of the golden rhomboid triangle tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/golden-rhomboid-triangle/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.19 

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y, solve_system

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
YTILE = 1; 
OTILE = 2; 
BTILE = 3;

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

def contained_in_rhomb(P, A, B, C, D): 
     return contained_in_triangle(P, A, B, C) or \
            contained_in_triangle(P, A, C, D)
## def

## GRTriangleTile
 # A class that represents the triangular tiles in the golden rhomboid triangle tiling
##
class GRTriangleTile(object): 

     ## __init__
      # Initialization function for the ETriangleTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of YTILE or OTILE or BTILE
      # @param pa        The vector coordinate of the vertex A in the triangle
      # @param pb        The vector coordinate of the vertex B in the triangle
      # @param pc        The vector coordinate of the vertex C in the triangle
      # @param pd        The vector coordinate of the vertex D in the quadrilateral
     ##
     def __init__(self, tile_type, pa, pb, pc, pd = None): 
          self.tile_type = tile_type; 
          self.pa = pa; 
          self.pb = pb; 
          self.pc = pc; 
          self.pd = pd;
     ## def 

     ## to_points
      # Returns a list of the vertex point vectors in the tile
     ##
     def to_points(self): 
          if self.tile_type == BTILE: 
               return [self.pa, self.pb, self.pc, self.pd]
          else:
               return [self.pa, self.pb, self.pc]
     ## def 
     
     ## to_subtiles
      # Returns a list of golden triangle subtiles after one more 
      # substitution step
     ##
     def to_subtiles(self): 
          A, B, C, D = self.pa, self.pb, self.pc, self.pd
          Ax, Bx, Cx, Dx, Ay, By, Cy, Dy = X(A), X(B), X(C), X(D), \
                                           Y(A), Y(B), Y(C), Y(D)
          if self.tile_type == YTILE: 
               return [
                    GRTriangleTile(OTILE, A, B, C)
               ];
          elif self.tile_type == OTILE: 
               M1 = A / 3.0 + C * 2.0 / 3.0
               M2 = B / 3.0 + C * 2.0 / 3.0
               M3 = A / 3.0 + B * 2.0 / 3.0
               return[ 
                    GRTriangleTile(YTILE, 
                                   pa = M1, 
                                   pb = M2, 
                                   pc = C), 
                    GRTriangleTile(OTILE, 
                                   pa = A, 
                                   pb = M3, 
                                   pc = M1), 
                    GRTriangleTile(BTILE, 
                                   pa = M3, 
                                   pb = B, 
                                   pc = M2, 
                                   pd = M1), 
               ]; 
          else: # BTILE 
               t = edist(A, B)
               #cond_func1 = lambda x, y: contained_in_triangle(vector([x, y]), A, B, C)
               cond_func1 = lambda x, y: n((Cy-By)/(Cx-Bx)*(x-Cx) + Cy, 2) == n(y, 2)
               #cond_func2 = lambda x, y: contained_in_triangle(vector([x, y]), A, C, D)
               cond_func2 = lambda x, y: n((Dy-Ay)/(Dx-Ax)*(x-Dx) + Dy, 2) == n(y, 2)
               [M1x, M1y] = solve_system([Bx, By], t, [Ax, Ay], t, cond_func1)
               [M2x, M2y] = solve_system([Ax, Ay], t, [M1x, M1y], t, cond_func2)
               M1, M2 = vector([M1x, M1y]), vector([M2x, M2y])
               return [ 
                    GRTriangleTile(BTILE, 
                                   pa = C, 
                                   pb = M1, 
                                   pc = M2, 
                                   pd = D), 
                    GRTriangleTile(OTILE, 
                                   pa = A, 
                                   pb = B, 
                                   pc = M1), 
                    GRTriangleTile(OTILE, 
                                   pa = A, 
                                   pb = M1, 
                                   pc = M2), 
               ]; 
          ##           
     ## def 

## class 

## GRTriangle_Tiling
 # A Tiling subclass implementing the substitution tiling 
##
class GRTriangle_Tiling(Tiling): 

     ## __init__
      # Initialization function for the GRTriangle_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "GRTriangle")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "GRTriangle"): 
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
          return "the golden rhomboid triangle tiling"; 
     
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
          init_gt_tile = GRTriangleTile(YTILE, init_tile[0], init_tile[2], init_tile[1]); 
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

