#### Tiling.py 
#### Defines a base class for generating arbitrary tilings of the plane 
#### Author: Maxie D. Schmidt
#### Created: 2016.02.20 

import numpy as np
import pprint 
from math import sin, cos

from sage.all import *
from AffineTransformOp import AffineTransformOp

__major_version__ = "0.0";
__release__ = "1"; 
__version__ = "%s.%s" % (__major_version__, __release__); 

NUMCPUS = 8

## pifp
 # A python float of the PI constant
##
pifp = float(pi);

## X, Y
 # Returns the respective x or y component of an input vector
 # @param input_point A vector
 # @return            The X (Y) component of the vector
##
def X(input_point): return input_point[0] if input_point != None else None; 
def Y(input_point): return input_point[1] if input_point != None else None; 

def V(x, y): return vector([x, y])
def midpoint(A, B): return (A + B) / 2.0
def midpoint2(t, A, B): return (1 - float(t)) * A + float(t) * B

def RotationMatrix(theta): matrix([[cos(theta), -1 * sin(theta)], \
                                   [sin(theta), cos(theta)]])

def get_solutionsXY(solns):
     if solns == None: 
          return []
     XYsol_func = lambda i: [real(n(solns[i][0].rhs())), real(n(solns[i][1].rhs()))]
     XYsols = map(XYsol_func, range(0, len(solns)))
     return XYsols
## def

## solve_system
@parallel(NUMCPUS)
def solve_system(Axy, RA, Bxy, RB, cond_func = lambda x, y: True):
     [Ax, Ay], [Bx, By] = Axy, Bxy
     nfunc = lambda x: Rational(x)
     [Ax, Ay, Bx, By, RA, RB] = map(nfunc, [Ax, Ay, Bx, By, RA, RB]) # inexact reals throw errors ... 
     Mx, My = var('Mx My')
     eqn1 = (Ax - Mx) ** 2 + (Ay - My) ** 2 == RA ** 2
     eqn2 = (Bx - Mx) ** 2 + (By - My) ** 2 == RB ** 2
     #print "solve_system: ", eqn1, eqn2
     solns = solve([eqn1, eqn2], Mx, My)
     solns = get_solutionsXY(solns)
     #print "solve_system: ", solns, "\n"
     for [x, y] in solns:
          if cond_func(x, y):
               return [x, y]
          ##
     ##
     return None
## def

## edist
 # Computes the Euclidean distance between two points
 # @param p0    The first 2D point
 # @param p1    The second 2D point
 # @param sqpow The optional power of the distance function 
 #              (defaults to the normal sqpow = 1/2)
 # @return      The (power modified) Euclidean distance between the points
##
def edist(p0, p1, sqpow = 0.5): 
     (x1, y1, x2, y2) = (p0[0], p0[1], p1[0], p1[1]); 
     return ( ((x1 - x2) ** 2) + ((y1 - y2) ** 2) ) ** sqpow; 
##def 

## sort_points_complex
 # Sorts a list of 2D points, or tuples, using the numpy sort_complex routine
 # @param points_list A list of 2D points
 # @return            A sorted list containing the original points 
 #                    sorted first with respect to the first coordinates, then 
 #                    with respect to the second
##
def sort_points_complex(points_list):

     complex_points = [];
     for p in points_list: 
          x, y = p[0], p[1]; 
          cp = np.complex(x, y); 
          complex_points.append(cp); 
     ## for 
     
     complex_points = list(np.sort_complex(complex_points)); 
     
     points_list = [];
     for cp in complex_points: 
          re, im = real_part(cp), imag_part(cp); 
          points_list.append(vector([re, im])); 
     ## for 
     return points_list; 

## def

## sort_points_1D
 # Sorts a list of one-dimensional (i.e., no tuples) elements
 # @param points_list     A list of 1D elements to be sorted
 # @param sort_by_ycoords Always ignored
 # @return                A sorted list of the elements
##
def sort_points_1D(points_list, sort_by_ycoords = False): 
     return list(np.sort(points_list)); 
## def 

## unique_points
 # Computes a list of distinct tuples
 # @param points_list  A list of pairs
 # @param perform_sort Indicates whether to sort the list of points before the 
 #                     search for distinct pairs 
 #                     (note the list must be pre-sorted for this function 
 #                      to correctly determine the unique points in the list)
 # @return             A list of the distinct tuples in the list 
##
def unique_points(points_list, perform_sort = True): 

     if perform_sort == True: 
          points_list = sort_points_complex(points_list); 
     ## if 

     (last_xc, last_yc) = points_list[0]; 
     uidx = 1; 
     while uidx < len(points_list): 
          (px, py) = points_list[ uidx ]; 
          if last_xc != px or last_yc != py: 
               (last_xc, last_yc) = (px, py); 
               uidx += 1; 
          else: 
               points_list.pop(uidx); 
          ## if 
     ## while 
     
     return points_list; 

## def 

## unique_points_1D
 # Determines the unique 1D elements contained in the list 
 # @param points_list  A list of 1D (i.e., no tuples) elements
 # @param perform_sort Indicates whether to sort the list of points before the 
 #                     search for distinct elements
 #                     (note the list must be pre-sorted for this function 
 #                      to correctly determine the unique points in the list)
 # @return             A list of the distinct elements in the list 
##
def unique_points_1D(points_list, perform_sort = True): 

     if perform_sort == True: 
          points_list = sort_points_1D(points_list); 
     ## if 

     last_point = points_list[0]; 
     uidx = 1; 
     while uidx < len(points_list): 
          point = points_list[ uidx ]; 
          if last_point != point: 
               last_point = point; 
               uidx += 1; 
          else: 
               points_list.pop(uidx); 
          ## if 
     ## while 
     
     return points_list; 

## def

## Tiling
 # A super class intended to generate derived individual tiling classes 
 # implemented in the program
##
class Tiling(object): 
     
     ## __init__
      # The initialization function for the Tiling class
      # @param num_steps_N     Parameter number of substitution or replacement 
      #                        steps used in generating the sub-tiling
      # @param tiling_name_str A unique string identifier for the tiling
     ##
     def __init__(self, num_steps_N, tiling_name_str): 
          self.num_steps = num_steps_N; 
          self.tiling_name = tiling_name_str; 
     ## def 

     ## N
      # Provides access to the num_steps property of the tiling
     ##
     @property
     def N(self): 
          return copy(self.num_steps); 

     ## name
      # Provides access to the tiling_name property of the tiling
     ##
     @property
     def name(self): 
          return copy(self.tiling_name); 
     
     ## desc 
      # Returns a string description of the tiling
      # (intended to be overridden by the sub-classes)
     ##
     def desc(self): 
          return "<Tiling Description>"; 

     ## get_initial_tile
      # Returns the initial tile before performing N stages of the 
      # substitution routines 
      # (intended to be overridden by the sub-classes)
     ##
     def get_initial_tile(self): 
          return []; 

     ## get_tiles
      # Computes the polygon tiles (list of list of 2D vectors) of the 
      # tiling after N steps
      # (intended to be overridden by the sub-classes)
     ##
     def get_tiles(self): 
          return []; 
     
     ## get_tile_color
      # Returns the color of the tile polygon
      # @param tile Always ignored (could be re-written to use the tile's shape)
     ##
     def get_tile_color(self, tile): 
          return 'lightblue'; 
     
     ## get_tile_edge_color
      # Returns the border color between tiles in the images of the tiling
     ##
     def get_tile_edge_color(self): 
          return 'darkgray'; 

     ## get_tiling_image
      # Shows an image of the tiling specified by a list of polygonal tiles
      # @param tiles A list of polygonal tiles (list of 2D vectors)
      # @return      An image of the tiling
      # @see         Tiling.get_tile_color
      # @see         Tiling.get_tile_edge_color
     ##
     def get_tiling_image(self, tiles): 
          
          tile_graph = Graphics(); 
          edge_color = self.get_tile_edge_color(); 
          for (idx, tile) in enumerate(tiles): 
               tile_color = self.get_tile_color(tile); 
               tile_graph += polygon(tile, color = tile_color, edgecolor = edge_color); 
          ## for 
          
          ## plot tiling points in addition to the polygons corresponding to each tile:
          for (idx, tile) in enumerate(tiles): 
               for (idx2, tp) in enumerate(tile): 
                    tile_graph += point(tp, color = 'darkblue');
               ## for 
          ## for 
          
          tile_graph.show(); 
          return tile_graph; 
     
     ## def 
     
     ## transform_points
      # Applies an affine transformation to a list of points
      # @param points_list A list of points
      # @param op          An AffineTransformOp object representing the 
      #                    transformation
      # @return            A list of transformed points
     ##
     @staticmethod 
     def transform_points(points_list, op): 
          tfunc = lambda pt: op.apply_to_point(pt); 
          next_points_list = map(tfunc, points_list); 
          return next_points_list; 
     ## def 

     ## transform_full_points_list
      # Transforms all points in a list of lists of points
      # @param full_points_list A list of lists of 2D vectors
      # @param op               An AffineTransformOp object
      # @return                 A list of lists of transformed points
     ##
     @staticmethod
     def transform_full_points_list(full_points_list, op): 
          tfunc_helper = lambda pt: Tiling.transform_points(pt, op); 
          next_full_points_list = map(tfunc_helper, full_points_list); 
          return next_full_points_list; 
     ## def 
     
     ## tiling_to_points
      # Extracts the individual points from a list of polygonal tiles
      # @param tiles 
      # @param get_unique An optional parameter for whether to compute a list 
      #                   of only the distinct points in the tiling 
      #                   (i.e., since the tiles may contain overlapping points)
      # @return           A list of 2D vectors corresponding to the tiling 
      #                   vertices in the tiles
     ##
     @staticmethod 
     def tiling_to_points(tiles, get_unique = True): 
          tiling_points = []; 
          for (idx, tile) in enumerate(tiles): 
               tiling_points.extend(tile); 
          ## for 
          if get_unique: 
               tiling_points = unique_points(tiling_points, perform_sort = True); 
          ## if 
          return tiling_points; 
     ## def 
     
     ## compute_pc_edists
      # Computes the pair correlation data points, or a list of the O(n^2) 
      # Euclidean distances between distinct points in the tiling
      # @param tiling_points A list of 2D tiling point vectors
      # @param edist_squared An optional parameter denoting whether to square 
      #                      the returned distances
      # @param sort_edists   An optional parameter specifying whether to 
      #                      sort the computed list before returning it
      # @return              A list of the pair correlation distance data
     ##
     @staticmethod 
     @parallel(NUMCPUS)
     def compute_pc_edists(tiling_points, edist_squared = False, sort_edists = False): 
          
          edist_pow = 0.5; 
          if edist_squared: 
               edist_pow = 1.0; 
          ## if 
          
          edists = []; 
          for pt1 in tiling_points: 
               for pt2 in tiling_points: 
                    next_edist = edist(pt1, pt2, edist_pow); 
                    if next_edist != 0.0:
                         edists.append(next_edist); 
               ## for 
          ## for 
          
          if sort_edists: 
               edists = sort_points_1D(edists); 
          ## if 
          
          return edists; 
     
     ## def 
     
     ## compute_sorted_angles
      # Computes a list of sorted angles, arctan(y/x) for each point (x, y), 
      # of each point in the tiling
      # @param tiling_points A list of 2D vectors representing the tiling
      # @return              A list of angles of the tiling points 
     ##
     @staticmethod
     @parallel(NUMCPUS)
     def compute_sorted_angles(tiling_points): 
     
          angles = []; 
          for xyv in tiling_points: 
               x, y = xyv[0], xyv[1];
               angle = math.atan2(y, x) / (2 * pifp); 
               angles.append(angle); 
          ## for 
          angles = unique_points_1D(angles, perform_sort = True); 
          return angles; 
     
     ## def 
     
     ## compute_angle_gaps
      # Computes the gaps between the sorted angles of a list of tiling points
      # @param tiling_points A list of 2D vectors representing tiling points
      # @return              The angle gap distribution data of the differences 
      #                      between neighboring points in the sorted angle list
     ##
     @staticmethod 
     @parallel(NUMCPUS)
     def compute_angle_gaps(tiling_points): 
          
          angles = Tiling.compute_sorted_angles(tiling_points); 
          #normalize_factor = len(angles); 
          normalize_factor = 1.0; 
          #normalize_factor = 1.0 / float(len(angles));
          angle_gaps = []; 
          for i in range(1, len(angles)): 
               gap = (angles[i] - angles[i-1]) / normalize_factor; 
               angle_gaps.append(gap); 
          ## for 
          return angle_gaps;
     
     ## def 
     
     ## compute_sorted_slopes
      # Computes a sorted list of slopes (y/x for each point (x, y)) in a 
      # list of tiling points 
      # @param tiling_points A list of 2D vectors
      # @return              A sorted list of tiling point slopes
     ##
     @staticmethod
     @parallel(NUMCPUS)
     def compute_sorted_slopes(tiling_points): 
     
          slopes = []; 
          for xyv in tiling_points: 
               x, y = xyv[0], xyv[1];
               slope = y / float(x) if x != 0 else 0.0;
               slopes.append(slope); 
          ## for 
          slopes = unique_points_1D(slopes, perform_sort = True); 
          return slopes; 
     
     ## def 
     
     ## compute_slope_gaps
      # Computes the gaps between the sorted slopes of a list of tiling points
      # @param tiling_points A list of 2D vectors representing tiling points
      # @return              The slope gap distribution data of the differences 
      #                      between neighboring points in the sorted slope list
     ##
     @staticmethod 
     @parallel(NUMCPUS)
     def compute_slope_gaps(tiling_points): 
          
          slopes = Tiling.compute_sorted_slopes(tiling_points); 
          normalize_factor = 1.0; 
          #normalize_factor = 1 / (250.0 ** 2); 
          #normalize_factor = 1 / float(len(tiling_points))
          slope_gaps = []; 
          for i in range(1, len(slopes)): 
               gap = (slopes[i] - slopes[i-1]) / normalize_factor; 
               slope_gaps.append(gap); 
          ## for 
          return slope_gaps;
     
     ## def 
     
## class 

