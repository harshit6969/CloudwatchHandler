# CloudwatchHandler
 Get and put logs from AWS Cloudwatch

```bash
"""
    Event Parameters accepted
    ----------
        
    startTime: timestamp, optional
        Default: Current timestamp
        Example: 1580130578059

    endTime: timestamp, optional
        Default: Timestamp 8 weeks ago
        Example: 1580130578059
        
    filterPattern: object, optional
        Custom keys to add to filter_pattern

    Raises
    ------
    ClientError: 
        From AWS.
    KeyError: 
        LogGroup is not found.
"""
```

# Function Details

**Invoke API using this payload**

```json
{
    "LogGroup": "",
    "startTime": "",
    "endTime": "",
    "filterPattern": {}
}
```

## Package and deployment
Create an archive of the lambda function:

```bash
zip function.zip lambda_function.py
```

This will create a `function.zip` file in the root directory. Push the function to AWS.

```bash
aws lambda update-function-code --function-name home --zip-file fileb://function.zip
```

## Sample request payload
```json
{
    "LogGroup": "Authorizer",
	"startTime": 1580130578059,
	"endTime": 1580130578059,
	"filterPattern": {
    // Keys to filter the logs
	}
}
```


## Sample response
```json
[
    {
    "logStreamName": "2020/01/23/[$LATEST]",
    "timestamp": 1579811386853,
    "message": "{\"Timestamp\": \"2020-01-23 20:29:46\", \"TimestampUTC\": \"2020-01-23 20:29:46\", \"LEVEL\": \"INFO\", \"Message\": \"Hello From LSQ.\"}\n",
    "ingestionTime": 1579811396827,
    "eventId": "31199xxxxxxxx603245366"
  }
]
```