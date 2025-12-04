from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import List
from models import Event, EventCreate, EventUpdate
import database
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
