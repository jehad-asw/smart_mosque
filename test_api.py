import requests
import json
from datetime import datetime

# Base URL for our API
BASE_URL = "http://127.0.0.1:8000"

# Test data for different user types
teacher_data = {
    "username": "teacher1",
    "email": "teacher1@example.com",
    "password": "password123",
    "firstname": "Teacher",
    "lastname": "One",
    "role": "teacher",
    "phone_number": "+1234567890",
    "address": "123 Teacher St",
    "notification_preference": "email",
    "status": "active",
    "qualifications": "PhD in Islamic Studies",
    "center_id": None,
    "specialization": "Quran Memorization",
    "years_of_experience": 5,
    "certifications": "Certified Quran Teacher",
    "availability": "Weekdays 4-8pm"
}

student_data = {
    "username": "student1",
    "email": "student1@example.com",
    "password": "password123",
    "firstname": "Student",
    "lastname": "One",
    "role": "student",
    "phone_number": "+1234567891",
    "address": "456 Student Ave",
    "notification_preference": "email",
    "status": "active",
    "level": "Intermediate",
    "exemption_status": "non-exempted",
    "center_id": None,
    "birth_date": "2010-01-01",
    "gender": "male",
    "nationality": "Saudi",
    "id_number": "1234567890",
    "parent_name": "Parent One",
    "parent_phone": "+1234567892",
    "emergency_contact": "+1234567893",
    "medical_conditions": "None",
    "registration_date": datetime.now().strftime("%Y-%m-%d"),
    "preferred_circle_id": None,
    "previous_education": "Elementary School"
}

parent_data = {
    "username": "parent1",
    "email": "parent1@example.com",
    "password": "password123",
    "firstname": "Parent",
    "lastname": "One",
    "role": "parent",
    "phone_number": "+1234567894",
    "address": "789 Parent Blvd",
    "notification_preference": "email",
    "status": "active",
    "occupation": "Engineer",
    "relationship_to_student": "father",
    "emergency_contact": "+1234567895",
    "preferred_contact_time": "Evening",
    "notes": "Prefers to be contacted via email"
}

# Function to register a user
def register_user(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Registration Response ({endpoint}):", response.status_code)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)
    return response.json() if response.status_code == 200 else None

# Function to login a user
def login_user(email, password):
    url = f"{BASE_URL}/auth/login"
    headers = {"Content-Type": "application/json"}
    data = {"email": email, "password": password}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Login Response ({email}):", response.status_code)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)
    return response.json() if response.status_code == 200 else None

# Function to get user profile
def get_profile(endpoint, token):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"Profile Response ({endpoint}):", response.status_code)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)
    return response.json() if response.status_code == 200 else None

# Main test function
def run_tests():
    print("=== Testing Smart Mosque API ===")
    
    # Register users
    print("\n--- Registering Teacher ---")
    teacher = register_user("/auth/register/teacher", teacher_data)
    
    print("\n--- Registering Student ---")
    student = register_user("/auth/register/student", student_data)
    
    print("\n--- Registering Parent ---")
    parent = register_user("/auth/register/parent", parent_data)
    
    # Login users
    print("\n--- Login Teacher ---")
    teacher_login = login_user(teacher_data["email"], teacher_data["password"])
    
    print("\n--- Login Student ---")
    student_login = login_user(student_data["email"], student_data["password"])
    
    print("\n--- Login Parent ---")
    parent_login = login_user(parent_data["email"], parent_data["password"])
    
    # Get profiles
    if teacher_login:
        print("\n--- Teacher Profile ---")
        get_profile("/teachers/me", teacher_login["access_token"])
    
    if student_login:
        print("\n--- Student Profile ---")
        get_profile("/students/me", student_login["access_token"])
    
    if parent_login:
        print("\n--- Parent Profile ---")
        get_profile("/parents/me", parent_login["access_token"])

if __name__ == "__main__":
    run_tests()
