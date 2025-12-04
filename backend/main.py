from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import List
from models import (
    Event, EventCreate, EventUpdate,
    User, UserCreate, UserUpdate,
    RegistrationRequest, RegistrationResponse,
    UserRegistrations, EventRegistrations
)
import database
import registration_db
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Events API",
    version="1.0.0",
    description="REST API for managing events with DynamoDB"
)

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


@app.get("/")
def read_root():
    return {"message": "Events API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/events", response_model=Event, status_code=201)
def create_event(event: EventCreate):
    try:
        event_data = event.model_dump()
        created_event = database.create_event(event_data)
        logger.info(f"Created event: {created_event['eventId']}")
        return created_event
    except Exception as e:
        logger.error(f"Error creating event: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create event")


@app.get("/events", response_model=List[Event])
def get_all_events(status: str = None):
    try:
        events = database.get_all_events()
        
        # Filter by status if provided
        if status:
            events = [e for e in events if e.get('status') == status]
        
        logger.info(f"Retrieved {len(events)} events" + (f" with status={status}" if status else ""))
        return events
    except Exception as e:
        logger.error(f"Error retrieving events: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve events")


@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: str):
    try:
        if not event_id or not event_id.strip():
            raise HTTPException(status_code=400, detail="Event ID is required")
        
        event = database.get_event(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        logger.info(f"Retrieved event: {event_id}")
        return event
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving event {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve event")


@app.put("/events/{event_id}", response_model=Event)
def update_event(event_id: str, event_update: EventUpdate):
    try:
        if not event_id or not event_id.strip():
            raise HTTPException(status_code=400, detail="Event ID is required")
        
        update_data = {k: v for k, v in event_update.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        updated_event = database.update_event(event_id, update_data)
        if not updated_event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        logger.info(f"Updated event: {event_id}")
        return updated_event
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating event {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update event")


@app.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: str):
    try:
        if not event_id or not event_id.strip():
            raise HTTPException(status_code=400, detail="Event ID is required")
        
        success = database.delete_event(event_id)
        if not success:
            raise HTTPException(status_code=404, detail="Event not found")
        
        logger.info(f"Deleted event: {event_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting event {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete event")


# User Management Endpoints
@app.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate):
    try:
        user_data = user.model_dump()
        created_user = registration_db.create_user(user_data)
        logger.info(f"Created user: {created_user['userId']}")
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create user")


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    try:
        user = registration_db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user")


@app.get("/users", response_model=List[User])
def get_all_users():
    try:
        users = registration_db.get_all_users()
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user_update: UserUpdate):
    try:
        update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        updated_user = registration_db.update_user(user_id, update_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update user")


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: str):
    try:
        success = registration_db.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        
        logger.info(f"Deleted user: {user_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete user")


# Registration Endpoints
@app.post("/events/{event_id}/registrations", response_model=RegistrationResponse, status_code=201)
def register_for_event(event_id: str, request: RegistrationRequest):
    try:
        registration = registration_db.register_user(event_id, request.userId)
        logger.info(f"User {request.userId} registered for event {event_id}: {registration['status']}")
        return registration
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        elif "already" in error_msg.lower():
            raise HTTPException(status_code=409, detail=error_msg)
        elif "capacity" in error_msg.lower():
            raise HTTPException(status_code=409, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        logger.error(f"Error registering user for event: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to register for event")


@app.delete("/events/{event_id}/registrations/{user_id}", status_code=204)
def unregister_from_event(event_id: str, user_id: str):
    try:
        registration_db.unregister_user(event_id, user_id)
        logger.info(f"User {user_id} unregistered from event {event_id}")
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error unregistering user from event: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to unregister from event")


@app.get("/users/{user_id}/registrations", response_model=UserRegistrations)
def get_user_registrations(user_id: str):
    try:
        user = registration_db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        registrations = registration_db.get_user_registrations(user_id)
        
        # Enrich with event details
        enriched = []
        for reg in registrations:
            event = database.get_event(reg['eventId'])
            if event:
                enriched.append({
                    **reg,
                    'event': event
                })
        
        return {
            'userId': user_id,
            'registrations': enriched
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user registrations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve registrations")


@app.get("/events/{event_id}/registrations", response_model=EventRegistrations)
def get_event_registrations(event_id: str):
    try:
        event = database.get_event(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        registrations = registration_db.get_event_registrations(event_id)
        
        # Enrich with user details
        registered_enriched = []
        for reg in registrations['registered']:
            user = registration_db.get_user(reg['userId'])
            if user:
                registered_enriched.append({
                    **reg,
                    'user': user
                })
        
        waitlisted_enriched = []
        for reg in registrations['waitlisted']:
            user = registration_db.get_user(reg['userId'])
            if user:
                waitlisted_enriched.append({
                    **reg,
                    'user': user
                })
        
        return {
            'eventId': event_id,
            'registered': registered_enriched,
            'waitlisted': waitlisted_enriched,
            'counts': {
                'registered': len(registered_enriched),
                'waitlisted': len(waitlisted_enriched),
                'capacity': event.get('capacity', 0)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving event registrations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve event registrations")
