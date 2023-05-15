
from decimal import Decimal
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import boto3
import datetime

def scheduledEventLoggerHandler(event, context):

    dynamodb = boto3.resource('dynamodb')
    #print(dynamodb)

    # Create a datetime object
    my_date = datetime.datetime.now()
    # Convert the datetime object to a string using strftime
    my_string = my_date.strftime("%Y-%m-%d-%H:%M:%S")


    url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
            'start':'1',
            'limit':'5000',
            'convert':'USD'
        }
    headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
        }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text, parse_float=Decimal)

        dynamodb.batch_write_item(
            RequestItems={
                'coinmarketcap': [
                    {
                        'PutRequest': {
                            'Item': {
                                'date': my_string,
                                'data': data
                            }
                        }
                    }
                ]
            }
        )
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

