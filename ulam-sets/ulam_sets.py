from sys import argv


def infinity_norm(v):
    return max(abs(v[0]), abs(v[1]))


def two_norm_squared(v):
    return v[0]**2 + v[1]**2


def vector_sum(v, w):
    return (v[0]+w[0], v[1]+w[1])


def compute_ulam_set(n, init_vectors=[(1, 0), (0, 1)], norm=infinity_norm):
    # ulam_set is the set of all ulam elements found so far
    ulam_set = set(init_vectors)
    old_ulam_set = ulam_set.copy()

    # new_ulam is the set of all ulam elements found in the latest iteration
    new_ulam = set(init_vectors)

    # pairwise sums is the set of all pairwise sums of all ulam elements found
    # so far that are not already in ulam_set
    pairwise_sums = set([])
    unique_counts = dict()

    for nidx in range(n):
        # update pairwise sums by computing pairwise sums between new_ulam
        # elements and ulam_set elements and substracting ulam_set
        new_sums = [vector_sum(x, y) for x in old_ulam_set for y in new_ulam
                    if x != y]
        new_ulam = list(new_ulam)
        for (xidx, x) in enumerate(new_ulam): 
             for yidx in range(xidx + 1, len(new_ulam)): 
                  y = new_ulam[yidx]
                  new_sums += [vector_sum(x, y)]
             ##
        ##
        for nsum in new_sums: 
             if nsum in unique_counts and nidx > 0:
                  unique_counts[nsum] += 1
             else: 
                  unique_counts[nsum] = 1
        ##
        pairwise_sums = pairwise_sums.union(set(new_sums))
        pairwise_sums = pairwise_sums.difference(ulam_set)

        # remove elements that are not uniquely represented: 
        pairwise_sums_temp = pairwise_sums.copy()
        for v in pairwise_sums: 
             if unique_counts[v] > 1: 
                  pairwise_sums_temp.remove(v)
        ##
        pairwise_sums = pairwise_sums_temp

        # update new_ulam to be the set of pairwise sums of smallest norm
        smallest_norm = min([norm(x) for x in pairwise_sums])
        new_ulam = set([x for x in pairwise_sums if norm(x) == smallest_norm])
        
        # update ulam_set to include new_ulam
        old_ulam_set = ulam_set.copy()
        ulam_set = ulam_set.union(new_ulam)

    return ulam_set

try:
    m = int(argv[1])
except:
    m = 10
#ulam = compute_ulam_set(m)
# print(ulam)
#print(len(ulam))
