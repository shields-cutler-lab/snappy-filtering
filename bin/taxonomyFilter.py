import sys
import csv
import pandas as pd


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
    return array


def original_num_of_otus(data):
    return len(csv_to_dict(data))


def original_num_of_samples(data):
    return len(csv_to_dict(data)[0]) - 1


def sum_of_all_counts(data):
    df = import_data(data)
    df = df.drop([df.columns[0]], axis=1)
    return df.values.sum()


# I rewrite this function to avoid loops
def otu_processor(data):
    x = int(input("Enter an integer to filter OTUs that have low total counts across the data set: "))
    y = float(input("Enter a float to filter OTUs that are present in only a small proportion of the samples: "))
    df = import_data(data)
    sum_row = df.sum(axis=1)
    num_non_zero = df.astype(bool).sum(axis=1)
    otu_bool = pd.Series((sum_row > x) & (num_non_zero/original_num_of_samples(data) * 100 >= y))
    df = df[otu_bool.values]
    return df


def sample_processor(otudf):
    sum_column = otudf.sum(axis=0)
    print(sum_column.sort_values(ascending=True))
    threshold = int(input("Enter an integer for a threshold to filter out the samples:"))
    samp_bool = pd.Series(sum_column >= threshold)  # Creates a boolean (true/false) series based on the threshold
    otudf = otudf[otudf.columns[samp_bool]]  # Uses the boolean to select only columns that are "true" by the threshold test above
    return otudf


def processor():
    print("The sum of all counts in the entire OTU table is: %d" % sum_of_all_counts(data))
    df_after_otu_filter = otu_processor(data)
    df_after_both_filter = sample_processor(df_after_otu_filter)
    final_OTUs = df_after_both_filter.shape[0]
    final_samples = df_after_both_filter.shape[1]
    print("The original number of OTUs is : " + str(original_num_of_otus(data)))
    print("The original number of samples is : " + str(original_num_of_samples(data)))
    print("The final number of OTUs is: " + str(final_OTUs))
    print("The final number of samples is: " + str(final_samples))
    output_path = input("Enter a path to save the OTU table: ")
    df_after_both_filter.to_csv(output_path, sep='\t')


def delete_column(metadata, filter_list):
    metadf = import_data(metadata)
    metadf = metadf[metadf.index.isin(filter_list)]
    return metadf


def processor_with_metadata(metadata):
    print("The sum of all counts in the entire OTU table is: %d" % sum_of_all_counts(data))
    df_after_otu_filter = otu_processor(data)
    df_after_both_filter = sample_processor(df_after_otu_filter)
    df_metadata_after_sample_filter = delete_column(metadata, list(df_after_both_filter.columns))
    final_OTUs = df_after_both_filter.shape[0]
    final_samples = df_after_both_filter.shape[1]
    print(df_metadata_after_sample_filter)
    print("The original number of OTUs is : " + str(original_num_of_otus(data)))
    print("The original number of samples is : " + str(original_num_of_samples(data)))
    print("The final number of OTUs is: " + str(final_OTUs))
    print("The final number of samples is: " + str(final_samples))
    output_path1 = input("Enter a path to save the OTU table: ")
    df_after_both_filter.to_csv(output_path1, sep='\t')
    output_path2 = input("Enter a path to save the metadata file: ")
    df_metadata_after_sample_filter.to_csv(output_path2, sep='\t')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Must provide original input table')
        sys.exit()
    data = sys.argv[1]
    print(data)
    if len(sys.argv) == 3:
        metadata = sys.argv[2]
        processor_with_metadata(metadata)
    else:
        processor()

