#### AmmannA3.py 
#### Implementation of the Ammann (A3) tiling 
#### See: http://tilings.math.uni-bielefeld.de/substitution/ammann-a3/
#### Author: Maxie D. Schmidt
#### Created: 2016.09.30

from sage.all import *
from Tiling import Tiling, edist, X, Y, V, midpoint2
from AffineTransformOp import *

## 
 # Python constants that indicate the orientation of the A4 subtiles
##
A3CHAIR_TILE = 1; 
A3CHAIR2_TILE = 2;  
A3CHAIR3_TILE = 3; 

GOLDEN_RATIO = n(golden_ratio)
TAU = GOLDEN_RATIO

## AmmannA3Tile
 # A class that implements the two A3 prototiles subtiles
##
class AmmannA3Tile(object): 

     ## __init__
      # Initialization function for the AmmannA3Tile class
      # @param tile_type The orientation of the tile. Should be one of:
      #                  A3CHAIR_TILE or A3CHAIR2_TILE or A3CHAIR3_TILE
      # @param pi        The vector-valued rectangle vertex in the tile
      #                  ordered counterclockwise starting from the 
      #                  lower left point
     ##
     def __init__(self, tile_type, p1, p2, p3, p4, p5, p6, \
                  p7 = None, p8 = None, p9 = None, p10 = None): 
          self.tile_type = tile_type
          self.p1 = p1
          self.p2 = p2 
          self.p3 = p3 
          self.p4 = p4 
          self.p5 = p5 
          self.p6 = p6 
          self.p7 = p7 
          self.p8 = p8 
          self.p9 = p9
          self.p10 = p10
     ## def 
     
     def __str__(self): 
          return str(self.to_points())
     ## def
     
     ## to_points
      # Returns a list of the vertices of the tile
     ##
     def to_points(self): 
          if self.tile_type == A3CHAIR_TILE: 
               return [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]
          elif self.tile_type == A3CHAIR2_TILE:
               return [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, \
                       self.p7, self.p8]
          else: 
               return [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, \
                       self.p7, self.p8, self.p9, self.p10]
          
     ## def 
     
     ## to_subtiles
      # Returns a list of DominoTile objects corresponding to the next 
      # set of subtiles generated after one more step in the substitution tiling
     ##
     def to_subtiles(self): 
          PP = lambda points, i: points[i - 1]
          if self.tile_type == A3CHAIR_TILE: 
               p1, p2, p3, p4, p5, p6 = self.to_points()
               sf = edist(p1, p2) / (2 * TAU**2 + TAU) # scaling factor 
               sf = edist(p1, p2) / (TAU**3) # scaling factor 
               sf = edist(p1, p6) / (TAU**2) # scaling factor 
               T11, T12 = p2, p3
               T13 = midpoint2(sf * TAU**2 / edist(p3, p4), p3, p4)
               T16 = midpoint2(sf * TAU / edist(p1, p2), p2, p1)
               T14v1, T14v2, T15v2 = midpoint2(sf * TAU**2 / edist(p1, p2), p2, p1), \
                                     midpoint2(sf * TAU**2 / edist(p3, p4), p3, p4), \
                                     midpoint2(sf * TAU / edist(p3, p4), p3, p4)
               T14 = midpoint2(sf * TAU / edist(p2, p3), T14v1, T14v2)
               T15 = midpoint2(sf * TAU / edist(p2, p3), T16, T15v2)
               
               next_tiles = [
                    AmmannA3Tile(A3CHAIR_TILE, T11, T12, T13, T14, T15, T16), 
                    AmmannA3Tile(A3CHAIR2_TILE, p1, T16, T15, T14, T13, p4, p5, p6), 
               ]; 
          elif self.tile_type == A3CHAIR2_TILE: # for debugging 
               p1, p2, p3, p4, p5, p6, p7, p8 = self.to_points()
               sf = edist(p1, p8) / (TAU**3) # scaling factor 
               
               T11, T12 = p8, p1
               T13 = midpoint2(sf * TAU**2 / edist(p1, p2), p1, p2)
               T16 = midpoint2(sf * TAU / edist(p7, p8), p8, p7)
               T14v2 = midpoint2(sf * TAU**2 / edist(p7, p8), p8, p7)
               T14 = midpoint2(sf * TAU**2 / edist(p1, p8), T13, T14v2)
               T15v2 = midpoint2(sf * TAU / edist(p1, p2), p1, p2)
               T15 = midpoint2(sf * TAU**2 / edist(p1, p8), T15v2, T16)
               chairtile1 = AmmannA3Tile(A3CHAIR_TILE, T11, T12, T13, T14, T15, T16)
               
               ct2op = AffineTransformOp(matrix([[0, -1], [1, 0]]), V(0, 0))
               ct2points = Tiling.transform_points(chairtile1.to_points(), ct2op)
               ct2p2offset = p2 - PP(ct2points, 2)
               ct2 = map(lambda v: v + ct2p2offset, ct2points)
               chairtile2 = AmmannA3Tile(A3CHAIR_TILE, ct2[0], ct2[1], ct2[2], \
                                         ct2[3], ct2[4], ct2[5])
                                         
               ct3op = AffineTransformOp(matrix([[-1, 0], [0, -1]]), V(0, 0))
               ct3points = Tiling.transform_points(chairtile1.to_points(), ct3op)
               ct3p5offset = p5 - PP(ct3points, 2)
               ct3 = map(lambda v: v + ct3p5offset, ct3points)
               chairtile3 = AmmannA3Tile(A3CHAIR_TILE, ct3[0], ct3[1], ct3[2], \
                                         ct3[3], ct3[4], ct3[5])
                                         
               ct4 = [T13, PP(ct2, 1), PP(ct2, 6), PP(ct2, 5), PP(ct2, 4), \
                      PP(ct3, 6), PP(ct3, 5), T16, T15, T14]
               chair3tile4 = AmmannA3Tile(A3CHAIR3_TILE, ct4[0], ct4[1], ct4[2], \
                                         ct4[3], ct4[4], ct4[5], ct4[6], ct4[7], \
                                         ct4[8], ct4[9])
               
               next_tiles = [
                    chairtile1, 
                    chairtile2, 
                    chairtile3, 
                    chair3tile4, 
               ]; 
          else: # A3CHAIR3_TILE: 
               p1, p2, p3, p4, p5, p6, p7, p8, p9, p10 = self.to_points()
               sf = edist(p1, p2) / (TAU**2) # scaling factor 
               
               T11, T12, T13, T14 = p10, p1, p2, p3
               T16 = midpoint2(sf * TAU / edist(p6, p10), p10, p6)
               T15v2 = midpoint2(sf * TAU**2 / edist(p1, p10), p1, p10)
               T15 = midpoint2(sf / edist(p3, T15v2), p3, T15v2)
               chairtile1 = AmmannA3Tile(A3CHAIR_TILE, T11, T12, T13, T14, T15, T16)
               
               ct2op = AffineTransformOp(matrix([[0, 1], [-1, 0]]), V(0, 0))
               ct2points = Tiling.transform_points(chairtile1.to_points(), ct2op)
               ct2p8offset = p8 - PP(ct2points, 2)
               ct2 = map(lambda v: v + ct2p8offset, ct2points)
               chairtile2 = AmmannA3Tile(A3CHAIR_TILE, ct2[0], ct2[1], ct2[2], \
                                         ct2[3], ct2[4], ct2[5])
                                         
               ct3 = [p7, PP(ct2, 1), PP(ct2, 6), PP(ct2, 5), PP(ct2, 4), \
                      T16, T15, p4, p5, p6]
               chair3tile3 = AmmannA3Tile(A3CHAIR3_TILE, ct3[0], ct3[1], ct3[2], \
                                         ct3[3], ct3[4], ct3[5], ct3[6], ct3[7], \
                                         ct3[8], ct3[9])
               
               next_tiles = [
                    chairtile1, 
                    chairtile2, 
                    chair3tile3, 
               ];
               
          ## if 
          return next_tiles; 

     ## def 

## class 

## AmmannA3_Tiling
 # A Tiling subclass implementing the Ammann A3 substitution tiling 
##
class AmmannA3_Tiling(Tiling): 

     ## __init__
      # Initialization function for the AmmannA3_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "AmmannA3")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "AmmannA3"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([TAU**3, 0]), 
               vector([TAU**3, TAU**2]), 
               vector([TAU, TAU**2]), 
               vector([TAU, TAU]), 
               vector([0, TAU]), 
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the Ammann (A3) tiling"; 
     
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
          
          init_tile = AmmannA3Tile(A3CHAIR_TILE, self.INIT_TILE[0], \
                                   self.INIT_TILE[1], self.INIT_TILE[2], \
                                   self.INIT_TILE[3], self.INIT_TILE[4], \
                                   self.INIT_TILE[5]) 
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

