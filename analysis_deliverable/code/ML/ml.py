import numpy as np
import torch
import torch.nn as nn
from torch.nn import GRU
from os import path
from sklearn.model_selection import KFold
from preprocess import create_input_data
import pandas as pd

# Define hyperparameters
N_HIDDEN = 128
device = torch.device('cpu')

# Finds root directory of user
ROOT_DIR = path.dirname(path.abspath((__file__)))

# Final data filepaths (in CSV format)
PROPER_DATA = '/proper_data.csv'
MEME_DATA = '/meme_data.csv'

# General RNN model architecture taken from:
# 'https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html'
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, self.hidden_size)



    # # Split proper data
    # kf = KFold(n_splits=5)
    # for train_index, test_index in kf.split(X):
    #     X_train, X_test = X[train_index], X[test_index]
def post_to_tensor(post, ):
    '''
    Converts input post (array of one-hot vectors of size (1 x vocab_size)) into tensor.
    '''
    tensor = torch.zeros(1, n_letters)
    tensor[0][letterToIndex(letter)] = 1
    return tensor

# NOTE: delete meme_data.csv and proper_data.csv files if you wish to see them being computed in preprocess.py
def get_data():
    '''
    Retrieve data for the model for both coin types, X being the inputs and Y being the labels. The inputs are
    non-empty array of one-hot vectors of size (1 x vocab_size), and labels are -1 or 1 for the fluctuation 
    direction.
    '''
    proper_data, meme_data = create_input_data()
    proper_X = torch.from_numpy(proper_data[:, 0])
    proper_Y = torch.from_numpy(proper_data[:, 1])
    meme_X = torch.from_numpy(meme_data[:, 0])
    meme_Y = torch.from_numpy(meme_data[:, 1])
    # print(proper_X.shape) #(19391,)
    # print(proper_X[0].shape) # (298, 11165)
    # print(proper_X[0][0].shape) # (11165,)
    print(proper_X)
    print(meme_Y)
    return proper_X, proper_Y, meme_X, meme_Y

def main():
    proper_X, proper_Y, meme_X, meme_Y = get_data()
    # model = RNN(vocab_size, N_HIDDEN, 2)
    # output, next_hidden = model(input, hidden)

if __name__ == '__main__':
    main()