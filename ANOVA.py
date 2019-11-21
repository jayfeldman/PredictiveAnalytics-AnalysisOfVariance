{\rtf1\ansi\ansicpg1252\cocoartf2511
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python\
# coding: utf-8\
\
# # Analysis of Variance (ANOVA): Does number of plants per light matter?\
# BACKGROUND:  Assuming consistent canopy area, is there more yield with \
# more smaller plants or fewer larger plants?\
# \
\
from scipy import stats\
import numpy as np\
import matplotlib.pyplot as plt\
import pandas as pd\
import pingouin as pg\
import statsmodels\
import statsmodels.api as sm\
from statsmodels.formula.api import ols\
\
datafile = "PlantCountYield.csv"\
data = pd.read_csv(datafile)\
                 \
data.boxplot('Yields', by='PlantCount', figsize=(12, 8))\
plt.show()\
\
grps = pd.unique(data.PlantCount.values)\
d_data = \{grp:data['Yields'][data.PlantCount == grp] for grp in grps\}\
\
k = len(pd.unique(data.PlantCount))   # Number of groups\
N = len(data.values)                  # Number of datapoints total\
n = data.groupby('PlantCount').size() # Number of datapoints in each group\
\
group_averages = data.groupby('PlantCount').sum()['Yields']/n\
overall_average = sum(data['Yields'])/N\
\
data['GroupAverages'] = np.repeat(group_averages, 6).tolist()\
data['OverallAverage'] = overall_average\
\
SSTotal = sum((data['Yields'] - data['OverallAverage'])**2)\
SSWithin = sum((data['Yields'] - data['GroupAverages'])**2)\
SSBetween = sum((data['GroupAverages'] - data['OverallAverage'])**2)\
\
print("\\n\\nSum of Squares Between: \{:.2f\}. Degrees of Freedom: 3".format(SSBetween))\
print("Sum of Squares Within: \{:.2f\}. Degrees of Freedom: 20".format(SSWithin))\
print("Sum of Squares Total:  \{:.2f\}. Degrees of Freedom: 23\\n".format(SSTotal))    \
print("(SSB/DoF(SSB) / (SSW/DoF(SSW)) => F-statistic: \{:2f\}\\n\\n".format((SSBetween/3)/(SSWithin/20)))  \
\
aov = pg.anova(data=data, dv='Yields', between='PlantCount', detailed=True)\
print(aov)}