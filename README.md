# FastAPI TodoApp - Full Stack Application

A modern, full-featured todo application built with FastAPI, featuring user authentication, role-based access control, and a responsive web interface.

## 🎯 Features

### Core Functionality
- **User Management**: Registration, authentication, and profile management
- **Todo Management**: Create, read, update, and delete todos with priorities
- **Role-Based Access**: Admin and regular user roles with different permissions
- **Responsive Web Interface**: HTML templates with Bootstrap styling
- **Database Migrations**: Alembic integration for schema management

### Security Features
- JWT token-based authentication
- Password hashing with bcrypt
- Session management with HTTP-only cookies
- Role-based authorization middleware

### API Features
- **RESTful API**: Comprehensive REST endpoints for all operations
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc
- **Request Validation**: Pydantic models for data validation
- **Error Handling**: Comprehensive error responses and status codes

## 🛠 Technology Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern, fast web framework for building APIs
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: SQL toolkit and Object-Relational Mapping
- **[Alembic](https://alembic.sqlalchemy.org/)**: Database migration tool
- **[PostgreSQL](https://www.postgresql.org/)**: Primary database (configurable)
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Data validation using Python type annotations

### Authentication & Security
- **[python-jose](https://github.com/mpdavis/python-jose)**: JWT token handling
- **[passlib](https://passlib.readthedocs.io/)**: Password hashing utilities
- **[bcrypt](https://github.com/pyca/bcrypt/)**: Password hashing algorithm

### Frontend
- **[Jinja2](https://jinja.palletsprojects.com/)**: Template engine for HTML rendering
- **[Bootstrap](https://getbootstrap.com/)**: CSS framework for responsive design
- **[Starlette](https://www.starlette.io/)**: ASGI framework (FastAPI dependency)

### Development & Testing
- **[pytest](https://pytest.org/)**: Testing framework
- **[pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)**: Async testing support
- **[Uvicorn](https://www.uvicorn.org/)**: ASGI server implementation

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+ (or SQLite for development)
- Virtual environment tool (venv, virtualenv, or conda)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd fastapi-todo-fullstack
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
cd TodoApp
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the `TodoApp` directory:

```env
# Database Configuration
SQLALCHEMY_DATABASE_URL="postgresql://username:password@localhost:5432/todos_app"

# For development with SQLite (optional):
# SQLALCHEMY_DATABASE_URL="sqlite:///./todosapp.db"
```

### 5. Database Setup

#### PostgreSQL Setup
```bash
# Create database
createdb todos_app

# Run migrations
alembic upgrade head
```

#### SQLite Setup (Development)
```bash
# Database will be created automatically
alembic upgrade head
```

## 🏃‍♂️ Running the Application

### Development Server
```bash
uvicorn TodoApp.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Production Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📁 Project Structure

```
TodoApp/
├── main.py                 # Application entry point and configuration
├── database.py             # Database connection and session management
├── models.py               # SQLAlchemy database models
├── requirements.txt        # Python dependencies
├── alembic.ini            # Alembic configuration
├── schema.sql             # Database schema reference
├── .env                   # Environment variables
│
├── routers/               # API route modules
│   ├── __init__.py
│   ├── auth.py           # Authentication endpoints
│   ├── todos.py          # Todo CRUD operations
│   ├── users.py          # User management
│   └── admin.py          # Admin-only operations
│
├── templates/             # HTML templates
│   ├── layout.html       # Base template
│   ├── navbar.html       # Navigation component
│   ├── home.html         # Landing page
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   ├── todo.html         # Todo list view
│   ├── add-todo.html     # Add todo form
│   └── edit-todo.html    # Edit todo form
│
├── static/               # Static assets (CSS, JS, images)
│
├── test/                 # Test suite
│   ├── __init__.py
│   ├── utils.py          # Test utilities
│   ├── test_main.py      # Main application tests
│   ├── test_auth.py      # Authentication tests
│   ├── test_todos.py     # Todo operation tests
│   ├── test_users.py     # User management tests
│   └── test_admin.py     # Admin functionality tests
│
└── alemibc/              # Database migrations
    ├── env.py            # Migration environment
    ├── script.py.mako    # Migration template
    └── versions/         # Migration files
```

## 🔧 API Documentation

### Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/` | Create new user account |
| POST | `/auth/token` | Login and obtain access token |
| GET | `/auth/login-page` | Login form (HTML) |
| GET | `/auth/register-page` | Registration form (HTML) |
| GET | `/auth/logout` | Logout and clear session |

### Todo Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos/` | Get user's todos |
| GET | `/todos/{todo_id}` | Get specific todo |
| POST | `/todos/` | Create new todo |
| PUT | `/todos/{todo_id}` | Update existing todo |
| DELETE | `/todos/{todo_id}` | Delete todo |
| GET | `/todos/todo-page` | Todo management interface (HTML) |
| GET | `/todos/add-todo-page` | Add todo form (HTML) |
| GET | `/todos/edit-todo-page/{todo_id}` | Edit todo form (HTML) |

### User Management Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | Get current user info |
| PUT | `/users/password` | Change password |
| PUT | `/users/{user_id}` | Update user profile |
| GET | `/users/edit-profile-page` | Edit profile form (HTML) |

### Admin Endpoints (Admin Role Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/todo` | Get all todos (all users) |
| DELETE | `/admin/todo/delete/{todo_id}` | Delete any todo |

## 📊 Database Schema

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `username` (Unique)
- `first_name`
- `last_name`
- `hash_password`
- `is_active` (Boolean)
- `role` (admin/user)
- `phone_number`

### Todos Table
- `id` (Primary Key)
- `title`
- `description`
- `priority` (1-5 scale)
- `complete` (Boolean)
- `user_id` (Foreign Key to users.id)

## 🧪 Testing

### Run All Tests
```bash
cd TodoApp
pytest
```

### Run Specific Test Files
```bash
pytest test/test_auth.py
pytest test/test_todos.py
pytest test/test_users.py
pytest test/test_admin.py
```

### Run Tests with Coverage
```bash
pytest --cov=. --cov-report=html
```

### Test Database
The application uses a separate test database (`testdb.db`) for testing to avoid affecting development data.

## 🚀 Deployment

### Environment Variables for Production
```env
# Production Database
SQLALCHEMY_DATABASE_URL="postgresql://user:password@host:port/database"

# Security (generate new secret key)
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"

# Application Settings
DEBUG=False
```

### Database Migration in Production
```bash
# Apply pending migrations
alembic upgrade head

# Create new migration (if needed)
alembic revision --autogenerate -m "Description of changes"
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY TodoApp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY TodoApp/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔒 Security Considerations

### Authentication
- JWT tokens with configurable expiration
- Secure password hashing using bcrypt
- HTTP-only cookies for web interface
- CSRF protection for forms

### Authorization
- Role-based access control (Admin/User)
- User-specific data isolation
- Admin-only endpoints for management operations

### Best Practices
- Environment-based configuration
- SQL injection prevention via SQLAlchemy ORM
- Input validation with Pydantic models
- Proper error handling without information leakage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write tests for new functionality
- Update documentation for API changes
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🛟 Support

For questions, issues, or contributions:
- Open an issue in the GitHub repository
- Review the API documentation at `/docs` endpoint
- Check the test files for usage examples

## 🎯 Roadmap

- [ ] Email verification for user registration
- [ ] Password reset functionality
- [ ] Todo sharing and collaboration
- [ ] File attachments for todos
- [ ] Advanced filtering and search
- [ ] Mobile API optimization
- [ ] Real-time notifications
- [ ] Todo categories and tags

---

**Built with ❤️ using FastAPI and modern Python tools**