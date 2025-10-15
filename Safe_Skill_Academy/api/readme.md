# 🛡️ Safe Skill Academy API

**Safe Skill Academy** is a Django REST Framework–based backend system for managing an online learning platform.  
It supports secure user authentication, teacher–student interactions, course management, quizzes, and enrollment workflows — all through clean, RESTful API endpoints.

---

## 🚀 Features

### 🔐 Authentication & Users
- JWT-based authentication using **SimpleJWT**
- Secure registration with password validation
- Automatic username creation from email
- User profile management

### 👨‍🏫 Teachers & Courses
- Teachers can create and manage courses
- Each course includes:
  - Categories
  - Variants and items (curriculum)
  - Course materials (video, PDF, image, note)
  - Ratings and reviews

### 🧠 Quizzes & Assessments
- Teachers can create quizzes, questions, and multiple answers
- Students can attempt quizzes
- Scores are calculated automatically as percentages

### 🎓 Enrollment System
- Students can request to enroll in courses
- Validation prevents duplicate or pending requests
- Tracks completed and ongoing courses

### ❤️ Wishlist & Notifications
- Students can add courses to wishlist
- System supports notifications and messages between users

---

## 🗂️ Project Structure

