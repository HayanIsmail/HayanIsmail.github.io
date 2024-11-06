from django.shortcuts import render
from django.http import JsonResponse
import yfinance as yf
import json

def stock_form(request):
    return render(request, 'stock_form.html')

def fetch_stock_data(request):
    if request.method == 'POST':
        try:
            ticker = request.POST.get('ticker')
            start_date = request.POST.get('start-date')
            end_date = request.POST.get('end-date')

            data = yf.download(ticker, start=start_date, end=end_date)
            if data.empty:
                return JsonResponse({'error': f"No data found for ticker {ticker} in the given date range."}, status=404)

            stock_data = data[['Open', 'Close']]
            result = stock_data.reset_index().to_json(orient='records', date_format='iso')
            return JsonResponse(json.loads(result), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
