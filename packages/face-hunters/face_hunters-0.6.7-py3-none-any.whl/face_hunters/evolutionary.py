#before the initial sample
import numpy as np                   # advanced math library
import matplotlib.pyplot as plt      # plotting routines
import random
#import tensorflow as tf
#from tensorflow import keras
#import h5py
import os
#import cv2
from PIL import Image
import scipy.misc

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# UPLOAD THE DECODER :
from keras.models import load_model

sample_size=10
##

import doctest
doctest.testmod(verbose=True)


def cross_over(pop, parent, lamb):
    """ This function allows to cross-over the selected parent with random other images with the same characteristics (sex, age and hair/beard wise).
        It returns a new population of mutated vectors while keeping the parent.

        Args :
            pop : encoded images vector of the whole database\n
            parent: the array selected by the user\n
            lamb (int): the size of the total population (children + parent)

        Returns :
            array containing lamb vectors from encoded pictures

        Example :
            >>> len(cross_over(population, population[0], 4))
            4
            >>> population[0] in cross-over(population,population[0], 4)
            True
    """

    n_children = lamb -1
    N = len(pop)
    cross_index = np.random.choice(range(N), n_children)    # sélectionne 3 index au hasard dans notre base de données
    #print(cross_index)
    crossed = [parent]
    for i in cross_index:
        child=[]
        for j in range (len(parent)):
            child.append(np.average([parent[j],pop[i][j]], weights=[0.4,0.6])) # on fait la moyenne pour chaque attribut entre le vecteur parent et le vecteur choisi aléatoirement
        crossed.append(child)
    return np.asarray(crossed)


def mutation(pop):
    """ This function allows to mutate the picture's attributes using Gaussian distribution.
        It returns a new population of mutated vectors.

        Args :
            pop : encoded images vector to mute

        Returns :
            nparray containing modified vectors from encoded pictures

    """
    std=pop.std(axis=0)
    N = len(pop)
    for i in range(1,len(pop)):
        random_value=np.random.normal(0,1)  #pour chaque enfant on choisi alpha
        for j in range(1,len(pop[i])):
            pop[i][j]+=random_value*std[i]
    return pop


def get_children_from_parent(pop, parent, lamb):
    """ This function allows to cross-over the parent pictures with other pictures and mutate the result picture to add diversity.
        It returns a new population of mutated vectors.

        Args :
            pop : encoded images vector of the whole database\n
            parent: the array selected by the user\n
            lamb (int): the size of the total population (children + parent)

        Returns :
            array containing lamb vectors from encoded pictures
    """
    children=cross_over(pop, parent, lamb)
    mutated_children=mutation(children)
    return mutated_children




if __name__=="__main__":



    #import doctest
    #doctest.testmod(verbose=True)


    decoder = load_model("decodeur.h5")
    encoded_imgs=np.load("img_female_old_straight.csv.npy")



## Crossing cross_over
    children=cross_over(encoded_imgs, encoded_imgs[50], 4)
    children_decoded = decoder.predict(children)
    for i in range (len(children)):
        ax = plt.subplot(1, len(children), i + 1 )
        plt.imshow(children_decoded[i].reshape(128,128,3))
    plt.show()


## Mutation

    mutated_children=mutation(children)
    children_decoded2 = decoder.predict(mutated_children)
    for i in range (len(children)):
        ax = plt.subplot(1, len(children), i + 1 )
        plt.imshow(children_decoded2[i].reshape(128,128,3))
        plt.title("Mutated")
    plt.show()

## Generate new population

    x=get_children_from_parent(encoded_imgs, encoded_imgs[134], 4)
    decoded_x=decoder.predict(x)
    for i in range (len(x)):
        ax = plt.subplot(1, len(x), i + 1 )
        plt.imshow(decoded_x[i].reshape(128,128,3))
    plt.show()
