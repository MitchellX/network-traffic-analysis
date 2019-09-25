 # encoding:utf-8

from sklearn import linear_model, preprocessing, svm, neighbors
from operator import itemgetter
from data_parser import DataParser
import numpy as np
import random
import copy
import os


class KNNClassifier:
    def __init__(self, standardize=True, C=1e5):
        self.standardize = standardize
        self.non_zero_params = []

    def train(self, data, labels):
        # learn model for individual flows
        data = np.array(data)
        self.knn = neighbors.KNeighborsClassifier(1)
        self.knn.fit(data, labels)

    # test function for individual flow
    def test(self, data, labels=None):

        out = list(self.knn.predict(data))
        # predict_data假设有m个数据分了n类，那么会生成一个m×n的数组，其中n个数据代表这个数据是第n类的概率
        # print "out:",out
        if labels == None:
            return out, None, None
        TP = TN = FP = FN = 0
        for i in range(len(out)):
            if out[i] == labels[i]:
                if out[i]==1:
                    TP+=1
                else:
                    TN+=1
            else:
                if out[i]==1:
                    FP+=1
                else:
                     FN+=1

        return TP, TN, FP, FN

    def get_label(self, probs):
       a=[-1,1]
       for i, j in enumerate(probs):
           if j == np.amax(probs):
              return a[i]



