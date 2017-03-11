#### PChairs.py 
#### Implementation of the pregnant chairs tiling variant (variant)
#### See: http://tilings.math.uni-bielefeld.de/substitution/pregnant-chairs-variant/
#### Author: Maxie D. Schmidt
#### Created: 2016.03.29 and 2016.10.22

from sage.all import *
from AffineTransformOp import AffineTransformOp, IDENTITY_MATRIX, minverse
from Tiling import Tiling, midpoint2, V

Q = 1.0
P = n(sqrt(3)) * Q
SF  = 1.0 / 3.0 * P / Q
SF2 = Q / P * SF

## PChairsTile
 # A class that implements the PChairs subtiles
##
class PChairsTile(object): 

     ## __init__
      # Initialization function for the PChairsTile class
      # @param pi        The vector-valued rectangle vertex in the tile
      #                  ordered counterclockwise starting from the 
      #                  lower left point
     ##
     def __init__(self, p1, p2, p3, p4, p5, p6, last_matrix): 
          self.last_matrix = last_matrix
          self.p1 = p1;
          self.p2 = p2; 
          self.p3 = p3; 
          self.p4 = p4; 
          self.p5 = p5; 
          self.p6 = p6; 
     ## def 
     
     def __str__(self): 
          return str(self.to_points())
     ## def
     
     ## to_points
      # Returns a list of the vertices of the tile
     ##
     def to_points(self): 
          return [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]; 
     ## def 
     
     ## get_transformed_tile: 
      # Work-horse function to perform repeated affine transformations of the tiles:
     ##
     def get_transformed_tile(self, mtrxlst, pi, ppi, scaling_factor): 
          PP = lambda points, i: points[i - 1]
          last_matrix = self.last_matrix
          mtrxM = matrix(mtrxlst)
          atmtrx = last_matrix * mtrxM * minverse(last_matrix)
          ctop = AffineTransformOp(scaling_factor * atmtrx, V(0, 0))
          ct = Tiling.transform_points(self.to_points(), ctop)
          ctpoffset = pi - PP(ct, ppi) 
          ct = map(lambda v: v + ctpoffset, ct)
          chairtile = PChairsTile(ct[0], ct[1], ct[2], ct[3], ct[4], \
                                  ct[5], last_matrix * mtrxM)
          return chairtile
     ## def
     
     ## to_subtiles
      # Returns a list of PChairsTile objects corresponding to the next 
      # set of subtiles generated after one more step in the substitution tiling
     ##
     def to_subtiles(self): 
          p1, p2, p3, p4, p5, p6 = self.to_points()
          refpt34 = midpoint2(0.5, p1, p6)
          
          ct1 = self.get_transformed_tile([[0, 1], [1, 0]], p5, 3, SF)
          ct2 = self.get_transformed_tile([[1, 0], [0, 1]], p1, 1, SF2)
          ct3 = self.get_transformed_tile([[-1, 0], [0, -1]], refpt34, 2, SF2)
          ct4 = self.get_transformed_tile([[-1, 0], [0, 1]], refpt34, 2, SF2)
          ct5 = self.get_transformed_tile([[1, 0], [0, -1]], p6, 1, SF2)
          ct6 = self.get_transformed_tile([[1, 0], [0, 1]], p2, 2, SF2)
          ct7 = self.get_transformed_tile([[-1, 0], [0, -1]], p3, 1, SF2)
          
          return [ct1, ct2, ct3, ct4, ct5, ct6, ct7]; 

     ## def 

## class 

## PChairs_Tiling
 # A Tiling subclass implementing the pregnant chairs substitution tiling 
##
class PChairs_Tiling(Tiling): 

     ## __init__
      # Initialization function for the PChairs_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "PChairs")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "PChairs"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([2 * P, 0]), 
               vector([2 * P, Q]), 
               vector([P, Q]), 
               vector([P, 2 * Q]), 
               vector([0, 2 * Q]), 
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the pregnant chairs (variant) tiling"; 
     
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
          
          init_tile = PChairsTile(self.INIT_TILE[0], \
                                   self.INIT_TILE[1], self.INIT_TILE[2], \
                                   self.INIT_TILE[3], self.INIT_TILE[4], \
                                   self.INIT_TILE[5], IDENTITY_MATRIX);  
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

