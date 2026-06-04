import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tasks')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        task_name = body['taskName'].strip()

        existing = table.scan(
            FilterExpression='taskName = :name',
            ExpressionAttributeValues={':name': task_name}
        )

        if existing['Items']:
            return {
                'statusCode': 409,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({
                    'message': 'משימה עם שם זה כבר קיימת!'
                }, ensure_ascii=False)
            }

        task = {
            'taskId': str(uuid.uuid4()),
            'taskName': task_name,
            'status': 'pending',
            'createdAt': datetime.now().isoformat()
        }

        table.put_item(Item=task)

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'המשימה נוצרה בהצלחה!',
                'task': task
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'שגיאה ביצירת המשימה',
                'error': str(e)
            })
        }