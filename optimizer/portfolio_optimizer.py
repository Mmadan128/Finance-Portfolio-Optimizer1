# portfolio_optimizer.py

import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def fetch_stock_data(stock_tickers):
    """Fetch historical stock data from Yahoo Finance."""
    stock_data = yf.download(stock_tickers, start="2020-01-01", end="2023-01-01")['Adj Close']
    return stock_data

def calculate_portfolio_return(weights, returns):
    """Calculate expected portfolio return."""
    return np.sum(weights * returns.mean()) * 252  # Annualize return

def calculate_portfolio_volatility(weights, returns):
    """Calculate portfolio volatility."""
    return np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))  # Annualize volatility


def optimize_portfolio(investment_amount, time_horizon, stock_tickers, stock_percentages):
    # Fetch historical data for the tickers
    stock_data = yf.download(stock_tickers, period=f'{time_horizon}y')
    returns = stock_data['Adj Close'].pct_change().mean()
    covariance = stock_data['Adj Close'].pct_change().cov()

    # Convert stock_percentages to a numpy array
    weights = np.array(stock_percentages) / 100  # Convert percentages to decimal
    portfolio_return = np.sum(returns * weights) * 252  # Annualize return
    portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(covariance * 252, weights)))  # Annualized risk

    # Dummy optimized portfolio results
    optimized_results = {
        'stocks': weights.sum() * 100,  # Total stock allocation
        'bonds': (1 - weights.sum()) * 100,  # Remaining to bonds
        'real_estate': 0,  # Placeholder
    }
    
    return optimized_results
