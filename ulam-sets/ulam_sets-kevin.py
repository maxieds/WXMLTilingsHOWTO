from sage.all import *


def new_membership_test(old_ulam, candidate):
    """
    Return True if and only if the candidate is not in old_ulam and can be
    written uniquely as the binary sum of elements in old_ulam
    """
    if candidate in old_ulam:
        return False
    count = 0
    for v in old_ulam:
        if (candidate - v) in old_ulam:
            count += 1
            if count == 3:
                return False
    if count == 2:
        return True
    else:
        return False


def max_norm(v):
    return v.norm(p=infinity)


def candidates_max_norm(m):
    """
    Return a list of vectors of length m.
    """
    candidates = [vector([m, i]) for i in range(1, m+1)]
    candidates += [vector([i, m]) for i in range(1, m)]

    return candidates


def compute_ulam(n, init_vectors, norm_func=max_norm):
    """
    Return a set containing at least the first n ulam elements. This only works
    for the max norm for now with initial vectors [1,0] and [0,1]. The code
    should generalize though.

    INPUT:
    - ``n`` - the number of ulam elements to be returned

    - ``init_vectors`` - a list containing the initial vectors

    - ``norm_func`` - a function that takes a vector and outputs the desired
    norm

    """
    init_vectors = [vector(v) for v in init_vectors]
    ulam_set = init_vectors

    while len(ulam_set) < n:
        # m be the length of the largest vector found so far
        m = norm_func(ulam_set[-1])

        new_elements = []
        while not new_elements:
            # candidates is the set of vectors of length m that can be written
            # as a positive integral combination of the initial vectors.
            candidates = candidates_max_norm(m)

            # filter candidates that passed
            new_elements = [v for v in candidates
                            if new_membership_test(ulam_set, v)]

            # increase m if we can't find any at level m
            if not new_elements:
                m += 1

        ulam_set += new_elements

    return ulam_set


def main():
    init_vectors = [[1, 0], [0, 1]]
    # compute_ulam(100, init_vectors)
    print(compute_ulam(100, init_vectors))


if __name__ == "__main__":
    main()
