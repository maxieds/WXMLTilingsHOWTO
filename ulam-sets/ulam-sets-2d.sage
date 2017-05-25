from sage.all import *
from sage.plot.histogram import Histogram, histogram
from itertools import takewhile
from ulam_sets import compute_ulam_set

def V(x, y): 
     return vector([x, y])
##

def max_norm(v): 
     return max(map(abs, list(v)))
##

def edist(v): # === Euclidean distance squared
     xycoords = list(v)
     comps = map(lambda xycoord: xycoord ** 2, xycoords)
     return sum(comps)
##

def compute_Sn_set(ulam_set, norm_func, alpha = 2.5714474995): 
     Sn = []
     for an in ulam_set: ## my guess at what the set S_N should look like in 2d: 
          sn = norm_func(alpha * an) - float(2*pi) * floor(norm_func(alpha * an / 2.0 / float(pi)))
          Sn += [sn]
     ## 
     return Sn
##

def save_ulam_set_image_v2(outfile, init_vectors, n = 100, a1a2 = [1, 1], 
                           norm_funcs = [(max_norm, "Max Norm"), (edist, "Euclidean Distance")]):  
           
     # plot options (change these as you will to explore): 
     thickness, sbase, aratio, ps = 2, float(golden_ratio), 'automatic', 15
     scale_options = [('linear', 10), ('semilogy', sbase), ('semilogx', sbase), ('loglog', sbase)]
     
     # compute the plots: 
     init_conds_len = len(init_vectors)
     image_graphics = []
     for (norm_func, nfunc_desc) in norm_funcs: 
          ulam_set = compute_ulam_set_v2(a1a2[0], a1a2[1], n, init_vectors, norm_func)
          print "ULAM SET: ", ulam_set, "\n"
          gplot = point(ulam_set, pointsize=ps, axes = False, axes_labels = None, gridlines = None)
          snset = compute_Sn_set(ulam_set, norm_func)
          g1, g2, g3, g4 = Graphics(), Graphics(), Graphics(), Graphics()
          snhist = g1 + histogram(snset, normed = True)
          snhist_normed = g2 + histogram(snset, normed = True)
          snhist_normed_bins100 = g3 + histogram(snset, bins = 100, normed = True)
          snhist_normed_cdf = g4 + histogram(snset, normed = True, cumulative = True)
          graphics_row = [gplot, snhist, snhist_normed, snhist_normed_bins100, snhist_normed_cdf]
          for sopt in []: #scale_options: 
               plot_title = "Ulam Set Plots: $%s$\n\nUlam Set Plot\nNorm = %s, Scale = %s" % ("[]", nfunc_desc, sopt)
               #gplot = plot(ulam_set, title = plot_title, scale = sopt[0], base = sopt[1])
               gplot = point(ulam_set, pointsize=ps, scale = sopt, axes = False, 
                             axes_labels = None, gridlines = None, aspect_ratio = 'automatic', 
                             title = plot_title)
               #gplot.save("test-%s.png" % nfunc_desc, axes = False, axes_labels = None)
          ##
          image_graphics += [graphics_row]
          
     ## 
     garray = graphics_array(image_graphics)
     plot_title_lst = map(lambda (x, y): r'$[^{% 3g}_{% 3g}]$' % (x, y), init_vectors)[0:init_conds_len]
     plot_title = "\{" + ', '.join(plot_title_lst) + ", \ldots\}"
     garray.show(title = plot_title, fontsize = 5, frame = True, typeset = 'latex', axes = False, axes_labels = ("", ""))
     garray.save(outfile, title = plot_title, fontsize = 14, axes = False, frame = True, gridlines = False, axes_labels = ("", ""), typeset = 'latex', figsize = [10, 10])
     
## 

def save_ulam_set_image(outfile, init_vectors, n = 100, a1a2 = [1, 1], 
                        norm_funcs = [(max_norm, "Max Norm")]):  
           
     # plot options (change these as you will to explore): 
     thickness, sbase, aratio, ps = 2, float(golden_ratio), 'automatic', 15
     scale_options = [('linear', 10), ('semilogy', sbase), ('semilogx', sbase), ('loglog', sbase)]
     
     # compute the plots: 
     init_conds_len = len(init_vectors)
     image_graphics = []
     for (norm_func, nfunc_desc) in norm_funcs: 
          #ulam_set = compute_ulam_set_v2(a1a2[0], a1a2[1], n, init_vectors, norm_func)
          ulam_set = compute_ulam_set(n, init_vectors)
          print "ULAM SET: ", ulam_set, "\n"
          gplot = point(ulam_set, pointsize=ps, axes = False, axes_labels = None, gridlines = None)
          image_graphics += [[gplot]]     
     ## 
     garray = graphics_array(image_graphics)
     plot_title_lst = map(lambda (x, y): r'$[^{% 3g}_{% 3g}]$' % (x, y), init_vectors)[0:init_conds_len]
     plot_title = "\{" + ', '.join(plot_title_lst) + ", \ldots\}"
     garray.show(title = plot_title, fontsize = 5, frame = True, typeset = 'latex', axes = False, axes_labels = ("", ""))
     garray.save(outfile, title = plot_title, fontsize = 14, axes = False, frame = True, gridlines = False, axes_labels = ("", ""), typeset = 'latex', figsize = [10, 10])
     
## 

def save_example_images(n = 10, a1a2 = [1, 1]):    
     
     (a, b) = map(float, a1a2)
     absuffix = "a%03db%03d" % (a, b)
     initial_vector_configs = [ ## examples from Jayadev's talk and in the article: 
          [V(1, golden_ratio), V(0, 1)], 
          [V(1, golden_ratio), V(golden_ratio, 1)], 
          [V(1, golden_ratio), V(1, 0)], 
          [V(1, 0), V(0, 1)], 
          [V(9, 0), V(0, 9), V(1, 13)], 
          [V(2, 5), V(3, 1)], 
          [V(1, 0), V(2, 0), V(0, 1)], 
          [V(2, 0), V(0, 1), V(3, 1)], 
          [V(1, 0), V(0, 1), V(2, 3)], 
          [V(3, 0), V(0, 1), V(1, 1)], 
          [V(1, 0), V(2, 0), V(0, 1)], 
          [V(2, 0), V(3, 0), V(0, 1)], 
          [V(1, 0), V(0, 1), V(6, 4)], 
          [V(1, 0), V(0, 1), V(10, 9)], 
          [V(1, 0), V(0, 1), V(10, 3)], 
          [V(1, 3), V(3, 4)], 
          [V(1, 0), V(1, 1)]
     ] 
     
     for (icidx, init_vectors) in enumerate(initial_vector_configs): 
          plot_suffix = "ulam-set" + "-N." + "%05d" % n + "-" + absuffix + "-v" + str(icidx + 1) + ".png"
          print "  => Saving image \"%s\" ... " % plot_suffix
          print map(list, init_vectors)
          save_ulam_set_image(plot_suffix, map(tuple, init_vectors), n, a1a2)
     ## 
     
##

def generate_lincombo_comp_graphs(outfile_suffix, init_vectors, n, norm_func = max_norm): 
     
     garray_data = []
     for a1 in range(1, 5): 
          graphics_row = []
          for a2 in range(1, 5): 
               print "a1 / a2", [a1, a2]
               ulam_set = compute_ulam_set_v2(a1, a2, n, init_vectors, norm_func) 
               print "ULAM_SET: ", ulam_set
               plot_title = r"$a_1$ / $a_2$ = % 3g / % 3g" % (a1, a2)
               gplot = point(ulam_set, pointsize=2, axes = False, axes_labels = None, gridlines = None, 
                             title = plot_title)
               graphics_row += [gplot]
               #graphics_row += [ulam_set]
          ##
          garray_data += [graphics_row]
     ## 
     
     outfile = 'ulam-set-' + outfile_suffix + '.png'
     garray = graphics_array(garray_data)
     garray.show(fontsize = 5, frame = True, typeset = 'latex', axes = False, axes_labels = ("", ""))
     garray.save(outfile, fontsize = 14, axes = False, frame = True, gridlines = False, 
                 axes_labels = ("", ""), figsize = [10, 10])

##

def compute_2d_integral(n, init_vectors = [V(1, float(golden_ratio)), V(1, 0)]): 

     ulam_set = compute_ulam_set_v2(1, 1, n, init_vectors, max_norm)
     alpha, x, y = var('alpha x y')
     N = len(ulam_set)
     integrand = lambda x, y: sum(map(lambda (m, n): cos(2 * pi * alpha *(m*x+n*y)), ulam_set))
     defintx = lambda y: integral(integrand(x, y), x, 0, 1)
     defint = integral(defintx(y), y, 0, 1)
     graphics = plot(defint, (-2*pi, 2*pi))
     graphics += plot(N, (-2*pi, 2*pi), title = "N = %d" % N)
     return defint, graphics
     #print simplify(defint)
     #print find_root(defint == -0.8 * N, 0, 2*pi)
     #print defint.subs(alpha == 1.0).n()
     #print map(lambda soln: soln.rhs(), solve([defint == -0.8 * N], alpha))

##

def compute_2d_integral_plots(init_vectors = [V(1, golden_ratio), V(1, 0)]): 
     nvalues = [5, 10, 15, 20, 25, 30, 35, 40, 45, 45, 50, 55]
     garray, grow = [], []
     for (nidx, N) in enumerate(nvalues): 
          grow += [compute_2d_integral(N, init_vectors)]
          if nidx % 3 == 2: 
               garray += [grow]
               grow = []
          ##
     ##
     gplots = graphics_array(garray)
     gplots.show(frame = True)
##

a1a2_array = [ [ [1,1], [1,2], [1,3], [1,4] ], 
               [ [2,1], [2,2], [2,3], [2,4] ], 
               [ [3,1], [3,2], [3,3], [3,4] ], 
               [ [4,1], [4,2], [4,3], [4,4] ]
             ]
initial_vector_configs = [ ## examples from Jayadev's talk and in the article: 
          #[V(1, float(golden_ratio)), V(0, 1)], 
          #[V(1, float(golden_ratio)), V(float(golden_ratio), 1)], 
          #[V(1, float(golden_ratio)), V(1, 0)], 
          [V(1, 0), V(0, 1)], 
          #[V(9, 0), V(0, 9), V(1, 13)], 
          #[V(2, 5), V(3, 1)], 
          #[V(1, 0), V(2, 0), V(0, 1)], 
          #[V(2, 0), V(0, 1), V(3, 1)], 
          #[V(1, 0), V(0, 1), V(2, 3)], 
          #[V(3, 0), V(0, 1), V(1, 1)], 
          #[V(1, 0), V(2, 0), V(0, 1)], 
          #[V(2, 0), V(3, 0), V(0, 1)], 
          #[V(1, 0), V(0, 1), V(6, 4)], 
          #[V(1, 0), V(0, 1), V(10, 9)], 
          #[V(1, 0), V(0, 1), V(10, 3)], 
          #[V(1, 3), V(3, 4)], 
          #[V(1, 0), V(1, 1)]
     ] 
Nvalue = 20
init_vectors = initial_vector_configs[0]


     
