import numpy as np
import pandas as pd
import random
from itertools import combinations


def convert_attributes_into_pandas(filename):
    """
    Converts a csv file to a pandas.array matrix. The matrix contains all attributes as columns, and each photo ID and their corresponding attributes values in rows.
    Function used to build the clusters of photos.

    Args :
        filename (str) : path to csv file

    Returns :
        df_attributes (pandas.array) :  matrix of attributes that will be reduced to choose photos

    >>> type(convert_attributes_into_pandas("clusters/test_attributes.csv"))
    <class 'pandas.core.frame.DataFrame'>

    """
    return pd.read_csv(filename)

def matrix_reduction(df,fixed_att):
    """
    Reduces the matrix based on the traits specified by the witness and deletes all columns corresponding to the specified traits. The function returns a list of all the chosen photos id's as strings.
    Function used to build the clusters of photos.

    Args :
        df (pandas.array) : attributes matrix to reduce
        fixed_att (dict) : attributes that have been selected by witness to reduce our matrixby columns

    Returns :
        list_names : return a list of strings with all the ids from the photos that containe the fixed_att attributes

    >>> df_test = convert_attributes_into_pandas("clusters/test_attributes.csv")
    >>> fixed_attributes_test = {"Pale_Skin":-1,"Young":1,"Male":1,"Attractive":1,"Bags_Under_Eyes":1}
    >>> df_test_list = matrix_reduction(df_test,fixed_attributes_test)
    >>> matrix_reduction(df_test,fixed_attributes_test)
    ['000006', '000011', '000037', '000075', '000079', '000081']

    """
    new_df = df
    attributes = list(fixed_att.keys())
    values = list(fixed_att.values())
    for i in range(len(attributes)):
        new_df.drop(df.index[df[attributes[i]]!= values[i]],inplace=True)
    list_index = new_df.index.tolist()
    int_index=list(map(int,list_index))
    for index in int_index :
        index+=1
    list_index=list(map(str,int_index))
    new_list_index = []
    for i in range(len(list_index)):
        new_list_index.append(list_index[i])
        if len(new_list_index[i]) ==1:
            new_list_index[i] = '00000' + new_list_index[i]
        if len(new_list_index[i]) ==2:
            new_list_index[i] = '0000' + new_list_index[i]
        if len(new_list_index[i]) ==3:
            new_list_index[i] = '000' + new_list_index[i]
        if len(new_list_index[i]) ==4:
            new_list_index[i] = '00' + new_list_index[i]
        if len(new_list_index[i]) ==5:
            new_list_index[i] = '0' + new_list_index[i]
    return new_list_index

#################
#TESTS UNITAIRES#
#################

if __name__ == "__main__" :
    import doctest
    doctest.testmod(verbose = True)
