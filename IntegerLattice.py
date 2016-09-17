#### IntegerLattice.py 
#### Defines the integer lattice (in Z^2) to test points within some radius 
#### R depending on the step size N
#### Author: Maxie D. Schmidt
#### Created: 2016.03.24

## $ sage -python tiling_pc_plots.py -t IntegerLattice -g -n 1

from sage.all import *
from Tiling import Tiling, edist

## 
 # Python constant providing one setting of our large radius R used with the 
 # statistical plot routines over the integer lattice implemented below
##
LARGE_RADIUSR = 350;

## IntegerLattice_Tiling
 # A Tiling subclass implementing the integer lattice in the first quadrant 
 # with points satisfying 1 <= y < x <250
##
class IntegerLattice_Tiling(Tiling):

     ## __init__
      # Initialization function for the IntegerLattice_Tiling class 
      # @param num_steps_N     The number of substitution steps in the tiling
      # @param tiling_name_str Optional tiling name string 
      #                        (defaults to "IntegerLattice")
     ##
     def __init__(self, num_steps_N, tiling_name_str = "IntegerLattice"): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
          self.R = LARGE_RADIUSR + num_steps_N; 
     ## def
     
     ## desc 
      # Returns a description of the tiling
     ##
     def desc(self): 
          return "Integer lattice in the first quadrant (for comparison)"; 
     ## def
     
     ## generate_integer_lattice
      # Computes a list of integer lattice points in the first quadrant 
      # within some square with large side length R
      # @param radiusR The parameter defining what large radius R of lattice 
      #                points to compute
     ##
     def generate_integer_lattice(self, radiusR): 
     
          ilattice = [];
          for x in range(0, radiusR): 
               for y in range(0, radiusR): 
                    ilattice.append(vector([x, y]));
               ## for 
          ## for 
          return ilattice;
     
     ## def 
     
     ## get_tiles
      # Gets the single-point IntegerLattic tiles
      # @return A list of (semi-forced) tiles representing the lattice points
     ##
     def get_tiles(self): 
          
          lattice = self.generate_integer_lattice(self.R); 
          lattice_points = [];
          for (idx, lp) in enumerate(lattice): 
               
               #if edist(vector([0, 0]), lp) < self.R: 
               #     lattice_points.append([lp]); 
               ## if 
               x, y = lp[0], lp[1];
               if 0 < y and y < x and x < LARGE_RADIUSR:
                    lattice_points.append([lp]); 
               ## if 
          
          ## for 
          return lattice_points; 
          
     ## def

## class

