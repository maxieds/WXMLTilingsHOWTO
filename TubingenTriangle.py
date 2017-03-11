#### TubingenTriangle.py 
#### Implementation of the Tubingen triangle tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/tuebingen-triangle/
#### See also: https://arxiv.org/pdf/1402.2818v2.pdf
#### Author: Maxie D. Schmidt
#### Created: 2016.11.07 

from sage.all import *
from Tiling import Tiling, edist, X, Y, midpoint2

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
ATILE = 1; 
BTILE = 2; 

#phi = n(golden_ratio)

## TubingenTriangleTile
 # A class that represents the triangular tiles in the tiling
##
class TubingenTriangleTile(object): 

     ## __init__
      # Initialization function for the TubingenTriangleTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of ATILE or BTILE
      # @param pa        The vector coordinate of the vertex A in the triangle
      # @param pb        The vector coordinate of the vertex B in the triangle
      # @param pc        The vector coordinate of the vertex C in the triangle
     ##
     def __init__(self, tile_type, pa, pb, pc, phi = golden_ratio): 
          self.tile_type = tile_type; 
          self.pa = pa; 
          self.pb = pb; 
          self.pc = pc; 
          self.phi = phi
     ## def 

     ## __str__
      # Returns a string representation of the points in the tile
     ##
     def __str__(self): 
          return "pa = " + str(self.pa) + ", pb = " + str(self.pc) + \
                 ", pc = " + str(self.pc); 
     ## def 

     ## to_points
      # Returns a list of the vertex point vectors in the tile
     ##
     def to_points(self): 
          return [self.pa, self.pb, self.pc]; 
     ## def 
     
     def to_list_repr(self): 
          return [self.tile_type, self.pa, self.pb, self.pc]
     ##
     
     @staticmethod
     def from_list_repr(list_repr): 
          [tile_type, pa, pb, pc] = list_repr
          return TubingenTriangleTile(tile_type, pa, pb, pc)
     ##
     
     ## to_subtiles
      # Returns a list of golden triangle subtiles after one more 
      # substitution step
     ##
     def to_subtiles(self): 
          A, B, C = self.phi * self.pa, self.phi * self.pb, self.phi * self.pc     
          if self.tile_type == ATILE: 
               mp1 = midpoint2(1 / (self.phi**2), B, C)
               mp2 = midpoint2(1 / (self.phi**2), A, C)
               #mp1 = midpoint2(-self.phi + 2, B, C)
               #mp2 = midpoint2(-self.phi + 2, A, C)

               return[ 
                    TubingenTriangleTile(ATILE, mp1, mp2, C, self.phi), 
                    TubingenTriangleTile(BTILE, A, mp1, mp2, self.phi), 
                    TubingenTriangleTile(ATILE, B, mp1, A, self.phi), 
               ]; 
          else: # BTILE 
               mp = midpoint2(1 / self.phi**2, B, A)
               #mp = midpoint2(-self.phi + 2, B, A)

               return [ 
                    TubingenTriangleTile(ATILE, C, mp, A, self.phi), 
                    TubingenTriangleTile(BTILE, B, C, mp, self.phi), 
               ]; 
          ##           
     ## def 

## class 

## TubingenTriangle_Tiling
 # A Tiling subclass implementing the Tubingen triangle substitution tiling 
##
class TubingenTriangle_Tiling(Tiling): 

     ## __init__
      # Initialization function for the TubingenTriangle_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "TubingenTriangle")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "TubingenTriangle", 
                  phi = n(golden_ratio)): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.phi = phi

          s = phi #25.0
          itA, itC = vector([0, 0]), vector([s, 0])
          #itBx = X(0.5 * (itA + itC)) 
          #itBy = sqrt(self.phi**2-1/4) * s
          #itBy = sqrt(1-(self.phi**2)/4.0) * s
          itBx = 1 / 2.0 / phi
          itBy = sqrt(1-1/4.0/(phi**2))
          self.INIT_TILE = [
               itA, # pa
               vector([itBx, itBy]), # pb
               itC, # pc
          ];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "the Tubingen triangle tiling"; 
     
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
          #next_tiles = []; 
          #for tile in prev_tiles: 
          #     subtiles = tile.to_subtiles(); 
          #     next_tiles.extend(subtiles); 
          ## for 
          #return next_tiles; 
          next_tiles = []; 
          for tilelst in prev_tiles: 
               ttile = TubingenTriangleTile.from_list_repr(tilelst)
               subtiles = ttile.to_subtiles(); 
               subtiles = map(lambda ttile: ttile.to_list_repr(), subtiles)
               next_tiles.extend(subtiles); 
          ## for 
          return next_tiles;
     ## def 
     
     ## get_tiles
      # Gets the polygonal GoldenTriangle tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          init_tile = self.get_initial_tile(); 
          init_tt_tile = TubingenTriangleTile(ATILE, init_tile[1], init_tile[0], 
                                              init_tile[2], self.phi); 
          tile_list = [init_tt_tile.to_list_repr()]; 
          for n in range(1, self.num_steps + 1): 
               next_tiles_list = self.get_next_tiling(tile_list); 
               tile_list = next_tiles_list; 
          ## for 
          
          rtiles_list = []; 
          for (idx, tt_tile) in enumerate(tile_list): 
               tt_tile2 = TubingenTriangleTile.from_list_repr(tt_tile)
               rtiles_list.append(tt_tile2.to_points()); 
          ## for 
          return rtiles_list; 

     ## def 

## class 

