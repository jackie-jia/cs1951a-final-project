# ML_redesign Folder

## ML Model

The model we chose was an Recurrent Neural Network (RNN) deep learning model, which is a supervised learning algorithm. The recurrent structure of the model allows us to learn patterns in sequences of words (reddit posts/comments) as opposed to simple word inputs. The goal is to create a prediction model that takes as input comments/posts written within the 3 hours before a coin fluctuation and outputs the direction of the coin fluctuation. In essence, the model is testing the following hypothesis:
- "The reddit posts/comments on popular cryptocurrency reddit pages made within three hours of a coin fluctuation are correlated to the direction of the coin's fluctuation."

However, this is assuming that the pattern is learnable by our RNN. Thus, our model is also testing whether the correlation (if it exists) is learnable with an RNN.

## Redesign

Due to poor performance of the model in the analysis deliverable, we decided to redesign the model. This includes the following major changes:
1. Corrected the KFold cross validation to add shuffling and set its value to a default of 4 splits.
2. The previous model had numerical instability in the linear layers of the RNN due to inputs of large sizes (reddit posts rather than comments). This led to the hidden output blowing out of proportion, and in some cases leading to subsequent loss and gradient blowups. We fixed this by adding a sigmoid to the hidden output after each linear pass.
3. The hyperparameters were tuned through accuracy testing for optimal settings. A description of each hyperparameter can be found at the bottom of the README, and the hyperparameter testing can be run by following the instructions in the following README section.

Unfortunately, as can be seen in the poster/the visualizations folder, the hyperparameter values did not improve the performance of our model. The RNN remained about as good as random, which could be caused by any of the following reasons:
- The RNN model was not appropriate for what was attempted to be learned.
- There is no underlying correlation between the reddit data three hours prior to a coin fluctuation and the coin fluctuation's direction.
- The data was insufficient for our model to find a correlation between reddit posts/comments and coin fluctuations.

### Running the Model

To run the model run the following line in a python environment:

- python3 ml.py

The hyperparameter We warn you that testing different hyperparameter values is bvery computationally heavy, and that running the entire testing suite takes multiple hours to run!

To run the hyperparameter testing, at the top of the ml.py file change the global variable 'TESTING' value to True before running the above command. The default value for 'TESTING' is False, and the above command will run a standard KFold training loop on the data with the best hyperparameters values found.

(Note that the additional package 'emoji==1.7.0' is needed. For this reason, an additional 'requirements.txt' file is included in the folder to create a new virtual environment that includes this package.)

## Files

- 'ml.py': This is the file where the RNN model lies, along with its hyperparameters, training, and testing functions. The data is retrieved from preprocess.py into this file to begin training.
- 'preprocess.py': This is the file where the data preprocessing is done to clean and prepare the data for the model. The full description of the data cleaning process is included in the tech report of the analysis deliverable, and function docstrings describe what each function does.
- testing_files: The output of the model when testing hyperparameters, saved by precaution due to the model taking multiple hours to run for different hyperaparameter settings with KFold cross-validation.
- 'proper_vocab.json': The json file containing the dictionary of words used for the preprocessing of the proper coin reddit dataset for the default hyperparameter values described in the above section.
- 'meme_vocab.json': The json file containing the dictionary of words used for the preprocessing of the meme coin reddit dataset for the default hyperparameter values described in the above section.
- 'requirements.txt': The text file containing the packages for the python virtual environment that are required to run our model.

## Hyperparameters

The hyperparameters are set at the top of the ml.py file and are as follows.

#### Pre-processing:

- TESTED 'frequency': (int) The minimum frequency of words in reddit data to be considered for the word dictionary used for one-hot encoding of the reddit posts/comments.
- CONSTANT 'timeframe': (int) Maximum number of hours a post is assumed to have an effect on price. Default set to 3.
(see tech report for full description of data cleaning)

#### ML Model:

- TESTED 'learning_rate': (float) Rate at which the model learns for each input post/comment input for stochastic gradient descent.
- CONSTANT 'n_splits': (int) Number of splits for the k-fold cross validation, a.k.a. the variable 'k' in 'k-fold'. Default set to 4.
- TESTED 'hidden_size': (int) Number of parameters in hidden linear layer of RNN model.

## Acknowledgements

The RNN learning architecture in ml.py was inspired by [this](https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html) publicly avaiable model on pytorch.org.