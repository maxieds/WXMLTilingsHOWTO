#### Octagonal1225.py 
#### Implementation of the octagonal 1-2-2-5 tiling 
#### (i.e., the single entry of the Tilings Encyclopedia in the intersection of 
####  CS course numbers and the numeric digits of hacker's aliases at the 
####  University of Illinois at Urbana-Champaign)
#### See: http://tilings.math.uni-bielefeld.de/substitution/octagonal-1225/
#### Author: Maxie D. Schmidt
#### Created: 2016.09.27

from sage.all import *
from Tiling import Tiling, edist, X, Y, V, midpoint, midpoint2, RotationMatrix
from AffineTransformOp import *

## 
 # Python constants that indicate the distinct proto-tiles
##
SQUARE_TILE = 1; 
HOUSE_TILE = 2;  

T = 10.0
#S = n(sqrt(3 + 2 * sqrt(2)))
S = n(1 + sqrt(2))
X = T / (S - 1)
H = n((2.0 * S * T - 2 * sqrt(4 * T**2 - (S**2 - 4) * X**2)) / (S**2 - 4))

## Octagonal1225Tile
 # A class that implements the two tile types
##
class Octagonal1225Tile(object): 

     ## __init__
      # Initialization function for the Octagonal1225Tile class
      # @param tile_type The orientation of the tile. Should be one of:
      #                  SQUARE_TILE or HOUSE_TILE
      # @param pi        The vector-valued rectangle vertex in the tile
      #                  ordered counterclockwise starting from the 
      #                  lower left point
     ##
     def __init__(self, tile_type, p1, p2, p3, p4): 
          self.tile_type = tile_type; 
          self.p1 = p1;
          self.p2 = p2; 
          self.p3 = p3; 
          self.p4 = p4; 
     ## def 
     
     ## to_points
      # Returns a list of the vertices of the tile
     ##
     def to_points(self): 
          return [self.p1, self.p2, self.p3, self.p4]
     ## def 
     
     ## to_subtiles
      # Returns a list of DominoTile objects corresponding to the next 
      # set of subtiles generated after one more step in the substitution tiling
     ##
     def to_subtiles(self): 
          p1, p2, p3, p4 = self.to_points()
          P = lambda tile, vertex: tile[vertex - 1]
          if self.tile_type == SQUARE_TILE: 
               t, sf = edist(p1, p2), 1 / S
               s1, s2 = midpoint2(sf, p2, p1), p2
               p41, p42 = midpoint2(sf, p1, p4), midpoint2(sf, p2, p3)
               s3, s4 = p42, midpoint2(sf, p42, p41)
               square = [s1, s2, s3, s4]
               h1tile = Octagonal1225Tile(HOUSE_TILE, p1, P(square, 1), \
                                          P(square, 4), p4)
               h2tile = Octagonal1225Tile(HOUSE_TILE, p3, P(square, 3), \
                                          P(square, 4), p4)
               square_tile = Octagonal1225Tile(SQUARE_TILE, square[0], square[1], \
                                               square[2], square[3])
               next_tiles = [square_tile, h1tile, h2tile]; 
          
          else: ## HOUSE_TILE
               sf, x, t = 1 / S, edist(p1, p2), edist(p2, p3)
               
               h1offset = midpoint2(sf * x / edist(p1, p4), p1, p4)
               h1M, h1T = sf * matrix([[1, 0], [0, 1]]), V(0, 0)
               h1op = AffineTransformOp(h1M, h1T)
               h1 = Tiling.transform_points(self.to_points(), h1op)
               h1Txy = h1offset - P(h1, 1)
               h1 = map(lambda v: v + h1Txy, h1)
               
               s21 = midpoint2(sf, p3, p2)
               s13, s12 = midpoint(P(h1, 3), p3), midpoint(P(h1, 2), s21)
               s1 = [P(h1, 2), s12, s13, P(h1, 3)]
               s2 = [s12, s21, p3, s13]
               
               h23 = midpoint2(sf * t / x, p1, p2)
               h2 = [P(h1, 1), p1, h23, P(s1, 2)]
               h3 = [p2, P(s2, 2), P(s2, 1), h23]
               
               h1mpt, p34mpt = midpoint(P(h1, 3), P(h1, 4)), midpoint(p3, p4)
               h4 = [p34mpt, h1mpt, P(h1, 4), p4]
               h5 = [p34mpt, h1mpt, P(s1, 4), p3]
               
               next_tiles = [
                    Octagonal1225Tile(HOUSE_TILE, h1[0], h1[1], h1[2], h1[3]),       ## h1
                    Octagonal1225Tile(SQUARE_TILE, s1[0], s1[1], s1[2], s1[3]),      ## s1
                    Octagonal1225Tile(SQUARE_TILE, s2[0], s2[1], s2[2], s2[3]),      ## s2
                    Octagonal1225Tile(HOUSE_TILE, h2[0], h2[1], h2[2], h2[3]),       ## h2
                    Octagonal1225Tile(HOUSE_TILE, h3[0], h3[1], h3[2], h3[3]),       ## h3
                    Octagonal1225Tile(HOUSE_TILE, h4[0], h4[1], h4[2], h4[3]),       ## h4
                    Octagonal1225Tile(HOUSE_TILE, h5[0], h5[1], h5[2], h5[3]),       ## h5
               ];
          ##
          return next_tiles; 

     ## def 

## class 

## Octagonal1225_Tiling
 # A Tiling subclass implementing the octagonal 1-2-2-5 substitution tiling 
##
class Octagonal1225_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Octagonal1225_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Octagonal1225")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Octagonal1225"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          #self.INIT_TILE = [ ## initial house tile
          #     vector([0, 0]), 
          #     vector([X, 0]), 
          #     vector([X, T]), 
          #     vector([0, n(T + sqrt(H**2 - X**2))]),
          #];
          self.INIT_TILE = [ ## initial square tile
               vector([0, 0]), 
               vector([T, 0]), 
               vector([T, T]), 
               vector([0, T]),
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the octagonal 1-2-2-5 tiling"; 
     
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
          
          init_tile = Octagonal1225Tile(SQUARE_TILE, self.INIT_TILE[0], \
                                        self.INIT_TILE[1], self.INIT_TILE[2], \
                                        self.INIT_TILE[3]);  
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

