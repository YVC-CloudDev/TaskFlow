import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tasks')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        task_id = event['pathParameters']['taskId']
        new_status = body['status']
        
        table.update_item(
            Key={'taskId': task_id},
            UpdateExpression='SET #s = :status',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':status': new_status}
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'המשימה עודכנה בהצלחה!'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'שגיאה בעדכון המשימה',
                'error': str(e)
            })
        }