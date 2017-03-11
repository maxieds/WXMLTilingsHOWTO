#### tiling_pc_plots.py 
#### Program to generate pair correlation histogram plots for multiple tilings 
#### Author: Maxie D. Schmidt
#### Created: 2016.02.20 

import sys
import time
import numpy as np
import pprint 
import statistics as statpdf
from LocalSageHistogram import LocalHistogram
import matplotlib.pyplot as plt
from scipy.stats.mstats import mquantiles

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
from SaddleConnectionGoldenL import SaddleConnectionGoldenL, SaddleConnGoldenL_finfinity, fit_SaddleConnGoldenL_pdf
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
from WaltonChair import WaltonChair_Tiling
from Octagonal1225 import Octagonal1225_Tiling
from AmmannA3 import AmmannA3_Tiling
from Fibonacci2D import Fibonacci2D_Tiling
from PChairs import PChairs_Tiling
from TubingenTriangle import TubingenTriangle_Tiling

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
                 dest = "save_image", default = False, 
                 help = "Save a copy of the tiling image to output"), 
     make_option("-b", "--num-bins", metavar = "NUM-HIST-BINS", 
                 dest = "num_bins", default = -1, action = 'store', 
                 help = "Number of distinct equi-sized bins to use in the histograms"), 
     make_option("-c", "--config-file", metavar = "CONFIG-FILE", 
                 dest = "conf_file_path", default = "plots.conf", 
                 help = "Path to the config file for the plot ranges"), 
     make_option("-p", "--use-plot-ranges", metavar = "USE-PLOT-RANGES", 
                 dest = "use_plot_ranges", 
                 action = "store_true", default = False, 
                 help = "Use plot ranges in plots.conf"),  
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
     make_option("-i", "--image-only", 
                 action = "store_true", metavar = "COMPUTE-IMAGE-ONLY", 
                 dest = "image_only", default = False, 
                 help = "Compute and save the image of the tiling only before exiting"), 
     make_option("-v", "--verbose", 
                 action = "store_true", 
                 dest = "verbose", 
                 help = SUPPRESS_HELP), 
                 
]; 

argspec_usage = "%prog [-v] [-h] [--version] [-s] [-q] [-d] [-n NUM-STEPS] [-t TSPEC] [-b NUM-BINS]"; 
argspec_version = "%prog 1.0" 

#num_bins_arr = [10, 15, 25, 35, 50, 75, 85, 100, 125, 150, 175, 200, 250, 500, 750, 1000, 2000, 5000, 7500, 10000];
num_bins_arr = [10, 20, 35, 55, 75, 100, 125, 150, 200, 250, 350, 500, 750, 1000] 
#num_bins_arr = ['auto', 'fd', 'doane', 'scott', 'rice', 'sturges', 'sqrt']

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
     image_only = bool(cmdline_opts.image_only); 
     num_bins = int(cmdline_opts.num_bins); 
     use_edist_squared = bool(cmdline_opts.use_edist_squared); 
     use_angle_gaps = bool(cmdline_opts.use_angle_gaps); 
     use_angles = bool(cmdline_opts.use_angles); 
     use_slopes = bool(cmdline_opts.use_slopes); 
     use_slope_gaps = bool(cmdline_opts.use_slope_gaps); 
     conf_file_path = str(cmdline_opts.conf_file_path); 
     no_plot_ranges = not bool(cmdline_opts.use_plot_ranges)
     
     tiling = Tiling(num_steps, "<Unknown Tiling>");
     inflation_factor = 1.0
     if tiling_type == "AmmannChair": 
          tiling = AmmannChair_Tiling(num_steps, tiling_type); 
          inflation_factor = n(sqrt(golden_ratio))
     elif tiling_type == "AmmannChair2": 
          tiling = AmmannChair2_Tiling(num_steps, tiling_type); 
          inflation_factor = 2.0
     elif tiling_type == "GoldenTriangle": 
          tiling = GoldenTriangle_Tiling(num_steps, tiling_type); 
          inflation_factor = n(sqrt(golden_ratio))
     elif tiling_type == "Penrose": 
          tiling = Penrose_Tiling(num_steps, tiling_type); 
          inflation_factor = n(golden_ratio)
     elif tiling_type == "Sphinx": 
          tiling = Sphinx_Tiling(num_steps, tiling_type); 
          inflation_factor = 2.0
     elif tiling_type == "Pinwheel": 
          tiling = Pinwheel_Tiling(num_steps, tiling_type); 
          inflation_factor = 1.0 #n(sqrt(5))
     elif tiling_type == "Squares": 
          tiling = Square_Tiling(num_steps, tiling_type); 
          inflation_factor = 4.0
     elif tiling_type == "Triangles": 
          tiling = Triangle_Tiling(num_steps, tiling_type); 
          inflation_factor = 1.0
     elif tiling_type == "Domino": 
          tiling = Domino_Tiling(num_steps, tiling_type); 
          inflation_factor = 1.0
     elif tiling_type == "Pentagon1": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 1, 
                   AA = 1.0, BB = 2.0, b = 1.5, c = 0.5, e = 0.5); 
          inflation_factor = 1.0
     elif tiling_type == "Pentagon2": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 2, 
                   AA = 2.5, BB = 1.3, b = 1.35, c = 0.0, e = 1.0); 
          inflation_factor = 1.0
     elif tiling_type == "Pentagon3": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 3, 
                   AA = 0.0, BB = 0.0, b = 0.3, c = 0.0, e = 0.0); 
          inflation_factor = 1.0
     elif tiling_type == "Pentagon4": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 4, 
                   AA = 2.2, BB = 0.0, b = 1.6, c = 0.0, e = 0.0); 
          inflation_factor = 1.0
     elif tiling_type == "Pentagon5": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 5, 
                   AA = 2.356, BB = 0.0, b = 0.5, c = 0.0, e = 0.0); 
          inflation_factor = 1.0
     elif tiling_type == "Pentagon8": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 8, 
                   AA = 1.571, BB = 0.0, b = 0.0, c = 0.0, e = 0.0); 
     elif tiling_type == "Pentagon10": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 10, 
                   AA = 1.4, BB = 0.0, b = 0.0, c = 0.0, e = 0.0); 
          inflation_factor = 1.0
     elif tiling_type == "Pentagon11": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 11, 
                   AA = 2.113, BB = 0.0, b = 0.0, c = 0.0, e = 0.0); 
          inflation_factor = 1.0
     elif tiling_type == "Pentagon15": 
          tiling = Pentagon_Tiling(num_steps, tiling_type, 15, 
                   AA = 0.0, BB = 0.0, b = 0.0, c = 0.0, e = 0.0); 
          inflation_factor = 1.0
     elif tiling_type == "SaddleConnGoldenL": 
          tiling = SaddleConnectionGoldenL(num_steps, tiling_type);
          inflation_factor = 1.0
     elif tiling_type == "AmmannRhomb": 
          tiling = Ammann_Tiling(num_steps, tiling_type, RHOMB_TILE);
          inflation_factor = n(1 + sqrt(2))
     elif tiling_type == "AmmannTriangle": 
          tiling = Ammann_Tiling(num_steps, tiling_type, TRIANGLE_TILE);
          inflation_factor = n(1 + sqrt(2))
     elif tiling_type == "AmmannSquare": 
          tiling = Ammann_Tiling(num_steps, tiling_type, SQUARE_TILE);
          inflation_factor = n(1 + sqrt(2))
     elif tiling_type == "AmmannEightStar": 
          tiling = Ammann_Tiling(num_steps, tiling_type, 8);
          inflation_factor = n(1 + sqrt(2))
     elif tiling_type == "AmmannOctagon": 
          tiling = Ammann_Tiling(num_steps, tiling_type, 88);
          inflation_factor = n(1 + sqrt(2))
     elif tiling_type == "IntegerLattice": 
          tiling = IntegerLattice_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0
     elif tiling_type == "Chair3": 
          tiling = Chair3_Tiling(num_steps, tiling_type);
          inflation_factor = 3.0
     elif tiling_type == "MiniTangram": 
          tiling = MiniTangram_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0
     elif tiling_type == "Armchair": 
          tiling = Armchair_Tiling(num_steps, tiling_type);
          inflation_factor = 2.0
     elif tiling_type == "TriTriangle": 
          tiling = TriTriangle_Tiling(num_steps, tiling_type);
          inflation_factor = 2.0
     elif tiling_type == "Equithirds": 
          tiling = ETTriangle_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0
     elif tiling_type == "SDHouse": 
          tiling = SDHouse_Tiling(num_steps, tiling_type);
          inflation_factor = 2.0
     elif tiling_type == "Pentomino": 
          tiling = Pentomino_Tiling(num_steps, tiling_type);
          inflation_factor = 2.0
     elif tiling_type == "Cesi": 
          tiling = Cesi_Tiling(num_steps, tiling_type);
          inflation_factor = 2.0
     elif tiling_type == "STPinwheel": 
          tiling = STPinwheel_Tiling(num_steps, tiling_type);
          inflation_factor = n(sqrt(3))
     elif tiling_type == "GRTriangle": 
          tiling = GRTriangle_Tiling(num_steps, tiling_type);
          inflation_factor = 3.0
     elif tiling_type == "Domino-9Tile": 
          tiling = Domino9Tile_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0
     elif tiling_type == "Trihex": 
          tiling = Trihex_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0 # TODO
     elif tiling_type == "T2000Triangle": 
          tiling = T2000Triangle_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0 # TODO
     elif tiling_type == "AmmannA4": 
          tiling = AmmannA4_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0 # TODO
     elif tiling_type == "PenroseKD": 
          tiling = PenroseKD_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0 # TODO
     elif tiling_type == "DiamondTriangle": 
          tiling = DiamondTriangle_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0 # TODO
     elif tiling_type == "Tetris": 
          tiling = Tetris_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0
     elif tiling_type == "Danzer7Fold": 
          tiling = Danzer7Fold_Tiling(num_steps, tiling_type);
          inflation_factor = 1 + n(sin(2.0 * pi / 7.0) / sin(pi / 7.0))
     elif tiling_type == "WaltonChair": 
          tiling = WaltonChair_Tiling(num_steps, tiling_type);
          inflation_factor = n(sqrt(2))
     elif tiling_type == "Octagonal1225": 
          tiling = Octagonal1225_Tiling(num_steps, tiling_type);
          inflation_factor = n(1 + sqrt(2))
     elif tiling_type == "AmmannA3": 
          tiling = AmmannA3_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0 # TODO
     elif tiling_type == "Fibonacci2D": 
          tiling = Fibonacci2D_Tiling(num_steps, tiling_type);
          inflation_factor = 1.0
     elif tiling_type == "PChairs": 
          tiling = PChairs_Tiling(num_steps, tiling_type);
          inflation_factor = 3.0 / 2.0 * n(sqrt(2))
     elif tiling_type == "TubingenTriangle": 
          tiling = TubingenTriangle_Tiling(num_steps, tiling_type);
          inflation_factor = n(golden_ratio)
     #elif tiling_type == "AmmannBeenker": 
     #     tiling = ABRhombTriangle_Tiling(num_steps, tiling_type);
     #     inflation_factor = n(1 + sqrt(2))
     else: 
          print "Unknown tiling type: \"%s\" ... Exiting" % tiling_type; 
          sys.exit(1); 
     ## if 
     
     hist_type_desc, print_desc = "", "" 
     if use_angle_gaps: 
          hist_type_desc = "anglegaps" 
          print_desc = "Angle Gaps"
     elif use_angles: 
          hist_type_desc = "angles" 
          print_desc = "Angles"
     elif use_slopes: 
          hist_type_desc = "slopes"
          print_desc = "Slopes"
     elif use_slope_gaps: 
          hist_type_desc = "slopegaps"
          print_desc = "Slope Gaps"
     elif use_edist_squared: 
          hist_type_desc = "pc-edistsq"
          print_desc = "Pair Correlation (Squared)"
     else: 
          hist_type_desc = "pc-edist"
          print_desc = "Pair Correlation"
     ## if 
          
     config_params = ConfigParser(conf_file_path); 
     pxmin, pxmax = config_params.get_plot_range(tiling_type, hist_type_desc); 
     
     print "   Tiling Name: %s" % tiling.name; 
     print "   Tiling Desc: %s" % tiling.desc(); 
     print "   Num steps N := %d, Num bins = %d, Hist type = %s" \
           % (num_steps, num_bins, hist_type_desc); 
     print "   Config File: \"%s\"" % conf_file_path;
     print "   Using Plot Ranges: %s" % ("No" if no_plot_ranges else "Yes")
     
     start_time = time.time(); 
     tiles = tiling.get_tiles(); 
     
     if save_image: 
          tiling_image = tiling.get_tiling_image(tiles); 
          image_path = "./output/%s-N.%03d-tiling.png" % (tiling.name, num_steps); 
          tiling_image.save(image_path); 
          tiling_image.show()
          print "   Saved tiling image to \"%s\" ... " % image_path; 
     ## if 
     if image_only: 
          sys.exit(0);
     ##
     
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
          scaling_factor = (num_steps ** 2) #/ float( len(hist_data) ); 
     ## 
     temp_hist_data = hist_data
     hist_data = []
     for (idx, hd) in enumerate(temp_hist_data): 
          hist_data += [scaling_factor * hd * (inflation_factor ** num_steps)]; 
     ## for 
     hist_data = list(np.sort(hist_data))

     if no_plot_ranges: # plot the most natural range based on quantiles
          [qlower, qupper] = list(mquantiles(np.array(hist_data), prob = [0.15, 0.80]))
          pxmin, pxmax = qlower, qupper
     print "   [XMIN, XMAX]: [%g, %g]" % (pxmin, pxmax)

     ## smooth approximating curves:
     #if tiling_type == "SaddleConnGoldenL":
     #     x, fcmin, fcmax = var('x'), 0, min(10, pxmax)
     #     fitcurve += SaddleConnGoldenL_finfinity(x).plot(x, fcmin, fcmax, \
     #                 linestyle = '-.', rgbcolor = Color('purple').lighter(0.4), 
     #                 thickness = 1.25, 
     #                 legend_label = 'SaddleConnGoldenL Limiting Gap Dist', 
     #                 aspect_ratio = 'automatic')
     ## 

     end_time = time.time(); 
     print "   Total time to compute histogram data: %g seconds" \
           % (end_time - start_time); 
     
     for nbins in num_bins_arr: 

          num_bins, hmin, hmax = nbins, pxmin, pxmax
          bin_size = (hmax - hmin) / float(num_bins)
          coarsebins = list(np.arange(hmin - bin_size, hmax + bin_size, bin_size))
          
          ## add higher bin resolution at the beginning of the distribution:
          [lowerdist_max] = mquantiles(np.array(hist_data), prob = [0.05])
          rbinsize = bin_size / 4.0
          refinedbins = list(np.arange(hmin - rbinsize, lowerdist_max + rbinsize, rbinsize))
          histbins = np.sort(np.unique(refinedbins + coarsebins))
          
          #lhistpdf = LocalHistogram(hist_data, bins = histbins, rgbcolor = 'darkorange', 
          #                          thickness = 1.0, aspect_ratio = 'automatic', 
          #                          legend_label = 'Coarse Histogram Distribution (pdf)', 
          #                          cumulative = False, probability = False, 
          #                          xran = [hmin, hmax])
          lhistpdf = LocalHistogram(hist_data, bins = nbins, rgbcolor = 'darkorange', 
                                    thickness = 1.0, aspect_ratio = 'automatic', 
                                    legend_label = 'Coarse Histogram Distribution (pdf)', 
                                    cumulative = False, probability = False, 
                                    xran = [hmin, hmax])
          lhistcdf = LocalHistogram(hist_data, bins = histbins, rgbcolor = 'green', 
                                    thickness = 1.0, aspect_ratio = 'automatic', 
                                    legend_label = 'Coarse Histogram Distribution (cdf)', 
                                    cumulative = True, probability = False, 
                                    xran = [hmin, hmax])
          plthistpdf, histx, histy = lhistpdf.get_histogram_plot(), \
                                     lhistpdf.histx, lhistpdf.histy
          plthistcdf = lhistcdf.get_histogram_plot()
          approx_pdf_points = lhistcdf.compute_derivative_list()
          approx_pdf_plot = list_plot(approx_pdf_points, linestyle = '-.', 
                                      rgbcolor = Color('purple').darker(0.4), 
                                      plotjoined = True, 
                                      thickness = 1.5, ymin = 0, 
                                      legend_label = 'Approximate Derivative of cdf(x) / pdf(x)')
          plthistcdf += approx_pdf_plot
          
          #hist = histogram(hist_data, 
          #                 bins = histbins, weights = None, 
          #                 normed = True, cumulative = False, 
          #                 xmin = hmin, xmax = hmax, 
          #                 #range = [hmin, hmax], 
          #                  color = 'darkorange', \
          #                  edgecolor = Color('green').darker().html_color(), \
          #                  alpha = 1.0, hatch = "*", zorder = 0, align = "mid", rwidth = 0.5, 
          #                  aspect_ratio = 'automatic')
          # plthist = plt.hist(np.array(hist_data), bins = coarsebins, weights = None, 
          #                  normed = True, cumulative = False, 
          #                  #xmin = hmin, xmax = hmax, 
          #                  range = [hmin, hmax], 
          #                  color = 'darkorange', \
          #                  edgecolor = Color('darkorange').darker().html_color(), \
          #                  alpha = 0.5, hatch = "*", zorder = 0, align = "mid")
          # plthisty, plthistx = map(list, list(plthist)[0:2])
          # plthist = plot_step_function(zip(plthistx, plthisty), vertical_lines = True, 
          #                              rgbcolor = 'darkblue', thickness = 1.25, 
          #                              legend_label = 'Coarse Histogram Distribution', 
          #                              aspect_ratio = 'automatic')
          # 
          #plthistpdf += hist
          #plthistpdf += plthist
          
          if tiling.name == "SaddleConnGoldenL" or tiling.name == "TubingenTriangle" and \
             hist_type_desc == "slopegaps": 
               try:
                    print len(histx), len(histy)
                    bin_centers = histx[:-1] + 0.5 * np.diff(histx)
                    fitfunc, plot_lowerx, [a, b, c, d] = fit_SaddleConnGoldenL_pdf(hist_data, 
                                                                                   bin_centers, 
                                                                                   histy, 
                                                                                   [hmin, hmax])
                    fitlabel = "%s: %03g * f(%03g x + %03g) + %03g" % \
                               ('Limiting Gap Dist', a, b, c, d)
                    plot_points = [(t, n(fitfunc(t))) for t in 
                                   srange(plot_lowerx + 2 * bin_size, hmax, bin_size / 2.0, 
                                          include_endpoint = True)]
                    fitcurve = list_plot(plot_points, linestyle = '-.', 
                                         rgbcolor = Color('purple').darker(0.4), 
                                         plotjoined = True, 
                                         thickness = 1.5, ymin = 0, 
                                         legend_label = fitlabel)
                    #fitcurve = plot(fitfunc(x), x, plot_lowerx + 2 * bin_size, hmax, 
                    #               linestyle = '-.', rgbcolor = Color('purple').darker(0.4), 
                    #               thickness = 1.5, ymin = 0, 
                    #               legend_label = 'Scaled / Translated Limiting Gap Dist')
                    plthistpdf += fitcurve
               except RuntimeError: 
                    print "Unable to fit the exact distribution to our local plot."
               ##
          ##
          
          time_taken = time.time() - start_time
          hist_image_path = "./output/%s-NUMBINS.%06d-N.%03d-%s.png" \
                            % (tiling.name, num_bins, num_steps, hist_type_desc);
          hist_title =  "%s(N:=%d) %s:\n" % (tiling.name, num_steps, print_desc) 
          hist_title += "#bins=%d, #tiling points = %d\n" \
                        % (num_bins, len(tiling_points)); 
          #hist_title += "$\\mu = %04g$, $\\sigma = %04g$/n" % (mean(hist_data), std(hist_data))
          hist_title += "Time Taken: %g sec (%g mins)\n" % (time_taken, time_taken / 60.0)
          hist_end_time = time.time(); 
          
          plthistpdf.set_legend_options(\
                         loc = 'upper right', 
                         font_family = 'fantasy', font_variant = 'small-caps', 
                         font_weight = 'bold', font_size = 'x-small', 
                         shadow = True, handlelength = 2); 
          plthistpdf.axes_labels(['x', 'pdf(x)'])
          plthistcdf.set_legend_options(\
                         loc = 'upper right', 
                         font_family = 'fantasy', font_variant = 'small-caps', 
                         font_weight = 'bold', font_size = 'x-small', 
                         shadow = True, handlelength = 2); 
          plthistpdf.axes_labels(['x', 'cdf(x)'])
          plthistpdf.show(title = hist_image_path, fontsize = 10, frame = True, 
                          font_weight = 'bold', fig_tight = False)
          plthistcdf.show(title = hist_image_path, fontsize = 10, frame = True, 
                          font_weight = 'bold', fig_tight = False)
                          
          full_hist_plot = graphics_array([[plthistpdf, plthistcdf]])
          full_hist_plot.show(title = hist_image_path, fontsize = 10, frame = True)
          full_hist_plot.save(hist_image_path, title = hist_title, fontsize = 12.5, 
                              axes_labels = ['x', 'pdf/cdf(y)'], axes_labels_size = 2.5, 
                              gridlines = ['major', 'major'], frame = True, 
                              figsize = [12, 8])
     
          print "   Saved pc histogram image to \"%s\" ... " % hist_image_path; 
          print "   Total time to generate histogram: %g seconds (%g sec)" \
                % (end_time - start_time, hist_end_time - end_time); 
     ## for 
     
     print "\n"; 
     sys.exit(0); 
