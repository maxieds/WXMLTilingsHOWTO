#### Triangles.py 
#### Implementation of a periodic triangle (X2) tiling for comparison.  
#### Author: Maxie D. Schmidt
#### Created: 2016.03.05

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling

## TriangleTile
 # Class implementing the individual triangle-shaped tiles in the 
 # "Triangles" tiling
##
class TriangleTile(object): 

     ## __init__
      # Initialization function / constructor for the TriangleTile class 
      # @param pa The triangle vertex labeled A in the tile
      # @param pb The triangle vertex labeled B in the tile
      # @param pc The triangle vertex labeled C in the tile
     ##
     def __init__(self, pa, pb, pc): 
          self.pa = pa; 
          self.pb = pb; 
          self.pc = pc;
     ## def 
     
     ## to_points 
      # Returns a list of vertices in the tile
     ##
     def to_points(self): 
          return [self.pa, self.pb, self.pc];
     ## def 
     
     ## __str__
      # Returns a string representation of the tile for printing
     ##
     def __str__(self): 
          return "pa = " + str(self.pa) + ", pb = " + str(self.pc) + \
                 ", pc = " + str(self.pc); 
     ## def 
     
     ## to_subtiles 
      # Returns a list of subtiles after one more substitution step
     ##
     def to_subtiles(self): 
          A, B, C, M = self.pa, self.pb, self.pc, 0.5 * (self.pb + self.pc); 
          next_tiles = [
               TriangleTile(pa = M, pb = A, pc = B), 
               TriangleTile(pa = M, pb = C, pc = A)
          ]; 
          return next_tiles; 
     ## def 
     
## class

## Triangle_Tiling
 # A Tiling subclass implementing a periodic triangular substitution tiling 
 # for testing an comparison
##
class Triangle_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Triangle_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Triangles")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Triangles"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([0, 1]), 
               vector([1, 0])
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Periodic triangle tiling (for comparison)"; 
     
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
      # Gets the polygonal Triangles tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          init_tile = TriangleTile(self.INIT_TILE[0], self.INIT_TILE[1], self.INIT_TILE[2]); 
          tile_list = [init_tile]; 
          for n in range(1, self.N): 
               next_tiles_list = self.get_next_tiling(tile_list); 
               tile_list = next_tiles_list;
          ## for 
          
          rtiles_list = []; 
          for (idx, ttile) in enumerate(tile_list): 
               rtiles_list.append(ttile.to_points()); 
          ## for 
          return rtiles_list; 

     ## def 

## class 
 
