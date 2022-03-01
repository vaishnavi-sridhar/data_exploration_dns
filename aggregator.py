import argparse
import json
import pandas as pd
import fileinput
from collections import OrderedDict


def main():
    message = ("Data exploration - analyzing DNS files and aggregating data to derive insights through graphs.")
    parser = argparse.ArgumentParser(message,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input_file", type=str, required=False,
                        help="The dns log file(s) to use.",
                        default="/home/vasr2545/uncompressed_dns/2021-08-01_dns.00:00:00-01:00:00.log")
    FLAGS = parser.parse_args()
    aggregate_data(FLAGS.input_file)


def aggregate_data(input_file):
    df = pd.read_csv(input_file, delim_whitespace=True, skiprows=8, header=None)#uncomment this setting on local
    #df = pd.read_csv(input_file,delimiter="\t", skiprows=8, header=None) #uncomment this setting on server
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    header_names = ["ts", "uid", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p", "proto", "trans_id", "rtt",
                    "query",
                    "qclass", "qclass_name", "qtype", "qtype_name", "rcode", "rcode_name", "AA", "TC", "RD", "RA", "Z",
                    "answers", "TTLs", "rejected"]
    df.columns = header_names
    generate_graph1_data(df, input_file)
    generate_graph2_data(df)
    generate_graph4_data(df, input_file)
    generate_graph3_data(df, input_file)

    # print(df.groupby(['query', 'qtype_name']).size().reset_index(name='count').sort_values(['count'],ascending=False).head(5))

    #
    # print(df.groupby(['id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'trans_id']).size().reset_index(
    #     name='count').sort_values(['count'], ascending=False).head(100))
    # print(df.groupby(['id.orig_h','id.orig_p','id.resp_h','id.resp_p','trans_id']).size().reset_index(name='counts'))


def generate_graph2_data(df):
    sub_df = df.groupby(['qtype_name']).size().reset_index(name='count').sort_values(['count'], ascending=False).head(
        100)
    print(type(sub_df))
    qtype_dict = {}
    for item in sub_df.to_dict('split')['data']:
        key = 'None' if item[0] == '-' else item[0]
        qtype_dict[key] = item[1]
    print(qtype_dict)
    append_to_file("Graph2.txt", qtype_dict)


def generate_graph1_data(df, input_file):
    print("# of DNS records:", len(df.index))
    key = extract_tod(input_file.split("\\")[-1])
    content_as_dict = read_content_from_file("Graph1.txt")
    orig_val = 0
    if content_as_dict:
        if key in content_as_dict:
            orig_val = content_as_dict[key]
    value = orig_val + len(df.index)
    content_as_dict[key] = value
    content_as_dict = OrderedDict(sorted(content_as_dict.items()))
    append_to_file("Graph1.txt", content_as_dict)

def generate_graph3_data(df, input_file):
    print("--------------------------")
    lst = ['A', 'AAAA', 'NS', 'PTR', 'CNAME']
    sub_df = df.groupby(['qtype_name']).size().reset_index(name='count').sort_values(['count'], ascending=False).query('qtype_name in @lst')
    print("--------------------------")
    time_of_day = extract_tod(input_file.split("\\")[-1])
    content_as_dict = read_content_from_file("Graph3.txt")
    q_dict = {}
    for item in sub_df.to_dict('split')['data']:
        if item[0] != "-" and item[0] != "(empty)":
            q_dict[item[0]] = item[1]
    print(q_dict)
    for i in ['A','AAAA','PTR','CNAME', 'NS']:
        if i not in q_dict.keys():
            q_dict[i] = 0
    for key in q_dict.keys():
        if key not in ['A','AAAA','PTR','CNAME', 'NS']: 
            q_dict.pop(key)
    if time_of_day not in content_as_dict.keys():
        content_as_dict[time_of_day] = q_dict
    else:
        for item in q_dict.items():
            key = item[0]
            val = item[1]
            orig_inner_dict = content_as_dict[time_of_day]
            orig_domain_count = 0
            if key not in orig_inner_dict.keys():
                orig_inner_dict[key] = val
            else:
                orig_domain_count = orig_inner_dict[key]
                orig_inner_dict[key] = orig_domain_count + val
        content_as_dict[time_of_day] = orig_inner_dict
    content_as_dict = OrderedDict(sorted(content_as_dict.items()))
    print(content_as_dict)
    append_to_file("Graph3.txt", content_as_dict)

def generate_graph4_data(df, input_file):
    print("--------------------------")
    sub_df = df.groupby(['query']).size().reset_index(name='count').sort_values(['count'], ascending=False).head(5)
    print("--------------------------")
    time_of_day = extract_tod(input_file.split("\\")[-1])
    content_as_dict = read_content_from_file("Graph4.txt")
    q_dict = {}
    for item in sub_df.to_dict('split')['data']:
        if item[0] != "-" and item[0] != "(empty)":
            q_dict[item[0]] = item[1]
    print(q_dict)

    if time_of_day not in content_as_dict.keys():
        content_as_dict[time_of_day] = q_dict
    else:
        for item in q_dict.items():
            key = item[0]
            val = item[1]
            orig_inner_dict = content_as_dict[time_of_day]
            orig_domain_count = 0
            if key not in orig_inner_dict.keys():
                orig_inner_dict[key] = val
            else:
                orig_domain_count = orig_inner_dict[key]
                orig_inner_dict[key] = orig_domain_count + val
        content_as_dict[time_of_day] = orig_inner_dict
    content_as_dict = OrderedDict(sorted(content_as_dict.items()))
    print(content_as_dict)
    append_to_file("Graph4.txt", content_as_dict)




def extract_tod(file_name):
    hour_limit = file_name.split(".")[1]
    return "Hours " + hour_limit.split(":")[0] + "-" + hour_limit.split("-")[1][0:2]


def append_to_file(name, dict):
    json.dump(dict, open(name, "w"))


def replace_row(old_text, new_text):
    f = open("Graph1.txt", "r+")
    f.write(fileinput.input)
    f.close()


def read_content_from_file(name):
    try:
        return json.load(open(name))
    except:
        return {}


if __name__ == '__main__':
    main()
