# 🎨 Swagger UI with JWT Authentication - Complete Guide

## 📦 OpenApiConfig Java class

**`OpenApiConfig.java`** - Configures Swagger UI with JWT Bearer authentication support

This configuration adds:
- 🔓 **"Authorize" button** in Swagger UI
- 📝 **Automatic JWT token field** for Bearer authentication
- 📖 **Enhanced API documentation** with usage instructions
- 🔒 **Security indicators** showing which endpoints require authentication

---

## 🎯 How to Use Swagger UI with JWT

### Step 1: Start the Application
```bash
.\mvnw.cmd spring-boot:run
```

### Step 2: Open Swagger UI
Navigate to: **http://localhost:8080/swagger-ui.html**

You should see:
- Two sections: **Authentication** and **Users**
- A **🔓 Authorize** button at the top right
- Lock icons (🔒) next to protected endpoints

---

### Step 3: Get JWT Token

1. In Swagger UI, find the **Authentication** section
2. Click on **POST /api/v1/auth/login**
3. Click **"Try it out"**
4. The request body is pre-filled with:
   ```json
   {
     "username": "demo",
     "password": "12345"
   }
   ```
5. Click **"Execute"**
6. In the response body, you'll see:
   ```json
   {
     "token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWI...",
     "type": "Bearer",
     "expiresIn": 86400000
   }
   ```
7. **Copy the entire token value** (the long string starting with `eyJ...`)

---

### Step 4: Authorize in Swagger UI

1. Click the **🔓 Authorize** button at the top of the page
2. A dialog will appear with a field labeled **"Bearer Authentication"**
3. In the **Value** field, enter:
   ```
   YOUR_TOKEN_HERE
   ```
   
   Example:
   ```
   eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkZW1vIiwiaWF0IjoxNzA2MjY...
   ```

4. Click **"Authorize"**
5. Click **"Close"**

✅ **You're now authenticated!** The lock icon should change from 🔓 to 🔒

---

### Step 5: Test Protected Endpoints

Now you can test all protected endpoints in the **Users** section:

#### Get All Users
1. Click on **GET /api/v1/users**
2. Click **"Try it out"**
3. Click **"Execute"**
4. ✅ You should see a list of users (HTTP 200)

#### Get User by ID
1. Click on **GET /api/v1/users/{id}**
2. Click **"Try it out"**
3. Enter ID: `1`
4. Click **"Execute"**
5. ✅ You should see Alice's details

#### Create New User
1. Click on **POST /api/v1/users**
2. Click **"Try it out"**
3. Modify the request body:
   ```json
   {
     "name": "Charlie",
     "email": "charlie@example.com"
   }
   ```
4. Click **"Execute"**
5. ✅ You should see the created user with a new ID

#### Update User
1. Click on **PUT /api/v1/users/{id}**
2. Click **"Try it out"**
3. Enter ID: `1`
4. Modify the request body:
   ```json
   {
     "name": "Alice Updated",
     "email": "alice.updated@example.com"
   }
   ```
5. Click **"Execute"**
6. ✅ You should see the updated user

#### Delete User
1. Click on **DELETE /api/v1/users/{id}**
2. Click **"Try it out"**
3. Enter ID: `2`
4. Click **"Execute"**
5. ✅ You should see HTTP 204 No Content

---

## 🔍 Visual Indicators in Swagger UI

### Before Authentication:
- 🔓 **Open lock** icon at the top
- 🔒 **Closed lock** icons next to protected endpoints

### After Authentication:
- 🔒 **Closed lock** icon at the top
- ✅ All protected endpoints are accessible

### Public Endpoints:
- Only `/api/v1/auth/login` is public

---

## 🎨 What You'll See in Swagger UI

### API Information Section:
```
REST Lab API with JWT Security
Version: 1.0.0

Spring Boot REST API Demo with JWT Authentication

How to use:
1. Call /api/v1/auth/login with credentials
2. Copy the token from the response
3. Click the Authorize button (🔓) at the top
4. Enter: <your_token>
5. Click Authorize and close the dialog
6. Now you can test all protected endpoints!
```

### Endpoints Overview:

#### Authentication (No lock - Public)
- `POST /api/v1/auth/login` - Login to get JWT token

#### Users (🔒 Lock icon - Protected)
- `GET /api/v1/users` - Get all users (requires JWT token)
- `POST /api/v1/users` - Create new user (requires JWT token)
- `GET /api/v1/users/{id}` - Get user by ID (requires JWT token)
- `PUT /api/v1/users/{id}` - Update user (requires JWT token)
- `DELETE /api/v1/users/{id}` - Delete user (requires JWT token)

---

## 📋 Quick Reference

### Demo Credentials
```
Username: demo
Password: 12345
```

### Swagger UI URL
```
http://localhost:8080/swagger-ui.html
```

### OpenAPI JSON
```
http://localhost:8080/v3/api-docs
```

### Authorization Header Format
```
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWI...
```

---

## 🔧 Technical Details

### OpenAPI Configuration (`OpenApiConfig.java`)

```java
@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .addSecurityItem(new SecurityRequirement()
                .addList("Bearer Authentication"))
            .components(new Components()
                .addSecuritySchemes("Bearer Authentication",
                    new SecurityScheme()
                        .type(SecurityScheme.Type.HTTP)
                        .scheme("bearer")
                        .bearerFormat("JWT")));
    }
}
```

### Controller Annotations

**AuthController:**
```java
@Tag(name = "Authentication", 
     description = "Endpoints for user authentication and JWT token generation")
```

**UserController:**
```java
@Tag(name = "Users", 
     description = "User management endpoints (requires JWT authentication)")
@SecurityRequirement(name = "Bearer Authentication")
```
