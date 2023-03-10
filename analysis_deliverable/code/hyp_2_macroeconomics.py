import pandas as pd
import numpy as np
import scipy
from scipy.stats import ttest_ind
import re
import matplotlib.pyplot as plt
from collections import defaultdict

meme_posts = pd.read_csv("/Users/nicksawicki/Desktop/Data_Science/The-Flintstones/data_deliverable/data/reddit/cleaned/meme_posts.csv")
meme_comments = pd.read_csv("/Users/nicksawicki/Desktop/Data_Science/The-Flintstones/data_deliverable/data/reddit/cleaned/meme_comments.csv")
proper_posts = pd.read_csv("/Users/nicksawicki/Desktop/Data_Science/The-Flintstones/data_deliverable/data/reddit/cleaned/proper_posts.csv")
proper_comments = pd.read_csv("/Users/nicksawicki/Desktop/Data_Science/The-Flintstones/data_deliverable/data/reddit/cleaned/proper_comments.csv")

# Emoji Remover Code: https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python 
# Re (Regular Expression Operations) https://docs.python.org/3/library/re.html 


"""
Converts text column of the dataframe into a python list
"""
proper_posts_list = proper_posts['selftext'].tolist()
meme_posts_list = meme_posts['selftext'].tolist()

"""
Codes for emojies that get recognized by the re package and eliminated from a string
"""
emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002500-\U00002BEF"  
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  
        u"\u3030"
                      "]+", re.UNICODE)

"""
This method takes in a list and gets rid of all the emojies, symbols, and makes everything lowercase. 
It returns a cleaned list of all of the posts. 
"""
def clean_data(dirty_data):
    clean_list = []
    for i in range(0, 1014): #  for i in range(0,len(dirty_data)):
        no_emoji = re.sub(emoj, '', dirty_data[i])
        no_symbols = re.sub(r'[^\w]', ' ', no_emoji)
        lower_case = no_symbols.lower()
        clean_list.append(lower_case)
    return clean_list
    

"""
This method parses each line of the list into individual words and checks to 
see if any of the words in the post equal the finance words. If it does,
then a 1 will be added to an array indicating that the post contains content 
that relates to monetary policy. If the post is not related to monetary policy,
a 0 will be placed in the array instead. 
"""
def scan_data(formatted_list):
    post_counter = 0 
    finance_words = ['fed', 'rates', 'interest', 'gdp', 'nominal', 'cpi']
    word_flag = False   
    post_tracker_list = []
    for i in range(0, len(formatted_list)):
        split_entry = formatted_list[i].split()
        for j in range(0, len(split_entry)):
            for k in range(0, len(finance_words)):
                if finance_words[k] == split_entry[j]:
                    word_flag = True
        if word_flag:
            post_counter = post_counter + 1
            post_tracker_list.append(1)
        else:
            post_tracker_list.append(0) 
        word_flag = False

    return post_tracker_list


def two_sample_ttest(values_a, values_b):
    tstats, pvalue = scipy.stats.ttest_ind(values_a, values_b, nan_policy='omit')
    print(tstats, pvalue)

    # t-statistic: 2.900667250991424    p-value: 0.003763836254154633


def get_value_counts_table(data, col_name):
  count_dict = defaultdict(int)
  def update_count_dict(r):
    count_dict[r[col_name]] += 1
  data.apply(lambda x: update_count_dict(x), axis=1)
  rows = [[e, count_dict[e]] for e in count_dict]
  return pd.DataFrame(rows, columns=[col_name, "count"])




if __name__ == "__main__":
    proper_binary_list = scan_data(clean_data(proper_posts_list))
    meme_binary_list = scan_data(clean_data(meme_posts_list))
    two_sample_ttest(proper_binary_list, meme_binary_list)
   
    
    # print(df)

    # Data Visualization
    proper_list_df = pd.DataFrame(proper_binary_list, columns=['isFinance'])
    proper_count_table = get_value_counts_table(proper_list_df, "isFinance")
    proper_count_table["count"].plot(kind='pie', labels=proper_count_table["count"], startangle=90, autopct='%1.1f%%', title='Num Posts With Financial Terms (Proper Coins)')
    print(proper_count_table)
    plt.savefig("Proper.png")

    meme_list_df = pd.DataFrame(meme_binary_list, columns=['isFinance'])
    meme_count_table = get_value_counts_table(meme_list_df, "isFinance")
    meme_count_table["count"].plot(kind='pie', labels=meme_count_table["count"], startangle=90, autopct='%1.1f%%', title='Num Posts With Financial Terms (Meme Coins)')
    print(meme_count_table)
    plt.savefig("Meme.png")
