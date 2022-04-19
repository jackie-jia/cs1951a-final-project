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

UNK = '<UNK>'
TIMEFRAME = 48 # Maximum number of hours before a fluctuation a post is considered influential

def retrieve_data(coin_type):
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
	print(f"The concatenated raw dataframe is {df}.")
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
	print(f"The concatenated cleaned dataframe is {df}.")
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

	return: (dict) word to unique index for words found in comments/posts of desired type.
	'''
	if coin_type != 'proper' and coin_type != 'meme':
		print("Coin type was incorrectly given to data retrieval function. Input 'proper' or 'meme'.")
		return None
	else:
		df = None
		if coin_type == 'proper':
			df = retrieve_data('proper')
		else:
			df = retrieve_data('meme')
		# Clean text and find recurring words
		frequent = find_frequent(clean_text(df), frequency)
		vocabulary = find_vocabulary(frequent, coin_type)
		print("Vocabulary has been created! Seee json files in ML folder.")
		return vocabulary

def convert_to_id(vocab, sentences):
	# '''
	# DO NOT CHANGE

  	# Convert sentences to indexed 

	# :param vocab:  dictionary, word --> unique index
	# :param sentences:  list of lists of words, each representing padded sentence
	# :return: numpy array of integers, with each row representing the word indeces in the corresponding sentences
  	# '''
	# return np.stack([[vocab[word] if word in vocab else vocab[UNK_TOKEN] for word in sentence] for sentence in sentences])
	pass

if __name__ == "__main__":
	print(f"First we find the meme coin posts/comments.")
	meme_vocab = create_vocabulary('meme', 1)
	print(f"Then we find the proper coin posts/comments.")
	proper_vocab = create_vocabulary('proper', 1)