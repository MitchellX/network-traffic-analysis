from __future__ import division,print_function,absolute_import

import tensorflow as tf
import argparse
import numpy as np
import random
import sklearn.preprocessing as prep
from pull_data import Pull
from sklearn import metrics
import time
import os 

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# linux 命令行操作argparser，附加提示
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


data = np.array(data)

#print(len(data[0]))


#print(len(data))

#print(len(labels[0]))


#data_new = np.zeros((len(data), 660))

data_new = data[0:len(data), 0:660]

data_new = prep.scale(data_new)

#data_new = tf.reshape(data_new, [-1, 66, 10, 1])

#print(len(data_new[0]))

#print(len(data_new))


max_steps = 2500
batch_size = 128 

def variable_with_weight_loss(shape, stddev, w1):
        var = tf.Variable(tf.truncated_normal(shape, stddev = stddev))
        if w1 is not None:
                weight_loss = tf.multiply(tf.nn.l2_loss(var), w1, name = 'weight_loss')
                tf.add_to_collection('losses', weight_loss)
        return var 


#images_train = data_new

#labels_train = labels

#images_test = data_new

#labels_test = labels

image_holder = tf.placeholder(tf.float32, [batch_size, 660])
#image_holder = tf.placeholder(tf.float32, [None, 660]) 

label_holder = tf.placeholder(tf.int32, [batch_size])
#label_holder = tf.placeholder(tf.int32, [None])

image_holder_new = tf.reshape(image_holder, [-1, 66, 10, 1])

weight1 = variable_with_weight_loss(shape = [5, 5, 1, 64], stddev = 5e-2, w1 = 0.0)
kernel1 = tf.nn.conv2d(image_holder_new, weight1, [1, 1, 1, 1], padding = 'SAME')
bias1 = tf.Variable(tf.constant(0.0, shape = [64]))
conv1 = tf.nn.relu(tf.nn.bias_add(kernel1, bias1))
pool1 = tf.nn.max_pool(conv1, ksize = [1, 3, 3, 1], strides = [1, 2, 2, 1], padding = 'SAME')
norm1 = tf.nn.lrn(pool1, 4, bias = 1.0, alpha = 0.001 / 9.0, beta = 0.75)

weight2 = variable_with_weight_loss(shape = [5, 5, 64, 64], stddev = 5e-2, w1 = 0.0)
kernel2 = tf.nn.conv2d(norm1, weight2, [1, 1, 1, 1], padding = 'SAME')
bias2 = tf.Variable(tf.constant(0.1, shape = [64]))
conv2 = tf.nn.relu(tf.nn.bias_add(kernel2, bias2))
norm2 = tf.nn.lrn(conv2, 4, bias = 1.0, alpha = 0.001 / 9.0, beta = 0.75)
pool2 = tf.nn.max_pool(norm2, ksize = [1, 3, 3, 1], strides = [1, 2, 2, 1], padding = 'SAME')

reshape = tf.reshape(pool2, [batch_size, -1])
dim = reshape.get_shape()[1].value
weight3 = variable_with_weight_loss(shape = [dim, 384], stddev = 0.04, w1 = 0.004)
bias3 = tf.Variable(tf.constant(0.1, shape = [384]))
local3 = tf.nn.relu(tf.matmul(reshape, weight3) + bias3)

weight4 = variable_with_weight_loss(shape = [384, 192], stddev = 0.04, w1 = 0.004)
bias4 = tf.Variable(tf.constant(0.1, shape = [192]))
local4 = tf.nn.relu(tf.matmul(local3, weight4) + bias4)

weight5 = variable_with_weight_loss(shape = [192, 2], stddev = 1/192.0, w1 = 0.0)
bias5 = tf.Variable(tf.constant(0.0, shape = [2]))
logits = tf.add(tf.matmul(local4, weight5), bias5)

def loss(logits, labels):
        labels = tf.cast(labels, tf.int64)
        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
                logits = logits, labels = labels, name = 'cross_entropy_per_example')
        cross_entropy_mean = tf.reduce_mean(cross_entropy, name = 'cross_entropy')
        tf.add_to_collection('losses', cross_entropy_mean)
        return tf.add_n(tf.get_collection('losses'), name = 'total_loss')

loss = loss(logits, label_holder)

train_op = tf.train.AdamOptimizer(1e-3).minimize(loss)

top_k_op = tf.nn.in_top_k(logits, label_holder, 1)

#sess = tf.InteractiveSession()
#tf.global_variables_initializer().run()

#tf.train.start_queue_runners()

out_cv = []

labels_cv = []

acc_cv = []

correct_cv = []

acc2_cv = []

recall_cv = []

folds = 10

for i in range(folds):

        sess = tf.InteractiveSession()
        
        tf.global_variables_initializer().run()

        tf.train.start_queue_runners()

        start = int((i / float(folds)) * len(data))

        end = int(((i + 1) / float(folds)) * len(data))

        images_train = np.zeros((len(data_new[0:start]) + len(data_new[end:]),660))

        images_train[0:start] = data_new[0:start]

        images_train[start:] = data_new[end:]

        labels_train = labels[0:start] + labels[end:]
  
        images_test = np.zeros((len(data_new[start:end]),660))

        images_test = data_new[start:end]

        labels_test = labels[start:end]

        for step in range(max_steps):

                start_time = time.time()

                image_batch, label_batch = get_random_block_from_data(images_train, labels_train, batch_size)

                _, loss_value = sess.run([train_op, loss], feed_dict = {image_holder: image_batch, label_holder: label_batch})

                duration = time.time() - start_time

                #if step % 10 == 0:

                 #       examples_per_sec = batch_size / duration

                  #      sec_per_batch = float(duration)

                   #     format_str = ('step %d, loss = %.2f (%.1f examples/sec; %.3f sec/batch)')

                    #    print(format_str % (step, loss_value, examples_per_sec, sec_per_batch))

        num_examples = len(images_test) 

        import math

        num_iter = int(math.ceil(num_examples / batch_size))

        true_count = 0

        total_sample_count = num_iter * batch_size

        step = 0

        while step < num_iter:

                image_batch, label_batch = get_random_block_from_data(images_test, labels_test, batch_size)

                out = list(tf.argmax(logits, 1).eval({image_holder: image_batch, label_holder: label_batch}))

                print(out)

                print(label_batch)

                TP = TN = FP = FN = 0

                for m in range(len(out)):

                        if out[m] == label_batch[m]:

                                if out[m] == 1:

                                        TP += 1

                                else:

                                        TN += 1

                        else:

                                if out[m] == 1:

                                        FP += 1

                                else:

                                        FN += 1



                predictions = sess.run([top_k_op], feed_dict = {image_holder: image_batch, label_holder: label_batch})

                true_count += np.sum(predictions)

                step += 1
        precision = true_count / total_sample_count

        print(i)

        print(TP, TN, FP, FN)

        print("*****************")

        print('precision @ 1 = %.3f' % precision)

        acc2 = float((TP)/(TP+FP))

        recall = float((TP)/(TP+FN))

        out_cv.append(precision)

        acc2_cv.append(acc2)

        recall_cv.append(recall)

print("准确率:", np.mean(acc2_cv))

print("召回率:", np.mean(recall_cv))     

print("out:",np.mean(out_cv))     
'''                                
for step in range(max_steps):
        start_time = time.time()
        image_batch, label_batch = get_random_block_from_data(images_train, labels_train, batch_size)

        #image_batch = tf.reshape(image_batch, [-1, 66, 10, 1])

        #image_batch = list(image_batch)

        _, loss_value = sess.run([train_op, loss], feed_dict = {image_holder: image_batch, label_holder: label_batch})
        duration = time.time() - start_time

        if step % 10 == 0:
                examples_per_sec = batch_size / duration
                sec_per_batch = float(duration)
                format_str = ('step %d, loss = %.2f (%.1f examples/sec; %.3f sec/batch)')
                print(format_str % (step, loss_value, examples_per_sec, sec_per_batch))

num_examples = 1419
import math
num_iter = int(math.ceil(num_examples / batch_size))
true_count = 0
total_sample_count = num_iter * batch_size
step = 0
while step < num_iter:
        image_batch, label_batch = get_random_block_from_data(images_test, labels_test, batch_size)

        out = list(tf.argmax(logits, 1).eval({image_holder: image_batch, label_holder: label_batch}))
        print(out)
        print(label_batch)

        predictions = sess.run([top_k_op], feed_dict = {image_holder: image_batch, label_holder: label_batch})
        #prediction = sess.run([logits], feed_dict = {image_holder: image_batch, label_holder: label_batch}) 
        true_count += np.sum(predictions)
        step += 1

precision = true_count / total_sample_count
print('precision @ 1 = %.3f' % precision)
'''

'''
num_examples = 1419
image_batch = images_test
label_batch = labels_test
#prediction = sess.sun([logits], feed_dict = {iamge_holder: image_batch, label_holder: label_batch})
out = list(tf.argmax(logits, 1).eval({image_holder: image_batch, label_holder: label_batch}))
print(out)

print(label_batch)

'''







'''

sess = tf.InteractiveSession()

def weight_variable(shape):
	
	initial = tf.truncated_normal(shape, stddev=0.1)

	return tf.Variable(initial)

def bias_variable(shape):

	initial = tf.constant(0.1, shape=shape)

	return tf.Variable(initial)

def conv2d(x, W):
	
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding = 'SAME')

def max_pool_2x2(x):

	return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1],padding='SAME')

x = tf.placeholder(tf.float32, [None, 784])

y_ = tf.placeholder(tf.float32, [None, 10])

x_image = tf.reshape(x, [-1, 28,28,1])

W_conv1 = weight_variable([5,5,1,32])

b_conv1 = bias_variable([32])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5,5,32,64])

b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([7 * 7 * 64, 1024])

b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])

h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)

h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 10])

b_fc2 = bias_varibale([10])

'''

