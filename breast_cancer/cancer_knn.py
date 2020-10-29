# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:19:56 2019

@author: D3ll
"""

""" cancer project using K Nearest Neighbors """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import perceptron_mod as pm
import math

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

data=pd.read_csv("wdbc.data",header=None)
d=data.values
target=((d[:,1]=="M")*1).reshape((len(d),1))
d=d[:,3:13].astype(float)

d=np.hstack((d,target))
benign=d[d[:,-1]==0,:-1]
malign=d[d[:,-1]==1,:-1]

plt.figure()
ax.scatter(malign[:,1],malign[:,3],malign[:,4],c="red") # best texture area smoothness
ax.scatter(benign[:,1],benign[:,3],benign[:,4],c="blue")
plt.show()

d=d[:,[1,3,4,-1]]

ptrain=.6
i=d.shape[0]
index=math.floor(i*ptrain)
data_val=np.random.permutation(d)
training=data_val[:index,:]
testing=data_val[index:,:]


def knn(x,k):
    assigned_types=[]
    target=x[-1]
    x=x[:-1].reshape((1,len(x)-1))
    dist=np.sum((training[:,:-1]-x)**2,axis=1)
    ind=np.argsort(dist)
    dist=dist[ind[:k]]
    neighbors=training[ind[:k],:]
    types=list(set(neighbors[:,-1]))
    n_type=[]
    for t in types:
        n_type.append(np.sum((neighbors[:,-1]==t)*1))
        
    assigned_types.append(types[np.argmax(n_type)])
    assigned_types=np.array(assigned_types)
    assigned_types=np.resize(assigned_types,(len(assigned_types),1))
    x=np.hstack((x,assigned_types)) #ultima columna idica resultado de knn
    return (np.float(x[:,-1]),target)
    

error=[]
for n in range(3,50,2):
    mistakes=0
    correct=0 
    false_neg=0 
    false_pos=0 
    for item in range(testing.shape[0]):
        res=knn(testing[item,:],n)
        if res[0]==res[1]:
            correct+=1
        elif res[0]-res[1] < 0:
            false_neg+=1
        else:
            false_pos+=1
        mistakes+= (res[0]-res[1])**2
    error.append(mistakes)

n=np.argsort(error)[0]
print(mistakes," mistakes out of ", testing.shape[0],"\n")
print(false_neg, "were classified as false negatives \n")
print("and ", false_pos, "as false positives.")
