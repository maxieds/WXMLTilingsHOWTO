#### tiling_pc_plots.py 
#### Program to generate pair correlation histogram plots for multiple tilings 
#### Author: Maxie D. Schmidt
#### Created: 2016.02.20 

import sys
import time
import numpy as np
import pprint 

from optparse import OptionParser, SUPPRESS_HELP, make_option
from sage.all import *

from Tiling import Tiling
from ConfigParser import ConfigParser

from AmmannChair import AmmannChair_Tiling
from AmmannChair2 import AmmannChair2_Tiling
from GoldenTriangle import GoldenTriangle_Tiling
from Penrose import Penrose_Tiling
from Sphinx import Sphinx_Tiling
from Pinwheel import Pinwheel_Tiling
from Squares import Square_Tiling
from Triangles import Triangle_Tiling
from Domino import Domino_Tiling
from Pentagons import Pentagon_Tiling
from SaddleConnectionGoldenL import SaddleConnectionGoldenL
from AmmannOctagon import Ammann_Tiling, RHOMB_TILE, SQUARE_TILE, TRIANGLE_TILE
from IntegerLattice import IntegerLattice_Tiling, LARGE_RADIUSR
from Chair3 import Chair3_Tiling
from MiniTangram import MiniTangram_Tiling
from Armchair import Armchair_Tiling
from Tritriangle import TriTriangle_Tiling
from Equithirds import ETTriangle_Tiling
from SDHouse import SDHouse_Tiling
from Pentomino import Pentomino_Tiling
from Cesi import Cesi_Tiling
from SquareTrianglePinwheel import STPinwheel_Tiling
from GoldenRhomboidTriangle import GRTriangle_Tiling
from Domino9Tile import Domino9Tile_Tiling
from Trihex import Trihex_Tiling
from T2000Triangle import T2000Triangle_Tiling
from AmmannA4 import AmmannA4_Tiling
from PenroseKD import PenroseKD_Tiling
from DiamondTriangle import DiamondTriangle_Tiling
from TetrisTiling import Tetris_Tiling
from Danzer7Fold import Danzer7Fold_Tiling

__major_version__ = "2.0";
__release__ = "3"; 
__version__ = "%s.%s" % (__major_version__, __release__); 

##
 # Define command-line options to the program: 
## 
argspec_option_list = [ 

     make_option("-n", "--num-steps", 
                 action = "store", metavar = "NUM-STEPS", 
                 dest = "num_steps", default = 1, 
                 help = "Number of deflations to perform"), 
     make_option("-q", "--edist-squared", 
                 action = "store_true", metavar = "EDIST-SQUARED", 
                 dest = "use_edist_squared", default = False, 
                 help = "Compute pc histograms of the Euclidean distances squared"), 
     make_option("-t", "--tiling", metavar = "TILING-ID", 
                 dest = "tiling_id", default = "AmmannChair2", 
                 help = "Specify the tiling, i.e., AmmannChair, AmmannChair2"), 
     make_option("-s", "--save-tiling-image", 
                 action = "store_true", metavar = "SAVE-TILING-IMAGE", 
                 dest = "save_image", default = True, 
                 help = "Save a copy of the tiling image to output"), 
     make_option("-b", "--num-bins", metavar = "NUM-HIST-BINS", 
                 dest = "num_bins", default = 50, 
                 help = "Number of distinct equi-sized bins to use in the histograms"), 
     make_option("-c", "--config-file", metavar = "CONFIG-FILE", 
                 dest = "conf_file_path", default = "plots.conf", 
                 help = "Path to the config file for the plot ranges"), 
     make_option("-d", "--compute-angle-gaps", 
                 action = "store_true", metavar = "COMPUTE-ANGLE-GAPS", 
                 dest = "use_angle_gaps", default = False, 
                 help = "Compute histograms of the tiling point *angle gaps* (Defaults to pc)"), 
     make_option("-a", "--compute-angles", 
                 action = "store_true", metavar = "COMPUTE-ANGLES", 
                 dest = "use_angles", default = False, 
                 help = "Compute histograms of the tiling point *angles* (Defaults to pc)"), 
     make_option("-l", "--compute-slopes", 
                 action = "store_true", metavar = "COMPUTE-SLOPES", 
                 dest = "use_slopes", default = False, 
                 help = "Compute histograms of the tiling point *slopes* (Defaults to pc)"), 
     make_option("-g", "--compute-slope-gaps", 
                 action = "store_true", metavar = "COMPUTE-SLOPE-GAPS", 
                 dest = "use_slope_gaps", default = False, 
                 help = "Compute histograms of the tiling point *slope gaps* (Defaults to pc)"), 
     make_option("-v", "--verbose", 
                 action = "store_true", 
                 dest = "verbose", 
                 help = SUPPRESS_HELP), 
                 
]; 

argspec_usage = "%prog [-v] [-h] [--version] [-s] [-q] [-d] [-n NUM-STEPS] [-t TSPEC] [-b NUM-BINS]"; 
argspec_version = "%prog 1.0" 

#num_bins_arr = [10, 15, 25, 35, 50, 75, 85, 100, 125, 150, 175, 200, 250, 500, 750, 1000, 2000, 5000, 7500, 10000];
num_bins_arr = [100, 150, 200, 250, 750, 1000, 5000, 10000];
## __main__
 # The main runner code when the program is called from the commandline. 
 # The code parses the commandline arguments (and the config file), 
 # computes data depending on the plot type, and then generates and saves 
 # images for the resulting histogram plot.
##
if __name__ == "__main__":
         
     pp = pprint.PrettyPrinter(indent = 4, width = 16, depth = 4); 
     
     opt_parser = OptionParser(usage = argspec_usage, 
                               version = argspec_version, 
                               option_list = argspec_option_list); 
     (cmdline_opts, cmdline_args) = opt_parser.parse_args(sys.argv); 
     
     num_steps = int(eval(cmdline_opts.num_steps)); 
     tiling_type = str(cmdline_opts.tiling_id); 
     save_image = bool(cmdline_opts.save_image); 
     num_bins = int(cmdline_opts.num_bins); 
     use_edist_squared = bool(cmdline_opts.use_edist_squared); 
     use_angle_gaps = bool(cmdline_opts.use_angle_gaps); 
     use_angles = bool(cmdline_opts.use_angles); 
     use_slopes = bool(cmdline_opts.use_slopes); 
     use_slope_gaps = bool(cmdline_opts.use_slope_gaps); 
     conf_file_path = str(cmdline_opts.conf_file_path); 
     
     tiling = Tiling(num_steps, "<Unknown Tiling>"); 
     if tiling_type == "AmmannChair": 
          tiling = AmmannChair_Tiling(num_steps, tiling_type); 
     elif tiling_type == "AmmannChair2": 
          tiling = AmmannChair2_Tiling(num_steps, tiling_type); 
     elif tiling_type == "GoldenTriangle": 
          tiling = GoldenTriangle_Tiling(num_steps, tiling_type); 
     elif tiling_type == "Penrose": 
          tiling = Penrose_Tiling(num_steps, tiling_type); 
     elif tiling_type == "Sphinx": 
          tiling = Sphinx_Tiling(num_steps, tiling_type); 
     elif tiling_type == "Pinwheel": 
          tiling = Pinwheel_Tiling(num_steps, tiling_type); 
     elif tiling_type == "Squares": 
          tiling = Square_Tiling(num_steps, tiling_type); 
     elif tiling_type == "Triangles": 
          tiling = Triangle_Tiling(num_steps, tiling_type); 
     elif tiling_type == "Domino": 
          tiling = Domino_Tiling(num_steps, tiling_type); 
     elif tiling_type == "Pentagon1": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 1, 
                   AA = 1.0, BB = 2.0, b = 1.5, c = 0.5, e = 0.5); 
     elif tiling_type == "Pentagon2": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 2, 
                   AA = 2.5, BB = 1.3, b = 1.35, c = 0.0, e = 1.0); 
     elif tiling_type == "Pentagon3": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 3, 
                   AA = 0.0, BB = 0.0, b = 0.3, c = 0.0, e = 0.0); 
     elif tiling_type == "Pentagon4": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 4, 
                   AA = 2.2, BB = 0.0, b = 1.6, c = 0.0, e = 0.0); 
     elif tiling_type == "Pentagon5": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 5, 
                   AA = 2.356, BB = 0.0, b = 0.5, c = 0.0, e = 0.0); 
     elif tiling_type == "Pentagon8": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 8, 
                   AA = 1.571, BB = 0.0, b = 0.0, c = 0.0, e = 0.0); 
     elif tiling_type == "Pentagon10": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 10, 
                   AA = 1.4, BB = 0.0, b = 0.0, c = 0.0, e = 0.0); 
     elif tiling_type == "Pentagon11": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 11, 
                   AA = 2.113, BB = 0.0, b = 0.0, c = 0.0, e = 0.0); 
     elif tiling_type == "Pentagon15": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 15, 
                   AA = 0.0, BB = 0.0, b = 0.0, c = 0.0, e = 0.0); 
     elif tiling_type == "SaddleConnGoldenL": 
          tiling = SaddleConnectionGoldenL(num_steps, tiling_type);
     elif tiling_type == "AmmannRhomb": 
          tiling = Ammann_Tiling(num_steps, tiling_type, RHOMB_TILE);
     elif tiling_type == "AmmannTriangle": 
          tiling = Ammann_Tiling(num_steps, tiling_type, TRIANGLE_TILE);
     elif tiling_type == "AmmannSquare": 
          tiling = Ammann_Tiling(num_steps, tiling_type, SQUARE_TILE);
     elif tiling_type == "AmmannEightStar": 
          tiling = Ammann_Tiling(num_steps, tiling_type, 8);
     elif tiling_type == "AmmannOctagon": 
          tiling = Ammann_Tiling(num_steps, tiling_type, 88);
     elif tiling_type == "IntegerLattice": 
          tiling = IntegerLattice_Tiling(num_steps, tiling_type);
     elif tiling_type == "Chair3": 
          tiling = Chair3_Tiling(num_steps, tiling_type);
     elif tiling_type == "MiniTangram": 
          tiling = MiniTangram_Tiling(num_steps, tiling_type);
     elif tiling_type == "Armchair": 
          tiling = Armchair_Tiling(num_steps, tiling_type);
     elif tiling_type == "TriTriangle": 
          tiling = TriTriangle_Tiling(num_steps, tiling_type);
     elif tiling_type == "Equithirds": 
          tiling = ETTriangle_Tiling(num_steps, tiling_type);
     elif tiling_type == "SDHouse": 
          tiling = SDHouse_Tiling(num_steps, tiling_type);
     elif tiling_type == "Pentomino": 
          tiling = Pentomino_Tiling(num_steps, tiling_type);
     elif tiling_type == "Cesi": 
          tiling = Cesi_Tiling(num_steps, tiling_type);
     elif tiling_type == "STPinwheel": 
          tiling = STPinwheel_Tiling(num_steps, tiling_type);
     elif tiling_type == "GRTriangle": 
          tiling = GRTriangle_Tiling(num_steps, tiling_type);
     elif tiling_type == "Domino-9Tile": 
          tiling = Domino9Tile_Tiling(num_steps, tiling_type);
     elif tiling_type == "Trihex": 
          tiling = Trihex_Tiling(num_steps, tiling_type);
     elif tiling_type == "T2000Triangle": 
          tiling = T2000Triangle_Tiling(num_steps, tiling_type);
     elif tiling_type == "AmmannA4": 
          tiling = AmmannA4_Tiling(num_steps, tiling_type);
     elif tiling_type == "PenroseKD": 
          tiling = PenroseKD_Tiling(num_steps, tiling_type);
     elif tiling_type == "DiamondTriangle": 
          tiling = DiamondTriangle_Tiling(num_steps, tiling_type);
     elif tiling_type == "Tetris": 
          tiling = Tetris_Tiling(num_steps, tiling_type);
     elif tiling_type == "Danzer7Fold": 
          tiling = Danzer7Fold_Tiling(num_steps, tiling_type);
     else: 
          print "Unknown tiling type: \"%s\" ... Exiting" % tiling_type; 
          sys.exit(1); 
     ## if 
     
     hist_type_desc = ""; 
     if use_angle_gaps: 
          hist_type_desc = "anglegaps"; 
     elif use_angles: 
          hist_type_desc = "angles"; 
     elif use_slopes: 
          hist_type_desc = "slopes";
     elif use_slope_gaps: 
          hist_type_desc = "slopegaps";
     elif use_edist_squared: 
          hist_type_desc = "pc-edistsq"; 
     else: 
          hist_type_desc = "pc-edist"; 
     ## if 
          
     config_params = ConfigParser(conf_file_path); 
     pxmin, pxmax = config_params.get_plot_range(tiling_type, hist_type_desc); 
     
     print "   Tiling Name: %s" % tiling.name; 
     print "   Tiling Desc: %s" % tiling.desc(); 
     print "   Num steps N := %d, Num bins = %d, Hist type = %s" \
           % (num_steps, num_bins, hist_type_desc); 
     print "   Config File: \"%s\"" % conf_file_path;
     print "   [XMIN, XMAX]: [%g, %g]" % (pxmin, pxmax)
     
     start_time = time.time(); 
     tiles = tiling.get_tiles(); 
     
     if save_image: 
          tiling_image = tiling.get_tiling_image(tiles); 
          image_path = "./output/%s-N.%03d-tiling.png" % (tiling.name, num_steps); 
          tiling_image.save(image_path); 
          tiling_image.show()
          print "   Saved tiling image to \"%s\" ... " % image_path; 
     ## if 
     #sys.exit(0);
     
     tiling_points = Tiling.tiling_to_points(tiles, True); 
     num_tiling_points = len(tiling_points); 
     
     hist_data = []; 
     if use_angle_gaps: 
          hist_data = Tiling.compute_angle_gaps(tiling_points); 
     elif use_angles: 
          hist_data = Tiling.compute_sorted_angles(tiling_points); 
     elif use_slopes:
          hist_data = Tiling.compute_sorted_slopes(tiling_points); 
     elif use_slope_gaps:
          hist_data = Tiling.compute_slope_gaps(tiling_points); 
     else: 
          hist_data = Tiling.compute_pc_edists(tiling_points, use_edist_squared, True); 
     ## if 

     ## re-scale the data if necessary: 
     scaling_factor = 1.0;
     if tiling_type == "IntegerLattice":
          scaling_factor = (LARGE_RADIUSR ** 2); 
     elif hist_type_desc == "anglegaps" or hist_type_desc == "slopegaps": 
          scaling_factor = float( len(hist_data) ** 2 ); 
     ## if 
     for (idx, hd) in enumerate(hist_data): 
          hist_data[idx] = scaling_factor * hd; 
     ## for 
     
     end_time = time.time(); 
     print "   Total time to compute histogram data: %g seconds" \
           % (end_time - start_time); 
     
     for nbins in num_bins_arr: 

          num_bins = nbins; 
          bin_size = (max(hist_data) - min(hist_data)) / float(num_bins); 
          bins = np.arange(min(hist_data), max(hist_data), bin_size); 
          
          hist = histogram(hist_data, bins = bins, \
                           xmin = pxmin, xmax = pxmax, normed = True, \
                           color = 'darkorange', \
                           edgecolor = Color('darkorange').darker().html_color(), \
                           alpha = 1.0, hatch = "*", zorder = 0, align = "mid", \
                           label = "label"); 
          if use_slope_gaps or use_slopes or use_angle_gaps or use_angles: 
               hist = histogram(hist_data, bins = bins, \
                                color = 'darkorange', \
                                edgecolor = Color('darkorange').darker().html_color(), \
                                alpha = 1.0, hatch = "*", zorder = 0, align = "mid", \
                                label = "label", xmin = pxmin, xmax = pxmax, normed = True); 
          ## if
                      
          hist_image_path = "./output/%s-NUMBINS.%06d-N.%03d-%s.png" \
                            % (tiling.name, num_bins, num_steps, hist_type_desc);
          hist_title =  "Histogram Parameters (%s):\n" % tiling.name; 
          hist_title += "N=%d, #bins=%d, hist type=%s\n" \
                        % (num_steps, num_bins, hist_type_desc); 
          hist_title += "#tiling points = %d, time taken = %g sec\n" \
                        % (len(tiling_points), time.time() - start_time); 
          hist_title += "Image Path: %s" % hist_image_path;
          hist_end_time = time.time(); 
     
          #hist.set_legend_options(\
          #     title = hist_title, loc = 'upper right', 
          #     font_family = 'fantasy', font_variant = 'small-caps', 
          #     font_weight = 'bold', font_size = 'x-small', 
          #     shadow = True, handlelength = 2); 
          hist.axes_labels(['hist value (x)', 'count (y)']); 
     
          hist.show(title = hist_image_path, fontsize = 10);
          hist.save(hist_image_path, title = hist_title, fontsize = 8); 
     
          print "   Saved pc histogram image to \"%s\" ... " % hist_image_path; 
          print "   Total time to generate histogram: %g seconds (%g sec)" \
                % (end_time - start_time, hist_end_time - end_time); 
     ## for 
     
     print "\n"; 
     sys.exit(0); 
