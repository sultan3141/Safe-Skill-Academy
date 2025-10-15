# 🛡️ Safe Skill Academy

Safe Skill Academy is a full-stack **Django web platform** designed to deliver secure, interactive, and scalable online learning experiences.  
It enables students to register, take quizzes, and track their progress — while teachers can create and manage quizzes efficiently.

---

## 🧭 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [Admin Credentials](#-admin-credentials)
- [API Overview](#-api-overview)
- [Screenshots](#-screenshots)
- [Author](#-author)
- [License](#-license)

---

## 🌍 Overview

Many students face challenges accessing quality skill training and assessments.  
**Safe Skill Academy** solves this by providing:
- A reliable platform for teachers to create quizzes
- A simple, modern interface for students to learn and be tested
- A secure backend for user and quiz management

---

## ⚙️ Features

### 👥 User System
- Custom `User` model using email for authentication
- Auto-generated `Profile` with image, country, and bio
- OTP and token-based authentication (for API integration)

### 🧠 Quiz Management
- Teachers can create quizzes with multiple questions and answers
- Students can take quizzes and view their scores
- Quiz, Question, and Answer models registered in Django Admin

### 🧰 Admin Dashboard
- Enhanced UI using **Jazzmin**
- CRUD operations for users, quizzes, and profiles

### 🖼️ Media & File Management
- All uploaded files stored in `/media/category/`
- Default images for user profiles

---

## 💻 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend Framework** | Django 5.x |
| **Database** | SQLite (default) |
| **Frontend Template** | Django Template Engine |
| **Admin Theme** | Jazzmin |
| **Language** | Python 3.10+ |
| **Authentication** | Django Auth / Token-based |

---

## 🗂️ Project Structure

