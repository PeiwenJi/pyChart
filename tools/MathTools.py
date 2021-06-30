# Author: PeiwenJi
# Date created: 2021.5.2
# Name: MathTools
# Description: A set of mathematical transformation functions


# -*- coding: utf-8 -*-
import numpy as np


class MathTransformation(object):
    # 返回x的余弦值
    @classmethod
    def cos(self, x):
        np_x = np.array(x)
        return np.cos(np_x)

    # 返回x的正弦值
    @classmethod
    def sin(self, x):
        np_x = np.array(x)
        return np.sin(np_x)
    
    # 返回x的正切值
    @classmethod
    def tan(self, x):
        np_x = np.array(x)
        return np.tan(np_x)

    # 返回x的差分
    @classmethod
    def diff(self, x):
        np_x = np.array(x)
        np_x = np.append(np_x, 0) # 计算差分会使x少一个值，在最后填一个0补齐
        return np.diff(np_x)
    
    # 选择对x进行哪种数学变换
    @classmethod
    def process(self, x, transformation):
        if transformation == "cos":
            x = self.cos(x)
        elif transformation == "sin":
            x = self.sin(x)
        elif transformation == "tan":
            x = self.tan(x)
        elif transformation == "diff":
            x = self.diff(x)
        else:
            print("请正确输入变换名称：cos or sin or tan or diff")
        return x


'''if __name__ == '__main__':
    example = MathTransformation()
    x = [0, 5, 2, 3, 10]
    print(example.cos(x))
    print(example.sin(x))
    print(example.tan(x))
    print(example.diff(x))'''


