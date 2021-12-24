import numpy as np
import pandas as pd

pd.set_option('display.width', None)
data = [
'Z12.700 ' ,
'G1Z-1.270F203.2 ' ,
'X120.000Y174.000F508.0 ' ,
'X162.000Y72.000 ' ,
'X60.000Y156.000 ' ,
'X192.000Y144.000 ' ,
'X66.000Y72.000 ' ,
'Z-2.540F203.2 ' ,
'X120.000Y174.000F508.0 ' ,
'X162.000Y72.000 ' ,
'X60.000Y156.000 ' ,
'X192.000Y144.000 ' ,
'X66.000Y72.000 ' ,
'Z12.700 ' ,
'M02 ' ]

df = pd.DataFrame(data, columns = ['Name']) #converts str to a df and then splits txt to columns
coords = df["Name"].str.split("X", n = 1, expand = True)
df["xpos"] = coords[1]
df["xpos"] = df["xpos"].str.slice(0,6)
coords = df["Name"].str.split("Y", n = 1, expand = True)
df["ypos"] = coords[1]
df["ypos"] = df["ypos"].str.slice(0,6)

df["ypos"] = df["ypos"].astype(float) #briefly converts to float for math operations
df["ypos"] = df["ypos"].mul(1)
df["ypos"] = df["ypos"].astype(str)


dfwrite = 'Line#' + df['xpos'] + '#' + df['ypos'] + '#400#ON#Valid#30'
nullboolean = dfwrite[dfwrite.isnull()]
dfwrite.drop(nullboolean.index, inplace=True)

with open('C:/users/andre/Downloads/testprg.txt', 'a') as f:
    dfAsString = dfwrite.to_string(header=False, index=False)
    f.write(dfAsString)
#print(dfwrite)
