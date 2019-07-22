import matplotlib.pyplot as plt
import pandas as pd
#to plot a histogram
data = pd.read_csv('country_visits.csv', header = None)

plt.plot(data)
plt.title("Visiting patterns for United States traverlers")
plt.xlabel("Countries visited")
plt.ylabel("Number of user visits")
plt.show()
