import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

def get_daily_pct_change(filtered_meme, filtered_proper):

    #---------- getting the average % change in price per day for meme coins --------------
    meme_grouped = filtered_meme.groupby(pd.Grouper(key='time'), sort=True)
    max_doge = meme_grouped['doge_high'].max()
    min_doge = meme_grouped['doge_low'].min()
    doge_diff = (max_doge - min_doge) / min_doge * 100

    max_shib = meme_grouped['shib_high'].max()
    min_shib = meme_grouped['shib_low'].min()
    shib_diff = (max_shib - min_shib) / min_shib * 100

    max_sushi = meme_grouped['sushi_high'].max()
    min_sushi = meme_grouped['sushi_low'].min()
    sushi_diff = (max_sushi - min_sushi) / min_sushi * 100

    meme_diffs = pd.concat([doge_diff,shib_diff,sushi_diff])
    meme_diffs_grouped = meme_diffs.groupby('time').mean().values
    nan_meme = np.isnan(meme_diffs_grouped)
    meme_diffs_grouped = meme_diffs_grouped[~ nan_meme]

    #---------- getting the average % change in price per day for proper coins --------------
    proper_grouped = filtered_proper.groupby(pd.Grouper(key='time'), sort=True)
    max_btc = proper_grouped['btc_high'].max()
    min_btc = proper_grouped['btc_low'].min()
    btc_diff = (max_btc - min_btc) / min_btc * 100

    max_eth = proper_grouped['eth_high'].max()
    min_eth = proper_grouped['eth_low'].min()
    eth_diff = (max_eth - min_eth) / min_eth * 100

    max_sol = proper_grouped['sol_high'].max()
    min_sol = proper_grouped['sol_low'].min()
    sol_diff = (max_sol- min_sol) / min_sol * 100

    proper_diffs = pd.concat([btc_diff,eth_diff,sol_diff])
    print(proper_diffs)
    proper_diffs_grouped = proper_diffs.groupby('time').mean().values
    nan_proper = np.isnan(proper_diffs_grouped)
    proper_diffs_grouped = proper_diffs_grouped[~ nan_proper]
    

    return meme_diffs_grouped, proper_diffs_grouped

def plot_price_diff_hist(filtered_meme, filtered_proper):

    meme_diff, proper_diff = get_daily_pct_change(filtered_meme, filtered_proper)

    print("MIN MEME", meme_diff.min())
    print("MAX MEME", meme_diff.max())
    print("MEAN MEME", meme_diff.mean())

    print("MIN PROPER", proper_diff.min())
    print("MAX PROPER", proper_diff.max())
    print("MEAN PROPER", proper_diff.mean())


    plt.hist(proper_diff, bins=range(0,105,1), alpha=0.5, label='proper')
    plt.hist(meme_diff, bins=range(0, 90, 1), alpha=0.5, label='meme')
    plt.legend(loc='upper right')
    plt.xlim(left=0)
    plt.xlabel('Average Change in Price per Day (%)')
    plt.ylabel('Number of Days')
    plt.title('Comparison of Daily Price Change for Meme and Proper Coins')
    #plt.savefig('../visualizations/histogram_comparison.png')
    plt.show()
    

def volatility_test(filtered_meme, filtered_proper):
    
    meme_diffs_grouped, proper_diffs_grouped = get_daily_pct_change(filtered_meme, filtered_proper)  
    [statistic, pval] = ttest_ind(meme_diffs_grouped, proper_diffs_grouped, alternative='greater')
    return statistic, pval

def main():

    MEME_COIN_PATH = '../../data_deliverable/data/coin/cleaned/meme_coin_data.csv'
    PROPER_COIN_PATH = '../../data_deliverable/data/coin/cleaned/proper_coin_data.csv'

    meme_coins = pd.read_csv(MEME_COIN_PATH)
    proper_coins = pd.read_csv(PROPER_COIN_PATH)

    meme_coins['time'] = pd.to_datetime(meme_coins['time']).dt.date
    proper_coins['time'] = pd.to_datetime(proper_coins['time']).dt.date

    filtered_meme = pd.DataFrame(meme_coins, columns=['time', 'doge_high', 'doge_low', 'shib_high', 'shib_low', 'sushi_high', 'sushi_low'])
    filtered_proper = pd.DataFrame(proper_coins, columns=['time', 'btc_high', 'btc_low', 'eth_high', 'eth_low', 'sol_high', 'sol_low'])

    plot_price_diff_hist(filtered_meme, filtered_proper)
    statistic, pval = volatility_test(filtered_meme, filtered_proper)
    print(statistic)
    print(pval)

if __name__ == '__main__':
    main()
