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
from ibmcloudant.cloudant_v1 import CloudantV1, Document

def main(dict):
    
    try:
        review = dict["review"]
    except KeyError:
        return {
            "error": {
                "statusCode": 500,
                "message": "No review supplied"
            }
        }
    
    try:
        new_doc = Document()
        # new_doc.id = review["id"]
        new_doc.name = review["name"]
        new_doc.dealership = review["dealership"]
        new_doc.review = review["review"]
        new_doc.purchase = review["purchase"]
        new_doc.another = review["another"]
        new_doc.purchase_date = review["purchase_date"]
        new_doc.car_make = review["car_make"]
        new_doc.car_model = review["car_model"]
        new_doc.car_year = review["car_year"]
    except Exception as err:
        return {
            "error": {
                "statusCode": 500,
                "message": f"Could not create document: {str(err)}"
            }
        }
    
    service = CloudantV1(authenticator = IAMAuthenticator(dict["CLOUDANT_APIKEY"]))
    service.set_service_url(dict["CLOUDANT_URL"])
    
    response = service.post_document(
        db="reviews",
        document=new_doc
    ).get_result()
    
    return { "statusCode": 200, "response": response }
