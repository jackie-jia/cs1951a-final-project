import pandas as pd
import numpy as np
import scipy
from scipy.stats import ttest_ind
import re

meme_posts = pd.read_csv("/Users/nicksawicki/Desktop/Data_Science/The-Flintstones/data_deliverable/data/reddit/cleaned/meme_posts.csv")
meme_comments = pd.read_csv("/Users/nicksawicki/Desktop/Data_Science/The-Flintstones/data_deliverable/data/reddit/cleaned/meme_comments.csv")
proper_posts = pd.read_csv("/Users/nicksawicki/Desktop/Data_Science/The-Flintstones/data_deliverable/data/reddit/cleaned/proper_posts.csv")
proper_comments = pd.read_csv("/Users/nicksawicki/Desktop/Data_Science/The-Flintstones/data_deliverable/data/reddit/cleaned/proper_comments.csv")

# Emoji Remover Code: https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python 
# Re (Regular Expression Operations) https://docs.python.org/3/library/re.html 


proper_posts_list = proper_posts['selftext'].tolist()
meme_posts_list = meme_posts['selftext'].tolist()


emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
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
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)

def clean_data(dirty_data):
    clean_list = []
    for i in range(0, 1014): #  for i in range(0,len(dirty_data)):
        no_emoji = re.sub(emoj, '', dirty_data[i])
        no_symbols = re.sub(r'[^\w]', ' ', no_emoji)
        lower_case = no_symbols.lower()
        clean_list.append(lower_case)
    return clean_list
    

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


if __name__ == "__main__":
    proper_binary_list = scan_data(clean_data(proper_posts_list))
    meme_binary_list = scan_data(clean_data(meme_posts_list))
    two_sample_ttest(proper_binary_list, meme_binary_list)
    
