from flask import Flask, request, jsonify, render_template_string, redirect, url_for, flash, make_response
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

@app.route('/')
def home():
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
    <a href="{{ url_for('employees') }}">View Employees</a>
    <a href="{{ url_for('search_employee') }}">Search Employees</a>
</body>
</html>
    ''')


@app.route('/search_employee', methods=['GET', 'POST'])
def search_employee():
    if request.method == 'POST':
        search_criteria = request.form['search_criteria']
        search_value = request.form['search_value']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = f"SELECT * FROM employee WHERE {search_criteria} LIKE %s"
        cursor.execute(query, (f"%{search_value}%",))
        employees = cursor.fetchall()
        
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results</title>
</head>
<body>
    <h1>Search Results</h1>
    {% if employees %}
        <ul>
        {% for employee in employees %}
            <li>{{ employee.ssn }} - {{ employee.Fname }} {{ employee.Lname }} ({{ employee.Address }})
                <a href="{{ url_for('update_employee', ssn=employee.ssn) }}">Edit</a>
                <form action="{{ url_for('delete_employee', ssn=employee.ssn) }}" method="POST" style="display:inline;">
                    <button type="submit">Delete</button>
                </form>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No employees found matching your criteria.</p>
    {% endif %}
    <a href="{{ url_for('employees') }}">Back to Employee List</a>
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
        <label for="search_criteria">Search by:</label>
        <select name="search_criteria" id="search_criteria" required>
            <option value="ssn">SSN</option>
            <option value="Fname">First Name</option>
            <option value="Lname">Last Name</option>
            <option value="Address">Address</option>
            <!-- Add other search criteria as needed -->
        </select><br>
        <input type="text" name="search_value" placeholder="Search value" required><br>
        <button type="submit">Search</button>
    </form>
    <a href="{{ url_for('employees') }}">Back to Employee List</a>
</body>
</html>
    ''')


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
    <title>Employee List</title>
</head>
<body>
    <h1>Employee List</h1>
    <ul>
    {% for employee in employees %}
        <li>{{ employee.ssn }} - {{ employee.Fname }} {{ employee.Lname }} ({{ employee.Address }})
            <a href="{{ url_for('update_employee', ssn=employee.ssn) }}">Edit</a>
            <form action="{{ url_for('delete_employee', ssn=employee.ssn) }}" method="POST" style="display:inline;">
                <button type="submit">Delete</button>
            </form>
        </li>
    {% endfor %}
    </ul>
    <a href="{{ url_for('add_employee') }}">Add Employee</a>
    <a href="{{ url_for('search_employee') }}">Search Employees</a>
</body>
</html>
    ''', employees=employees)


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

# Add resources for other tables (department, dependent, etc.)

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Employee, '/employee')
api.add_resource(EmployeeList, '/employees')

if __name__ == "__main__":
    app.run(debug=True)
