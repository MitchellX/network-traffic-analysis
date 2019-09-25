from __future__ import division,print_function,absolute_import

import tensorflow as tf
import numpy as np
import random
import sklearn.preprocessing as prep
from pull_data import Pull
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.svm import LinearSVC

import argparse
parser = argparse.ArgumentParser(description="Generate Model Parameters for analysis",add_help = True)
parser.add_argument('-p', '--pos_dir', action = "store", help="Directory of Positive Example(JSON Format)")
parser.add_argument('-n', '--neg_dir', action="store", help="Directory of Negtive Example (JSON Format)")
parser.add_argument('-m', '--meta', action="store_true", default=False, help="Parse Metadata Information")
parser.add_argument('-l', '--lengths', action="store_true", default=False, help="Parse Packet Size Information")
parser.add_argument('-t', '--times', action="store_true", default=False, help="Parse Inter-packet Time Information")
parser.add_argument('-d', '--dist', action="store_true", default=False, help="Parse Byte Distribution Information")
parser.add_argument('-o', '--output', action="store", help="Output file for parameters")
parser.add_argument('-e', '--tls', action="store_true", default=False, help="Parse TLS Information")
parser.add_argument('-c', '--classifier', action="store", help="Classifier methos")
args = parser.parse_args()
max_files = [None, None]
compact = 1
bd_compact = 0
types = []
if args.meta:
        types.append(0)
if args.lengths:
        types.append(1)
if args.times:
        types.append(2)
if args.dist:
        types.append(3)
if args.tls:
        types.append(4)
def get_random_block_from_data(data, labels, batch_size):
        start_index = np.random.randint(0, len(data) - batch_size)
        return data[start_index:(start_index + batch_size)],labels[start_index:(start_index + batch_size)]

def xavier_init(fan_in, fan_out, constant = 1):
        low = -constant * np.sqrt(6.0 / (fan_in + fan_out))
        high = constant * np.sqrt(6.0 / (fan_in + fan_out))
        return tf.random_uniform((fan_in, fan_out), minval = low, maxval = high, dtype = tf.float32)

def standard_scale(X_train):
        preprocessor = prep.StandardScaler().fit(X_train)
        X_train = preprocessor.transform(X_train)
        return X_train


d = Pull(args.pos_dir, args.neg_dir, types, compact, max_files, bd_compact)
data = d.data
labels = d.labels
tmp = list(zip(data, labels))
random.shuffle(tmp)
tmp2 = list(zip(*tmp))
data = list(tmp2[0])
labels = list(tmp2[1])
data = prep.scale(data)


#data = np.array(data)
labels = np.array(labels)

out_cv = []

labels_cv = []

acc_cv = []

correct_cv = []

acc2_cv = []

recall_cv = []

folds = 10

for i in range(folds):

	start = int((i / float(folds)) * len(data))

	end = int(((i + 1) / float(folds)) * len(data))

	train_data = np.zeros((len(data[0:start]) + len(data[end:]),205))

	train_data[0:start] = data[0:start]

	train_data[start:] = data[end:]

	train_labels = np.zeros((len(labels[0:start]) + len(labels[end:])))
	
	train_labels[0:start] = labels[0:start]
	
	train_labels[start:] = labels[end:]

	#train_labels = labels[0:start] + labels[end:]

	test_data = np.zeros((len(data[start:end]),205))

	test_data = data[start:end]
	
	test_labels = labels[start:end]

	params = {'kernel':'linear','class_weight':'auto'}

	classifier = SVC(**params)

	classifier.fit(train_data, train_labels)

	y_pred = classifier.predict(test_data)

	out = list(y_pred)

	out_labels = list(test_labels)

	TP = TN = FP = FN = 0

	for m in range(len(out)):
	
		if out[m] == out_labels[m]:

			if out[m] == 1:
	
				TP += 1

			else:
	
				TN += 1

		else:
	
			if out[m] == 0:

				FP += 1

			else:

				FN += 1

	print(i)

	print(TP, TN, FP, FN)

	print("**********************************")

	acc2 = float((TP)/(TP+FP))

	recall = float((TP)/(TP+FN))

	acc2_cv.append(acc2)
	
	recall_cv.append(recall)

print("准确率:",np.mean(acc2_cv))

print("召回率:",np.mean(recall_cv))



	
	




























'''


params = {'kernel':'linear','class_weight':'auto'}

classifier = SVC(**params)

classifier.fit(data, labels)

y_pred = classifier.predict(data)

print(list(labels))

print(list(y_pred))

out = list(y_pred)

out_labels = list(labels)

TP = TN = FP = FN = 0

for m in range(len(out)):

	if out[m] == out_labels[m]:
	
		if out[m] == 1:
	
			TP += 1
	
		else:
	
			TN += 1
	
	else:
	
		if out[m] == 0:
	
			FP += 1
	
		else:
	
			FN += 1

print(TP, TN, FP, FN)

acc2 = float((TP+TN)/(TP+TN+FP+FN))

print(acc2)
'''


