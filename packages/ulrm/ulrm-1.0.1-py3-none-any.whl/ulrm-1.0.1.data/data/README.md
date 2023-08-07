# ✨✨✨Univariate Linear Regression Model✨✨✨

Univariate Linear Regression Model is what we must study in senior high school.This package is used to calculate Univariate Linear Regression Model and draw its picture.

**language:*English*/[Chinese](README-cn.md)**

## start quickly

```python
pip install ulrm
```

## use it in your progress

### Initialize data

#### you can use list to get data

```python
from ulrm import ULRM #import module

a = ULRM()

a.getdataway=False #use list to get data
a.list1=[1,2,3,4,5,6,7,8,9] #X axis
a.list2=[100,112,121,133,140,150,166,172,181] #y axis

a.xlabelset="X"
a.ylabelset="Y"
# set label name

a.readdata()


```

#### you can also use excel to get data

only support `*.xlsx` and `*.xls`

```python
a = ULRM()
a.getdataway=True #use excel to get data
a.excelget='example.xlsx' #get excel
a.xlabelset="X axis"
a.ylabelset="Y axls"

a.readdata()

```

#### Excel File Format Requirements

There must be two columns in the excel, the first column is the X-axis data, the second column is the Y-axis data, and the first row must be "X" and "Y". The data is recorded from the second row. For example, the following example is excellent:

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

### process data

you can get the function of the Univariate Linear Regression Model:

```python
print(a.getfunc())

#output(example):
# The linear model is: Y =119.0X+-25.0
```

you can draw the pictures:

```python
a.makeplt()
```

![output](https://fastly.jsdelivr.net/gh/billma007/imagesave/ulrmexample1.png)

you can print more information about this function:

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

if you only want the data,instead of print them,you can use `a.showinfo_return()`

```python
b=a.showinfo_return()
print(b)
```

## About

A student in Suzhou,People's Republic of China.An OIer.LIKE C++,C and Python.

* QQ:36937975
* Twitter:@billma6688
* Facebook/Instagram:billma007
* CodeForces/USACO/AtCoder:billma007(useless)
* Email:[maboning237103015@163.com](mailto:maboning237103015@163.com)

## LICENSE

[MIT LICENSE](LICENSE.txt)
