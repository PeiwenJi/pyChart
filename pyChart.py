# Author: PeiwenJi
# Date created: 2021.4.30
# Name: pyChart
# Description: Open any binary file and display it as a curve in the window.


# -*- coding: utf-8 -*-
# 引用常用库
import sys
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget
from PyQt5 import QtWidgets

# 引用pyqt5生成的界面
from ui.MainUI import Ui_Main

# 引用工具类
from tools.CoreTools import CoreTools
from tools.MathTools import MathTransformation


class QtDraw(QMainWindow, Ui_Main): 
    def __init__(self, parent=None):
        # 打开主界面
        super(QtDraw, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("pyChart ©PeiwenJi, Sichuan University") # 设置窗口名称
        self.setFixedSize(self.width(),self.height()) # 固定窗口大小
        self.rbtCos.setChecked(True)

        # 成员变量
        self.axisX_step = 1 # 默认x轴的递增步长为1
        self.transformation = "cos" # 默认数学变换是cos

        # 初始化widget窗口
        self.init_widgetUI()

        # 信号槽绑定
        self.btFile.clicked.connect(self.file_open)
        self.btDraw.clicked.connect(self.draw)

    # 初始化widget容器的界面
    def init_widgetUI(self):
        # pyqt5与matplotlib结合
        self.fig = plt.Figure()
        self.fig = plt.figure(figsize=(10.5, 6), dpi=100) # 设置图像大小（这里figsize是随便取的，刚好能占满widget容器）
        self.canvas = FC(self.fig)
        self.verticalLayout.addWidget(self.canvas)

        # 给widget容器添加滚动条
        self.scroll = QtWidgets.QScrollArea(self.widget) 
        self.scroll.setWidget(self.canvas)
        self.scroll.setStyleSheet("background-color: white;") # 修改滚动条背景颜色
        
        # 添加matplotlib.pyplot自带的导航栏
        self.nav = NavigationToolbar(self.canvas, self.widget) 
        self.verticalLayout.addWidget(self.nav)

        # 将滚动条添加到widget容器最下面
        self.verticalLayout.addWidget(self.scroll)
        
        # 修改widget背景颜色
        self.widget.setStyleSheet("background-color: white;")

    # 点击 按钮"Open File" 的响应函数
    def file_open(self):
        try:
            fileName, fileType = QtWidgets.QFileDialog.getOpenFileName( self, 
                                                                        "请选择一个文件", 
                                                                        os.getcwd(), 
                                                                        "All Files(*);;Text Files(*.txt)")
            self.edtFilePath.setText(fileName)
        except Exception as chooseFileException:
            print(chooseFileException)

    # 获取filepath
    def get_filepath(self):
        return self.edtFilePath.text()

    # 判断groupBox里哪个QRadioButton被选中，返回transformation
    def get_rbt_clicked(self):
        if self.rbtCos.isChecked() == True:
            self.transformation = "cos"
        elif self.rbtSin.isChecked() == True:
            self.transformation = "sin"
        elif self.rbtTan.isChecked() == True:
            self.transformation = "tan"
        elif self.rbtDiff.isChecked() == True:
            self.transformation = "diff"
        else: # 如果没有RadioButton被选中，则设置rbtCos被选中，并返回"cos"
            self.rbtCos.setChecked(True)
            self.transformation = "cos"
        print(self.transformation)
        return self.transformation

    # 绘图
    def draw(self, axisX_step=1):
        try:
            # 获取文件路径和选中的变换
            fileName = self.get_filepath()
            transformation = self.get_rbt_clicked()

            # 第一个图：原数据
            ax_top = self.fig.add_subplot(211)
            axisX_top, axisY_top = CoreTools.file_to_axisData(fileName)
            ax_top.cla()  # 删除原图，让画布上只有新的一次的图
            ax_top.plot(axisX_top, axisY_top)
            ax_top.set_title('Original Data')
            ax_top.set_xlabel("X")
            ax_top.set_ylabel("Y")

            # 第二个图：数学变换后的图
            ax_bottom = self.fig.add_subplot(212, sharex=ax_top) # 共享轴线：当缩放某个Axes时，另一个Axes也跟着缩放
            axisX_bottom = axisX_top
            axisY_bottom = MathTransformation.process(axisY_top, transformation)
            ax_bottom.cla()  # 删除原图，让画布上只有新的一次的图
            ax_bottom.plot(axisX_bottom, axisY_bottom)
            ax_bottom.set_title(transformation)
            ax_bottom.set_xlabel("X")
            ax_bottom.set_ylabel("Y")

            # 调整subplot的间隔
            plt.subplots_adjust(hspace=0.4)

            self.canvas.draw()
        except:
            QtWidgets.QMessageBox.critical(self, "Error", "请检查文件路径是否正确")


# 主函数
def main():
    app = QApplication(sys.argv)
    window = QtDraw()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()