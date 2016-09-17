#### ConfigParser.py 
#### Configuration file parser for the plot ranges
#### Author: Maxie D. Schmidt
#### Created: 2016.04.10 

import string
import sys

PCEDIST_INDEX = 0; 
PCEDISTSQ_INDEX = 1;
ANGLES_INDEX = 2;
ANGLEGAPS_INDEX = 3;
SLOPES_INDEX = 4; 
SLOPEGAPS_INDEX = 5;

## strip_whitespace
 # Strips any whitespace characters from a string
 # @param s The input string we operate on
 # @return  The string with all whitespace characters replaced by ""
##
def strip_whitespace(s): 

     wchars = string.whitespace;
     for cidx in range(0, len(wchars)): 
          wch = wchars[cidx]; 
          s.replace(wch, "");
     ## for 
     return s;

## def 

## ConfigParser
 # A class defining a configuration file parser to change the x-axis bounds 
 # in a displayed histogram
##
class ConfigParser(object): 

     ## __init__
      # Initialization function for the ConfigParser class
      # @param config_file The path to the configuration file we will be parsing
     ##
     def __init__(self, config_file): 
          self.cpath = config_file; 
          self.range_dict = dict();
          self.parse(config_file);
     ## def 
     
     ## parse
      # Parses the config file in the format of the "plots-test.conf" example
      # @param config_file The path to the config file we're parsing
      # @return            Always 0
     ##
     def parse(self, config_file): 
     
          cfile = open(config_file, "r");
          line_number = 0; 
          for line in cfile:
               
               line_number += 1; 
               line = strip_whitespace(line); 
               if line == "" or line == "\n" or line[0] == '#':
                    continue; 
               ## if 
               
               [tiling, ranges] = line.split(':', 2); 
               ranges = ranges.split(';'); 
               if len(ranges) != 6: 
                    print "Insufficient number of plot ranges on line %d" % line_number;
                    sys.exit(1); 
               ## if 
               
               for (idx, r) in enumerate(ranges): 
                    [xmin, xmax] = r.split(',', 2); 
                    #self.range_dict[tiling] += (float(xmin), float(xmax)); 
                    self.range_dict.update({(tiling, idx) : (float(xmin), float(xmax))}); 
               ## for
               
          ## for 
          cfile.close(); 
          
          return 0; 
     
     ## def 
     
     ## plot_type_to_index
      # Converts the histogram plot type string to a locally defined index
      # @param plot_type The string of which plot type we're working with
      # @return          The corresponding index associated with the plot type
     ##
     @staticmethod
     def plot_type_to_index(plot_type): 
     
          if plot_type == "pc-edist":
               return PCEDIST_INDEX; 
          elif plot_type == "pc-edistsq": 
               return PCEDISTSQ_INDEX; 
          elif plot_type == "angles":
               return ANGLES_INDEX; 
          elif plot_type == "anglegaps":
               return ANGLEGAPS_INDEX;
          elif plot_type == "slopes":
               return SLOPES_INDEX; 
          elif plot_type == "slopegaps":
               return SLOPEGAPS_INDEX; 
          else: 
               print "Unknown plot type \"%s\"" % plot_type; 
               sys.exit(1); 
          ## if 
          
          return -1; 
     
     ## def 
     
     ## get_plot_range
      # Returns the minimum and maximum x-axis bounds on the plot
      # @param tiling    A string of the tiling identifier string
      # @param hist_type The histogram plot type string
      # @return          A comma-separated pair of values for the range: 
      #                  xmin, xmax
     ##
     def get_plot_range(self, tiling, hist_type): 
     
          plot_type_index = self.plot_type_to_index(hist_type); 
          (xmin, xmax) = self.range_dict[(tiling, plot_type_index)]; 
          return xmin, xmax; 

     ## def 

## class

