# Data Spec

## Structure of json files:

**Coin data:**

We got one year of hour to hour historical data for 6 different cryptocurrencies. The data is from 12:00 AM on March 1st 2021 to 12:00 AM on March 1st 2022 (inclusive) for UTC-05:00 (EST), giving 8761 data points for each coin. It covers three of some of the top 'proper' cryptocurrencies (Bictoin, Ethereum, Solana) and three of some of the top 'meme' cryptocurrencies (Dogecoin, Shiba Inu, Sushi) by market capitalization.

***Proper Coins:***

The 'proper' coins are cryptocurrencies that have some of the highest market capitalization out there. They are treated more seriously than others as new potential currencies. In fact, two of those that we chose to collect data for are starting to be accepted as forms of payment by certain businesses. For this category we chose Bitcoin (BTC), Ethereum (ETH), and Solona (SOL). 

The data for these coins has the following attributes:
- **time**
  - This attribute is the date timestamp for the start of this data point.
  - This attribute was converted to the date format, and shows up only once in the table for all three coins.
  - The range of values is 12:00 AM on March 1st 2021 to 12:00 AM on March 1st 2022.
  - The values are uniformly distributed in order by hour from 12:00 AM on March 1st 2021 to 12:00 AM on March 1st 2022.
  - This attribute is an identifier, and is unique. 
  - Since this value is meant to be unique and outputted by the API, no duplicate records exist.
  - This value is required, and was checked to be complete.
  - We plan on using this attribute to find the time at which large fluctuations in price took place. We then plan on linking posts of a certain time interval before the time of the fluctuation to the fluctuation for text analysis.
  -  This feature does not include any sensitive information.
All three coins then have the following six attributes differentiated by the suffix 'SYMBOL_' in the column name:
- **high**:
  - This attribute is the highest price of the coin during the hour following its corresponding ***time*** attribute.
  - This attribute is of the type FLOAT.
  - Its range of values is minimum to maximum price of the cryptocurrency in the given year expressed in USD.
  - The distribution of this attribute is complex, and follows the fluctuations of the specific cryptocurrency.
  - This is not an identifier, and the values are not necessarily unique, so it will not be used to identify duplicate records.
  - This value is required for analysis, and was checked to be complete.
  - We plan on using this attribute to spot large fluctuations in price.
  - This feature does not include any sensitive information.
- **low**
  - This attribute is the lowest price of the coin during the hour following its corresponding ***time*** attribute.
  - This attribute is of the type FLOAT.
  - Its range of values is minimum to maximum price of the cryptocurrency in the given year expressed in USD.
  - The distribution of this attribute is complex, and follows the fluctuations of the specific cryptocurrency.
  - This is not an identifier, and the values are not necessarily unique, so it will not be used to identify duplicate records.
  - This value is required for analysis, and was checked to be complete.
  - We plan on using this attribute to spot large fluctuations in price.
  - This feature does not include any sensitive information.
- **open**
Type of data that will be used for the representation.
Default value
Range of value.
Simplified analysis of the distribution of values
Is this an identifier?
Are these values unique?
Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how?
Is this a required value?
Do you plan to use this attribute/feature in the analysis? If so, how?
Does this feature include potentially sensitive information? If so, how do you suggest handling such issues?

- **volumefrom**
- **volumeto**
- **close**

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

The samples for the data can be found [here](sample).
