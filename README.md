# University Complaint Management System

A Python-based system designed to streamline the process of lodging and resolving university complaints. This project was developed as a semester project for Software Engineering-2, focusing on **Object-Oriented Programming (OOP)** and **SOLID Design Principles**.

## Features
* **Student Portal:** Allows students to log complaints with their Name and Roll Number.
* **Teacher Dashboard:** Allows faculty to view, track, and update complaint statuses (Resolved, In Progress, Rejected).
* **Data Persistence:** All data is saved automatically to a text file database (`complaints_data.txt`), ensuring no data is lost when the program closes.
* **Modular Design:** Separated into `student.py` and `teacher.py` for better security and code management.

##  Tech Stack
* **Language:** Python 3.x
* **Concepts:** OOP (Classes, Inheritance), File I/O, SOLID Principles.

##  Project Structure
* `student.py`: The client-side application for submitting forms.
* `teacher.py`: The admin-side application for managing issues.
* `complaints_data.txt`: The file-based database (generated automatically).

##  How to Run
1. Clone the repository.
2. Run the student portal:
   ```bash
   python student.py
3. Run the teacher portal:
   ```bash
   python teacher.py
