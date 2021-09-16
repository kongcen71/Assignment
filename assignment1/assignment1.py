import pandas as pd
from matplotlib import pyplot as plt

print('So let`s begin the task!')
w_no=input('Please enter the number of the weeks in the month:')
t_no=input('Please enter the number of the tasks:')


list=[]
for i in range(int(t_no)):
    t_name=input('Please the name of No.'+str(i)+' task:')
    task = {'name': t_name}
    for f in range(int(w_no)):
        t_time=input('How many hours did Task '+str(t_name)+' in week'+str(f)+' cost?:')
        task['week'+str(f)]=t_time
    list.append(task)
print(list)

df=pd.DataFrame(list)
print(df)
df.to_csv('WeeklyTasks.csv',mode='w',index=False)

dff = pd.read_csv("WeeklyTasks.csv")
#print(dff)

#print(dff['week1'])
#print(dff.mean())
dff=dff.append(dff.mean(),ignore_index=True)
dff.iloc[-1,0]='avg'
print(dff)

x=range(dff.shape[1]-1)

for i in range(dff.shape[0]):
    plt.plot(x,dff.loc[i,'week0':])

plt.legend(dff['name'])
plt.xlabel("Week")
plt.ylabel("hrs")
plt.title('WeeklyTask')
plt.show()



