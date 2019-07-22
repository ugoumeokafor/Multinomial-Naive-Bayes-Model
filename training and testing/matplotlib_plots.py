import matplotlib.pyplot as plt
import numpy as np
import pandas


df = pandas.read_csv('country_visits.csv')
#df.plot(x=0)

plt.plot(df)
plt.show