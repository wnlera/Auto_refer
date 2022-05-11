import pandas as pd
import os
import sentence_filter

# df = pd.read_csv('../big_files/citation.csv')
# df["sentence"] = df["sentence"].astype('str')
# df_big_sentence = df.loc[df["sentence"].str.len() > 184]
# start_lem = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# df_big_sentence = df_big_sentence.loc[df_big_sentence["sentence"].apply(lambda x: (str(x)[0] in start_lem) and (str(x)[-1] == "."))]
# df_big_sentence["file_name"] = df_big_sentence["file_name"].apply(lambda x: x.replace(x, "".join(x.split("/")[-1])))
# df_big_sentence = df_big_sentence.loc[df_big_sentence["sentence"].apply(lambda x: sentence_filter.get_unic_word_percent(x) > 40)]
#
# df_file_name = '../big_files/big_sentence.csv'
# df_big_sentence.to_csv(df_file_name, encoding='utf-8', index=False)


# Create df with list of links
# df = pd.read_csv('../big_files/big_sentence.csv')
# df_group = df.groupby(["file_name", "sentence"])["citation_number_from_sentence"].apply(list).reset_index(name='links')
# df_file_name = '../big_files/group_link.csv'
# df_group.to_csv(df_file_name, encoding='utf-8', index=False)
