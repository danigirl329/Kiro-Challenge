import boto3
from botocore.exceptions import ClientError
import os
from typing import List, Optional
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('DYNAMODB_TABLE_NAME', 'Events')
table = dynamodb.Table(table_name)


def create_event(event_data: dict) -> dict:
    if 'eventId' not in event_data or not event_data['eventId']:
        event_data['eventId'] = str(uuid.uuid4())
    
    # Initialize registration fields
    if 'currentRegistrations' not in event_data:
        event_data['currentRegistrations'] = 0
    if 'currentWaitlist' not in event_data:
        event_data['currentWaitlist'] = 0
    if 'waitlistEnabled' not in event_data:
        event_data['waitlistEnabled'] = False
    
    table.put_item(Item=event_data)
    return event_data


def get_event(event_id: str) -> Optional[dict]:
    try:
        response = table.get_item(Key={'eventId': event_id})
        return response.get('Item')
    except ClientError:
        return None


def get_all_events() -> List[dict]:
    try:
        response = table.scan()
        return response.get('Items', [])
    except ClientError:
        return []


def update_event(event_id: str, update_data: dict) -> Optional[dict]:
    update_expr = "SET " + ", ".join([f"#{k} = :{k}" for k in update_data.keys()])
    expr_attr_names = {f"#{k}": k for k in update_data.keys()}
    expr_attr_values = {f":{k}": v for k, v in update_data.items()}
    
    try:
        response = table.update_item(
            Key={'eventId': event_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            ReturnValues="ALL_NEW"
        )
        return response.get('Attributes')
    except ClientError:
        return None


def delete_event(event_id: str) -> bool:
    try:
        table.delete_item(Key={'eventId': event_id})
        return True
    except ClientError:
        return False
