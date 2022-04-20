import numpy as np
import torch
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
import pickle

'''
This file retrieves and prepares the data for the RNN model.
'''

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
	Gets reddit text data of desired type from csv files in data folder of data_deliverable.

	coin_type (str): Either "proper" or "meme", the desired coin type.
	
	return: pd.DataFrame containing concatenated comments and posts of desired coin type.
	'''
	# Set correct filepaths based on input coin type
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
	# Concatenate them
	df = pd.concat([posts_df, comments_df])
	print(f"The concatenated raw dataframe looks like \n\n {df.head(4)} \n")
	return df

def _separate_emojis(post, emojis):
	'''
	Separates emojis in input post/comment with a space for tokenization.

	post (str): Input post to modify.
	emojis (set): Set of emojis to separate.
	
	return: (str) Input post with emojis separated by a space.
	'''
	return ''.join(' ' + char if char in emojis else char for char in post)

def _contains_number(word):
	'''
	Checks if an input word contains a number.

	word (str): Single token to check.
	
	return: (boolean)
	'''
	for char in word:
		if char.isdigit():
			return True
	return False

def _tokenize(post, stop_words, emojis):
	'''
	Helper function that tokenizes posts/comments into individual words. In doing so, removes stop words, 
	and non-emoji words that have a number in them.

	post (str): Post/comment to tokenize.
	stop_words (set): Set of stop words not to tokenize, which includes coin keywords which were searched for
	to get dataset.
	emojis (set): Set of emojis.
	
	return: (list) Tokenized text by word.
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
	Cleans reddit text data: removes links, punctuation, whitespace, stopwords (including coin keywords). Also separates
	emojis with whitespace, turns into lowercase, and tokenizes text into words.

	df (pd.DataFrame): Dataframe containing post/comment data with three columns: ['time', 'text', 'coin']
	
	return: (pd.DataFrame) Dataframe with text column cleaned.
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
	# Add coin keywords to set of stopwords
	coins = ['bitcoin', 'btc', 'ethereum', 'eth', 'solona', 'sol', 'dogecoin', 'doge', 'shiba inu', \
		 'shiba', 'inu', 'sushi', 'coin']
	stop_words = set(stopwords.words('english') + coins)
	# Tokenize, remove standard stopwords and words with numbers that aren't emojis
	df[['text']] = df['text'].apply(lambda x: _tokenize(x, stop_words, emojis))
	print(f"The concatenated cleaned dataframe looks like \n\n{df.head(4)} \n")
	return df

def find_frequent(df, frequency):
	'''
	Finds words from input tokenized dataframe with 'text' column that show up at least frequency times.

	df (pd.DataFrame): DataFrame containing combined posts and comments data with three columns: ['time', 'text', 'coin']
	frequency (int): Minimum frequency of words in reddit data to be considered for final dictionary.
	
	return: (list) List of words with required minimum frequency.
	'''
	# Get all tokens in df
	tokens = list(chain(*df.text))
	# Count their frequencies in input data
	word_count = Counter(tokens)
	# Find words that only show up less than frequency times
	low_freq_words = []
	for k, v in word_count.items():
		if v < frequency:
			low_freq_words.append(k)
	# Remove them from the dictionary
	for w in low_freq_words:
		word_count.pop(w)
	return word_count.keys()

def create_vocabulary(frequent, coin_type):
	'''
  	Builds the vocabulary from the input list of words that show up at least frequency times in input data.

	frequent (list): List of words that show up at least frequency times in input data.
	coin_type (str): Either "proper" or "meme", the desired coin type.

	saves: Output dictionary to json file in ML folder for viewing.
	return: (dict) Word from input data to unique index.
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

def find_vocabulary(coin_type, frequency):
	'''
	Finds vocabulary for posts and comments about coins of desired type, and removes duplicate tokens in each post/
	comment in original dataframe.

	coin_type (str): Either "proper" or "meme", the desired coin type.
	frequency: (int) Minimum frequency of words in reddit data to be considered for dictionary

	return: Tuple -> size 2:
	- (pd.DataFrame) Dataframe with 'text' column cleaned.
	- (dict) Word to unique index for words found in comments/posts of desired coin type.
	'''
	if coin_type != 'proper' and coin_type != 'meme':
		print("Coin type was incorrectly given to data retrieval function. Input 'proper' or 'meme'.")
		return None
	else:
		df = 0
		if coin_type == 'proper':
			df = retrieve_reddit_data('proper')
		else:
			df = retrieve_reddit_data('meme')
		# Clean text and find recurring words
		df = clean_text(df)
		frequent = find_frequent(df, frequency)
		vocabulary = create_vocabulary(frequent, coin_type)
		print(f"Vocabulary for {coin_type} coins has been created! It is of size {len(vocabulary)}. See json files in ML folder.")
		# Remove duplicates in text tokenization after dictionary has been created
		df[['text']] = df['text'].apply(lambda x: list(dict.fromkeys(x)))
		return df, vocabulary

def one_hot_tokens(tokens, vocabulary):
	'''
	Convert input tokens into one-hot tensor array of size (post_length x (1 x vocab_size)) w.r.t. input vocabulary.

	tokens (list): List of words to convert to one-hot vectors.
	vocabulary (dict): Dictionary of word to unique index for the data.

	return: (list) Torch tensor array of size (post_length x (1 x vocab_size)).
  	'''
	count = 0
	indices = []
	for t in tokens:
		if t in vocabulary:
			count += 1
			# Index to one-hot encode
			indices.append(vocabulary[t])
	if count > 0:
		# One-hot encode posts in tensor of size (post_length x 1 x vocab_size)
		tensor = torch.zeros(count, 1, len(vocabulary), dtype=int)
		for i, ind in enumerate(indices):
			tensor[i][0][ind] = 1
		return tensor
	return None

def one_hot_text(df, vocabulary):
	'''
	One-hots input token lists from 'text' column of input dataframe w.r.t. input vocabulary, and drops those
	that are subsequently empty.

	df (pd.DataFrame): DataFrame containing combined cleaned and tokenized posts and comments data with 
	three columns: ['time', 'text', 'coin']

	return: (pandas.DataFrame) Original dataframe but with text one-hotted for DL model (as torch tensors).
  	'''
	# Convery text to array of one-hot vectors w.r.t. input dictionary
	df[['text']] = df['text'].apply(lambda x: one_hot_tokens(x, vocabulary))
	# Drop empty posts
	df.dropna(inplace=True)
	return df

def retrieve_coin_data(coin_type):
	'''
	Retrieve coin data of desired coin type from data file of data_deliverable.

	coin_type (str): Either "proper" or "meme", the desired coin type.

	return: (pd.DataFrame) Dataframe of coin data of desired coin type found in data_deliverable.
  	'''
	COIN_PATH = ''
	if coin_type == 'proper':
		COIN_PATH = ROOT_DIR + PROPER_COINS
	else:
		COIN_PATH = ROOT_DIR + MEME_COINS
	coins_df = pd.read_csv(COIN_PATH)
	return coins_df

def find_fluctuations(coin_type):
	'''
	Calculates fluctuations in price for each hour using opening and closing price for each coin in the 
	three coins of the desired type.

	coin_type (str): Either "proper" or "meme", the desired coin type.

	return: (pd.DataFrame) Dataframe with columns: [time -> converted to UNIX timestamp, 
	COIN_fluc_dir -> -1,0,1 for each COIN]
  	'''
	df = retrieve_coin_data(coin_type)
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
		df = df[['time', coins[0] + 'fluc_dir', coins[1] + 'fluc_dir', coins[2] + 'fluc_dir']]
		print(f"The hour by hour fluctuation direction data looks like \n\n{df.head(4)}\n")
		return df

def cross_match(reddit_df, coin_df, coin_type, timeframe):
	'''
	Associates posts to price fluctuations using input timeframe (maximum number of hours a post/comment is assumed to
	take to affect the coin price).

	reddit_df: Cleaned, one-hot tensor encoded reddit text dataframe.
	coin_df: Coin fluctuation dataframe.
	coin_type (str): Either "proper" or "meme", the desired coin type.
	timeframe: (int) Maximum number of hours a post is assumed to have an effect on price.

	return: Tuple (size 2)
	- Data_X -> List of posts (one-hot encoded tensors) of size (post_length x 1 x vocab_size)
	- Data_Y -> List of fluctuation direction as tensors of size 1 (0 for fall, 1 for increase in price)
  	'''
	coins = []
	if coin_type == 'proper':
		coins = ['bitcoin', 'ethereum', 'solona']
	else:
		coins = ['dogecoin', 'shiba_inu', 'sushi']
	data_X = []
	data_Y = []
	coin_np = coin_df.to_numpy()
	# Loop through all gathered coin fluctuation times
	for i in range(coin_np.shape[0]):
		time = coin_np[i, 0]
		# Gather posts within timeframe hours before a fluctuation
		rows = reddit_df.loc[(reddit_df['time'] >= time - timeframe * 60 * 60) & (reddit_df['time'] < time)]
		if not rows.empty:
			for j, coin in enumerate(coins):
				# Gather posts referring to particular coin
				posts = rows.loc[rows['coin'] == coin]
				if not posts.empty:
					posts = posts['text'].to_numpy()
					for post in posts:
						# Ensure post is not empty, fluctuation is not NaN or 0
						if not isnan(coin_np[i, j+1]) and coin_np[i, j+1] != 0:
							data_X.append(post)
							label = 0
							# Create appropriate tensor for label
							if int(coin_np[i, j+1]) == 1:
								label = torch.ones(1, dtype=int)
							else:
								label = torch.zeros(1, dtype=int)
							data_Y.append(label)
	print(f"Data for {coin_type} coins has {len(data_X)} examples.")
	return data_X, data_Y

def create_input_data(frequency, timeframe):
	'''
	Creates input data using above functions for RNN model and returns them for both coin types
	using the input hyperparameters.

	Pre-Processing Hyperparameters ------
	frequency: (int) Minimum frequency of words in reddit data to be considered for dictionary.
	timeframe: (int) Maximum number of hours a post is assumed to have an effect on price.

	return: tuple -> (proper data X, proper data Y, meme data X, meme data Y) as lists of tensors.
  	'''
	# Reddit one-hotted data
	print('——————————————————————————————————————————————————————————')
	print("First we find the proper coin posts/comments. \n\n")
	proper_reddit_df, proper_vocab = find_vocabulary('proper', frequency)
	proper_reddit_df = one_hot_text(proper_reddit_df, proper_vocab)
	print('——————————————————————————————————————————————————————————')
	print("Then we find the meme coin posts/comments. \n\n")
	meme_reddit_df, meme_vocab = find_vocabulary('meme', frequency)
	meme_reddit_df = one_hot_text(meme_reddit_df, meme_vocab)
	# Coin fluctuation data
	print('——————————————————————————————————————————————————————————')
	print("We now find the proper coin fluctuation directions for each hour. \n\n")
	proper_coin_df = find_fluctuations('proper')
	print('——————————————————————————————————————————————————————————')
	print("Then we find the meme coin fluctuation directions for each hour. \n\n")
	meme_coin_df = find_fluctuations('meme')
	# Cross-match reddit post data to coin fluctuation data to create input data
	print('——————————————————————————————————————————————————————————')
	print("Finally, we cross-match the reddit data to the fluctuations using the timeframe hyperparameter. \n\n")
	proper_X, proper_Y = cross_match(proper_reddit_df, proper_coin_df, 'proper', timeframe)
	meme_X, meme_Y = cross_match(meme_reddit_df, meme_coin_df, 'meme', timeframe)
	return proper_X, proper_Y, meme_X, meme_Y