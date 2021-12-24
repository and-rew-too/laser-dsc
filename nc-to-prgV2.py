import numpy as np
import pandas as pd

# cell parameters needed here
# busbarpitch = ??? currently set to 36.1
# celldimensions = ?? 166 or 156.75
# shinglewidth = ?? 156 or 133
Power = 30
wsh = 12

if (wsh >= 5) & (wsh < 18):
    wshcut = 18.05-wsh
elif (Wsh >= 18) & (wsh < 54):
    wshcut = 36.1-wsh
else:
    print("bruh huh why are you cutting shit that large/small")
    exit()

# DATAFRAME START initial three rows of laser cuts
sdf = pd.DataFrame(np.zeros([3,7])*np.nan)
sdf.iloc[0,0:3] = 'Y-axis', 0, 8.5
sdf.iloc[1:3,0:3] = 'X-axis', 167, 0
#print(sdf)



# DATAFRAME MIDDLE
pd.set_option('display.width', None)
ROWS = 50
df = pd.DataFrame(np.zeros([ROWS,7])*np.nan)

iloop = 0
numloop = int(156//(Wsh+Wshcut) )
for j in range(0,numloop):
#for j in range(0,4):
    for i in range(iloop,iloop+6):
        if (i+1) % 6 == 0:
            df.iloc[i,0:3] = "Y-axis", 0, Wshcut
        elif (i+1) % 3 == 0:
            df.iloc[i,0:3] = "Y-axis", 0, Wsh
        else:
            df.iloc[i,0:3] = "X-axis", 167, 0
    iloop = iloop + 6
# now the middle portion is finished
# but the very last y-axis 9.6 is extra, and doesn't need to be cut
# code below goes through df, any NaN rows get dropped, along wit hthe very last non-NaN y-axis value
is_NaN = df.isnull()
for kk in range(0,len(df.index)):
    if is_NaN.iloc[kk,0] == True:
        df.drop(labels=kk-1, inplace=True)
    else:
        pass
df.drop(labels=0, inplace=True) #first X-axis 0.0 row that isn't used
df.drop(labels=1, inplace=True) #second X-axis 0.0 row that isn't used
df.drop(labels=ROWS-1, inplace=True) #additional NaN row that isn't used


#DATAFRAME END
edf = pd.DataFrame(np.zeros([6,7])*np.nan)
edf.iloc[0,0:3] = 'X-axis', 3.625, 0
edf.iloc[1,0:3] = 'Y-axis', 0, -135
edf.iloc[2,0:3] = 'Y-axis', 0, 135
edf.iloc[3,0:3] = 'X-axis', 167-8.25, 0
edf.iloc[4,0:3] = 'Y-axis', 0, -135
edf.iloc[5,0:3] = 'Y-axis', 0, 135
#print(edf)


# compiles the start, middle, end into one single dataframe
df = pd.concat([sdf, df, edf])
# this takes col 1 values has the 167, 167 turn into 167 -167
for i in range(1,len(df.index)):
    if df.iloc[i-1,1] == 167:
        df.iloc[i,1] = -df.iloc[i,1]
    else:
        pass
df.iloc[:,3] = 400
df.iloc[:,4] = "ON"
df.iloc[:,5] = "Valid"
df.iloc[:,6] = Power
print(df)

with open('C:/users/andre/Downloads/ncprgtest.txt', 'a') as f:
    dfAsString = df.to_string(header=False, index=False)
    f.write(dfAsString)
