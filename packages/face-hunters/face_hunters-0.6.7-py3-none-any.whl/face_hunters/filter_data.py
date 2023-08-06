import pandas as pds
import numpy as np
import csv
from matplotlib import image
from skimage.transform import resize
import os

def filter(path):
    """
    This function creates 8 files containing different pictures sorted according specific attributes.

    Args :
        path : path to the database

    Returns :
        None

    """

    db = pds.read_csv(path, sep=",") # load a pandas dataframe from csv in current directory
    #print(db.head())
    #print(db.shape)

    #sorting male/female
    db_male=db.loc[db['Male']==1]
    db_female=db.loc[db['Male']==-1]


    #sorting young/old

    db_male_young=db_male.loc[db['Young']==1]
    db_male_old=db_male.loc[db['Young']==-1]
    #print("Liste des hommes jeunes :",db_male_young)

    db_female_young=db_female.loc[db['Young']==1]
    db_female_old=db_female.loc[db['Young']==-1]
    #print("Liste des femmes jeunes :", db_female_young)

    #sorting beard/no beard

    db_male_young_nobeard=db_male_young.loc[db['No_Beard']==1]
    # Enregister notre structure de données dans un fichier.csv
    db_male_young_nobeard.to_csv('male_young_nobeard.csv',mode='w+')
    db_male_young_beard=db_male_young.loc[db['No_Beard']==-1]
    db_male_young_beard.to_csv('male_young_beard.csv',mode='w+')

    db_male_old_nobeard=db_male_old.loc[db['No_Beard']==1]
    db_male_old_nobeard.to_csv('male_old_nobeard.csv',mode='w+')
    db_male_old_beard=db_male_old.loc[db['No_Beard']==-1]
    db_male_old_beard.to_csv('male_old_beard.csv',mode='w+')

    #print("Liste des hommes jeunes avec barbe :", db_male_young_beard)
    #print("Liste des hommes vieux sans barbe :", db_male_old_nobeard)

    #sorting wavy/straight hair

    db_female_young_wavy=db_female_young.loc[db['Straight_Hair']==-1]
    db_female_young_wavy.to_csv('female_young_wavy.csv',mode='w+')
    db_female_young_straight=db_female_young.loc[db['Straight_Hair']==1]
    db_female_young_straight.to_csv('female_young_straight.csv',mode='w+')

    db_female_old_wavy=db_female_old.loc[db['Straight_Hair']==-1]
    db_female_old_wavy.to_csv('female_old_wavy.csv',mode='w+')
    db_female_old_straight=db_female_old.loc[db['Straight_Hair']==1]
    db_female_old_straight.to_csv('female_old_straight.csv',mode='w+')

    #print("Liste des femmes jeunes avec straight :", db_female_young_straight)
    #print("Liste des femmes jeunes sans straight :", db_female_young_wavy)
    #print("Liste des femmes vieilles sans straight :", db_female_old_wavy)


def split_encoded_images(encoder, csv_file):

    """
    This function creates a file containing encoded vectors of images with the same caracteristics.

    Args :
        encoder : encoder loaded from file "encodeur.h5"
        csv_file : path to the csv file containing the listed pictures with the same caracteristics

    Returns :
        None

    """

    f=open(csv_file)
    csv_f = csv.reader(f)
    list_ref=[]

    for row in csv_f:
        ref=row[1]
        #print(ref)
        list_ref.append(ref)

    original_images=[]
    data_path="../database/img_align_celeba/img_align_celeba/"
    for file in list_ref[1:1001]:
            chemin= data_path+file
            im = image.imread(chemin)
            resized_img = resize(im,(128,128))
            original_images.append(resized_img)
    #print(np.shape(resized_img))
    nparray = np.array(original_images)

    #encode images and save them in a file :
    encoded_images = encoder.predict(nparray)
    np.save("images/img_"+str(csv_file[10:])+".npy", encoded_images)


#modif

if __name__=="__main__" :
    # UPLOAD THE DECODER :
    from keras.models import load_model
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    #decodeur=np.save(".../decodeur.h5",x[0])
    encoder = load_model("model/encodeur.h5")

    #filter('databases/list_attr_celeba.csv')
    #db = pds.read_csv('female_young_wavy.csv', sep=",")
    #print(db["image_id"][0])




    split_encoded_images(encoder, "databases/female_old_wavy.csv")
    vecteur=np.load("images/img_female_old_wavy.csv.npy")
    print(len(vecteur))
    print(len(vecteur[0]))
