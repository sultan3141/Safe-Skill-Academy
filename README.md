# 🛡️ Safe Skill Academy

**Safe Skill Academy** is a Django-based backend platform built to help users discover, enroll in, and track progress across various skill-building courses.  
It emphasizes **secure authentication**, **structured learning paths**, and **scalable RESTful API design**.

---

## 🚀 Project Goals
- Provide a robust backend for a skill development platform.  
- Implement secure user authentication and course management.  
- Design RESTful APIs for seamless frontend integration.  
- Support multilingual and multi-level course offerings.  

---

## 🏗️ System Overview
The backend serves as the **central API** for handling:
- User registration, authentication, and roles  
- Course creation and management  
- Quiz creation, submission, and results  
- Enrollment tracking  
- Notifications and reviews  

This backend can power a web or mobile frontend for online learning platforms.

---

## 🔐 Authentication & Authorization
The project uses **JWT (JSON Web Token)** for secure user authentication.  

### User Roles:
- 👨‍🏫 **Teacher** – can create courses, quizzes, and review enrollment requests.  
- 👩‍🎓 **Student** – can enroll in courses, take quizzes, and view progress.  

### Authentication Endpoints:
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `POST` | `/api/user/register/` | Register a new user |
| `POST` | `/api/user/token/` | Obtain access and refresh tokens |
| `POST` | `/api/user/token/refresh/` | Refresh access token |

---

## 🧍‍♂️ Student Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/api/student/summery/<user_id>/` | View student progress summary |
| `GET` | `/api/student/course-list/<user_id>/` | Get list of enrolled courses |
| `GET` | `/api/student/course-detail/<user_id>/<enrollment_id>/` | Get detailed course info |
| `POST` | `/api/student/course-completed/` | Mark a course as completed |
| `POST` | `/api/student/course-Note-create/` | Create a note for a course |
| `GET` | `/api/student/course-Note-detail/` | Retrieve saved notes |
| `POST` | `/api/student/rate-course/` | Rate or review a course |
| `PUT` | `/api/student/review-detail/` | Update course review |
| `POST` | `/api/student/wishlist-create/` | Add a course to wishlist |
| `POST` | `/api/student/enrollment-requests/create/` | Submit enrollment request |
| `GET` | `/api/student/enrollment-requests/my/` | View own enrollment requests |
| `GET` | `/api/student/quiz-list/<course_id>/` | List all quizzes for a course |
| `POST` | `/api/student/quiz/<quiz_id>/submit/` | Submit a quiz attempt |
| `GET` | `/api/student/quiz-result/<student_id>/<attempt_id>/` | View quiz result |

---

## 👨‍🏫 Teacher Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/api/teacher/enrollment-requests/` | View all student enrollment requests |
| `PUT` | `/api/teacher/enrollment-requests/<request_id>/review/` | Approve or reject request |
| `GET` | `/api/teacher/course-list/<teacher_id>/` | List all teacher’s courses |
| `GET` | `/api/teacher/review-list/<teacher_id>/` | View all course reviews |
| `GET` | `/api/teacher/review-detail/<teacher_id>/<review_id>/` | Get details of specific review |
| `GET` | `/api/teacher/student-list/<teacher_id>/` | Get list of students per teacher |
| `POST` | `/api/teacher/courses/create/` | Create a new course |
| `PUT` | `/api/teacher/courses/<pk>/` | Update or delete a course |
| `DELETE` | `/api/teacher/variant-delete/<teacher_id>/<course_id>/<variant_id>/` | Delete a course variant |
| `DELETE` | `/api/teacher/variant-item-delete/<teacher_id>/<course_id>/<variant_id>/<variant_item_id>/` | Delete a variant item |
| `GET/POST` | `/api/teacher/quizzes/` | List or create quizzes |
| `GET` | `/api/teacher/quizzes/<quiz_id>/` | Retrieve specific quiz |
| `GET/POST` | `/api/teacher/quizzes/<quiz_id>/questions/` | Manage quiz questions |
| `GET/POST` | `/api/teacher/quizzes/<quiz_id>/questions/<question_id>/answers/` | Manage answers for a question |
| `GET/POST` | `/api/teacher/materials/` | List or create course materials |
| `GET/PUT/DELETE` | `/api/teacher/materials/<material_id>/` | Manage material details |

---

## 🧱 Course & General API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET/POST` | `/api/categories/` | List or create categories |
| `GET/POST` | `/api/courses/` | List or create courses |
| `GET/POST` | `/api/variants/` | List or create course variants |
| `GET/POST` | `/api/variant-items/` | List or create variant items |
| `GET/POST` | `/api/notes/` | Manage notes |
| `GET/POST` | `/api/reviews/` | Manage course reviews |
| `GET/POST` | `/api/notifications/` | Get or send notifications |
| `GET/POST` | `/api/messages/` | Question and answer messages |
| `GET/POST` | `/api/completed-courses/` | View completed courses |
| `GET/POST` | `/api/enrolled-courses/` | Manage enrolled courses |
| `GET` | `/api/countries/` | List supported countries |

---

## 🧰 Tools & Technologies

| Technology | Purpose |
|-------------|----------|
| **Django** | Web framework for backend development |
| **Django REST Framework (DRF)** | API layer and serialization |
| **SimpleJWT** | Secure JWT-based authentication |
| **drf-yasg** | Swagger API documentation |
| **PostgreSQL / SQLite** | Database |
| **Render** | Cloud deployment |

---

## 🌐 Deployment

Deployed on **Render**:  
🔗 [https://safe-skill-academy.onrender.com](https://safe-skill-academy.onrender.com/api/)

Example:
- Swagger UI → `/`  
- Redoc → `/redoc/`  
- Base API → `/api/`


