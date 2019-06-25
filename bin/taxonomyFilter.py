import sys
import csv
import pandas as pd


def convert_txt_to_csv(data):
    df = pd.read_fwf(data)
    df.to_csv(data)
    return data


def import_data(data):
    return pd.read_csv(data, delimiter="\t", header=0, index_col=0)


def csv_to_dict(data):
    reader = csv.DictReader(open(data), delimiter='\t')
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list


def csv_to_array(data):
    reader = csv.reader(open(data), delimiter='\t')
    array = []
    for line in reader:
        array.append(line)
    print(array)
    return array


def original_num_of_otus(data):
    return len(csv_to_dict(data))


def original_num_of_samples(data):
    return len(csv_to_dict(data)[0]) - 1


def find_smallest(list):
    smallest = list[1]
    for i in range(1, len(list)):
        if list[i] < smallest:
            smallest = list[i]
    return smallest


def find_smallest_index(list):
    smallest = list[1]
    index = 1
    for i in range(1, len(list)):
        if list[i] < smallest:
            smallest = list[i]
            index = i
    return index


def sum_of_all_counts(data):
    count = 0
    for i in range(1, len(csv_to_array(data)) - 1):
        for h in range(1, len(csv_to_array(data)[i])):
            count = count + int(csv_to_array(data)[i][h])
    return count


def otu_processor(data):
    x = int(input("Enter an integer to filter OTUs that have low total counts across the dataset: "))
    y = float(input("Enter a float to filter OTUs that are present in onlt a small proportion of the samples: "))
    df = import_data(data)
    for i in range(1, len(csv_to_array(data))):
        sum_of_row = 0
        num_of_non0 = 0
        for h in range(1, len(csv_to_array(data)[i])):
            sum_of_row = sum_of_row + int(csv_to_array(data)[i][h])
            if int(csv_to_array(data)[i][h]) > 0:
                num_of_non0 = num_of_non0 + 1
        percentage = (num_of_non0 / original_num_of_samples(data)) * 100
        if sum_of_row <= x or percentage < y:
            df = df.drop(i - 1)
    return df


def sample_processor(df):
    sum_column = df.sum(axis=0)
    index_list = list(sum_column.index.values)
    value_list = list(sum_column.values)
    index_list[0] = "SampleID"
    value_list[0] = "Total Counts"
    new_index_list = list()
    new_value_list = list()
    new_index_list.append(index_list[0])
    new_value_list.append(value_list[0])
    for i in range(0,len(index_list)-1):
        smallest = find_smallest(value_list)
        smallest_index = find_smallest_index(value_list)
        new_value_list.append(smallest)
        new_index_list.append(index_list[smallest_index])
        index_list.remove(index_list[smallest_index])
        value_list.remove(smallest)
    new_series = pd.Series(new_value_list, index=new_index_list)
    print(new_series)
    threshold = int(input("Enter an integer for a threshold to filter out the samples:"))
    df_list = list(df.values)
    for h in range(1, len(df_list[1])):
        sum_of_each_column = 0
        for i in range(1, len(df_list)):
            sum_of_each_column = sum_of_each_column + int(df_list[i][h])
        if sum_of_each_column < threshold:
            column_name = csv_to_array(data)[0][h]
            df = df.drop([column_name], axis=1)
    return df


def processor(data):
    print("The sum of all counts in the entire table is: %d" % sum_of_all_counts(data))
#     print(sum_of_all_counts(data))
    df_after_otu_filter = otu_processor(data)
    df_after_both_filter = sample_processor(df_after_otu_filter)

    final_OTUs = df_after_both_filter.shape[0]
    final_samples = df_after_both_filter.shape[1] -1
    print("The original number of OTUs is : " + str(original_num_of_otus(data)))
    print("The original number of samples is : " + str(original_num_of_samples(data)))
    print("The final number of OTUs is: " + str(final_OTUs))
    print("The final number of samples is: " + str(final_samples))
    output_path = input("Enter a path to save the file: ")
    df_after_both_filter.to_csv(output_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Must provide original input table')
        sys.exit()
    data = sys.argv[1]
    processor(data)

