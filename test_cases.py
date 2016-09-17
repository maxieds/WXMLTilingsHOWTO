#### test_cases.py 
#### Runs unit tests to test the tiling routines
#### Author: Maxie D. Schmidt
#### Created: 2016.04.01

import unittest
from Tiling import *
from ConfigParser import ConfigParser

## TestTilingMethods
 # A class containing the unit tests for the program
##
class TestTilingMethods(unittest.TestCase):

     ## test_XY
      # Tests whether the Tiling functions, X and Y, work correctly
     ##
     def test_XY(self): 
          self.assertEqual(X(vector([1, 2])), 1);
          self.assertEqual(Y(vector([1, 2])), 2);
          self.assertNotEqual(X(vector([1, 2])), Y(vector([1, 2])));
     ## def

     ## test_edist
      # Tests whether the Tiling edist function works as expected
     ##
     def test_edist(self):
          v1, v2, v3, v4 = vector([0, 2]), vector([0, 0]), vector([1, 0]), vector([2, 0]);
          self.assertEqual(edist(v1, v2), 2.0);
          self.assertEqual(edist(v3, v4), 1.0);
          self.assertEqual(edist(v1, v2, sqpow = 1.0), 4.0);
          self.assertEqual(edist(v3, v4, sqpow = 1.0), 1.0);
     ## def

     ## test_sort_points_complex
      # Tests the Tiling.sort_points_complex function
     ##
     def test_sort_points_complex(self): 
          a1 = [vector([0, 0]), vector([0, 1]), vector([0, 0]), vector([0, 1]), 
                vector([2, 2]), vector([3, 1]), vector([3, 0]), vector([2, 2])];
          expected = [vector([0, 0]), vector([0, 0]), vector([0, 1]), 
                      vector([0, 1]), vector([2, 2]), vector([2, 2]), 
                      vector([3, 0]), vector([3, 1])];
          self.assertEqual(sort_points_complex(a1), expected); 
     ## def
     
     ## test_sort_points_1D
      # Tests the Tiling.sort_points_1D function
     ##
     def test_sort_points_1D(self):
          a1, a2, a3 = [-1, 0, 1, 2, 3], [1, 0], [1, 0, 1.5, 0.5];
          a4, a5 = [1, 4, 5, 2, 8, 7, 9, 3, 6, 2.5, 3.5], [2, 1, 3];
          self.assertEqual(sort_points_1D(a1), a1);
          self.assertEqual(sort_points_1D(a2), [0, 1]);
          self.assertEqual(sort_points_1D(a3), [0, 0.5, 1, 1.5]);
          self.assertEqual(sort_points_1D(a4), [1, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9]);
          self.assertEqual(sort_points_1D(a5), [1, 2, 3]);
     ## def
     
     ## test_unique_points
      # Tests the Tiling.unique_points function
     ##
     def test_unique_points(self):
          a1 = [vector([0, 0]), vector([0, 1]), vector([0, 0]), vector([0, 1]), 
                vector([2, 2]), vector([3, 1]), vector([3, 0]), vector([2, 2])];
          expected = [vector([0, 0]), vector([0, 1]), vector([2, 2]), 
                      vector([3, 0]), vector([3, 1])];
          self.assertEqual(unique_points(a1, True), expected); 
          self.assertEqual(unique_points(a1, False), a1); 
          
          a2, a3, a4, a5 = [vector([0, 0]), vector([0, 1])], \
                           [vector([0, 1]), vector([0, 0])], \
                           [vector([0, 1]), vector([0, 1])], \
                           [vector([0, 1])];
          self.assertEqual(unique_points(a2), [vector([0, 0]), vector([0, 1])]);
          self.assertEqual(unique_points(a2), unique_points(a3));
          self.assertEqual(unique_points(a4), [vector([0, 1])]);
          self.assertEqual(unique_points(a4), unique_points(a5));
     ## def
     
     ## test_unique_points_1D
      # Tests the Tiling.unique_points_1D function
     ##
     def test_unique_points_1D(self):
          a1, a2 = [1, 1, 2, 2, 3, 3, 4.0, 4.0, 4.0], [2, 1, 3, 2, 3, 1, 5, 5, 5, 4, 4];
          self.assertEqual(unique_points_1D(a1, True), [1, 2, 3, 4.0]);
          self.assertEqual(unique_points_1D(a1, False), [1, 2, 3, 4.0]);
          self.assertEqual(unique_points_1D(a2, True), [1, 2, 3, 4, 5]);
     ## def
     
     ## test_tiling_to_points
      # Tests the Tiling.tiling_to_points function
     ##
     def test_tiling_to_points(self):
          tiles = [ [vector([0, 0])], 
                    [vector([1, 0]), vector([0, 0]), vector([2, 1])], 
                    [vector([2, 1]), vector([3, 1])], 
                    [vector([3, 0]), vector([0, 0]), vector([1, 2])]
                  ];
          expected = [vector([0, 0]), vector([1, 0]), vector([1, 2]), 
                      vector([2, 1]), vector([3, 0]), vector([3, 1])];
          self.assertEqual(Tiling.tiling_to_points(tiles, True), expected); 
     ## def
     
     ## test_config_parser
      # Tests that the parsing functions are working correctly in the 
      # ConfigParser class
     ##
     def test_config_parser(self): 
     
          cp = ConfigParser("plots-test.conf"); 
          r11, r12 = cp.get_plot_range("GoldenTriangleTest", "pc-edist"); 
          r21, r22 = cp.get_plot_range("GoldenTriangleTest", "pc-edistsq"); 
          r31, r32 = cp.get_plot_range("GoldenTriangleTest", "angles"); 
          r41, r42 = cp.get_plot_range("GoldenTriangleTest", "anglegaps"); 
          r51, r52 = cp.get_plot_range("GoldenTriangleTest", "slopes"); 
          r61, r62 = cp.get_plot_range("GoldenTriangleTest", "slopegaps"); 
          test_arr = [r11, r12, r21, r22, r31, r32, r41, r42, r51, r52, r61, r62];
          expected = [-1.5, -0.05, 2.5, 3, 4, 5.3, 6, 7, 8.1, -9, 10.0, 111];
          self.assertEqual(test_arr, expected); 
     
     ## def

## __main__
 # Main runner code to run all of the unit tests
##
if __name__ == '__main__':
    unittest.main()

