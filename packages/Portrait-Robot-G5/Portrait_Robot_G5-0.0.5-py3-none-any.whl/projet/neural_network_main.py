import numpy as np
import pandas as pd
import random
import common_functions as cf
import sys
from matplotlib import image
from matplotlib import pyplot
from PIL.Image import *
import glob
from skimage import io, transform
import skimage
from tensorflow import keras
from sklearn.model_selection import train_test_split
import neural_network_function as nn

if __name__ == "__main__" :

    # Clusters:
    # att_cluster1 = {"Male":-1,"Straight_Hair":-1,"Young":-1}
    #att_cluster2= {"Male":-1,"Straight_Hair":-1,"Young":1}
    att_cluster3 = {"Male":-1,"Straight_Hair":1,"Young":1}
    # att_cluster4 = {"Male":1,"Straight_Hair":1,"Young":-1}
    # att_cluster5 = {"Male":1,"Straight_Hair":-1,"Young":1}
    # att_cluster6 = {"Male":1,"Straight_Hair":-1,"Young":-1}
    # att_cluster7 = {"Male":-1,"Straight_Hair":1,"Young":-1}
    # att_cluster8 = {"Male":1,"Straight_Hair":1,"Young":1}


    df_attributes = cf.convert_attributes_into_pandas("attributes_data.csv")

    # index_cluster1 =cf.matrix_reduction(df_attributes,att_cluster1)
    #index_cluster2 =cf.matrix_reduction(df_attributes,att_cluster2)
    index_cluster3 =cf.matrix_reduction(df_attributes,att_cluster3)
    # index_cluster4 =cf.matrix_reduction(df_attributes,att_cluster4)
    # index_cluster5 =cf.matrix_reduction(df_attributes,att_cluster5)
    # index_cluster6 =cf.matrix_reduction(df_attributes,att_cluster6)
    # index_cluster7 =cf.matrix_reduction(df_attributes,att_cluster7)
    # index_cluster8 =cf.matrix_reduction(df_attributes,att_cluster8)


    #Upload pictures with cluster1
    images=[]
    for k in range(700):
        images.append(glob.glob("/media/cloisel/SAMSUNG/projet4BIM/img_align_celeba/"+index_cluster3[k]+".jpg")[0])
    i=0
    n=len(images)
    img=[None]*n
    image_size=(128,128)
    for image_ in images:
        picture = pyplot.imread(image_)
        img[i] = transform.resize(picture, image_size)
        i+=1
    dataset=[None]*n
    for j in range(n):
        dataset[j]=np.reshape(np.asarray(img[j]),(128*128*3))
    data=np.array(dataset)
    X=data[0:700]

    #Upload attributs
    y = cf.convert_attributes_into_pandas("attributes_data.csv")
    y = y.drop('ID', axis=1)
    y = y.to_numpy()
    y=y[0:700]

    #Suppression of useless variables
    del images
    del index_cluster3
    del att_cluster3
    del dataset

    # Split the dataset
    (X_train_, X_test_, y_train_, y_test_) = nn.split_dataset(X, y)

    # Creation model
    (encoder_, decoder_, autoencoder_) = nn.model()

    # Compile the model
    autoencoder_.compile(optimizer='adam', loss='binary_crossentropy')

    # Resize X_train and X_test
    X_train = X_train_.reshape(-3,128,128,3)
    X_test = X_test_.reshape(-3,128,128,3)

    # Fit the model
    autoencoder.fit(X_train, X_train,
                    epochs=100,  #100
                    batch_size=1,  #32
                    shuffle=True,
                    validation_data=(X_test, X_test))

    # Plot reconstruction
    encoded_imgs = encoder_.predict(X.reshape(-3,128,128,3))
    decoded_imgs = decoder_.predict(encoded_imgs)
    nn.save_reconstruction(1, decoded_imgs)

    # save model
    np.save('encoded_imgs3', encoded_imgs)
    decoder_.save('decoder3.h5')

    # Plot the learning curve to test the model
    nn.loss_test(autoencoder_)
