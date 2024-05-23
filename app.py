from flask import Flask, request, jsonify, render_template_string, redirect, url_for, flash, make_response, Response, session
from flask_mysqldb import MySQL
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import MySQLdb.cursors
import xmltodict

app = Flask(__name__)
api = Api(app)

app.secret_key = '0415'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lanuza123'
app.config['MYSQL_DB'] = 'company'
app.config['JWT_SECRET_KEY'] = '0415'

mysql = MySQL(app)
jwt = JWTManager(app)

@app.route('/register_page', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists!', 'danger')
        else:
            users[username] = password
            flash('User registered successfully!', 'success')
            return redirect(url_for('login_page'))

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    <form action="{{ url_for('register_page') }}" method="POST">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Register</button>
    </form>
    <a href="{{ url_for('login_page') }}">Login</a>
</body>
</html>
    ''')

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form action="{{ url_for('login_page') }}" method="POST">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
    <a href="{{ url_for('register_page') }}">Register</a>
</body>
</html>
    ''')

@app.route('/')
def home():
    if 'username' not in session:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login_page'))
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Company Database</title>
</head>
<body>
    <h1>Welcome to the Company Database</h1>
    <form action="{{ url_for('add_employee') }}" method="get">
        <button type="submit">Add Employee</button>
    </form>
    <form action="{{ url_for('search_employee') }}" method="get">
        <button type="submit">Search Employees</button>
    </form>
    <form action="{{ url_for('employees') }}" method="get">
        <button type="submit">Employee List</button>
    </form>
    <form action="{{ url_for('logout') }}" method="get">
        <button type="submit">Logout</button>
    </form>
</body>
</html>
    ''')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('login_page'))

# Ensure users dictionary is defined
users = {}



@app.route('/employees')
def employees():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee')
    employees = cursor.fetchall()
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EMPLOYEE LIST</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        th {
            background-color: #f2f2f2;
        }

        .center {
            text-align: center;
        }

        .dropdown {
            position: relative;
            display: inline-block;
        }

        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #f9f9f9;
            min-width: 160px;
            z-index: 1;
        }

        .dropdown-content a {
            color: black;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            text-align: center;
        }

        .dropdown-content a:hover {
            background-color: #f1f1f1;
        }

        .dropdown:hover .dropdown-content {
            display: block;
        }

        .dropdown:hover .dropbtn {
            background-color: #3e8e41;
        }
    </style>
</head>
<body>

<div class="center">
    <h2>EMPLOYEE LIST</h2>

    <table>
        <tr>
            <th>SSN</th>
            <th>First Name</th>
            <th>Middle Initial</th>
            <th>Last Name</th>
            <th>Birth Date</th>
            <th>Address</th>
            <th>Sex</th>
            <th>Salary</th>
            <th>Supervisor SSN</th>
            <th>DL ID</th>
        </tr>
        {% for employee in employees %}
        <tr>
            <td>{{ employee.ssn }}</td>
            <td>{{ employee.Fname }}</td>
            <td>{{ employee.Minit }}</td>
            <td>{{ employee.Lname }}</td>
            <td>{{ employee.Bdate }}</td>
            <td>{{ employee.Address }}</td>
            <td>{{ employee.Sex }}</td>
            <td>{{ employee.Salary }}</td>
            <td>{{ employee.Super_ssn }}</td>
            <td>{{ employee.DL_id }}</td>
        </tr>
        {% endfor %}
    </table>

    <div class="dropdown">
        <button class="dropbtn">Download</button>
        <div class="dropdown-content">
            <a href="{{ url_for('download_json') }}" download="employees.json">JSON</a>
            <a href="{{ url_for('download_xml') }}" download="employees.xml">XML</a>
        </div>
    </div>
</div>

<form action="{{ url_for('add_employee') }}" method="get">
    <button type="submit">Add Employee</button>
</form>

<form action="{{ url_for('search_employee') }}" method="get">
    <button type="submit">Search Employees</button>
</form>
</body>
</html>


    ''', employees=employees)
    
@app.route('/search_employee', methods=['GET', 'POST'])
def search_employee():
    if request.method == 'POST':
        search_term = request.form['search_term']
        search_type = request.form['search_type']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = f"SELECT * FROM employee WHERE {search_type} LIKE %s"
        cursor.execute(query, ('%' + search_term + '%',))
        employees = cursor.fetchall()
        
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        th {
            background-color: #f2f2f2;
        }

        .center {
            text-align: center;
        }
    </style>
</head>
<body>
<div class="center">
    <h2>Search Results</h2>
    <table>
        <tr>
            <th>SSN</th>
            <th>First Name</th>
            <th>Middle Initial</th>
            <th>Last Name</th>
            <th>Birth Date</th>
            <th>Address</th>
            <th>Sex</th>
            <th>Salary</th>
            <th>Supervisor SSN</th>
            <th>DL ID</th>
            <th>Actions</th>
        </tr>
        {% for employee in employees %}
        <tr>
            <td>{{ employee.ssn }}</td>
            <td>{{ employee.Fname }}</td>
            <td>{{ employee.Minit }}</td>
            <td>{{ employee.Lname }}</td>
            <td>{{ employee.Bdate }}</td>
            <td>{{ employee.Address }}</td>
            <td>{{ employee.Sex }}</td>
            <td>{{ employee.Salary }}</td>
            <td>{{ employee.Super_ssn }}</td>
            <td>{{ employee.DL_id }}</td>
            <td>
                <form action="{{ url_for('update_employee', ssn=employee.ssn) }}" method="get" style="display:inline;">
                    <button type="submit">Edit</button>
                </form>
                <form action="{{ url_for('delete_employee', ssn=employee.ssn) }}" method="post" style="display:inline;">
                    <button type="submit">Delete</button>
                </form>

            </td>
        </tr>
        {% endfor %}
    </table>
    <a href="{{ url_for('home') }}">Back to Home</a>
    <a href="{{ url_for('employees') }}">Go to Employees List</a>
</div>
</body>
</html>
        ''', employees=employees)
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Employee</title>
</head>
<body>
    <h1>Search Employee</h1>
    <form action="{{ url_for('search_employee') }}" method="POST">
        <input type="text" name="search_term" placeholder="Search Term" required><br>
        <select name="search_type">
            <option value="ssn">SSN</option>
            <option value="Fname">First Name</option>
            <option value="Lname">Last Name</option>
        </select><br>
        <button type="submit">Search</button>
    </form>
    <a href="{{ url_for('home') }}">Back to Home</a>
</body>
</html>
    ''')


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        ssn = request.form['ssn']
        Fname = request.form['Fname']
        Minit = request.form['Minit']
        Lname = request.form['Lname']
        Bdate = request.form['Bdate']
        Address = request.form['Address']
        Sex = request.form['Sex']
        Salary = request.form['Salary']
        Super_ssn = request.form['Super_ssn']
        DL_id = request.form['DL_id']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                       (ssn, Fname, Minit, Lname, Bdate, Address, Sex, Salary, Super_ssn, DL_id))
        mysql.connection.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('employees'))
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Employee</title>
</head>
<body>
    <h1>Add Employee</h1>
    <form action="{{ url_for('add_employee') }}" method="POST">
        <input type="text" name="ssn" placeholder="SSN" required><br>
        <input type="text" name="Fname" placeholder="First Name" required><br>
        <input type="text" name="Minit" placeholder="Middle Initial"><br>
        <input type="text" name="Lname" placeholder="Last Name" required><br>
        <input type="date" name="Bdate" placeholder="Birth Date" required><br>
        <input type="text" name="Address" placeholder="Address" required><br>
        <input type="text" name="Sex" placeholder="Sex" required><br>
        <input type="text" name="Salary" placeholder="Salary" required><br>
        <input type="text" name="Super_ssn" placeholder="Super SSN"><br>
        <input type="text" name="DL_id" placeholder="Department Location ID" required><br>
        <button type="submit">Add</button>
    </form>
    <a href="{{ url_for('employees') }}">Back to Employee List</a>
</body>
</html>
    ''')

@app.route('/update_employee/<ssn>', methods=['GET', 'POST'])
def update_employee(ssn):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        Fname = request.form['Fname']
        Minit = request.form['Minit']
        Lname = request.form['Lname']
        Bdate = request.form['Bdate']
        Address = request.form['Address']
        Sex = request.form['Sex']
        Salary = request.form['Salary']
        Super_ssn = request.form['Super_ssn']
        DL_id = request.form['DL_id']

        cursor.execute('UPDATE employee SET Fname = %s, Minit = %s, Lname = %s, Bdate = %s, Address = %s, Sex = %s, Salary = %s, Super_ssn = %s, DL_id = %s WHERE ssn = %s', 
                       (Fname, Minit, Lname, Bdate, Address, Sex, Salary, Super_ssn, DL_id, ssn))
        mysql.connection.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('employees'))
    cursor.execute('SELECT * FROM employee WHERE ssn = %s', (ssn,))
    employee = cursor.fetchone()
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Employee</title>
</head>
<body>
    <h1>Update Employee</h1>
    <form action="{{ url_for('update_employee', ssn=employee.ssn) }}" method="POST">
        <input type="text" name="Fname" placeholder="First Name" value="{{ employee.Fname }}" required><br>
        <input type="text" name="Minit" placeholder="Middle Initial" value="{{ employee.Minit }}"><br>
        <input type="text" name="Lname" placeholder="Last Name" value="{{ employee.Lname }}" required><br>
        <input type="date" name="Bdate" placeholder="Birth Date" value="{{ employee.Bdate }}" required><br>
        <input type="text" name="Address" placeholder="Address" value="{{ employee.Address }}" required><br>
        <input type="text" name="Sex" placeholder="Sex" value="{{ employee.Sex }}" required><br>
        <input type="text" name="Salary" placeholder="Salary" value="{{ employee.Salary }}" required><br>
        <input type="text" name="Super_ssn" placeholder="Super SSN" value="{{ employee.Super_ssn }}"><br>
        <input type="text" name="DL_id" placeholder="Department Location ID" value="{{ employee.DL_id }}" required><br>
        <button type="submit">Update</button>
    </form>
    <a href="{{ url_for('employees') }}">Back to Employee List</a>
</body>
</html>
    ''', employee=employee)
    
@app.route('/delete_employee/<ssn>', methods=['POST'])
def delete_employee(ssn):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM employee WHERE ssn = %s', (ssn,))
    mysql.connection.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('employees'))

def output_format(data, format='json'):
    if format == 'xml':
        response = make_response(xmltodict.unparse({"response": data}, pretty=True))
        response.headers['Content-Type'] = 'application/xml'
    else:
        response = make_response(jsonify(data))
        response.headers['Content-Type'] = 'application/json'
    return response

# API Endpoints
class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ssn', required=True, help="SSN cannot be blank!")
        parser.add_argument('Fname', required=True, help="First Name cannot be blank!")
        parser.add_argument('Minit')
        parser.add_argument('Lname', required=True, help="Last Name cannot be blank!")
        parser.add_argument('Bdate', required=True, help="Birth Date cannot be blank!")
        parser.add_argument('Address', required=True, help="Address cannot be blank!")
        parser.add_argument('Sex', required=True, help="Sex cannot be blank!")
        parser.add_argument('Salary', required=True, help="Salary cannot be blank!")
        parser.add_argument('Super_ssn')
        parser.add_argument('DL_id', required=True, help="Department Location ID cannot be blank!")
        args = parser.parse_args()

        ssn = args['ssn']
        Fname = args['Fname']
        Minit = args['Minit']
        Lname = args['Lname']
        Bdate = args['Bdate']
        Address = args['Address']
        Sex = args['Sex']
        Salary = args['Salary']
        Super_ssn = args['Super_ssn']
        DL_id = args['DL_id']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE ssn = %s', (ssn,))
        employee = cursor.fetchone()
        
        if employee:
            return {'message': 'Employee already exists!'}, 400
        else:
            cursor.execute('INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                           (ssn, Fname, Minit, Lname, Bdate, Address, Sex, Salary, Super_ssn, DL_id))
            mysql.connection.commit()
            return {'message': 'Employee registered successfully!'}, 201

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ssn', required=True, help="SSN cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        ssn = args['ssn']
        password = args['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE ssn = %s AND password = %s', (ssn, password))
        employee = cursor.fetchone()
        
        if employee:
            access_token = create_access_token(identity={'ssn': ssn})
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials!'}, 401

class Employee(Resource):
    @jwt_required()
    def get(self):
        ssn = request.args.get('ssn')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE ssn = %s', (ssn,))
        employee = cursor.fetchone()
        if employee:
            return employee, 200
        else:
            return {'message': 'Employee not found!'}, 404

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ssn', required=True)
        parser.add_argument('Fname', required=True)
        parser.add_argument('Minit')
        parser.add_argument('Lname', required=True)
        parser.add_argument('Bdate', required=True)
        parser.add_argument('Address', required=True)
        parser.add_argument('Sex', required=True)
        parser.add_argument('Salary', required=True)
        parser.add_argument('Super_ssn')
        parser.add_argument('DL_id', required=True)
        args = parser.parse_args()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE employee SET Fname = %s, Minit = %s, Lname = %s, Bdate = %s, Address = %s, Sex = %s, Salary = %s, Super_ssn = %s, DL_id = %s WHERE ssn = %s', 
                       (args['Fname'], args['Minit'], args['Lname'], args['Bdate'], args['Address'], args['Sex'], args['Salary'], args['Super_ssn'], args['DL_id'], args['ssn']))
        mysql.connection.commit()
        return {'message': 'Employee updated successfully!'}, 200

    @jwt_required()
    def delete(self):
        ssn = request.args.get('ssn')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM employee WHERE ssn = %s', (ssn,))
        mysql.connection.commit()
        return {'message': 'Employee deleted successfully!'}, 200

class EmployeeList(Resource):
    def get(self):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee')
        employees = cursor.fetchall()
        format = request.args.get('format', 'json')
        return output_format(employees, format), 200

def generate_json_data():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee')
    employees = cursor.fetchall()
    return jsonify(employees)

def generate_xml_data():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee')
    employees = cursor.fetchall()
    xml_data = '<?xml version="1.0" encoding="UTF-8"?><employees>'
    for employee in employees:
        xml_data += '<employee>'
        for key, value in employee.items():
            xml_data += f'<{key}>{value}</{key}>'
        xml_data += '</employee>'
    xml_data += '</employees>'
    return Response(xml_data, mimetype='text/xml')

@app.route('/download_json')
def download_json():
    return generate_json_data()

@app.route('/download_xml')
def download_xml():
    return generate_xml_data()
# Add resources for other tables (department, dependent, etc.)

api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Employee, '/api/employee')
api.add_resource(EmployeeList, '/api/employees')

if __name__ == "__main__":
    app.run(debug=True)
