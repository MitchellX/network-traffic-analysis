# encoding:utf-8
from data_parser import DataParser
import os
import scipy.io as sio
import random

class Pull:
    def __init__(self, pos_dir, neg_dir, types=[0], compact=1, max_files=[None,None], bd_compact=0):
        self.num_params = 0
        self.types = types
        self.compact = compact
        self.bd_compact = bd_compact

        for t in self.types:
            if t == 0:
                self.num_params += 7
            elif t == 1 and self.compact == 0:
                self.num_params += 3600
            elif t == 1 and self.compact == 1:
                self.num_params += 100
            elif t == 2 and self.compact == 0:
                self.num_params += 900
            elif t == 2 and self.compact == 1:
                self.num_params += 100
            elif t == 3 and self.bd_compact == 0:
                self.num_params += 256
            elif t == 3 and self.bd_compact == 1:
                self.num_params += 16
            elif t == 3 and self.bd_compact == 2:
                self.num_params += 9
            elif t == 4:
                self.num_params += 198


        self.data = []
        self.labels = []

        if neg_dir != None:
            packet_neg=self.load_data(neg_dir,2, max_files[1])
            self.packet_neg=packet_neg
        if pos_dir != None:
            packet_pos=self.load_data(pos_dir,1, max_files[0])
            self.packet_pos=packet_pos

    def load_data(self, idir, label, max_files):
        files = os.listdir(idir)
        num_files = 0
        packet_total=0
        for f in files:
            try:
                dParse = DataParser(idir + f,self.compact)
            except:
                print idir + f
                print 'fail'
                continue

            num_files += 1

            tmpTLS = dParse.getTLSInfo()
            print f,"网络流数目：",len(tmpTLS)
            tmpBD = dParse.getByteDistribution()
            tmpIPT = dParse.getIndividualFlowIPTs()
            tmpPL = dParse.getIndividualFlowPacketLengths()
            tmp, ignore,packet_num = dParse.getIndividualFlowMetadata()
            packet_total+=packet_num
            if tmp != None and tmpPL != None and tmpIPT != None:
                for i in range(len(tmp)):
                    if ignore[i] == 1 and label == 1.0:
                        continue
                    tmp_data = []
                    if 0 in self.types:
                        tmp_data.extend(tmp[i])
                    if 1 in self.types:
                        tmp_data.extend(tmpPL[i])
                    if 2 in self.types:
                        tmp_data.extend(tmpIPT[i])
                    if 3 in self.types:
                        tmp_data.extend(tmpBD[i])
                    if 4 in self.types:
                        tmp_data.extend(tmpTLS[i])
                    if len(tmp_data) != self.num_params:
                        print len(tmp_data)
                    self.data.append(tmp_data)
                for i in range(len(tmp)):
                    if ignore[i] == 1 and label == 1.0:
                        continue
                    self.labels.append(label)
            if max_files != None and num_files >= max_files:
                break
        return packet_total
def main2():
    pos_dir = "/home/xmc/桌面/code/ssl_ml/json/positive2/"
    neg_dir = "/home/xmc/桌面/code/ssl_ml/json/negative2/"
    # types[0:metadata,1:length,2:time,3:bd,4:tls]
    types = [0, 1, 2, 3, 4]
    types=[0]
    d = Pull(pos_dir, neg_dir, types, 1, [500, 500], 0)
    data = d.data
    labels = d.labels
    tmp = zip(data, labels)
    random.shuffle(tmp)  # 重新为tmp的数据排序
    tmp2 = zip(*tmp)
    data = list(tmp2[0])
    labels = list(tmp2[1])

    # data=data[0:3]
    # print len(data)
    # print type(data)

    num_positive = 0
    num_negative = 0
    for l in labels:
        if l == 1:
            num_positive += 1
        else:
            num_negative += 1

    # print '正样本:\t网络流数目%i\t数据包数目%i' % (num_positive/20,d.packet_pos/20)
    # print '负样本:\t网络流数目%i\t数据包数目%i' % (num_negative,d.packet_neg)
    print '正样本:\t网络流数目%i\t数据包数目%i' % (num_positive, d.packet_pos)
    print '负样本:\t网络流数目%i\t数据包数目%i' % (num_negative, d.packet_neg)
    sio.savemat('saveddata.mat', {'data': data, 'labels': labels})
if __name__ == "__main__":
    main2()


