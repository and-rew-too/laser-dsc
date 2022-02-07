import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

#https://sci-hub.se/https://pubmed.ncbi.nlm.nih.gov/33919970/
#T is a linear line from 380 to 520 K (10K / min), for 14 minutes
T= np.linspace(380,520,400)
HEATRATE = 10
TIME = (np.linspace(380,520,400) -T[0])/HEATRATE
#nonlinear line example #T= np.linspace(380,450,421) #T2 = np.linspace(450,380,420) #T = np.append([T],[T2])
Size = (len(T))
Stepsize = T[2]-T[1]
print(Stepsize)


# CURVE FITTING intially using Ea as a broad check to ensure that
# 1. obtained data made sense 2. advanced curve fitting below yields similar Ea values
# KAS Kissinger-Akahira-Sunose equation
# np.log(beta/Tp**2) = np.log(A*R/E) - (Ea/(8.314*Tp))
# y = const + (1/Tp) * (-Ea/8.314)
beta = np.zeros((4))
Tp = np.zeros((4))
beta[0:4] = [10,20,30,40]
Tp[0:4] = [193,207,216,223]



#solving for dalpha dT
#initialize alpha, fill this np array
alpha = np.zeros((Size))
A = np.exp(16.924)
m = 0.107
n = 0.973
E = 66830
HEATRATE= HEATRATE #reshown to iterate the importance of this variable
alpha[0] = 0.001
for i in range(0,Size-1):
    dalphadT = A*np.exp((-E)/(8.314*T[i]))*(alpha[i]**m)*((1-alpha[i])**n)
    #dalpha dT is the change in alpha under a Temp step (T[i+1]-T[i])
    alpha[i+1] = alpha[i] + (dalphadT*Stepsize/HEATRATE) #normalize temp step
print(T)

################################################################################
alpha = alpha
DaDT = np.zeros((Size)) #initialize dalphadT for curve fitting later
for i in range(0,Size-2):
    DaDT[i+1] = (alpha[i+1]-alpha[i])/Stepsize





#non-linear fit on the sestak berggren function given Y
Y = np.log(HEATRATE*DaDT) + E/(8.314*T)
Y[0] = Y[1]
Y[Size-1] = Y[Size-2]#remove first and last infinity value here
print(Y)  #Y, left hand side is found, now can use non-linear solver
def objective(alpha, m, n, A):
	return np.log(A)+m*np.log(alpha)+n*np.log(1-alpha)
popt, _ = curve_fit(objective, alpha, Y)
m, n, A = popt
print(A)
print(n)




#NOW given any temperature step ever, can determine the evolution of cure given these constants A,m,n,E
#HEATRATE, distance between T STILL NEEDED
XX = np.zeros((Size))
for i in range(0,Size-1):
    dalphadT = A*np.exp((-E)/(8.314*T[i]))*(XX[i]**m)*((1-XX[i])**n)
    XX[i+1] = XX[i] + dalphadT*Stepsize



#plotting the dadT plots below
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("fitted pFF","evolution of cure over time","Fig2b"))
fig.add_trace(go.Scatter(x=alpha, y=DaDT*HEATRATE),
              row=1, col=3)
fig.add_trace(go.Scatter(x=TIME, y=alpha),
              row=1, col=2)
fig.show()
