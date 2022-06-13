import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import plotly.graph_objects as go
#doublecheck curve fit
#https://www.desmos.com/calculator/5wczwp0vth


#Xval below is the temps, taken at each temp curve fit line
Xval = np.array([
25, 85, 125, 150])
#Yval below is the val in amperes
Yval = np.array([35,2000,12500,40000])
Yval = Yval/1000

def func(x, a,b):
	return a*x**5+b*x**4

popt, _ = curve_fit(func,Xval,Yval)
a,b = popt
print(b)

xstar = np.linspace(10,40,31)
ystar = func(xstar,a,b)
print(xstar)
exit()

fig = go.Figure()
fig.add_trace(go.Scatter(x=xstar, y=ystar,
                    mode='lines',
                    name='lines'))
fig.show()

