# Events Management API

A serverless REST API for managing events, built with FastAPI and deployed on AWS using Lambda, API Gateway, and DynamoDB.

## 🚀 Live API

**Base URL:** `https://myto1dwcaa.execute-api.us-west-2.amazonaws.com/prod/`

## 📋 Features

- Full CRUD operations for events
- Serverless architecture using AWS Lambda
- DynamoDB for data persistence
- API Gateway with CORS enabled
- Input validation and error handling
- Custom event IDs support
- Status-based filtering

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────────┐
│   Client    │─────▶│ API Gateway  │─────▶│   Lambda    │─────▶│  DynamoDB    │
└─────────────┘      └──────────────┘      └─────────────┘      └──────────────┘
                                                  │
                                                  │ FastAPI
                                                  │ + Mangum
```

## 📁 Project Structure

```
.
├── backend/              # FastAPI application
│   ├── main.py          # API endpoints
│   ├── models.py        # Pydantic models
│   ├── database.py      # DynamoDB operations
│   ├── lambda_handler.py # Lambda entry point
│   └── requirements.txt # Python dependencies
├── infrastructure/       # AWS CDK Infrastructure as Code
│   ├── bin/
│   │   └── app.ts       # CDK app entry point
│   ├── lib/
│   │   └── infrastructure-stack.ts  # Stack definition
│   ├── cdk.json         # CDK configuration
│   └── package.json     # Node dependencies
└── README.md
```

## 🔧 Local Development

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run Locally

```bash
# Set environment variable for local DynamoDB
export DYNAMODB_TABLE_NAME=Events

# Start the API
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Infrastructure Setup

```bash
cd infrastructure
npm install
npm run build
```

## 🚀 Deployment

### Prerequisites

- AWS CLI configured with appropriate credentials
- Docker running (for Lambda bundling)
- Node.js and npm installed
- AWS CDK CLI installed: `npm install -g aws-cdk`

### Deploy to AWS

```bash
cd infrastructure
cdk bootstrap  # First time only
cdk deploy
```

The deployment will output your API URL.

## 📚 API Documentation

### Event Model

```json
{
  "eventId": "string",
  "title": "string (1-200 chars)",
  "description": "string (1-1000 chars)",
  "date": "string (ISO 8601 format)",
  "location": "string (1-200 chars)",
  "capacity": "integer (1-100000)",
  "organizer": "string (1-100 chars)",
  "status": "string (draft|published|cancelled|completed|active)"
}
```

### Endpoints

#### Create Event
```bash
POST /events
Content-Type: application/json

{
  "eventId": "optional-custom-id",  # Optional, auto-generated if not provided
  "title": "Tech Conference 2024",
  "description": "Annual technology conference",
  "date": "2024-12-15",
  "location": "San Francisco, CA",
  "capacity": 500,
  "organizer": "Tech Corp",
  "status": "published"
}

Response: 201 Created
```

#### Get All Events
```bash
GET /events
GET /events?status=active  # Filter by status

Response: 200 OK
[
  {
    "eventId": "...",
    "title": "...",
    ...
  }
]
```

#### Get Event by ID
```bash
GET /events/{event_id}

Response: 200 OK
{
  "eventId": "...",
  "title": "...",
  ...
}
```

#### Update Event
```bash
PUT /events/{event_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "capacity": 600
}

Response: 200 OK
```

#### Delete Event
```bash
DELETE /events/{event_id}

Response: 204 No Content
```

### Example Usage

```bash
# Create an event
curl -X POST https://myto1dwcaa.execute-api.us-west-2.amazonaws.com/prod/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Workshop 2024",
    "description": "Hands-on coding workshop",
    "date": "2024-12-20",
    "location": "Online",
    "capacity": 100,
    "organizer": "Dev Community",
    "status": "published"
  }'

# Get all events
curl https://myto1dwcaa.execute-api.us-west-2.amazonaws.com/prod/events

# Get events by status
curl "https://myto1dwcaa.execute-api.us-west-2.amazonaws.com/prod/events?status=published"

# Update an event
curl -X PUT https://myto1dwcaa.execute-api.us-west-2.amazonaws.com/prod/events/{event_id} \
  -H "Content-Type: application/json" \
  -d '{"capacity": 150}'

# Delete an event
curl -X DELETE https://myto1dwcaa.execute-api.us-west-2.amazonaws.com/prod/events/{event_id}
```

## 🛠️ Technology Stack

- **Backend:** FastAPI, Pydantic, Boto3
- **Infrastructure:** AWS CDK (TypeScript)
- **AWS Services:** Lambda, API Gateway, DynamoDB
- **Runtime:** Python 3.11
- **Adapter:** Mangum (ASGI to Lambda)

## 🔒 Security Features

- Input validation with Pydantic
- CORS configuration
- Error handling and logging
- DynamoDB encryption at rest
- IAM role-based permissions

## 📊 AWS Resources

- **DynamoDB Table:** `Events` (PAY_PER_REQUEST billing)
- **Lambda Function:** Python 3.11, 512MB memory, 30s timeout
- **API Gateway:** REST API with CORS enabled
- **IAM Roles:** Least privilege access for Lambda

## 🧪 Testing

The API has been tested against the following scenarios:
- ✅ Create event with custom ID
- ✅ Get all events
- ✅ Filter events by status
- ✅ Get specific event
- ✅ Update event fields
- ✅ Delete event

## 🗑️ Cleanup

To remove all AWS resources:

```bash
cd infrastructure
cdk destroy
```

## 📝 License

This project is part of the Kiro Challenge.

## 👤 Author

Built with Kiro AI Assistant
