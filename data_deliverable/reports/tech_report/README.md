# Tech Report

### Where is the data from?
The cryptocurrency historical data is from the CryptoCompare. For social media, we chose to focus on crypto-related subreddits, in particular r/CryptoMoonShots.

#### How did you collect your data?
We collected data on 6 cryptocurrencies (bitcoin, ethereum, solana, dogecoin, sushi, and shiba_inu). For each coin, we used the CryptoCompare API to get its historical data from the past year. We also scraped the r/CryptoMoonShots subreddit for posts and comments that mention each of the 6 coins. To do this, we used the Python Reddit API Wrapper (PRAW).

#### Is the source reputable?
Yes

#### How did you generate the sample? Is it comparably small or large? Is it representative or is it likely to exhibit some kind of sampling bias?
Our project will compare more established coins (bitcoin, ethereum, solano) to meme coins (dogecoin, sushi, shiba_inu) by looking at relationships between price fluctuations and the content of reddit posts/comments that mention each of these coins.


#### Are there any other considerations you took into account when collecting your data? This is open-ended based on your data; feel free to leave this blank. (Example: If it's user data, is it public/are they consenting to have their data used? Is the data potentially skewed in any direction?)
When choosing a subreddit to get data from, we decided to focus on a more generic one that doesn't center around just one coin. We scraped all of our data for each of the coins from this one subreddit that provides a broader look into what the crypto community is discussing. 

### How clean is the data? Does this data contain what you need in order to complete the project you proposed to do? (Each team will have to go about answering this question differently, but use the following questions as a guide. Graphs and tables are highly encouraged if they allow you to answer these questions more succinctly.)


#### How many data points are there total? How many are there in each group you care about (e.g. if you are dividing your data into positive/negative examples, are they split evenly)? Do you think this is enough data to perform your analysis later on?

Reddit: 



#### Are there missing values? Do these occur in fields that are important for your project's goals?


#### Are there duplicates? Do these occur in fields that are important for your project's goals?


#### How is the data distributed? Is it uniform or skewed? Are there outliers? What are the min/max values? (focus on the fields that are most relevant to your project goals)

#### Are there any data type issues (e.g. words in fields that were supposed to be numeric)? Where are these coming from? (E.g. a bug in your scraper? User input?) How will you fix them?

#### Do you need to throw any data away? What data? Why? Any reason this might affect the analyses you are able to run or the conclusions you are able to draw?


### Summarize any challenges or observations you have made since collecting your data. Then, discuss your next steps and how your data collection has impacted the type of analysis you will perform. (approximately 3-5 sentences)
