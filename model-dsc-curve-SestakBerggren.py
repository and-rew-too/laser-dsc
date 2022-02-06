import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

TIME = np.linspace(0,14,842)
#T is a linear line from 380 to 520 K (10K / min), for 14 minutes
T= np.linspace(380,520,842)
#T= np.linspace(380,450,421)
#T2 = np.linspace(450,380,420)
#T = np.append([T],[T2])



alpha = np.zeros((842)) #initialize alpha, fill up this np array
A = np.exp(16.924)
m = 0.107
n = 0.973
E = 66830
#print(alpha)
alpha[0] = 0.001
for i in range(0,841):
    dalphadt = A*np.exp((-E)/(8.314*T[i]))*(alpha[i]**m)*((1-alpha[i])**n)
    alpha[i+1] = alpha[i] + 0.1*0.16667*dalphadt
    # IF HEATING RATE IS 10, 1/10*stepsize of T
    # IF HEATING RATE IS 40, 1/4 * 1/10 * stepsize of T
print(alpha[:])
print(T)
#dalphadT = A*np.exp((-E)/(8.314*T))*alpha**m*(1-alpha)**n
#dalphadT = A*np.exp((-E)/(8.314*T))*alpha**m*(1-alpha)**n


################################################################################
alpha = alpha 
DaDt = np.zeros((842)) #initiaize dalphadT for curve fitting later
for i in range(0,840):
    DaDt[i+1] = (alpha[i+1]-alpha[i])/0.16667
Y = np.log(10*DaDt) + E/(8.314*T)
Y[0] = 16
Y[841] = 16 #need to remove the first and last infinity value here
print(Y) #initialize the 'Y' in the x-y curve fit below




def objective(alpha, m, n, A):
	return np.log(A)+m*np.log(alpha)+n*np.log(1-alpha)
popt, _ = curve_fit(objective, alpha, Y)
# summarize the parameter values
m, n, A = popt
print(A)
print(n)



fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("fitted pFF","real pFF","Voltage change/laser"))
fig.add_trace(go.Scatter(x=alpha, y=DaDt),
              row=1, col=3)
#fig.add_trace(go.Scatter(x=TIME, y=T),
#              row=1, col=3)
fig.show()
