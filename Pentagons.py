#### Pentagons.py 
#### Implementation of the numbered pentagon tilings from the 
#### Wolfram demos website by Ed Pegg Jr
#### See: http://demonstrations.wolfram.com/PentagonTilings/
#### Author: Maxie D. Schmidt
#### Created: 2016.03.08

import sys
from math import sin, cos, tan
from sage.all import *
from Tiling import Tiling

## cot
 # Defines the cotangent function not present in the Python math library
## 
def cot(x): return 1 / tan(x)

## Pentagon_Tiling
 # A Tiling subclass implementing a few of the numbered pentagonal tilings 
 # of the plane as numbered in the interactive Wolfram demo
 # See: http://demonstrations.wolfram.com/PentagonTilings/
##
class Pentagon_Tiling(Tiling): 

     ## __init__
      # Initialization function for the Pentagon_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Tiling name string 
      #                        (defaults to "Pentagon#" or "Pentagon##")
      # @param tiling_type     An integer in {1, 2, 3, 4, 5, 8, 10, 11, 15} 
      #                        specifying which of the known pentagon tilings 
      #                        we are computing
      # @param AA, BB, b, c, e Parameters in the tiling that change the 
      #                        shapes of the tiles when modified 
      #                        (see the interactive Wolfram demo for examples)
     ##
     def __init__(self, num_steps_N, tiling_name_str, 
                  tiling_type, AA, BB, b, c, e): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.ttype = tiling_type; 
          self.AA = AA; 
          self.BB = BB; 
          self.b = b; 
          self.c = c; 
          self.e = e; 
     ## def 
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Generic pentagon tiling (AA, BB, b, c, e)"; 
     
     ## offset 
      # Returns a list of offset data for the pentagonal tiles
      # @param ttype           The integer number of the pentagon tiling
      # @param AA, BB, b, c, e Tiling parameters
     ##
     @staticmethod
     def offset(ttype, AA, BB, b, c, e): 
          
          offset_data = []; 
          if ttype == 1: 
               offset_data = [
                    vector([-1 + b * cos(AA) - e* cos(AA), -b * sin(AA) + e * sin(AA)]), 
                    vector([-b * cos(AA) - e * cos(AA) + c * cos(AA + BB), \
                     b * sin(AA) + e * sin(AA) - c * sin(AA + BB)])
               ]; 
          elif ttype == 2: 
               offset_data = [ 
                    vector([b/2 - cos(AA) + 0.5 * (b + 2 * b * cos(AA-BB) - 2 * cos(BB)), 
                     -sin(AA) + b * sin(AA-BB) + sin(BB)]), 
                    vector([b + e - 2 * cos(AA) + (b - e) * cos(AA-BB), 
                     -2 * sin(AA) + (b - e) * sin(AA-BB)])
               ]; 
          elif ttype == 3: 
               offset_data = [
                    vector([1.5, float(sqrt(3) / 2.0)]), 
                    vector([0, float(sqrt(3))]) 
               ]; 
          elif ttype == 4: 
               offset_data = [
                    vector([-1 + b * (cos(AA) - sin(AA)), 1 - b * (cos(AA) + sin(AA))]), 
                    vector([1 - b * (cos(AA) + sin(AA)), 1 - b * (cos(AA) - sin(AA))])
               ]; 
          elif ttype == 5: 
               offset_data = [
                    vector([0.5 * (3 - 3 * b * cos(AA) + float(sqrt(3)) * b * sin(AA)), 
                            0.5 * (-1 * float(sqrt(3)) + float(sqrt(3)) * b * cos(AA) + 3 * b * sin(AA))]), 
                    vector([-float(sqrt(3)) * b * sin(AA), float(sqrt(3)) * (1 - b * cos(AA))])
               ]; 
          elif ttype == 8: 
               offset_data = [ 
                    vector([(12 * cos(AA/4)**2 * (cos(AA/2) + 2 * cos(AA))) / (5 + 4 * cos(AA/2)), 
                            (3 * (4 * sin(AA/2) + 5 * sin(AA) + 2 * sin(3 * AA / 2))) / (5 + 4 * cos(AA/2))]), 
                    vector([(11 + 22 * cos(AA/2) + 11 * cos(AA) - 4 * cos(3 * AA / 2) - 4 * cos(2 * AA)) / (5 + 4 * cos(AA/2)), 
                           (18 * sin(AA/2) + 11 * sin(AA) - 4 * (sin(3 * AA / 2) + sin(2 * AA))) / (5 + 4 * cos(AA/2))])
               ]; 
          elif ttype == 10: 
               offset_data = [ 
                    vector([-3 + 3 * cos(AA) + 6 / (1 + cot(AA/2)) + sin(AA), 
                            (1 + 2 * cos(AA) + 4 * sin(AA)) / (1 + cot(AA/2))]), 
                    vector([(3 - 4 * cos(AA)) / (1 + tan(AA/2)), 
                            -((sin(AA/2) + 2 * sin(3 * AA / 2)) / (cos(AA/2) + sin(AA/2)))])
               ]; 
          elif ttype == 11: 
               offset_data = [
                    vector([(8 * cos(AA) * sin(AA)**3) / (-1 + 2 * cos(AA)), 
                            -((8 * (-1 + cos(AA)) * cos(AA) * sin(AA)**2) / (-1 + 2 * cos(AA)))]), 
                    vector([((3 - 8 * cos(AA) + 4 * cos(2 * AA)) * sin(AA)) / (-1 + 2 * cos(AA)), 
                            (1 + 3 * cos(AA) - 2 * cos(3 * AA)) / (-1 + 2 * cos(AA))])
               ]; 
          elif ttype == 15: 
               offset_data = [
                    vector([3 * (1 + float(sqrt(3))) / 2.0, 0]), 
                    vector([0.0, 1.0])
               ];
          else: 
               print "Unknown tiling type: ", self.ttype; 
               sys.exit(1); 
          ## if 
          return offset_data; 
     
     ## def 
     
     ## motif
      # Returns a list of lists of five-vector-element lists providing motif 
      # data for the pentagonal tiles
      # @param ttype           The integer number of the pentagon tiling
      # @param AA, BB, b, c, e Tiling parameters
     ##
     @staticmethod
     def motif(ttype, AA, BB, b, c, e): 

          motif_data = []; 
          if ttype == 1: 
               motif_data = [
                    [vector([0.5 - b * cos(AA), b * sin(AA)]), 
                     vector([0.5 - b * cos(AA) + c * cos(AA + BB), b * sin(AA) - c * sin(AA + BB)]), 
                     vector([-0.5 - e * cos(AA), e * sin(AA)]), 
                     vector([-0.5, 0.0]), 
                     vector([0.5, 0.0])
                    ], 
                    [vector([-0.5 + b * cos(AA), -b * sin(AA)]), 
                     vector([-0.5 + b * cos(AA) - c * cos(AA + BB), -b * sin(AA) + c * sin(AA + BB)]), 
                     vector([0.5 + e * cos(AA), -e * sin(AA)]), 
                     vector([0.5, 0.0]), 
                     vector([-0.5, 0.0]) 
                    ]
               ]; 
          elif ttype == 2: 
               motif_data = [
                    [vector([0.5 * (b - 2 * cos(BB)), sin(BB)]), 
                     vector([-(b / 2.0) + cos(AA) + e * cos(AA - BB), sin(AA) + e * sin(AA - BB)]), 
                     vector([-(b / 2.0) + cos(AA), sin(AA)]), 
                     vector([-(b / 2.0), 0.0]), 
                     vector([b / 2.0, 0.0])
                    ], 
                    [vector([0.5 * (b - 2 * cos(AA) + 2 * b * cos(AA - BB) - 2 * cos(BB)), 
                             -sin(AA) + b * sin(AA - BB) + sin(BB)]), 
                     vector([b / 2.0 + e, 0.0]), 
                     vector([b / 2.0, 0.0]), 
                     vector([0.5 * (b - 2 * cos(BB)), sin(BB)]), 
                     vector([0.5 * (b + 2 * b * cos(AA - BB) - 2 * cos(BB)), 
                             b * sin(AA - BB) + sin(BB)])
                    ], 
                    [vector([-(b / 2.0) + cos(AA) + e * cos(AA - BB), 
                             sin(AA) + e * sin(AA - BB)]), 
                     vector([0.5 * (b - 2 * cos(BB)), sin(BB)]), 
                     vector([b / 2.0 + e * cos(AA - BB) - cos(BB), 
                             e * sin(AA - BB) + sin(BB)]), 
                     vector([b / 2.0 + cos(AA) + e * cos(AA-BB) - cos(BB), 
                             sin(AA) + e * sin(AA - BB) + sin(BB)]), 
                     vector([-(b / 2.0) + cos(AA) + e * cos(AA - BB) - cos(BB), 
                             sin(AA) + e * sin(AA - BB) + sin(BB)])
                    ], 
                    [vector([-(b / 2.0) + 2 * cos(AA) + (e - b) * cos(AA - BB), 
                             2 * sin(AA) + (e - b) * sin(AA-BB)]), 
                     vector([-(b / 2.0) - e + cos(AA) + e * cos(AA - BB) - cos(BB), 
                             sin(AA) + e * sin(AA - BB) + sin(BB)]), 
                     vector([-(b / 2.0) + cos(AA) + e * cos(AA - BB) - cos(BB), 
                             sin(AA) + e * sin(AA - BB) + sin(BB)]), 
                     vector([-(b / 2.0) + cos(AA) + e * cos(AA - BB), 
                             sin(AA) + e * sin(AA - BB)]), 
                     vector([-(b / 2.0) + cos(AA) + (e - b) * cos(AA - BB), 
                             sin(AA) + (e - b) * sin(AA-BB)]) 
                    ]
               ];
          elif ttype == 3: 
               motif_data = [
                    [vector([0.0, 0.0]), 
                     vector([0.5, float(sqrt(3)) / 2]), 
                     vector([b / 2.0, - 0.5 * float(sqrt(3)) * (b - 2)]), 
                     vector([-0.5, float(sqrt(3)) / 2]), 
                     vector([-b, 0.0])
                    ], 
                    [vector([-1.5, float(sqrt(3)) / 2]), 
                     vector([-1.0, 0.0]), 
                     vector([-b, 0.0]), 
                     vector([-0.5, float(sqrt(3)) / 2]), 
                     vector([0.5 * (b - 3), 0.5 * float(sqrt(3)) * (b + 1)])
                    ], 
                    [vector([0.0, float(sqrt(3))]), 
                     vector([-1.0, float(sqrt(3))]), 
                     vector([0.5 * (b - 3), 0.5 * float(sqrt(3)) * (b + 1)]), 
                     vector([-0.5, float(sqrt(3)) / 2]), 
                     vector([b / 2.0, -0.5 * float(sqrt(3)) * (b - 2)])
                    ]
               ]; 
          elif ttype == 4: 
               motif_data = [ 
                    [vector([0.0, 0.0]), 
                     vector([0.0, 1.0]), 
                     vector([-b * sin(AA), 1 - b * cos(AA)]), 
                     vector([b * (cos(AA) - sin(AA)), 1 - b * (cos(AA) + sin(AA))]), 
                     vector([-1.0, 0.0])
                    ], 
                    [vector([0.0, 0.0]), 
                     vector([-1.0, 0.0]), 
                     vector([b * cos(AA) - 1, -b * sin(AA)]),
                     vector([b * (cos(AA) + sin(AA)) - 1, b * (cos(AA) - sin(AA))]), 
                     vector([0.0, -1.0]) 
                    ], 
                    [vector([0.0, 0.0]), 
                     vector([0.0, -1.0]), 
                     vector([b * sin(AA),b * cos(AA) - 1]), 
                     vector([-b * (cos(AA) - sin(AA)), b * (cos(AA) + sin(AA)) - 1]), 
                     vector([1.0, 0.0]) 
                    ], 
                    [vector([0.0, 0.0]), 
                     vector([1.0, 0.0]), 
                     vector([1 - b * cos(AA), b * sin(AA)]), 
                     vector([1 - b * (cos(AA) + sin(AA)), -b * (cos(AA) - sin(AA))]), 
                     vector([0.0, 1.0])
                    ]               
               ]; 
          elif ttype == 5: 
               motif_data = [ 
                    [vector([0.0, 0.0]), 
                     vector([1.0, 0.0]), 
                     vector([1 - b * cos(AA), b * sin(AA)]), 
                     vector([0.5 * (2 - 3 * b * cos(AA) - float(sqrt(3)) * b * sin(AA)), 
                             -0.5 * b * (float(sqrt(3)) * cos(AA) - 3 * sin(AA))]), 
                     vector([0.5, float(sqrt(3)) / 2.0])
                    ], 
                    [vector([0.0, 0.0]), 
                     vector([0.5, float(sqrt(3)) / 2.0]), 
                     vector([0.5 * (1 - b * (cos(AA) + float(sqrt(3)) * sin(AA))), 
                             0.5 * (float(sqrt(3)) * (1 - b * cos(AA)) + b * sin(AA))]),# 
                     vector([0.5 - float(sqrt(3)) * b * sin(AA), 
                             0.5 * float(sqrt(3)) * (1 - 2 * b * cos(AA))]), 
                     vector([-0.5, float(sqrt(3)) / 2.0]) 
                    ], 
                    [vector([0.0, 0.0]), 
                     vector([-0.5, float(sqrt(3)) / 2.0]), 
                     vector([0.5 * (-1 + b * cos(AA) - float(sqrt(3)) * b * sin(AA)), 
                             0.5 * (float(sqrt(3)) * (1 - b * cos(AA)) - b * sin(AA))]), #
                     vector([0.5 * (-1 + 3 * b * cos(AA) - float(sqrt(3)) * b * sin(AA)), 
                             0.5 * (float(sqrt(3)) - float(sqrt(3)) * b * cos(AA) - 3 * b * sin(AA))]), 
                     vector([-1.0, 0.0]) 
                    ], 
                    [vector([0.0, 0.0]), 
                     vector([-1.0, 0.0]), 
                     vector([-1 + b * cos(AA), -b * sin(AA)]), 
                     vector([0.5 * (-2 + 3 * b * cos(AA) + float(sqrt(3)) * b * sin(AA)), 
                             0.5 * b * (float(sqrt(3)) * cos(AA) - 3 * sin(AA))]), 
                     vector([-0.5, -float(sqrt(3)) / 2.0])
                    ], 
                    [vector([0.0, 0.0]), 
                     vector([-0.5, -float(sqrt(3)) / 2.0]), 
                     vector([0.5 * (-1 + b * cos(AA) + float(sqrt(3)) * b * sin(AA)), 
                             0.5 * (float(sqrt(3)) * (-1 + b * cos(AA)) - b * sin(AA))]), 
                     vector([-0.5 + float(sqrt(3)) * b * sin(AA), 
                             0.5 * float(sqrt(3)) * (-1 + 2 * b * cos(AA))]), 
                     vector([0.5, -float(sqrt(3)) / 2.0]) 
                    ], 
                    [vector([0.0, 0.0]), 
                     vector([0.5, -float(sqrt(3)) / 2.0]), 
                     vector([0.5 * (1 - b * cos(AA) + float(sqrt(3)) * b * sin(AA)), 
                             0.5 * (float(sqrt(3)) * (-1 + b * cos(AA)) + b * sin(AA))]), 
                     vector([0.5 * (1 - 3 * b * cos(AA) + float(sqrt(3)) * b * sin(AA)), 
                             0.5 * (-float(sqrt(3)) + float(sqrt(3)) * b * cos(AA) +3 * b * sin(AA))]), 
                     vector([1.0, 0.0]) 
                    ]
               ]; 
          elif ttype == 8: 
               motif_data = [
                    [vector([-0.5, 0.0]), 
                     vector([0.5, 0.0]), 
                     vector([0.5 - cos(AA), -sin(AA)]), 
                     vector([-0.75 + 9 / (4 * (5 + 4 * cos(AA/2))) - cos(AA), 
                             (-5 * (sin(AA/2) + sin(AA)) - 2 * sin(3 * AA / 2)) / (5 + 4 * cos(AA/2))]), 
                     vector([-0.5 - cos(AA/2), -sin(AA/2)]) 
                    ], 
                    [vector([-((11 + 22 * cos(AA/2) + 12 * cos(AA)) / (10 + 8 * cos(AA/2))), 
                             -((3 * (3 * sin(AA/2) + 2 * sin(AA))) / (5 + 4 * cos(AA/2)))]), 
                     vector([-((11 + 24 * cos(AA/2) + 20 * cos(AA) + 8 * cos(3 * AA / 2)) / (10 + 8 * cos(AA/2))), 
                             -((2 * (5 * (sin(AA/2) + sin(AA)) + 2 * sin(3 * AA / 2))) / (5 + 4 * cos(AA/2)))]), 
                     vector([-((3 + 14 * cos(AA/2) + 20 * cos(AA) + 8 * cos(3 * AA / 2)) / (10 + 8 * cos(AA/2))), 
                             -(((11 + 20 * cos(AA/2) + 8 * cos(AA)) * sin(AA/2)) / (5 + 4 * cos(AA/2)))]), 
                     vector([-((3 + 10 * cos(AA/2) + 10 * cos(AA) + 4 * cos(3 * AA / 2)) / (10 + 8 * cos(AA/2))), 
                             (-5 * (sin(AA/2) + sin(AA)) - 2 * sin(3 * AA / 2)) / (5 + 4 * cos(AA/2))]), 
                     vector([-0.5 - cos(AA/2), -sin(AA/2)]) 
                    ], 
                    [vector([0.5, 0.0]), 
                     vector([-0.5, 0.0]), 
                     vector([-0.5 + cos(AA), sin(AA)]), 
                     vector([0.75 - 9 / (4 * (5 + 4 * cos(AA/2))) + cos(AA), 
                             (5 * (sin(AA/2) + sin(AA)) + 2 * sin(3 * AA / 2)) / (5 + 4 * cos(AA/2))]), 
                     vector([0.5 + cos(AA/2), sin(AA/2)]) 
                    ], 
                    [vector([(11 + 22 * cos(AA/2) + 12 * cos(AA)) / (10 + 8 * cos(AA/2)), 
                             (9 * sin(AA/2) + 6 * sin(AA)) / (5 + 4 * cos(AA/2))]), 
                     vector([(11 + 24 * cos(AA/2) + 20 * cos(AA) + 8 * cos(3 * AA / 2)) / (10 + 8 * cos(AA/2)), 
                             (2 * (5 * (sin(AA/2) + sin(AA)) + 2 * sin(3 * AA / 2))) / (5 + 4 * cos(AA/2))]), 
                     vector([(3 + 14 * cos(AA/2) + 20 * cos(AA) + 8 * cos(3 * AA / 2)) / (10 + 8 * cos(AA/2)), 
                             ((11 + 20 * cos(AA/2) + 8 * cos(AA)) * sin(AA/2)) / (5 + 4 * cos(AA/2))]), 
                     vector([(3 + 10 * cos(AA/2) + 10 * cos(AA) + 4 * cos(3 * AA / 2)) / (10 + 8 * cos(AA/2)), 
                             (5 * (sin(AA/2) + sin(AA)) + 2 * sin(3 * AA / 2)) / (5 + 4 * cos(AA/2))]), 
                     vector([0.5 + cos(AA/2), sin(AA/2)])
                    ], 
                    [vector([-0.5, 0.0]), 
                     vector([-0.5 - cos(AA/2), -sin(AA/2)]), 
                     vector([-0.5 - cos(AA/2) + cos(3 * AA / 2), 2 * cos(AA) * sin(AA/2)]), 
                     vector([(-7 - 6 * cos(AA/2) + 8 * cos(AA) + 10 * cos(3 * AA / 2) + 4 * cos(2 * AA)) / (10 + 8 * cos(AA/2)), 
                            (-sin(AA/2) + 4 * sin(AA) + 5 * sin(3 * AA / 2) + 2 * sin(2 * AA)) / (5 + 4 * cos(AA/2))]), 
                     vector([-0.5 + cos(AA), sin(AA)])
                    ], 
                    [vector([(-11 - 22 * cos(AA/2) - 10 * cos(AA) + 8 * cos(3 * AA / 2) + 8 * cos(2 * AA)) / (10 + 8 * cos(AA/2)), 
                             ((-5 + 8 * cos(AA)) * (sin(AA/2) + sin(AA))) / (5 + 4 * cos(AA/2))]), 
                     vector([-((11 + 22 * cos(AA/2) + 12 * cos(AA)) / (10 + 8 * cos(AA/2))), 
                             -((3 * (3 * sin(AA/2) + 2 * sin(AA))) / (5 + 4 * cos(AA/2)))]), 
                     vector([-0.5 - cos(AA/2), -sin(AA/2)]), 
                     vector([-0.5 - cos(AA/2) + cos(3 * AA / 2), 2 * cos(AA) * sin(AA/2)]), 
                     vector([(-11 - 20 * cos(AA/2) - 2 * cos(AA) + 16 * cos(3 * AA / 2) + 8 * cos(2 * AA)) / (10 + 8 * cos(AA/2)), 
                             (2 * (3 * cos(AA/2) + 8 * cos(AA) + 4 * cos(3 * AA / 2)) * sin(AA/2)) / (5 + 4 * cos(AA/2))])
                    ], 
                    [vector([0.5, 0.0]), 
                     vector([0.5 + cos(AA/2), sin(AA/2)]), 
                     vector([0.5 + cos(AA/2) - cos(3 * AA / 2), -2 * cos(AA) * sin(AA/2)]), 
                     vector([(7 + 6 * cos(AA/2) - 8 * cos(AA) - 10 * cos(3 * AA / 2) - 4 * cos(2 * AA)) / (10 + 8 * cos(AA/2)), 
                             (sin(AA/2) - 4 * sin(AA) - 5 * sin(3 * AA / 2) - 2 * sin(2 * AA))/(5 + 4 * cos(AA/2))]), 
                     vector([0.5 - cos(AA), -sin(AA)])
                    ], 
                    [vector([(11 + 22 * cos(AA/2) + 10 * cos(AA) - 8 * cos(3 * AA / 2) - 8 * cos(2 * AA)) / (10 + 8 * cos(AA/2)), 
                             -(((-5 + 8 * cos(AA)) * (sin(AA/2) + sin(AA))) / (5 + 4 * cos(AA/2)))]), 
                     vector([(11 + 22 * cos(AA/2) + 12 * cos(AA)) / (10 + 8 * cos(AA/2)), 
                             (9 * sin(AA/2) + 6 * sin(AA)) / (5 + 4 * cos(AA/2))]), 
                     vector([0.5 + cos(AA/2), sin(AA/2)]), 
                     vector([0.5 + cos(AA/2) - cos(3 * AA / 2), -2 * cos(AA) * sin(AA/2)]), 
                     vector([(11 + 20 * cos(AA/2) + 2 * cos(AA) - 16 * cos(3 * AA / 2) - 8 * cos(2 * AA)) / (10 + 8 * cos(AA/2)), 
                             (8 * sin(AA/2) + sin(AA) - 4 * (2 * sin(3 * AA / 2) + sin(2 * AA))) / (5 + 4 * cos(AA/2))])
                    ]
               ]; 
          elif ttype == 10: 
               motif_data = [ 
                    [vector([1.0, 0.0]), 
                     vector([0.5 * (-1 + cos(AA) + 3 * sin(AA)), 
                             -((-2 + 2 * cos(AA) + sin(AA)) / (1 + tan(AA/2)))]), 
                     vector([sin(AA) * (-1 + 3 / (1 + tan(AA/2))), 
                             0.5 * (-1-cos(AA) + 3 * sin(AA))]), 
                     vector([0.0, 1.0]), 
                     vector([0.0, 0.0])
                    ], 
                    [vector([0.0, 1.0]), 
                     vector([(-2 + 2 * cos(AA) + sin(AA)) / (1 + tan(AA/2)), 
                             0.5 * (-1 + cos(AA) + 3 * sin(AA))]), 
                     vector([0.5 * (1 + cos(AA)-3 * sin(AA)), 
                             sin(AA) * (-1 + 3 / (1 + tan(AA/2)))]), 
                     vector([-1.0, 0.0]), 
                     vector([0.0, 0.0]) 
                    ], 
                    [vector([-1.0, 0.0]), 
                     vector([0.5 * (1-cos(AA)-3 * sin(AA)), 
                             (-2 + 2 * cos(AA) + sin(AA)) / (1 + tan(AA/2))]), 
                     vector([sin(AA) * (1-3 / (1 + tan(AA/2))), 
                             0.5 * (1 + cos(AA)-3 * sin(AA))]), 
                     vector([0.0, -1.0]), 
                     vector([0.0, 0.0])
                    ], 
                    [vector([0.0, -1.0]), 
                     vector([-((-2 + 2 * cos(AA) + sin(AA)) / (1 + tan(AA/2))), 
                             0.5 * (1-cos(AA)-3 * sin(AA))]), 
                     vector([0.5 * (-1-cos(AA) + 3 * sin(AA)), 
                             sin(AA) * (1-3 / (1 + tan(AA/2)))]), 
                     vector([1.0, 0.0]), 
                     vector([0.0, 0.0]), 
                    ], 
                    [vector([0.5 * (-3 + cos(AA) + 6 / (1 + cot(AA/2)) + 3 * sin(AA)), 
                             -((cos(AA/2) * (-2 + 2 * cos(AA) + sin(AA))) / (cos(AA/2) + sin(AA/2)))]), 
                     vector([0.5 * (-1 + cos(AA) + 3 * sin(AA)), 
                             -((-2 + 2 * cos(AA) + sin(AA)) / (1 + tan(AA/2)))]), 
                     vector([(-1 + cos(AA) + 2 * sin(AA)) / (1 + tan(AA/2)), 
                             0.5 * (-1-cos(AA) + 3 * sin(AA))]), 
                     vector([(cos(AA/2) * (-1 + cos(AA) + 2 * sin(AA))) / (cos(AA/2) + sin(AA/2)), 
                             (cos(AA) + cot(AA/2) + 2 * sin(AA)) / (1 + cot(AA/2))]), 
                     vector([(3 * sin(AA)**2) / (1-cos(AA) + sin(AA)), 
                             (3 * sin(AA))/(1 + cot(AA/2))])
                    ], 
                    [vector([0.5 * (3-cos(AA)-6 / (1 + cot(AA/2))-3 * sin(AA)), 
                             (cos(AA/2) * (-2 + 2 * cos(AA) + sin(AA))) / (cos(AA/2) + sin(AA/2))]), 
                     vector([0.5 * (1-cos(AA)-3 * sin(AA)), 
                             (-2 + 2 * cos(AA) + sin(AA)) / (1 + tan(AA/2))]), 
                     vector([-((-1 + cos(AA) + 2 * sin(AA)) / (1 + tan(AA/2))), 
                             0.5 * (1 + cos(AA)-3 * sin(AA))]), 
                     vector([-((cos(AA/2) * (-1 + cos(AA) + 2 * sin(AA))) / (cos(AA/2) + sin(AA/2))), 
                             -((cos(AA) + cot(AA/2) + 2 * sin(AA)) / (1 + cot(AA/2)))]), 
                     vector([-((3 * sin(AA)**2) / (1-cos(AA) + sin(AA))), 
                             -((3 * sin(AA)) / (1 + cot(AA/2)))])
                    ]
               ]; 
          elif ttype == 11: 
               motif_data = [
                    [vector([0.0, 0.0]), 
                     vector([sin(AA) + (3 * sin(AA))/(-1 + 2 * cos(AA))-2 * sin(2 * AA), 0.0]), 
                     vector([sin(AA)-sin(2 * AA), 
                             cos(AA) * (1 + (4 * sin(AA)**2)/(-1 + 2 * cos(AA)))]), 
                     vector([-sin(2 * AA), 
                             (4 * cos(AA) * sin(AA)**2)/(-1 + 2 * cos(AA))]), 
                     vector([0.0, (-2 * cos(AA) + cos(2 * AA))/(1-2 * cos(AA))])
                    ],
                    [vector([0.0, 0.0]), 
                     vector([sin(AA) + (3 * sin(AA))/(-1 + 2 * cos(AA))-2 * sin(2 * AA), 0.0]), 
                     vector([sin(AA)-sin(2 * AA), 
                             -cos(AA) * (1 + (4 * sin(AA)**2)/(-1 + 2 * cos(AA)))]), 
                     vector([-sin(2 * AA), 
                             -((4 * cos(AA) * sin(AA)**2)/(-1 + 2 * cos(AA)))]), 
                     vector([0.0, -((-2 * cos(AA) + cos(2 * AA))/(1-2 * cos(AA)))])
                    ],
                    [vector([(2-6 * cos(AA) + 3/(-1 + 2 * cos(AA))) * sin(AA), 
                             (-2 * cos(AA)**2 + cos(3 * AA))/(-1 + 2 * cos(AA))]), 
                     vector([(1-2 * cos(AA)) * sin(AA), 
                             (-2 * cos(AA)**2 + cos(3 * AA))/(-1 + 2 * cos(AA))]), 
                     vector([sin(AA) + (3 * sin(AA))/(-1 + 2 * cos(AA))-2 * sin(2 * AA), 
                             -1 + 3/(1-2 * cos(AA)) + 2 * cos(2 * AA)]), 
                     vector([(2-4 * cos(AA) + 3/(-1 + 2 * cos(AA))) * sin(AA), 
                             -1 + 3/(1-2 * cos(AA)) + cos(AA) + 2 * cos(2 * AA)]), 
                     vector([(2-6 * cos(AA) + 3/(-1 + 2 * cos(AA))) * sin(AA), 
                             -1 + 3/(1-2 * cos(AA)) + cos(AA) + cos(2 * AA)])
                    ],  
                    [vector([(2-6 * cos(AA) + 3/(-1 + 2 * cos(AA))) * sin(AA), 
                             (-2 * cos(AA)**2 + cos(3 * AA))/(-1 + 2 * cos(AA))]), 
                     vector([(1-2 * cos(AA)) * sin(AA), 
                             (-2 * cos(AA)**2 + cos(3 * AA))/(-1 + 2 * cos(AA))]), 
                     vector([sin(AA) + (3 * sin(AA))/(-1 + 2 * cos(AA))-2 * sin(2 * AA), 0.0]), 
                     vector([(2-4 * cos(AA) + 3/(-1 + 2 * cos(AA))) * sin(AA), -cos(AA)]), 
                     vector([(2-6 * cos(AA) + 3/(-1 + 2 * cos(AA))) * sin(AA), 
                             -cos(AA) + cos(2 * AA)])
                    ],  
                    [vector([((-2 + 4 * cos(AA)-3 * cos(2 * AA)) * sin(AA))/(-1 + 2 * cos(AA)), 
                             (2 + cos(AA) + 2 * cos(2 * AA)-3 * cos(3 * AA))/(2-4 * cos(AA))]), 
                     vector([-2 * sin(2 * AA) + sin(3 * AA), 
                             (1 + 2 * cos(AA)-3 * cos(3 * AA) + cos(4 * AA))/(1-2 * cos(AA))]), 
                     vector([(2-3/(1-2 * cos(AA))-4 * cos(AA)) * sin(AA), 
                             -2 + 3/(1-2 * cos(AA)) + cos(AA) + 2 * cos(2 * AA)]), 
                     vector([(2-3/(1-2 * cos(AA))-4 * cos(AA)) * sin(AA), 
                             -1 + 3/(1-2 * cos(AA)) + cos(AA) + 2 * cos(2 * AA)]), 
                     vector([sin(AA) + (3 * sin(AA))/(-1 + 2 * cos(AA))-2 * sin(2 * AA), 
                             -1 + 3/(1-2 * cos(AA)) + 2 * cos(2 * AA)])
                    ], 
                    [vector([((-2 + 4 * cos(AA)-3 * cos(2 * AA)) * sin(AA))/(-1 + 2 * cos(AA)), 
                             (2 + cos(AA) + 2 * cos(2 * AA)-3 * cos(3 * AA))/(2-4 * cos(AA))]), 
                     vector([-2 * sin(2 * AA) + sin(3 * AA), 
                             (1 + 2 * cos(AA)-3 * cos(3 * AA) + cos(4 * AA))/(1-2 * cos(AA))]), 
                     vector([-2 * sin(2 * AA) + sin(3 * AA), 
                             (2 * cos(2 * AA)-3 * cos(3 * AA) + cos(4 * AA))/(1-2 * cos(AA))]), 
                     vector([-sin(2 * AA) + sin(3 * AA), 
                             (cos(AA)-4 * cos(3 * AA) * sin(AA/2)**2)/(1-2 * cos(AA))]), 
                     vector([-sin(2 * AA), (4 * cos(AA) * sin(AA)**2)/(1-2 * cos(AA))])
                    ],  
                    [vector([(3 * (sin(AA)-2 * sin(2 * AA) + sin(3 * AA)))/(2-4 * cos(AA)), 
                             (sin(AA) * sin(2 * AA))/(-1 + 2 * cos(AA))]), 
                     vector([(8 * cos(AA) * sin(AA)**3)/(-1 + 2 * cos(AA)), 
                             -3 * cos(AA) + 3/(-1 + 2 * cos(AA))-cos(2 * AA) + cos(3 * AA)]), 
                     vector([-sin(2 * AA), 
                             (1-3 * cos(AA) + cos(3 * AA))/(1-2 * cos(AA))]), 
                     vector([-sin(2 * AA), (4 * cos(AA) * sin(AA)**2)/(-1 + 2 * cos(AA))]), 
                     vector([(1-2 * cos(AA)) * sin(AA), 
                             (1 + cos(2 * AA)-cos(3 * AA))/(-1 + 2 * cos(AA))])
                    ], 
                    [vector([(3 * (sin(AA)-2 * sin(2 * AA) + sin(3 * AA)))/(2-4 * cos(AA)), 
                             (sin(AA) * sin(2 * AA))/(-1 + 2 * cos(AA))]), 
                     vector([(8 * cos(AA) * sin(AA)**3)/(-1 + 2 * cos(AA)), 
                             -3 * cos(AA) + 3/(-1 + 2 * cos(AA))-cos(2 * AA) + cos(3 * AA)]), 
                     vector([(8 * cos(AA) * sin(AA)**3)/(-1 + 2 * cos(AA)), 
                             -cos(AA)-cos(2 * AA) + cos(3 * AA)]), 
                     vector([(sin(AA)-3 * sin(2 * AA) + sin(3 * AA) + sin(4 * AA))/(1-2 * cos(AA)), 
                             -4 * cos(AA) * sin(AA)**2]), 
                     vector([(2 + 3/(-1 + 2 * cos(AA))) * sin(AA)-2 * sin(2 * AA), -cos(AA)])
                    ]
               ];
          elif ttype == 15: 
               motif_data = [
                    [vector([0.125 * (5-5 * float(sqrt(3))), 
                             0.125 * (1+float(sqrt(3)))]), 
                     vector([0.125 * (5-5 * float(sqrt(3))), 
                             0.125 * (5-3 * float(sqrt(3)))]), 
                     vector([0.125 * (1-float(sqrt(3))), 
                             0.125 * (-7+float(sqrt(3)))]), 
                     vector([0.125 * (-1+float(sqrt(3))), 
                             0.125 * (-1-float(sqrt(3)))]), 
                     vector([0.125 * (1-float(sqrt(3))), 
                             0.125 * (1+float(sqrt(3)))])
                    ], 
                    [vector([0.125 * (-5-3 * float(sqrt(3))), 
                             0.125 * (7-float(sqrt(3)))]), 
                     vector([0.125 * (-7-float(sqrt(3))), 
                             0.125 * (1+float(sqrt(3)))]), 
                     vector([0.125 * (5-5 * float(sqrt(3))), 
                             0.125 * (5-3 * float(sqrt(3)))]), 
                     vector([0.125 * (5-5 * float(sqrt(3))), 
                             0.125 * (1+float(sqrt(3)))]), 
                     vector([0.125 * (1-5 * float(sqrt(3))), 
                             0.125 * (5+float(sqrt(3)))]) 
                    ], 
                    [vector([0.125 * (-1-3 * float(sqrt(3))), 
                             0.125 * (11-float(sqrt(3)))]), 
                     vector([0.125 * (5-5 * float(sqrt(3))), 
                             0.125 * (13-3 * float(sqrt(3)))]), 
                     vector([0.125 * (1-float(sqrt(3))), 
                             0.125 * (1+float(sqrt(3)))]), 
                     vector([0.125 * (5-5 * float(sqrt(3))), 
                             0.125 * (1+float(sqrt(3)))]), 
                     vector([0.125 * (1-5 * float(sqrt(3))), 
                             0.125 * (5+float(sqrt(3)))])
                    ], 
                    [vector([0.125 * (-1-3 * float(sqrt(3))), 
                             0.125 * (3-float(sqrt(3)))]), 
                     vector([0.125 * (1-5 * float(sqrt(3))), 
                             0.125 * (-3+float(sqrt(3)))]), 
                     vector([0.125 * (-11-float(sqrt(3))), 
                             0.125 * (1-3 * float(sqrt(3)))]), 
                     vector([0.125 * (-11-float(sqrt(3))), 
                             0.125 * (-3+float(sqrt(3)))]), 
                     vector([0.125 * (-7-float(sqrt(3))), 
                             0.125 * (1+float(sqrt(3)))])
                    ], 
                    [vector([0.125 * (-5-3 * float(sqrt(3))), 
                             0.125 * (7-float(sqrt(3)))]), 
                     vector([0.125 * (-11-float(sqrt(3))), 
                             0.125 * (9-3 * float(sqrt(3)))]), 
                     vector([0.125 * (-7-5 * float(sqrt(3))), 
                             0.125 * (-3+float(sqrt(3)))]), 
                     vector([0.125 * (-11-float(sqrt(3))), 
                             0.125 * (-3+float(sqrt(3)))]), 
                     vector([0.125 * (-7-float(sqrt(3))), 
                             0.125 * (1+float(sqrt(3)))])
                    ], 
                    [vector([0.125 * (-11-float(sqrt(3))), 
                             0.125 * (-3+float(sqrt(3)))]), 
                     vector([0.125 * (-11-float(sqrt(3))), 
                             0.125 * (1-3 * float(sqrt(3)))]), 
                     vector([0.125 * (-7-5 * float(sqrt(3))), 
                             0.125 * (-11+float(sqrt(3)))]), 
                     vector([0.125 * (-5-7 * float(sqrt(3))), 
                             0.125 * (-5-float(sqrt(3)))]), 
                     vector([0.125 * (-7-5 * float(sqrt(3))), 
                             0.125 * (-3+float(sqrt(3)))])
                    ],
                    [vector([0.125 * (-5+5 * float(sqrt(3))), 
                             0.125 * (-1-float(sqrt(3)))]), 
                     vector([0.125 * (-5+5 * float(sqrt(3))), 
                             0.125 * (-5+3 * float(sqrt(3)))]), 
                     vector([0.125 * (-1+float(sqrt(3))), 
                             0.125 * (7-float(sqrt(3)))]), 
                     vector([0.125 * (1-float(sqrt(3))), 
                             0.125 * (1+float(sqrt(3)))]), 
                     vector([0.125 * (-1+float(sqrt(3))), 
                             0.125 * (-1-float(sqrt(3)))]) 
                    ], 
                    [vector([0.125 * (5+3 * float(sqrt(3))), 
                             0.125 * (-7+float(sqrt(3)))]), 
                     vector([0.125 * (7+float(sqrt(3))), 
                             0.125 * (-1-float(sqrt(3)))]), 
                     vector([0.125 * (-5+5 * float(sqrt(3))), 
                             0.125 * (-5+3 * float(sqrt(3)))]), 
                     vector([0.125 * (-5+5 * float(sqrt(3))), 
                             0.125 * (-1-float(sqrt(3)))]), 
                     vector([0.125 * (-1+5 * float(sqrt(3))), 
                             0.125 * (-5-float(sqrt(3)))])
                    ],
                    [vector([0.125 * (1+3 * float(sqrt(3))), 
                             0.125 * (-11+float(sqrt(3)))]), 
                     vector([0.125 * (-5+5 * float(sqrt(3))), 
                             0.125 * (-13+3 * float(sqrt(3)))]), 
                     vector([0.125 * (-1+float(sqrt(3))), 
                             0.125 * (-1-float(sqrt(3)))]), 
                     vector([0.125 * (-5+5 * float(sqrt(3))), 
                             0.125 * (-1-float(sqrt(3)))]), 
                     vector([0.125 * (-1+5 * float(sqrt(3))), 
                             0.125 * (-5-float(sqrt(3)))])
                    ], 
                    [vector([0.125 * (1+3 * float(sqrt(3))), 
                             0.125 * (-3+float(sqrt(3)))]), 
                     vector([0.125 * (-1+5 * float(sqrt(3))), 
                             0.125 * (3-float(sqrt(3)))]), 
                     vector([0.125 * (11+float(sqrt(3))), 
                             0.125 * (-1+3 * float(sqrt(3)))]), 
                     vector([0.125 * (11+float(sqrt(3))), 
                             0.125 * (3-float(sqrt(3)))]), 
                     vector([0.125 * (7+float(sqrt(3))), 
                             0.125 * (-1-float(sqrt(3)))])
                    ],
                    [vector([0.125 * (5+3 * float(sqrt(3))), 
                             0.125 * (-7+float(sqrt(3)))]), 
                     vector([0.125 * (11+float(sqrt(3))), 
                             0.125 * (-9+3 * float(sqrt(3)))]), 
                     vector([0.125 * (7+5 * float(sqrt(3))), 
                             0.125 * (3-float(sqrt(3)))]), 
                     vector([0.125 * (11+float(sqrt(3))), 
                             0.125 * (3-float(sqrt(3)))]), 
                     vector([0.125 * (7+float(sqrt(3))), 
                             0.125 * (-1-float(sqrt(3)))])
                    ],
                    [vector([0.125 * (11+float(sqrt(3))), 
                             0.125 * (3-float(sqrt(3)))]), 
                     vector([0.125 * (11+float(sqrt(3))), 
                             0.125 * (-1+3 * float(sqrt(3)))]), 
                     vector([0.125 * (7+5 * float(sqrt(3))), 
                             0.125 * (11-float(sqrt(3)))]), 
                     vector([0.125 * (5+7 * float(sqrt(3))), 
                             0.125 * (5+float(sqrt(3)))]), 
                     vector([0.125 * (7+5 * float(sqrt(3))), 
                             0.125 * (3-float(sqrt(3)))])
                    ]
               ];
          else: 
               print "Unknown tiling type: ", self.ttype; 
               sys.exit(1); 
          ## if 
          return motif_data; 

     ## def      
     
     ## coordwise_add
      # Defines coordinatewise addition operations on vectors of the same 
      # dimension in place of Python's usual list addition operations
      # len(v1) == len(v2)
      # @param v1 The first vector addend 
      # @param v2 The second vector addend 
      # @return   A vector with coordinates that are the sum of the two 
      #           input vectors
     ##
     @staticmethod
     def coordwise_add(v1, v2): 
          
          if len(v1) != len(v2): 
               print "vector lengths unequal (v1, v2) = (", len(v1), ", ", len(v2), ")"; 
               sys.exit(1); 
          ## if 
          
          rvec = []; 
          for idx in range(0, len(v1)): 
               added_element = v1[idx] + v2[idx]; 
               rvec.append(added_element); 
          ## for 
          return rvec; 
          
     ## def 
     
     ## get_tiles
      # Gets the pentagonal tiles after N steps of iteration (same-sized 
      # tiles expanded over an increasingly larger portion of the plane)
      # @return A list of tiles in the computed partial tiling
     ##
     def get_tiles(self): 
          
          ## assuming that N should correspond to v1 = v2: 
          v1, v2 = self.N, self.N
          AA, BB, b, c, e = self.AA, self.BB, self.b, self.c, self.e; 
          pentset = Pentagon_Tiling.motif(self.ttype, AA, BB, b, c, e); 
          offsets = Pentagon_Tiling.offset(self.ttype, AA, BB, b, c, e); 
          offsetxy = lambda x, y: vector([
                          x * offsets[0][0] + y * offsets[1][0], 
                          x * offsets[0][1] + y * offsets[1][1]
                     ]); 
                     
          tiles = []; 
          for x in range(-v1, v1 + 1): 
               for y in range(-v2, v2 + 1): 
               
                    for i in range(0, len(pentset)): 
                         
                         coords5 = []; 
                         for c2 in range(0, 5): 
                              coords5.append(offsetxy(x, y)); 
                         ## for 
                         tile = Pentagon_Tiling.coordwise_add(pentset[i], coords5); 
                         tiles.append(tile); 
                    
                    ## for i 
               
               ## for y
          ## for x
          return tiles; 

     ## def 

## class 

