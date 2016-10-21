#### Sphinx.py 
#### Implementation of the sphinx tiling. 
#### Adapted from the source code for the Mathematica 
#### AperiodicTilings`SphinxTiling` package by Uwe Grimm
#### See: http://tilings.math.uni-bielefeld.de/substitution_rules/sphinx
#### Author: Maxie D. Schmidt
#### Created: 2016.03.02 / 2016.10.21

import numpy as np
import math
import sys

from sage.all import *
from AffineTransformOp import AffineTransformOp, IDENTITY_MATRIX, minverse
from Tiling import Tiling, edist, X, Y, V, midpoint

##
 # Definition of the default scaling parameter in the inflation procedure
##
SCALE_FACTOR = 1 / 2.0

## SphinxTile
 # A class that implements 4-tile sphinx tiles
##
class SphinxTile(object): 

     ## __init__
      # Initialization function for the SphinxTile class
      # @param pi        The vector-valued vertex in the tile
      #                  ordered counterclockwise starting from the 
      #                  lower left point
     ##
     def __init__(self, p1, p2, p3, p4, p5, last_matrix): 
          self.p1 = p1;
          self.p2 = p2; 
          self.p3 = p3; 
          self.p4 = p4; 
          self.p5 = p5; 
          self.last_matrix = last_matrix
     ## def 
     
     ## to_points
      # Returns a list of the vertices of the tile
     ##
     def to_points(self): 
          return [self.p1, self.p2, self.p3, self.p4, self.p5]; 
     ## def 
     
     ## to_subtiles
      # Returns a list of DominoTile objects corresponding to the next 
      # set of subtiles generated after one more step in the substitution tiling
     ##
     def to_subtiles(self): 
          PP = lambda points, i: points[i - 1] 
          p1, p2, p3, p4, p5 = self.to_points()
          sf = SCALE_FACTOR ## deflation scaling factor
          last_matrix = self.last_matrix
          
          M1 = matrix([[-1, 0], [0, 1]])
          t12op = AffineTransformOp(sf * last_matrix * M1 * minverse(last_matrix), V(0, 0))
          t12 = Tiling.transform_points(self.to_points(), t12op)
          t1 = map(lambda v: v + p1 - PP(t12, 2), t12)
          t2 = map(lambda v: v + midpoint(p1, p2) - PP(t12, 2), t12)
          tile1 = SphinxTile(t1[0], t1[1], t1[2], t1[3], t1[4], last_matrix * M1)
          tile2 = SphinxTile(t2[0], t2[1], t2[2], t2[3], t2[4], last_matrix * M1)
          
          M3 = matrix([[1, 0], [0, -1]])
          t3op = AffineTransformOp(sf * last_matrix * M3 * minverse(last_matrix), V(0, 0))
          t3 = Tiling.transform_points(self.to_points(), t3op)
          t3 = map(lambda v: v + midpoint(p1, p2) - PP(t3, 5), t3)
          tile3 = SphinxTile(t3[0], t3[1], t3[2], t3[3], t3[4], last_matrix * M3)
          
          M4 = 1 / 2.0 * matrix([[-1, n(sqrt(3))], [-n(sqrt(3)), -1]])
          t4op = AffineTransformOp(sf * last_matrix * M4 * minverse(last_matrix), V(0, 0))
          t4 = Tiling.transform_points(self.to_points(), t4op)
          t4 = map(lambda v: v + p5 - PP(t4, 1), t4)
          tile4 = SphinxTile(t4[0], t4[1], t4[2], t4[3], t4[4], last_matrix * M4)
          
          return [
               tile1, 
               tile2, 
               tile3, 
               tile4, 
          ];
          
     ## def 

## class 

## Sphinx_Tiling
 # A Tiling subclass implementing the sphinx tiling 
 # See: http://tilings.math.uni-bielefeld.de/substitution_rules/sphinx
##
class Sphinx_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Sphinx_Tilin class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Sphinx")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Sphinx"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [
               vector([0, 0]), 
               vector([3, 0]), 
               vector([5.0 / 2.0, sqrt(3) / 2.0]), 
               vector([3.0 / 2.0, sqrt(3) / 2.0]), 
               vector([1, sqrt(3)]), 
          ];
          self.INIT_TILE = map(n, self.INIT_TILE)
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Sphinx tiling"; 
     
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
      # Gets the polygonal Sphinx tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          init_tile = SphinxTile(self.INIT_TILE[0], \
                                 self.INIT_TILE[1], self.INIT_TILE[2], \
                                 self.INIT_TILE[3], self.INIT_TILE[4], \
                                 IDENTITY_MATRIX);  
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

