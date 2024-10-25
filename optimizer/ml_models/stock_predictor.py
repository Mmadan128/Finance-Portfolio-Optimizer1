# optimizer/ml_models/stock_predictor.py
import yfinance as yf
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Ensure reproducibility
np.random.seed(42)
torch.manual_seed(42)

# LSTM Model Definition
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)  # Predict a single output (price change)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Output from the last time step
        return out

class StockPredictor:
    def __init__(self, ticker, time_step=60):
        self.ticker = ticker
        self.time_step = time_step  # Number of time steps for LSTM input
        self.model = LSTMModel(input_size=5, hidden_size=50, num_layers=2).to(self.get_device())
        self.scaler = MinMaxScaler()

    def get_device(self):
        # Check if GPU is available
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def fetch_data(self):
        # Fetch historical data using yfinance
        data = yf.download(self.ticker, start="2010-01-01", end="2023-01-01")
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        return data

    def prepare_data(self, data):
        # Normalize the data
        scaled_data = self.scaler.fit_transform(data)

        # Create dataset for LSTM
        X, y = [], []
        for i in range(len(scaled_data) - self.time_step):
            X.append(scaled_data[i:i + self.time_step])
            y.append(scaled_data[i + self.time_step, 3])  # Predict 'Close' price

        X, y = np.array(X), np.array(y)

        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Convert to PyTorch tensors
        X_train = torch.tensor(X_train, dtype=torch.float32).to(self.get_device())
        X_test = torch.tensor(X_test, dtype=torch.float32).to(self.get_device())
        y_train = torch.tensor(y_train, dtype=torch.float32).reshape(-1, 1).to(self.get_device())
        y_test = torch.tensor(y_test, dtype=torch.float32).reshape(-1, 1).to(self.get_device())

        return X_train, X_test, y_train, y_test

    def train(self, epochs=50, batch_size=32):
        data = self.fetch_data()
        X_train, X_test, y_train, y_test = self.prepare_data(data)

        # Loss function and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        # Train the model
        self.model.train()
        for epoch in range(epochs):
            for i in range(0, len(X_train), batch_size):
                batch_X = X_train[i:i + batch_size]
                batch_y = y_train[i:i + batch_size]

                # Forward pass
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)

                # Backward pass and optimization
                loss.backward()
                optimizer.step()

            if epoch % 10 == 0:
                print(f"Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}")

        # Evaluate the model on the test set
        self.model.eval()
        with torch.no_grad():
            test_outputs = self.model(X_test)
            test_loss = criterion(test_outputs, y_test)
            print(f"Test Loss: {test_loss.item():.4f}")

    def predict(self, recent_data):
        # Prepare the input (last 'time_step' data points)
        recent_data = self.scaler.transform(recent_data)
        recent_data = torch.tensor(recent_data, dtype=torch.float32).reshape(1, self.time_step, -1).to(self.get_device())

        # Make prediction
        self.model.eval()
        with torch.no_grad():
            prediction = self.model(recent_data)

        # Inverse scale the prediction
        predicted_price = self.scaler.inverse_transform(
            np.hstack((np.zeros((1, 4)), prediction.cpu().numpy()))
        )[0, 4]  # Extract the 'Close' price

        return predicted_price

# Example usage
if __name__ == "__main__":
    ticker = "AAPL"  # Example stock ticker
    predictor = StockPredictor(ticker)

    print("Training the LSTM model...")
    predictor.train(epochs=50)

    # Fetch recent data for prediction
    recent_data = predictor.fetch_data().tail(60)  # Last 60 days of data
    print(f"Predicted Close Price: {predictor.predict(recent_data)}")
