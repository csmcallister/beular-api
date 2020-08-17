import json
import boto3
import os


def main(event, context):
    """Parse the POST request, invoke the Sagemaker endpoint, parse the 
    returned prediction, and send it back to user.

    Arguments:
        event {dict} -- API Gateway Event
        context {dict} -- Lambda context

    Returns:
        dict -- response
    """
    
    client = boto3.client('sagemaker-runtime')
    endpoint_name = os.environ.get('ENDPOINT_NAME')
    
    data = json.loads(json.dumps(event))
    body = data['body']
    print(body)

    try:
        _ = json.loads(body)
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            Body=body,
            ContentType='application/json'
        )
        # e.g. b'[{"prob": [1.0000100135803223], "label": ["__label__0"]}]'
        results = json.loads(response['Body'].read())
        print(results)
        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }

    
    except json.decoder.JSONDecodeError:
        # sklearn model 
        content_type = os.environ.get('CONTENT_TYPE')
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            Body=body,
            ContentType=content_type
        )
    
        results = json.loads(response['Body'].read())

        predictions = results['instances']
    
        return {
            'statusCode': 200,
            'body': json.dumps(predictions)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(dict(error=e))
        }
