# Tech Report

### **Where is the data from?**
- The cryptocurrency historical data is from the CryptoCompare. For social media, we chose to focus on crypto-related subreddits, in particular r/CryptoMoonShots.

#### **How did you collect your data?**
- We collected data on 6 cryptocurrencies (bitcoin, ethereum, solana, dogecoin, sushi, and shiba inu). For each coin, we used the CryptoCompare API to get its historical data hour to hour for the past year. We also scraped the r/CryptoMoonShots subreddit for posts and comments that mention each of the 6 coins. To do this, we used the Python Reddit API Wrapper (PRAW).

#### **Is the source reputable?**
- **Reddit**: Since we are looking at popularity and sentiment on social media, Reddit is a reputable source for our specific purposes.
- **Crypto**: Yes, this source does seem to be reputable.

#### **How did you generate the sample? Is it comparably small or large? Is it representative or is it likely to exhibit some kind of sampling bias?**
- Our project will compare more established coins (bitcoin, ethereum, solano) to meme coins (dogecoin, sushi, shiba_inu) by looking at relationships between price fluctuations and the content of reddit posts/comments that mention each of these coins.

#### **Are there any other considerations you took into account when collecting your data? This is open-ended based on your data; feel free to leave this blank. (Example: If it's user data, is it public/are they consenting to have their data used? Is the data potentially skewed in any direction?)**
- When choosing a subreddit to get data from, we decided to focus on a more generic one that doesn't center around just one coin. We scraped all of our data for each of the coins from r/CryptoMoonShots, which provides a broader look into what the crypto community is discussing. 

### **How clean is the data? Does this data contain what you need in order to complete the project you proposed to do?**
- The data is clean and complete for the cryptocurrencies
 
#### **How many data points are there total? How many are there in each group you care about (e.g. if you are dividing your data into positive/negative examples, are they split evenly)? Do you think this is enough data to perform your analysis later on?**

- **Reddit**: This should be more than enough data.
    - Proper posts: 10344 entries 
    - Proper comments: 41730 entries
    - Meme posts: 8640 entries
    - Meme comments: 31152 entries
- **Crypto**: This should be enough data.
    - Proper coins: 8761 entries (365 days worth), with 16 attributes each.
    - Meme coins: 8761 entries (365 days worth), with 16 attributes each.


#### Are there missing values? Do these occur in fields that are important for your project's goals?
- **Reddit**: In the selftext/body columns of our data, it may contain "[removed]" or "[deleted]" in the case that the user deleted the post/comment or it is removed by a moderator. Since we hope to use the text of the Reddit posts and comments for our analyses, the removed posts and comments are not very useful to us. Thus, we filtered these removed posts and comments out of our datasets. 
- **Crypto**: There are no missing values, this was checked before saving the data.


#### Are there duplicates? Do these occur in fields that are important for your project's goals?
- **Reddit**: There are duplicates for posts/comments that were found using multiple keywords for different coins. We want to keep some of these duplicates so that we can use those posts/comments in the analyses for all the coins they are tagged with. However, we did remove certain duplicate posts and comments in which the text is identical and found using the same coin search as we believe this is likely due to spamming and not an accurate representation of the discourse surrounding the coin. 
- **Crypto**: There are no duplicate values.

#### How is the data distributed? Is it uniform or skewed? Are there outliers? What are the min/max values? (focus on the fields that are most relevant to your project goals)
- **Crypto**: The minimum/maximum values for the cryptocurrency data can be found [here](../../data/sample/range).

#### Are there any data type issues (e.g. words in fields that were supposed to be numeric)? Where are these coming from? (E.g. a bug in your scraper? User input?) How will you fix them?
- **Reddit**: There are no data type issues.
- **Crypto**: There are no data type issues.

#### Do you need to throw any data away? What data? Why? Any reason this might affect the analyses you are able to run or the conclusions you are able to draw?
- **Reddit**: In our data collection, we only chose to obtain the columns of data that we thought were useful. In our data column, we removed some duplicates as well as posts and comments that were missing content since they would not be useful for us. Removing duplicate data and missing posts should help us obtain better analyses. While there may have been certain attributes of the data we chose not to inclue that could be helpful in our analysis, we do not think this would affect the conclusions we are able to draw in the end. All of the data kept after data cleaning will be used. 
- **Crypto**: We do not need to throw any crypto data away.

### Summarize any challenges or observations you have made since collecting your data. Then, discuss your next steps and how your data collection has impacted the type of analysis you will perform. (approximately 3-5 sentences)

One observation we have after collecting our data from Reddit is that there is simply a lot of data and many simply seem tangential to the coin and not directly talking about the coin itself. Thus, in our analysis we will focus on time periods of large fluctuations for the coins by analyzing the coin data, then using this information to analyze portions of the Reddit data that correspond to these times. We will also likely conduct sentiment analysis to explore whether there is a correlation between sentiment and the coin's price, as well as whether or not this differs between proper and meme coins. 
