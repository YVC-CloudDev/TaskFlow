import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tasks')

def lambda_handler(event, context):
    try:
        task_id = event['pathParameters']['taskId']
        
        table.delete_item(
            Key={'taskId': task_id}
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'המשימה נמחקה בהצלחה!'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'שגיאה במחיקת המשימה',
                'error': str(e)
            })
        }