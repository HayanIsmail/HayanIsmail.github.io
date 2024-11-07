def fetch_stock_data(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        start_date = request.POST['start-date']
        end_date = request.POST['end-date']

        data = yf.download(ticker, start=start_date, end=end_date)
        stock_data = data[['Open', 'Close']]
        
        result = stock_data.reset_index().to_json(orient='records', date_format='iso')
        
        return JsonResponse(json.loads(result), safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
