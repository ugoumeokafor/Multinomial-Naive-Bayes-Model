import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

class Draw:
    def __init__(self):
        self.fig, (self.ax1,self.ax2) = plt.subplots(1,2,sharey=True)
        self.fig, (self.ax) = plt.subplots()
        self.path = r"E:/directed_research/tables and results_trimmed_data/matplotlib_ugo/"
        self.file_histogram = 'country_visits.csv'
        self.file_likelyhodd = 'likelyhood_stackedbar.csv'
        self.file_posterior_probability = r"pp_stackedbar.csv"
        self.width = 0.65
        self.seed = 2535


    def bar(self):
        filename = self.path+self.file_histogram
        with open(filename, "r") as csvfile:
            data = pd.read_csv(csvfile,header=None, names=('country','visits'))
            country = (data['country']).tolist()
            visits = data['visits'].tolist()
            x = np.arange(1,11)
            self.ax.bar(x, visits, self.width)
            #refer to https://matplotlib.org/examples/api/barchart_demo.html
            #set up the x ticks and labels
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(country, rotation=65, fontsize=30)
            # set up y labels,
            self.ax.set_ylim([0, 450])
            self.ax.set_yticklabels(np.arange(0, 500, 50), fontsize=20)
            self.ax.set_ylabel('# of Visits', fontsize=40)
            #set up grid lines
            #set up background color
            plt.show()

    def stackedBar(self):
        #random.seed(self.seed)
        #features = random.sample(xrange(256),10)
        file_name = self.path+self.file_likelyhodd
        ind = np.arange(10)
        listgo_legend = []
        listnogo_legend = []
        base_go =np.zeros(10)
        base_nogo = np.zeros(10)
        with open(file_name,"r") as csvfile:
            data = pd.read_csv(csvfile)
            xlabel = data['Features']
            headers_go = ['29_go','88_go','206_go','8_go','64_go','71_go','85_go','187_go','23_go','153_go']
            headers_nogo = ['29_nogo','88_nogo','206_nogo','8_nogo','64_nogo','71_nogo','85_nogo','187_nogo','23_nogo','153_nogo']
            data_go = data[headers_go]
            legend = ['29','88','206','8','64','71','85','187','23','153']
            data_nogo = data[headers_nogo]

            for i in range(0,10):
                row_go = data_go.iloc[:,i]
                row_go =row_go.tolist()
                row_nogo = data_nogo.iloc[:,i]
                row_nogo = row_nogo.tolist()
                p_go = self.ax1.bar(ind,row_go,self.width, bottom=base_go)
                p_nogo = self.ax2.bar(ind, row_nogo, self.width,bottom=base_nogo)
                listgo_legend.append(p_go)
                listnogo_legend.append(p_nogo)
                base_go += row_go
                base_nogo += row_nogo

            self.ax1.legend(listgo_legend,legend, title="Classes",fontsize=15)
            self.ax2.legend(listnogo_legend, legend, title="Classes", fontsize=15)
            # set up the x ticks and labels
            x = np.arange(0, 10)
            self.ax1.set_xlabel('Features',fontsize=35)
            self.ax2.set_xlabel('Features',fontsize=35)
            #set up 2 subtiles
            self.ax1.set_title('Likelihoods of Visit to Class',fontsize=20)
            self.ax2.set_title('Likelihoods of no Visit to Class',fontsize=20)
            self.ax1.set_xticks(x)
            self.ax2.set_xticks(x)
            self.ax1.set_xticklabels(xlabel,fontsize=20)
            self.ax2.set_xticklabels(xlabel,fontsize=20)
            # set up y labels,
            self.ax1.set_ylim([0, 0.40])
            self.ax1.set_yticklabels(np.arange(0.00, 0.45, 0.05),fontsize=20)
            self.ax1.set_ylabel('Percentage', fontsize=35)
            # set up title
            #self.fig.suptitle("Likelyhoods of Features", fontsize=14)

            plt.show()

    def stackedBar_pp(self):
        # random.seed(self.seed)
        # features = random.sample(xrange(256),10)
        file_name = self.path + self.file_posterior_probability
        ind = np.arange(10)
        listgo_legend = []
        listnogo_legend = []
        base_go = np.zeros(10)
        base_nogo = np.zeros(10)
        with open(file_name, "r") as csvfile:
            data = pd.read_csv(csvfile)
            xlabel = data['Features']
            headers_go = ['29_go', '88_go', '206_go', '8_go', '64_go', '71_go', '85_go', '187_go', '23_go', '153_go']
            headers_nogo = ['29_nogo', '88_nogo', '206_nogo', '8_nogo', '64_nogo', '71_nogo', '85_nogo', '187_nogo',
                            '23_nogo', '153_nogo']
            data_go = data[headers_go]
            legend = ['29', '88', '206', '8', '64', '71', '85', '187', '23', '153']
            data_nogo = data[headers_nogo]

            for i in range(0, 10):
                row_go = data_go.iloc[:, i]
                row_go = row_go.tolist()
                row_nogo = data_nogo.iloc[:, i]
                row_nogo = row_nogo.tolist()
                p_go = self.ax1.bar(ind, row_go, self.width, bottom=base_go)
                p_nogo = self.ax2.bar(ind, row_nogo, self.width, bottom=base_nogo)
                listgo_legend.append(p_go)
                listnogo_legend.append(p_nogo)
                base_go += row_go
                base_nogo += row_nogo

            self.ax1.legend(listgo_legend, legend, title="Classes", fontsize=15)
            self.ax2.legend(listnogo_legend, legend, title="Classes", fontsize=15)
            # set up the x ticks and labels
            x = np.arange(0, 10)
            self.ax1.set_xlabel('Users', fontsize=35)
            self.ax2.set_xlabel('Users', fontsize=35)
            # set up 2 subtiles
            self.ax1.set_title('Posteriors of Users belonging to Class', fontsize=20)
            self.ax2.set_title('Posteriors of Users not belonging to Class', fontsize=20)
            self.ax1.set_xticks(x)
            self.ax2.set_xticks(x)
            self.ax1.set_xticklabels(xlabel, fontsize=20)
            self.ax2.set_xticklabels(xlabel, fontsize=20)
            # set up y labels,
            self.ax1.set_ylim([0.000, 0.010])
            self.ax1.set_yticklabels(np.arange(0.000, 0.012, 0.002), fontsize=20)
            self.ax1.set_ylabel('Percentage', fontsize=35)
            # set up title
            # self.fig.suptitle("Likelyhoods of Features", fontsize=14)

            plt.show()

if __name__ == "__main__":
    obj = Draw()
    #obj.bar()
    obj.stackedBar()
    #obj.stackedBar_pp()





