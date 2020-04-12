import json, re, time, logging
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError

logs = boto3.client('logs')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Helper function to generate response of AWS Lambda function
def make_response(status_code, body):
    return {
        "statusCode": status_code, 
        "body": json.dumps(body), 
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin": "*"
            }
        }

def get_cloudwatch_api_options(input_params):
    body = {}
    log_group = '/aws/lambda/' + input_params['LogGroup']
    start_time = input_params["startTime"] if "startTime" in input_params else int(time.mktime((datetime.now() - timedelta(days=2)).timetuple()))
    end_time = input_params["endTime"] if "endTime" in input_params else int(time.time()) * 1000
    filter_pattern_array = []
    filter_pattern = None
    if "filterPattern" in input_params:
        for key, value in input_params['filterPattern'].items():
            filter_pattern_array.append("$." + key + " = " + value)
        filter_pattern = "{ " + " && ".join(filter_pattern_array) + " }"
    body = {
        "logGroupName": log_group,
        "startTime": start_time,
        "endTime":end_time
    }
    if filter_pattern:
        body["filterPattern"] = filter_pattern
    return body

# (/GetCloudwatchLogs) to retrieve logs
def lambda_handler(event, context):
    # status_code: Response code of the API
    # response: Response of the API
    status_code = 200
    response = {}
    try:
        logger.info(event)
        # Fetch logs from cloudwatch using boto3
        api_response = logs.filter_log_events(**get_cloudwatch_api_options(json.loads(event["body"])))
        status_code = api_response["ResponseMetadata"]["HTTPStatusCode"]
        response = api_response["events"]
        logger.debug("Logs fetched successfully")
    except KeyError as key:
        status_code = 400
        response = {
          "Status": "Error",
          "ExceptionMessage": "{0} is required.".format(key),
        }
        logger.error(response)
    except Exception as error:
        status_code = 500
        response = {
          "Status": "Error",
          "ExceptionMessage": str(error),
        }
        logger.fatal(response)
    finally:
        # Format and return response
        return make_response(status_code, response)
