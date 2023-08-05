# Project_4bim

## Table of Contents
1. [Software Description ](#software-description)
2. [Repository Organization](#repository-information)
3. [Methodologies Description](#methodologies_desciption)
4. [Tutoriel](#tutoriel)
5. [Installation](#technologies)
6. [Technologies](#installation)
7. [Limits and Improvements](#limits-and-improvements)
8. [Collaboration](#collaboration)
9. [FAQs](#faqs)

### Software Description
***
This software creates a synthesized portrait with facial features that resemble as close as possible to a criminal. The creation of the portrait is made based on a witness's successive choices between different propositions taken from a large-scale face attributes dataset. These choices are used by the software to identify the most likely facial characteristics in order to select and propose an image that corresponds to the witness's expectations and hopefully to the actual criminal. 

The software contains a user friendly Graphical User Interface and the algorithms used to propose a final portrait include a Neural Network Algorithm, that will reduce the size of the dataset images and a Genetic Algorithm that will combine and modify the image selected by the witness and propose new image.

### Repository Organization
*** 
The folder projet contains all the folders that define the software structure. This folder projet contains the main python file that defines the software execution. It also contains :
- in the clusters folder, all numpy and csv files needed for the genetic algorithm and neural network algorithm. 
- in the decoders folder, all decoder files .h5 needed for the photo decoding in the main. 
- in the selectionimage, son, father, choice and final_choice folders, all photos saved during the main execution.
- in  build/html/index.html, a link that takes to an index where you can easily find all the function's docstrings. 

The folder Tutoriel contains two jupyther notebooks that can help you train with the Genetic Algorithm and the Neural Network Algorithm. 

### Methodologies Description
Our project is based on 3 methodologies.

1.  *Neural Network*

A Neural Network Algorithm is used to reduce the size of all the dataset images for the software to modify them faster. It contains an encoder that compresses the images and a decoder that decompresses them later in order to display them.

The database used to create the software has more than 200,000 photos. With the aim of not having to train our Neural Network model on all the dataset every time the software was run, we decided to create 8 clusters of the dataset based on all the possible combinations of 3 attributes (Hairstyle, Gender and Age) that we consider reduced significantly the size of the database. Each cluster has a specific encoder and decoder and all these files needed for the Neural Network to run were created in advance. The only image kept in memory at run time are the ones that are being displayed.

2. *Genetic Algorithm*

A Genetic algorithm is used to generate a high-quality solution to the search of the criminal's face by the witness. It relies on two biological inspired operators: a mutation and a crossover. The idea is to include the witness's successive photo choices and use that information to generate new photos that contain some of the traits selected.


3. *Graphical User Interface*

In order to present a user friendly software, a Graphical User Interface was created with buttons that allow the witness to select different photos, stop and restart the program. It also displays all the photos selected in the previous steps of the software.

### Technologies
***
A list of technologies used within the project:
* [python3](https://www.python.org/downloads/): Version 3.7.3
* [Library keras](https://keras.io/about/): Version 2.8.0
* [Library tensorflow](https://www.tensorflow.org/api_docs/python/tf): Version 2.8.0
* [Library cv2](https://pypi.org/project/opencv-python/):Version 4.3.0
  $ pip3 install opencv-python
* [Library scikit-image](https://scikit-image.org/):Version 0.19.2
  $ pip3 install scikit-image
* [Large-scale CelebFaces Attributes (CelebA) Dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)

### Installation
***
To use the application you need a python environnement and you have to verify the versions of python and modules.
In addition to use the following instructions you need a linux terminal.  
```
$ git clone https://example.com
$ cd ../path/to/the/file
$ pip3 install keras
$ python3 mainGUI.py
Then follow the intructions of the graphic interface.
```
### Collaboration
***
You can download the project on github but you can't collaborate directly on the project (it is private).

### Tutoriel 
***
First, select an initial set of physical traits for the search. Click on the options and then click on next. 
<p align="center">
<img src="images_tutorial/1.png" alt="1" width="400"/>
</p>

Then, 9 photos that correspond to the initial selected traits will be displayed. Select 4 of them and click on next.
<p align="center">
<img src="images_tutorial/2.png" alt="1" width="400"/>
</p>

Then, 6 new created photos will be displayed. In the top right part of the window you can check your previous selected photos. 
You have two possibilities: 

1. Select one photo from the left buttom and 3 from the right side

or

2. Select 4 photos from the right side

Note that at anytime you can restart the software by clicking on restart.
<p align="center">
<img src="images_tutorial/3.png" alt="1" width="400"/>
</p> 

All your choices will be displayed on the bottom left side of the window. 
<p align="center">
<img src="images_tutorial/4.png" alt="1" width="400"/>
</p>
When you think you've found the best portrait, click on the I found suspect and then select the corresponding image. 
<p align="center">
<img src="images_tutorial/5.png" alt="1" width="400"/>
</p>
Finally, confirm your choice by clicking yes. 

### Limits and Improvements

1. The software doesn't have a maximum number of iterations and there is no convergence criteria.  
2. The software has no Home Page that presents the context in which the program can be used. 
3. The quality of the images could definitely be improved by changing the database or the using additional programming languages. 
4. The graphical interface buttons don't change color when they are selected, implementing this feature could make the program more user interactive. 


## FAQs
***
A list of frequently asked questions
1. **Are the images created during the previous executions saved in a folder?**
The images created during previous executions are kept in memory until a new execution is done. A final portrait is kept in a folder until a new exeution's final portrait is chosen. 


