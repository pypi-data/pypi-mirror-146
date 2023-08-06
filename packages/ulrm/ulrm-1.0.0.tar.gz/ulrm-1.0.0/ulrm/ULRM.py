'''
Univariate Linear Regression Model
A module that can make Univariate Linear Regression Model
Aut:billma007
Email:maboning237103015@163.com
twitter:@billma007cool
'''

import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import statsmodels.api as sm
class ULRM():
    getdataway=False
    excelget=''
    list1=[]
    list2=[]
    '''
    如果getdataway==False，则采用列表传入来处理数据
    list1是x轴，list2是y轴
    如果是True，则采用Excel传入数据
    Excelget是读入的Excel文件路径和名称
    '''
    xlabelset="X"
    ylabelset="Y"
    '''
    设置坐标轴名称
    '''

    _icon=''
    def __init__(self):
            pass
    def makeplt(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False      # 用来正常显示负号


        #对数据集拟合直线并给出参数
        X=self.data['X'].values.reshape(-1,1)
        Y=self.data['Y'].values.reshape(-1,1)

        reg=LinearRegression()
        reg.fit(X,Y)
        print("The linear model is: Y ={:.5}X+{:.5}".format((reg.coef_[0][0]),reg.intercept_[0]))

        #数据拟合线可视化
        predictions=reg.predict(X)
        plt.figure(figsize=(16,8))
        plt.scatter(
            self.data['X'],
            self.data['Y'],
            c='black'
        )
        plt.plot(
        self.data['X'],
            predictions,
            c='blue',
            linewidth=2
        )
        plt.xlabel(self.xlabelset)
        plt.ylabel(self.ylabelset)
        plt.show()
    def getfunc(self):
        X=self.data['X'].values.reshape(-1,1)
        Y=self.data['Y'].values.reshape(-1,1)
        reg=LinearRegression()
        reg.fit(X,Y)
        returnfunc="Y ={:.5}X+{:.5}".format((reg.coef_[0][0]),reg.intercept_[0])
        return returnfunc
    def showinfo_print(self):
        #评估模型相关性
        X=self.data['X']
        Y=self.data['Y']

        X2=sm.add_constant(X)
        est=sm.OLS(Y,X2.astype(float))
        est2=est.fit()
        print(est2.summary())
    def showinfo_return(self):
            #评估模型相关性
        X=self.data['X']
        Y=self.data['Y']

        X2=sm.add_constant(X)
        est=sm.OLS(Y,X2.astype(float))
        est2=est.fit()
        return est2.summary()
    def readdata(self):
        if self.getdataway==True:
        #读取数据
            file = self.excelget
            if file=='':
                raise Exception("""When you choose to use the table to enter self.data, please use the "ULRM.excelget=xxx" statement to read the table self.data""")
            elif "xls" not in file:
                raise Exception("Please select the correct file format (only xls and xlsx formats are supported)")
            elif os.path.isfile(file)==False:
                raise Exception("Please enter the correct file name and path!")
            self.data = pd.read_excel(file,index_col=False)
        else:

            listall=[list(l) for l in zip(self.list1, self.list2)]
            self.data=pd.DataFrame(data=listall,columns=['X','Y'])
if __name__=="__main__":
    a=ULRM()
    a.getdataway=True
    a.xlabelset="X轴"
    a.ylabelset="Y轴"
    a.excelget="1.xlsx"
    a.readdata()
    print(a.getfunc())
    a.showinfo_print()
    a.makeplt()
    print(a.showinfo_return())