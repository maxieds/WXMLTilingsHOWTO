#### SquareTrianglePinwheel.py 
#### Implementation of the square triangle pinwheel variant substitution tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/square-triangle-pinwheel-variant/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.19

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y, solve_system

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
RED_TILE = 1; 
BLUE_TILE = 2; 
U_TILE = 3;

## See: http://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not
def contained_in_square(vxy, A, B, C, D): 
     AB, AM, BC, BM = A - B, A - vxy, B - C, B - vxy
     return 0 <= AB.inner_product(AM) and \
            AB.inner_product(AM) <= AB.inner_product(AB) and \
            0 <= BC.inner_product(BM) and \
            BC.inner_product(BM) <= BC.inner_product(BC)
## def

## STPinwheelTile
 # A class that represents the triangular and square tiles in the tiling
##
class STPinwheelTile(object): 

     ## __init__
      # Initialization function for the STPinwheelile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of RED_TILE or BLUE_TILE
      # @param pa        The vector coordinate of the vertex A in the quadrilateral
      # @param pb        The vector coordinate of the vertex B in the quadrilateral
      # @param pc        The vector coordinate of the vertex C in the quadrilateral
      # @param pd        The vector coordinate of the vertex D in the quadrilateral (optional)
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
          if self.tile_type == RED_TILE or self.tile_type == U_TILE:
               return [self.pa, self.pb, self.pc];
          else:
               return [self.pa, self.pb, self.pc, self.pd]; 
     ## def 
     
     ## to_subtiles
      # Returns a list of golden triangle subtiles after one more 
      # substitution step
     ##
     def to_subtiles(self): 
          A, B, C, D = self.pa, self.pb, self.pc, self.pd
          Ax, Bx, Cx, Dx = X(A), X(B), X(C), X(D)
          Ay, By, Cy, Dy = Y(A), Y(B), Y(C), Y(D)
          if self.tile_type == BLUE_TILE: 
               s = edist(A, B)
               s0 = n(sqrt(5)) / 5.0 * s
               cond_func = lambda x, y: contained_in_square(vector([x, y]), A, B, C, D)
               [SCx, SCy] = solve_system([Cx, Cy], s0, [Dx, Dy], 2.0 * s0, cond_func)
               [SBx, SBy] = solve_system([Bx, By], s0, [Cx, Cy], 2.0 * s0, cond_func)
               [SAx, SAy] = solve_system([Ax, Ay], s0, [SBx, SBy], s0, cond_func)
               [SDx, SDy] = solve_system([SAx, SAy], s0, [Ax, Ay], 2.0 * s0, cond_func)
               SA, SB, SC, SD = vector([SAx, SAy]), vector([SBx, SBy]), \
                                vector([SCx, SCy]), vector([SDx, SDy])
               return [
                    STPinwheelTile(BLUE_TILE, 
                                   pa = SB, 
                                   pb = SC, 
                                   pc = SD, 
                                   pd = SA), 
                    STPinwheelTile(RED_TILE, 
                                   pa = SA, 
                                   pb = A, 
                                   pc = B), 
                    STPinwheelTile(RED_TILE, 
                                   pa = SB, 
                                   pb = B, 
                                   pc = C), 
                    STPinwheelTile(RED_TILE, 
                                   pa = SC, 
                                   pb = C, 
                                   pc = D), 
                    STPinwheelTile(RED_TILE, 
                                   pa = SD, 
                                   pb = D, 
                                   pc = A),                              
               ];
          elif self.tile_type == U_TILE:
               return [
                    STPinwheelTile(U_TILE, A, B, C, D)
               ];
          else: # RED_TILE 
               s = edist(B, C) / 5.0
               M1 = (A + C) / 2.0
               liney = lambda x: ((By - Cy) / (Bx - Cx)) * (x - Bx) + By
               cond_func = lambda x, y: round(y - liney(x), 3) == 0.0 \
                           if Bx - Cx != 0.0 else x == Bx # points must be on this line
               M2 = C * 3.0 / 5.0 + B * 2.0 / 5.0
               M3 = C * 2.0 / 5.0 + B * 3.0 / 5.0
               M4 = C / 5.0 + B * 4.0 / 5.0
               M5 = (A + M4) / 2.0
               M6 = (M1 + M5) / 2.0
               return [ 
                    STPinwheelTile(RED_TILE, 
                                   pa = M4, 
                                   pb = B, 
                                   pc = A), 
                    STPinwheelTile(RED_TILE, 
                                   pa = M5, 
                                   pb = A, 
                                   pc = M1), 
                    STPinwheelTile(RED_TILE, 
                                   pa = M2, 
                                   pb = M1, 
                                   pc = C), 
                    STPinwheelTile(BLUE_TILE, 
                                   pa = M6, 
                                   pb = M1, 
                                   pc = M2, 
                                   pd = M3), 
                    STPinwheelTile(BLUE_TILE, 
                                   pa = M5, 
                                   pb = M6, 
                                   pc = M3, 
                                   pd = M4), 
               ]; 
          ##           
     ## def 

## class 

## STPinwheel_Tiling
 # A Tiling subclass implementing the STPinwheel substitution tiling 
##
class STPinwheel_Tiling(Tiling): 

     ## __init__
      # Initialization function for the STPinwheel_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "STPinwheel")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "STPinwheel"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), # pa
               vector([10, 0]), # pb
               vector([10, 10]), # pc
               vector([0, 10]), #pd
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the square triangle pinwheel (variant) tiling"; 
     
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
      # Gets the polygonal tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          init_tile = self.get_initial_tile(); 
          init_gt_tile = STPinwheelTile(BLUE_TILE, init_tile[0], init_tile[1], \
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

