#### Domino.py 
#### Implementation of the domino tiling 
#### See: http://www.wolframalpha.com/input/?i=domino+tiling
#### Author: Maxie D. Schmidt
#### Created: 2016.03.06

from sage.all import *
from Tiling import Tiling, edist

## 
 # Python constants that indicate the orientation of the domino subtiles
##
HORIZ_TILE = 1; 
VERT_TILE = 2; 

## DominoTile
 # A class that implements the individual rectangular-shaped domino subtiles
##
class DominoTile(object): 

     ## __init__
      # Initialization function for the DominoTile class
      # @param tile_type The orientation of the tile. Should be one of:
      #                  HORIZ_TILE or VERT_TILE
      # @param pa        The vector-valued rectangle vertex A in the tile
      # @param pb        The vector-valued rectangle vertex B in the tile
      # @param pc        The vector-valued rectangle vertex C in the tile
      # @param pd        The vector-valued rectangle vertex D in the tile
     ##
     def __init__(self, tile_type, pa, pb, pc, pd): 
          self.tile_type = tile_type; 
          self.pa = pa;
          self.pb = pb; 
          self.pc = pc; 
          self.pd = pd; 
     ## def 
     
     ## to_points
      # Returns a list of the four vector vertices of the tile
     ##
     def to_points(self): 
          return [self.pa, self.pb, self.pc, self.pd]; 
     ## def 
     
     ## to_substiles
      # Returns a list of DominoTile objects corresponding to the next 
      # set of subtiles generated after one more step in the substitution tiling
     ##
     def to_subtiles(self): 
          
          A, B, C, D = self.pa, self.pb, self.pc, self.pd; 
          s1, s2 = edist(A, B), edist(A, D); 
          next_tiles = []; 
          if self.tile_type == VERT_TILE: 
               next_tiles = [
                    DominoTile(HORIZ_TILE, 
                               pa = A + vector([0, -s1 / 4]), 
                               pb = D + vector([0, -s1 / 4]), 
                               pc = D, pd = A), 
                    DominoTile(HORIZ_TILE, 
                               pa = B, pb = C, 
                               pc = C + vector([0, s1 / 4]), 
                               pd = B + vector([0, s1 / 4])), 
                    DominoTile(VERT_TILE, 
                               pa = A + vector([0, -s1 / 4]), 
                               pb = B + vector([0, s1 / 4]), 
                               pc = B + vector([s2 / 2, s1 / 4]), 
                               pd = A + vector([s2 / 2, -s1 / 4])), 
                    DominoTile(VERT_TILE, 
                               pa = A + vector([s2 / 2, -s1 / 4]), 
                               pb = B + vector([s2 / 2, s1 / 4]), 
                               pc = C + vector([0, s1 / 4]), 
                               pd = D + vector([0, -s1 / 4]))
               ]; 
          else: # HORIZ_TILE: 
               next_tiles = [
                    DominoTile(VERT_TILE, 
                               pa = D, pb = A, 
                               pc = A + vector([s1 / 4, 0]), 
                               pd = D + vector([s1 / 4, 0])), 
                    DominoTile(VERT_TILE, 
                               pa = C + vector([-s1 / 4, 0]), 
                               pb = B + vector([-s1 / 4, 0]), 
                               pc = B, pd = C), 
                    DominoTile(HORIZ_TILE, 
                               pa = A + vector([s1 / 4, s2 / 2]), 
                               pb = B + vector([-s1 / 4, s2 / 2]), 
                               pc = C + vector([-s1 / 4, 0]), 
                               pd = D + vector([s1 / 4, 0])), 
                    DominoTile(HORIZ_TILE, 
                               pa = A + vector([s1 / 4, 0]), 
                               pb = B + vector([-s1 / 4, 0]), 
                               pc = C + vector([-s1 / 4, -s2 / 2]), 
                               pd = D + vector([s1 / 4, -s2 / 2]))
               ]; 
          ## if 
          return next_tiles; 

     ## def 

## class 

## Domino_Tiling
 # A Tiling subclass implementing the domino substitution tiling 
 # See: http://www.wolframalpha.com/input/?i=domino+tiling
##
class Domino_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Domino_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Domino")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Domino"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 4]), 
               vector([0, 0]), 
               vector([2, 0]), 
               vector([2, 4])
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Domino substitution tiling"; 
     
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
      # Gets the polygonal Domino tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          init_tile = DominoTile(VERT_TILE, \
                                 self.INIT_TILE[0], self.INIT_TILE[1], \
                                 self.INIT_TILE[2], self.INIT_TILE[3]);  
          tile_list = [init_tile]; 
          for n in range(1, self.N): 
               next_tiles_list = self.get_next_tiling(tile_list); 
               tile_list = next_tiles_list;
          ## for 
          
          rtiles_list = []; 
          for (idx, stile) in enumerate(tile_list): 
               rtiles_list.append(stile.to_points()); 
          ## for 
          return rtiles_list; 

     ## def 

## class 

