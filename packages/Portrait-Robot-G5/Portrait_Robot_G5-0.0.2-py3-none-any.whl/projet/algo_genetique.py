import numpy as np
import pandas as pd
import random
import common_functions as cf
from itertools import combinations

def crossover_pixels(parents):
    """
    Function that crosses the vectors corresponding to encoded photos, from n parents to make an offspring.
    For all possible combinations of two parents, we create the offspring by computing the mean between each element of the parents vectors.
    
    Args :
        parents (list(np.array)) : list of np.array representing the reduced pixel matrix (a simple vector) of the parents we will use for the crossover
    Returns :
        offsprings (list(np.array)) : offspring of the given previous generation

    >>> encoded_imgs_test = np.load('clusters/encoded_imgs_test.npy')
    >>> offsprings = crossover_pixels(encoded_imgs_test)
    >>> offsprings[0][:10]
    [0.3932449519634247, 0.0, 1.1216704845428467, 1.4052040576934814, 0.228857159614563, 0.0, 1.2136073112487793, 1.3344969749450684, 0.0, 0.0]
    """

    index_parents = list(range(0,len(parents)))
    p_combinations = list(combinations(index_parents,2))
    offsprings = []
    for i in range(len(p_combinations)):
        #Goes through every possible combinations between the parents (without taking care of the order) 
        parent_1 = (parents[p_combinations[i][0]]).tolist()
        parent_2 = (parents[p_combinations[i][1]]).tolist()
        offsprings_temp=[]
        for j in range(len(parent_1)) :
            #Goes trough every element of the vector (encoded photo) and computes the mean to create offspring
            offsprings_temp.append((parent_1[j]+parent_2[j])/2)
        offsprings.append(offsprings_temp)
    while(len(offsprings))<13:
        offsprings.append(offsprings[2])
    return offsprings

def mutation_pixels():
    """
    Function that mutates a parent by replacing it by another encoded photo from the same cluster.

    Args :
    Returns :
        mutated_parent (np.array) : new array representing an encoded photo, ready to be decoded and displayed

    >>> encoded_imgs_test = np.load('clusters/encoded_imgs_test.npy')
    >>> random.seed(4)
    >>> new_parents = mutation_pixels()
    >>> print(new_parents[:10])
    [0.33924556 0.5726387  0.7653752  0.12993433 1.230257   0.
     0.20445274 0.03274947 0.2659498  0.5143205 ]
    """
    parentbase = np.load("clusters/encoded.npy")
    p = random.choice(range(len(parentbase)))
    return parentbase[p]

#################
#TESTS UNITAIRES#
#################

if __name__ == "__main__" :
    import doctest
    doctest.testmod(verbose = True)
