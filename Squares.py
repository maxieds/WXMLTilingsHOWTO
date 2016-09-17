#### Squares.py 
#### Implementation of a periodic square (X4) tiling for comparison.  
#### Author: Maxie D. Schmidt
#### Created: 2016.03.05

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling

## SquareTile
 # Class implementing the individual square-shaped tiles in the "Squares" tiling
##
class SquareTile(object): 

     ## __init__
      # Initialization function / constructor for the SquareTile class 
      # @param A The corner vertex in the square tile
      # @param s The side length of the square-shaped tile
     ##
     def __init__(self, A, s): 
          self.corner_point = A; 
          self.side_length = s; 
     ## def 
     
     ## to_points 
      # Returns a list of vertices in the tile
     ##
     def to_points(self): 
          A, s = self.corner_point, self.side_length; 
          vectors = [
               vector([0, 0]), 
               vector([0, -s]), 
               vector([s, -s]), 
               vector([s, 0])
          ];
          add_vertices = lambda v: A + v; 
          square_vertices = map(add_vertices, vectors); 
          return square_vertices; 
     ## def 
     
     ## __str__
      # Returns a string representation of the tile for printing
     ##
     def __str__(self): 
          return str(self.to_points()); 
     ## def 
     
     ## to_subtiles 
      # Returns a list of subtiles after one more substitution step
     ##
     def to_subtiles(self): 
          A, s = self.corner_point, self.side_length; 
          next_tiles = [
               SquareTile(A + vector([0, 0]), s / 2), 
               SquareTile(A + vector([0, -s / 2]), s / 2), 
               SquareTile(A + vector([s / 2, -s / 2]), s / 2), 
               SquareTile(A + vector([s / 2, 0]), s / 2) 
          ]; 
          return next_tiles; 
     ## def 

## class 

## Square_Tiling
 # A Tiling subclass implementing a periodic squares substitution tiling 
 # for testing an comparison
##
class Square_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Square_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Squares")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Squares"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 1]), 
               vector([0, 0]), 
               vector([1, 0]), 
               vector([1, 1])
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Periodic square tiling (for comparison)"; 
     
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
      # Gets the polygonal Squares tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          init_tile = SquareTile(vector([0, 1]), 1.0);  
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
