# Data Spec

## Structure of json files:

**Coin data:**

We got one year of hour to hour historical data for 6 different cryptocurrencies. The data is from 12:00 AM on March 1st 2021 to 12:00 AM on March 1st 2022 (inclusive) for UTC-05:00 (EST), giving 8761 data points for each coin. It covers three of some of the top 'proper' cryptocurrencies (Bictoin, Ethereum, Solana) and three of some of the top 'meme' cryptocurrencies (Dogecoin, Shiba Inu, Sushi) by market capitalization.

***Proper Coins:***

The 'proper' coins are cryptocurrencies that have some of the highest market capitalization out there. They are treated more seriously than others as new potential currencies. In fact, two of those that we chose to collect data for are starting to be accepted as forms of payment by certain businesses. For this category we chose Bitcoin (BTC), Ethereum (ETH), and Solona (SOL). The table is of dimensions (8761 x 16).

The data for these coins has the following attributes:
- **time**
  - The date timestamp for the start of this data point (in UTC format, not EST)
  - This attribute was converted to the date format, and shows up only once in the table for all three coins.
  - The range of values is 05:00 AM (UTC) on March 1st 2021 to 12:00 AM (UTC) on March 1st 2022.
  - The values are uniformly distributed in order by hour from 12:00 AM (UTC) on March 1st 2021 to 12:00 AM (UTC) on March 1st 2022.
  - This attribute is an identifier, and is unique. 
  - Since this value is meant to be unique and outputted by the API, no duplicate records exist.
  - This value is required, and was checked to be complete.
  - We plan on using this attribute to find the time at which large fluctuations in price and demand took place. We then plan on linking reddit posts in a certain time interval before the time of the fluctuation to the fluctuation for text analysis purposes.
  -  This feature does not include any sensitive information.

All three coins then have the following five attributes differentiated by the suffix 'SYMBOL_' in the column name:

- **high**
  - The highest price of the coin in USD during the hour following its corresponding ***time*** attribute.
  - This attribute is of the type FLOAT.
  - Its range of values is minimum to maximum price of the cryptocurrency in the given year.
  - The distribution of this attribute is complex, and follows the fluctuations of the specific cryptocurrency.
  - This is not an identifier, and the values are not necessarily unique, so it will not be used to identify duplicate records.
  - This value is required for analysis, and was checked to be complete.
  - We plan on using this attribute to spot small fluctuations in price within the following hour.
  - This feature does not include any sensitive information.
- **low**
  - The lowest price of the coin in USD during the hour following its corresponding ***time*** attribute.
  - This attribute is of the type FLOAT.
  - Its range of values is minimum to maximum price of the cryptocurrency in the given year.
  - The distribution of this attribute is complex, and follows the fluctuations of the specific cryptocurrency.
  - This is not an identifier, and the values are not necessarily unique, so it will not be used to identify duplicate records.
  - This value is required for analysis, and was checked to be complete.
  - We plan on using this attribute to spot small fluctuations in price within the following hour.
  - This feature does not include any sensitive information.
- **open**
  - The price of the coin in USD at the exact time of its corresponding ***time*** attribute.
  - This attribute is of the type FLOAT.
  - Its range of values is minimum to maximum price of the cryptocurrency in the given year.
  - The distribution of this attribute is complex, and follows the fluctuations of the specific cryptocurrency.
  - This is not an identifier, and the values are not necessarily unique, so it will not be used to identify duplicate records.
  - This value is required for analysis, and was checked to be complete.
  - We plan on using this attribute to spot large fluctuations in price over multiple hours.
  - This feature does not include any sensitive information.
- **volumefrom**
  - The total amount of the coin traded into USD during the hour following its corresponding ***time*** attribute (in units of the coin).
  - This attribute is of the type FLOAT.
  - Its range of values is minimum to maximum number of coins traded into USD in the given year.
  - The distribution of this attribute is complex, and follows the changes in demand for the currency.
  - This is not an identifier, and the values are not necessarily unique, so it will not be used to identify duplicate records.
  - This value is required for analysis, and was checked to be complete.
  - The value will be used to check fluctuations in currency demand.
  - This feature does not include any sensitive information.
- **volumeto**
  - The total amount of USD traded into the coin during the hour following its corresponding ***time*** attribute (in units of USD).
  - This attribute is of the type FLOAT.
  - Its range of values is minimum to maximum number of coins traded into USD in the given year.
  - The distribution of this attribute is complex, and follows the changes in demand for the currency.
  - This is not an identifier, and the values are not necessarily unique, so it will not be used to identify duplicate records.
  - This value is required for analysis, and was checked to be complete.
  - The value will be used to check fluctuations in currency demand.
  - This feature does not include any sensitive information.
 
***Meme Coins:***

The 'meme' coins are cryptocurrencies that have some of the highest market capitalization out there. They are treated more seriously than others as new potential currencies. In fact, two of those that we chose to collect data for are starting to be accepted as forms of payment by certain businesses. For this category we chose Bitcoin (BTC), Ethereum (ETH), and Solona (SOL). The table is of dimensions (8761 x 16).
***Further Notes:***


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
