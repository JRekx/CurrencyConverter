from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Function to fetch exchange rates from the API
def get_exchange_rates():
    url = 'https://api.exchangerate.host/latest'
    response = requests.get(url)
    data = response.json()

    # Create a new dictionary to store currency information
    currency_data = {}

    # Add currency symbols and codes to the currency_data dictionary
    for currency, rate in data.get('rates', {}).items():
        currency_info = get_currency_info(currency)
        currency_data[currency] = {
            'rate': rate,
            'symbol': currency_info['symbol'],
            'code': currency_info['code']
        }

    return currency_data

# Function to get currency symbols and codes based on currency code
def get_currency_info(currency_code):
    # Define a dictionary mapping currency codes to symbols and names
    currency_info = {
        'USD': {'symbol': '$', 'code': 'USD'},
        'EUR': {'symbol': '€', 'code': 'EUR'},
        # Add more currencies as needed
    }

    return currency_info.get(currency_code, {'symbol': '', 'code': currency_code})

# Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    exchange_rates = get_exchange_rates()

    if request.method == 'POST':
        amount = float(request.form['amount'])
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']

        if from_currency in exchange_rates and to_currency in exchange_rates:
            converted_amount = amount * exchange_rates[to_currency]['rate'] / exchange_rates[from_currency]['rate']
            result_amount = f"{converted_amount:.2f}"  # Format the converted amount with two decimal places
            result_from_currency_symbol = exchange_rates[from_currency]['symbol']
            result_to_currency_symbol = exchange_rates[to_currency]['symbol']
            result = f"{amount} {exchange_rates[from_currency]['code']} is equal to {result_amount} {exchange_rates[to_currency]['code']}"
        else:
            result = "Invalid currency codes. Please enter valid currency codes."

        return render_template('index.html', result=result, exchange_rates=exchange_rates,
                               result_amount=result_amount, result_from_currency_symbol=result_from_currency_symbol,
                               result_to_currency_symbol=result_to_currency_symbol)

    return render_template('index.html', exchange_rates=exchange_rates)

if __name__ == '__main__':
    app.run(debug=True)
