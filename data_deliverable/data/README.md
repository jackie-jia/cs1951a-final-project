# Data Spec

The samples for the data can be found [here](sample).

## Coin data:

We collected one year of hour to hour historical data for 6 different cryptocurrencies. The data is from 12:00 AM on March 1st 2021 to 12:00 AM on March 1st 2022 (inclusive) for UTC-05:00 (EST), giving 8761 hours of data for each coin. It covers three of some of the top 'proper' cryptocurrencies (Bictoin, Ethereum, Solana) and three of some of the top 'meme' cryptocurrencies (Dogecoin, Shiba Inu, Sushi) by market capitalization, and is stored it as two separate csv files for the two categories of coins. A description of the attributes for the two tables can be found below.

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

The csv file containing the range of values for these attributes can be found [here](sample/range/proper_coin_range.csv).

***Meme Coins:***

The 'meme' coins are cryptocurrencies that have some of the highest market capitalization but are considered to have been created for the 'meme. They are known to be very volatile cryptocurrencies. For this category we chose Dogecoin (DOGE), Shiba Inu (SHIB), and Sushi (SUSHI). The table is of dimensions (8761 x 16).

These coins have the same attributes described in the ***Proper Coins*** section above. The csv file containing the range of values for these attributes can be found [here](sample/range/meme_coin_range.csv).

***Further Notes:***

The Shiba Inu coin was released on June 14th 2021, so has incomplete data for the year. This coin was still included out of interest for analysis of the emergence of the coin and the high initial increase in price that followed its release.

## Reddit data:

We have four .csv files storing the meme coin comment data, meme post data, serious coin comment data, and serious post data.

For the comment data, the attributes are:
- **id**: The unique identifier for the comment
  - This attribute is a seven alphanumeric STRING.
  - Since this attribute is a string id and not a quantitative value, it is difficult to determine its distribution, but it is important to note that the id is a unique identifier, which we used to remove duplicate posts. 
  - This value is useful for analysis, and was checked to be complete.
  - We plan on using this attribute to determine the number of posts under different conditions, which we could then use to make inferences on the popularity of different coins.
  - This feature does not include any sensitive information.
- **submission_id**: The id of the post that the comment belongs to
  - This attribute is a STRING.
  - Since this attribute is a string id with approximately the same range as the range for the id column in the post data. This attribute is used to identify the post under which it was commented.
  - This value is may or may not be needed for analysis, but it is helpful for us to link the comment to its parent post.
  - This feature does not include any sensitive information.
- **created_utc**: The timestamp at which the comment was posted
- **body**: The text of the comment
  - This attribute is a STRING.
  - Since this attribute contains the text of a user's comment, there is no particular distribution of the text.
  - This data is needed for analysis, and we have filtered out all comments where the body has been marked as [removed] or [deleted] on Reddit. 
  - We plan on using this attribute to conduct sentiment analysis to analyze the sentiment around our coins.
  - This feature could potentially have sensitive information if a user were to share it, but this is highly unlikely given the nature of Reddit as a public platform. 
- **score**: The number of upvotes the comment received
  - This attribute is an INTEGER.
  - This attribute ranges from -33 to 513 for the proper coin comments dataset and -57 to 515 for the meme coin comments dataset. Both datasets are heavily right skewed, likely due to the fact that most Reddit posts do not receive many upvotes, with only a few gaining more traction.
  - This value could be used for analysis in weighting certain comments to add an extra layer to our sentiment analysis. 
  - This feature does not include any sensitive information.
- **coin**: The coin that the post the comment belongs to is relevant to
  - This attribute is a STRING
  - This attribute can take 6 possible values, which are the names of each of our coins. Out of the 6 values, "ethereum" is the most popular. 
  - This value is was created after the raw data was obtained in order to link each comment to the coin through which the comment was found when obtaining the data. 
  - We plan on using this attribute to determine the number of comments related to a coin, which can help us track its popularity in the subreddit's discourse.
  - This feature does not include any sensitive information.


For the post data, the attributes are:
- **id**: The unique identifier for the post
- **created_utc**: The timestamp at which the post was created
- **title**: The title of the post
- **selftext**: The text of the post
- **num_comments**: The number of comments the post received
- **score**: The number of upvotes the post received 
- **upvote_ratio**: The percentage of upvotes out of all votes for the post
- **coin**: The coin whose keyword search led to the discovery of the post
