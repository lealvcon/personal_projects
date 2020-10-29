# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 18:46:33 2019

@author: D3ll
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import perceptron_mod as pm
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
training=data_val[:index,:].copy()
testing=data_val[index:,:].copy()

#layer 1
p11=pm.Perceptron(3,1)
p12=pm.Perceptron(3,1)
p13=pm.Perceptron(3,1)
p14=pm.Perceptron(3,1)
p15=pm.Perceptron(3,1)
layer_1=[p11,p12,p13]
l1=len(layer_1)
#layer 2
p21=pm.Perceptron(l1,1)
#p22=pm.Perceptron(3,1)
layer_2=[p21]
l2=len(layer_2)

training[:,:-1]=p11.normalize(training[:,:-1])
testing[:,:-1]=p11.normalize(testing[:,:-1])


#X must be a column vector
learning_rate=0.9
n=training[:,:-1].shape[1]
E=[]
epochs=1000
w1=layer_1[0].weights.T
b1=layer_1[0].bias
w2=layer_2[0].weights.T
b2=layer_2[0].bias
delta2=[]
sigma= lambda x: 1/(1+np.exp(-x))
dsigma= lambda x: sigma(x)*(1-sigma(x))
for neuron in range(1,l1):
    w1=np.vstack((w1,layer_1[neuron].weights.T))
    b1=np.vstack((b1,layer_1[neuron].bias))
    
for neuron in range(1,l2):
    w2=np.vstack((w2,layer_2[neuron].weights.T))
    b2=np.vstack((b2,layer_2[neuron].bias))
    
def test_nn(x):
    t=x[-1]
    x=x[:-1].reshape((n,1))
    #x=p11.normalize(x)
    net1=w1.dot(x)+b1
    out1=sigma(net1)
    net2=w2.dot(out1)+b2
    out2=sigma(net2)
    if np.float(out2)>.5:
        y=1
    else:
        y=0
    return (y,t)


    

#%% cuadractic error 
    
for epoch in range(epochs):
    error=0
    for item in range(training.shape[0]):
#        print("w1: ", w1)
#        print("b1: ", b1)
#        print("w2 :", w2)
#        print("b2 :", b2 )
#        print("\n")
        x=training[item,:-1].reshape((n,1))
        #x=p11.normalize(x)
        target=training[item,-1]
        net1=w1.dot(x)+b1
        out1=sigma(net1)
        net2=w2.dot(out1)+b2
        out2=sigma(net2)
        e2=target-out2
        error+=e2**2
        delta2=dsigma(net2)*e2
        e1=w2.T.dot(delta2)
        delta1=np.multiply(dsigma(net1),e1)
        #weight and bias update   
        w1=w1+learning_rate*x.dot(delta1.T).T
        b1=b1+learning_rate*delta1
        #for neuron in range(l1):
            #w1[neuron,:]=w1[neuron,:]+learning_rate*np.multiply(delta1[neuron],x).T
            #b1[neuron,:]=b1[neuron,:]+learning_rate*delta1[neuron]
        w2=w2+learning_rate*out1.dot(delta2.T).T
        b2=b2+learning_rate*delta2
        #for neuron in range(l2):
            #w2[neuron,:]=w2[neuron,:]+learning_rate*np.multiply(delta2[neuron],out1).T
            #b2[neuron,:]=b2[neuron,:]+learning_rate*delta2[neuron]
        
    error=error*.5/training.shape[0]
    E.append(np.float(error))
        
plt.figure()
plt.plot(range(epochs),E)

mistakes=0

for i in range(testing.shape[0]):
    (r,t)=test_nn(testing[i,:])
    if r!=t:
        mistakes+=1
        
print("error= %f"%(mistakes/testing.shape[0]))

#%% cross entropy

    
#for epoch in range(epochs):
#    error=0
#    for item in range(training.shape[0]):
##        print("w1: ", w1)
##        print("b1: ", b1)
##        print("w2 :", w2)
##        print("b2 :", b2 )
##        print("\n")
#        #x=training[item,:-1].reshape((n,1))
#        x=p11.normalize(x)
#        target=training[item,-1]
#        net1=w1.dot(x)#+b1
#        out1=sigma(net1)
#        net2=w2.dot(out1)#+b2
#        out2=sigma(net2)
#        e2= target-out2#-(target*np.log(out2)+(1-target)*np.log(1-out2))
#        #error+= -(target*np.log(out2)+(1-target)*np.log(1-out2))
#        delta2=e2
#        e1=w2.T.dot(delta2)
#        delta1=np.multiply(dsigma(net1),e1)
#        for neuron in range(l1):
#            w1[neuron,:]=w1[neuron,:]+learning_rate*np.multiply(delta1[neuron],x).T
#            #b1[neuron,:]=b1[neuron,:]+learning_rate*delta1[neuron]
#        for neuron in range(l2):
#            w2[neuron,:]=w2[neuron,:]+learning_rate*np.multiply(delta2[neuron],out1).T
#            #b2[neuron,:]=b2[neuron,:]+learning_rate*delta2[neuron]
#        
#    #E.append(np.float(error))
#        
##plt.figure()
##plt.plot(range(epochs),E)
#
#for i in range(50):
#    print(test_nn(testing[i,:]))