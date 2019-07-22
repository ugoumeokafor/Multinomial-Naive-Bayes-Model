from matplotlib import pyplot, dates
from csv import reader

#to plot likelihood of 29_go, 88_go and 29_nogo, 88_nogo
with open('C:\Users\Ugochukwu\Desktop\GIS classes\Directed research\matplotlib\likelyhood_set_ugo.csv', 'r') as f:
    data = list(reader(f))

temp = [i[1] for i in data[1::]]
time = [i[2] for i in data[1::]]
#pls add two more lines for nogo

pyplot.plot(time, temp)
pyplot.title("Likelihood probabilities of features belonging to class 29 & class 88")
pyplot.xlabel("Features (country codes)")
pyplot.ylabel("Percentage")
pyplot.show()