# Hostel Management System

A comprehensive web-based hostel management system built with Django 5.x and MySQL. Manage rooms, students, wardens, fees, complaints, and notices with role-based access control.

## Features

### Three User Roles

**Administrator**
- Dashboard with key statistics (students, rooms, fees, complaints)
- Manage rooms (add, view, delete)
- Manage students (add, view, delete, assign/vacate rooms)
- Manage wardens (add, view, delete)
- Manage fees (add, mark paid, delete)
- View and resolve complaints
- Manage notices (add, view, delete)

**Warden**
- Dashboard with overview statistics
- View all students (filter by room assignment status)
- View all rooms and occupants
- Manage fees (add, mark paid)
- View and resolve complaints

**Student**
- Self-registration with photo and ID proof
- Personal dashboard with room and roommate info
- View and pay pending fees
- File and track complaints
- Read hostel notices

### Business Rules
- Room bed count automatically managed on student assignment/vacation
- Cannot assign student to a room with 0 available beds
- Available beds never exceed total beds or go negative
- Safe deletion handling (students with/without rooms)

### Security Features
- Session-based authentication
- Password hashing with Django's `make_password`/`check_password`
- Role-based access decorators on all protected views
- CSRF protection on all forms
- POST-only for delete, resolve, vacate, and payment actions
- Server-side validation with error messages
- Image type validation for uploads

## Tech Stack

- **Backend:** Django 5.x
- **Database:** MySQL
- **Frontend:** Django Templates (HTML/CSS)
- **Image Handling:** Pillow
- **Environment:** python-decouple

## Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip

## Installation

### 1. Clone or navigate to the project

```bash
cd hostel_management
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create MySQL database

```sql
mysql -u root -p
```

```sql
CREATE DATABASE hostel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 5. Configure environment variables

Copy the example file and edit with your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```ini
# Django Settings
SECRET_KEY=your-secret-key-generate-a-new-one
DEBUG=True

# Database Settings
DB_NAME=hostel_db
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

**Generate a new SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create media directory

```bash
mkdir -p media/students/photos media/students/id_proofs media/rooms media/wardens
```

### 8. Run the development server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

## Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Warden | *(create via admin panel)* | - |
| Student | *(self-registration)* | - |

> **Note:** Admin credentials are configured in your `.env` file. Change them for production!

## Project Structure

```
hostel_management/
├── hostel_management/       # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # User authentication & wardens
│   ├── models.py           # Warden model
│   ├── views.py            # Login/logout/dashboard views
│   ├── decorators.py       # Role-based access decorators
│   └── urls.py
├── students/                # Student management
│   ├── models.py           # Student model
│   ├── views.py            # CRUD views
│   └── urls.py
├── rooms/                   # Room management
│   ├── models.py           # Room model
│   ├── views.py            # CRUD views
│   └── urls.py
├── fees/                    # Fee management
│   ├── models.py           # Fee model
│   ├── views.py            # Fee views
│   └── urls.py
├── complaints/              # Complaint management
│   ├── models.py           # Complaint model
│   ├── views.py            # Complaint views
│   └── urls.py
├── notice/                  # Notice management
│   ├── models.py           # Notice model
│   ├── views.py            # Notice views
│   └── urls.py
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── accounts/           # Auth templates
│   ├── students/           # Student templates
│   ├── rooms/              # Room templates
│   ├── fees/               # Fee templates
│   ├── complaints/         # Complaint templates
│   └── notice/             # Notice templates
├── static/
│   └── css/
│       └── style.css       # All styles
├── media/                   # Uploaded files (gitignored)
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Models Overview

| Model | App | Key Fields |
|-------|-----|------------|
| Warden | accounts | name, email, phone, username, password, photo |
| Room | rooms | room_number, room_type, floor, total_beds, available_beds, rent |
| Student | students | name, email, phone, college, course, username, password, photo, id_proof, room (FK) |
| Fee | fees | student (FK), month, amount, status, payment_date |
| Complaint | complaints | student (FK), title, description, status, date |
| Notice | notice | title, description, date |

## URL Endpoints

### Public
- `/` - Home page
- `/admin/login/` - Admin login
- `/warden/login/` - Warden login
- `/student/login/` - Student login
- `/student/register/` - Student registration

### Admin (requires admin login)
- `/admin/dashboard/` - Admin dashboard
- `/rooms/` - Room management
- `/students/` - Student management
- `/admin/wardens/` - Warden management
- `/fees/` - Fee management
- `/complaints/` - Complaint management
- `/notice/` - Notice management

### Warden (requires warden login)
- `/warden/dashboard/` - Warden dashboard
- `/rooms/warden/` - View rooms
- `/students/warden/` - View students
- `/fees/warden/` - Manage fees
- `/complaints/warden/` - View complaints

### Student (requires student login)
- `/student/dashboard/` - Student dashboard
- `/fees/student/` - View/pay fees
- `/complaints/student/` - File/view complaints
- `/notice/student/` - Read notices

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Generate a new `SECRET_KEY`
3. Change admin credentials
4. Configure `ALLOWED_HOSTS` in `settings.py`
5. Set up static file serving (whitenoise or nginx)
6. Use a production-grade WSGI server (gunicorn)
7. Enable HTTPS

```bash
# Example with gunicorn
pip install gunicorn
gunicorn hostel_management.wsgi:application --bind 0.0.0.0:8000
```

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL is running
- Verify credentials in `.env`
- Check that the database exists

### Migration Errors
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Permission Denied on Media
```bash
chmod -R 755 media/
```

## License

This project is for educational purposes.

---

Built with Django 5.x | MySQL | Python
