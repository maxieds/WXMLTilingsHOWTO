#### Penrose.py 
#### Implementation of the Penrose kite-dart tiling 
#### Author: Maxie D. Schmidt
#### Created: 2016.08.31 
#### See: http://tilings.math.uni-bielefeld.de/substitution/penrose-kite-dart/
#### Adapted From: http://preshing.com/20110831/penrose-tiling-explained/

import math
import cmath
import sys

from sage.all import *
from AffineTransformOp import AffineTransformOp
from Tiling import Tiling

## 
 # Python constants denoting the type of the tile
##
COLOR_RED = 0; 
COLOR_BLUE = 1; 

## 
 # Python constants defining a default "large radius R" and a floating 
 # point constant for the golden ratio
##
DEFAULT_RADIUS_R = 10; 
GOLDEN_RATIO = float(golden_ratio); 

## PenroseKD_Tiling
 # A Tiling subclass implementing the penrose kite-dart tiling 
##
class PenroseKD_Tiling(Tiling): 

     ## __init__
      # Initialization function for the PenroseKD_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "PenroseKD")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "PenroseKD"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.INIT_TILE = [];
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Penrose kite-dart tiling"; 
     
     ## get_initial_tile
      # Returns the only tile in the tiling after zero steps
     ##
     def get_initial_tile(self): 
          return self.INIT_TILE; 
     
     ## subdivide
      # Gets the next list of tiles after one subsequent substitution step
      # @param triangles        A list of the tiles after one step back
      # @return                 A list of tiles after one more step
     ##
     def subdivide(self, triangles):
    
         result = []
         for color, A, B, C in triangles:
             if color == COLOR_RED: # Subdivide red (halk kite) triangle: 
                 Q = A + (B - A) / GOLDEN_RATIO
                 R = B + (C - B) / GOLDEN_RATIO
                 result += [(COLOR_BLUE, R, Q, B), (COLOR_RED, Q, A, R), \
                            (COLOR_RED, C, A, R)]
             elif color == COLOR_BLUE: # Subdivide blue (half dart) triangle: 
                 P = C + (A - C) / GOLDEN_RATIO
                 result += [(COLOR_BLUE, B, P, A), (COLOR_RED, P, C, B)] 
             else: 
                 sys.exit(1)
         return result
     ## def 
     
     ## complex_to_vector
      # Static method that converts an input 2D vector point into its 
      # corresponding complex number representation
     ##
     @staticmethod
     def complex_to_vector(point): 
          return vector([point.real, point.imag]); 
     
     ## get_tiles
      # Gets the polygonal Penrose tiles after N steps
      # @return A list of tiles in the computed substitution tiling
     ##
     def get_tiles(self): 
          
          # Create an initial wheel of red triangles around the origin 
          # (from the comments section of the reference): 
          radiusR = DEFAULT_RADIUS_R; 
          triangles = []
          for i in xrange(10):
               B = cmath.rect(1, (2*i - 1) * math.pi / radiusR)
               C = cmath.rect(1, (2*i + 1) * math.pi / radiusR)
               if i % 2 == 0:
                    B, C = C, B # Make sure to mirror every second triangle
               ##
               triangles.append((COLOR_RED, B, 0j, C)) 
          ##
          
          for i in range(self.num_steps):
               triangles = self.subdivide(triangles)
    
          point_to_vector = lambda pt: PenroseKD_Tiling.complex_to_vector(pt);
          
          tile_list = []; 
          for (color, A, B, C) in triangles:
               tile_list.append([point_to_vector(A), point_to_vector(B), \
                                 point_to_vector(C)]); 
          return tile_list; 

     ## def 

## class 






