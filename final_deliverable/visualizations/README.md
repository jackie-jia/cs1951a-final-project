# Visualizations

The visualizations found in this folder are the accuracy results for the different hyperparameter values from our redesign of the RNN model. The hyperparameters that were tested were: frequency (minimum frequency necessary for a word to be considered in the dictionary in pre-processing), learning rate (multiplier on the loss gradient when learning), and the hidden layer size (the size of the linear matrix in the hidden layer of the RNN).

As we can see, the RNN model remained about as good as random for all hyperparameters, which could be caused by any of the following reasons:
- The RNN model was not appropriate for what was attempted to be learned.
- There is no underlying correlation between the reddit data three hours prior to a coin fluctuation and the coin fluctuation's direction.
- The data was insufficient for our model to find a correlation between reddit posts/comments and coin fluctuations.