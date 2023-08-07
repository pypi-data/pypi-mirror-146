from setuptools import setup, find_packages


setup(
    name="ulrm",
    version="1.0.1",
    author="billma007",
    author_email="maboning237103015g@163.com",
    description="A module that can make Univariate Linear Regression Model",
    url="http://billma.top/", 
    packages=find_packages(),
    install_requires=[         
        'pandas',         
        'numpy',
        'matplotlib',
        'statsmodels',
        'sklearn'
    ],
    data_files=["README.md","README-cn.md","LICENSE.txt"]
)