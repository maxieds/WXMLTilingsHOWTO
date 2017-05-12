from sage.all import *
from sage.plot.histogram import Histogram, histogram

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

def compute_next_ulam_element(prev_elts, a1a2 = [1.0, 1.0], norm_func = max_norm): 
     [a1, a2] = a1a2
     pwdistinct_vectors = Combinations(prev_elts, 2).list()
     pwd_vector_sums = map(lambda v12: a1 * v12[0] + a2 * v12[1], pwdistinct_vectors)
     pwd_vector_sums2 = map(lambda vsum: norm_func(vsum), pwd_vector_sums)
     distinct_vsums = []
     for (idx, norm) in enumerate(pwd_vector_sums2): 
          if pwd_vector_sums.count(pwd_vector_sums[idx]) == 1 and prev_elts.count(pwd_vector_sums[idx]) == 0: 
               distinct_vsums += [(pwd_vector_sums[idx], norm)]
          ##
     ##
     vsum, maxnorm = min(distinct_vsums, key = lambda v: v[1])
     return vector(vsum)
## 

def compute_ulam_set(n, init_vectors, a1a2 = [1.0, 1.0], norm_func = max_norm): 
     ulam_set = init_vectors
     for k in range(len(ulam_set), n + 1): 
          ulam_set += [compute_next_ulam_element(ulam_set, a1a2, norm_func)]
     ## 
     return ulam_set
## 

def compute_Sn_set(ulam_set, norm_func, alpha = 2.5714474995): 
     Sn = []
     for an in ulam_set: ## my guess at what the set S_N should look like in 2d: 
          sn = norm_func(alpha * an) - float(2*pi) * floor(norm_func(alpha * an / 2.0 / float(pi)))
          Sn += [sn]
     ## 
     return Sn
##

def save_ulam_set_image(outfile, init_vectors, n = 100, a1a2 = [1.0, 1.0], 
                        norm_funcs = [(max_norm, "Max Norm"), (edist, "Euclidean Distance")]):  
           
     # plot options (change these as you will to explore): 
     thickness, sbase, aratio, ps = 2, float(golden_ratio), 'automatic', 15
     scale_options = [('linear', 10), ('semilogy', sbase), ('semilogx', sbase), ('loglog', sbase)]
     
     # compute the plots: 
     init_conds_len = len(init_vectors)
     image_graphics = []
     for (norm_func, nfunc_desc) in norm_funcs: 
          ulam_set = compute_ulam_set(n, init_vectors, a1a2, norm_func)
          #print "ULAM SET: ", ulam_set, "\n"
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

def save_example_images(n = 10, a1a2 = [1.0, 1.0]):    
     
     (a, b) = map(float, a1a2)
     absuffix = "a%03db%03d" % (a, b)
     initial_vector_configs = [ ## examples from Jayadev's talk and in the article: 
          #[V(1, float(golden_ratio)), V(0, 1)], 
          #[V(1, float(golden_ratio)), V(float(golden_ratio), 1)], 
          #[V(1, float(golden_ratio)), V(1, 0)], 
          [V(9, 0), V(0, 9), V(1, 13)], 
          [V(2, 5), V(3, 1)], 
          [V(1, 0), V(2, 0), V(0, 1)], 
          [V(1, 0), V(0, 1)], 
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
          save_ulam_set_image(plot_suffix, init_vectors, n, a1a2)
     ## 
     
##
     
