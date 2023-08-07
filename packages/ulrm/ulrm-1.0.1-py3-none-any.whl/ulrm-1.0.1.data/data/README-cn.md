# ✨✨✨一元线性回归模型的计算✨✨✨

一元线性回归模型是高中阶段必学内容，本工具可以轻松计算一元线性回归函数和画图。

## 快速开始🎉

```python
pip install ulrm
```

## 在你的程序中使用

### 初始化数据😎

#### 你可以通过传入列表来获取数据

```python
from ulrm import ULRM #import module

a = ULRM()

a.getdataway=False #False代表你使用列表还处理数据
a.list1=[1,2,3,4,5,6,7,8,9] #x轴数据
a.list2=[100,112,121,133,140,150,166,172,181] #y轴数据

a.xlabelset="X"
a.ylabelset="Y"
# 坐标轴名称

a.readdata()


```

#### 你也可以使用excel来传入数据

目前仅支持 `*.xlsx` and `*.xls`

```python
a = ULRM()
a.getdataway=True #True代表你使用Excel来导入数据
a.excelget='example.xlsx' #excel名称
a.xlabelset="X axis"
a.ylabelset="Y axls"

a.readdata()

```

#### Excel的格式

excel中必须有两列，第一列是X轴数据，第二列是Y轴数据，第一行必须是“X”和“Y”。从第二行开始记录数据。**例如，以下示例合法：**

| X | Y   |
| :-: | --- |
| 1 | 100 |
| 2 | 201 |
| 3 | 333 |
| 4 | 424 |
| 5 | 501 |
| 6 | 607 |
| 7 | 705 |
| 8 | 870 |

### 处理数据👍

你可以同或以下函数来获取最拟合的线性回归函数

```python
print(a.getfunc())

#output(example):
# The linear model is: Y =119.0X+-25.0
```

你也可以把它划出来:

```python
a.makeplt()
```

![output](https://fastly.jsdelivr.net/gh/billma007/imagesave/ulrmexample1.png)

你也可以将该函数的更多信息打印出来:

```python
a.showinfo_print()

# output(example):
"""
                            OLS Regression Results
==============================================================================
Dep. Variable:                      Y   R-squared:                       0.996
Model:                            OLS   Adj. R-squared:                  0.994
Method:                 Least Squares   F-statistic:                     524.5
Date:                Sat, 16 Apr 2022   Prob (F-statistic):            0.00190
Time:                        10:28:16   Log-Likelihood:                -14.100
No. Observations:                   4   AIC:                             32.20
Df Residuals:                       2   BIC:                             30.97
Df Model:                           1
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const        -25.0000     14.230     -1.757      0.221     -86.228      36.228
X            119.0000      5.196     22.902      0.002      96.643     141.357
==============================================================================
Omnibus:                          nan   Durbin-Watson:                   3.270
Prob(Omnibus):                    nan   Jarque-Bera (JB):                0.508
Skew:                          -0.663   Prob(JB):                        0.776
Kurtosis:                       1.863   Cond. No.                         7.47
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""
```

如果你只想获取这些信息而不是把它打印出来，可以使用 `a.showinfo_return()`

```python
b=a.showinfo_return()
print(b)
```

## LICENSE

[MIT LICENSE](LICENSE.txt)

## 关于作者😁

江苏省苏州市的一个普通高中牲，一个因为~玩电脑被学校处分~在省赛就被刷下来的信息学奥林匹克竞赛选手，热爱编程，但不喜欢前端。

欢迎通过以下联系方式与我探讨信息竞赛、博客搭建、学术讨论以及扯皮：

* QQ:36937975
* Twitter:@billma6688
* Facebook/Instagram:billma007
* CodeForces/USACO/AtCoder:billma007(~别看我很拉的~不常用)
* Email:[maboning237103015@163.com](mailto:maboning237103015@163.com)

## 推广：我的博客🤞

[欢迎光临！](https://billma.top/)
