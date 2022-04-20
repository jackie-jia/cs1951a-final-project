# Tech Report
This is where you can type out your tech report.

## Hypothesis Test 1

#### A defined hypothesis or prediction task, with clearly stated metrics for success.
- *State hypothesis*: The Reddit post frequency distribution for established cryptocurrencies differs from the distribution of post frequency for meme coins. Specifically, we predict that established cryptocurrencies have a higher post frequency within a 24 hour time frame. 
The null hypothesis is that there is no significant difference between the mean frequency of posts for proper/established cryptocurrencies compared to the mean frequency of posts for meme coins. 
The alternative hypothesis is that there is a significant difference between the mean frequency of posts for proper coins compared to meme coins. Specifically, we would expect the proper coin post frequency to be significantly greater than the meme coin post frequency. 
*NOTE: This hypothesis was tested on both the post frequencies and comment 


#### Why did you use this statistical test or ML algorithm? Which other tests did you consider or evaluate?
- I conducted a two sample T-test to compare the mean frequencies of the established/proper coins versus the meme coins because this tests the null hypothesis that two independent samples have identical expected values. Since the null hypothesis in this case is that the mean meme coin post frequency and the mean proper coin post frequency, a two sample T-test makes the most sense to use. Since there are over 8000 posts in both datasets (meme and proper), we can use the central limit theorem and thus can apply the T-test. I also considered using a paired T-test since the data could be paired based on the date to directly compare the frequency of posts for each day. However, the date range for the meme post data was much larger than that of the proper coin post data, and it was hard to determine whether this was a result of differences in frequencies of posts or rather just due to the way we scraped our data from Reddit. Hence, I decided to simply use a two sample T-test because the dates in the data are not exactly paired one-to-one. 


#### How did you measure success or failure? Why that metric/value? What challenges did you face evaluating the model? 
- Success was measured by the p-value obtained from the T-test, as this shows us whether or not the differences in mean post/comment frequency were statistically significant. 

#### Did you have to clean or restructure your data?
- I had to clean my data by first converting the UNIX timestamps to readable datetimes. Then, I calculated the number of posts for each unique day in the four datasets I used (proper_posts, proper_comments, meme_posts, meme_comments). 


#### What is your interpretation of the results? Do accept or deny the hypothesis, or are you satisfied with your prediction accuracy? For prediction projects, we expect you to argue why you got the accuracy/success metric you have. Intuitively, how do you react to the results? Are you confident in the results?
- From my two sample t-test, I obtained a T-statistic of 2.7997 and a p-value of 0.0053 for the test on post frequencies, and a T-statistic of 3.8502 and a p-value of 0.00013 for the test on comment frequencies. Hence, at a 99% significance level, I can reject the null hypothesis and conclude that there is a statistically significant difference between the proper post frequency and the meme post frequency. The same can be said about the comment frequencies. In particular, the proper coins had higher post and comment frequencies, meaning that they had greater amounts of discussion surrounding them on social media (specifically in the subreddit r/CryptoMoonshots). 
- The results correspond to my initial belief on the data because we would expect that the more established coins are more well-known and have more conversation surrounding them and thus it makes sense that the post frequency for the proper coins is higher than those for the meme coins. Due to the large amount of data we obtained and the very low p-values, I am fairly confident with the results of my hypothesis test. 

#### Do you believe the tools for analysis that you chose were appropriate? If Yes/No why or what method could have been used?
- I believe the tools used for analysis were appropriate for this specific hypothesis, although I think it could also be interesting to look at post frequencies within smaller timeframes (per hour instead of per day, for example) as well as looking at the variance in the post frequency rather than simply the mean frequencies. 

#### Was the data adequate for your analysis? If not what aspects of the data was problematic and how could you have remedied that?
- The data was adequate for our analysis. However, since the data was scraped, we may not have the entire set of data from Reddit to get an exact and accurate result. For example, we are unable to differentiate between a day with 0 posts and a day for which no data was scraped. I did check the ranges for the post/comment frequencies for each dataset, and the minimum was 6 for both meme and proper coin comments. Hence, I made the assumption that dates which did not exist in the dataset were a result of not scraping any data for those days rather than a lack of posts on those days. This issue could potentially be remedied by perhaps obtaining subreddit activity data rather than directly obtaining the posts, although this may not be particularly feasible either. Overall, due to the large sample size, our data seems adequate for our analysis. Our method of data scraping could potentially impact the calculated post frequencies, but likely not enough for it to significantly change the results we obtained in the end. 

## Hypothesis Test 3

#### A defined hypothesis or prediction task, with clearly stated metrics for success.
- *State hypothesis*: The average daily price percentage change for established cryptocurrencies differs from that of meme coins. Specifically, we predict that meme cryptocurrencies have a larger mean daily price percentage change. 
The null hypothesis is that the mean daily price percentage change for meme cryptocurrencies is equal to that of established coins. 
The alternative hypothesis is that the mean daily price percentage change for meme cryptocurrencies is greater than that of established coins.

#### Why did you use this statistical test or ML algorithm? Which other tests did you consider or evaluate?
- I conducted a two sample T-test to compare the mean daily price change of the established/proper coins versus the meme coins because this tests the null hypothesis that two independent samples have identical expected values. Since the null hypothesis in this case is that the mean meme coin daily price change and the mean proper coin daily price change are equal, a two sample T-test makes the most sense to use. Since there are 365 data points in both datasets (average price percentage change for each day in a year), we can use the central limit theorem and thus can apply the T-test. We also considered using a paired T-test, but that is directly applicable to two correlated samples whereas our samples are of two independent sets of coin data.

#### How did you measure success or failure? Why that metric/value? What challenges did you face evaluating the model? 
- Success was measured by the p-value obtained from the T-test, as this shows us whether or not the mean price percentage change of the meme coins were statistically greater than that of the proper coins. 

#### Did you have to clean or restructure your data?
- I had to clean my data by converting the datetimes to just dates so that I could group the data by date and subsequently calculate the mean price change per day. I performed this conversion and calculation across all 6 coin datasets (3 meme and 3 established). Then, I concatenated all the meme coin data and all the propercoin data into two DataFrames. I grouped each of the two DataFrames by date and averaged the data by date.

#### What is your interpretation of the results? Do accept or deny the hypothesis, or are you satisfied with your prediction accuracy? For prediction projects, we expect you to argue why you got the accuracy/success metric you have. Intuitively, how do you react to the results? Are you confident in the results?
- From my two sample t-test, I obtained a T-statistic of 6.90596 and a p-value of 5.4331e-12. Hence, at a 99% significance level, I can reject the null hypothesis and conclude that the average daily percentage change for meme coins is significantly greater than that of the proper coins. 
- The results correspond to my initial belief on the data because we would expect that the price of the more established coins are more stable while the meme coin prices would be more volatile. This makes sense because the value of meme cryptocurrencies is largely driven by social media support and activity. Hence, they would be much more subject to sudden changes in value in shorter periods of time than established/proper coins. Due to the fair amount of data we obtained and the very low p-values, I am fairly confident with the results of my hypothesis test. 

#### Do you believe the tools for analysis that you chose were appropriate? If Yes/No why or what method could have been used?
- I believe the tools used for analysis were appropriate for this specific hypothesis, although a potential follow up test would be to look at price changes over larger time frames (per week instead of per day, for example). There are many ways to look at price volatility, and perhaps averaging daily changes may be too narrow of an approach. Another metric with which to evaluate volatility is standard deviation.

#### Was the data adequate for your analysis? If not what aspects of the data was problematic and how could you have remedied that?
- The data was adequate for our analysis. We had sufficient data to apply the CLT and perform a t-test on our data. However, for more interesting analyses and more data, it would be useful to have access to data over a longer period of time (our dataset is limited to a year’s worth of data from 3/1/2021 to 3/1/2022).  

## Visualization 1: Histogram Comparison 
### For your visualization, why did you pick this graph? What alternative ways might you communicate the result? Were there any challenges visualizing the results, if so, what where they? Will your visualization require text to provide context or is it standalone (either is fine, but it's recognize which type your visualization is)?
- I picked a histogram because I wanted to visualize the distribution (over a sample size of 365 days) of the average percentage change in price per day. A histogram allows me to graph the frequency of a metric, so that's why I chose this type of graph. Another way in which I could have communicated the result was a box plot, which would provide additional information about the 25th, 50th and, 75th percentiles of each of the data sets, but I thought that a histogram would be easier to interpret. For the most part, I think that the legend, axis labels, and title of the graph provide enough information to interpret the visualization.


### Full results + graphs (at least 1 stats/ml test and at least 1 visualization). You should push your visualizations to the /analysis_deliverable/visualizations folder in your repo. Depending on your model/test/project we would ideally like you to show us your full process so we can evaluate how you conducted the test!


You can also attach photos from your repo

