 # encoding:utf-8

# sklearn的SVC 能够实现多分类算法
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from data_parser import DataParser
import numpy as np
import random
import copy
import os


class SVMClassifier:
    def __init__(self, standardize=True):
        self.standardize = standardize
        self.non_zero_params = []

    def train(self, data, labels):
        # learn model for individual flows
        data = np.array(data)
        # RBF, Linear, Poly, Sigmoid
        print "svm train begin"
        self.svm = SVC(kernel='rbf',verbose=1)
        # self.svm = LinearSVC(penalty='l2')
        self.svm.fit(data, labels)

        print "svm train end"
    # test function for individual flow
    def test(self, data, labels=None):

        out = list(self.svm.predict_proba(data))
        # print "out:",out
        if labels == None:
            return out, None, None
        TP = TN = FP = FN = 0
        for i in range(len(out)):
            if self.get_label(out[i]) == labels[i]:
                if labels[i]==1:
                    TP+=1
                else:
                    TN+=1
            else:
                if self.get_label(out[i])==1:
                    FP+=1
                else:
                     FN+=1
        return  TP, TN, FP, FN


    def get_label(self, probs):
       a=[-1,1]
       for i, j in enumerate(probs):
           if j == np.amax(probs):
              return a[i]


