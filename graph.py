import json
import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy as np


def plot_graph(inputfile, label_plot, x_axis, y_axis, title_plot):
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


plot_graph('Graph1.txt', 'DNS Record count', 'Times of day', 'No. of DNS records (normalized)', 'DNS record count (vs) Time of the day')
plot_graph('Graph2.txt', 'Record Count', 'Query Type', 'Query Type Count', 'Query Type (vs) Count')
plot_graph4()
