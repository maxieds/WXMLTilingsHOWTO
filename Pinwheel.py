#### Pinwheel.py 
#### Implementation of the pinwheel tiling. 
#### Adapted from the source code for the Mathematica 
#### AperiodicTilings`PinwheelTiling` package by Uwe Grimm
#### See: http://tilings.math.uni-bielefeld.de/substitution_rules/pinwheel
#### Author: Maxie D. Schmidt
#### Created: 2016.03.02 

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y

##
 # Definition of the default scaling parameter in the inflation procedure
##
SCALE_FACTOR = float(sqrt(5)); 

## TileInflation
 # Performs one step forward in the tile inflation procedure
 # @param tv1 First tile vertex in the substitution procedure
 # @param tv2 Second tile vertex in the substitution procedure
 # @param tv3 Third tile vertex in the substitution procedure
 # @return A list of subtiles after one substitution step forward for the 
 #         input tile vertices 
##
def TileInflation(tv1, tv2, tv3): 

     inflate = lambda a1, a2, a3, a4, a5, a6, a7: \
               [[a1, a5, a4], 
                [a4, a7, a2], 
                [a4, a7, a6], 
                [a6, a5, a4], 
                [a2, a6, a3]]; 
     inflated_tiles = inflate(tv1, tv2, tv3, \
                              tv1 / 2 + tv2 / 2, \
                              3 * tv1 / 5 + 2 * tv3 / 5, \
                              tv1 / 5 + 4 * tv3 / 5, \
                              tv1 / 10 + tv2 / 2 + 2 * tv3 / 5); 
     scalefn = lambda v: SCALE_FACTOR * v; 
     next_tiles = []; 
     for tile in inflated_tiles: 
          next_tile = map(scalefn, tile); 
          next_tiles.append(next_tile); 
     ## for 
     return next_tiles; 

## def

## Inflate
 # Gets the next list of tiles after one subsequent substitution step
 # @param tiles_list A list of previous tiles in the substitution procedure 
 # @return           A list of subtiles representing one step forward in the 
 #                   substitution procedure 
##
def Inflate(tiles_list): 
     
     mapfn = lambda input_list: \
             TileInflation(input_list[0], input_list[1], input_list[2]); 
     next_tiles_list = map(mapfn, tiles_list); 
     rtiles_list = []; 
     for tlist in next_tiles_list: 
          rtiles_list.extend(tlist); 
     ## for 
     return rtiles_list; 

## def 

## Pinwheel_Tiling
 # A Tiling subclass implementing the pinwheel tiling 
 # See: http://tilings.math.uni-bielefeld.de/substitution_rules/pinwheel
##
class Pinwheel_Tiling(Tiling): 

      ## __init__
      # Initialization function for the Pinwheel_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "Pinwheel")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "Pinwheel"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [vector([0, 0]), vector([2, 0]), vector([2, 1])];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Pinwheel tiling"; 
     
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
      # Gets the polygonal Pinwheel tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          init_tile = self.get_initial_tile(); 
          tile_list = [init_tile]; 
          for n in range(1, self.N): 
               next_tiles_list = self.get_next_tiling(tile_list); 
               tile_list = next_tiles_list;
          ## for 
          return tile_list;

     ## def 

## class 

