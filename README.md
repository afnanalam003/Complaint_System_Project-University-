# U-CMS: University Complaint Management System

A modern, high-performance desktop application designed to streamline student grievance resolution. Built with **Python** and **CustomTkinter**, this project features a "Glassmorphism" UI, animated backgrounds, and role-based access control.

> **Project Status:** Completed (Semester Project for Software Engineering-2)

## Key Features

### User Interface & Experience (UI/UX)

* **Breathing Gradient Background:** A subtle, non-intrusive animated background that shifts colors dynamically.
* **Glassmorphism Design:** Modern, semi-transparent dashboard cards with rounded corners.
* **Responsive Grid Tables:** perfectly aligned data columns that replace old-school text displays.
* **Custom Dialogs:** Styled pop-up windows for alerts and confirmations (no system default message boxes).
* **Interactive Sidebar:** Navigation state highlighting to indicate the active section.

### Student Portal

* **Complaint Submission:** Easy-to-use form with validation logic.
* **Real-time Tracking:** Students can search their **Roll Number** to see the status of their specific complaints.
* **Self-Management:** Students can delete their own complaints if filed in error.
* **Auto-Reset:** Input fields auto-clear and reset placeholders after submission.

### Admin Panel (Teacher Dashboard)

* **Secure Authentication:** Protected by a login system (Credentials: `admin` / `admin123`).
* **Live Statistics:** Dashboard cards showing real-time counts for **Total**, **Pending**, and **Resolved** cases.
* **CRUD Operations:** Full capability to **Read**, **Update** (Status), and **Delete** records.
* **Color-Coded Status:** Visual indicators (🟢 Resolved, 🟡 Pending, 🔴 Rejected) in the data table.

## Tech Stack

* **Language:** Python 3.10+
* **GUI Framework:** `customtkinter` (Modern wrapper for Tkinter)
* **Concepts:** OOP (Encapsulation, Modular Design), File I/O (TXT Database), Event Binding.

## Project Structure

```bash
📂 U-CMS-Project/
│
├── 📄 MainApp.py           # The entry point (GUI & Animation Engine)
├── 📄 StudentSide.py       # Logic module for handling student data
├── 📄 AdminSide.py         # Logic module for Admin CRUD operations
├── 📄 complaints_data.txt  # Auto-generated database file
└── 📄 README.md            # Project Documentation

```

## Installation & Setup

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/U-CMS-Project.git
cd U-CMS-Project

```


2. **Install Dependencies**
You need the `customtkinter` library for the UI.
```bash
pip install customtkinter

```


3. **Run the Application**
```bash
python MainApp.py

```



## Access Credentials

To access the **Admin Panel**, use the following default credentials:

* **Username:** `admin`
* **Password:** `admin123`

## Design Principles

This project adheres to **SOLID Principles** by separating concerns:

* **UI Layer (`MainApp.py`)**: Handles presentation and user interaction only.
* **Logic Layer (`StudentSide.py`, `AdminSide.py`)**: Handles data processing and file storage.
* **Data Layer**: Persistent storage via text files.

---

*Developed by [Your Name] | Department of Computer Science*
