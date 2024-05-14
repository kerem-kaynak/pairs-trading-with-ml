# Pairs Trading Using Machine Learning

This project is the implementation of the machine learning augmented approach to pairs trading for a bachelor's thesis. Pairs trading is a market-neutral algorithmic trading strategy that focuses on pairs of assets that share similar stochastic trends and have a mean-reverting spread.

More on market neutrality [here](https://www.investopedia.com/terms/m/marketneutral.asp).
More on pairs trading [here](https://www.investopedia.com/terms/p/pairstrade.asp).
More on mean-reversion [here](https://www.investopedia.com/terms/m/meanreversion.asp).


## Objective

Traditional pairs trading methods rely on cointegration / correlation tests alone to choose pairs and typically use OLS estimators to model the spread. The research question of this project is: Can augmenting both steps with machine learning improve the results of the overall strategy?


## Approach

The overall approach is to cluster the pairs using OPTICS, then apply statistical criteria to clustered assets to choose viable pairs. Use LSTM / LSTM Encoder Decoder to model returns and then backtest the overall strategy with completely new data. More details can be found in the implementation details section.


## Pre-requisites

- Polygon API Key (only if you'd like to refetch the data)
- Python 3.10


## Project Structure
```
-assets  # Static assets produced by the notebooks, e.g. graphs and visualizations
-data  # CSV files and pickles to store source and intermediate data
-notebooks  # Notebooks where we implement all the statistical applications and models
-utils  # Utility functions
-scripts  # Scripts to run workflows, e.g. fetch data from Polygon API
```


## Getting started

Clone the repo
```
git clone https://github.com/kerem-kaynak/pairs-trading-with-ml.git
```

Create and activate a virtual environment
```
pip3 -m venv <name-of-venv>
pip3 install -r requirements.txt
```

**From here on, you can use and run all the notebooks in the project. If you'd like to refetch the data and reconstruct the .csv file:**


Create a .env file at the root of the project and place your API key in it
```
POLYGON_API_KEY=<your-api-key>
```

Run the script to refetch the data
```
python3 price_series.py
```


## Implementation Details

### Preprocessing

1. Fetch daily price data of ETFs traded in NASDAQ using Polygon.
2. Eliminate series with missing values above a certain threshold.
3. Eliminate ETFs that were inactive at the start or end of the testing period.
4. Interpolate missing data points.
5. Compute daily returns per ticker to normalize the time series.

### Dimensionality Reduction

1. Apply PCA to returns to reduce dimensions.
2. Normalize principal components using a standard scaler.

### Clustering

1. Fit normalized principal components into OPTICS.
2. Visualize clusters using t-SNE to assess viability.
3. Compute cluster assignments for each asset, possible number of pairs and combinations.
4. Run a cointegration test to reject the null hypothesis at p=0.1, checking for a stationary linear combination of the two series. Use an Augmented Dickey-Fuller Test to estimate. More [here](https://corporatefinanceinstitute.com/resources/data-science/cointegration/).
5. Run a test to check if Hurst exponent of the spread of two series is smaller than 0.5, exhibiting mean-reverting properties. More [here](https://en.wikipedia.org/wiki/Hurst_exponent).
6. Run a test to check if half-life of the spread of two series is smaller than 260, meaning that it takes at most a year for the spread to revert back to its mean. More [here](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Nuclear_Chemistry/Nuclear_Kinetics/Half-Lives_and_Radioactive_Decay_Kinetics). I know it's from a chemistry book, the same concept of "decaying" applies to the spread reverting back to its mean.
7. Run a test to check if the spread crosses its own mean more than 48 times, averaging at least one cross per month throughout the testing period.
8. Choose pairs that pass all tests.

### Pair Selection Results Exploratory Data Analysis

1. Identify all selected pairs and fetch the full name of the asset using Polygon.
2. Plot both time series and visualize similarities.
3. Plot Moving Average Convergence Divergence (MACD) indicators for both series and visualize similarities. More [here](https://www.investopedia.com/terms/m/macd.asp).
4. Plot Relative Strength Index (RSI) indicators for both series and visualize similarities. More [here](https://www.investopedia.com/terms/r/rsi.asp).

### Modelling Returns
TBD

### Return Modelling Results Exploratory Data Analysis
TBD

### Constructing the Trading Strategy and Backtesting
TBD

### Backtesting Exploratory Data Analysis
TBD

## Todos:
- [ ] Add Makefile for scripts
- [ ] Structure data dir
- [ ] Clear unused deps and pin versions