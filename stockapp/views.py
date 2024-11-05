from django.shortcuts import render
from django.http import JsonResponse
import yfinance as yf
import json

def stock_form(request):
    return render(request, 'stockapp/stock_form.html')

def fetch_stock_data(request):
    if request.method == 'POST':
        try:
            print("POST request received")
            print(request.POST)
            ticker = request.POST['ticker']
            start_date = request.POST['start-date']
            end_date = request.POST['end-date']
            print(f"Ticker: {ticker}, Start Date: {start_date}, End Date: {end_date}")

            data = yf.download(ticker, start=start_date, end=end_date)
            print(f"Fetched data for {ticker}:")
            print(data)

            if data.empty:
                return JsonResponse({'error': f"No data found for ticker {ticker} in the given date range."}, status=404)

            stock_data = data[['Open', 'Close']]
            result = stock_data.reset_index().to_json(orient='records', date_format='iso')
            print(result)  # Debug the result

            return JsonResponse(json.loads(result), safe=False)
        except Exception as e:
            print("Error occurred:", e)
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
