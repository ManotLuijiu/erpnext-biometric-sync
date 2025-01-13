import requests
import json
from datetime import datetime
import importlib.util
import os
import sys

def load_config(config_file='local_config.py'):
    """
    Load configuration from external file
    """
    try:
        config_path = os.path.abspath(config_file)
        spec = importlib.util.spec_from_file_location("config", config_path)
        if spec is None:
            raise ImportError(f"Could not load specification from {config_file}")
        config = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            raise ImportError(f"Could not load module from {config_file}")
        spec.loader.exec_module(config)
        return config
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        sys.exit(1)

class ERPNextTester:
    def __init__(self, config):
        self.config = config
        self.headers = {
            "Authorization": f"token {config.ERPNEXT_API_KEY}:{config.ERPNEXT_API_SECRET}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def test_permissions(self):
        """
        Test API user permissions
        """
        print("\n1. Testing API Permissions...")
        
        endpoints = [
            ("Employee Checkin", "/api/resource/Employee Checkin"),
            ("Employee", "/api/resource/Employee"),
            ("Shift Type", "/api/resource/Shift Type")
        ]
        
        all_permissions_ok = True
        for name, endpoint in endpoints:
            url = f"{self.config.ERPNEXT_URL}{endpoint}"
            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    print(f"✅ Can access {name}")
                else:
                    print(f"❌ Cannot access {name}")
                    print(f"Error: {response.text}")
                    all_permissions_ok = False
            except Exception as e:
                print(f"Error checking {name} permissions: {str(e)}")
                all_permissions_ok = False
        
        return all_permissions_ok

    def get_all_employees(self):
        """
        Get list of all employees with their attendance device IDs
        """
        url = f"{self.config.ERPNEXT_URL}/api/resource/Employee"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                employees = response.json().get('data', [])
                if employees:
                    return employees
            return []
        except Exception as e:
            print(f"Error fetching employees: {str(e)}")
            return []

    def get_employee_details(self, employee_id):
        """
        Get details for a specific employee
        """
        url = f"{self.config.ERPNEXT_URL}/api/resource/Employee/{employee_id}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json().get('data', {})
            return None
        except Exception as e:
            print(f"Error fetching employee details: {str(e)}")
            return None

    def test_checkin_api(self, employee_id=None):
        """
        Test the Employee Checkin API with optional employee ID input
        """
        if employee_id is None:
            print("\nEmployee ID Selection:")
            print("1. Enter Employee ID manually")
            print("2. List all employees")
            choice = input("Enter your choice (1/2): ")

            if choice == "2":
                employees = self.get_all_employees()
                if employees:
                    print("\nAvailable Employees:")
                    for emp in employees:
                        emp_details = self.get_employee_details(emp['name'])
                        if emp_details:
                            print(f"ID: {emp_details.get('attendance_device_id', 'N/A')} - Name: {emp_details.get('employee_name')} ({emp['name']})")
                
            employee_id = input("\nEnter Employee ID to test: ").strip()
            if not employee_id:
                print("Employee ID is required. Exiting test.")
                return False

        print(f"\n2. Testing Employee Checkin API for Employee ID: {employee_id}")
        
        checkin_url = f"{self.config.ERPNEXT_URL}/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field"
        
        test_data = {
            "employee_field_value": employee_id,
            "attendance_device_id": employee_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "device_id": self.config.devices[0]['device_id'],
            "log_type": "IN",
            "latitude": "13.3184624",
            "longitude": "100.9242073"
        }
        
        print(f"Request Data: {json.dumps(test_data, indent=2)}")
        
        try:
            response = requests.post(checkin_url, headers=self.headers, json=test_data)
            print(f"\nResponse Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            
            if response.status_code == 200:
                print("\n✅ Checkin API Test Successful!")
                return True
            else:
                print("\n❌ Checkin API Test Failed!")
                try:
                    error_json = json.loads(response.text)
                    if "exception" in error_json:
                        print(f"Error Message: {error_json['exception']}")
                    if "_server_messages" in error_json:
                        print(f"Server Messages: {error_json['_server_messages']}")
                except:
                    print(f"Raw Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"\n❌ Error making request: {str(e)}")
            return False

    def test_shift_type_api(self):
        """
        Test the Shift Type API
        """
        print("\n3. Testing Shift Type API...")
        
        for shift_mapping in self.config.shift_type_device_mapping:
            for shift_name in shift_mapping['shift_type_name']:
                url = f"{self.config.ERPNEXT_URL}/api/resource/Shift Type/{shift_name}"
                
                try:
                    response = requests.get(url, headers=self.headers)
                    if response.status_code == 200:
                        print(f"✅ Can access Shift Type: {shift_name}")
                    else:
                        print(f"❌ Cannot access Shift Type: {shift_name}")
                        print(f"Error: {response.text}")
                except Exception as e:
                    print(f"Error checking Shift Type {shift_name}: {str(e)}")

def main():
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Create tester instance
    tester = ERPNextTester(config)
    
    # Run all tests
    permissions_ok = tester.test_permissions()
    if permissions_ok:
        # Interactive employee selection and checkin test
        tester.test_checkin_api()
        tester.test_shift_type_api()
    else:
        print("\n⚠️ Skipping further tests due to permission issues.")
        print("Please fix permissions first.")

if __name__ == "__main__":
    main()