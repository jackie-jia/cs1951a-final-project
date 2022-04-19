import numpy as np
import pandas as pd
from datetime import datetime
import scipy
from scipy.stats import ttest_ind

## CLEAN POST DATA ## 

# convert unix timestamps to dates
proper_posts = pd.read_csv("../../data_deliverable/data/reddit/cleaned/proper_posts.csv")
proper_posts['created_utc'] = pd.to_datetime(proper_posts['created_utc'], unit='s')
proper_posts['created_utc'] = proper_posts['created_utc'].apply(lambda x: x.date())

meme_posts = pd.read_csv("../../data_deliverable/data/reddit/cleaned/meme_posts.csv")
meme_posts['created_utc'] = pd.to_datetime(meme_posts['created_utc'], unit='s')
meme_posts['created_utc'] = meme_posts['created_utc'].apply(lambda x: x.date())

# get posts per day
proper_post_days = proper_posts.created_utc.unique()
proper_post_freqs = []

for day in proper_post_days:
    proper_post_freqs.append(proper_posts[proper_posts['created_utc'] == day].size)

meme_post_days = meme_posts.created_utc.unique()
meme_post_freqs = []

for day in meme_post_days:
    meme_post_freqs.append(meme_posts[meme_posts['created_utc'] == day].size)

print("MAX POSTS: ", max(meme_post_freqs), max(proper_post_freqs))
print("MIN POSTS: ", min(meme_post_freqs), min(proper_post_freqs))

## CLEAN COMMENT DATA ## 

# convert unix timestamps to dates
proper_comments = pd.read_csv("../../data_deliverable/data/reddit/cleaned/proper_comments.csv")
proper_comments['created_utc'] = pd.to_datetime(proper_comments['created_utc'], unit='s')
proper_comments['created_utc'] = proper_comments['created_utc'].apply(lambda x: x.date())

meme_comments = pd.read_csv("../../data_deliverable/data/reddit/cleaned/meme_comments.csv")
meme_comments['created_utc'] = pd.to_datetime(meme_comments['created_utc'], unit='s')
meme_comments['created_utc'] = meme_comments['created_utc'].apply(lambda x: x.date())


# get comments per day
proper_comment_days = proper_comments.created_utc.unique()
proper_comment_freqs = []

for day in proper_comment_days:
    proper_comment_freqs.append(proper_comments[proper_comments['created_utc'] == day].size)

meme_comment_days = meme_comments.created_utc.unique()
meme_comment_freqs = []

for day in meme_comment_days:
    meme_comment_freqs.append(meme_comments[meme_comments['created_utc'] == day].size)


print("MAX COMMENTS: ", max(meme_comment_freqs), max(proper_comment_freqs))
print("MIN COMMENTS: ", min(meme_comment_freqs), min(proper_comment_freqs))
# min is 6 for both; we can assume that lack of days in data is not due to having no posts, but rather due to not scraping the data


## RUN T TEST ## 

def two_sample_ttest(values_a, values_b):
    ## Stencil: Error check input - do not modify this part
    
    # TODO: Use scipy's ttest_ind
    # (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html)
    # to get the t-statistic and the p-value
    # Note: Be sure to make the function call in a way such that the code will disregard
    # null (nan) values. Additionally, you can assume equal variance.
    tstats, pvalue = scipy.stats.ttest_ind(values_a, values_b, nan_policy='omit')

    # TODO: You can print out the tstats, pvalue, and other necessary
    # calculations to determine your answer to the questions
    print(tstats, pvalue)

    # and then we'll return tstats and pvalue
    return tstats, pvalue

#### PROPER POST FREQUENCY VS MEME POST FREQUENCY #### 

t_post, p_post = two_sample_ttest(proper_post_freqs, meme_post_freqs)
# tstat = 2.7997, pval = 0.0053

#### PROPER COMMENT FREQUENCY VS MEME COMMENT FREQUENCY #### 
t_commment, p_comment = two_sample_ttest(proper_comment_freqs, meme_comment_freqs)
# tstat = 3.8502, pval = 0.00013