import os
import requests

def scheduledEventLoggerHandler(event, context):
    # set up the API endpoint and headers
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {'X-CMC_PRO_API_KEY': os.environ['1e302b38-b278-493b-8303-fa7c56a6c17a']}
    
    # set up the API parameters (in this case, we're fetching the Bitcoin price)
    params = {'symbol': 'BTC'}
    
    # make the API request
    response = requests.get(url, headers=headers, params=params)
    
    # parse the response and extract the Bitcoin price
    data = response.json()
    price = data['data']['BTC']['quote']['USD']['price']
    
    # log the Bitcoin price and return it as the response body
    print('Current Bitcoin price: ${}'.format(price))
    return {
        'statusCode': 200,
        'body': 'Current Bitcoin price: ${}'.format(price)
    }