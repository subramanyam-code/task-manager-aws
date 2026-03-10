import json
import boto3
import uuid
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

def lambda_handler(event, context):

    print("Lambda started")
    print("Event received:", json.dumps(event))

    # Default user for API Gateway test
    user_id = "test-user"

    # If request comes from Cognito authenticated user
    if "requestContext" in event and "authorizer" in event["requestContext"]:
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

    print("User ID:", user_id)

    try:
        # Read request body
        body = json.loads(event.get("body", "{}"))
        print("Request body:", body)

        title = body.get("title", "No title provided")

        # Generate task id
        task_id = str(uuid.uuid4())

        item = {
            "userId": user_id,
            "taskId": task_id,
            "title": title,
            "status": "Pending",
            "createdAt": str(datetime.now())
        }

        print("Saving item to DynamoDB:", item)

        # Store in DynamoDB
        table.put_item(Item=item)

        print("Task saved successfully")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Task created successfully",
                "taskId": task_id
            })
        }

    except Exception as e:

        print("Error occurred:", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }