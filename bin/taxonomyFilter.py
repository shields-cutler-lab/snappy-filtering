import csv
import pandas as pd


def convert_txt_to_csv(data):
    df = pd.read_fwf(data)
    df.to_csv(data)
    return data


def import_data(data):
    return pd.read_csv(data)


def csv_to_dict(data):
    reader = csv.DictReader(open(data))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list


def csv_to_array(data):
    reader = csv.reader(open(data))
    array = []
    for line in reader:
        array.append(line)
    return array


def original_num_of_otus(data):
    return len(csv_to_dict(data))


def original_num_of_samples(data):
    return len(csv_to_dict(data)[0]) - 1


def sum_of_all_counts(data):
    count = 0
    for i in range(1, len(csv_to_array(data)) - 1):
        for h in range(1, len(csv_to_array(data)[i])):
            count = count + int(csv_to_array(data)[i][h])
    return count


def otu_processor(data):
    x = int(input("Enter an integer to filter OTUs that have low total counts across the dataset"))
    y = float(input("Enter a float to filter OTUs that are present in onlt a small proportion of the samples"))
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
    print(sum_column)
    threshold = int(input("Enter an integer for a threshold to filter out the samples:"))
    for h in range(1, len(csv_to_array(data)[1])):
        sum_of_each_column = 0
        for i in range(1, len(csv_to_array(data))):
            sum_of_each_column = sum_of_each_column + int(csv_to_array(data)[i][h])
        if sum_of_each_column < threshold:
            column_name = csv_to_array(data)[0][h]
            df = df.drop([column_name], axis=1)
    return df


def processor(data):
    print("The sum of all counts in the entire table is:")
    print(sum_of_all_counts(data))
    df_after_otu_filter = otu_processor(data)
    df_after_both_filter = sample_processor(df_after_otu_filter)

    final_OTUs = df_after_both_filter.shape[0]
    final_samples = df_after_both_filter.shape[1] -1
    print("The original number of OTUs is :" + str(original_num_of_otus(data)))
    print("The original number of samples is :" + str(original_num_of_samples(data)))
    print("The final number of OTUs is: " + str(final_OTUs))
    print("The final number of samples is: " + str(final_samples))
    output_path = input("Enter a path to save the file: ")
    df_after_both_filter.to_csv(output_path)







if __name__ == '__main__':
    data = 'original_SIMULATED_OTUtable_ForTestOnly.csv'
    processor(data)

