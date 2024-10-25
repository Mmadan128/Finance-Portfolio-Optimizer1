from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    amount_invested = models.FloatField()

class OptimizationResult(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    risk_level = models.FloatField()  # A scale from 0 to 1
    optimized_allocation = models.JSONField()
