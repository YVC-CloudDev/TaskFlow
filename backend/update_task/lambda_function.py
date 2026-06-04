import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tasks')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        task_id = event['pathParameters']['taskId']
        new_status = body.get('status')
        new_name = body.get('taskName', '').strip()

        if new_name:
            existing = table.scan(
                FilterExpression='taskName = :name',
                ExpressionAttributeValues={':name': new_name}
            )
            duplicates = [t for t in existing['Items'] if t['taskId'] != task_id]

            if duplicates:
                return {
                    'statusCode': 409,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({
                        'message': 'משימה עם שם זה כבר קיימת!'
                    }, ensure_ascii=False)
                }

            table.update_item(
                Key={'taskId': task_id},
                UpdateExpression='SET taskName = :name, #s = :status',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={
                    ':name': new_name,
                    ':status': new_status or 'pending'
                }
            )
        else:
            table.update_item(
                Key={'taskId': task_id},
                UpdateExpression='SET #s = :status',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':status': new_status}
            )

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'המשימה עודכנה בהצלחה!'
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'שגיאה בעדכון המשימה',
                'error': str(e)
            })
        }