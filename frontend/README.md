# Event Management Frontend

A React TypeScript application built with Vite and AWS Cloudscape Design System for managing events, users, and registrations.

## Features

- **Event Management**: Create, view, edit, and delete events with capacity tracking
- **User Management**: Create and manage users
- **Registration System**: Handle event registrations with waitlist support
- **Cloudscape Design**: Professional AWS-style UI components
- **Real-time Updates**: Refresh data and filter by status
- **Responsive Layout**: Side navigation with multiple views

## Prerequisites

- Node.js 18+ and npm
- Backend API running at: `https://myto1dwcaa.execute-api.us-west-2.amazonaws.com/prod`

## Setup Instructions

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

3. **Open in browser**:
   Navigate to `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint for code quality

## Project Structure

```
frontend/
├── src/
│   ├── App.tsx          # Main application component
│   ├── main.tsx         # Application entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── package.json         # Dependencies and scripts
└── vite.config.ts       # Vite configuration
```

## Technology Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Cloudscape Design System** - AWS UI components
- **Fetch API** - HTTP requests to backend

## Features Overview

### Events View
- View all events in a table format
- Filter events by status (active, completed, cancelled)
- Create new events with full details
- Edit and delete existing events
- Track registrations vs capacity
- Enable/disable waitlist per event

### Users View
- View all registered users
- Create new users
- Delete users (automatically unregisters from events)
- View user creation timestamps

### Registrations View
- View all event registrations
- See registration status (registered or waitlisted)
- View waitlist positions
- Unregister users from events
- Automatic waitlist promotion

## API Integration

The frontend connects to the backend API with the following endpoints:

- `GET /events` - List all events
- `POST /events` - Create event
- `PUT /events/{id}` - Update event
- `DELETE /events/{id}` - Delete event
- `GET /users` - List all users
- `POST /users` - Create user
- `DELETE /users/{id}` - Delete user
- `POST /events/{id}/registrations` - Register for event
- `DELETE /events/{id}/registrations/{userId}` - Unregister
- `GET /events/{id}/registrations` - Get event registrations

## Configuration

To change the API endpoint, update the `API_BASE_URL` constant in `src/App.tsx`:

```typescript
const API_BASE_URL = 'https://your-api-endpoint.com/prod';
```

## Building for Production

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Output**: Production files will be in the `dist/` directory

3. **Deploy**: Upload the `dist/` folder to your hosting service (S3, CloudFront, etc.)

## Development Tips

- The app uses Cloudscape Design System components for consistent AWS-style UI
- All state management is handled with React hooks
- API calls use native Fetch API with async/await
- TypeScript interfaces ensure type safety for all data models

## Troubleshooting

**Port already in use**:
```bash
# Vite will automatically try the next available port
# Or specify a different port in vite.config.ts
```

**API connection errors**:
- Verify the backend API is running
- Check CORS configuration on the backend
- Ensure the API_BASE_URL is correct

**Build errors**:
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## License

MIT
