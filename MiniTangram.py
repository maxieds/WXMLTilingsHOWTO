#### MiniTangram.py 
#### Implementation of a minitangram tiling variant
#### See: http://tilings.math.uni-bielefeld.de/substitution_rules/minitangram
#### Author: Maxie D. Schmidt
#### Created: 2016.03.22

from sage.all import *
from Tiling import Tiling, edist

## 
 # Python constants defining the distinct tile types, or shapes
##
TRIANGLE_TILE = 1;
SQUARE_TILE = 2;
RHOMB_TILE = 3;

## MiniTangramTile
 # Class representing the individual subtiles in the mini-tangram tiling variant
 # See: http://tilings.math.uni-bielefeld.de/substitution_rules/minitangram
##
class MiniTangramTile(object):

     ## __init__
      # Initialization function for the MiniTangramTile class
      # @param tile_type  The shape of the tile. Should be one of:
      #                   TRIANGLE_TILE, SQUARE_TILE, RHOMB_TILE
      # @param a, b, c, d The vector-valued vertices of the tile (d is optional)
     ##
     def __init__(self, tile_type, a, b, c, d = None): 
          self.tile_type = tile_type; 
          self.a = a; 
          self.b = b;
          self.c = c;
          self.d = d;     
     ## def 

     ## to_points
      # Returns a list of the vector vertices in the tile
     ##
     def to_points(self): 
          if self.tile_type == SQUARE_TILE or self.tile_type == RHOMB_TILE: 
               return [self.a, self.b, self.c, self.d]; 
          else: 
               return [self.a, self.b, self.c]; 
     ## def 

     ## to_subtiles_triangle
      # Returns a list of the next subtiles from a triangular tile 
      # after one more substiution step
     ##
     def to_subtiles_triangle(self): 
          A, B, C = self.a, self.b, self.c;
          mp1, mp2, mp3 = (A + B) / 2.0, (A + C) / 2.0, (B + C) / 2.0; 
          return [ 
               MiniTangramTile(TRIANGLE_TILE, 
                               a = mp1, b = B, c = mp3), 
               MiniTangramTile(SQUARE_TILE, 
                               a = A, b = mp1, c = mp3, d = mp2), 
               MiniTangramTile(TRIANGLE_TILE, 
                               a = mp2, b = mp3, c = C)
          ]; 
     ## def 
     
     ## to_subtiles_square
      # Returns a list of the next subtiles from a square tile 
      # after one more substiution step
     ##
     def to_subtiles_square(self): 
          A, B, C, D = self.a, self.b, self.c, self.d; 
          mp1, mp2, mp3, mp4, cp = (A + B) / 2.0, (B + C) / 2.0, \
                                   (C + D) / 2.0, (A + D) / 2.0, \
                                   (A + C) / 2.0; 
          return [
               MiniTangramTile(TRIANGLE_TILE, 
                               a = B, b = mp2, c = mp1), 
               MiniTangramTile(RHOMB_TILE, 
                               a = cp, b = mp2, c = mp1, d = A), 
               MiniTangramTile(RHOMB_TILE, 
                               a = mp3, b = cp, c = A, d = mp4), 
               MiniTangramTile(SQUARE_TILE, 
                               a = cp, b = mp2, c = C, d = mp3), 
               MiniTangramTile(TRIANGLE_TILE, 
                               a = D, b = mp3, c = mp4)
          ]; 
     ## def 
     
     ## to_subtiles_rhomb
      # This variant of the tiling defines that the rhombic tiles should not 
      # subdivide further. That is, the next subtile is the same as the 
      # original tile
     ##
     def to_subtiles_rhomb(self): 
          return [self];
     ## def 

     ## to_subtiles
      # Returns the next list of subtiles after one more substitution step
      # @see MiniTangramTile.to_subtiles_triangle
      # @see MiniTangramTile.to_subtiles_square
      # @see MiniTangramTile.to_subtiles_rhomb
     ##
     def to_subtiles(self): 
          if self.tile_type == TRIANGLE_TILE: 
               return self.to_subtiles_triangle(); 
          elif self.tile_type == SQUARE_TILE: 
               return self.to_subtiles_square(); 
          else: 
               return self.to_subtiles_rhomb(); 
     ## def

## class

## MiniTangram_Tiling
 # A Tiling subclass implementing a slight variant of the mini-tangram tiling 
 # See: http://tilings.math.uni-bielefeld.de/substitution_rules/minitangram
##
class MiniTangram_Tiling(Tiling): 

     ## __init__
      # Initialization function for the MiniTangram_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "MiniTangram")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "MiniTangram"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([0, 10]), 
               vector([10, 10]), 
               vector([10, 0])
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Mini-tangram tiling for an initial square tile"; 
     
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
      # Gets the polygonal MiniTangram tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          tile_list = [MiniTangramTile(SQUARE_TILE, 
                                       self.INIT_TILE[0], self.INIT_TILE[1], 
                                       self.INIT_TILE[2], self.INIT_TILE[3])
                      ]; 
          for n in range(1, self.N): 
               next_tiles_list = self.get_next_tiling(tile_list); 
               tile_list = next_tiles_list;
          ## for 
          
          rtiles_list = []; 
          for (idx, mtile) in enumerate(tile_list): 
               rtiles_list.append(mtile.to_points()); 
          ## for 
          return rtiles_list; 

     ## def 

## class 



