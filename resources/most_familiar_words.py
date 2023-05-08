import pandas as pd

# Load the SUBTLEX-US corpus
# ['Word', 'FREQcount', 'CDcount', 'FREQlow', 'Cdlow', 'SUBTLWF', 'Lg10WF', 'SUBTLCD', 'Lg10CD', 'Dom_PoS_SUBTLEX', 'Freq_dom_PoS_SUBTLEX', 'Percentage_dom_PoS', 'All_PoS_SUBTLEX', 'All_freqs_SUBTLEX', 'Zipf-value']
subtlex_us = pd.read_excel("SUBTLEX-US frequency list with PoS and Zipf information.xlsx", engine='openpyxl', sheet_name='out1g')
subtlex_us = subtlex_us[subtlex_us['Word'].str.len() == 5]

# Select only the "Word" and "Zipf-value" columns
df_subset = subtlex_us[["Word", "Zipf-value"]]
# print(df_subset['Zipf-value'].median()) # 2.6897741508164974
# print(df_subset['Zipf-value'].mean()) # 2.8179383795207413
# print(df_subset['Zipf-value'].max()) # 6.637707562972593
# print(df_subset['Zipf-value'].min()) # 1.5928641378084412
# below_count = (df_subset['Zipf-value'] <= 3).sum()
# above_count = (df_subset['Zipf-value'] > 3).sum()
# print(f"Below: {below_count} - Above: {above_count}")
# print(f"Total words {below_count + above_count}")

# Write the contents to a file
df_subset.to_csv("word_freq_measure.txt", sep=",", index=False, header=False)

