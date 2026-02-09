# FastAPI Task Management System - Microservices

## Overview
This project is a microservices-based backend architecture decomposing the monolithic Task Management System into independent, scalable services. It demonstrates modern distributed system design with service isolation, inter-service communication, and decentralized authentication.

The system comprises three independent services: **Auth Service** (authentication & user management), **Task Service** (task operations), and **User Service** (user profiles), each with its own database and API. An **API Gateway** acts as a single entry point, routing requests to the respective services.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| API Framework | FastAPI |
| Server | Uvicorn |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Authentication | JWT (JSON Web Tokens) |
| Database | PostgreSQL (per service) |
| Password Hashing | Bcrypt |
| Inter-service Communication | Async HTTP (httpx.AsyncClient) |

---

## Architecture Decisions

### Service Separation
- **Auth Service**: Handles user registration, login, and JWT token validation
- **Task Service**: Manages task CRUD operations (requires valid JWT)
- **User Service**: Manages user profiles (requires valid JWT)

### Key Design Choices
1. **Database per Service**: Each service has its own PostgreSQL database for independence and scalability
2. **JWT-based Authentication**: Stateless auth tokens validated across services without session management
3. **Async HTTP Communication**: Services communicate via async HTTP using httpx.AsyncClient for non-blocking inter-service calls
4. **Shared Security Model**: Auth Service acts as the source of truth for token validation
5. **Independent Deployments**: Services can be deployed, scaled, and updated independently

---

## Service Communication Flow

```
Client Requests
    ↓
┌─────────────────────────────────────┐
│      API Gateway (Port 8000)        │
│  • Routes all client requests       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│      Auth Service   │  Task Service   │  User Service       │
│      (Port 8001)    │  (Port 8002)    │  (Port 8003)        │
└─────────────────────────────────────────────────────────────┘
    ↓ (Internal validation)
    └→ Auth Service: `/auth/validate-token` for JWT verification
```

### Communication Details
- **Client → API Gateway**: Single entry point for all requests (http://localhost:8000)
- **API Gateway → Services**: Routes requests to appropriate microservices internally
- **Task/User Services → Auth Service**: Async HTTP call to `/auth/validate-token` to verify JWT tokens
- Each service maintains its own PostgreSQL database

---

## How Authentication Works

1. **Registration/Login** (via Auth Service)
   - User registers with email & password
   - Auth Service hashes password using Bcrypt
   - On login, Auth Service generates JWT token containing `user_id`, `email`, `is_active`, and `created_at`

2. **Token Structure**
   - JWT encoded with SECRET_KEY
   - Contains user identity information
   - Used across all services without storing session data

3. **Service-to-Service Validation** (via Dependencies)
   - Task & User Services receive JWT from client
   - Services call Auth Service's `/auth/validate-token` endpoint
   - Auth Service validates token signature and returns user information
   - Services use returned user info to enforce data isolation (users can only access their own data)

4. **Protected Routes**
   - All non-auth endpoints require valid JWT token
   - Dependency injection via `get_current_user()` extracts and validates user from token

---

## Project Structure

```
.
├── auth_service/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py          # Settings & environment
│   │   │   ├── database.py        # DB engine & session
│   │   │   ├── security.py        # Password hashing & JWT
│   │   │   └── responses.py       # Standardized responses
│   │   ├── models/
│   │   │   └── user.py            # User model
│   │   ├── schemas/
│   │   │   └── auth.py            # Request/response schemas
│   │   ├── routers/
│   │   │   └── auth.py            # Auth endpoints
│   │   ├── services/
│   │   │   └── auth_service.py    # Auth business logic
│   │   ├── dependencies/
│   │   │   └── db.py              # DB session dependency
│   │   ├── migrations/            # Alembic migrations
│   │   ├── alembic.ini
│   │   ├── main.py                # App entry point
│   │   └── requirements.txt
│   └── .env
│
├── task_service/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── responses.py
│   │   ├── models/
│   │   │   └── task.py            # Task model
│   │   ├── schemas/
│   │   │   └── task.py
│   │   ├── routers/
│   │   │   └── task.py            # Task endpoints
│   │   ├── services/
│   │   │   └── task_service.py    # Task business logic
│   │   ├── dependencies/
│   │   │   ├── db.py
│   │   │   └── auth.py            # Token validation
│   │   ├── migrations/
│   │   ├── alembic.ini
│   │   ├── main.py
│   │   └── requirements.txt
│   └── .env
│
├── user_service/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── responses.py
│   │   ├── models/
│   │   │   └── user_profile.py    # User profile model
│   │   ├── schemas/
│   │   │   └── user.py
│   │   ├── routers/
│   │   │   └── user.py            # User profile endpoints
│   │   ├── services/
│   │   │   └── user_service.py    # Profile business logic
│   │   ├── dependencies/
│   │   │   ├── db.py
│   │   │   └── auth.py            # Token validation
│   │   ├── migrations/
│   │   ├── alembic.ini
│   │   ├── main.py
│   │   └── requirements.txt
│   └── .env
│
├── api_gateway/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py          # Gateway settings
│   │   ├── routers/
│   │   │   ├── auth.py            # Auth route forwarding
│   │   │   ├── tasks.py           # Task route forwarding
│   │   │   └── users.py           # User route forwarding
│   │   └── main.py                # Gateway entry point
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- PostgreSQL (3 separate databases or schemas)
- pip package manager

### Step 1: Clone and Navigate
```bash
cd Task-Management-System-MicroServices
```

### Step 2: Setup Auth Service

```bash
cd auth_service

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://username:password@localhost:5432/auth_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
EOF

# Apply migrations
alembic upgrade head

# Start Auth Service (Port 8001)
uvicorn app.main:app --reload --port 8001
```

### Step 3: Setup Task Service

```bash
cd ../task_service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://username:password@localhost:5432/task_db
AUTH_SERVICE_URL=http://localhost:8001
EOF

alembic upgrade head

# Start Task Service (Port 8002)
uvicorn app.main:app --reload --port 8002
```

### Step 4: Setup User Service

```bash
cd ../user_service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://username:password@localhost:5432/user_db
AUTH_SERVICE_URL=http://localhost:8001
EOF

alembic upgrade head

# Start User Service (Port 8003)
uvicorn app.main:app --reload --port 8003
```

---

## API Gateway Endpoints (Port 8000)

The API Gateway routes all requests to the appropriate microservices:

### Authentication
- POST `/auth/register` - Register new user
- POST `/auth/login` - Login and get JWT token
- POST `/auth/validate-token` - Validate token (internal use)

### Tasks - *Requires JWT Token*
- POST `/tasks` - Create task
- GET `/tasks` - List user's tasks
- PUT `/tasks` - Update task
- DELETE `/tasks` - Delete task

### Users - *Requires JWT Token*
- GET `/users/me` - Get user profile
- POST `/users/createprofile` - Create user profile
- PUT `/users/me` - Update user profile
- DELETE `/users/deleteprofile` - Delete user profile

---

## Database & Migrations

- Each service has its own PostgreSQL database (auth_db, task_db, user_db)
- Alembic manages schema migrations per service
- Run `alembic upgrade head` in each service directory

### Common Alembic Commands
```bash
alembic revision --autogenerate -m "message"
alembic upgrade head
alembic downgrade -1
```

---

## How to Run All Services

### Option 1: Manual Terminal Sessions
Open 4 terminal windows and run each service separately as shown in Setup Instructions above (Auth, Task, User, then API Gateway).

### Option 2: Using a Process Manager
Example with tmux:
```bash
tmux new-session -d -s tms 'cd auth_service && source venv/bin/activate && uvicorn app.main:app --port 8001'
tmux new-window -t tms 'cd task_service && source venv/bin/activate && uvicorn app.main:app --port 8002'
tmux new-window -t tms 'cd user_service && source venv/bin/activate && uvicorn app.main:app --port 8003'
tmux new-window -t tms 'cd api_gateway && source venv/bin/activate && uvicorn app.main:app --port 8000'
tmux attach -t tms
```

### Verifying All Services Are Running
```bash
curl http://localhost:8000/health  # API Gateway health check
curl http://localhost:8001/health  # Auth Service
curl http://localhost:8002/health  # Task Service
curl http://localhost:8003/health  # User Service
```

---

## Example Workflow (via API Gateway)

```bash
# 1. Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "password":"password123"}'

# 2. Login and get token
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "password":"password123"}' | jq -r '.data.access_token')

# 3. Create task
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Task", "description":"Task description"}'

# 4. Get user profile
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## Key Design Patterns

- **Service Isolation**: Independent data storage and business logic
- **Stateless Authentication**: JWT tokens eliminate need for shared session storage
- **Dependency Injection**: FastAPI dependencies manage database sessions and auth validation
- **Error Handling**: Standardized response format across all services
- **Environment Configuration**: Sensitive values loaded from `.env` files

---

## Key Learnings

- Microservices architecture design and implementation
- Service decomposition and boundary identification
- Inter-service communication patterns
- Distributed authentication using JWT
- Database per service pattern
- Independent scaling and deployment strategies

---

**Note**: This project is built as part of a FastAPI practical assignment to demonstrate microservices architecture, distributed system design, and backend development practices.