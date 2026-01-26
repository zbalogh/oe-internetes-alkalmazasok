# JWT Security Testing Guide

### Demo User Credentials:
- **Username:** demo
- **Password:** 12345

---

## How to Test

### Step 1: Start the Application

```bash
# Using Maven wrapper
.\mvnw.cmd spring-boot:run
```

Wait for the application to start (you should see "Started RestLabApplication" in the logs).

---

### Step 2: Test Protected Endpoints (Should Fail)

Try to access the users endpoint without authentication:

```bash
curl http://localhost:8080/api/v1/users
```

**Expected Result:** HTTP 403 Forbidden (endpoint is protected)

---

### Step 3: Login to Get JWT Token

Send a POST request to the authentication endpoint:

```bash
curl -X POST http://localhost:8080/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"demo\",\"password\":\"12345\"}"
```

**Expected Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkZW1vIiwiaWF0IjoxNzM3ODk1MDAwLCJleHAiOjE3Mzc5ODE0MDB9.xxxxx",
  "type": "Bearer",
  "expiresIn": 86400000
}
```

**Copy the token value** from the response.

---

### Step 4: Access Protected Endpoints with JWT Token

Use the JWT token in the Authorization header:

```bash
curl http://localhost:8080/api/v1/users ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response:** List of users (HTTP 200 OK)
```json
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  {
    "id": 2,
    "name": "Bob",
    "email": "bob@example.com"
  }
]
```

---

### Step 5: Test Other CRUD Operations

#### Get Single User:
```bash
curl http://localhost:8080/api/v1/users/1 ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Create New User:
```bash
curl -X POST http://localhost:8080/api/v1/users ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE" ^
  -d "{\"name\":\"Charlie\",\"email\":\"charlie@example.com\"}"
```

#### Update User:
```bash
curl -X PUT http://localhost:8080/api/v1/users/1 ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE" ^
  -d "{\"name\":\"Alice Updated\",\"email\":\"alice.updated@example.com\"}"
```

#### Delete User:
```bash
curl -X DELETE http://localhost:8080/api/v1/users/1 ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

### Step 6: Test Invalid Credentials

Try to login with wrong credentials:

```bash
curl -X POST http://localhost:8080/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"demo\",\"password\":\"wrongpassword\"}"
```

**Expected Response:** HTTP 401 Unauthorized
```json
{
  "error": "Authentication failed",
  "message": "Invalid username or password"
}
```

---

### Step 7: Test Invalid/Expired Token

Try to access protected endpoint with invalid token:

```bash
curl http://localhost:8080/api/v1/users ^
  -H "Authorization: Bearer invalid_token_here"
```

**Expected Result:** HTTP 403 Forbidden

---

## Swagger UI Access

The Swagger UI is accessible **without authentication** at:

```
http://localhost:8080/swagger-ui.html
```

You can test the API endpoints using Swagger UI:
1. First, use the `/api/v1/auth/login` endpoint to get a token
2. Click the "Authorize" button at the top
3. Enter: `YOUR_TOKEN_HERE`
4. Now you can test all protected endpoints

---

## Security Configuration Details

### Public Endpoints (No Authentication Required):
- `/api/v1/auth/**` - Authentication endpoints
- `/swagger-ui/**` - Swagger UI
- `/v3/api-docs/**` - OpenAPI documentation

### Protected Endpoints (JWT Required):
- `/api/v1/users/**` - All user CRUD operations
- Any other endpoints not explicitly made public

### Session Management:
- **Stateless** - No server-side sessions
- **JWT token** is the only authentication mechanism
- Token expires after 24 hours (86400000 ms)

---

## Architecture

```
Client Request
    ↓
JwtAuthenticationFilter (Extract & Validate JWT)
    ↓
SecurityContext (Set Authentication)
    ↓
Controller (Access Granted/Denied)
```

1. **Client** sends request with `Authorization: Bearer <token>` header
2. **JwtAuthenticationFilter** intercepts the request
3. Filter extracts token from header and validates it using **JwtUtil**
4. If valid, authentication is set in **SecurityContext**
5. **Controller** receives the request (Spring Security allows access)
6. If token is invalid/missing, Spring Security returns 403 Forbidden

---

## Token Structure

The JWT token contains:
- **Subject (sub):** username ("demo")
- **Issued At (iat):** timestamp when token was created
- **Expiration (exp):** timestamp when token expires
- **Signature:** HMAC-SHA256 signature using the secret key

