import argparse
import json
import pandas as pd
import fileinput


def main():
    message = ("Data exploration - analyzing DNS files and aggregating data to derive insights through graphs.")
    parser = argparse.ArgumentParser(message,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input_file", type=str, required=True,
                        help="The dns log file(s) to use.",
                        default="/home/vasr2545/uncompressed_dns/2021-08-01_dns.01:00:00-02:00:00.log")
    FLAGS = parser.parse_args()
    # df = pd.read_csv(FLAGS.input_file,delimiter="\t", skiprows=8, header=None)
    aggregate_data(FLAGS.input_file)


def aggregate_data(input_file):
    df = pd.read_csv(input_file, delim_whitespace=True, skiprows=8, header=None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    header_names = ["ts", "uid", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p", "proto", "trans_id", "rtt",
                    "query",
                    "qclass", "qclass_name", "qtype", "qtype_name", "rcode", "rcode_name", "AA", "TC", "RD", "RA", "Z",
                    "answers", "TTLs", "rejected"]
    df.columns = header_names
    print("# of DNS records:", len(df.index))
    key = extract_tod(input_file.split("\\")[-1])
    content_as_dict = read_val("Graph1.txt")
    orig_val = 0
    if content_as_dict:
        if key in content_as_dict:
            orig_val = content_as_dict[key]
    value = orig_val + len(df.index)
    content_as_dict[key] = value
    append_to_file("Graph1.txt", content_as_dict)

    print("--------------------------")
    sub_df = df.groupby(['qtype_name']).size().reset_index(name='count').sort_values(['count'], ascending=False).head(100)
    print(type(sub_df))
    print("--------------------------")
    print(df.groupby(['query']).size().reset_index(name='count').sort_values(['count'], ascending=False).head(100))
    print("--------------------------")
    print(df.groupby(['query', 'qtype_name']).size().reset_index(name='count').sort_values(['count'],
                                                                                           ascending=False).head(
        100))
    print("--------------------------")
    print(df.groupby(['id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'trans_id']).size().reset_index(
        name='count').sort_values(['count'], ascending=False).head(100))
    # print(df.groupby(['id.orig_h','id.orig_p','id.resp_h','id.resp_p','trans_id']).size().reset_index(name='counts'))


def extract_tod(file_name):
    hour_limit = file_name.split(".")[1]
    return "Hours " + hour_limit.split(":")[0] + "-" + hour_limit.split("-")[1][0:2]


def append_to_file(name, dict):
    json.dump(dict, open(name, "w"))


def replace_row(old_text, new_text):
    f = open("Graph1.txt", "r+")
    f.write(fileinput.input)
    f.close()


def read_val(name):
    try:
        return json.load(open(name))
    except:
        return {}





if __name__ == '__main__':
    main()
