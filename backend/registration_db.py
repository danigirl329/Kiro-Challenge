import boto3
from botocore.exceptions import ClientError
import os
from typing import List, Optional, Dict
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
users_table_name = os.getenv('USERS_TABLE_NAME', 'Users')
registrations_table_name = os.getenv('REGISTRATIONS_TABLE_NAME', 'Registrations')
events_table_name = os.getenv('DYNAMODB_TABLE_NAME', 'Events')

users_table = dynamodb.Table(users_table_name)
registrations_table = dynamodb.Table(registrations_table_name)
events_table = dynamodb.Table(events_table_name)


# User operations
def create_user(user_data: dict) -> dict:
    if 'userId' not in user_data or not user_data['userId']:
        user_data['userId'] = str(uuid.uuid4())
    
    now = datetime.utcnow().isoformat()
    user_data['createdAt'] = now
    user_data['updatedAt'] = now
    
    try:
        users_table.put_item(
            Item=user_data,
            ConditionExpression='attribute_not_exists(userId)'
        )
        return user_data
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise ValueError(f"User with userId {user_data['userId']} already exists")
        raise


def get_user(user_id: str) -> Optional[dict]:
    try:
        response = users_table.get_item(Key={'userId': user_id})
        return response.get('Item')
    except ClientError:
        return None


def get_all_users() -> List[dict]:
    try:
        response = users_table.scan()
        return response.get('Items', [])
    except ClientError:
        return []


def update_user(user_id: str, update_data: dict) -> Optional[dict]:
    update_data['updatedAt'] = datetime.utcnow().isoformat()
    
    update_expr = "SET " + ", ".join([f"#{k} = :{k}" for k in update_data.keys()])
    expr_attr_names = {f"#{k}": k for k in update_data.keys()}
    expr_attr_values = {f":{k}": v for k, v in update_data.items()}
    
    try:
        response = users_table.update_item(
            Key={'userId': user_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            ReturnValues="ALL_NEW"
        )
        return response.get('Attributes')
    except ClientError:
        return None


def delete_user(user_id: str) -> bool:
    try:
        # Delete all user registrations first
        registrations = get_user_registrations(user_id)
        for reg in registrations:
            unregister_user(reg['eventId'], user_id)
        
        users_table.delete_item(Key={'userId': user_id})
        return True
    except ClientError:
        return False


# Registration operations
def register_user(event_id: str, user_id: str) -> dict:
    # Get event details
    event_response = events_table.get_item(Key={'eventId': event_id})
    event = event_response.get('Item')
    
    if not event:
        raise ValueError("Event not found")
    
    # Check if user exists
    user = get_user(user_id)
    if not user:
        raise ValueError("User not found")
    
    # Check if already registered
    existing = get_registration(event_id, user_id)
    if existing:
        raise ValueError(f"User already {existing['status']} for this event")
    
    # Check capacity
    current_registrations = event.get('currentRegistrations', 0)
    capacity = event.get('capacity', 0)
    has_waitlist = event.get('waitlistEnabled', False)
    
    registration_id = f"{user_id}#{event_id}"
    now = datetime.utcnow().isoformat()
    
    if current_registrations < capacity:
        # Register user
        registration = {
            'registrationId': registration_id,
            'eventId': event_id,
            'userId': user_id,
            'status': 'registered',
            'registeredAt': now,
            'position': None
        }
        
        registrations_table.put_item(Item=registration)
        
        # Update event registration count
        events_table.update_item(
            Key={'eventId': event_id},
            UpdateExpression='SET currentRegistrations = currentRegistrations + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
        
        return {**registration, 'message': 'Successfully registered for event'}
    
    elif has_waitlist:
        # Add to waitlist
        current_waitlist = event.get('currentWaitlist', 0)
        position = current_waitlist + 1
        
        registration = {
            'registrationId': registration_id,
            'eventId': event_id,
            'userId': user_id,
            'status': 'waitlisted',
            'registeredAt': now,
            'position': position
        }
        
        registrations_table.put_item(Item=registration)
        
        # Update event waitlist count
        events_table.update_item(
            Key={'eventId': event_id},
            UpdateExpression='SET currentWaitlist = currentWaitlist + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
        
        return {**registration, 'message': f'Event is full. Added to waitlist at position {position}'}
    
    else:
        raise ValueError("Event is at capacity and has no waitlist")


def unregister_user(event_id: str, user_id: str) -> bool:
    registration = get_registration(event_id, user_id)
    
    if not registration:
        raise ValueError("User is not registered for this event")
    
    # Delete registration
    registrations_table.delete_item(
        Key={'eventId': event_id, 'userId': user_id}
    )
    
    if registration['status'] == 'registered':
        # Decrement registration count
        events_table.update_item(
            Key={'eventId': event_id},
            UpdateExpression='SET currentRegistrations = currentRegistrations - :dec',
            ExpressionAttributeValues={':dec': 1}
        )
        
        # Promote first waitlisted user
        promote_from_waitlist(event_id)
    
    elif registration['status'] == 'waitlisted':
        # Decrement waitlist count and update positions
        events_table.update_item(
            Key={'eventId': event_id},
            UpdateExpression='SET currentWaitlist = currentWaitlist - :dec',
            ExpressionAttributeValues={':dec': 1}
        )
        
        # Update positions for remaining waitlisted users
        update_waitlist_positions(event_id, registration.get('position', 0))
    
    return True


def promote_from_waitlist(event_id: str):
    # Get first waitlisted user
    response = registrations_table.query(
        KeyConditionExpression='eventId = :eid',
        FilterExpression='#status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':eid': event_id, ':status': 'waitlisted'}
    )
    
    waitlisted = response.get('Items', [])
    if not waitlisted:
        return
    
    # Sort by position
    waitlisted.sort(key=lambda x: x.get('position', 999))
    first_user = waitlisted[0]
    
    # Update to registered
    registrations_table.update_item(
        Key={'eventId': event_id, 'userId': first_user['userId']},
        UpdateExpression='SET #status = :status, #position = :pos',
        ExpressionAttributeNames={'#status': 'status', '#position': 'position'},
        ExpressionAttributeValues={':status': 'registered', ':pos': None}
    )
    
    # Update counts
    events_table.update_item(
        Key={'eventId': event_id},
        UpdateExpression='SET currentRegistrations = currentRegistrations + :inc, currentWaitlist = currentWaitlist - :dec',
        ExpressionAttributeValues={':inc': 1, ':dec': 1}
    )
    
    # Update remaining waitlist positions
    update_waitlist_positions(event_id, first_user.get('position', 1))


def update_waitlist_positions(event_id: str, removed_position: int):
    response = registrations_table.query(
        KeyConditionExpression='eventId = :eid',
        FilterExpression='#status = :status AND #position > :pos',
        ExpressionAttributeNames={'#status': 'status', '#position': 'position'},
        ExpressionAttributeValues={':eid': event_id, ':status': 'waitlisted', ':pos': removed_position}
    )
    
    for item in response.get('Items', []):
        registrations_table.update_item(
            Key={'eventId': event_id, 'userId': item['userId']},
            UpdateExpression='SET #position = #position - :dec',
            ExpressionAttributeNames={'#position': 'position'},
            ExpressionAttributeValues={':dec': 1}
        )


def get_registration(event_id: str, user_id: str) -> Optional[dict]:
    try:
        response = registrations_table.get_item(
            Key={'eventId': event_id, 'userId': user_id}
        )
        return response.get('Item')
    except ClientError:
        return None


def get_user_registrations(user_id: str) -> List[dict]:
    try:
        response = registrations_table.query(
            IndexName='userId-index',
            KeyConditionExpression='userId = :uid',
            ExpressionAttributeValues={':uid': user_id}
        )
        return response.get('Items', [])
    except ClientError:
        return []


def get_event_registrations(event_id: str) -> Dict[str, List[dict]]:
    try:
        response = registrations_table.query(
            KeyConditionExpression='eventId = :eid',
            ExpressionAttributeValues={':eid': event_id}
        )
        
        items = response.get('Items', [])
        registered = [item for item in items if item['status'] == 'registered']
        waitlisted = [item for item in items if item['status'] == 'waitlisted']
        
        # Sort waitlist by position
        waitlisted.sort(key=lambda x: x.get('position', 999))
        
        return {
            'registered': registered,
            'waitlisted': waitlisted
        }
    except ClientError:
        return {'registered': [], 'waitlisted': []}
