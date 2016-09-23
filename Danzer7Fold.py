#### Danzer7Fold.py 
#### Implementation of the tetris tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/danzers-7-fold-original/
#### Author: Maxie D. Schmidt
#### Created: 2016.09.23 

from sage.all import *
from Tiling import Tiling, edist, X, Y, V, midpoint, midpoint2

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
BLUE_TILE = 1; 
ORANGE_TILE = 2; 
YELLOW_TILE = 3;
NON_TILE = 4; ## for debugging

## Define constants for the three different edge lengths: 
sc1, sc2, sc3 = n(sin(pi / 7.0)), n(sin(2.0 *pi / 7.0)), n(sin(3.0 *pi / 7.0))

## Danzer7FoldTile
 # A class that represents the triangular tiles in the tiling
##
class Danzer7FoldTile(object): 

     ## __init__
      # Initialization function for the Danzer7FoldTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of BLUE_TILE or ORANGE_TILE or YELLOW_TILE or
      #                  NON_TILE (for debugging)
      # @param pa        The vector coordinate of the vertex A in the triangle
      # @param pb        The vector coordinate of the vertex B in the triangle
      # @param pc        The vector coordinate of the vertex C in the triangle
     ##
     def __init__(self, tile_type, pa, pb, pc): 
          self.tile_type = tile_type 
          self.pa = pa 
          self.pb = pb 
          self.pc = pc 
     ## def 

     ## to_points
      # Returns a list of the vertex point vectors in the tile
     ##
     def to_points(self): 
          return [self.pa, self.pb, self.pc]
     ## def 
     
     ## to_subtiles
      # Returns a list of subtiles after one more 
      # substitution step
     ##
     def to_subtiles(self): 
          A, B, C = self.pa, self.pb, self.pc  
          if self.tile_type == BLUE_TILE: 
               side3_ratio, side1_ratio, side2_ratio = 3 * sc3, sc1 + sc2, \
                                                       sc1 + sc2 + sc3
               T1 = midpoint2(sc3 / side3_ratio, A, B)
               T2 = midpoint2(sc3 / side3_ratio, B, A)
               T3 = midpoint2(sc1 / side1_ratio, B, C)
               T4 = midpoint2(sc1 / side2_ratio, C, A)
               T5 = midpoint2(sc3 / side2_ratio, A, C)
               return[ 
                    Danzer7FoldTile(ORANGE_TILE, 
                                    pa = T1, 
                                    pb = A, 
                                    pc = T5), 
                    Danzer7FoldTile(BLUE_TILE, 
                                    pa = T5, 
                                    pb = T2, 
                                    pc = T1), 
                    Danzer7FoldTile(BLUE_TILE, 
                                    pa = T2, 
                                    pb = B, 
                                    pc = T3), 
                    Danzer7FoldTile(YELLOW_TILE, 
                                    pa = T4, 
                                    pb = T5, 
                                    pc = T2), 
                    Danzer7FoldTile(BLUE_TILE, 
                                    pa = T2, 
                                    pb = C, 
                                    pc = T4), 
                    Danzer7FoldTile(YELLOW_TILE, 
                                    pa = T3, 
                                    pb = C, 
                                    pc = T2), 
               ]; 
          #### !!!! Fill these coordinates in for the HOWTO !!!! ####
          elif self.tile_type == ORANGE_TILE: 
               return [
                    Danzer7FoldTile(ORANGE_TILE, A, B, C), 
               ]; 
          elif self.tile_type == YELLOW_TILE: 
               return [
                    Danzer7FoldTile(YELLOW_TILE, A, B, C), 
               ]; 
          else: # NON_TILE 
               return [ 
                    Danzer7FoldTile(NON_TILE, A, B, C), 
               ]; 
          ##           
     ## def 

## class 

## Danzer7Fold_Tiling
 # A Tiling subclass implementing Danzer's original 7-fold substitution tiling 
##
class Danzer7Fold_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Danzer7Fold_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Danzer7Fold")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Danzer7Fold"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          baset = (sc2**2 + sc3**2 - sc1**2) / (2.0 * sc3)
          self.INIT_TILE = [ ## large square initial tile
               V(0, 0), 
               V(sc3, 0), 
               V(baset, (sc2**2 - baset**2) ** 0.5), 
          ];
          scaling_factor = 50
          self.INIT_TILE = map(lambda v: scaling_factor * v, self.INIT_TILE)
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Danzer's 7-fold (original) tiling"; 
     
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
          init_gt_tile = Danzer7FoldTile(BLUE_TILE, init_tile[0], init_tile[1], \
                                         init_tile[2]); 
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

