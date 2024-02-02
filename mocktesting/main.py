import requests, responses
from unittest.mock import patch, Mock

username = "rakadmin"
password = "T0mat066"
login_url = "http://localhost:9000/adminuser/login/"
testId='15'
testId_delete = '65b101300069fc22f7f6328e'
srv_id = 'SV23'

# Extracting token for login
def login_and_get_token(username, password, login_url):
   
    login_data = {
        'username': username,
        'password': password
    }

    login_response = requests.post(login_url, data=login_data)

    if login_response.status_code == 200:
        token = login_response.json().get('token')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {token}',   
        }

        return headers
token = login_and_get_token(username, password, login_url)

def logout ():
    url = "https://localhost:9000/adminuser/logout/"
    response = requests.post(url, headers=token)
    return response

# rakadmin
def add_service():
    url = "http://localhost:9000/rakadmin/service/add-service/"
    data = {
        "service_id": "SV69",
        "additional_fields": [
            {
                "condition": None,
                "field_name": "Please Attach your National ID",
                "field_type": "document",
                "document_type": "National ID",
                "is_required": True,
                "is_ai_compatible": False
            },
            {
                "condition": {
                    "condition_type": "min-max",
                    "values": [
                        "18",
                        "60"
                    ]
                },
                "field_name": "Age",
                "field_type": "number",
                "document_type": "Passport",
                "is_required": True,
                "is_ai_compatible": False
            },
            {
                "condition": {
                    "condition_type": "selection",
                    "values": [
                        "Joe",
                        " Joe",
                        " Joe",
                        " Youssef Nassar"
                    ]
                },
                "field_name": "Ashtar Katkout",
                "field_type": "dropdown",
                "document_type": "Passport",
                "is_required": True,
                "is_ai_compatible": False
            }
        ],
        "service_name": "Test Service",
        "service_type": "Request",
        "department": "Land",
        "sla_value": 1,
        "sla_unit": "Week",
        "description": "pizza pizza piizzaaa",
        "points": 50
    }

    response = requests.post(url, headers=token, json=data)
    return response
    
def getStaffbyID(staff_id):
    url = f"http://localhost:9000/rakadmin/staff/get-staff-by-id/{staff_id}/"
    response = requests.get(url, headers=token)
    
    if (response.status_code==200):
        print('Authenticated and request is successful')
        return response
    elif(response.status_code==500):
        print("Bad Request, incorrect staff ID")
        return response
    elif(response.status_code==401):
        print("Unauthorized, incorrect token or header credentials")
        return response
    elif(response.status_code==404):
        print("Not Found, Url is incorrect")
        return response
    else:
        print("Bad Request")
        return response
    

def get_all_staff():
    url = "http://localhost:9000/rakadmin/staff/get-all-staff/"
    response = requests.get(url, headers = token)

    if (response.status_code==200):
        print('Authenticated and request is successful')
        return response
    elif(response.status_code==500):
        print("Server side error")
        return response
    elif(response.status_code==401):
        print("Unauthorized, incorrect token or header credentials")
        return response
    elif(response.status_code==404):
        print("Not Found, Url is incorrect")
        return response
    else:
        print("Bad Request")
        return response

def add_staff():
    url = "http://localhost:9000/rakadmin/staff/add-staff/"
    staff_data = {
            "name":"akram",
            "email":"heshaaa3@gmail.com",
            "department":"Water",
            "password":"kokakoka",
            "confirmPassword":"kokakoka"
        }
    response = requests.post(url, json=staff_data, headers=token)
    return response


def edit_sevice(srv_id):
    url = f"http://localhost:9000/rakadmin/service/edit-service/{srv_id}/"
    data = {
    "service_id": "SV28",  
    "sla_value": 4
    }
    response = requests.put(url, headers=token, json=data)
    return response

def delete_service(srv_id):
    url = f"http://localhost:9000/rakadmin/service/remove-service/{srv_id}/"
    response=requests.delete(url, headers=token)
    return response

def delete_staff_by_id(testId):
    url = f"http://localhost:9000/rakadmin/staff/remove-staff/{testId}/"
    response=requests.delete(url, headers=token)
    return response

def delete_multiple_staff():
    url = "http://localhost:9000/rakadmin/staff/remove-multiple-staff/"
    data = {
    "staffIDs": [
        "65afb6b9fa75f2aa5c555263",
        "65afb17dfa75f2aa5c555239"
        ]
    }
    response = requests.delete(url, headers=token, json=data)
    return response

def edit_staff_department(testId):
    url = f"https://localhost:9000/rakadmin/staff/change-staff-dept/{testId}"
    data ={"department":"egac"}
    response = requests.patch(url, headers=token,json=data)
    return response


# service-catalog
def get_all_services ():
    url = "http://localhost:9000/servicecatalog/get-all-services/"
    response = requests.get(url)
    if (response.status_code==200):
        print("Request Successful")
        return response
    elif (response.status_code==404):
        print("Bad Request, Url not found")
        return response
    else:
        print("Bad Request")
        return response
    


# http://localhost:9000/

