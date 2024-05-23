
# CRUD REST API - Company Database Employee Management

A simple employee management system built with Flask and MySQL.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [API Usage](#api-usage)
- [Additional Information](#additional-information)

## Introduction

This project is a basic employee management system built using Flask, a Python web framework, and MySQL database. It provides functionalities to create, read, update, and delete employee records. Additionally, it offers endpoints to view employee records in JSON and XML formats.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/ejlanuza123/CRUD-REST-API.git

   ```

2. Navigate to the project directory:

   ```bash
   cd CRUD-REST-API
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your MySQL database:
   
   - Open a MySQL database named `company`.
   - Update the database connection settings in `app.py` with your MySQL username, password, host, and database name.

5. Run the Flask application:

   ```bash
   python app.py
   ```

6. The application should now be running locally. Access it in your web browser at `http://localhost:5000`.

## Usage

Once the application is running, you can perform the following actions:

- Add a new employee
- View all employees
- Update an existing employee
- Delete an employee
- View employees in JSON or XML format

## API Usage

The application exposes the following API endpoints:

- `POST /add_employee`: Create a new employee.
- `GET /employees`: View all employees.
- `PUT /update_employee`: Update an existing employee.
- `DELETE /delete_employee`: Delete an employee.
- `GET /view_as?format=json`: View employees in JSON format.
- `GET /view_as?format=xml`: View employees in XML format.

## Additional Information

- This project is for educational purposes and may not be suitable for production use without further enhancements.
- Contributions are welcome. Feel free to submit issues or pull requests.

---
