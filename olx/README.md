# olx-clone

OLX Clone App built with Django and Django REST Framework (DRF).

## Features

- Product Listings with hierarchical Categories and Subcategories
- Products with customizable fields
- User Authentication and Management with JWT (JSON Web Tokens)
- RESTful API endpoints for listings and users
- PostgreSQL as the database backend
- Containerized with Docker and Docker Compose for easy deployment

## Technology Stack

- Python 3.12
- Django 4.2
- Django REST Framework
- PostgreSQL 15
- Docker & Docker Compose
- Gunicorn WSGI HTTP Server

## Installation and Setup

### Prerequisites

- Python 3.12+
- PostgreSQL
- Docker and Docker Compose (optional, for containerized setup)

### Local Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd olx
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Configure PostgreSQL database:

   Create a PostgreSQL database named `olxdb` and a user `user1` with password `1234`. Update the database settings in `olx/olx/settings.py` if needed.

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional, for admin access):

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

The app will be accessible at `http://127.0.0.1:8000/`.

### Docker Setup

1. Build and start the containers:

   ```bash
   docker-compose up --build
   ```

2. The web service will be available at `http://localhost:8000/`.

3. To stop the containers:

   ```bash
   docker-compose down
   ```

## Running the Application

- The API endpoints for listings and users are available via RESTful routes.
- Authentication uses JWT tokens.
- Admin interface is available at `/admin` (requires superuser).

## Project Structure

```
olx/
├── listings/           # Listings app: categories, products, serializers, views
├── users/              # Users app: custom user model, authentication
├── olx/                # Project settings and configuration
├── Dockerfile          # Docker image build instructions
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
├── manage.py           # Django management script
└── README.md           # This file
```

## Running Tests

Run Django tests with:

```bash
python manage.py test
```

## Contribution Guidelines

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
