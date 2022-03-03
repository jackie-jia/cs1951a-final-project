import praw
from praw.models import MoreComments
from psaw import PushshiftAPI
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

"""
api = PushshiftAPI()
def data_prep_posts(subreddit, start_time, end_time, filters, limit):
    if(len(filters) == 0):
        filters = ['id', 'author', 'created_utc',
                   'domain', 'url',
                   'title', 'num_comments']                 
                   #We set by default some useful columns

    print("hello")
    posts = list(api.search_submissions(
        subreddit=subreddit,   #Subreddit we want to audit
        after=start_time,      #Start date
        #before=end_time,       #End date
        filter=filters,        #Column names we want to retrieve
        limit=limit))          ##Max number of posts
    print("hello")

    return pd.DataFrame(posts) #Return dataframe for analysis

def count_posts_per_date(df_p, title, xlabel, ylabel):
    df_p.groupby([df_p.datetime.dt.date]).count().plot(y='id', rot=45, kind='bar', label='Posts')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def main():
    subreddit = "CryptoMoonShots"     #Subreddit we are auditing
    start_time = int(dt.datetime(2021, 12, 1).timestamp())  
                                     #Starting date for our search
    end_time = int(dt.datetime(2021, 3, 1).timestamp())   
                                     #Ending date for our search
    filters = []                     #We don´t want specific filters
    limit = 1000                     #Elelemts we want to recieve

    #Here we are going to get subreddits for a brief analysis
    #Call function for dataframe creation of comments
    df_p = data_prep_posts(subreddit,start_time,
                         end_time,filters,limit) 

    #Drop the column on timestamp format
    df_p['datetime'] = df_p['created_utc'].map(
        lambda t: dt.datetime.fromtimestamp(t))
    df_p = df_p.drop('created_utc', axis=1) 
    #Sort the Row by datetime               
    df_p = df_p.sort_values(by='datetime')  
    #Convert timestamp format to datetime for data analysis               
    df_p["datetime"] = pd.to_datetime(df_p["datetime"])

    # get comments for brief analysis
    # term = 'bitcoin'            #Term we want to search for
    # limit = 10                  #Number of elelemts 
    # df_c = data_prep_comments(term, start_time, end_time, filters, limit)
    #Call function for dataframe creation of comments

    #Function to plot the number of posts per day on the specified subreddit
    count_posts_per_date(df_p, 'Post per day', 'Days', 'posts')


if __name__ == '__main__':
    main()
"""

def scrapeSubreddit(subreddit_name, keywords, coin_name):

    reddit = praw.Reddit(client_id='T9am9v3IGT4Dtj73TTzG2g', client_secret='f9C3Leopd1q5g8mKYHee99wP39fZmw', user_agent='Jacqueline Jia')

    subreddits = []
    for word in keywords:
        subreddits.append(reddit.subreddit(subreddit_name).search(word, 'hot'))
        subreddits.append(reddit.subreddit(subreddit_name).search(word, 'relevance'))
        subreddits.append(reddit.subreddit(subreddit_name).search(word, 'top'))
        
    post_dict = {'id': [], 'created_utc': [], 'title': [], 'selftext': [],
             'num_comments': [], 'score': [], 'upvote_ratio': []}

    comment_dict = {'id': [], 'submission_id': [], 'created_utc': [], 'body': [], 'score': []}

    for subreddit in subreddits:
        for post in subreddit:
            post_dict['id'].append(post.id)
            post_dict['created_utc'].append(post.created_utc)
            post_dict['title'].append(post.title)
            post_dict['selftext'].append(post.selftext)
            post_dict['num_comments'].append(post.num_comments)
            post_dict['score'].append(post.score)
            post_dict['upvote_ratio'].append(post.upvote_ratio)
        
            post.comments.replace_more(limit=None)
            for comment in post.comments.list():
                comment_dict['id'].append(comment.id)
                comment_dict['submission_id'].append(comment.link_id)
                comment_dict['created_utc'].append(comment.created_utc)
                comment_dict['body'].append(comment.body)
                comment_dict['score'].append(comment.score)
    
    post_dict, comment_dict = pd.DataFrame(post_dict), pd.DataFrame(comment_dict)
    post_dict.to_json('../data/reddit/' + subreddit_name + '/' + coin_name + '/posts.json')
    comment_dict.to_json('../data/reddit/' + subreddit_name + '/' + coin_name + '/comments.json')
    
    # if sorted_by.equals('top'):
    #     subreddit = reddit.subreddit(subreddit).search('bitcoin').top('all')
    # elif sorted_by.equals('controversial'):
    #     subreddit = reddit.subreddit(subreddit).controversial('all')
    # elif sorted_by.equals('hot'):
    #     subreddit = reddit.subreddit(subreddit).hot('all')
    # elif sorted_by.equals('relevance'):
    #     subreddit = reddit.subreddit(subreddit).relevance('all')

    # post_dict, comment_dict = pd.DataFrame(post_dict), pd.DataFrame(comment_dict)
    # #indexNames = post_dict[(post_dict.body == '[removed]') | (post_dict.body == '[deleted]')].index
    # #post_dict.drop(indexNames, inplace=True)
    # post_dict.to_json('CryptoMoonShots_posts.json')
    # comment_dict.to_json('CryptoMoonShots_comments.json')

def main():
    bitcoin = ['bitcoin', 'btc']
    ethereum = ['ethereum', 'eth', 'ether']
    solana =  ['solana', 'sol']

    dogecoin = ['dogecoin', 'doge']
    sushi = ['sushi']
    shiba_inu = ['Shiba inu', 'shib', 'shb']

    subreddit = 'CryptoMoonShots'
    scrapeSubreddit(subreddit, bitcoin, 'bitcoin')
    scrapeSubreddit(subreddit, ethereum, 'ethereum')
    scrapeSubreddit(subreddit, solana, 'solana')
    scrapeSubreddit(subreddit, dogecoin, 'dogecoin')
    scrapeSubreddit(subreddit, sushi, 'sushi')
    scrapeSubreddit(subreddit, shiba_inu, 'shiba_inu')


if __name__ == '__main__':
    main()
