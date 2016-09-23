#### TetrisTiling.py 
#### Implementation of the tetris tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/tetris/
#### Author: Maxie D. Schmidt
#### Created: 2016.09.22 

from sage.all import *
from Tiling import Tiling, edist, X, Y, V, midpoint, midpoint2

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
SQUARE_TILE = 1; 
LINE_TILE = 2; 
LSHAPED_TILE = 3;
TRIANGLE_TILE = 4;
ZSHAPED_TILE = 5;
NON_TILE = 6; ## for debugging

## TetrisTile
 # A class that represents the polygonal tiles in the tiling
##
class TetrisTile(object): 

     ## __init__
      # Initialization function for the TetrisTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of SQUARE_TILE or LINE_TILE or LSHAPED_TILE or
      #                  TRIANGLE_TILE or ZSHAPED_TILE or NON_TILE (for debugging)
      # @param p*        The vector coordinate of the vertex A in the triangle
     ##
     def __init__(self, tile_type, p1, p2, p3, p4, p5 = None, p6 = None, \
                  p7 = None, p8 = None): 
          self.tile_type = tile_type 
          self.p1 = p1 
          self.p2 = p2 
          self.p3 = p3 
          self.p4 = p4
          self.p5 = p5 
          self.p6 = p6
          self.p7 = p7
          self.p8 = p8
     ## def 

     ## to_points
      # Returns a list of the vertex point vectors in the tile
     ##
     def to_points(self): 
          if self.tile_type == SQUARE_TILE or self.tile_type == LINE_TILE:
               return [self.p1, self.p2, self.p3, self.p4]
          elif self.tile_type == LSHAPED_TILE: 
               return [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]
          else: 
               return [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, \
                       self.p7, self.p8]
     ## def 
     
     ## to_subtiles
      # Returns a list of subtiles after one more 
      # substitution step
     ##
     def to_subtiles(self): 
          P1, P2, P3, P4, P5, P6, P7, P8 = self.p1, self.p2, self.p3, self.p4,\
                                           self.p5, self.p6, self.p7, self.p8    
          if self.tile_type == SQUARE_TILE: 
               t1, t11 = midpoint(P1, P2), midpoint(P3, P4)
               t2, t12 = midpoint2(0.25, t1, t11), midpoint2(0.25, P2, P3)
               t62, t121 = midpoint2(0.25, P3, P2), midpoint2(0.25, P1, P4)
               t3, t6 = midpoint2(0.25, t121, t12), midpoint2(0.75, P1, P4)
               t41, t42 = midpoint2(0.25, P4, P3), midpoint2(0.25, P1, P2)
               t4 = midpoint(t41, t42)
               t5 = midpoint2(0.25, t6, t62)
               t7, t8 = midpoint(t1, t11), midpoint2(0.75, t1, t11)
               t9, t10 = midpoint2(0.75, t6, t62), midpoint2(0.25, P3, P4)
               t11 = midpoint2(0.75, t121, t12)
               t131, t132 = midpoint2(0.75, P4, P3), midpoint2(0.75, P1, P2) 
               t13 = midpoint(t131, t132)
               return[ 
                    TetrisTile(LSHAPED_TILE, 
                                  p1 = t6, 
                                  p2 = t5, 
                                  p3 = t3, 
                                  p4 = t2, 
                                  p5 = t1, 
                                  p6 = P1), 
                    TetrisTile(ZSHAPED_TILE, 
                                  p1 = t1, 
                                  p2 = P2, 
                                  p3 = t12, 
                                  p4 = t11, 
                                  p5 = t13, 
                                  p6 = t4, 
                                  p7 = t3, 
                                  p8 = t2), 
                    TetrisTile(TRIANGLE_TILE, ## right-most triangle tile
                                  p1 = t12, 
                                  p2 = P3, 
                                  p3 = t10, 
                                  p4 = t9, 
                                  p5 = t8, 
                                  p6 = t7, 
                                  p7 = t13, 
                                  p8 = t11), 
                    TetrisTile(TRIANGLE_TILE, 
                                  p1 = P4, 
                                  p2 = t10, 
                                  p3 = t9, 
                                  p4 = t8, 
                                  p5 = t7, 
                                  p6 = t4, 
                                  p7 = t5, 
                                  p8 = t6), 
               ]; 
          #### !!!! Fill these coordinates in for the HOWTO !!!! ####
          elif self.tile_type == LINE_TILE: 
               T1, T2 = midpoint2(0.25, P4, P1), midpoint2(0.25, P3, P2)
               T3 = midpoint2(0.375, P1, P4)
               T4, T7 = midpoint2(0.625, P2, P3), midpoint2(0.125, P2, P3)
               t12, t34 = midpoint(P1, P2), midpoint(P3, P4)
               T5 = midpoint2(0.375, t12, t34)
               T6 = midpoint2(0.125, t12, t34)
               T8 = midpoint2(0.625, t12, t34)
               return [
                    TetrisTile(SQUARE_TILE, 
                               p1 = T1, 
                               p2 = T2, 
                               p3 = P3, 
                               p4 = P4), 
                    TetrisTile(LSHAPED_TILE, ## upper-most L tile
                               p1 = T3, 
                               p2 = T5, 
                               p3 = T8, 
                               p4 = T4, 
                               p5 = T2, 
                               p6 = T1), 
                    TetrisTile(LINE_TILE, 
                               p1 = T6, 
                               p2 = T7, 
                               p3 = T4, 
                               p4 = T8), 
                    TetrisTile(LSHAPED_TILE, 
                               p1 = T3, 
                               p2 = T5, 
                               p3 = T6, 
                               p4 = T7, 
                               p5 = P2, 
                               p6 = P1), 
               ];
               return [
                    TetrisTile(LINE_TILE, P1, P2, P3, P4, P5, P6), 
               ]; 
          elif self.tile_type == LSHAPED_TILE: 
               T1, T2 = midpoint2(1.0 / 3.0, P1, P6), midpoint(P2, P3)
               T4, T6 = midpoint(P3, P4), midpoint2(0.25, P6, P5)
               t12, t54 = midpoint(P1, P2), midpoint(P4, P5)
               T3 = midpoint2(1.0 / 3.0, t12, T6) 
               T5 = midpoint2(0.25, T6, T3)
               T7 = midpoint2(2.0 / 3.0, T5, t54)
               return [
                    TetrisTile(SQUARE_TILE, 
                               p1 = P1, 
                               p2 = P2, 
                               p3 = T2, 
                               p4 = T1), 
                    TetrisTile(LINE_TILE, 
                               p1 = T1, 
                               p2 = T3, 
                               p3 = T6, 
                               p4 = P6), 
                    TetrisTile(LSHAPED_TILE, ## bottom-most L tile
                               p1 = T3, 
                               p2 = T2, 
                               p3 = P3, 
                               p4 = T4, 
                               p5 = T7, 
                               p6 = T5), 
                    TetrisTile(LSHAPED_TILE, ## top-most L tile
                               p1 = T6, 
                               p2 = T5, 
                               p3 = T7, 
                               p4 = T4, 
                               p5 = P4, 
                               p6 = P5), 
               ]; 
          elif self.tile_type == TRIANGLE_TILE: 
               T1, t21 = midpoint(P1, P2), midpoint(P5, P6)
               T2 = midpoint2(0.25, T1, t21)
               T3, T4 = midpoint(P7, P8), midpoint(P3, P4)
               t51, t61 = midpoint2(1.0 / 3.0, P1, T1), midpoint2(1.0 / 3.0, P2, T1)
               T5, T6 = midpoint(T3, t51), midpoint(T4, t61)
               return [
                    TetrisTile(SQUARE_TILE, 
                               p1 = P7, 
                               p2 = P4, 
                               p3 = P5, 
                               p4 = P6), 
                    TetrisTile(LINE_TILE, 
                               p1 = T3, 
                               p2 = T5, 
                               p3 = T6, 
                               p4 = T4), 
                    TetrisTile(LSHAPED_TILE, ## left-most L tile
                               p1 = T1, 
                               p2 = T2, 
                               p3 = T5, 
                               p4 = T3, 
                               p5 = P8, 
                               p6 = P1), 
                    TetrisTile(LSHAPED_TILE, ## right-most L tile
                               p1 = T1, 
                               p2 = T2, 
                               p3 = T6, 
                               p4 = T4, 
                               p5 = P3, 
                               p6 = P2), 
               ]; 
          elif self.tile_type == ZSHAPED_TILE:
               T1, T2 = midpoint(P1, P2), midpoint(P1, P8)
               T4, T6 = midpoint(P4, P5), midpoint(P6, P7)
               T5, t31 = midpoint2(0.25, T4, T6), midpoint(P2, P3)
               T3 = midpoint2(0.25, T2, t31)
               return [
                    TetrisTile(LINE_TILE, 
                               p1 = P6, 
                               p2 = T6, 
                               p3 = T4, 
                               p4 = P5), 
                    TetrisTile(LSHAPED_TILE, ## left-most L tile
                               p1 = T6, 
                               p2 = P7, 
                               p3 = P8, 
                               p4 = T2, 
                               p5 = T3, 
                               p6 = T5), 
                    TetrisTile(LSHAPED_TILE, ## right-most L tile
                               p1 = T4, 
                               p2 = T5, 
                               p3 = T3, 
                               p4 = T2, 
                               p5 = P1, 
                               p6 = T1), 
                    TetrisTile(SQUARE_TILE, 
                               p1 = T1, 
                               p2 = P2, 
                               p3 = P3, 
                               p4 = P4), 
               ]; 
          else: # NON_TILE 
               return [ 
                    TetrisTile(NON_TILE, P1, P2, P3, P4, P5, P6, P7, P8), 
               ]; 
          ##           
     ## def 

## class 

## Tetris_Tiling
 # A Tiling subclass implementing the first tetris substitution tiling 
##
class Tetris_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Tetris_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Tetris")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Tetris"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [ ## large square initial tile
               V(0, 0), 
               V(50, 0), 
               V(50, 50), 
               V(0, 50), 
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the tetris tiling"; 
     
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
          init_gt_tile = TetrisTile(SQUARE_TILE, init_tile[0], init_tile[1], \
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

