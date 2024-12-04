# **Django RBAC Project**

This project implements a **Role-Based Access Control (RBAC)** system using Django, providing secure authentication, authorization, and role management for a web application. The project allows administrators, moderators, and users to perform specific actions based on their assigned roles. It is designed with flexibility, security, and modularity in mind.

UI
![image](https://github.com/user-attachments/assets/1dad1cd9-6f56-41e5-89f1-7c7332e4b59c)
![image](https://github.com/user-attachments/assets/99b25c07-ff3a-482b-ba08-961d35b5bbc1)
![image](https://github.com/user-attachments/assets/b117dca8-44e6-42d0-968e-3c8c94fed690)
When admin tries for user view but can gain privilage manually :  
![image](https://github.com/user-attachments/assets/1078f043-46fd-4527-9be0-b31e39550f82)

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

### **1. Authentication Endpoints**

![image](https://github.com/user-attachments/assets/14aaca50-3d9e-4c10-a540-8dac023e9fe7)
![image](https://github.com/user-attachments/assets/d002a19e-9825-4b48-91a1-2aeb825be573)
| **Method** | **Endpoint**                     | **Description**                | **Role**        |
|------------|----------------------------------|--------------------------------|-----------------|
| POST       | `/auth/register/`                | Register a new user.           | Public          |
| POST       | `/auth/login/`                   | Login and obtain a JWT token.  | Public          |
| POST       | `/auth/token/refresh/`           | Refresh JWT token.             | Authenticated   |
| POST       | `/auth/logout/`                  | Logout and invalidate token.   | Authenticated   |

---

### **2. Admin Endpoints**

![image](https://github.com/user-attachments/assets/ba426c62-a14f-427d-b352-333f8f58cd77)

| **Method** | **Endpoint**                     | **Description**                | **Role**        |
|------------|----------------------------------|--------------------------------|-----------------|
| GET        | `/auth/admin-view/`              | Admin-only access endpoint.    | Admin           |

---

![image](https://github.com/user-attachments/assets/d4e798ed-8b21-46eb-9e07-d630667ae2cf)

### **3. Moderator Endpoints**

| **Method** | **Endpoint**                     | **Description**                | **Role**        |
|------------|----------------------------------|--------------------------------|-----------------|
| GET        | `/auth/moderator-view/`          | Moderator-only access endpoint.| Moderator       |

---

### **4. Admin and Moderator Endpoints**

| **Method** | **Endpoint**                     | **Description**                | **Role**        |
|------------|----------------------------------|--------------------------------|-----------------|
| GET        | `/auth/admin-or-moderator-view/` | Shared access for Admins and Moderators. | Admin, Moderator |

---

### **5. User Endpoints**
![image](https://github.com/user-attachments/assets/5e5024e8-ed62-45e0-8fdd-6e88719bc378)

| **Method** | **Endpoint**                     | **Description**                | **Role**        |
|------------|----------------------------------|--------------------------------|-----------------|
| GET        | `/auth/user-view/`               | User-only access endpoint.     | User            |


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
git clone https://github.com/kimforee/rbac.git
cd rbac
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
| `ALLOWED_HOSTS`        | Comma-separated list of allowed hosts (e.g., `localhost, rbac.vercel.app`). |
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
