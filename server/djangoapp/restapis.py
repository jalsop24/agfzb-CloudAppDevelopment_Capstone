import requests
import json
import os
# import related models here
from djangoapp.models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import dotenv

dotenv.load_dotenv()

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, params=None, api_key=None):
    print(params)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params, auth=HTTPBasicAuth("apikey", api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
        return {}
    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = {}
    if response.ok:
        json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, params, payload):

    response = requests.post(url, headers={'Content-Type': 'application/json'}, 
        params=params, 
        json=payload)
    
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        results = [CarDealer(
                    address = dealer_doc["address"], 
                    city = dealer_doc["city"], 
                    full_name = dealer_doc["full_name"],
                    id = dealer_doc["id"], 
                    lat = dealer_doc["lat"], 
                    long = dealer_doc["long"],
                    short_name = dealer_doc["short_name"],
                    st = dealer_doc["st"],  
                    zip = dealer_doc["zip"]
                ) for dealer_doc in dealers]
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    params = {
        "dealerId": dealerId
    }
    json_result = get_request(url, params=params)
    if json_result:
        results = [DealerReview(
                    id=review["_id"],
                    name=review["name"],
                    text=review["review"],
                    dealer_id=review["dealership"],
                    car_make=review["car_make"],
                    car_model=review["car_model"],
                    car_year=review["car_year"],
                    did_purchase=review["purchase"],
                    purchase_date=review["purchase_date"],
                    sentiment=analyse_review_sentiments(review["review"])
                ) for review in json_result]
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyse_review_sentiments(text: str):
    API_PATH = "/v1/analyze"

    try:
        url = os.environ["NLU_URL"]
        api_key = os.environ["NLU_API_KEY"]
    except KeyError as err:
        print(err)
        return None
    
    params = {
        "text": text,
        "version": "2021-08-01",
        "features": {
            "sentiment"
        },
        "return_analyzed_text": False
    }

    result = get_request(url + API_PATH, api_key=api_key, params=params)

    print(result)

    sentiment = result["sentiment"]["document"]["label"] if result.get("sentiment", None) else "neutral"

    return sentiment
