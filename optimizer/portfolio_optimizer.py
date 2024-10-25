import yfinance as yf
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import List, Dict


def fetch_stock_data(stock_tickers):
    """Fetch historical stock data from Yahoo Finance."""
    try:
        stock_data = yf.download(stock_tickers, start="2000-01-01", end="2023-01-01")


        # Check if data is returned and contains 'Adj Close'
        if stock_data.empty or 'Adj Close' not in stock_data.columns:
            raise ValueError("Failed to fetch stock data: No data available for the provided tickers.")
        
        return stock_data['Adj Close']
    except Exception as e:
        raise ValueError(f"Error fetching stock data: {str(e)}")
def calculate_annualized_metrics(returns: pd.DataFrame) -> Dict:
    """Calculate annualized return and covariance matrix from stock returns."""
    
    # Check if returns DataFrame is empty
    if returns.empty:
        raise ValueError("The returns DataFrame is empty. Please check the stock data.")
    
    mean_returns = returns.mean() * 252  # Annualized returns
    
    # Calculate covariance only if there is more than one stock
    if returns.shape[1] > 1:
        cov_matrix = returns.cov() * 252  # Annualized covariance matrix
    else:
        # If there's only one stock, return a zero matrix for covariance
        cov_matrix = pd.DataFrame([[0]], columns=[returns.columns[0]], index=[returns.columns[0]])

    return {"mean_returns": mean_returns, "cov_matrix": cov_matrix}


def portfolio_performance(weights: np.array, mean_returns: pd.Series, cov_matrix: pd.DataFrame) -> Dict:
    """Calculate portfolio's expected return, volatility, and Sharpe ratio."""
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility != 0 else 0

    return {
        "return": portfolio_return,
        "volatility": portfolio_volatility,
        "sharpe_ratio": sharpe_ratio,
    }

def optimize_portfolio(
    investment_amount: float, 
    time_horizon: int, 
    stock_tickers: List[str], 
    stock_percentages: List[float]
) -> Dict:
    """
    Optimizes the portfolio by minimizing risk or maximizing Sharpe ratio.

    Parameters:
    - investment_amount: Total amount to invest.
    - time_horizon: Investment period in years.
    - stock_tickers: List of stock tickers.
    - stock_percentages: Initial weights in percentages.

    Returns:
    - A dictionary with optimized portfolio weights and performance metrics.
    """
    # Fetch stock data and calculate metrics
    stock_data = fetch_stock_data(stock_tickers)
    returns = stock_data.pct_change().dropna()  # Daily returns
    metrics = calculate_annualized_metrics(returns)
    
    # Extract annualized metrics
    mean_returns = metrics["mean_returns"]
    cov_matrix = metrics["cov_matrix"]

    # Convert input percentages to initial weights
    initial_weights = np.array(stock_percentages) / 100

    # Define the objective function to minimize (negative Sharpe ratio for maximization)
    def negative_sharpe_ratio(weights: np.ndarray) -> float:
        """Objective function to minimize."""
        performance = portfolio_performance(weights, mean_returns, cov_matrix)
        return -performance["sharpe_ratio"]

    # Define constraints and bounds
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in stock_tickers)

    # Optimize portfolio using SLSQP (Sequential Least Squares Programming)
    result = minimize(
        fun=negative_sharpe_ratio,
        x0=initial_weights,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    # Check if optimization was successful
    if not result.success:
        return {
            "success": False,
            "message": result.message
        }

    # Extract optimized weights and calculate performance
    optimized_weights = result.x
    performance = portfolio_performance(optimized_weights, mean_returns, cov_matrix)

    # Calculate allocation in currency
    allocation = {
        ticker: round(weight * investment_amount, 2) 
        for ticker, weight in zip(stock_tickers, optimized_weights)
    }

    # Prepare the results dictionary
    results = {
        "optimized_weights": {ticker: round(weight * 100, 2) for ticker, weight in zip(stock_tickers, optimized_weights)},
        "allocation": allocation,
        "expected_return": round(performance["return"] * 100, 2),  # In percentage
        "expected_volatility": round(performance["volatility"] * 100, 2),  # In percentage
        "sharpe_ratio": round(performance["sharpe_ratio"], 2),
        "success": True
    }

    return results
