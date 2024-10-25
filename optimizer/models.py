from django.db import models

class Portfolio(models.Model):
    user = models.CharField(max_length=100)
    stock_symbol = models.CharField(max_length=10)
    amount_invested = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.stock_symbol}"

class OptimizationResult(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    risk_level = models.FloatField()
    optimized_allocation = models.JSONField()

    def __str__(self):
        return f"Optimization for {self.portfolio.stock_symbol}"
