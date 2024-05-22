import unittest
import json
from app import app

class ApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_register_employee(self):
        response = self.app.post('/register', data=json.dumps({
            "ssn": 123456789, 
            "Fname": "John", 
            "Minit": "B", 
            "Lname": "Doe", 
            "Bdate": "1990-01-01", 
            "Address": "123 Elm St", 
            "Sex": "M", 
            "Salary": 50000, 
            "Super_ssn": None, 
            "DL_id": 1
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_login_employee(self):
        response = self.app.post('/login', data=json.dumps({
            "ssn": 123456789, 
            "password": "lanuza123"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data))

    def test_get_employee(self):
        login_response = self.app.post('/login', data=json.dumps({
            "ssn": 123456789, 
            "password": "lanuza123"
        }), content_type='application/json')
        access_token = json.loads(login_response.data)['access_token']

        response = self.app.get('/employee', headers={
            'Authorization': f'Bearer {access_token}'
        }, query_string={'ssn': 123456789})
        self.assertEqual(response.status_code, 200)

    def test_update_employee(self):
        login_response = self.app.post('/login', data=json.dumps({
            "ssn": 123456789, 
            "password": "lanuza123"
        }), content_type='application/json')
        access_token = json.loads(login_response.data)['access_token']

        response = self.app.put('/employee', headers={
            'Authorization': f'Bearer {access_token}'
        }, data=json.dumps({
            "ssn": 123456789, 
            "Fname": "John", 
            "Minit": "B", 
            "Lname": "Doe", 
            "Bdate": "1990-01-01", 
            "Address": "123 Updated St", 
            "Sex": "M", 
            "Salary": 55000, 
            "Super_ssn": None, 
            "DL_id": 1
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_employee(self):
        login_response = self.app.post('/login', data=json.dumps({
            "ssn": 123456789, 
            "password": "lanuza123"
        }), content_type='application/json')
        access_token = json.loads(login_response.data)['access_token']

        response = self.app.delete('/employee', headers={
            'Authorization': f'Bearer {access_token}'
        }, data=json.dumps({'ssn': 123456789}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
