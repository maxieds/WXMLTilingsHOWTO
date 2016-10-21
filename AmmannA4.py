#### AmmannA4.py 
#### Implementation of the Ammann (A4) tiling 
#### See: http://tilings.math.uni-bielefeld.de/substitution/ammann-a4/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.27

from sage.all import *
from Tiling import Tiling, edist, X, Y, V, midpoint2
from AffineTransformOp import *
import itertools

## 
 # Python constants that indicate the orientation of the A4 subtiles
##
A4SQUARE_TILE = 1; 
A4CHAIR_TILE = 2; 
A4SQUARE_UTILE = 3; 
A4CHAIR_UTILE = 4; 

P, Q = n(1.0), n(sqrt(2))

## From: http://stackoverflow.com/questions/2150108/efficient-way-to-shift-a-list-in-python
def shift(lst, n):
    return list(reversed(list(itertools.islice(itertools.cycle(lst), n , n + len(lst)))))

## AmmannA4Tile
 # A class that implements the two A4 prototiles subtiles
##
class AmmannA4Tile(object): 

     ## __init__
      # Initialization function for the AmmannA4Tile class
      # @param tile_type The orientation of the tile. Should be one of:
      #                  A4SQUARE_TILE or A4CHAIR_TILE
      # @param pi        The vector-valued rectangle vertex in the tile
      #                  ordered counterclockwise starting from the 
      #                  lower left point
     ##
     def __init__(self, tile_type, last_matrix, p1, p2, p3, p4, p5, p6, \
                  p7 = None, p8 = None, num_reflections = 0): 
          self.tile_type = tile_type; 
          self.last_matrix = last_matrix
          self.nr = num_reflections
          self.p1 = p1;
          self.p2 = p2; 
          self.p3 = p3; 
          self.p4 = p4; 
          self.p5 = p5; 
          self.p6 = p6; 
          self.p7 = p7; 
          self.p8 = p8; 
     ## def 
     
     def __str__(self): 
          return str(self.to_points())
     ## def
     
     ## to_points
      # Returns a list of the vertices of the tile
     ##
     def to_points(self): 
          if self.tile_type == A4CHAIR_TILE or self.tile_type == A4CHAIR_UTILE: 
               return [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]; 
          else:
               return [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, \
                       self.p7, self.p8]; 
     ## def 
     
     ## to_substiles
      # Returns a list of DominoTile objects corresponding to the next 
      # set of subtiles generated after one more step in the substitution tiling
     ##
     def to_subtiles(self): 
          PP = lambda points, i: points[i - 1] 
          if self.tile_type == A4CHAIR_TILE: 
               p1, p2, p3, p4, p5, p6 = self.to_points()
               sf = P / (P + Q) # scaling factor
               Pl = edist(p3, p4)
               Ql = edist(p1, p2) - Pl
               last_matrix = self.last_matrix
               
               last_matrix_arg1 = last_matrix * matrix([[0, -1], [-1, 0]]) * minverse(last_matrix)
               ct1op = AffineTransformOp(sf * last_matrix_arg1, V(0, 0))
               ct1 = Tiling.transform_points(self.to_points(), ct1op)
               ct1poffset = p2 - PP(ct1, 2) 
               ct1 = map(lambda v: v + ct1poffset, ct1)
               chairtile1 = AmmannA4Tile(A4CHAIR_TILE, matrix([[0, -1], [-1, 0]]) * last_matrix, 
                                         ct1[0], ct1[1], ct1[2], \
                                         ct1[3], ct1[4], ct1[5], self.nr)
               
               last_matrix_arg2 = last_matrix * matrix([[1, 0], [0, -1]]) * minverse(last_matrix)
               ct2op = AffineTransformOp(sf * last_matrix_arg2, V(0, 0))
               ct2points = Tiling.transform_points(self.to_points(), ct2op)
               ct2p3offset = p4 - PP(ct2points, 1)
               ct2 = map(lambda v: v + ct2p3offset, ct2points)
               chairtile2 = AmmannA4Tile(A4CHAIR_TILE, matrix([[1, 0], [0, -1]]) * last_matrix, 
                                         ct2[0], ct2[1], ct2[2], \
                                         ct2[3], ct2[4], ct2[5], self.nr)
                                         
               last_matrix_arg3 = last_matrix * matrix([[-1, 0], [0, -1]]) * minverse(last_matrix)
               ct3op = AffineTransformOp(sf * last_matrix_arg3, V(0, 0))
               ct3points = Tiling.transform_points(self.to_points(), ct3op)
               ct3p6offset = p6 - PP(ct3points, 2)
               ct3 = map(lambda v: v + ct3p6offset, ct3points)
               chairtile3 = AmmannA4Tile(A4CHAIR_TILE, matrix([[-1, 0], [0, -1]]) * last_matrix, 
                                         ct3[0], ct3[1], ct3[2], \
                                         ct3[3], ct3[4], ct3[5], self.nr)
                                         
               T56v2 = midpoint2(sf * (Pl + Ql) / edist(p1, p2), p2, p1)
               sqtile_intpt = midpoint2(sf * (2 * Pl + Ql) / edist(p1, p6), T56v2, p5)
               
               st1 = [p1, PP(ct1, 3), PP(ct1, 4), PP(ct1, 5), sqtile_intpt, \
                      PP(ct3, 5), PP(ct3, 4), PP(ct3, 3)]
               sqtile1 = AmmannA4Tile(A4SQUARE_TILE, last_matrix, 
                                      st1[0], st1[1], st1[2], \
                                      st1[3], st1[4], st1[5], st1[6], st1[7], self.nr)
               
               #st2 = [PP(ct1, 1), PP(ct2, 3), PP(ct2, 4), PP(ct2, 5), \
               #       PP(ct3, 1), PP(ct3, 6), sqtile_intpt, PP(ct1, 6)]
               st2 = [PP(ct1, 1), PP(ct1, 6), sqtile_intpt, PP(ct3, 6), \
                      PP(ct3, 1), PP(ct2, 5), PP(ct2, 4), PP(ct2, 3)]
               sqtile2 = AmmannA4Tile(A4SQUARE_TILE, matrix([[-1, 0], [0, 1]]) * last_matrix, 
                                      st2[0], st2[1], st2[2], \
                                      st2[3], st2[4], st2[5], st2[6], st2[7], self.nr + 1)

               next_tiles = [
                    chairtile1, 
                    chairtile2, 
                    chairtile3, 
                    sqtile1, 
                    sqtile2, 
               ]; 
          elif self.tile_type == A4SQUARE_TILE:
               
               p1, p2, p3, p4, p5, p6, p7, p8 = self.to_points() 
               #if self.nr % 2 == 0: 
               #     p1, p2, p3, p4, p5, p6, p7, p8 = \
               #     map(lambda idx: self.to_points()[idx], shift(list(reversed(range(0, 8))), self.nr % 2))
               tilepts = [p1, p2, p3, p4, p5, p6, p7, p8]
               sf = P / (P + Q) # scaling factor
               Pl = edist(p2, p3)
               Ql = edist(p1, p2) - Pl
               last_matrix = self.last_matrix
               
               last_matrix_arg12 = last_matrix * matrix([[1, 0], [0, 1]]) * minverse(last_matrix)
               st12op = AffineTransformOp(sf * last_matrix_arg12, V(0, 0))
               st1 = Tiling.transform_points(tilepts, st12op)
               st1 = map(lambda v: v + p1 - PP(st1, 1), st1)
               st2 = Tiling.transform_points(tilepts, st12op)
               st2poffset = p5 - PP(st2, 5)
               st2 = map(lambda v: v + st2poffset, st2)
               stile1 = AmmannA4Tile(A4SQUARE_TILE, last_matrix, st1[0], \
                                     st1[1], st1[2], st1[3], st1[4], \
                                     st1[5], st1[6], st1[7], self.nr)
               stile2 = AmmannA4Tile(A4SQUARE_TILE, last_matrix, st2[0], \
                                     st2[1], st2[2], st2[3], st2[4], \
                                     st2[5], st2[6], st2[7], self.nr)
                                         
               last_matrix_arg3 = last_matrix * matrix([[-1, 0], [0, 1]]) * minverse(last_matrix)
               st3op = AffineTransformOp(sf * last_matrix_arg3, V(0, 0))
               st3 = Tiling.transform_points(tilepts, st3op)
               st3poffset = p3 - PP(st3, 1)
               st3 = map(lambda v: v + st3poffset, st3)
               stile3 = AmmannA4Tile(A4SQUARE_TILE, matrix([[-1, 0], [0, 1]]) * last_matrix, 
                                     st3[0],st3[1], st3[2], st3[3], st3[4], \
                                     st3[5], st3[6], st3[7], self.nr + 1)
               
               ct1 = [p3, p2, PP(st1, 2), PP(st1, 3), PP(st1, 4), PP(st3, 2)] 
               ctile1 = AmmannA4Tile(A4CHAIR_TILE, matrix([[0, -1], [-1, 0]]) * last_matrix, 
                                     ct1[0], ct1[1], ct1[2], ct1[3], ct1[4], ct1[5], self.nr + 1)
                                     
               ct2 = [p3, p4, PP(st2, 4), PP(st2, 3), PP(st2, 2), PP(st3, 8)] 
               ctile2 = AmmannA4Tile(A4CHAIR_TILE, last_matrix, 
                                     ct2[0], ct2[1], ct2[2], ct2[3], ct2[4], ct2[5], self.nr)
                                     
               ct3 = [p7, p8, PP(st1, 8), PP(st1, 7), PP(st1, 6), \
                      PP(st3, 4)] 
               ctile3 = AmmannA4Tile(A4CHAIR_TILE, matrix([[-1, 0], [0, -1]]) * last_matrix, 
                                     ct3[0], ct3[1], ct3[2], ct3[3], ct3[4], ct3[5], self.nr)
               
               ct4 = [p7, p6, PP(st2, 6), PP(st2, 7), PP(st2, 8), \
                      PP(st3, 6)] 
               ctile4 = AmmannA4Tile(A4CHAIR_TILE, matrix([[0, 1], [1, 0]]) * last_matrix, 
                                     ct4[0], ct4[1], ct4[2], ct4[3], ct4[4], ct4[5], self.nr + 1)
               
               next_tiles = [
                    stile1, 
                    stile2, 
                    stile3, 
                    ctile1, 
                    ctile2, 
                    ctile3, 
                    ctile4, 
               ]; 
          else: 
               return [self];
          ## if 
          return next_tiles; 

     ## def 

## class 

## AmmannA4_Tiling
 # A Tiling subclass implementing the Ammann A4 substitution tiling 
##
class AmmannA4_Tiling(Tiling): 

     ## __init__
      # Initialization function for the AmmannA4_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "AmmannA4")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "AmmannA4"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([P + Q, 0]), 
               vector([P + Q, 2 * P + Q]), 
               vector([Q, 2 * P + Q]), 
               vector([Q, P + Q]), 
               vector([0, P + Q]), 
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the Ammann (A4) tiling"; 
     
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
          
          init_tile = AmmannA4Tile(A4CHAIR_TILE, IDENTITY_MATRIX, \
                                   self.INIT_TILE[0], \
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

