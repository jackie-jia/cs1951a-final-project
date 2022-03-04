import praw
import pandas as pd

def scrape_subreddit(subreddit_name, keywords, coin_name):

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

def main():
    bitcoin = ['bitcoin', 'btc']
    ethereum = ['ethereum', 'eth', 'ether']
    solana =  ['solana', 'sol']

    dogecoin = ['dogecoin', 'doge']
    sushi = ['sushi']
    shiba_inu = ['Shiba inu', 'shib', 'shb']

    subreddit = 'CryptoMoonShots'
    scrape_subreddit(subreddit, bitcoin, 'bitcoin')
    scrape_subreddit(subreddit, ethereum, 'ethereum')
    scrape_subreddit(subreddit, solana, 'solana')
    scrape_subreddit(subreddit, dogecoin, 'dogecoin')
    scrape_subreddit(subreddit, sushi, 'sushi')
    scrape_subreddit(subreddit, shiba_inu, 'shiba_inu')

if __name__ == '__main__':
    main()