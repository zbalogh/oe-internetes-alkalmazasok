# Spring Boot REST Lab (MVC + REST alapok)

## Előfeltételek
- JDK 17 vagy 21
- Maven 3.9+
- IDE: IntelliJ IDEA / Eclipse / VS Code
- VS Code-ban ajánlott telepíteni az "Extension Pack for Java" extension-t

## Compile & Build
```bash
mvnw clean package
```

## Futtatás
```bash
mvnw spring-boot:run
```

## Swagger UI
- http://localhost:8080/swagger-ui.html

## API végpontok
- GET    http://localhost:8080/api/v1/users
- GET    http://localhost:8080/api/v1/users/{id}
- POST   http://localhost:8080/api/v1/users
- PUT    http://localhost:8080/api/v1/users/{id}
- DELETE http://localhost:8080/api/v1/users/{id}

---

# 🚀 JWT Authentication Quick Reference

## 🔄 Authentication Flow

```
┌─────────┐                                  ┌─────────────────┐
│ Client  │                                  │  Spring Boot    │
│         │                                  │  Application    │
└────┬────┘                                  └────────┬────────┘
     │                                                 │
     │  1. POST /api/v1/auth/login                   │
     │     {username, password}                       │
     ├────────────────────────────────────────────────>
     │                                                 │
     │                    2. Validate credentials     │
     │                       (AuthenticationManager)  │
     │                                                 │
     │  3. Return JWT Token                           │
     │     {token, type, expiresIn}                   │
     <─────────────────────────────────────────────────
     │                                                 │
     │  4. GET /api/v1/users                          │
     │     Authorization: Bearer {token}              │
     ├────────────────────────────────────────────────>
     │                                                 │
     │              5. JwtAuthenticationFilter        │
     │                 - Extract token from header    │
     │                 - Validate token signature     │
     │                 - Set authentication context   │
     │                                                 │
     │  6. Return protected resource                  │
     │     [user list]                                │
     <─────────────────────────────────────────────────
     │                                                 │
```

## Demo Credentials
```
Username: demo
Password: 12345
```

## Authentication Endpoint
```bash
POST http://localhost:8080/api/v1/auth/login
Content-Type: application/json

{
  "username": "demo",
  "password": "12345"
}
```

## Response Format
```json
{
  "token": "eyJhbGc...",
  "type": "Bearer",
  "expiresIn": 86400000
}
```

## Using the Token
Add this header to all protected endpoint requests:
```
Authorization: Bearer YOUR_TOKEN
```

## CURL Examples

### Login:
```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"demo\",\"password\":\"12345\"}"
```

### Get Users (with token):
```bash
curl http://localhost:8080/api/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Protected Endpoints
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{id}` - Get user by ID
- `POST /api/v1/users` - Create user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Public Endpoints
- `POST /api/v1/auth/login` - Login
- `http://localhost:8080/swagger-ui.html` - Swagger UI

## Token Details
- **Expires:** 24 hours (86400000 ms)
- **Algorithm:** HMAC-SHA256
- **Type:** Bearer

## Troubleshooting

### 403 Forbidden?
✓ Check if token is included in Authorization header
✓ Verify token format: `Bearer {token}` (note the space)
✓ Check if token is expired (24h limit)

### 401 Unauthorized?
✓ Wrong username or password
✓ Check credentials: username=`demo`, password=`12345`

### Connection Refused?
✓ Make sure application is running on port 8080
