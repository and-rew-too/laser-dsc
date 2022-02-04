import plotly
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import math

directory = "C:/Users/andre/Downloads/20min130.txt"
pd.set_option('display.width', None)

dfL130 = pd.read_csv("C:/Users/andre/Downloads/20min130.txt", names=['Temp','Time','Response','Sens.'], skiprows=38, sep='\;', engine='python')
dfM130 = pd.read_csv("C:/Users/andre/Downloads/15min130.txt", names=['Temp','Time','Response','Sens.'], skiprows=38, sep='\;', engine='python')
dfS130 = pd.read_csv("C:/Users/andre/Downloads/10min130.txt", names=['Temp','Time','Response','Sens.'], skiprows=38, sep='\;', engine='python')

dfL145 = pd.read_csv("C:/Users/andre/Downloads/20min145.txt", names=['Temp','Time','Response','Sens.'], skiprows=38, sep='\;', engine='python')
dfM145 = pd.read_csv("C:/Users/andre/Downloads/15min145.txt", names=['Temp','Time','Response','Sens.'], skiprows=38, sep='\;', engine='python')
dfS145 = pd.read_csv("C:/Users/andre/Downloads/10min145.txt", names=['Temp','Time','Response','Sens.'], skiprows=38, sep='\;', engine='python')

dfL155 = pd.read_csv("C:/Users/andre/Downloads/20min155.txt", names=['Temp','Time','Response','Sens.'], skiprows=38, sep='\;', engine='python')
dfM155 = pd.read_csv("C:/Users/andre/Downloads/15min155.txt", names=['Temp','Time','Response','Sens.'], skiprows=38, sep='\;', engine='python')
dfS155 = pd.read_csv("C:/Users/andre/Downloads/10min155.txt", names=['Temp','Time','Response','Sens.'], skiprows=38, sep='\;', engine='python')
control = pd.read_csv("C:/Users/andre/Downloads/0min25.txt", names=['Temp','Time','Response','Sens.'], skiprows=38, sep='\;', engine='python')

LSIDE = 2100
RSIDE = 2300 #THIS IS FROM 88.9 c TO 96 c
print(sum(dfL130.iloc[LSIDE:RSIDE,2])/200)

L130shift = sum(dfL130.iloc[LSIDE:RSIDE,2])/(200)
M130shift = sum(dfM130.iloc[LSIDE:RSIDE,2])/(200)
S130shift = sum(dfS130.iloc[LSIDE:RSIDE,2])/(200)
L145shift = sum(dfL145.iloc[LSIDE:RSIDE,2])/(200)
M145shift = sum(dfM145.iloc[LSIDE:RSIDE,2])/(200)
S145shift = sum(dfS145.iloc[LSIDE:RSIDE,2])/(200)
L155shift = sum(dfL155.iloc[LSIDE:RSIDE,2])/(200)
M155shift = sum(dfM155.iloc[LSIDE:RSIDE,2])/(200)
S155shift = sum(dfS155.iloc[LSIDE:RSIDE,2])/(200)
controlshift = sum(control.iloc[LSIDE:RSIDE,2])/(200)

dfL130['Response'] = dfL130['Response'] + abs(L130shift)
dfM130['Response'] = dfM130['Response'] + abs(M130shift)
dfS130['Response'] = dfS130['Response'] + abs(S130shift)
dfL145['Response'] = dfL145['Response'] + abs(L145shift)
dfM145['Response'] = dfM145['Response'] + abs(M145shift)
dfS145['Response'] = dfS145['Response'] + abs(S145shift)
dfL155['Response'] = dfL155['Response'] + abs(L155shift)
dfM155['Response'] = dfM155['Response'] + abs(M155shift)
dfS155['Response'] = dfS155['Response'] + abs(S155shift)
control['Response'] = control['Response'] + abs(controlshift)


Ltemp = 3700
Rtemp = 5000 # AREA UNDER CURVE FROM 143C - 186C
print(dfL130.iloc[Ltemp:Rtemp,0])

#trapzoidal integration is 1/2 b * h  OR 1/2 * y(n)+y(n+1) * deltax
AL130 = 0
AM130 = 0
AS130 = 0
AL145 = 0
AM145 = 0
AS145 = 0
AL155 = 0
AM155 = 0
AS155 = 0
control25 = 0
for i in range(Ltemp,Rtemp):
    Astep = 0.5*(dfL130.iloc[i+1,2]+dfL130.iloc[i,2]) * ( dfL130.iloc[i+1,0]-dfL130.iloc[i,0] )
    AL130 = AL130+Astep
    bstep = 0.5*(dfM130.iloc[i+1,2]+dfM130.iloc[i,2]) * ( dfM130.iloc[i+1,0]-dfM130.iloc[i,0] )
    AM130 = AM130+bstep
    cstep = 0.5*(dfS130.iloc[i+1,2]+dfS130.iloc[i,2]) * ( dfS130.iloc[i+1,0]-dfS130.iloc[i,0] )
    AS130 = AS130+cstep
    dstep = 0.5*(dfL145.iloc[i+1,2]+dfL145.iloc[i,2]) * ( dfL145.iloc[i+1,0]-dfL145.iloc[i,0] )
    AL145 = AL145+dstep
    estep = 0.5*(dfM145.iloc[i+1,2]+dfM145.iloc[i,2]) * ( dfM145.iloc[i+1,0]-dfM145.iloc[i,0] )
    AM145 = AM145+estep
    fstep = 0.5*(dfS145.iloc[i+1,2]+dfS145.iloc[i,2]) * ( dfS145.iloc[i+1,0]-dfS145.iloc[i,0] )
    AS145 = AS145+fstep
    gstep = 0.5*(dfL155.iloc[i+1,2]+dfL155.iloc[i,2]) * ( dfL155.iloc[i+1,0]-dfL155.iloc[i,0] )
    AL155 = AL155+gstep
    hstep = 0.5*(dfM155.iloc[i+1,2]+dfM155.iloc[i,2]) * ( dfM155.iloc[i+1,0]-dfM155.iloc[i,0] )
    AM155 = AM155+hstep
    istep = 0.5*(dfS155.iloc[i+1,2]+dfS155.iloc[i,2]) * ( dfS155.iloc[i+1,0]-dfS155.iloc[i,0] )
    AS155 = AS155+istep
    jstep = 0.5*(control.iloc[i+1,2]+control.iloc[i,2]) * ( control.iloc[i+1,0]-control.iloc[i,0] )
    control25 = control25+jstep
print(AM155)




area = pd.DataFrame(np.array([AL130,AM130,AS130,AL145,AM145,AS145,AL155,AM155,AS155]))
cure = pd.DataFrame(np.array([0,0,0,0,0,0,0,0,0]))
for i in range(0,9):
    cure.iloc[i,0] = (control25-area.iloc[i,0])/control25
print(area)
print(cure)




X = pd.DataFrame(np.zeros([18, 1]))
Y = pd.DataFrame(np.zeros([18, 1]))

X.iloc[:, 0] = [130, 130, 130, 140, 140, 140, 150, 150,
                150, 130, 130, 130, 145, 145, 145, 155, 155, 155]
Y.iloc[:, 0] = [0.37, 0.426, 0.407, 0.547, 0.736, 0.791, 0.780, 0.871,
                0.888, 0.293, 0.169, 0.494, 0.340, 0.481, 0.560, 0.451, 0.658, 0.828]


fig.add_trace(go.Scatter(x=X.iloc[0:9, 0], y=Y.iloc[0:9, 0],
                         mode='markers',
                         name='Old Bridgestone EVA',
                         marker_color='lightskyblue'))
fig.add_trace(go.Scatter(x=X.iloc[10:18, 0], y=Y.iloc[10:18, 0],
                         mode='markers',
                         name='New RC028 EVA'))



fig = go.Figure()
# fig.add_trace(go.Scatter(x=dfS130.iloc[:,0], y=dfS130.iloc[:,2],
#                     mode='markers',
#                     name='markers'))
# fig.add_trace(go.Scatter(x=dfL130.iloc[:,0], y=dfL130.iloc[:,2],
#                     mode='markers',
#                     name='markers'))
# fig.add_trace(go.Scatter(x=dfM130.iloc[:,0], y=dfM130.iloc[:,2],
#                     mode='markers',
#                     name='markers'))
# fig.add_trace(go.Scatter(x=dfL155.iloc[:,0], y=dfL155.iloc[:,2],
#                     mode='markers',
#                     name='markers'))
# fig.add_trace(go.Scatter(x=dfL145.iloc[:,0], y=dfL145.iloc[:,2],
#                     mode='markers',
#                     name='markers'))
#
# fig.add_trace(go.Scatter(x=control.iloc[:,0], y=control.iloc[:,2],
#                     mode='markers',
#                     name='markers'))

fig.show()
