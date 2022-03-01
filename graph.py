import json
import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy as np
import operator


def plot_graph1(inputfile, label_plot, x_axis, y_axis, title_plot):
    content_as_dict = json.load(open(inputfile, 'r'))
    actual_values = list(content_as_dict.values())
    print(np.array(actual_values))

    val = preprocessing.normalize([np.array(list(content_as_dict.values()))], norm='max')
    print(list(val[0]))
    fig, ax = plt.subplots()
    bar_plot = plt.bar(content_as_dict.keys(), list(val[0]), color='b', label=label_plot)
    bar_plot = autolabel(bar_plot, ax, actual_values)
    fig.autofmt_xdate()
    plt.xlabel(x_axis, fontsize=12)
    plt.ylabel(y_axis, fontsize=12)
    plt.title(title_plot, fontsize=15)
    plt.legend()
    plt.show()


def plot_graph2(inputfile, label_plot, x_axis, y_axis, title_plot):
    content_as_dict = json.load(open(inputfile, 'r'))
    content_as_dict = dict( sorted(content_as_dict.items(), key=operator.itemgetter(1),reverse=True))

    top5_dict = {}
    for index, (key, value) in enumerate(content_as_dict.items()):
        if index <= 4:
            top5_dict[key] = value
    print(top5_dict)
    actual_values = list(top5_dict.values())
    val = preprocessing.normalize([np.array(list(top5_dict.values()))], norm='max')

    fig, ax = plt.subplots()
    bar_plot = plt.bar(top5_dict.keys(), list(val[0]), color='b', label=label_plot)
    bar_plot = autolabel(bar_plot, ax, actual_values)
    fig.autofmt_xdate()
    plt.xlabel(x_axis, fontsize=12)
    plt.ylabel(y_axis, fontsize=12)
    plt.title(title_plot, fontsize=15)
    plt.legend()
    plt.show()


def plot_graph4():
    content_as_dict = json.load(open('Graph4-old.txt', 'r'))
    labels = list(content_as_dict.keys())
    top_domains = [[], [], [], [], []]
    for inner_dict in content_as_dict.values():
        sorted_tuples = sorted(inner_dict.items(), key=lambda item: item[1])
        print(sorted_tuples)
        inner_dict = {k: v for k, v in sorted_tuples}
        for index, (key, value) in enumerate(inner_dict.items()):
            if index <= 4:
                top_domains[index].append(inner_dict[key])

    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars
    print(content_as_dict)
    fig, ax = plt.subplots()
    rects = []
    rects.append(ax.bar(x - width / 2, top_domains[0], width, label='Top1 domain'))
    rects.append(ax.bar(x + width / 2, top_domains[1], width, label='Top2 domain'))
    rects.append(ax.bar(x + 1.5 * width, top_domains[2], width, label='Top3 domain'))
    rects.append(ax.bar(x + 2.5 * width, top_domains[3], width, label='Top4 domain'))
    rects.append(ax.bar(x + 3.5 * width, top_domains[4], width, label='Top5 domain'))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Domain query count')
    ax.set_xlabel('Time of day')
    ax.set_title('Top 5 domains for different times of the day')
    ax.set_xticks(x, labels)
    ax.legend()
    for i in range(5):
        ax.bar_label(rects[i], padding=10)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()


def plot_graph3():
    content_as_dict = json.load(open('Graph3.txt', 'r'))

    labels = list(content_as_dict.keys())
    query_type_counts = [[], [], [], [], []]

    for inner_dict in content_as_dict.values():
        for index, (key, value) in enumerate(inner_dict.items()):
            if index == 0:
                query_type_counts[index].append(inner_dict[key])
            else:

                query_type_counts[index].append(inner_dict[key])
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    rects = []
    rects.append(ax.bar(x - width / 2, query_type_counts[0], width, label='A'))
    rects.append(ax.bar(x + width / 2, query_type_counts[1], width, label='AAAA'))
    rects.append(ax.bar(x + 1.5 * width, query_type_counts[1], width, label='CNAME'))
    rects.append(ax.bar(x + 2.5 * width, query_type_counts[1], width, label='PTR'))
    rects.append(ax.bar(x + 3.5 * width, query_type_counts[1], width, label='NS'))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Domain query count')
    ax.set_xlabel('Time of day')
    ax.set_title('Common 5 query type counts for different times of the day')
    ax.set_xticks(x, labels)
    ax.legend()
    for i in range(5):
        ax.bar_label(rects[i], padding=10)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()


def autolabel(rects, ax, values):
    for idx, rect in enumerate(rects):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1 * height,
                values[idx],
                ha='center', va='bottom', rotation=0)
    return rects


# plot_graph1('Graph1.txt', 'DNS Record count', 'Times of day', 'No. of DNS records (normalized)', 'DNS record count (vs) Time of the day')
plot_graph2('Graph2.txt', 'Record Count', 'Query Type', 'Query Type Count', 'Query Type (vs) Count')
# plot_graph3()
# plot_graph4()
