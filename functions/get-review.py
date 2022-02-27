#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1

def main(dict):
    
    try:
        dealer_id = dict["dealerId"]
    except KeyError:
        return {
            "error": {
                "statusCode": 500
            }
        }
    
    service = CloudantV1(authenticator = IAMAuthenticator(dict["CLOUDANT_APIKEY"]))
    service.set_service_url(dict["CLOUDANT_URL"])
    
    response = service.post_find(
        db="reviews",
        selector={
                "dealership": {'$eq': int(dealer_id)}
            }
        ).get_result()
    
    if len(response["docs"]) == 0:
        return {
            "error": {
                "statusCode": 404
            }
        }
    
    return { 'result': response["docs"] }
