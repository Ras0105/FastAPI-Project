# FastAPI + MongoDB Student Management System

This document describes the workflow of the Student Management System built using **FastAPI**, **MongoDB**, **Jinja2 Templates**, and **HTML/CSS**.

---

# 1. Overall System Flow

```text
Start Uvicorn Server
        ↓
FastAPI Application Starts
        ↓
MongoDB Connection Established
        ↓
Browser Opens
http://127.0.0.1:8000/
        ↓
Login Page
        ↓
User Selects Role
(Admin / Student)
        ↓
Enter Email & Password
        ↓
Submit Login Form
        ↓
FastAPI Receives Request
        ↓
Validate Credentials from MongoDB
        ↓
Login Successful?
      /            \
    No              Yes
    ↓                ↓
Show Error      Redirect According to Role
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
    Admin Dashboard      Student Dashboard
```

---

# 2. Login Flow

```text
Browser Opens
        ↓
GET /
        ↓
FastAPI
        ↓
Render login.html
        ↓
User Selects Role
(Admin / Student)
        ↓
Enter Email & Password
        ↓
POST /student-login
        ↓
FastAPI Reads Form Data
        ↓
Search MongoDB
(email + password + role)
        ↓
User Found?
      /      \
    No        Yes
    ↓          ↓
Redirect      Check Role
/login?error=1
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
   /admin-page      /student-page
```

---

# 3. Student Registration Flow

```text
User Opens Signup Page
        ↓
GET /signup-student
        ↓
signup.html
        ↓
Enter Student Details
(Name, Age, Email,
Password, Role)
        ↓
Click Sign Up
        ↓
POST /create-student
        ↓
FastAPI
        ↓
Insert Document into MongoDB
        ↓
Redirect to Login Page
```

---

# 4. Password Reset Flow

```text
User Opens Reset Password Page
        ↓
GET /reset-password
        ↓
forget.html
        ↓
Enter Email
        ↓
Enter New Password
        ↓
POST /update-password
        ↓
FastAPI
        ↓
Search User by Email
        ↓
User Found?
      /         \
    No           Yes
    ↓             ↓
Show Message   Update Password
                    ↓
          Password Updated
                    ↓
            Return Login Page
```

---

# 5. Admin Workflow

```text
Admin Login
      ↓
Credentials Verified
      ↓
Admin Dashboard
      ↓
────────────────────────────────────
│                                  │
│      Select an Operation         │
│                                  │
────────────────────────────────────
      │
      ├──────────────┬───────────────────────┐
      │              │                       │
      ▼              ▼                       ▼

Show Students   Delete Selected      Delete All Students
      │              │                       │
      │              │                       │
Fetch Students   Select Students      Type "DELETE"
from MongoDB          │                for Confirmation
      │               │                       │
Display Table         │                       │
      │               │                       │
      ▼               ▼                       ▼
Back to Dashboard Delete Selected     Delete All Students
                       │                       │
                       ▼                       ▼
                 MongoDB Updated      MongoDB Updated
                       │                       │
                       └──────────┬────────────┘
                                  │
                                  ▼
                           Admin Dashboard
```

---

# 6. Student Workflow

```text
Student Login
        ↓
Credentials Verified
        ↓
Student Dashboard
        ↓
View Student Page
```

---

# 7. Show Students Flow

```text
Admin Dashboard
        ↓
Click "Show Students"
        ↓
FastAPI Fetches Students
from MongoDB
        ↓
Render admin.html
        ↓
JavaScript Toggles Table
Visibility
        ↓
Display Student List
```

---

# 8. Delete Selected Students Flow

```text
Admin Dashboard
        ↓
Select Student(s)
using Checkboxes
        ↓
Click Delete Selected
        ↓
POST /delete-some
        ↓
FastAPI
        ↓
delete_many()
        ↓
Redirect
/admin-page
```

---

# 9. Delete All Students Flow

```text
Admin Dashboard
        ↓
Type DELETE
        ↓
Click Delete All Students
        ↓
POST /delete-all
        ↓
Confirmation Correct?
      /         \
    No           Yes
    ↓             ↓
Show Message   delete_many()
                    ↓
          Redirect /admin-page
```

---

# 10. Request Processing Flow

```text
Browser
     │
HTTP Request
     ▼
Uvicorn Server
     ▼
FastAPI
     ▼
Route Matching
     ▼
Python Function
     ▼
MongoDB
(Read / Insert / Update / Delete)
     ▼
FastAPI Response
     ▼
Jinja2 Template
     ▼
Browser
```

---

# 11. Project Architecture

```text
User
 │
 ▼
Browser
 │
 ▼
HTML Form
 │
 ▼
FastAPI Route
 │
 ▼
Business Logic
 │
 ▼
MongoDB Database
 │
 ▼
Jinja2 Template
 │
 ▼
Browser
```

---

# 12. Folder Interaction Flow

```text
Browser
      │
      ▼
main.py
      │
      ▼
FastAPI Routes
      │
      ▼
MongoDB Database
      │
      ▼
Retrieve / Modify Data
      │
      ▼
Jinja2 Templates
(login.html
signup.html
student.html
admin.html)
      │
      ▼
Browser
```

---

# 13. Current Features

✔ Student Registration

✔ Student Login

✔ Admin Login

✔ Role-based Redirection

✔ Forgot Password

✔ View Students

✔ Delete Selected Students

✔ Delete All Students

✔ MongoDB Integration

✔ FastAPI Routing

✔ HTML + CSS Interface

---

# 14. Future Enhancements

```text
Password Hashing
        ↓
Session Management
        ↓
Remember Me
        ↓
Logout
        ↓
JWT Authentication
        ↓
Protected Routes
        ↓
Admin Add Student
        ↓
Admin Update Student
        ↓
Student Profile Editing
```

---

# 15. Complete Project Lifecycle

```text
Run Uvicorn
      ↓
FastAPI Starts
      ↓
Connect MongoDB
      ↓
Open Browser
      ↓
Login / Signup
      ↓
Authenticate User
      ↓
Redirect According to Role
      ↓
Admin
(View/Delete Students)

OR

Student
(View Dashboard)
      ↓
Exit Application
```