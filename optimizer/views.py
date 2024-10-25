# optimizer/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .ml_models.stock_predictor import StockPredictor  # Adjust the import based on your project structure
from django.contrib.auth.models import User
from django.contrib import messages
from .portfolio_optimizer import optimize_portfolio
from .ml_models.stock_predictor import StockPredictor



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)

    return render(request, 'login.html')
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')  # Redirect to login page after registration

    return render(request, 'register.html')  # Render registration template
def dashboard_view(request):
    prediction = None
    score = None

    if request.method == 'POST':
        ticker = request.POST.get('ticker')  # Get the ticker from the form
        predictor = StockPredictor(ticker)
        score = predictor.train()  # Train the model and get the score
        recent_data = [100, 101, 102, 103, 104]  # Example recent data, replace with actual
        prediction = predictor.predict(recent_data)  # Make a prediction

    return render(request, 'dashboard.html', {'prediction': prediction, 'score': score})

def home(request):
    return render(request, 'home.html')

def optimization(request):
    results = None

    if request.method == 'POST':
        risk_level = request.POST.get('risk_level')
        investment_amount = float(request.POST.get('investment_amount'))
        time_horizon = int(request.POST.get('time_horizon'))

        # Collect stock tickers and allocations as lists
        tickers = request.POST.getlist('stock_tickers')
        percentages = [float(p) for p in request.POST.getlist('stock_percentages')]

        # Call the optimization logic
        results = optimize_portfolio(risk_level, investment_amount, time_horizon, tickers, percentages)

    return render(request, 'optimizer/optimization.html', {'results': results})

def portfolio(request):
    return render(request, 'portfolio.html')

def reports(request):
    return render(request, 'reports.html')
def home(request):
    return render(request, 'home.html')