#### AmmannA4.py 
#### Implementation of the Ammann (A4) tiling 
#### See: http://tilings.math.uni-bielefeld.de/substitution/ammann-a4/
#### Author: Maxie D. Schmidt
#### Created: 2016.08.27

from sage.all import *
from Tiling import Tiling, edist, X, Y, V, solve_system
from AffineTransformOp import *

## 
 # Python constants that indicate the orientation of the A4 subtiles
##
A4SQUARE_TILE = 1; 
A4CHAIR_TILE = 2; 
A4SQUARE_UTILE = 3; 
A4CHAIR_UTILE = 4; 

P, Q = n(1.0), n(sqrt(2)) + 1

nfunc = lambda x: round(N(x, prec = 6), 10)
is_vertical = lambda P1, P2: nfunc(X(P1) - X(P2)) == 0.0
is_horizontal = lambda P1, P2: nfunc(Y(P1) - Y(P2)) == 0.0

def on_hvline_cond_func(P1, P2): 
     cond_func = lambda x, y: \
                 nfunc((Y(P1)-Y(P2))/(X(P1)-X(P2))*(x-X(P2)) + Y(P2) - y) == 0.0 \
                 if nfunc(X(P2)-X(P1)) != 0.0 else nfunc(X(P1) - x) == 0.0 and \
                 nfunc(X(P2) - x) == 0.0
     return cond_func
## def 

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
     def __init__(self, tile_type, p1, p2, p3, p4, p5, p6, p7 = None, p8 = None): 
          self.tile_type = tile_type; 
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
          s = Q / (2.0 * Q + P) # scaling factor 
          if self.tile_type == A4SQUARE_TILE: 
               Pl, Ql = edist(self.p2, self.p3), edist(self.p1, self.p2)
               lp, lq = s * Pl, s * Ql
               
               stile1op = AffineTransformOp(s * matrix([[1, 0], [0, 1]]), \
                                            vector([0, 0]))
               stile1 = map(lambda pt: s * pt, self.to_points())
               stile1_offset_vector = self.p1 - PP(stile1, 1)
               stile1 = map(lambda pt: pt + stile1_offset_vector, stile1)
               stile2_offset_vector = self.p5 - PP(stile1, 5)
               stile2 = map(lambda pt: pt + stile2_offset_vector, stile1)
               
               p1, p3, p5, p7 = self.p7, PP(stile1, 5), self.p3, PP(stile2, 1)
               cond_func4, cond_func2, cond_func6, cond_func8 = \
                    on_hvline_cond_func(self.p3, PP(stile1, 8)), \
                    on_hvline_cond_func(self.p7, PP(stile1, 3)), \
                    on_hvline_cond_func(self.p3, PP(stile2, 6)), \
                    on_hvline_cond_func(self.p7, PP(stile2, 3)) 
               [p2x, p2y] = solve_system([X(p3), Y(p3)], lp, [X(p1), Y(p1)], lq, cond_func2)
               [p4x, p4y] = solve_system([X(p3), Y(p3)], lp, [X(p5), Y(p5)], lq, cond_func4)
               #[p6x, p6y] = solve_system([X(p7), Y(p7)], lp, [X(p5), Y(p5)], lq, cond_func6)
               p6solve2, p8solve2, solve2_rhs = PP(stile2, 2), PP(stile2, 8), s * (Ql-Pl)
               [p6x, p6y] = solve_system([X(p7), Y(p7)], lp, [X(p6solve2), Y(p6solve2)], \
                                         solve2_rhs, cond_func6)
               #[p8x, p8y] = solve_system([X(p7), Y(p7)], lp, [X(p1), Y(p1)], lq, cond_func8)
               [p8x, p8y] = solve_system([X(p7), Y(p7)], lp, [X(p8solve2), Y(p8solve2)], \
                                         solve2_rhs, cond_func8)
               p2, p4, p6, p8 = vector([p2x, p2y]), vector([p4x, p4y]), \
                                vector([p6x, p6y]), vector([p8x, p8y]) 
               stile3 = [p1, p2, p3, p4, p5, p6, p7, p8]

               
               ast1 = AmmannA4Tile(A4SQUARE_TILE, stile1[0], stile1[1], stile1[2], \
                                   stile1[3], stile1[4], stile1[5], stile1[6], stile1[7])
               ast2 = AmmannA4Tile(A4SQUARE_TILE, stile2[0], stile2[1], stile2[2], \
                                   stile2[3], stile2[4], stile2[5], stile2[6], stile2[7])
               ast3 = AmmannA4Tile(A4SQUARE_TILE, stile3[0], stile3[1], stile3[2], \
                                   stile3[3], stile3[4], stile3[5], stile3[6], stile3[7])
               
               p11, p12, p13, p14, p15, p16 = self.p3, self.p2, PP(stile1, 2), \
                                              PP(stile1, 3), PP(stile1, 4), PP(stile3, 4)
               p21, p22, p23, p24, p25, p26 = PP(stile3, 5), self.p4, PP(stile2, 4), \
                                              PP(stile2, 3), PP(stile2, 2), PP(stile3, 6)
               p31, p32, p33, p34, p35, p36 = self.p7, self.p6, PP(stile2, 6), \
                                              PP(stile2, 7), PP(stile2, 8), PP(stile3, 8)
               p41, p42, p43, p44, p45, p46 = self.p7, self.p8, PP(stile1, 8), \
                                              PP(stile1, 7), PP(stile1, 6), PP(stile3, 2)
               act1 = AmmannA4Tile(A4CHAIR_TILE, p11, p12, p13, p14, p15, p16)
               act2 = AmmannA4Tile(A4CHAIR_TILE, p21, p22, p23, p24, p25, p26)
               act3 = AmmannA4Tile(A4CHAIR_TILE, p31, p32, p33, p34, p35, p36)
               act4 = AmmannA4Tile(A4CHAIR_TILE, p41, p42, p43, p44, p45, p46)
               
               next_tiles = [
                    ast1, ast2, ast3, act1, act2, act3, act4
               ]; 
          elif self.tile_type == A4SQUARE_UTILE: # for debugging 
               p1, p2, p3, p4, p5, p6, p7, p8 = self.to_points()
               next_tiles = [
                    AmmannA4Tile(A4SQUARE_UTILE, p1, p2, p3, p4, p5, p6, p7, p8), 
               ]; 
          elif self.tile_type == A4CHAIR_UTILE: # for debugging 
               p1, p2, p3, p4, p5, p6 = self.to_points()
               next_tiles = [
                    AmmannA4Tile(A4CHAIR_UTILE, p1, p2, p3, p4, p5, p6), 
               ]; 
          else: # A4CHAIR_TILE: 
               Pl, Ql = edist(self.p3, self.p4), edist(self.p1, self.p2)
               lp, lq = s * Pl, s * Ql
               
               c1op = AffineTransformOp(s * matrix([[-1, 0], [0, -1]]), \
                                            vector([0, 0]))
               c2op = AffineTransformOp(s * matrix([[0, -1], [-1, 0]]), \
                                            vector([0, 0]))
               
               c3op_matrix = s * matrix([[1, 0], [0, -1]])
               if is_vertical(self.p1, self.p2) and is_horizontal(self.p2, self.p3): 
                    c3op_matrix *= -1.0
               c3op = AffineTransformOp(c3op_matrix, V(0, 0))
               
               c1tile = Tiling.transform_points(self.to_points(), c1op)
               c1tile_offset = self.p6 - PP(c1tile, 2)
               c1tile = map(lambda pt: pt + c1tile_offset, c1tile)
               c2tile = Tiling.transform_points(self.to_points(), c2op)
               c2tile_offset = self.p2 - PP(c2tile, 2)
               c2tile = map(lambda pt: pt + c2tile_offset, c2tile)
               c3tile = Tiling.transform_points(self.to_points(), c3op)
               c3tile_offset = self.p3 - PP(c3tile, 2)
               c3tile = map(lambda pt: pt + c3tile_offset, c3tile)
               
               act1 = AmmannA4Tile(A4CHAIR_TILE, c1tile[0], c1tile[1], c1tile[2], \
                                   c1tile[3], c1tile[4], c1tile[5])
               act2 = AmmannA4Tile(A4CHAIR_TILE, c2tile[0], c2tile[1], c2tile[2], \
                                   c2tile[3], c2tile[4], c2tile[5])
               act3 = AmmannA4Tile(A4CHAIR_TILE, c3tile[0], c3tile[1], c3tile[2], \
                                   c3tile[3], c3tile[4], c3tile[5])

               cond_funcpm = lambda x, y: \
                    nfunc(edist(V(x, y), PP(c2tile, 6)) - lp) == 0.0 and \
                    nfunc(edist(V(x, y), PP(c1tile, 5)) - lq) == 0.0
               #cond_funcpm = lambda x, y: \
               #     nfunc(edist(V(x, y), self.p1) - n(sqrt(2)) * (lq + lp)) == 0.0
               print PP(c2tile, 6), ", ", lp, ", ", PP(c1tile, 5), ", ", lq
               print PP(c1tile, 6), ", ", lp, ", ", PP(c2tile, 5), ", ", lq, "\n"
               
               [pmx, pmy] = solve_system(PP(c1tile, 6), lp, PP(c2tile, 5), lq, cond_funcpm)
               pmid = vector([pmx, pmy])
               #pmid = (self.p2 + self.p6) / 2.0
               #print lq**2, ", ", X(self.p2)**2
               #pmx = n(sqrt(abs(lq**2 - X(self.p2)**2)))
               #pmy = Y((self.p1 + self.p6) / 2.0)
               #pmid = vector([pmx, pmy])
               
               #pmx, pmy = None, None
               #if is_horizontal(self.p1, self.p2):
               #     pmx = X(self.p1) + lq + lp
               #     pmy = Y((self.p1 + self.p6) / 2.0)
               #else:
               #     pmx = X(self.p6) + lq
               #     pmy = Y(self.p6) + lp + lq
               ###
               #pmid = vector([pmx, pmy])
               
               #cond_funcpm = lambda x, y: \
               #     nfunc(edist(V(x, y), PP(c2tile, 6))) == nfunc(lp)
               #pmdist = n(sqrt((lp+lq)**2 + lq**2))
               #[pmx, pmy] = solve_system(self.p6, pmdist, self.p2, pmdist, cond_funcpm)
               #pmid = vector([pmx, pmy])
               
               ps11, ps12, ps13, ps14, ps15, ps16, ps17, ps18 = \
                    self.p1, PP(c2tile, 3), PP(c2tile, 4), PP(c2tile, 5), \
                    pmid, PP(c1tile, 5), PP(c1tile, 4), PP(c1tile, 3)
               ps21, ps22, ps23, ps24, ps25, ps26, ps27, ps28 = \
                    PP(c1tile, 1), PP(c1tile, 6), pmid, PP(c2tile, 6), \
                    PP(c2tile, 1), PP(c3tile, 3), PP(c3tile, 4), PP(c3tile, 5)
               
               ast1 = AmmannA4Tile(A4SQUARE_TILE, ps11, ps12, ps13, ps14, \
                                   ps15, ps16, ps17, ps18) 
               ast2 = AmmannA4Tile(A4SQUARE_TILE, ps21, ps22, ps23, ps24, \
                                   ps25, ps26, ps27, ps28) 
               
               next_tiles = [
                    act1, act2, act3, ast1, ast2, 
               ];
               
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
               vector([Q, 0]), 
               vector([Q, P]), 
               vector([P + Q, P]), 
               vector([P + Q, P + Q]), 
               vector([P, P + Q]), 
               vector([P, Q]), 
               vector([0, Q]), 
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
          
          init_tile = AmmannA4Tile(A4SQUARE_TILE, self.INIT_TILE[0], \
                                   self.INIT_TILE[1], self.INIT_TILE[2], \
                                   self.INIT_TILE[3], self.INIT_TILE[4], \
                                   self.INIT_TILE[5], self.INIT_TILE[6], \
                                   self.INIT_TILE[7]);  
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

