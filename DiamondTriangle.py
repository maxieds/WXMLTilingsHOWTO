#### DiamondTriangle.py 
#### Implementation of the diamond triangle tiling
#### See: http://tilings.math.uni-bielefeld.de/substitution/diamond-triangle/
#### Author: Maxie D. Schmidt
#### Created: 2016.09.16 

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling, edist, X, Y

## 
 # Python constants to denote the distinct tile types in the substitution tiling
##
BTILE = 1; 
OTILE = 2; 

## DTriangleTile
 # A class that represents the triangular tiles in the tiling
##
class DTriangleTile(object): 

     ## __init__
      # Initialization function for the DTriangleTile
      # @param tile_type Tile type in the substitution tiling. Should be 
      #                  one of BTILE or OTILE
      # @param pa        The vector coordinate of the vertex A in the triangle
      # @param pb        The vector coordinate of the vertex B in the triangle
      # @param pc        The vector coordinate of the vertex C in the triangle
     ##
     def __init__(self, tile_type, pa, pb, pc, pd = None): 
          self.tile_type = tile_type 
          self.pa = pa 
          self.pb = pb 
          self.pc = pc 
          self.pd = pd
     ## def 

     ## to_points
      # Returns a list of the vertex point vectors in the tile
     ##
     def to_points(self): 
          if self.tile_type == OTILE:
               return [self.pa, self.pb, self.pc]
          else: 
               return [self.pa, self.pb, self.pc, self.pd]
     ## def 
     
     ## to_subtiles
      # Returns a list of subtiles after one more 
      # substitution step
     ##
     def to_subtiles(self): 
          A, B, C, D = self.pa, self.pb, self.pc, self.pd    
          if self.tile_type == OTILE: 
               t1AB, t1AC = 2.0 / 3.0 * A + 1.0 / 3.0 * B,\
                            2.0 / 3.0 * A + 1.0 / 3.0 * C
               t2AC, t2CB = 2.0 / 3.0 * C + 1.0 / 3.0 * A,\
                            2.0 / 3.0 * C + 1.0 / 3.0 * B
               t3CB, t3BA = 2.0 / 3.0 * B + 1.0 / 3.0 * C,\
                            2.0 / 3.0 * B + 1.0 / 3.0 * A
               midptt1, midptt2, midptt3 = (t1AB + t1AC) / 2.0, \
                    (t2AC + t2CB) / 2.0, (t3CB + t3BA) / 2.0
               mptAB, mptBC, mptAC = (t1AB + t3BA) / 2.0, \
                    (t3CB + t2CB) / 2.0, (t1AC + t2AC) / 2.0
               trimidpt = (midptt2 + mptAB) / 2.0
               pt1AB, pt2AB = 2.0 / 3.0 * midptt1 + 1.0 / 3.0 * midptt3, \
                              2.0 / 3.0 * midptt3 + 1.0 / 3.0 * midptt1
               pt1AC, pt2AC = 2.0 / 3.0 * midptt1 + 1.0 / 3.0 * midptt2, \
                              2.0 / 3.0 * midptt2 + 1.0 / 3.0 * midptt1
               pt1BC, pt2BC = 2.0 / 3.0 * midptt2 + 1.0 / 3.0 * midptt3, \
                              2.0 / 3.0 * midptt3 + 1.0 / 3.0 * midptt2
               return[ 
                    DTriangleTile(OTILE, 
                                  pa = A, 
                                  pb = t1AB, 
                                  pc = t1AC), 
                    DTriangleTile(OTILE, 
                                  pa = C, 
                                  pb = t2AC, 
                                  pc = t2CB), 
                    DTriangleTile(OTILE, 
                                  pa = B, 
                                  pb = t3CB, 
                                  pc = t3BA), 
                    DTriangleTile(BTILE, 
                                  pa = t1AB, 
                                  pb = mptAB, 
                                  pc = pt1AB, 
                                  pd = midptt1),  
                    DTriangleTile(BTILE, 
                                  pa = pt2AB, 
                                  pb = mptAB, 
                                  pc = pt1AB, 
                                  pd = trimidpt), 
                    DTriangleTile(BTILE, 
                                  pa = t3BA, 
                                  pb = mptAB, 
                                  pc = pt2AB, 
                                  pd = midptt3), 
                    DTriangleTile(BTILE, 
                                  pa = pt2AB, 
                                  pb = midptt3, 
                                  pc = pt2BC, 
                                  pd = trimidpt), 
                    DTriangleTile(BTILE, 
                                  pa = t3CB, 
                                  pb = midptt3, 
                                  pc = pt2BC, 
                                  pd = mptBC),  
                    DTriangleTile(BTILE, 
                                  pa = pt2BC, 
                                  pb = trimidpt, 
                                  pc = pt1BC, 
                                  pd = mptBC),  
                    DTriangleTile(BTILE, 
                                  pa = pt1BC, 
                                  pb = mptBC, 
                                  pc = t2CB, 
                                  pd = midptt2), 
                    DTriangleTile(BTILE, 
                                  pa = pt1BC, 
                                  pb = trimidpt, 
                                  pc = pt2AC, 
                                  pd = midptt2), 
                    DTriangleTile(BTILE, 
                                  pa = pt2AC, 
                                  pb = mptAC, 
                                  pc = t2AC, 
                                  pd = midptt2), 
                    DTriangleTile(BTILE, 
                                  pa = pt1AC, 
                                  pb = trimidpt, 
                                  pc = pt2AC, 
                                  pd = mptAC), 
                    DTriangleTile(BTILE, 
                                  pa = pt1AC, 
                                  pb = midptt1, 
                                  pc = t1AC, 
                                  pd = mptAC), 
                    DTriangleTile(BTILE, 
                                  pa = pt1AB, 
                                  pb = midptt1, 
                                  pc = pt1AC, 
                                  pd = trimidpt), 
               ]; 
          else: # BTILE 
               t11, t12, t21, t22 = 1.0 / 3.0 * D + 2.0 / 3.0 * C, \
                                    1.0 / 3.0 * D + 2.0 / 3.0 * A, \
                                    1.0 / 3.0 * B + 2.0 / 3.0 * C, \
                                    1.0 / 3.0 * B + 2.0 / 3.0 * A
               mptt1, mptt2 = (t11 + t12) / 2.0, (t21 + t22) / 2.0
               centpt1, centpt2 = 2.0 / 3.0 * A + 1.0 / 3.0 * C, \
                                  2.0 / 3.0 * C + 1.0 / 3.0 * A
               
               return [DTriangleTile(BTILE, A, B, C, D)]
               #### !!!! Fill these coordinates in for the HOWTO !!!! ####
               #return [ 
                    #DTriangleTile(OTILE, 
                    #              pa = D, 
                    #              pb = t11, 
                    #              pc = t12), 
                    #DTriangleTile(OTILE, 
                    #              pa = B, 
                    #              pb = t21, 
                    #              pc = t22), 
                    #DTriangleTile(BTILE, 
                    #              pa = , 
                    #              pb = , 
                    #              pc = , 
                    #              pd = ), 
                    #DTriangleTile(BTILE, 
                    #              pa = , 
                    #              pb = , 
                    #              pc = , 
                    #              pd = ), 
                    #DTriangleTile(BTILE, 
                    #              pa = , 
                    #              pb = , 
                    #              pc = , 
                    #              pd = ), 
                    #DTriangleTile(BTILE, 
                    #              pa = , 
                    #              pb = , 
                    #              pc = , 
                    #              pd = ), 
                    #DTriangleTile(BTILE, 
                    #              pa = , 
                    #              pb = , 
                    #              pc = , 
                    #              pd = ), 
               #]; 
          ##           
     ## def 

## class 

## DiamondTriangle_Tiling
 # A Tiling subclass implementing the diamond triangle substitution tiling 
##
class DiamondTriangle_Tiling(Tiling): 

     ## __init__
      # Initialization function for the DiamondTriangle_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "DiamondTriangle")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "DiamondTriangle"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          
          s = 25
          itA, itC = vector([0, 0]), vector([s, 0])
          itBx = X(0.5 * (itA + itC)) 
          itBy = sqrt(s ** 2  - itBx ** 2)
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
          return "the diamond triangle tiling"; 
     
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
      # Gets the polygonal GoldenTriangle tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          init_tile = self.get_initial_tile(); 
          init_gt_tile = DTriangleTile(OTILE, init_tile[0], init_tile[2], init_tile[1]); 
          tile_list = [init_gt_tile]; 
          for n in range(1, self.N): 
               next_tiles_list = self.get_next_tiling(tile_list); 
               tile_list = next_tiles_list; 
          ## for 
          
          rtiles_list = []; 
          for (idx, gt_tile) in enumerate(tile_list): 
               rtiles_list.append(gt_tile.to_points()); 
          ## for 
          return rtiles_list; 

     ## def 

## class 

