# optimizer/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .ml_models.stock_predictor import StockPredictor  # Adjust the import based on your project structure
from django.contrib.auth.models import User
from django.contrib import messages
from .portfolio_optimizer import optimize_portfolio
from .ml_models.stock_predictor import StockPredictor
from .forms import RegistrationForm
from .models import OptimizationReport
from django.conf import settings
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
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Automatically log the user in
            return redirect('home')  # Redirect to home or dashboard after registration
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
def dashboard_view(request):
    if request.user.is_authenticated:
        context = {
            'is_authenticated': True,
            'user': request.user,
        }
    else:
        context = {
            'is_authenticated': False,
        }
    return render(request, 'dashboard.html', context)

def home(request):
    return render(request, 'home.html')




def optimization(request):
    results = None

    if request.method == 'POST':
        try:
            # Get user inputs from the form
            investment_amount = float(request.POST.get('investment_amount'))
            time_horizon = int(request.POST.get('time_horizon'))
            stock_tickers = [ticker.strip() for ticker in request.POST.get('stock_tickers').split(',')]
            stock_percentages_str = request.POST.get('stock_percentages')  # Assume this comes as a string
            stock_percentages = [float(p.strip()) for p in stock_percentages_str.split(',')]  # Split and convert

            # Call the optimize_portfolio function
            results = optimize_portfolio(investment_amount, time_horizon, stock_tickers, stock_percentages)

            # Save the optimization report
            report = OptimizationReport(
                investment_amount=investment_amount,
                time_horizon=time_horizon,
                stock_tickers=','.join(stock_tickers),
                stock_percentages=','.join(map(str, stock_percentages)),
                expected_return=results['expected_return'],
                expected_volatility=results['expected_volatility'],
                sharpe_ratio=results['sharpe_ratio']
            )
            report.save()

        except ValueError as e:
            results = {'success': False, 'message': f"Invalid input: {str(e)}"}

    return render(request, 'optimization.html', {'results': results})
def portfolio(request):
    # Define your portfolio
    portfolio = {
        'AAPL': {'shares': 50, 'purchase_price': 120.00},
        'MSFT': {'shares': 30, 'purchase_price': 200.00},
        'GOOGL': {'shares': 10, 'purchase_price': 1500.00},
        'TSLA': {'shares': 5, 'purchase_price': 600.00},
    }

    # Prepare a list of tickers for AJAX request
    tickers = list(portfolio.keys())

    # Pass tickers to the context
    context = {
        'portfolio': portfolio,
        'tickers': tickers,
    }
    
    return render(request, 'portfolio.html', context)

from .models import OptimizationReport

def reports(request):
    # Fetch all optimization reports
    reports = OptimizationReport.objects.all().distinct()  # Ensure distinct records
    
    # Preprocess the stock tickers and percentages
    for report in reports:
        report.stock_tickers_list = [ticker.strip() for ticker in report.stock_tickers.split(',')]
        report.stock_percentages_list = [percentage.strip() for percentage in report.stock_percentages.split(',')]
    
    return render(request, 'reports.html', {'reports': reports})
def home(request):
    return render(request, 'home.html')

# views.py

from django.http import JsonResponse
import yfinance as yf

def fetch_realtime_data(request):
    if request.method == "GET":
        tickers = request.GET.getlist('tickers[]')  # Expecting an array of tickers
        data = {}
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            current_price = stock.history(period='1d')['Close'].iloc[-1]  # Get the last closing price
            data[ticker] = current_price
        return JsonResponse(data)




from django.conf import settings
from web3 import Web3
import logging
logger = logging.getLogger(__name__)

# Your ABI stored as a Python list
ABI = [
    {
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "reward", "type": "uint256"}],
        "name": "distributeRewards",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "balances",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getBalance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getInvestors",
        "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "investors",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]


from django.shortcuts import render
from django.conf import settings
from web3 import Web3



from django.shortcuts import render
from django.conf import settings
from web3 import Web3

from django.conf import settings
from django.shortcuts import render
from web3 import Web3


def smart_form_view(request):
    txn_hash = None
    error_message = None

    if request.method == 'POST':
        action = request.POST.get('action')

        # Connect to Ethereum node
        w3 = Web3(Web3.HTTPProvider(settings.ETH_NODE_URL))

        # Check if the connection to the provider is successful
        if not w3.isConnected():
            error_message = "Unable to connect to Ethereum node."
            return render(request, 'smart_form.html', {
                'txn_hash': txn_hash,
                'error_message': error_message,
            })

        # Action handling
        if action == "transfer":
            recipient_address = request.POST.get('recipient_address')
            amount = request.POST.get('amount')

            # Validate recipient address
            if not w3.isAddress(recipient_address):
                error_message = "Invalid recipient address."
                return render(request, 'smart_form.html', {
                    'txn_hash': txn_hash,
                    'error_message': error_message,
                })

            try:
                # Get the transaction count for the default account
                default_account = settings.DEFAULT_ACCOUNT  # Ensure you set this in your settings
                nonce = w3.eth.getTransactionCount(default_account)

                # Prepare transaction
                tx = {
                    'to': recipient_address,
                    'value': w3.toWei(float(amount), 'ether'),  # Convert amount to wei
                    'gas': 2000000,
                    'gasPrice': w3.toWei('50', 'gwei'),
                    'nonce': nonce,
                }

                # Sign the transaction
                signed_tx = w3.eth.account.sign_transaction(tx, private_key=settings.PRIVATE_KEY)

                # Send the signed transaction
                txn_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

            except Exception as e:
                error_message = f"Transaction failed: {str(e)}"

    return render(request, 'smart_form.html', {
        'txn_hash': txn_hash.hex() if txn_hash else None,
        'error_message': error_message,
    })