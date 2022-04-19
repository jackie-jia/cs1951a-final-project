import numpy as np
import pandas as pd
from nltk.tokenize.casual import TweetTokenizer
from nltk.corpus import stopwords
import json
from os import path
import string
import re
import emoji
from itertools import chain
from collections import Counter
from math import isnan

# Pre-Processing Hyperparameters ------
# Threshold frequency at which words aren't considered for dictionary
FREQUENCY = 1
# Maximum number of hours a post takes to affect price
TIMEFRAME = 3

# Finds root directory of user
ROOT_DIR = path.dirname(path.abspath((__file__)))

# Coin data filepaths (in CSV format)
PROPER_COINS = '/../../../data_deliverable/data/coin/cleaned/proper_coin_data.csv'
MEME_COINS = '/../../../data_deliverable/data/coin/cleaned/meme_coin_data.csv'

# Reddit data filepaths (in CSV format)
PROPER_POSTS = '/../../../data_deliverable/data/reddit/cleaned/proper_posts.csv'
PROPER_COMMENTS = '/../../../data_deliverable/data/reddit/cleaned/proper_comments.csv'
MEME_POSTS = '/../../../data_deliverable/data/reddit/cleaned/meme_posts.csv'
MEME_COMMENTS = '/../../../data_deliverable/data/reddit/cleaned/meme_comments.csv'

# Final data filenames (in NPY format)
PROPER_DATA = 'proper_data.npy'
MEME_DATA = 'meme_data.npy'

def retrieve_reddit_data(coin_type):
	'''
	Gets reddit text data of desired type from csv files in data folder.

	coin_type (str): Either "proper" or "meme"
	
	return: pd.DataFrame containing comments and posts of desired type.
	'''
	POSTS_PATH = ''
	COMMENTS_PATH = ''
	if coin_type == 'proper':
		POSTS_PATH = ROOT_DIR + PROPER_POSTS
		COMMENTS_PATH = ROOT_DIR + PROPER_COMMENTS
	else:
		POSTS_PATH = ROOT_DIR + MEME_POSTS
		COMMENTS_PATH = ROOT_DIR + MEME_COMMENTS
	posts_df = pd.read_csv(POSTS_PATH)
	comments_df = pd.read_csv(COMMENTS_PATH)
	# Retrieve necessary and compatible columns, rename them
	posts_df = posts_df[['created_utc', 'selftext', 'coin']]
	posts_df.rename(columns={'created_utc': 'time', 'selftext': 'text'}, inplace=True)
	comments_df = comments_df[['created_utc', 'body', 'coin']]
	comments_df.rename(columns={'created_utc': 'time', 'body': 'text'}, inplace=True)
	df = pd.concat([posts_df, comments_df])
	# print(f"The concatenated raw dataframe is {df}.")
	return df

def _separate_emojis(post, emojis):
	'''
	Separates emojis in input post/comment.

	post (str): post to modify.
	emojis (set): Set of emojis
	
	return: str
	'''
	return ''.join(' ' + char if char in emojis else char for char in post)

def _contains_number(word):
	'''
	Check if an input word contains a number.

	word (str): Word to check.
	
	return: Boolean
	'''
	for char in word:
		if char.isdigit():
			return True
	return False

def _tokenize(post, stop_words, emojis):
	'''
	Helper function that tokenizes posts/comments by words, and removes common stop words, and non-emoji words
	that have a number in them.

	post (str): Text to tokenize.
	stop_words (set): Set of stop words not to tokenize.
	emojis (set): Set of emojis
	
	return: (list) Tokenized text.
	'''
	words = TweetTokenizer().tokenize(post)
	filtered_words = []
	for w in words:
		# Make sure word is not a stopword
		if w not in stop_words:
			# Ensure it doesn't contain a number or is an emoji
			if not _contains_number(w) or w in emojis:
				filtered_words.append(w)
	return filtered_words

def clean_text(df):
	'''
	Cleans reddit text data: removes punctuation and whitespace, tokenizes, and removes common words

	df (pandas.DataFrame): pd.DataFrame containing combined posts and comments data with three columns:
	['time', 'text', 'coin']
	
	return: pd.DataFrame with text column cleaned
	'''
	# Ensure column type is string
	df = df.astype({'text': str})
	# Dictionary of punctuations to remove
	characters = [char for char in string.punctuation]
	punctuation = {}
	for char in characters:
		punctuation[ord(char)] = None
	# Set of emojis to keep/separate
	emojis = set(emoji.UNICODE_EMOJI['en'])
	# Remove links, remove punctuation, switch to lowercase, separate emojis
	df[['text']] = df['text'].apply(lambda x: _separate_emojis(re.sub(r'http\S+', '', x).translate(punctuation).lower(), emojis))
	# Tokenize, remove standard stopwords and words with numbers that aren't emojis
	stop_words = set(stopwords.words('english'))
	df[['text']] = df['text'].apply(lambda x: _tokenize(x, stop_words, emojis))
	# print(f"The concatenated cleaned dataframe is {df}.")
	return df

def find_frequent(df, frequency):
	'''
	Finds the words that show up more than once in the posts/comments.

	df (pandas.DataFrame): pd.DataFrame containing combined posts and comments data with three columns:
	['time', 'text', 'coin']
	frequency (int): Minimum frequency required for a word to be added to the dictionary
	
	return: pd.DataFrame with text column cleaned
	'''
	# Get all tokens in df
	tokens = list(chain(*df.text))
	# Count their frequencies
	word_count = Counter(tokens)
	# Find words that only show up once
	low_freq_words = []
	for k, v in word_count.items():
		if v <= frequency:
			low_freq_words.append(k)
	# Remove them from the dictionary
	for w in low_freq_words:
		word_count.pop(w)
	return word_count.keys()

def find_vocabulary(frequent, coin_type):
	'''
  	Builds the vocabulary from the tokenized words.

	frequent (list): List of frequent words
	coin_type (str): Either "proper" or "meme"

	return: (dict) word to unique index
  	'''
	word_set = set(frequent)
	vocabulary = {word: i for i, word in enumerate(word_set)}
	VOCAB_FILE = ''
	if coin_type == 'proper':
		VOCAB_FILE = '/proper_vocab.json'
	else:
		VOCAB_FILE = '/meme_vocab.json'
	vocab_file = open(ROOT_DIR + VOCAB_FILE, "w")
	json.dump(vocabulary, vocab_file)
	vocab_file.close()
	return vocabulary

def create_vocabulary(coin_type, frequency):
	'''
	Creates vocabulary from posts and comments about coins of desired type.

	coin_type (str): Either "proper" or "meme"
	frequency (int): Minimum frequency required for a word to be added to the dictionary

	return: 
	(pd.DataFrame) Text column cleaned.
	(dict) word to unique index for words found in comments/posts of desired type.
	'''
	if coin_type != 'proper' and coin_type != 'meme':
		print("Coin type was incorrectly given to data retrieval function. Input 'proper' or 'meme'.")
		return None
	else:
		VOCAB_FILE = ''
		if coin_type == 'proper':
			df = retrieve_reddit_data('proper')
			VOCAB_FILE = 'proper_vocab.json'
		else:
			df = retrieve_reddit_data('meme')
			VOCAB_FILE = 'meme_vocab.json'
		# Clean text and find recurring words
		df = clean_text(df)
		frequent = find_frequent(df, frequency)
		vocabulary = {}
		if path.exists(ROOT_DIR + '/' + VOCAB_FILE):
			with open(VOCAB_FILE) as json_file:
				vocabulary = json.load(json_file)
		else:
			vocabulary = find_vocabulary(frequent, coin_type)
		# print("Vocabulary has been created! Seee json files in ML folder.")
		return df, vocabulary

def one_hot_tokens(tokens, vocabulary, identity):
	'''
	Convert tokens into list of one-hot vectors w.r.t. vocabulary.

	tokens (list): List of words to convert to one-hot vectors
	vocabulary (dict): word --> unique index
	identity (2x2 int array): Identity matrix of size vocab_size to slice for one-hotting

	return: (list) array of one-hotted vectors representing original tokens list.
  	'''
	array = []
	for t in tokens:
		if t in vocabulary:
			array.append(identity[vocabulary[t], :])
	if len(array) > 0:
		return np.array(array)
	return None

def one_hot_text(df, vocabulary):
	'''
	Converts tokenized text of df into arrays of one-hot vectors w.r.t. vocabulary.

	df (pandas.DataFrame): pd.DataFrame containing combined cleaned and tokenized posts and comments data with 
	three columns: ['time', 'text', 'coin']

	return: (pandas.DataFrame) Original dataframe but with text one-hotted for DL model:
	- None if no words from dictionary in input post/comment
	- Otherwise, (vocab_size x number of words from dict in token) matrix
  	'''
	# Create identity matrix for one-hotting
	vocab_size = len(vocabulary)
	identity = np.identity(vocab_size)
	# Convery text to array of one-hot vectors w.r.t. input dictionary
	df[['text']] = df['text'].apply(lambda x: one_hot_tokens(x, vocabulary, identity))
	return df

def find_fluctuations(df, coin_type):
	'''
	Calculates fluctuations in price for each hour of the year for each coin of desired type.

	coin_type (str): Either "proper" or "meme"
	df (pandas.DataFrame): pd.DataFrame containing coin data containing columns: [time, COIN_open -> for each COIN]

	return: (pandas.DataFrame) Dataframe with columns: [time -> converted to UNIX timestamp, COIN_fluc_dir -> -1,0,1 for each COIN]
  	'''
	# Convert dates to UNIX time
	df[['time']] = df['time'].apply(lambda x: int(pd.Timestamp(x).timestamp()))
	if coin_type != 'proper' and coin_type != 'meme':
		print("Coin type was incorrectly given to data retrieval function. Input 'proper' or 'meme'.")
		return None
	else:
		coins = []
		if coin_type == 'proper':
			coins = ['btc_', 'eth_', 'sol_']
		else:
			coins = ['doge_', 'shib_', 'sushi_']
		for coin in coins:
			df[coin + 'fluc_dir'] = (df[coin + 'close'] - df[coin + 'open']) / df[coin + 'close']
			df[[coin + 'fluc_dir']] = df[coin + 'fluc_dir'].apply(lambda x: np.sign(x))
		return df[['time', coins[0] + 'fluc_dir', coins[1] + 'fluc_dir', coins[2] + 'fluc_dir']]

def retrieve_coin_data(coin_type):
	'''
	Retrieve coin data of desired coin type.

	coin_type (str): Either "proper" or "meme"

	return: (pandas.DataFrame) Coin data dataframe with fluctuations
  	'''
	COIN_PATH = ''
	if coin_type == 'proper':
		COIN_PATH = ROOT_DIR + PROPER_COINS
	else:
		COIN_PATH = ROOT_DIR + MEME_COINS
	coins_df = pd.read_csv(COIN_PATH)
	return coins_df

def cross_match(reddit_df, coin_df, coin_type):
	'''
	Associates posts to price fluctuations using input timeframe (maximum number of hours a past takes to affect price).

	return:
  	'''
	coins = []
	if coin_type == 'proper':
		coins = ['bitcoin', 'ethereum', 'solona']
	else:
		coins = ['dogecoin', 'shiba_inu', 'sushi']
	data = []
	coin_np = coin_df.to_numpy()
	# Loop through all gathered coin fluctuation times
	for i in range(coin_np.shape[0]):
		time = coin_np[i, 0]
		# Gather posts within TIMEFRAME hours before a fluctuation
		rows = reddit_df.loc[(reddit_df['time'] >= time - TIMEFRAME * 60 * 60) & (reddit_df['time'] < time)]
		if not rows.empty:
			for j, coin in enumerate(coins):
				# Gather posts referring to particular coin
				posts = rows.loc[rows['coin'] == coin]
				if not posts.empty:
					posts = posts['text'].to_numpy()
					for post in posts:
						# Ensure post is not empty, fluctuation is not NaN or 0
						if post is not None and not isnan(coin_np[i, j+1]) and coin_np[i, j+1] != 0:
							data.append(([post, coin_np[i, j+1]]))
	data = np.array(data)
	# print(f"Input data for {coin_type} is of shape {data.shape}.")
	return data

def create_input_data():
	'''
	Creates input data for the GRU model and returns them.

	return: tuple -> (proper coin data, meme coin data) in numpy matrix format
  	'''
	# Reddit one-hotted data
	# print("First we find the proper coin posts/comments.")
	proper_reddit_df, proper_vocab = create_vocabulary('proper', FREQUENCY)
	proper_reddit_df = one_hot_text(proper_reddit_df, proper_vocab)
	# print("Then we find the meme coin posts/comments.")
	meme_reddit_df, meme_vocab = create_vocabulary('meme', FREQUENCY)
	meme_reddit_df = one_hot_text(meme_reddit_df, meme_vocab)
	# Coin fluctuation data
	# print("We now find the proper coin fluctuation directions for each hour.")
	proper_coin_df = retrieve_coin_data('proper')
	proper_coin_df = find_fluctuations(proper_coin_df, 'proper')
	# print(proper_coin_df)
	# print("Then we find the meme coin fluctuation directions for each hour.")
	meme_coin_df = retrieve_coin_data('meme')
	meme_coin_df = find_fluctuations(meme_coin_df, 'meme')
	# print(meme_coin_df)
	# Cross-match reddit post data to coin fluctuation data to create input data
	proper_data = cross_match(proper_reddit_df, proper_coin_df, 'proper')
	meme_data = cross_match(meme_reddit_df, meme_coin_df, 'meme')
	return proper_data, meme_data