# -*- coding: utf-8 -*-
"""Project_minor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rbebGKx23MO6Fe7VtQgxx91VHAlKVMqn
"""

from sklearn.model_selection import train_test_split
import numpy as np
import os
import PIL
import cv2
import pickle

from zipfile import ZipFile
file_name = "/content/Dataset.zip"

with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  zip.printdir()

import pathlib
DIRECTORY = "/content/Dataset" 
CATEGORIES = ['masked','unmasked']
IMG_SIZE = 64 # IMG_SIZE = 224 alternative size 

X = []
y = []

def create_data():
    for category in CATEGORIES:
        path = DIRECTORY + "/" + category
        class_num_label = CATEGORIES.index(category)
        for img in os.listdir(path):
            try:
              img_array = cv2.imread(path+"/"+img, cv2.IMREAD_GRAYSCALE) #converts image pixel values into an array 
              img_array = cv2.resize(img_array, (IMG_SIZE,IMG_SIZE))
              X.append(img_array)
              y.append(class_num_label)
            except Exeption as e:
              pass           
create_data()

X

SAMPLE_SIZE = len(y)
data = np.array(X).flatten().reshape(SAMPLE_SIZE, IMG_SIZE*IMG_SIZE) # pixel-features

# Turn X and y into numpy arrays
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE) # images
y = np.array(y) # target

print("Features, X shape: ", X.shape)
print("Target, y shape: ", y.shape)
print("Data shape: ", data.shape)

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt # to plot inage, graph
# %matplotlib inline

plt.figure(figsize=(20,10))
columns = 5
for i in range(5):
    plt.subplot(5 / columns + 1, columns, i + 1)
    plt.imshow(X[i],cmap=plt.cm.gray_r,interpolation='nearest')

print('No.of Samples:', len(y))
print('No.of Without A Mask:', (y == 0).sum())
print('No.of With A Mask:', (y == 1).sum())

X=X.reshape(3958,64*64)
X.shape

# Split our data into testing, training and validation.
X_train_new,X_test_new,Y_train_new,Y_test_new=train_test_split(X,y,test_size=0.3,random_state=42)
X_val_new,X_test_new,Y_val_new,Y_test_new=train_test_split(X_test_new,Y_test_new,test_size=0.1/0.3,random_state=42)

"""# **KNN**"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
parameters = {'n_neighbors':[1,3,9,15]}
GS_clf = GridSearchCV(KNeighborsClassifier(), parameters)
GS_clf.fit(X_val_new,Y_val_new)
GS_clf.best_params_

clf_01=KNeighborsClassifier(n_neighbors=1)
clf_01.fit(X_train_new, Y_train_new)

y_pred_01 = clf_01.predict(X_test_new)
accuracy_01 = clf_01.score(X_test_new, Y_test_new)
print("Accuracy %f" % accuracy_01)
metrics.accuracy_score(y_true=Y_test_new, y_pred=y_pred_01)

from sklearn.metrics import classification_report
print(classification_report(Y_test_new,y_pred_01))

from sklearn.model_selection import cross_val_score
scores=cross_val_score(clf_01,X,y,cv=5)
print(scores.mean())

img_ = X_test_new[20]
img_.shape

img_ = np.reshape(img_,(-1,4096))
img_.shape

y_pred = clf_01.predict(img_)

if y_pred==0:
  print("Masked")
else:
  print("Unmasked")

original_index = Y_test_new[20]
if original_index==y_pred:
   print("Correct prediction")
else:
  print("Incorrect prediction")

"""# **SVM**"""

from sklearn import svm
from sklearn import metrics
parameters_00 = {'kernel':['rbf','linear','poly'],'C':[0.001, 0.1, 100, 10e5]}
GS_clf_00 = GridSearchCV(svm.SVC(), parameters_00)
GS_clf_00.fit(X_val_new,Y_val_new)
GS_clf_00.best_params_

model_00 = svm.SVC(C=100,kernel='rbf')
model_00.fit(X_train_new, Y_train_new)

y_pred = model_00.predict(X_test_new)
accuracy = model_00.score(X_test_new, Y_test_new)
print("Accuracy %f" % accuracy)
metrics.accuracy_score(y_true=Y_test_new, y_pred=y_pred)

from sklearn.metrics import classification_report
print(classification_report(Y_test_new,y_pred))

from sklearn.model_selection import cross_val_score
scores=cross_val_score(model_00,X,y,cv=5)
print(scores.mean())

y_pred1 = model_00.predict(img_)

original_index = Y_test_new[20]
if original_index==y_pred1:
   print("Correct prediction")
else:
  print("Incorrect prediction")

"""# **MLP**"""

from sklearn.neural_network import MLPClassifier
parameters_10 = {'solver': ['lbfgs'], 'max_iter': [100,400,700,1000 ], 'alpha': 10.0 ** -np.arange(1, 10), 'hidden_layer_sizes':np.arange(10, 15)}
GS_clf_10 = GridSearchCV(MLPClassifier(), parameters_10)
GS_clf_10.fit(X_val_new,Y_val_new)
GS_clf_10.best_params_

# clf_10=MLPClassifier(alpha=0.0001,hidden_layer_sizes=13,max_iter=1000,solver='lbfgs')
clf_10=MLPClassifier(alpha=0.1,hidden_layer_sizes=12,max_iter=700,solver='lbfgs')
clf_10.fit(X_train_new,Y_train_new)

y_pred_10 = clf_10.predict(X_test_new)
accuracy_10 = clf_10.score(X_test_new, Y_test_new)
print("Accuracy %f" % accuracy_10)
metrics.accuracy_score(y_true=Y_test_new, y_pred=y_pred_10)

from sklearn.metrics import classification_report
print(classification_report(Y_test_new,y_pred_10))

from sklearn.model_selection import cross_val_score
scores=cross_val_score(clf_10,X,y,cv=5)
print(scores.mean())

y_pred2 = clf_10.predict(img_)

original_index = Y_test_new[20]
if original_index==y_pred2:
   print("Correct prediction")
else:
  print("Incorrect prediction")