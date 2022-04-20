import torch
import torch.nn as nn
from torch.nn import RNN
from os import path
from sklearn.model_selection import KFold
from preprocess import create_input_data

'''
This file creates the RNN model, calls for pre-processing, and trains the model on the input data using
k-fold cross validation for testing purposes.
'''

# Finds root directory of user
ROOT_DIR = path.dirname(path.abspath((__file__)))

'''
Here we define the hyperparameters of the data pre-processing and the RNN model.
'''

# Define Pre-Processing Hyperparameters ------
# Minimum frequency of words in reddit data to be considered for dictionary
FREQUENCY = 5
# Maximum number of hours a post takes to affect price
TIMEFRAME = 3

# Define ML hyperparameters ------
LEARNING_RATE = 0.01
# Number of split for k-fold validation
N_SPLITS = 4
# Hidden size of RNN model
HIDDEN_SIZE = 128

'''
Note that the general RNN architecture was taken from:
'https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html'
'''
device = torch.device('cpu')
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, learning_rate):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size
        self.learning_rate = learning_rate

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

        self.criterion =  nn.NLLLoss() # Negative Log Likelihood Loss

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, self.hidden_size)

def get_data():
    '''
    Retrieve data for the model for both coin types, X being the list of inputs and Y being the list of corresponding
    labels. Each input is a one-hot torch tensor of size (1 x vocab_size), and labels are 0 or 1 representing
    the fluctuation direction that followed.

    return: Tuple (size 4) -> (proper_X, proper_Y, meme_X, meme_Y) as list of tensors.
    '''
    return create_input_data(FREQUENCY, TIMEFRAME)

def prediction(output):
    '''
    Takes model output and returns the predicted label with the highest likelihood.

    return: (int) label -> 0 or 1
    '''
    return output.topk(1)[1][0].item()

def run(X, Y, num_splits, hidden_size):
    '''
    Runs model on the input data k times with k-fold cross validation.

    X: Input data
    Y: Input labels
    num_splits: Number of split for k-fold validation
    hidden_size: Size of hidden layer in RNN model

    return: Average k-fold accuracy of the model
    '''
    # Find vocabulary size of input data
    vocab_size = X[0].size(dim=2)
    # Split proper data
    kf = KFold(n_splits=num_splits)
    accuracies = []
    count = 0
    for train_indices, test_indices in kf.split(X):
        count += 1
        # Create model
        model = RNN(vocab_size, hidden_size, 2, LEARNING_RATE)
        print('——————————————————————————————————————————————————————————')
        print(f'Training split {count} of {num_splits} of size {len(train_indices)}.')
        # Train
        X_train, Y_train = [X[i] for i in train_indices], [Y[i] for i in train_indices]
        train_split(X_train, Y_train, model)
        print(f'Testing split {count} of {num_splits} of size {len(test_indices)}.')
        # Test
        X_test, Y_test = [X[i] for i in test_indices], [Y[i] for i in test_indices]
        accuracy = test_split(X_test, Y_test, model)
        print(f'Accuracy for split {count} of {num_splits} was found to be: {accuracy}.')
        # Add accuracy to list of accuracies
        accuracies.append(accuracy)
    print('——————————————————————————————————————————————————————————')
    average_acc = sum(accuracies) / len(accuracies)
    print(f'Final list of accuracies is: {accuracies} -> This gives an average of {average_acc}.')
    return average_acc

def train_split(X, Y, model):
    '''
    Trains the input RNN model using input training data and corresponding labels.

    X: Input data
    Y: Input labels
    model: Input RNN model to train
    '''
    for i in range(len(X)):
        hidden = model.initHidden()
        model.zero_grad()
        if i % 1000 == 0:
            print(f'Model has trained on {i} examples.')
        for j in range(X[i].size(dim=0)):
            output, hidden = model(X[i][j], hidden)
        loss = model.criterion(output, Y[i])
        loss.backward()
        # Modify parameters based on backprop gradients
        for p in model.parameters():
            p.data.add_(p.grad.data, alpha=-model.learning_rate)

def test_split(X, Y, model):
    '''
    Tests the input RNN model using input test data and corresponding labels.

    X: Input data
    Y: Input labels
    model: Input RNN model to train

    return: (float) accuracy of model on test data
    '''
    num_correct = 0
    for i in range(len(X)):
        hidden = model.initHidden()
        output = 0
        for j in range(X[i].size(dim=0)):
            output, hidden = model(X[i][j], hidden)
        if prediction(output) == Y[i].item():
            num_correct += 1
    return num_correct / len(X)

def main():
    '''
    Retrieves the proper and meme datasets, then trains the model on them and finds the average k-fold accuracy.
    '''
    print('\n\nCreating data for RNN model.')
    proper_X, proper_Y, meme_X, meme_Y = get_data()
    print('——————————————————————————————————————————————————————————')
    # Train on proper coin data
    print('Begin training on proper coin dataset.')
    proper_acc = run(proper_X, proper_Y, HIDDEN_SIZE, N_SPLITS)
    print('Done training on proper coin dataset!\n\n')
    print('——————————————————————————————————————————————————————————')
    # Train on meme coin data
    print('Begin training on meme coin dataset.')
    meme_acc = run(meme_X, meme_Y, HIDDEN_SIZE, N_SPLITS)
    print('Done training on meme coin dataset!\n\n')
    print('——————————————————————————————————————————————————————————')
    print('The model obtained the following training accuracies:\n')
    print(f'Proper coin dataset accuracy = {proper_acc}')
    print(f'Proper coin dataset accuracy = {meme_acc}')

if __name__ == '__main__':
    main()