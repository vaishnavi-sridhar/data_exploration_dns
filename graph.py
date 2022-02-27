import json
import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy as np


def plot_graph1(inputfile,label_plot,x_axis, y_axis, title_plot):
    content_as_dict = json.load(open(inputfile, 'r'))
    actual_values = list(content_as_dict.values())
    print(np.array(actual_values))

    val = preprocessing.normalize([np.array(list(content_as_dict.values()))], norm='max')
    print(list(val[0]))
    fig, ax = plt.subplots()
    bar_plot = plt.bar(content_as_dict.keys(), list(val[0]), color='b', label=label_plot)

    bar_plot = autolabel(bar_plot,ax, actual_values)
    plt.xlabel(x_axis, fontsize=12)
    plt.ylabel(y_axis, fontsize=12)
    plt.title(title_plot, fontsize=15)
    plt.legend()
    plt.show()


def autolabel(rects,ax,values):
    for idx, rect in enumerate(rects):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1*height,
                values[idx],
                ha='center', va='bottom', rotation=0)
    return rects



#plot_graph1('Graph1.txt','DNS Record count','Times of day','No. of DNS records (normalized)','DNS record count (vs) Time of the day')
plot_graph1('Graph2.txt','Record Count','Query Type','Query Type Count','Query Type (vs) Count')
