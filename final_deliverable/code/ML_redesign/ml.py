import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn import RNN
import os
from os import path
from sklearn.model_selection import KFold
from preprocess import create_input_data
import json
import matplotlib.pyplot as plt

# Set boolean for whether testing should take place
TESTING = True

'''
This file creates the RNN model, calls for pre-processing, and trains the model on the input data using
k-fold cross validation for testing purposes.
'''

# Finds root directory of user
ROOT_DIR = path.dirname(path.abspath((__file__)))

'''
Here we define the hyperparameters of the data pre-processing and the RNN model.
'''

# Define default Hyperparameters ------
# Maximum number of hours a post takes to affect price
TIMEFRAME = 3
# Number of splits for KFold testing
NUM_SPLITS = 4

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

        self.criterion = nn.NLLLoss() # Negative Log Likelihood Loss

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = torch.sigmoid(self.i2h(combined))
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, self.hidden_size)

def get_data(frequency):
    '''
    Retrieve data for the model for both coin types, X being the list of inputs and Y being the list of corresponding
    labels. Each input is a one-hot torch tensor of size (1 x vocab_size), and labels are 0 or 1 representing
    the fluctuation direction that followed.

    return: Tuple (size 4) -> (proper_X, proper_Y, meme_X, meme_Y) as list of tensors.
    '''
    return create_input_data(frequency, TIMEFRAME)

def prediction(output):
    '''
    Takes model output and returns the predicted label with the highest likelihood.

    return: (int) label -> 0 or 1
    '''
    return (output).topk(1)[1].item()

def run(X, Y, hidden_size, num_splits, learning_rate):
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
    kf = KFold(n_splits=num_splits, shuffle=True)
    accuracies = []
    count = 0
    for train_indices, test_indices in kf.split(X):
        count += 1
        # Create model
        model = RNN(vocab_size, hidden_size, 2, learning_rate)
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
    optimizer = optim.Adam(model.parameters(), lr=model.learning_rate)
    for i in range(len(X)):
        if i % 1000 == 0:
            print(f'Model has trained on {i} examples.')
        hidden = model.initHidden()
        optimizer.zero_grad()
        for j in range(X[i].size(dim=0)):
            output, hidden = model(X[i][j], hidden)
        loss = model.criterion(output, Y[i])
        loss.backward()
        # Modify parameters based on backprop gradients
        optimizer.step()

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


def test_frequency():
    '''
    Tests frequency setting (minimum frequency of words in reddit data to be considered for dictionary) to
    find optimal setting for the model.
    '''
    print(f'\n\nTesting minimum frequency settings to find optimal setting.\n\n')
    # Default hyperparameter settings for testing:
    hidden_size = 128
    prop_learning_rate = 0.01
    meme_learning_rate = 0.00001
    # Storage for raw accuracies:
    if path.isfile(ROOT_DIR + "/testing_files/frequency_testing.txt"):
        os.remove(ROOT_DIR + "/testing_files/frequency_testing.txt")
    frequencies = []
    prop_accuracies = []
    meme_accuracies = []
    for i in range(5, 35, 5):
        frequency = i
        frequencies.append(frequency)
        # Get data for this frequency
        print('——————————————————————————————————————————————————————————')
        print(f'\n\nCreating data for RNN model with vocabulary minimum frequency {frequency}.')
        proper_X, proper_Y, meme_X, meme_Y = get_data(frequency)
        # Train on proper coin data
        print(f'Beginning training on proper coin dataset for frequency {frequency}.')
        proper_acc = run(proper_X, proper_Y, hidden_size, NUM_SPLITS, prop_learning_rate)
        print('Done training on proper coin dataset!\n')
        # Train on meme coin data
        print(f'Beginning training on meme coin dataset for frequency {frequency}.')
        meme_acc = run(meme_X, meme_Y, hidden_size, NUM_SPLITS, meme_learning_rate)
        prop_accuracies.append(proper_acc)
        meme_accuracies.append(meme_acc)
        print('Done training on meme coin dataset!\n')
        print('The model obtained the following training accuracies:\n')
        print(f'Proper coin dataset accuracy for frequency {frequency} is {proper_acc}')
        print(f'Meme coin dataset accuracy for frequency {frequency} is {meme_acc}')
        print('——————————————————————————————————————————————————————————')
        with open(ROOT_DIR + "/testing_files/frequency_testing.txt", "a") as file:
            file.write(str(i) + ', ' + str(proper_acc) + ', ' + str(meme_acc) + '\n')
    # Dump accuracy data into json for safety due to high training times
    if path.isfile(ROOT_DIR + "/testing_files/frequencies.json"):
        os.remove(ROOT_DIR + "/testing_files/frequencies.json")
    with open(ROOT_DIR + "/testing_files/frequencies.json", "w") as f:
        json.dump(frequencies, f)
    if path.isfile(ROOT_DIR + "/testing_files/frequency_prop_acc.json"):
        os.remove(ROOT_DIR + "/testing_files/frequency_prop_acc.json")
    with open(ROOT_DIR + "/testing_files/frequency_prop_acc.json", "w") as f:
        json.dump(prop_accuracies, f)
    if path.isfile(ROOT_DIR + "/testing_files/frequency_meme_acc.json"):
        os.remove(ROOT_DIR + "/testing_files/frequency_meme_acc.json")
    with open(ROOT_DIR + "/testing_files/frequency_meme_acc.json", "w") as f:
        json.dump(meme_accuracies, f)
    # Plot the results
    fig, ax = plt.subplots()
    plt.xlim([5, 30])
    plt.ylim([0, 1])
    ax.plot(frequencies, prop_accuracies, "orange", label='Proper coin accuracy')
    ax.plot(frequencies, meme_accuracies, "blue", label='Meme coin accuracy')
    # setting labels
    ax.set_xlabel("Frequency")
    ax.set_ylabel("K-Fold Accuracy")
    ax.set_title("K-Fold Accuracy by Minimum Frequency in Vocabulary")
    plt.legend()
    plt.savefig(ROOT_DIR + "/../../visualizations/frequency_testing_graph.png")
    plt.show()


def test_learning_rate(proper_X, proper_Y, meme_X, meme_Y):
    '''
    Tests learning rate parameter for RNN to find the optimal setting.
    '''
    print(f'\n\nTesting learning rate hyperparameter values to find optimal setting.\n\n')
    # Default hyperparameter settings for testing:
    hidden_size = 128
    # Storage for raw accuracies:
    if path.isfile(ROOT_DIR + "/testing_files/learning_rate_testing.txt"):
        os.remove(ROOT_DIR + "/testing_files/learning_rate_testing.txt")
    learning_rates = []
    prop_accuracies = []
    meme_accuracies = []
    for i in range(6):
        learning_rate = 10 ** (-i)
        learning_rates.append(-i)
        # Train on proper coin data
        print('——————————————————————————————————————————————————————————')
        print(f'Begin training on proper coin dataset for learning rate {learning_rate}.')
        proper_acc = run(proper_X, proper_Y, hidden_size, NUM_SPLITS, learning_rate)
        print('Done training on proper coin dataset!\n')
        # Train on meme coin data
        print('Begin training on meme coin dataset.')
        meme_acc = run(meme_X, meme_Y, hidden_size, NUM_SPLITS, learning_rate)
        prop_accuracies.append(proper_acc)
        meme_accuracies.append(meme_acc)
        print('Done training on meme coin dataset!\n')
        print('The model obtained the following training accuracies:\n')
        print(f'Proper coin dataset accuracy for learning rate {learning_rate} is {proper_acc}')
        print(f'Meme coin dataset accuracy for learning rate {learning_rate} is {meme_acc}')
        print('——————————————————————————————————————————————————————————')
        with open(ROOT_DIR + "/testing_files/learning_rate_testing.txt", "a") as file:
            file.write(str(10 ** (-i)) + ', ' + str(proper_acc) + ', ' + str(meme_acc) + '\n')
    # Dump accuracy data into json for safety due to high training times
    if path.isfile(ROOT_DIR + "/testing_files/learning_rates.json"):
        os.remove(ROOT_DIR + "/testing_files/learning_rates.json")
    with open(ROOT_DIR + "/testing_files/learning_rates.json", "w") as f:
        json.dump(learning_rates, f)
    if path.isfile(ROOT_DIR + "/testing_files/learning_rate_prop_acc.json"):
        os.remove(ROOT_DIR + "/testing_files/learning_rate_prop_acc.json")
    with open(ROOT_DIR + "/testing_files/learning_rate_prop_acc.json", "w") as f:
        json.dump(prop_accuracies, f)
    if path.isfile(ROOT_DIR + "/testing_files/learning_rate_meme_acc.json"):
        os.remove(ROOT_DIR + "/testing_files/learning_rate_meme_acc.json")
    with open(ROOT_DIR + "/testing_files/learning_rate_meme_acc.json", "w") as f:
        json.dump(meme_accuracies, f)
    # Plot the results
    fig, ax = plt.subplots()
    plt.xlim([-5, 0])
    plt.ylim([0, 1])
    ax.plot(learning_rates, prop_accuracies, "orange", label='Proper coin accuracy')
    ax.plot(learning_rates, meme_accuracies, "blue", label='Meme coin accuracy')
    # setting labels
    ax.set_xlabel("Learning Rate (log unit)")
    ax.set_ylabel("K-Fold Accuracy")
    ax.set_title("K-Fold Accuracy by Learning Rate")
    plt.legend()
    plt.savefig(ROOT_DIR + "/../../visualizations/learning_rate_testing_graph.png")
    plt.show()


def test_hidden_size(proper_X, proper_Y, meme_X, meme_Y):
    '''
    Tests hidden layer size parameter for RNN to find the optimal setting.
    '''
    print(f'\n\nTesting hidden size hyperparameter values to find optimal setting.\n\n')
    # Default hyperparameter settings for testing:
    prop_learning_rate = 0.01
    meme_learning_rate = 0.00001
    # Storage for raw accuracies:
    if path.isfile(ROOT_DIR + "/testing_files/hidden_size_testing.txt"):
        os.remove(ROOT_DIR + "/testing_files/hidden_size_testing.txt")
    hidden_sizes = []
    prop_accuracies = []
    meme_accuracies = []
    for i in range(6, 11):
        hidden_size = 2 ** i
        hidden_sizes.append(i)
        # Train on proper coin data
        print('——————————————————————————————————————————————————————————')
        print(f'Begin training on proper coin dataset for hidden size {hidden_size}.')
        proper_acc = run(proper_X, proper_Y, hidden_size, NUM_SPLITS, prop_learning_rate)
        print(f'Done training on proper coin dataset for hidden size {hidden_size}!\n')
        # Train on meme coin data
        print('Begin training on meme coin dataset.')
        meme_acc = run(meme_X, meme_Y, hidden_size, NUM_SPLITS, meme_learning_rate)
        prop_accuracies.append(proper_acc)
        meme_accuracies.append(meme_acc)
        print(f'Done training on meme coin dataset for hidden size {hidden_size}!\n')
        print('The model obtained the following training accuracies:\n')
        print(f'Proper coin dataset accuracy for hidden size {hidden_size} is {proper_acc}')
        print(f'Meme coin dataset accuracy for hidden size {hidden_size} is {meme_acc}')
        print('——————————————————————————————————————————————————————————')
        with open(ROOT_DIR + "/testing_files/hidden_size_testing.txt", "a") as file:
            file.write(str(10 ** (-i)) + ', ' + str(proper_acc) + ', ' + str(meme_acc) + '\n')
    # Dump accuracy data into json for safety due to high training times
    if path.isfile(ROOT_DIR + "/testing_files/hidden_sizes.json"):
        os.remove(ROOT_DIR + "/testing_files/hidden_sizes.json")
    with open(ROOT_DIR + "/testing_files/hidden_sizes.json", "w") as f:
        json.dump(hidden_sizes, f)
    if path.isfile(ROOT_DIR + "/testing_files/hidden_size_prop_acc.json"):
        os.remove(ROOT_DIR + "/testing_files/hidden_size_prop_acc.json")
    with open(ROOT_DIR + "/testing_files/hidden_size_prop_acc.json", "w") as f:
        json.dump(prop_accuracies, f)
    if path.isfile(ROOT_DIR + "/testing_files/hidden_size_meme_acc.json"):
        os.remove(ROOT_DIR + "/testing_files/hidden_size_meme_acc.json")
    with open(ROOT_DIR + "/testing_files/hidden_size_meme_acc.json", "w") as f:
        json.dump(meme_accuracies, f)
    # Plot the results
    fig, ax = plt.subplots()
    plt.xlim([6, 10])
    plt.ylim([0, 1])
    ax.plot(hidden_sizes, prop_accuracies, "orange", label='Proper coin accuracy')
    ax.plot(hidden_sizes, meme_accuracies, "blue", label='Meme coin accuracy')
    # setting labels
    ax.set_xlabel("Hidden Size (log_2 unit)")
    ax.set_ylabel("K-Fold Accuracy")
    ax.set_title("K-Fold Accuracy by RNN Hidden Layer Size")
    plt.legend()
    plt.savefig(ROOT_DIR + "/../../visualizations/hidden_size_testing_graph.png")
    plt.show()


def main():
    '''
    # Retrieves the proper and meme datasets, then trains the model on them and finds the average k-fold accuracy.
    # '''
    frequency = 30
    # Change TESTING value at top of file to run testing
    if TESTING:
        # test_frequency()
        print('\n\nCreating data for RNN model.')
        proper_X, proper_Y, meme_X, meme_Y = get_data(frequency)
        print('——————————————————————————————————————————————————————————')
        # test_learning_rate(proper_X, proper_Y, meme_X, meme_Y)
        test_hidden_size(proper_X, proper_Y, meme_X, meme_Y)
    else:
        print('\n\nCreating data for RNN model.')
        proper_X, proper_Y, meme_X, meme_Y = get_data(frequency)
        print('——————————————————————————————————————————————————————————')
        # Optimal hyperparameter settings:
        hidden_size = 128
        learning_rate = 0.01
        print('Begin training on proper coin dataset.')
        proper_acc = run(proper_X, proper_Y, hidden_size, NUM_SPLITS, learning_rate)
        print('Done training on proper coin dataset!\n\n')
        print('——————————————————————————————————————————————————————————')
        # Train on meme coin data
        print('Begin training on meme coin dataset.')
        meme_acc = run(meme_X, meme_Y, hidden_size, NUM_SPLITS, learning_rate)
        print('Done training on meme coin dataset!\n\n')
        print('——————————————————————————————————————————————————————————')
        print('The model obtained the following training accuracies:\n')
        print(f'Proper coin dataset accuracy = {proper_acc}')
        print(f'Proper coin dataset accuracy = {meme_acc}')


if __name__ == '__main__':
    main()