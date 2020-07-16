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
    content_type = os.environ.get('CONTENT_TYPE')

    data = json.loads(json.dumps(event))
    body = data['body'].read()
   
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        Body=body,
        ContentType=content_type)
    
    results = json.loads(response['Body'].read())

    predictions = results['predictions']
    
    return {
        'statusCode': 200,
        'body': json.dumps(predictions)
    }
