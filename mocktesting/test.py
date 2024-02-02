import requests, responses
import unittest
from unittest.mock import patch, Mock
from main import *

def get_mock_response(status_code, fake_data):
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = fake_data
    return mock_response

class TestUserData(unittest.TestCase):

##adminuser
    @patch('requests.post')
    def test_login(self, mock_post):
        fake_token = 'fake_token'
        fake_data = {'token': fake_token}
        login_data = {
        'username': username,
        'password': password
        }
        mock_post.return_value = get_mock_response(200, fake_data)

        headers = login_and_get_token(username, password, login_url)
        self.assertEqual(username, "rakadmin")
        self.assertEqual(password, "T0mat066")
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['Authorization'], f'Token {fake_token}')
        mock_post.assert_called_once_with("http://localhost:9000/adminuser/login/",data=login_data)

        #testing for failed login
        mock_post.return_value = get_mock_response(401, {'error': 'Unauthorized'})
        headers = login_and_get_token ("invalid_user", "invalid_password", login_url)
    
    @patch('requests.post')
    @patch('main.login_and_get_token')
    def test_logout(self, mock_login, mock_post):
        fake_token = 'fake_token'
        fake_data = {"detail":"Successfully logged out"}
        mock_login.return_value = {'Authorization': f'Token {fake_token}'}
        mock_post.return_value = get_mock_response(200, fake_data)

        result = logout()
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), fake_data)
        mock_post.assert_called_once_with("https://localhost:9000/adminuser/logout/", headers = token)


##rakadmin
        
    @patch('requests.post')
    @patch('main.login_and_get_token')
    def test_add_service(self, mock_login, mock_post):
        fake_token = 'fake_token'
        fake_data = {'result': 'service added'}
        mock_login.return_value = {'Authorization': f'Token {fake_token}'}
        mock_post.return_value = get_mock_response(201, fake_data)
        
        #test for success
        result = add_service()
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.json(), fake_data)

        #test for failure
        mock_login.return_value = None
        mock_post.return_value = None
        result = add_service()
        self.assertIsNone(result)
    
    testId = '15'
    @patch('main.requests.get')
    def test_staff_id(self, mock_get):
        fake_json = [{'name': "Hisham", 'email': "Hesham@motori.rak.ae"}]
        mock_response = get_mock_response(200,fake_json)
        mock_get.return_value = mock_response

        staff_data = getStaffbyID(self.testId)


        self.assertEqual(mock_response.status_code, 200)
        mock_get.assert_called_once_with(f"http://localhost:9000/rakadmin/staff/get-staff-by-id/{testId}/", headers = token)
        self.assertEqual(staff_data.json(), fake_json)


    @patch('requests.get')
    def test_get_all_staff (self, mock_get):
        fake_json = [{
            "users": [{
                "_id": "659e4328baa9244d8fd9c56e",
                "name": "Tarek",
                "department": "Registry",
                "email": "Tarek@gmail.com",
                },
                {
                    "_id": "65a66f4757e5290035fa8155",
                    "name": "Hajar",
                    "department": "Housing",
                    "email": "hajar@gmail.com",
                    }]
                }]
        mock_response = get_mock_response(200,fake_json)

        mock_get.return_value = mock_response

        all_staff_data = get_all_staff()

        self.assertEqual(mock_response.status_code, 200)
        mock_get.assert_called_once_with("http://localhost:9000/rakadmin/staff/get-all-staff/", headers = token)
        self.assertEqual(all_staff_data.json(), fake_json)

    @patch('requests.post')
    @patch('main.login_and_get_token')
    def test_add_staff(self,mock_login, mock_post):
        fake_token = 'fake_token'
        fake_data = {'result': 'success'}
        mock_login.return_value = {'Authorization': f'Token {fake_token}'}
        mock_post.return_value = get_mock_response(201, fake_data)

        #test for success
        result = add_staff()
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.json(), fake_data)

        #test for failure
        mock_login.return_value = None
        mock_post.return_value = None
        result = add_staff()
        self.assertIsNone(result)

    @patch('requests.put')
    @patch('main.login_and_get_token')
    def test_edit_service(self, mock_login, mock_post):
        fake_token = 'fake_token'
        fake_data = {'service_id': 'SV28', 'sla_value': 4}
        mock_login.return_value = {'Authorization': f'Token {fake_token}'}
        mock_post.return_value = get_mock_response(200, fake_data)

        #test for success
        result = edit_sevice(srv_id)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), fake_data)
        mock_post.assert_called_once_with(f"http://localhost:9000/rakadmin/service/edit-service/{srv_id}/", headers = token, json = result.json())

    @patch('requests.delete')
    @patch('main.login_and_get_token')
    def test_delete_service(self,mock_login, mock_post):
        fake_token = 'fake_token'
        mock_login.return_value = {'Authorization': f'Token {fake_token}'}
        fake_data = None
        mock_post.return_value = get_mock_response(204, fake_data)

        result = delete_service(srv_id)
        self.assertEqual(result.status_code, 204)
        mock_post.assert_called_once_with(f"http://localhost:9000/rakadmin/service/remove-service/{srv_id}/", headers = token)


    @patch('requests.delete')
    @patch('main.login_and_get_token')
    def test_delete_staff_by_id(self,mock_login, mock_post):
        fake_token = 'fake_token'
        mock_login.return_value = {'Authorization': f'Token {fake_token}'}
        fake_data = None
        mock_post.return_value = get_mock_response(201, fake_data)

        result = delete_staff_by_id(testId_delete)
        self.assertEqual(result.status_code, 201)
        mock_post.assert_called_once_with(f"http://localhost:9000/rakadmin/staff/remove-staff/{testId_delete}/", headers = token)

    @patch('requests.delete')
    @patch ('main.login_and_get_token')
    def test_delete_multiple_staff(self, mock_login, mock_post):
        fake_token = 'fake_token'
        mock_login.return_value = {'Authorization': f'Token {fake_token}'}
        fake_data = {
            "staffIDs": [
                "65afb6b9fa75f2aa5c555263",
                "65afb17dfa75f2aa5c555239"
                ]
                }
        mock_post.return_value = get_mock_response(201, fake_data)

        result = delete_multiple_staff()
        self.assertEqual(result.status_code, 201)
        mock_post.assert_called_once_with("http://localhost:9000/rakadmin/staff/remove-multiple-staff/", headers = token, json = result.json())

    @patch ('requests.patch')
    @patch ('main.login_and_get_token')
    def test_edit_staff_department (self, mock_login, mock_post):
        fake_token = 'fake_token'
        mock_login.return_value = {'Authorization': f'Token {fake_token}'}
        fake_data = {"department":"egac"}
        mock_post.return_value = get_mock_response(200, fake_data)

        result = edit_staff_department(testId)
        self.assertEqual(result.status_code, 200)
        mock_post.assert_called_once_with(f"https://localhost:9000/rakadmin/staff/change-staff-dept/{testId}", headers = token, json = result.json())



        

        

##service-catalog
    @patch('requests.get')
    def test_get_all_services (self, mock_get):
        fake_json = [{'service_id': "WT02", 'service_name': "Low Water Pressure", 'service_type': "Complaint"}]
        mock_response = get_mock_response (200,fake_json)
        mock_get.return_value = mock_response

        all_services = get_all_services()

        self.assertEqual(mock_response.status_code, 200)
        mock_get.assert_called_once_with("http://localhost:9000/servicecatalog/get-all-services/")
        self.assertEqual(all_services.json(), fake_json)


if __name__ == '__main__':
    unittest.main()