# Frappy API Billing

API Quota and Billing System for Flask - compatible with the Frappy framework.

- This is the backend module for Flask
- Frontend package for React can be found here: 
  [@frappy/react-api-billing](http://github.com/ilfrich/frappy-react-api-billing)
- Usage store modules for Python can be found here:
    - [MongoDB Store](http://github.com/ilfrich/frappy-py-mongo-api-billing-store)
    - [SQL Store (SQL Alchemy)](http://github.com/ilfrich/frappy-py-sql-api-billing-store)
    
## Usage

```python
from frappyapibilling import ApiBilling, QuotaDuration, QuotaDefinition
from frappymongoapibilling import UsageStore
from datetime import datetime
from flask import Flask, jsonify, make_response

# init the usage store and the api billing handler instance
store = UsageStore(mongo_url="mongodb://localhost:27015", mongo_db="myDbName", collection_name="apiUsage")
api_billing = ApiBilling(usage_store=store)

# define the quotas for any existing client and feed them into the ApiBilling instance
client_id = "client1"
quotas = [
    QuotaDefinition(duration_type=QuotaDuration.DAY, credit_limit=500, start_date=datetime(2022, 1, 1)),
    QuotaDefinition(duration_type=QuotaDuration.MONTH, credit_limit=10000, start_date=datetime(2022, 1, 1)),
]
api_billing.update_client_quotas(client_id=client_id, quota_definitions=quotas)

app = Flask(__name__)

@app.route("/api/fetch-data", methods=["GET"])
def fetch_data_api_handler():
    # run authentication of the user
    authenticated_client = "client1" # replace with your auth mechanism
    api_billing.track_client_usage(client_id=authenticated_client)  # will abort if insufficient credits and deduct 1 credit
    # run your method
    result = ...
    return jsonify(result)


@app.route("/api/fetch-expensive-data", methods=["GET"])
def fetch_expensive_data_api_handler():
    # run authentication of the user
    authenticated_client = "client1" # replace with your auth mechanism
    credits_used = 5.0  # this can also be determined dynamically by the request
    api_billing.track_client_usage(client_id=authenticated_client, credits_used=credits_used)  
    # run your method
    result = ...
    # return a response with X-RateLimit-[Remaining|Reset] headers
    return api_billing.create_response_with_header(client_id=authenticated_client, response_body=jsonify(result))
```

## Quota Definitions

It is up to you, where and how you store quota definitions. The API Billing module does not store the quota definitions 
 anywhere. 

When your API starts up you need to fetch any pre-existing clients and their respective quota limits and 
 create the quota definitions. The module will fetch existing usage and update the current renew interval with already 
 used up credits.

Likewise, while the API is running, if a new client registers, you can feed the quota definitions into the ApiBilling
instance using the `update_client_quotas(client_id, quota_definitions: List[QuotdaDefinition])` method.

## Error Handling

The `track_client_usage` method will first check if sufficient credits are available. If not there are 2 possible 
 behaviours:

- by default a 429 will be returned to the caller with an error message and `RateLimit` headers
- if the parameter `use_abort=False` is passed into the `track_client_usage` a `QuotaException` will be thrown and you
 have to handle the error.

A `QuotaException` has 2 fields storing `quota_remaining` (a number) and `quota_renew` (`datetime`) for the "shortest 
 quota" - i.e. the quota definition with the fewest remaining credits.

You can also pass the `QuotaException` instance into the `create_response_with_header` method of `ApiBilling` as the 
 optional `exception` parameter, which can reduce required computation to determining the next renew and remaining 
 credits. 

Please note, all `datetime` objects are relative to the server's timezone.
