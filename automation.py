# This python script is used for running through each log file and generating dict file with aggregated data for
# plotting graph
import os
import aggregator


def main():
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".log"):
            aggregator.aggregate_data(filename)
        else:
            continue


if __name__ == '__main__':
    main()
