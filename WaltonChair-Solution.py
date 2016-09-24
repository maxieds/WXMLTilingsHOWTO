#### WaltonChair.py.py 
#### Implementation of the Walton chair tiling 
#### See: http://tilings.math.uni-bielefeld.de/substitution/waltonchair/
#### See also: https://xa.yimg.com/kq/groups/13997333/.../name/WaltonChair.pdf (on Google)
#### Author: Maxie D. Schmidt
#### Created: 2016.08.31

from sage.all import *
from Tiling import Tiling, edist, X, Y, V
from AffineTransformOp import *

## 
 # Python constants that indicate the orientation of the A4 subtiles
##
WTILE = 1; 
RTILE = 2;  

Q = 2.0 * n(sqrt(2)) / 3.0
R = 2.0 / 3.0
P = n(sqrt(2)) / 3.0

## WaltonChairTile
 # A class that implements the two tile types
##
class WaltonChairTile(object): 

     ## __init__
      # Initialization function for the WaltonChairTile class
      # @param tile_type The orientation of the tile. Should be one of:
      #                  WTILE or RTILE
      # @param pi        The vector-valued rectangle vertex in the tile
      #                  ordered counterclockwise starting from the 
      #                  lower left point
     ##
     def __init__(self, tile_type, p1, p2, p3, p4, p5, p6): 
          self.tile_type = tile_type; 
          self.p1 = p1;
          self.p2 = p2; 
          self.p3 = p3; 
          self.p4 = p4; 
          self.p5 = p5; 
          self.p6 = p6; 
     ## def 
     
     ## to_points
      # Returns a list of the vertices of the tile
     ##
     def to_points(self): 
          return [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]; 
     ## def 
     
     ## to_substiles
      # Returns a list of DominoTile objects corresponding to the next 
      # set of subtiles generated after one more step in the substitution tiling
     ##
     def to_subtiles(self): 
          p1, p2, p3, p4, p5, p6 = self.to_points()
          if self.tile_type == WTILE or self.tile_type == RTILE: 
               M1, M2, M3 = 0.5 * matrix([[1, 0], [0, 1]]), \
                            0.5 * matrix([[1, 0], [0, -1]]), \
                            n(sqrt(2) / 2.0) * matrix([[0, -1], [-1, 0]])
               T1, T2, T3 = V(0, 0), V(0, 1), 1.0 / 3.0 * V(n(2.0 * sqrt(2)), 2.0)
               
               wtile1op = AffineTransformOp(M1, T1)
               wtile2op = AffineTransformOp(M2, T2)
               wtile3op = AffineTransformOp(M3, T3)
               wtile1 = Tiling.transform_points(self.to_points(), wtile1op)
               wtile2 = Tiling.transform_points(self.to_points(), wtile2op)
               wtile3 = Tiling.transform_points(self.to_points(), wtile3op)
               wt1 = WaltonChairTile(RTILE, wtile1[0], wtile1[1], wtile1[2], \
                                     wtile1[3], wtile1[4], wtile1[5])
               wt2 = WaltonChairTile(RTILE, wtile2[0], wtile2[1], wtile2[2], \
                                     wtile2[3], wtile2[4], wtile2[5])
               wt3 = WaltonChairTile(RTILE, wtile3[0], wtile3[1], wtile3[2], \
                                     wtile3[3], wtile3[4], wtile3[5])
                                  
               next_tiles = [
                    wt1, wt2, wt3, 
               ]; 
          ##
          return next_tiles; 

     ## def 

## class 

## WaltonChair_Tiling
 # A Tiling subclass implementing the Walton chair substitution tiling 
##
class WaltonChair_Tiling(Tiling): 

     ## __init__
      # Initialization function for the WaltonChair_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "WaltonChair")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "WaltonChair"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([Q, 0]), 
               vector([Q, R]), 
               vector([P, R]), 
               vector([P, 1.0]), 
               vector([0, 1.0]), 
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the Walton chair tiling"; 
     
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
          
          init_tile = WaltonChairTile(WTILE, self.INIT_TILE[0], \
                                   self.INIT_TILE[1], self.INIT_TILE[2], \
                                   self.INIT_TILE[3], self.INIT_TILE[4], \
                                   self.INIT_TILE[5]);  
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

