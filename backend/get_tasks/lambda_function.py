import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tasks')

def lambda_handler(event, context):
    try:
        response = table.scan()
        tasks = response['Items']
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'tasks': tasks
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'שגיאה בטעינת המשימות',
                'error': str(e)
            })
        }