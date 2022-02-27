/**
 *
 * main() will be run when you invoke this action
 *
 * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
 *
 * @return The output of this action, which must be a JSON object.
 *
 */

const Cloudant = require('@cloudant/cloudant');


async function main(params) {
    
    const cloudant = Cloudant({
            url: params.COUCH_URL,
            plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
        });
    
    try {
        
        const db = await cloudant.use("dealerships");
        
        const query = {
            selector: {
                state: params.state
            },
            fields: [ "id", "full_name", "short_name", "address", "zip", "city", "state", "st", "lat", "long"],
        };
        
        let result = await db.find(query);
        
        if (result.docs.length == 0){
            return {
                "error": {
                    "statusCode": 404
                }
            }
        }
        
        return {
            "result": result.docs,
        }
        
    } catch (error) {
        return {
            "error": {
                "statusCode": 500,
                "msg": error.description 
            }
        }
    }
}
