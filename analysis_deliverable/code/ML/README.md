# ML Folder

## ML Model

The model we chose was an RNN deep learning model, which is a supervised learning algorithm. The goal of the model is to take as input comments/posts written within 'timeframe' hours before a coin fluctuation, and output the direction of the coin fluctuation that follows.

### Running the Model

To run the model run the following line in a python environment:

- python3 ml.py

Note that the additional package 'emoji==1.7.0' is needed. For this reason, an additional 'requirements.txt' file is included in the folder to create a new virtual environment that includes this package.

## Files

- 'ml.py': This is the file where the RNN model lies, along with its hyperparameters, training, and testing functions. The data is also retrieved from preprocess.py into this file to begin training.
- 'preprocess.py': This is the file where the data preprocessing is done to clean and prepare the data for the model. The full description of the data cleaning process is included in the tech report, and function docstrings describe what each function does.
- 'proper_vocab.json': The json file containing the dictionary of words used for the preprocessing of the proper coin reddit dataset for the default hyperparameter values described in the above section.
- 'meme_vocab.json': The json file containing the dictionary of words used for the preprocessing of the meme coin reddit dataset for the default hyperparameter values described in the above section.
- 'requirements.txt': The text file containing the packages for the python virtual environment that are required to run our model.

## Hyperparameters

The hyperparameters are set at the top of the ml.py file and are as follows.

#### Pre-processing:
- 'frequency': (int) Minimum frequency of words in reddit data to be considered for the word dictionary used for one-hot encoding of the reddit posts/comments. Default set to 5.
- 'timeframe': (int) Maximum number of hours a post is assumed to have an effect on price. Default set to 3.
(see tech report for full description of data cleaning)

#### ML Model:
- 'learning_rate': (float) Rate at which the model learns for each input post/comment input for stochastic gradient descent. Default set to 0.01.
- 'n_splits': (int) Number of splits for the k-fold cross validation, a.k.a. the variable 'k' in 'k-fold'. Default set to 4.
- 'hidden_size': (int) Number of parameters in hidden linear layer of RNN model. Default set to 128.