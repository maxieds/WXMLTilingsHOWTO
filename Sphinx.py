#### Sphinx.py 
#### Implementation of the sphinx tiling. 
#### Adapted from the source code for the Mathematica 
#### AperiodicTilings`SphinxTiling` package by Uwe Grimm
#### See: http://tilings.math.uni-bielefeld.de/substitution_rules/sphinx
#### Author: Maxie D. Schmidt
#### Created: 2016.03.02 

import numpy as np
import math
import sys

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y

##
 # Definition of the default scaling parameter in the inflation procedure
##
SCALE_FACTOR = 2; 

## TwoVector
 # Recursive procedure to generate a vector from an input tile number
 # @param num Non-negative integer representing a tile number 
 # @return    A vector representing the input tile vertex
##
def TwoVector(num): 
     if num == 0: 
          return vector([1, 0]); 
     elif num == 1: 
          return vector([0, 1]); 
     elif num == 2:
          return vector([-1, 1]); 
     elif num == 3: 
          return -1 * TwoVector(0); 
     elif num == 4: 
          return -1 * TwoVector(1); 
     elif num == 5: 
          return -1 * TwoVector(2); 
     else: 
          return TwoVector(num % 6); 
## def 

## TileMod
 # Returns a modded integer index for the input tile's label number
 # @param num An integer tile number label
 # @return    An integer corresponding to the tile's integer label
##
def TileMod(num): 
     modfn = lambda x: x + 6 * math.floor((6 - x) / 6); 
     return np.sign(num) * modfn(abs(num) % 6); 
## def 

## TwoCoordinates
 # Returns an actual vector representing the tiling coordinates of the input 
 # local vector used in the substitution procedure
 # @param xy An input vector in local coordinates 
 # @return   A transformed vector in actual plot coordinates
##
def TwoCoordinates(xy): 
     return vector([X(xy) + Y(xy) * 0.5, float(sqrt(3)) * Y(xy) * 0.5]); 
## def 

## TileCoordinates
 # Computes the local sphinx tile representation corresponding to the 
 # input parameters 
 # @param tile      An integer tile index
 # @param ref_point An integer tile reference point index 
 # @return          A corresponding polygonal tile in the sphinx tiling 
## 
def TileCoordinates(tile, ref_point): 

     if tile == 0: 
          print "TileInflation: Error tile need to be positive or negative"; 
          sys.exit(1); 
     ## if 
    
     mapfn = lambda l: ref_point + l; 
     coordfn = lambda a1, a2: \
               map(mapfn, [0, a2, a1 + a2, a1 + 2 * a2, 3 * a1]); 
     
     if tile > 0: 
          return coordfn(TwoVector(tile - 1), TwoVector(tile)); 
     else: #tile < 0: 
          return coordfn(TwoVector(tile + 4), TwoVector(tile + 3)); 
     ## if 
     
## def 

## TileInflation
 # Performs one step forward in the tile inflation procedure
 # @param tile      The initial tile number as an integer 
 # @param ref_point Tile reference point as an integer
 # @return          A list of subtiles after one substitution step forward 
 #                  for the input tile
##
def TileInflation(tile, ref_point): 
     
     if tile > 0: 
          inflate = lambda a1, a2, a3, a4, a5, a6, a7: \
                    [[a6, SCALE_FACTOR * (a7 + 3 * TwoVector(a1) / 2)], 
                     [a6, SCALE_FACTOR * (a7 + 3 * TwoVector(a1))], 
                     [a4, SCALE_FACTOR * (a7 + 3 * TwoVector(a1) + TwoVector(a3) / 2)], 
                     [a5, SCALE_FACTOR * (a7 + TwoVector(a2))], 
                    ]; 
          return inflate(TileMod(tile - 1), TileMod(tile), TileMod(tile + 1), \
                         TileMod(tile + 2), TileMod(tile - 11), \
                         TileMod(tile - 8), ref_point); 
     elif tile < 0: 
          inflate = lambda a1, a2, a3, a4, a5, a6: \
                    [[a5, SCALE_FACTOR * (a6 + 3 * TwoVector(a1) / 2)], 
                     [a5, SCALE_FACTOR * (a6 + 3 * TwoVector(a1))], 
                     [a1, SCALE_FACTOR * (a6 + 3 * TwoVector(a1) + TwoVector(a3) / 2)], 
                     [a4, SCALE_FACTOR * (a6 + TwoVector(a2))], 
                    ]; 
          return inflate(TileMod(tile - 2), TileMod(tile - 3), \
                         TileMod(tile - 4), TileMod(tile + 11), \
                         TileMod(tile + 8), ref_point); 
     else: 
          print "TileInflation: Error tile need to be positive or negative"; 
          sys.exit(1); 
     ## if 

## def 

## Inflate
 # Gets the next list of tiles after one subsequent substitution step
 # @param tiles_list A list of previous tiles in the substitution procedure 
 # @return           A list of subtiles representing one step forward in the 
 #                   substitution procedure 
##
def Inflate(tiles_list): 
     
     mapfn = lambda input_list: \
             TileInflation(input_list[0], input_list[1]); 
     next_tiles_list = map(mapfn, tiles_list); 
     rtiles_list = []; 
     for tlist in next_tiles_list: 
          rtiles_list.extend(tlist); 
     ## for 
     return rtiles_list; 

## def 

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
          self.INIT_TILE = [];
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
          return Inflate(prev_tiles); 
     ## def 
     
     ## get_tiles
      # Gets the polygonal Sphinx tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          init_tile = [1, vector([0, 0])]; 
          tile_list = [init_tile]; 
          for n in range(1, self.N): 
               next_tiles_list = self.get_next_tiling(tile_list); 
               tile_list = next_tiles_list;
          ## for 
          
          tile_points = []; 
          for tile in tile_list: 
               tile_coords = TileCoordinates(tile[0], tile[1]); 
               two_coords = map(TwoCoordinates, tile_coords); 
               tile_points.append(two_coords); 
          ## for 
          
          return tile_points; 

     ## def 

## class 

