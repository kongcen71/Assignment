import pandas as pd
from matplotlib import pyplot as plt

dff = pd.read_csv("WeeklyTask.csv")
#print(dff)

#print(dff['week1'])
print(dff.mean())
dff=dff.append(dff.mean(),ignore_index=True)
print(dff)

dff.iloc[-1,0]='avg'

#print('!!!!!!',dff.iloc[-1,0])

print('coloum no:',dff.shape[1]-1)
print(dff.loc[0,'week0':])
x=range(dff.shape[1]-1)

for i in range(dff.shape[0]):
    plt.plot(x,dff.loc[i,'week0':])

plt.legend(dff['name'])
plt.xlabel("Week")
plt.ylabel("hrs")
plt.title('WeeklyTask')
plt.show()

#week=range()