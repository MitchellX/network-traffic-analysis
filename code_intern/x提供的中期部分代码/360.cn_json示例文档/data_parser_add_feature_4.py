import numpy as np
import math
import json
import gzip

# 176
cs = {u'c005': 0, u'c004': 1, u'c007': 2, u'0039': 3, u'0038': 4, u'c003': 5, u'c002': 6, u'0035': 7, u'0034': 8, u'0037': 9, u'0036': 10, u'c009': 11, u'c008': 12, u'0033': 13, u'0032': 14, u'c07a': 15, u'c07b': 16, u'c07c': 17, u'c07d': 18, u'0065': 19, u'c087': 21, u'c086': 22, u'c081': 23, u'c080': 24, u'c072': 25, u'c073': 26, u'c076': 27, u'c077': 28, u'0040': 29, u'0041': 30, u'0042': 31, u'feff': 32, u'0044': 33, u'0045': 34, u'0046': 35, u'0030': 36, u'c00e': 37, u'c00d': 38, u'c00f': 39, u'c00a': 40, u'c00c': 41, u'003e': 42, u'003d': 43, u'003f': 44, u'003a': 45, u'003c': 46, u'003b': 47, u'006a': 109, u'00ff': 49, u'00fd': 50, u'00fb': 51, u'00fc': 52, u'c08a': 53, u'c08b': 54, u'5600': 55, u'c05d': 56, u'c05c': 57, u'00af': 58, u'00ae': 59, u'0017': 113, u'00a7': 60, u'00a6': 61, u'00a5': 62, u'00a4': 63, u'00a3': 64, u'00a2': 65, u'00a1': 66, u'00a0': 67, u'cc13': 68, u'cc15': 69, u'cc14': 70, u'c049': 71, u'c048': 20, u'0016': 114, u'000d': 74, u'000f': 75, u'000a': 76, u'000c': 77, u'0064': 81, u'0066': 79, u'0067': 80, u'00b0': 78, u'00b1': 82, u'0062': 83, u'0063': 84, u'0060': 85, u'0061': 86, u'0068': 87, u'0069': 88, u'0004': 89, u'0005': 90, u'0006': 91, u'0007': 92, u'0001': 93, u'0002': 94, u'0003': 95, u'0008': 96, u'0009': 97, u'0031': 98, u'0019': 125, u'0018': 126, u'c030': 101, u'c031': 102, u'c032': 103, u'006d': 104, u'00ba': 105, u'006b': 106, u'006c': 107, u'00bd': 108, u'00be': 48, u'00c4': 110, u'00c0': 111, u'00c3': 112, u'cca9': 72, u'cca8': 73, u'0015': 115, u'0014': 116, u'0013': 117, u'0012': 118, u'0011': 119, u'0010': 120, u'c01b': 121, u'c01c': 122, u'c01a': 123, u'c01f': 124, u'c01d': 99, u'c01e': 100, u'002c': 127, u'002f': 128, u'c029': 129, u'c028': 130, u'c027': 131, u'c026': 132, u'c025': 133, u'c024': 134, u'c023': 135, u'c022': 136, u'c021': 137, u'c020': 138, u'009f': 139, u'009e': 140, u'009d': 141, u'009c': 142, u'009b': 143, u'009a': 144, u'0088': 145, u'0089': 146, u'0084': 147, u'0085': 148, u'0086': 149, u'0087': 150, u'0043': 151, u'c02f': 152, u'c02e': 153, u'c02d': 154, u'c02c': 155, u'c02b': 156, u'c02a': 157, u'c018': 158, u'c019': 159, u'001b': 160, u'001a': 161, u'c012': 162, u'c013': 163, u'c011': 164, u'c016': 165, u'c017': 166, u'c014': 167, u'008d': 168, u'008a': 169, u'008b': 170, u'008c': 171, u'0099': 172, u'0098': 173, u'0097': 174, u'0096': 175}

# 21
ext = {u'0017': 0, u'0023': 1, u'0015': 2, u'0000': 3, u'0012': 4, u'0005': 5, u'3374': 6, u'6a5a': 7, u'8b47': 8, u'754f': 9, u'000d': 10, u'ff01': 11, u'000f': 12, u'eb02': 13, u'0010': 14, u'000a': 15, u'000b': 16, u'a878': 17, u'7550': 18, u'5500': 19, u'79d1': 20}

bd_merges = [[0, 65, 69, 48, 109, 77, 47, 112, 52, 117, 57], [10, 99, 13], [130, 7, 9, 139, 20, 25, 28, 31, 42, 54, 55, 187, 64, 68, 73, 74, 80, 209, 210, 213, 86, 215, 228, 229, 102, 238, 246, 252, 253, 126], [32, 97, 45], [67, 114, 111, 49, 50, 116], [100, 84], [101], [194, 162, 104, 105, 75, 44, 98, 108, 115, 53, 118, 56, 184, 61], [201, 203, 233], [193, 226, 171, 197, 198, 231, 234, 235, 174, 175, 208, 146, 147, 181, 217, 199, 159], [131, 137, 150, 151, 221, 185, 186, 190, 63, 206, 211, 85, 89, 93, 95, 224, 227, 236, 237, 240, 113, 242, 244, 245], [2, 3, 8, 21, 34, 168, 41, 43, 46, 178, 51, 182, 58, 71, 72, 76, 202, 204, 78, 207, 248, 82, 83, 214, 79, 103, 106, 110, 239, 40, 119, 120, 121, 122], [128, 1, 225, 132, 133, 6, 129, 136, 138, 11, 140, 141, 15, 144, 152, 18, 19, 148, 22, 23, 24, 4, 154, 155, 156, 26, 30, 5, 160, 33, 27, 164, 165, 166, 39, 169, 135, 172, 173, 29, 176, 177, 91, 180, 59, 188, 189, 134, 35, 192, 66, 70, 161, 12, 143, 92, 81, 163, 87, 88, 36, 90, 219, 220, 94, 96, 16, 38, 107, 157, 243, 62, 249, 250, 124, 125, 127], [142, 17, 149, 153, 158, 37, 167, 170, 179, 183, 60, 191, 195, 196, 200, 205, 212, 14, 216, 218, 222, 223, 123, 230, 145, 232, 241, 247, 251], [254], [255]]


def getTLSVersionVector(cs_list, ext):
    tls_info = np.zeros(len(cs.keys())+36)

    for c in cs_list:
        if c in cs:
            tls_info[cs[c]] = 1

    for c in ext:
        if int(c['type'],16) < 36:
            tls_info[int(c['type'],16)+len(cs.keys())] = 1

    return tls_info



bd_comp = {}
for i in range(len(bd_merges)):
    for x in bd_merges[i]:
        bd_comp[x] = i

class DataParser:
    def __init__(self, json_file, compact=1):
        self.compact = compact
        self.skipped = 0
        self.legacy_format = False
        self.flows = []
        self.advancedInfo = {}
        self.all_flows = {}

        # print json_file
        with open(json_file, 'r') as fp:
            try:  # for incomplete gzip files
                for line in fp:
                    #                    if line.strip == '{' or 'metadata' in line:
                    #                    if 'metadata' in line:
                    #                        self.legacy_format = True
                    #                        break

                    try:

                        if ('mozilla' not in line) and ('SNI' in line):
                        
                            tmp = json.loads(line)
                            if ('bpf' not in tmp) and ('tls' in tmp):
                                tls_str = tmp['tls']
                                if "SNI" in tls_str:
                                    self.flows.append(tmp)
                            '''
                            tls_str = tmp['tls']
                            if "SNI" in tls_str:
                                if ('bpf' not in tmp)
                                print(1)
 
                            if ('bpf' not in tmp) and ('tls' in tmp):
                                self.flows.append(tmp)
                            '''









                        '''
                        tmp = json.loads(line)
                        #if ('bpf' not in tmp) and ('mozilla' not in tmp):
                        if 'bpf' not in tmp:

                            if 'tls' in tmp:

                                sni = tmp['tls']['SNI']
                                #print(sni)

                                if 'mozilla.com' not in sni:
                                    #print(sni)
                                    self.flows.append(tmp)
                        '''

                            #sni = tmp['SNI']
                            #print(sni)
                            #if 'mozilla' not in sni:
                                


                            #   self.flows.append(tmp)
                    except:
                        continue
            except:
                return


        if self.legacy_format:
            data = ""
            with open(json_file,'r') as fp:
                for line in fp:
                    if "\"hd\"" in line:
                        continue
                    data += line.strip().replace('"x": i','"x": "i"').replace('"x": a','"x": "a"')
            try:
                self.flows = json.loads(data)
            except:
                if not data.endswith("] }"):
                    data += "] }"
                self.flows = json.loads(data)


    def getTLSInfo(self):
        # print "&&&&&&&&&&&&&&&&"
        if self.legacy_format == False:
            if self.flows == []:
                data = []
                return data

            data = []
            for flow in self.flows:
                if len(flow['packets']) == 0:
                    continue
                tls_info = np.zeros(len(cs.keys())+len(ext.keys())+1)

                if 'tls' in flow and 'cs' in flow['tls']:
                    # flow['tls']['cs'].sort()
                    # print flow['tls']['cs']
                    for c in flow['tls']['cs']:
                        # print c
                        if c in cs:
                            tls_info[cs[c]] = 1

                # type_list=[]
                # if 'tls' in flow and 'tls_ext' in flow['tls']:
                #     flow['tls']['tls_ext'].sort()
                #     # print flow['tls']['tls_ext']
                #     for c in flow['tls']['tls_ext']:
                #         # type_list.append(c['type'])
                #         if c['type'] in ext:
                #             tls_info[len(cs.keys())+ext[c['type']]] = 1

                if 'tls' in flow and ' s_tls_ext' in flow['tls']:
                    flow['tls']['s_tls_ext'].sort()
                    # print flow['tls']['tls_ext']
                    for c in flow['tls']['s_tls_ext']:
                        # type_list.append(c['type'])
                        if c['type'] in ext:
                            tls_info[len(cs.keys()) + ext[c['type']]] =1
                            # type_list.sort()
                # print type_list
                if 'tls' in flow and 'tls_client_key_length' in flow['tls']:
                    tls_info[len(cs.keys())+len(ext.keys())] = flow['tls']['tls_client_key_length']


                data.append(list(tls_info))

            return data



    def getByteDistribution(self):
        if self.legacy_format == False:
            if self.flows == []:
                return None

            data = []
            for flow in self.flows:
                if len(flow['packets']) == 0:
                    continue
                if 'bd' in flow and sum(flow['bd']) > 0:
                    tmp = map(lambda x: x/float(sum(flow['bd'])),flow['bd'])
                    data.append(tmp)
                else:
                    data.append(np.zeros(256))

            return data


    def getIndividualFlowPacketLengths(self):
        if self.legacy_format == False:
            if self.flows == []:
                return None

            data = []
            if self.compact:
                numRows = 10
                binSize = 150.0
            else:
                numRows = 60
                binSize = 25.0
            for flow in self.flows:
                transMat = np.zeros((numRows,numRows))
                if len(flow['packets']) == 0:
                    continue
                elif len(flow['packets']) == 1:
                    curPacketSize = min(int(flow['packets'][0]['b']/binSize),numRows-1)
                    transMat[curPacketSize,curPacketSize] = 1
                    data.append(list(transMat.flatten()))
                    continue

                # get raw transition counts
                for i in range(1,len(flow['packets'])):
                    prevPacketSize = min(int(flow['packets'][i-1]['b']/binSize),numRows-1)
                    if 'b' not in flow['packets'][i]:
                        break
                    curPacketSize = min(int(flow['packets'][i]['b']/binSize),numRows-1)
                    transMat[prevPacketSize,curPacketSize] += 1

                # get empirical transition probabilities
                for i in range(numRows):
                    if float(np.sum(transMat[i:i+1])) != 0:
                        transMat[i:i+1] = transMat[i:i+1]/float(np.sum(transMat[i:i+1]))

                data.append(list(transMat.flatten()))

            return data
  
    def getIndividualFlowPacketLengthGraph(self):

        data = []

        for flow in self.flows:

            length_list = []

            for num in range(150):

                length_list.append(0)

            if len(flow['packets']) == 0:

                continue

            for i in range(len(flow['packets'])):

                length_num = math.floor(flow['packets'][i]['b']/10)

                if length_num < 150:

                    length_list[length_num] += 1

                else:

                    length_list[149] += 1

            data.append(length_list)


        return data







    def getIndividualFlowIPTs(self):
        if self.legacy_format == False:
            if self.flows == []:
                return None

            data = []
            if self.compact:
                numRows = 10
                binSize = 50.0
            else:
                numRows = 30
                binSize = 50.0
            for flow in self.flows:
                transMat = np.zeros((numRows,numRows))
                if len(flow['packets']) == 0:
                    continue
                elif len(flow['packets']) == 1:
                    curIPT = min(int(flow['packets'][0]['ipt']/float(binSize)),numRows-1)
                    transMat[curIPT,curIPT] = 1
                    data.append(list(transMat.flatten()))
                    continue

                # get raw transition counts
                for i in range(1,len(flow['packets'])):
                    prevIPT = min(int(flow['packets'][i-1]['ipt']/float(binSize)),numRows-1)
                    curIPT = min(int(flow['packets'][i]['ipt']/float(binSize)),numRows-1)
                    transMat[prevIPT,curIPT] += 1
                # print transMat
                # get empirical transition probabilities
                for i in range(numRows):
                    if float(np.sum(transMat[i:i+1])) != 0:
                        transMat[i:i+1] = transMat[i:i+1]/float(np.sum(transMat[i:i+1]))

                data.append(list(transMat.flatten()))

            return data
  
    def getIndividualFlowPacketTimeGraph(self):

        data =[]

        for flow in self.flows:

            time_lists = []

            for num in range(100):
   
                time_lists.append(0)

            if len(flow['packets']) == 0:

                continue

            for i in range(len(flow['packets'])):

                if flow['packets'][i]['ipt'] == 0:

                    time_lists[0] += 1

                else:

                    #length_num = math.floor(flow['packets'][i]['b']/10)

                    time_num = math.floor(flow['packets'][i]['ipt']/5)
 
                    #time_num = math.floor(math.log(flow['packets'][i]['ipt'], 2))

                    if time_num < 100:

                        time_lists[time_num] += 1

                    else:

                        time_lists[99] += 1


            data.append(time_lists)

        return data


    def getIndividualFlowMetadata(self):
        if self.legacy_format == False:
            if self.flows == []:
                return None, None,0,0
            packet_num=0
            data = []
            metadata = []
            # print "len(self.flows):",len(self.flows)
            for flow in self.flows:
                if len(flow['packets']) == 0:
                    continue
                tmp = []
                tmp_m = []
                tmp_b = 0
                if 'ib' in flow:
                    tmp_b += flow['ib']
                if 'ob' in flow:
                    tmp_b += flow['ob']
            

                key = flow['sa'].replace('.','')+flow['da'].replace('.','')+str(int(flow['sp']))+str(int(flow['dp']))+str(tmp_b)
                key = str(key)
                bd = None
                if 'bd' in flow:
                    bd = flow['bd']
                self.advancedInfo[key] = (flow['sa'],flow['da'],flow['sp'],flow['dp'],flow['packets'],bd)
                self.all_flows[key] = flow
                tmp_m.append(flow['sa']) # source port
                tmp_m.append(flow['da']) # destination address
                tmp_m.append(flow['sp']) # source port
                tmp_m.append(flow['dp']) # destination port
                tmp.append(float(flow['dp'])) # destination port
                tmp.append(float(flow['sp'])) # source port
                if 'ip' in flow:
                    tmp.append(flow['ip']) # inbound packets
                    tmp_m.append(flow['ip'])
                else:
                    tmp.append(0)
                    tmp_m.append(0)
                if 'op' in flow:
                    tmp.append(flow['op']) # outbound packets
                    tmp_m.append(flow['op'])
                else:
                    tmp.append(0)
                    tmp_m.append(0)
                if 'ib' in flow:
                    tmp.append(flow['ib']) # inbound bytes
                    tmp_m.append(flow['ib'])
                else:
                    tmp.append(0)
                    tmp_m.append(0)
                if 'ob' in flow:
                    tmp.append(flow['ob']) # outbound bytes
                    tmp_m.append(flow['ob'])
                else:
                    tmp_m.append(0)
                    tmp.append(0)
                # elapsed time of flow
                if flow['packets'] == []:
                    tmp.append(0)
                else:
                    time = 0
                    for packet in flow['packets']:
                        time += packet['ipt']
                    tmp.append(time)
                if 'pr' in flow:
                    tmp_m.append(flow['pr'])
                else:
                    tmp_m.append(0)

                # add tls specific items
                if 'tls' in flow and 'scs' in flow['tls']:
                    tmp_m.append(flow['tls']['scs'])
                else:
                    tmp_m.append(-1)
                if 'tls' in flow and 'tls_client_key_length' in flow['tls']:
                    tmp_m.append(flow['tls']['tls_client_key_length'])
                else:
                    tmp_m.append(-1)
                if 'tls' in flow and 'tls_ov' in flow['tls'] and 'tls_iv' in flow['tls']:
                    tmp_v = max(flow['tls']['tls_iv'],flow['tls']['tls_ov'])
                elif 'tls' in flow and 'tls_ov' in flow['tls']:
                    tmp_v = flow['tls']['tls_ov']
                elif 'tls' in flow and 'tls_iv' in flow['tls']:
                    tmp_v = flow['tls']['tls_iv']
                else:
                    tmp_v = -1
                if tmp_v == 5:
                    tmp_m.append('TLS 1.2')
                elif tmp_v == 4:
                    tmp_m.append('TLS 1.1')
                elif tmp_v == 3:
                    tmp_m.append('TLS 1.0')
                elif tmp_v == 2:
                    tmp_m.append('SSL 3.0')
                elif tmp_v == 1:
                    tmp_m.append('SSL 2.0')
                else:
                    tmp_m.append(-1)


                tmp_m.append(tmp_v) # for convenience

                data.append(tmp)
                metadata.append(tmp_m)

                packet_num2=tmp[2]+tmp[3]
                packet_num = packet_num+packet_num2
            if data == []:
                return None,None,0,0
		#return None,None,0
            return data, metadata, packet_num, len(data)
            #return data, metadata, packet_num

