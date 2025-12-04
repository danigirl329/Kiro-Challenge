# Kiro Challenge Project

A FastAPI backend application with AWS CDK infrastructure.

## Structure

- `backend/` - FastAPI Python application
- `infrastructure/` - AWS CDK Infrastructure as Code

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Infrastructure
```bash
cd infrastructure
npm install
cdk deploy
```
