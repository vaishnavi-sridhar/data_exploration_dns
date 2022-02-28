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


def plot_graph4():
    content_as_dict = json.load(open('Graph4.txt', 'r'))

    labels = list(content_as_dict.keys())
    top1_domain =[]
    top2_domain = []
    for inner_dict in content_as_dict.values():
        for index, (key,value) in enumerate(inner_dict.items()):
            if index == 0:
                top1_domain.append(inner_dict[key])
            else:
                top2_domain.append(inner_dict[key])

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, top1_domain, width, label='Top1 domain')
    rects2 = ax.bar(x + width / 2, top2_domain, width, label='Top2 domain')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Domain query count')
    ax.set_xlabel('Time of day')
    ax.set_title('Top 2 domains for different times of the day')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()


def autolabel(rects,ax,values):
    for idx, rect in enumerate(rects):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1*height,
                values[idx],
                ha='center', va='bottom', rotation=0)
    return rects


# plot_graph1()
plot_graph4()
