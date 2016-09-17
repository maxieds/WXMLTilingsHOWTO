#### Cesi.py 
#### Implementation of the Cesi's substitution tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/cesis-substitution/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.16 

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y, solve_system

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
P0_TILE = 1; 
P1_TILE = 2; 
P2_TILE = 3;
P3_TILE = 4;

c = n(cos(pi / 7), 32);
s = n(sin(pi / 7), 32);

## CesiTile
 # A class that represents the triangular tiles in the tiling
##
class CesiTile(object): 

     ## __init__
      # Initialization function for the CesiTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of P*_TILE 
      # @param pa        The vector coordinate of the vertex A in the quadrilateral
      # @param pb        The vector coordinate of the vertex B in the quadrilateral
      # @param pc        The vector coordinate of the vertex C in the quadrilateral
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
          if self.tile_type == P3_TILE:
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
          if self.tile_type == P0_TILE: 
               r = edist(A, B) / 2.0
               #r2 = (c + s) / 2.0
               [M1x, M1y] = solve_system([Ax, Ay], r * (c+s), [Bx, By], r * (2-c-s))
               [M2x, M2y] = solve_system([Bx, By], r * (c+s), [Cx, Cy], r * (2-c-s))
               [M3x, M3y] = solve_system([Dx, Dy], r * (c+s), [Cx, Cy], r * (2-c-s))
               [M4x, M4y] = solve_system([Ax, Ay], r * (c+s), [Dx, Dy], r * (2-c-s))
               #[M5x, M5y] = solve_system([M4x, M4y], r * (c+s), \
               #                          [M2x, M2y], r * (2-c-s))
               [M5x, M5y] = solve_system([Ax, Ay], r * n(sqrt(2)) * (c+s), \
                                         [Cx, Cy], r * n(sqrt(2)) * (2-c-s))
               M1, M2, M3, M4, M5 = vector([M1x, M1y]), vector([M2x, M2y]), \
                                    vector([M3x, M3y]), vector([M4x, M4y]), \
                                    vector([M5x, M5y]) 
               [M6x, M6y] = solve_system([Ax, Ay], r * c, [M1x, M1y], r * s)
               [M7x, M7y] = solve_system([M1x, M1y], r * c, [M5x, M5y], r * s)
               [M8x, M8y] = solve_system([M5x, M5y], r * c, [M4x, M4y], r * s)
               [M9x, M9y] = solve_system([M4x, M4y], r * c, [Ax, Ay], r * s)
               M6, M7, M8, M9 = vector([M6x, M6y]), vector([M7x, M7y]), \
                                vector([M8x, M8y]), vector([M9x, M9y]) 
               return [
                    CesiTile(P0_TILE, 
                             pa = M6, 
                             pb = M7, 
                             pc = M8, 
                             pd = M9), 
                    CesiTile(P3_TILE, 
                             pa = M9, 
                             pb = A, 
                             pc = M6), 
                    CesiTile(P3_TILE, 
                             pa = M6, 
                             pb = M1, 
                             pc = M7), 
                    CesiTile(P3_TILE, 
                             pa = M7, 
                             pb = M5, 
                             pc = M8), 
                    CesiTile(P3_TILE, 
                             pa = M8, 
                             pb = M4, 
                             pc = M9), 
                    CesiTile(P2_TILE, 
                             pa = B, 
                             pb = M2, 
                             pc = M5, 
                             pd = M1), 
                    CesiTile(P1_TILE, 
                             pa = M5, 
                             pb = M2, 
                             pc = C, 
                             pd = M3), 
                    CesiTile(P2_TILE, 
                             pa = M4, 
                             pb = M5, 
                             pc = M3, 
                             pd = D), 
                             
               ];
          elif self.tile_type == P1_TILE or self.tile_type == P2_TILE: 
               TT = self.tile_type
               M1, M2, M3, M4 = (A + D) / 2.0, (A + B) / 2.0, (C + B) / 2.0, \
                                (C + D) / 2.0
               M5 = (M2 + M4) / 2.0
               return [
                    CesiTile(TT, 
                             pa = A, 
                             pb = M2, 
                             pc = M5, 
                             pd = M1), 
                    CesiTile(TT, 
                             pa = M2, 
                             pb = B, 
                             pc = M3, 
                             pd = M5), 
                    CesiTile(TT, 
                             pa = M1, 
                             pb = M5, 
                             pc = M4, 
                             pd = D), 
                    CesiTile(TT, 
                             pa = M5, 
                             pb = M3, 
                             pc = C, 
                             pd = M4), 
               ];
          else: # P3_TILE 
               M1, M2, M3 = (A + C) / 2.0, (A + B) / 2.0, (B + C) / 2.0
               return [ 
                    CesiTile(P3_TILE, 
                             pa = A, 
                             pb = M2, 
                             pc = M1), 
                    CesiTile(P3_TILE, 
                             pa = M3, 
                             pb = M1, 
                             pc = M2), 
                    CesiTile(P3_TILE, 
                             pa = M2, 
                             pb = B, 
                             pc = M3), 
                    CesiTile(P3_TILE, 
                             pa = M1, 
                             pb = M3, 
                             pc = C), 
               ]; 
          ##           
     ## def 

## class 

## Cesi_Tiling
 # A Tiling subclass implementing Cesi's substitution tiling 
##
class Cesi_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Cesi_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Cesi")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Cesi"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), # pa
               vector([2, 0]), # pb
               vector([2, 2]), # pc
               vector([0, 2]), #pd
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Cesi's substitution tiling"; 
     
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
          init_gt_tile = CesiTile(P0_TILE, init_tile[0], init_tile[1], \
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

