# Angular Frontend for User Management System

This is an Angular-based frontend application that provides a user interface for the Spring Boot REST API backend. It demonstrates a complete CRUD (Create, Read, Update, Delete) implementation for managing users.

## Technology Stack

- **Angular**: 17.3.12
- **TypeScript**: 5.4.5
- **RxJS**: 7.8.1
- **Node.js**: 20+
- **npm**: 10+

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── components/          # Application components
│   │   │   ├── home/            # Home page component
│   │   │   ├── users/           # Users list component
│   │   │   └── edit/            # User edit/create component
│   │   ├── models/              # TypeScript interfaces
│   │   │   └── user.model.ts    # User model interface
│   │   ├── services/            # Angular services
│   │   │   └── user.service.ts  # User service with HTTP client
│   │   ├── app-routing.module.ts # Routing configuration
│   │   ├── app.module.ts         # Root module
│   │   └── app.component.*       # Root component with navigation
│   └── proxy-config.json         # Development proxy configuration
├── angular.json                  # Angular CLI configuration
└── package.json                  # NPM dependencies and scripts
```


## Features

### 1. Home Component
- Welcome page with application overview
- Introduction to the user management system
- Feature list and getting started information

### 2. Users Component
- Display all users in a table format
- Add new user button
- Edit user functionality
- Delete user with confirmation
- Success and error message handling
- Loading state indicator

### 3. Edit Component
- Dual-purpose component for creating and editing users
- Form validation for name and email
- Client-side validation with error messages
- Navigation back to users list after save

### 4. User Service
- Complete CRUD operations:
  - `getAllUsers()` - Fetch all users
  - `getUserById(id)` - Fetch a single user
  - `createUser(user)` - Create a new user
  - `updateUser(id, user)` - Update an existing user
  - `deleteUser(id)` - Delete a user
- HTTP error handling with user-friendly messages
- Integration with HttpClient for REST API communication

### 5. Navigation
- Header with application title
- Navigation links (Home, Users)
- Active route highlighting
- Responsive design for mobile devices


## Development Setup

### Prerequisites
- Node.js (v20 or higher)
- Angular CLI (v17)
- Spring Boot backend running on port 8080

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

### Development Server

Run the development server with proxy configuration:
```bash
npm start
```

The application will be available at `http://localhost:4200/`

The proxy configuration will forward all API requests (starting with `/api`) to the Spring Boot backend at `http://localhost:8080`.


### Build for Production

To build the project for production deployment:
```bash
npm run build:prod
```

This will:
- Build the Angular application with production optimizations
- Output the compiled files to `../src/main/resources/static` directory
- The static files will be served by the Spring Boot application


## API Communication

### Proxy Configuration (Development)

The `proxy-config.json` file configures the development server to proxy API requests:

```json
{
  "/api": {
    "target": "http://localhost:8080",
    "secure": false,
    "logLevel": "debug",
    "changeOrigin": true
  }
}
```

This allows the Angular application to make API calls to `/api/v1/users` which will be forwarded to `http://localhost:8080/api/v1/users`.

### Production Deployment

In production, the Angular application is built and placed in the Spring Boot's static resources folder. The Spring Boot application serves both the API and the static frontend files.


## Routing

The application uses Angular Router with the following routes:

- `/` - Redirects to `/home`
- `/home` - Home component
- `/users` - Users list component
- `/users/new` - Create new user (Edit component)
- `/users/edit/:id` - Edit existing user (Edit component)
- `**` - Wildcard route redirects to `/home`


## Components Overview

### HomeComponent
Displays the welcome page with:
- Application title and introduction
- Feature list
- Getting started instructions

### UsersComponent
Main user management interface:
- Fetches and displays all users in a table
- Provides buttons to add, edit, and delete users
- Shows loading state while fetching data
- Displays success/error messages
- Confirms before deleting a user

### EditComponent
Form for creating and editing users:
- Detects mode (create/edit) from route parameters
- Loads existing user data when editing
- Validates form input (name and email)
- Displays validation error messages
- Saves changes via UserService
- Navigates back to users list after successful save


## User Model

```typescript
export interface User {
  id: number;
  name: string;
  email: string;
}

export interface UserRequest {
  name: string;
  email: string;
}
```


## Error Handling

The UserService includes comprehensive error handling:

- **Client-side errors**: Network errors, client-side exceptions
- **HTTP errors**:
  - 400 Bad Request: Invalid data provided
  - 404 Not Found: User does not exist
  - 500 Server Error: Backend error
- All errors are logged to console for debugging
- User-friendly error messages are displayed in the UI


## Styling

The application uses custom CSS with:
- Responsive design for mobile devices
- Consistent color scheme and typography
- Hover effects and transitions
- Clean and modern UI
- Alert messages for success/error feedback


## Running the Complete Application

### Step 1: Start the Spring Boot Backend
```bash
cd ..
mvnw spring-boot:run
```

The backend will start on `http://localhost:8080`

### Step 2: Start the Angular Frontend
```bash
cd frontend
npm start
```

The frontend will start on `http://localhost:4200`

### Step 3: Access the Application
Open your browser and navigate to `http://localhost:4200`


## Production Deployment

### Step 1: Build the Angular Application
```bash
cd frontend
npm run build:prod
```

### Step 2: Start the Spring Boot Application
```bash
cd ..
mvnw spring-boot:run
```

### Step 3: Access the Application
The complete application (frontend + backend) will be available at `http://localhost:8080`


## Educational Notes

This application is designed as an educational example for university students. Key learning points:

1. **Angular Architecture**: Component-based structure, services, routing
2. **HTTP Communication**: Using HttpClient for REST API calls
3. **RxJS Observables**: Handling asynchronous data streams
4. **Form Handling**: Template-driven forms with validation
5. **Error Handling**: Proper error handling and user feedback
6. **Routing**: Navigation between different views
7. **Proxy Configuration**: Development vs production configuration
8. **Integration**: Connecting Angular frontend with Spring Boot backend


## Best Practices Demonstrated

- Separation of concerns (components, services, models)
- Dependency injection
- Reactive programming with RxJS
- Comprehensive commenting for educational purposes
- Error handling at multiple levels
- User feedback (loading states, success/error messages)
- Responsive design
- Clean code structure and organization


## Future Enhancements

Possible improvements for learning purposes:
- Form validation with reactive forms
- Pagination for large user lists
- Search and filter functionality
- User authentication and authorization
- Unit tests for components and services
- E2E tests with Protractor or Cypress
- Angular Material UI components
- Internationalization (i18n)
