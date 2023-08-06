def cut_list(list, length):
    """ This function allows to cut a list into parts of a certain length.
        It returns a new list wich takes less memory and contains fo each index a part of the initial list.

        Args :
            list : list of the images path of the whole database\n
            length (int): the length of the parts\n

        Returns :
            list containing the images path cut by parts of <length>

    """

    listing_parts = []
    intervalle_0 = 0
    intervalle_1 = length
    while intervalle_0 <=(len(list)):
        listing_parts.append(list[intervalle_0:intervalle_1])
        intervalle_0 = intervalle_1
        intervalle_1 = intervalle_1 + length
    return listing_parts

def show_face_data(nparray, n=10, title=""):
    """ This function allows to show the faces from a numpy array.

        Args :
            nparray : array containing the images \n
            n (int): the number of images we want to plot (default=10)\n
            title : the title of the plotted faces

        Returns :
            None

    """

    plt.figure(figsize=(30, 5))
    for i in range(n):
        ax = plt.subplot(2,n,i+1)
        plt.imshow(array_to_img(nparray[i]))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.suptitle(title, fontsize = 20)
    plt.show()


if __name__=="__main__" :



    import numpy as np
    import matplotlib.pyplot as plt
    from keras.models import Model
    from keras.layers.core import Dense, Dropout, Activation
    from keras.utils import np_utils
    import keras
    import tensorflow as tf
    from keras.preprocessing.image import img_to_array
    from keras.preprocessing.image import array_to_img
    from multiprocessing import Pool
    import os
    from PIL import Image
    from matplotlib import image
    from keras.datasets import mnist
    from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Conv2DTranspose, Reshape
    from keras import layers

    # PART 1
    # In this code, we need to work with numpys. To do so, we need to convert our database
    # To an numpy array.
    # UPLOAD THE PATH OF THE DATABASE:
    data_path="../database/img_align_celeba/img_align_celeba"
    listing = os.listdir(data_path)
    #print(listing) #returns a list of all the files of the path
    listarray = [] # creating the array list that will contain the information of our images

    #cut_list was originally here


    # we choose first to work with only 500 images.
    listing_parts=cut_list(listing,500)
    print(len(listing_parts))

    #Once we have uploaded all our images, we resize our images and fit them in numpy array
    from skimage.transform import resize
    for file in listing_parts[0]:
            if file == file + '.DS_Store':
                continue
            chemin= "../database/img_align_celeba/img_align_celeba/" + file
            im = image.imread(chemin)
            resized_img = resize(im,(128,128))
            listarray.append(resized_img)
    print(np.shape(resized_img))
    nparray = np.array(listarray)

    #######################################################################################################

    # PART 2:  THE ENCODER
    #we construct our encoder :
    from sklearn.model_selection import train_test_split
    X_train, X_test = train_test_split(nparray, test_size=0.2, random_state=0)


    input_img = keras.Input(shape=(128, 128, 3))
    # x = layers.Conv2D(8, (3, 3), activation='relu', padding='same')(input_img)
    # x = layers.MaxPooling2D((2, 2), padding='same')(x)
    # x = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    # x = layers.MaxPooling2D((2, 2), padding='same')(x)
    # x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    # x = layers.MaxPooling2D((2, 2), padding='same')(x)
    # x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    # x=  layers.MaxPooling2D((2, 2), padding='same')(x)
    # x=  layers.Flatten()(x)
    # encoded=  layers.Dense(1000, activation='relu', name="CODE")(x)
    #
    # ########################################################################################################
    #
    # # PART 3:  THE DECODER
    # x=layers.Dense(4096,activation='relu')(encoded)
    # x=layers.Reshape((8,8,64))(x)
    # x = layers.UpSampling2D((2, 2))(x)
    # x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    # x = layers.UpSampling2D((2, 2))(x)
    # x = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    # x = layers.UpSampling2D((2, 2))(x)
    # x = layers.Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    # x = layers.UpSampling2D((2, 2))(x)

    x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2))(x)
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    x =  MaxPooling2D((2, 2))(x)
    encoded = layers.Flatten(name="CODE")(x)

    #encoded = layers.Dense(1000, activation='relu', name="CODE")(x)


    #x=layers.Dense(2048,activation='relu')(encoded)
    x = layers.Reshape((16,16,8))(encoded)
    x = Conv2DTranspose(8, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2DTranspose(16, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2DTranspose(32, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2,2))(x)


    decoded = layers.Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    autoencoder = keras.Model(input_img, decoded)
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy', metrics=["accuracy"])
    autoencoder.summary()

    # We train the encoder
    history=autoencoder.fit(X_train, X_train, epochs=150, batch_size=32, shuffle=True, validation_data=(X_test, X_test))

    # We create the decoder model
    Decodeur = Model(encoded, decoded)
    Decodeur.compile(optimizer='adam', loss='mse')
    Decodeur.save("decodeur.h5")

    #######################################################################################################


    #PART 4: THE VECTOR
    # We need now to obtain the encoded vector that will be used for the genetic algorithms part:

    get_encoded_X = Model(inputs=autoencoder.input, outputs=autoencoder.get_layer("CODE").output)
    get_encoded_X.compile(optimizer='adam', loss='mse')
    get_encoded_X.save("encodeur.h5")
    encoded = get_encoded_X.predict(X_test)
    print(len(X_test))
    print(np.shape(encoded))
    #encoded = encoded.reshape(100,100)
    reconstructed = autoencoder.predict(X_test)

    np.save("model/vecteur.npy", encoded) # THE ENCODED VECTOR IS HERE, A npy file is given. to use it for the genetic algorithm
    # you need to reupload it ;)


    #######################################################################################################

    # PART 5: PLOTTING THE PICTURES

    #show_face_data was originally here


    show_face_data(X_test, title="original faces")
    show_face_data(reconstructed, title="reconstructed faces")



    ########################################################################################################

    # PART 6 : PLOTTING MODEL ACCURACY AND loss

    # summarize model for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
