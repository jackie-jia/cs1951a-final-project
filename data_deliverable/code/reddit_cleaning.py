import os
import pandas as pd

# Finds root directory of user
ROOT_DIR = os.path.dirname(os.path.abspath((__file__)))

'''POST DATA'''
# Reddit post data filepaths
BTC_posts_path = '/../data/reddit/CryptoMoonShots/bitcoin/posts.json'
ETH_posts_path = '/../data/reddit/CryptoMoonShots/ethereum/posts.json'
SOL_posts_path = '/../data/reddit/CryptoMoonShots/solana/posts.json'
DOGE_posts_path = '/../data/reddit/CryptoMoonShots/dogecoin/posts.json'
SHIB_posts_path = '/../data/reddit/CryptoMoonShots/shiba_inu/posts.json'
SUSHI_posts_path = '/../data/reddit/CryptoMoonShots/sushi/posts.json'

# Proper coin post data
btc_posts = pd.read_json(ROOT_DIR + BTC_posts_path)
btc_posts['coin'] = 'bitcoin'
eth_posts = pd.read_json(ROOT_DIR + ETH_posts_path)
eth_posts['coin'] = 'ethereum'
sol_posts = pd.read_json(ROOT_DIR + SOL_posts_path)
sol_posts['coin'] = 'solana'

proper_posts_df = pd.concat([btc_posts, eth_posts, sol_posts])
proper_posts_df = proper_posts_df.drop_duplicates(subset=['id', 'coin']).drop_duplicates(subset=['selftext', 'coin'])

# Meme coin post data
doge_posts = pd.read_json(ROOT_DIR + DOGE_posts_path)
doge_posts['coin'] = 'dogecoin'
shib_posts = pd.read_json(ROOT_DIR + SHIB_posts_path)
shib_posts['coin'] = 'shiba_inu'
sushi_posts = pd.read_json(ROOT_DIR + SUSHI_posts_path)
sushi_posts['coin'] = 'sushi'

meme_posts_df = pd.concat([doge_posts, shib_posts, sushi_posts])
meme_posts_df = meme_posts_df.drop_duplicates(subset=['id', 'coin']).drop_duplicates(subset=['selftext', 'coin'])



'''COMMENT DATA'''
# Reddit comment data filepaths
BTC_comments_path = '/../data/reddit/CryptoMoonShots/bitcoin/comments.json'
ETH_comments_path = '/../data/reddit/CryptoMoonShots/ethereum/comments.json'
SOL_comments_path = '/../data/reddit/CryptoMoonShots/solana/comments.json'
DOGE_comments_path = '/../data/reddit/CryptoMoonShots/dogecoin/comments.json'
SHIB_comments_path = '/../data/reddit/CryptoMoonShots/shiba_inu/comments.json'
SUSHI_comments_path = '/../data/reddit/CryptoMoonShots/sushi/comments.json'

# Proper coin comment data
btc_comments = pd.read_json(ROOT_DIR + BTC_comments_path)
btc_comments['coin'] = 'bitcoin'
eth_comments = pd.read_json(ROOT_DIR + ETH_comments_path)
eth_comments['coin'] = 'ethereum'
sol_comments = pd.read_json(ROOT_DIR + SOL_comments_path)
sol_comments['coin'] = 'solana'

proper_comments_df = pd.concat([btc_comments, eth_comments, sol_comments])
proper_comments_df = proper_comments_df.drop_duplicates(subset=['id', 'coin']).drop_duplicates(subset=['body', 'coin'])

# Meme coin comment data
doge_comments = pd.read_json(ROOT_DIR + DOGE_comments_path)
doge_comments['coin'] = 'dogecoin'
shib_comments = pd.read_json(ROOT_DIR + SHIB_comments_path)
shib_comments['coin'] = 'shiba_inu'
sushi_comments = pd.read_json(ROOT_DIR + SUSHI_comments_path)
sushi_comments['coin'] = 'sushi'

meme_comments_df = pd.concat([doge_comments, shib_comments, sushi_comments])
meme_comments_df = meme_comments_df.drop_duplicates(subset=['id', 'coin']).drop_duplicates(subset=['body', 'coin'])

# Store final dataframe as CSVs
PROPER_POSTS_PATH = ROOT_DIR + "/../data/reddit/cleaned/proper_posts.csv"
PROPER_COMMENTS_PATH = ROOT_DIR + "/../data/reddit/cleaned/proper_comments.csv"
MEME_POSTS_PATH = ROOT_DIR + "/../data/reddit/cleaned/meme_posts.csv"
MEME_COMMENTS_PATH = ROOT_DIR + "/../data/reddit/cleaned/meme_comments.csv"

proper_posts_df.to_csv(PROPER_POSTS_PATH, index=False)
proper_comments_df.to_csv(PROPER_COMMENTS_PATH, index=False)
meme_posts_df.to_csv(MEME_POSTS_PATH, index=False)
meme_comments_df.to_csv(MEME_COMMENTS_PATH, index=False)

# Store sample data
SAMPLE_POSTS_PATH = ROOT_DIR + "/../data/sample/sample_posts.csv"
SAMPLE_COMMENTS_PATH = ROOT_DIR + "/../data/sample/sample_comments.csv"

proper_posts_df.head(100).to_csv(SAMPLE_POSTS_PATH)
meme_comments_df.head(100).to_csv(SAMPLE_COMMENTS_PATH)