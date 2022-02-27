import json
import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy as np


def plot_graph1():
    content_as_dict = json.load(open('Graph1.txt', 'r'))
    actual_values = list(content_as_dict.values())
    print(np.array(actual_values))

    val = preprocessing.normalize([np.array(list(content_as_dict.values()))], norm='max')
    print(list(val[0]))
    fig, ax = plt.subplots()
    bar_plot = plt.bar(content_as_dict.keys(), list(val[0]), color='b', label='DNS Record count')

    bar_plot = autolabel(bar_plot,ax, actual_values)
    plt.xlabel('Times of day', fontsize=12)
    plt.ylabel('No. of DNS records (normalized)', fontsize=12)
    plt.title('DNS record count (vs) Time of the day', fontsize=15)
    plt.legend()
    plt.show()


def autolabel(rects,ax,values):
    for idx, rect in enumerate(rects):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1*height,
                values[idx],
                ha='center', va='bottom', rotation=0)
    return rects


plot_graph1()
