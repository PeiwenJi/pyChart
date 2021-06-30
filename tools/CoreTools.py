# Author: PeiwenJi
# Date created: 2021.5.1
# Name: CoreTools
# Description: Core functions of the program


# -*- coding: utf-8 -*-
import sys
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets


class CoreTools(object):

    # 名称：file_to_axisData
    # 描述：将文件内容变成chart上的横纵坐标数据
    # 解释：每次两个字节读取文件，利用unpack函数将读取内容解析为10进制的数字，最后将这些10进制存在axisY数组里；
    #      横坐标axisX是从0开始，以axisX_step递增的序列
    # 返回：横坐标和纵坐标的数组
    @classmethod
    def file_to_axisData(self, fileName, axisX_step=1):
        axisX = [] # 横坐标
        axisY = [] # 纵坐标
        count = 0 # 计数器
        
        # 打开文件
        try:
            inputFile = open(fileName, 'rb')
            while True:
                count = count + axisX_step # 每次按一定步长增加横坐标值
                binaryChunk = inputFile.read(2)  # 每次按2bytes(16bit)读取              
                
                # 将两个字节（16位）内容解析为10进制的数
                try: 
                    binaryChunk = struct.unpack("H", binaryChunk)[0]
                    axisX.append(count)
                    axisY.append(binaryChunk)
                except: # 最后只有一个字节或者为空时，struct.unpack会抛出异常
                    break

        except Exception as openFileException:
            print(openFileException)        
        finally:
            inputFile.close()
        
        return axisX, axisY


'''if __name__ == '__main__':
    tools = MyTools()
    print(tools.file_to_axisData())'''