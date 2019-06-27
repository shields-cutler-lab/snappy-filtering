import sys
import csv
import pandas as pd


def import_data(data):
    return pd.read_csv(data, delimiter="\t")


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
    return array


def original_num_of_otus(data):
    return len(csv_to_dict(data))


def original_num_of_samples(data):
    return len(csv_to_dict(data)[0]) - 1


def find_smallest(list):
    list2 = list.copy()
    if list2[0] == 'Total Counts':
        list2.remove('Total Counts')
    list2.sort()
    return list2[0]


def find_smallest_index(list):
    list2 = list.copy()
    if list2[0] == 'Total Counts':
        list2.remove('Total Counts')
    return list2.index(min(list2))


def sum_of_all_counts(data):
    df = import_data(data)
    df = df.drop([df.columns[0]], axis=1)
    return df.values.sum()


def otu_processor(data):
    x = int(input("Enter an integer to filter OTUs that have low total counts across the data set: "))
    y = float(input("Enter a float to filter OTUs that are present in only a small proportion of the samples: "))
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
            df = df.drop(i-1)
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
    for i in range(0, len(index_list)-1):
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
    delete_column_index = list()
    for h in range(1, len(df_list[1])):
        sum_of_each_column = 0
        for i in range(1, len(df_list)):
            sum_of_each_column = sum_of_each_column + int(df_list[i][h])
        if sum_of_each_column < threshold:
            column_name = csv_to_array(data)[0][h]
            delete_column_index.append(h-1)
            df = df.drop([column_name], axis=1)
    return df, delete_column_index


def processor():
    print("The sum of all counts in the entire OTU table is: %d" % sum_of_all_counts(data))
    df_after_otu_filter = otu_processor(data)
    df_after_both_filter, delete_column_name = sample_processor(df_after_otu_filter)
    final_OTUs = df_after_both_filter.shape[0]
    final_samples = df_after_both_filter.shape[1] - 1
    print("The original number of OTUs is : " + str(original_num_of_otus(data)))
    print("The original number of samples is : " + str(original_num_of_samples(data)))
    print("The final number of OTUs is: " + str(final_OTUs))
    print("The final number of samples is: " + str(final_samples))
    output_path = input("Enter a path to save the OTU table: ")
    df_after_both_filter.to_csv(output_path, sep=' ')


def delete_column(metadata, list):
    df = import_data(metadata)
    df = df.drop(list, axis=0)
    return df


def processor_with_metadata():
    print("The sum of all counts in the entire OTU table is: %d" % sum_of_all_counts(data))
    df_after_otu_filter = otu_processor(data)
    df_after_both_filter, delete_column_index = sample_processor(df_after_otu_filter)
    df_metadata_after_sample_filter = delete_column(metadata, delete_column_index)
    final_OTUs = df_after_both_filter.shape[0]
    final_samples = df_after_both_filter.shape[1] - 1
    print("The original number of OTUs is : " + str(original_num_of_otus(data)))
    print("The original number of samples is : " + str(original_num_of_samples(data)))
    print("The final number of OTUs is: " + str(final_OTUs))
    print("The final number of samples is: " + str(final_samples))
    output_path1 = input("Enter a path to save the OTU table: ")
    df_after_both_filter.to_csv(output_path1, sep='\t', index=False)
    output_path2 = input("Enter a path to save the metadata file: ")
    df_metadata_after_sample_filter.to_csv(output_path2, sep='\t', index=False)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Must provide original input table')
        sys.exit()
    data = sys.argv[1]
    if len(sys.argv) == 3:
        metadata = sys.argv[2]
        processor_with_metadata()
    else:
        processor()

