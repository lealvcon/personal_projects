#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 09:55:47 2019

@author: fac
"""

import numpy as np

class Perceptron:
    """Single perceptron with sigmoidal activation.
    
    attributes: ins, outs, weights, bias, rate, net, out
    """
    
    def __init__(self, inputs, outputs = 1, std=1):
        """Perceptron(inputs)
        
        Perceptron Constructor
        """
        self.ins = inputs
        self.outs = outputs
        self.reset(std)

    def __str__(self):
        return "W = " + self.weights.T.__str__() + ", b = " + self.bias.__str__()
       
    def sigma(self, z):
        return 1 / (1 + np.exp(-z))
    
    def dsigma(self, z):
        s = self.sigma(z)
        return s * (1 - s)
    
    def normalize(self, d):
#        m = d.max(axis=0)
#        return d / m
        return (d - d.mean(axis=0)) / d.std(axis=0)
    
    def prob_from_class(self, c):
        """prob_from_class(c)
        
        This method converts a vector c of integer class
        labels (zero-based) into a (binary) matrix of probabilities
        where the j-th of each row takes the value 1 if the
        corresponding class is j, and zero otherwise."""
        cf = c.flatten().astype(int)
        nc = max(cf) + 1    # number of classes
        p = np.zeros((len(cf), nc))
        for i in range(len(cf)):
            p[i, cf[i]] = 1
        return p
    
    def class_from_prob(self, p):
        """class_from_prob(p)
        
        This method returns a vector of zero-based class labels
        corresponding to the highest entry of each row in the 
        input matrix."""
        return p.argmax(axis = 1).reshape((len(p), 1))
    
    def reset(self, std = 1):
        self.weights = np.random.randn(self.ins, self.outs) * std
        self.bias = np.random.randn(1, self.outs) * std
    
    def calc_output(self, X):
        self.net = X.dot(self.weights) + self.bias
        self.out = self.sigma(self.net)
        #return self.out
    
    def error(self, train_data, train_target):
        self.calc_output(train_data)
        e = self.out - train_target.reshape(train_target.shape[0],1)
        e = e * e
        return 0.5 * e.sum() / len(train_data)
    
    def sgd(self, train_data, train_target):
        for i in range(len(train_data)):
            x = train_data[i].reshape((1,self.ins))
            t = train_target[i].reshape((1,self.outs))
            y = self.calc_output(x)
            self.deltab = self.rate * (t - y) * self.dsigma(self.net)
            self.deltaW = x.T.dot(self.deltab)
            self.weights += self.deltaW
            self.bias += self.deltab
    
    def batch(self, train_data, train_target):
        self.calc_output(train_data)
        self.deltab = self.rate * (train_target - self.out) * self.dsigma(self.net) 
        #self.deltab /= len(train_data)
        self.deltaW = train_data.T.dot(self.deltab)
        self.weights += self.deltaW
        self.bias += self.deltab.sum(axis=0)
    
    def train(self, train_data, train_target, rate, how = 'sgd', eps = 0.00001, maxiter = 100, verbose=False):
        """train(train_data, train_target, rate, how, eps, maxiter, verbose)
        
        Trains the perceptron using the given training data
        
        train_data is an MxN matrix of M data points with N features each
        train_target is a Mx1 vector of target values (assumed to be 0 or 1)
        rate is the learning rate
        how is 'sgd' or 'batch'
        eps is the convergence threshold (defaults to 0.01)
        maxiter is the maximum number of iterations (defaults to 100)
        verbose is a boolean flag which generates verbose output
        """
        self.rate = rate
        how = how.lower()
        old_error = self.error(train_data, train_target)
        E = [old_error]
        epoch = 0
        not_converged = True
        while not_converged:
            if how == 'sgd':
                self.sgd(train_data, train_target)
            else:
                self.batch(train_data, train_target)
            error = self.error(train_data, train_target)
            rel_error = abs(error - old_error) / error
            old_error = error
            epoch += 1
            E.append(error)
            not_converged = (rel_error > eps) and (epoch < maxiter)
            if verbose:
                print("Epoch " + str(epoch) + " - Error = " + str(error)) # + " - Rel. Error = " + (rel_error))
        return E
            
    def test(self, test_data, test_target):
        """test(test_data, test_target)
        
        Test the performance of the perceptron using given test data
        
        test_data is an MxN matrix of M data points with N features each
        test_target is a Mx1 vector of target values (assumed to be 0 or 1)
        
        Returns: number of test data points incorrectly classified
        """
        out = self.calc_output(test_data)
        if self.outs > 1:
            y = self.class_from_prob(out)
        else:
            y = np.zeros(out.shape)
            y[out > 0.5] = 1
        
        return np.sum((y != test_target.reshape((test_target.shape[0],1))))
        