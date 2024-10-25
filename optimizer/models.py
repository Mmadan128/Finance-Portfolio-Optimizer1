from django.db import models

class Portfolio(models.Model):
    user = models.CharField(max_length=100)
    stock_symbol = models.CharField(max_length=10)
    amount_invested = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.stock_symbol}"


class OptimizationReport(models.Model):
    investment_amount = models.FloatField()
    time_horizon = models.IntegerField()
    stock_tickers = models.CharField(max_length=255)  # Comma-separated string
    stock_percentages = models.CharField(max_length=255)  # Comma-separated string
    expected_return = models.FloatField()
    expected_volatility = models.FloatField()
    sharpe_ratio = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return f"Optimization for {self.portfolio.stock_symbol}"
class PortfolioOptimization(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Link to Django's built-in User model
    optimized_weights = models.JSONField()  # Store optimized weights as JSON
    expected_return = models.FloatField()
    expected_volatility = models.FloatField()
    sharpe_ratio = models.FloatField()
    allocation = models.JSONField()  # Store allocation as JSON
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the date/time when created

    def __str__(self):
        return f"Optimization result for {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"    
