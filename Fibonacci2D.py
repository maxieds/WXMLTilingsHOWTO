#### Fibonacci2D.py 
#### Implementation of a 2D "Fibonacci Times Fibonacci" tiling variant
#### See: http://tilings.math.uni-bielefeld.de/substitution_rules/fibonacci_times_fibonacci_0
#### Author: Maxie D. Schmidt
#### Created: 2016.04.04

from sage.all import *
from Tiling import Tiling, edist, X, Y, V, midpoint2

BLUE_TILE = 1;
YELLOW_TILE = 2; 
ORANGE_TILE = 3;

one_third = float(1.0 / 3.0); 
two_thirds = float(2.0 / 3.0); 

class Fibonacci2DTile(object):

     def __init__(self, tile_type, a, b, c, d = None): 
          self.tile_type = tile_type; 
          self.a = a; 
          self.b = b;
          self.c = c;
          self.d = d;     
     ## def 

     def to_points(self): 
          return [self.a, self.b, self.c, self.d];
     ## def 

     def to_subtiles_blue(self): 
          return [
               Fibonacci2DTile(YELLOW_TILE, 
                               self.a, 
                               self.b, 
                               self.c, 
                               self.d)
          ];
     ## def 
     
     def to_subtiles_yellow(self):
          A, B, C, D = self.a, self.b, self.c, self.d;
          mp1 = midpoint2(two_thirds, A, B)
          mp2 = midpoint2(two_thirds, B, C)
          mp3 = midpoint2(one_third, C, D)
          mp4 = midpoint2(one_third, D, A)
          cp = midpoint2(one_third, mp3, mp1)
          return [
               Fibonacci2DTile(ORANGE_TILE, 
                               a = mp1, b = B, c = mp2, d = cp), 
               Fibonacci2DTile(YELLOW_TILE, 
                               a = A, b = mp1, c = cp, d = mp4), 
               Fibonacci2DTile(BLUE_TILE, 
                               a = cp, b = mp2, c = C, d = mp3), 
               Fibonacci2DTile(ORANGE_TILE, 
                               a = mp4, b = D, c = mp3, d = cp)
          ];
     ## def
     
     def to_subtiles_orange(self):
          #return [self]
          A, B, C, D = self.a, self.b, self.c, self.d;
          mp1 = midpoint2(two_thirds, B, C)
          mp2 = midpoint2(one_third, D, A)
          sqtile_offset = 2 * edist(A, B)
          sqtile_offsetV = V(sqtile_offset, sqtile_offset)
          return [
               Fibonacci2DTile(ORANGE_TILE, 
                               mp2, 
                               D, 
                               C, 
                               mp1), 
               Fibonacci2DTile(YELLOW_TILE, 
                               A, 
                               B, 
                               mp1, 
                               mp2)
          ];
     ## def

     def to_subtiles(self): 
          if self.tile_type == BLUE_TILE: 
               return self.to_subtiles_blue(); 
          elif self.tile_type == YELLOW_TILE: 
               return self.to_subtiles_yellow(); 
          else: 
               return self.to_subtiles_orange(); 
     ## def

## class 

class Fibonacci2D_Tiling(Tiling): 

     def __init__(self, num_steps_N, tiling_name_str): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([0, 9]), 
               vector([9, 9]), 
               vector([9, 0])
          ];
     ## def 
          
     def desc(self): 
          return "Two-dimensional Fibonacci tiling"; 
          
     def get_initial_tile(self): 
          return self.INIT_TILE; 
     
     def get_next_tiling(self, prev_tiles): 
          next_tiles = []; 
          for tile in prev_tiles: 
               subtiles = tile.to_subtiles(); 
               next_tiles.extend(subtiles); 
          ## for 
          return next_tiles; 
     ## def 
     
     def get_tiles(self): 
          
          tile_list = [Fibonacci2DTile(YELLOW_TILE, 
                                       self.INIT_TILE[0], self.INIT_TILE[1], 
                                       self.INIT_TILE[2], self.INIT_TILE[3])
                      ]; 
          for n in range(1, self.N): 
               next_tiles_list = self.get_next_tiling(tile_list); 
               tile_list = next_tiles_list;
          ## for 
          
          rtiles_list = []; 
          for (idx, ftile) in enumerate(tile_list): 
               rtiles_list.append(ftile.to_points()); 
          ## for 
          return rtiles_list; 

## class 

