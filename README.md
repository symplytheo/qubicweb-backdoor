# Qubicweb Backdoor

Admin and API interface for QubicWeb - News Aggregator platform.

## Features

- **News Aggregation**: RSS feed management and article aggregation from multiple sources
- **Blog Management (Qubic Originals)**: Create, read, update, and delete blog posts with rich text editing
- **User Management**: Custom user authentication with email verification and password reset
- **RSS Feed Automation**: Management commands to populate news articles from RSS feeds
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Custom JSON Response**: Consistent API response format across all endpoints
- **Pagination**: Customizable pagination with page size controls
- **Modern Admin Interface**: Enhanced Django admin panel with Django Unfold theme

## Tech Stack

- **Backend**: Django 4.2.24
- **API**: Django REST Framework 3.16.1
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (development), PostgreSQL ready
- **Admin UI**: Django Unfold 0.65.0
- **Rich Text Editor**: Django TinyMCE 4.1.0
- **RSS Parsing**: Feedparser 6.0.12
- **Static Files**: WhiteNoise
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Environment Management**: django-environ
- **Code Formatting**: Black
- **Web Server**: Gunicorn (production ready)
- **Python**: 3.x

## Project Structure

```
qubicweb-backdoor/
├── accounts/              # User accounts and authentication
│   ├── models.py          # User models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # Account URL patterns
│   ├── admin.py           # Admin configuration
│   └── migrations/        # Database migrations
|
├── blog/                  # Blog app (Qubic Originals)
│   ├── models.py          # Category, Post, Comment, Reply models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # Blog URL patterns
│   ├── admin.py           # Admin configuration
│   └── migrations/        # Database migrations
|
├── core/                  # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   ├── helpers.py         # Custom renderers and pagination
│   ├── views.py           # Core views
│   ├── asgi.py            # ASGI configuration
│   └── wsgi.py            # WSGI configuration
|
├── news/                  # News aggregation app
│   ├── models.py          # News models
│   ├── views.py           # News views
│   ├── urls.py            # News URL patterns
│   ├── utils.py           # News utilities
│   ├── admin.py           # Admin configuration
│   ├── management/        # Management commands
│   │   └── commands/
│   │       └── populate_rss.py  # RSS population command
│   └── migrations/        # Database migrations
|
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Makefile               # Development commands
├── README.md              # Project documentation
└── venv/                  # Virtual environment (created after setup)
```

## Installation & Setup

### Prerequisites

- Python 3.x
- pip (Python package manager)

### 1. Clone the repository

```bash
git clone <repository-url>
cd qubicweb-backdoor
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
# or using make command
make install
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
# or using make command
make migrate
```

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
# or using make command
make superuser
```

### 6. Populate RSS feeds (optional)

```bash
python manage.py populate_rss
```

### 7. Run the development server

```bash
python manage.py runserver 3010
# or using make command
make run
```

The API will be available at `http://localhost:3010/`

## API Endpoints

The application provides RESTful API endpoints for:

- **Authentication**: `/api/accounts/` - User registration, login, and profile management
- **Blog**: `/api/blog/` - Blog posts and categories management
- **News**: `/api/news/` - News articles and sources from RSS feeds
- **API Documentation**: `/api/docs/swagger/` - Interactive Swagger documentation
- **API Schema**: `/api/docs/schema/` - OpenAPI schema

## RSS Feed Management

The news aggregation system includes:

- **RSS Sources**: Manage multiple news sources with RSS feed URLs
- **Automatic Article Fetching**: Use `python manage.py populate_rss` to fetch latest articles
- **Article Management**: Full CRUD operations for news articles
- **Source Management**: Organize news sources by country and category

## API Response Format

All API responses follow a consistent format:

```json
{
  "success": true,
  "message": "Request completed successfully.",
  "data": {
    // Response data here
  },
  "errors": null
}
```

For paginated responses:

```json
{
  "success": true,
  "message": "Request completed successfully.",
  "data": {
    "items": [...],
    "meta": {
      "page": 1,
      "limit": 10,
      "total_pages": 5,
      "total_items": 50
    }
  },
  "errors": null
}
```

## Development Scripts

The project includes a Makefile for common development tasks:

- `make run` - Start development server on port 3010
- `make migrate` - Run makemigrations and migrate
- `make freeze` - Update requirements.txt with current packages
- `make install` - Install dependencies from requirements.txt
- `make superuser` - Create Django superuser
- `make shell` - Open Django shell
- `make collect` - Collect static files
- `make test` - Run tests
- `make format` - Format code with Black (line length: 120)
- `make help` - Show all available commands

## Admin Panel

The Django admin panel is accessible at `http://localhost:3010/admin/`.
The admin interface features a modern, responsive design powered by `Django Unfold` with:

- **Custom Theme**: Light theme with custom color scheme
- **Enhanced UI**: Modern sidebar with search functionality
- **Rich Text Editing**: TinyMCE integration for blog content
- **User Management**: Extended user model with verification features
- **News Management**: RSS sources and articles management
- **Blog Management**: Categories and posts with slug generation

## Environment Configuration

The project supports environment-based configuration using `.env` file:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

For production deployment, make sure to:

- Set `DJANGO_DEBUG=False`
- Configure `DJANGO_ALLOWED_HOSTS` with your domain
- Use PostgreSQL database instead of SQLite
- Set up proper static file serving with `collectstatic`
