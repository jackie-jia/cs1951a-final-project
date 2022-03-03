# Data Spec

## Structure of json files:

**Coin data:**

We got the historical data for 6 coins: bitcoin, ethereum, solana, dogecoin, shiba inu, and sushi. The data for all the coins is combined into a single json file with the following attributes:

- **time**
- **btc_high**: 
- **btc_low**
- **btc_open**
- **btc_volumefrom**
- **btc_volumeto**
- **btc_close**

- **eth_high**
- **eth_low**
- **eth_open**
- **eth_volumefrom**
- **eth_volumeto**
- **eth_close**

- **sol_high**
- **sol_low**
- **sol_open**
- **sol_volumefrom**
- **sol_volumeto**
- **sol_close**

- **doge_high**
- **doge_low**
- **doge_open**
- **doge_volumefrom**
- **doge_volumeto**
- **doge_close**

- **shib_high**
- **shib_low**
- **shib_open**
- **shib_volumefrom**
- **shib_volumeto**
- **shib_close**

- **sushi_high**
- **sushi_low**
- **sushi_open**
- **sushi_volumefrom**
- **sushi_volumeto**
- **sushi_close**

## Structure of csv files:

**Subreddit data:**

We have four .csv files storing the meme coin comment data, meme post data, serious coin comment data, and serious post data.

For the comment data, the attributes are:
- **id**: The unique identifier for the comment
- **submission_id**: The id of the post that the comment belongs to
- **created_utc**: The timestamp at which the comment was posted
- **body**: The text of the comment
- **score**: The number of upvotes the comment received
- **coin**: The coin that the post the comment belongs to is relevant to

For the post data, the attributes are:
- **id**: The unique identifier for the post
- **created_utc**: The timestamp at which the post was created
- **title**: The title of the post
- **selftext**: The text of the post
- **num_comments**: The number of comments the post received
- **score**: The number of upvotes the post received 
- **upvote_ratio**: The percentage of upvotes out of all votes for the post
- **coin**: The coin whose keyword search led to the discovery of the post


You will also need to provide a sample of your data in this directory. Please delete the example `sample.db` and replace it with your own data sample. ***Your sample does not necessarily have to be in the `.db` format; feel free to use `.json`, `.csv`, or any other data format that you are most comfortable with***.