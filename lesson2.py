import numpy as np
import pandas as pd

total=0

for i in range(7):
    tep=input('Today`s temp is:')
    tep=float(tep)
    fah=(tep*9/5)+32
    print('It`s ',fah,' in Fahrenheit')
    total=total+fah

print('The avarage Fahrenhait is ',round(total/7,2))