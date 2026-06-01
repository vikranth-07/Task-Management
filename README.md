# 📋 Smart Task Manager

## Project Overview

Smart Task Manager is a web-based Task Management System developed using Streamlit, Python, and SQLite. The application allows users to manage their daily tasks efficiently through complete CRUD (Create, Read, Update, Delete) operations.

This project was developed as part of the Xebia Internship Assignment to demonstrate database integration, user authentication, and task management functionality.

---

## Features

### User Authentication

* User Registration
* User Login
* Session Management
* Logout Functionality

### Task Management (CRUD Operations)

#### Create

* Add new tasks
* Assign priority levels
* Set due dates
* Define task status

#### Read

* View all tasks
* Display tasks in tabular format

#### Update

* Modify task status
* Track task progress

#### Delete

* Remove completed or unwanted tasks

### Additional Features

* Priority Tracking (High, Medium, Low)
* Due Date Management
* Status Monitoring

  * Pending
  * In Progress
  * Completed
* Interactive Dashboard
* Modern UI using Custom CSS

---

## Technology Stack

| Component       | Technology   |
| --------------- | ------------ |
| Frontend        | Streamlit    |
| Backend         | Python       |
| Database        | SQLite       |
| Data Handling   | Pandas       |
| Visualization   | Plotly       |
| Version Control | Git & GitHub |

---

## Project Architecture

User Interface (Streamlit)

↓

Business Logic (Python Functions)

↓

Database Operations (SQLite)

↓

Data Storage

---

## Database Schema

### Users Table

| Column   | Type    |
| -------- | ------- |
| id       | Integer |
| username | Text    |
| password | Text    |

### Tasks Table

| Column    | Type    |
| --------- | ------- |
| id        | Integer |
| username  | Text    |
| task_name | Text    |
| priority  | Text    |
| due_date  | Text    |
| status    | Text    |

---

## CRUD Operations Mapping

| Operation | Functionality       |
| --------- | ------------------- |
| Create    | Add New Task        |
| Read      | View Existing Tasks |
| Update    | Modify Task Status  |
| Delete    | Remove Task         |

---


## Future Enhancements

* Password Hashing using bcrypt
* Email Notifications
* Task Search & Filtering
* Role-Based Access Control
* Cloud Deployment
* Advanced Analytics Dashboard
* Team Collaboration Features

---

## Learning Outcomes

Through this project, the following concepts were implemented:

* Python Programming
* Streamlit Development
* SQLite Database Management
* CRUD Operations
* User Authentication
* Session Management
* Data Visualization
* GitHub Version Control

---

## Author

Mandava Sai Vikranth Goud

Xebia Internship Project
