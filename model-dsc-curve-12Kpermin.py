import numpy as np
import pandas as pd
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from scipy.optimize import curve_fit


T = np.array([
108.0172,
109.0172,
110.0172,
111.0172,
112.0172,
113.0172,
114.0172,
115.0172,
116.0172,
117.0172,
118.0172,
119.0172,
120.0172,
121.0172,
122.0172,
123.0172,
124.0172,
125.0172,
126.0172,
127.0172,
128.0172,
129.0172,
130.0172,
131.0172,
132.0172,
133.0172,
])
T = T+273.15

FR12 = np.array([
0.5701,
0.97732,
1.67527,
2.84552,
4.69027,
7.19402,
9.82333,
11.90016,
13.15876,
13.56117,
13.33928,
12.64636,
11.59629,
10.29178,
8.79597,
7.2291,
5.74817,
4.47514,
3.42595,
2.61211,
2.03753,
1.62131,
1.34143,
1.16505,
1.03497,
0.9356])
print(T)


length = len(FR12)


deltaH = 0
for i in range(0,length-1):
    Astep = 0.5*(FR12[i+1]+FR12[i]) * 1
    deltaH = deltaH + Astep


alpha = np.zeros((length))

for i in range(0,length-1):
    truncateda = FR12[0:i]
    alpha[i] = (truncateda.sum())/deltaH
alpha[length-1]=0.999
print(alpha)

dalphadT = np.zeros((length))
for i in range(0,length-1):
    dalphadT[i] = (alpha[i+1]-alpha[i])/1
dalphadT[length-3] = 0.004
dalphadT[length-2] = 0.000
dalphadT[length-1] =-0.004
print(dalphadT)


#now finally have the dalphadT function can do non-linear regression to find n,m,A
#E = 134281

E = 98830
Y = np.log(12*dalphadT) + E/(8.314*T)
Y[length-1] = Y[length-3]
Y[length-2] = Y[length-3]

# then the fillna turns any NaN into just a 0
#Y.replace([np.inf, -np.inf], np.nan, inplace=True)
#Y.iloc[:,0] = Y.iloc[:,0].fillna(0)


#def objective(alpha, m, n, A):
#	return np.log(A)+m*np.log(alpha)+n*np.log(1-alpha)
#popt, _ = curve_fit(objective, alpha, Y)
#m, n, A = popt
def objective(alpha, m, n,  A):
	return np.log(A)+m*np.log(alpha)+n*np.log(1-alpha)
#popt, _ = curve_fit(objective, alpha, Y, maxfev=10000)
# https://www.desmos.com/calculator/pysdgucpz7
# DESMOS WAS GETTING A = 3.35*10^13 m = 0.688 n =0.943







time = np.linspace(0,20,length)
T = np.zeros([length])
T = T + 100 +273.15


###############################################################################
alpha = np.zeros((length))
alpha[0] = 0.01
m = 0.688
n = 0.943
A = 3.35*10**13
# does better with A = 5.35*10**12
dAdT = np.zeros((length))
for i in range(0,length-1):
    dAdT[i] = (A)*np.exp((-E)/(8.314*T[i]))*(alpha[i]**m)*((1-alpha[i])**n)
    alpha[i+1] = alpha[i] + (dAdT[i])
print(alpha)


fig = go.Figure()
fig.add_trace(go.Scatter(x=time, y=alpha,
                    mode='markers',
                    name='markers'))

fig.show()
