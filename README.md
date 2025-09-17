# Qubicweb Backdoor

Admin and API interface for QubicWeb - News Aggregator platform.

## Features

- **Blog Management (Qubic Originals)**: Create, read, update, and delete blog posts
- **Custom JSON Response**: Consistent API response format
- **Pagination**: Customizable pagination with page size controls
- **Modern Admin Interface**: Enhanced Django admin panel with Django Unfold theme

## Tech Stack

- **Backend**: Django v4
- **API**: Django REST Framework
- **Database**: SQLite (development)
- **Admin UI**: Django Unfold
- **Rich Text Editor**: Django TinyMCE 4.1.0
- **Code Formatting**: Black
- **Python**: 3.x

## Project Structure

```
qubicweb-backdoor/
├── blog/                   # Blog app
│   ├── models.py          # Category, Post, Comment, Reply models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # Blog URL patterns
│   └── migrations/        # Database migrations
├── core/                # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   ├── helpers.py         # Custom renderers and pagination
│   └── wsgi.py            # WSGI configuration
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── package.json           # NPM scripts for development
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
# or using npm script
npm run install
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
# or using npm script
npm run migrate
```

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver 3010
# or using npm script
npm run dev
```

The API will be available at `http://localhost:3010/`

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

## Admin Panel

The Django admin panel is accessible at `http://localhost:3010/admin/`.
The admin interface features a modern, responsive design powered by `Django Unfold`.
