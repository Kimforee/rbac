# **Django RBAC Project**

This project implements a **Role-Based Access Control (RBAC)** system using Django, providing secure authentication, authorization, and role management for a web application. The project allows administrators, moderators, and users to perform specific actions based on their assigned roles. It is designed with flexibility, security, and modularity in mind.

---

## **Table of Contents**
1. [Endpoints](#endpoints)
    - [Authentication](#authentication)
    - [User Endpoints](#user-endpoints)
    - [Moderator Endpoints](#moderator-endpoints)
    - [Admin Endpoints](#admin-endpoints)
2. [Features](#features)
3. [Environment Setup](#environment-setup)
4. [Technologies Used](#technologies-used)
5. [Environment Variables](#environment-variables)
6. [Testing Tokens](#testing-tokens)
7. [Static Files](#static-files)

---

## **Endpoints**

### **1. Authentication**

| **Method** | **Endpoint**        | **Description**                        | **Role**        |
|------------|---------------------|----------------------------------------|-----------------|
| POST       | `/auth/login/`      | Login and generate a JWT token.        | All roles       |
| POST       | `/auth/logout/`     | Invalidate the JWT token.              | All roles       |
| POST       | `/auth/register/`   | Register a new user.                   | Public          |

---

### **2. User Endpoints**

| **Method** | **Endpoint**         | **Description**                        | **Role**        |
|------------|----------------------|----------------------------------------|-----------------|
| GET        | `/user/profile/`     | View profile information.              | User, Moderator, Admin |
| PATCH      | `/user/update/`      | Update user profile.                   | User, Moderator, Admin |

---

### **3. Moderator Endpoints**

| **Method** | **Endpoint**         | **Description**                        | **Role**        |
|------------|----------------------|----------------------------------------|-----------------|
| GET        | `/mod/review/`       | Review pending content.                | Moderator, Admin |
| POST       | `/mod/approve/`      | Approve submitted content.             | Moderator, Admin |

---

### **4. Admin Endpoints**

| **Method** | **Endpoint**          | **Description**                        | **Role**        |
|------------|-----------------------|----------------------------------------|-----------------|
| GET        | `/admin/users/`       | View all users.                        | Admin           |
| POST       | `/admin/assign-role/` | Assign or change a user's role.        | Admin           |
| DELETE     | `/admin/delete-user/` | Delete a user.                         | Admin           |

## **Features**

- **Authentication**: Secure login and logout with JWT.
- **Role-Based Access**: Admin, Moderator, and User roles with specific permissions.
- **Endpoints**:
  - Admins can manage users and roles.
  - Moderators can approve or review content.
  - Users can perform standard actions.
- **Secure Token Management**: Uses **JSON Web Tokens (JWT)** for session handling.
- **Django Templates**: Integrated basic frontend for testing RBAC logic.
- **DRF Browsable API**: Includes an interface for API exploration.

---

## **Environment Setup**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/rbac-deploy.git
cd rbac-deploy
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run Migrations**
```bash
python manage.py migrate
```

### **4. Create a Superuser**
```bash
python manage.py createsuperuser
```

### **5. Start the Server**
```bash
python manage.py runserver
```

## **Environment Variables**

| **Variable**          | **Description**                       |
|------------------------|---------------------------------------|
| `DJANGO_SECRET_KEY`    | The Django project's secret key.      |
| `DEBUG`                | Set to `True` for development, `False` for production. |
| `DATABASE_URL`         | Database connection URL (e.g., PostgreSQL). |
| `ALLOWED_HOSTS`        | Comma-separated list of allowed hosts (e.g., `localhost, rbac-deploy.vercel.app`). |
| `JWT_SECRET`           | Secret key for signing JWT tokens.    |

---
## **Technologies Used**

- **Django** (Backend Framework)
- **Django REST Framework** (API Development)
- **Django Allauth** (User Authentication)
- **PostgreSQL** (Database)
- **Gunicorn** (Production WSGI server)

---

## **Testing Tokens**

You can use the following JWT tokens to test role-based access:

1. **Admin Token**:
   - Generate a token by logging in with an admin account (`/auth/login/`).
   - Add the token to the **Authorization Header** as:
     ```
     Authorization: Bearer <admin-token>
     ```

2. **Moderator Token**:
   - Generate a token by logging in with a moderator account.
   - Add the token to the **Authorization Header**.

3. **User Token**:
   - Generate a token by logging in with a standard user account.

---

## **Static Files**

To collect static files for production:
```bash
python manage.py collectstatic
```

Ensure `STATIC_URL` and `STATIC_ROOT` are correctly set in `settings.py`:
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## **License**

This project is licensed under the MIT License.

---
