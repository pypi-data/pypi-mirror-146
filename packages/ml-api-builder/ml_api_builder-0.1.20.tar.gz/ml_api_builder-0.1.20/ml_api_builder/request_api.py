import json
import requests

def make_request(data, ml_config):
    
    url = ml_config.make_request_url
    # data = {"Id":{"0":1,"1":2,"2":3,"3":4,"4":5},"SepalLengthCm":{"0":5.1,"1":4.9,"2":4.7,"3":4.6,"4":5.0},"SepalWidthCm":{"0":3.5,"1":3.0,"2":3.2,"3":3.1,"4":3.6},"PetalLengthCm":{"0":1.4,"1":1.4,"2":1.3,"3":1.5,"4":1.4},"PetalWidthCm":{"0":0.2,"1":0.2,"2":0.2,"3":0.2,"4":0.2},"Species":{"0":"Iris-setosa","1":"Iris-setosa","2":"Iris-setosa","3":"Iris-setosa","4":"Iris-setosa"}}

    r = requests.post(url = url, json = data)

    # extracting data in json format
    print(f'r is: {r}')
    print(f'r is: {type(r)}')


    if 'Endpoint request timed out' in r:
        return {
        'statusCode': 500,
        'error': 'Endpoint request timed out'
        }   
    else:
        print('ok status')


    data = r.content

    print(f'predictions are: {data}')


    return {
        'statusCode': 200,
        'predictions': data
    }


if __name__ == 'main':
    pass