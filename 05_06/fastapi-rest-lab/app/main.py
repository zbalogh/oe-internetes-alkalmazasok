from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List


# FastAPI application instance
app = FastAPI(
    title="REST API Demo",
    version="1.0.0",
    description="REST API Demo based on FastAPI. The 'View' is JSON, the 'Controller' is the route handler."
)


# Pydantic models for request and response bodies
#
# User model for requesting to create a user
class UserCreate(BaseModel):
    name: str = Field(min_length=1, description="User name")
    email: EmailStr | None = None

# User model for response (includes ID)
class User(UserCreate):
    id: int


# In-memory storage for users
_users: Dict[int, User] = {
    1: User(id=1, name="Alice", email="alice@example.com"),
    2: User(id=2, name="Bob", email="bob@example.com"),
}

# Next user ID counter (for auto-increment)
_next_id: int = 2


#
# RESTful API endpoints for user management
#

# List all users
@app.get("/api/v1/users", response_model=List[User])
def list_users():
    return [ _users[k] for k in sorted(_users.keys()) ]

# Get a specific user by ID
@app.get("/api/v1/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = _users.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Create a new user
@app.post("/api/v1/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(req: UserCreate):
    global _next_id
    _next_id += 1
    user = User(id=_next_id, name=req.name, email=req.email)
    _users[user.id] = user
    return user

# Update an existing user
@app.put("/api/v1/users/{user_id}", response_model=User)
def update_user(user_id: int, req: UserCreate):
    if user_id not in _users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated_user = User(id=user_id, name=req.name, email=req.email)
    _users[user_id] = updated_user
    return updated_user

# Delete a user
@app.delete("/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in _users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    del _users[user_id]
    return None
