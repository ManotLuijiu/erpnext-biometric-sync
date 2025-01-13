import requests
import json
from datetime import datetime
import importlib.util
import os
import sys
from loguru import logger

# Configure loguru logger
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    colorize=True,
)
logger.add(
    "logs/erpnext_test_{time}.log",
    rotation="500 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
)

def load_config(config_file='local_config.py'):
    """
    Load configuration from external file
    """
    try:
        config_path = os.path.abspath(config_file)
        logger.info(f"Loading configuration from {config_path}")
        
        spec = importlib.util.spec_from_file_location("config", config_path)
        if spec is None:
            raise ImportError(f"Could not load specification from {config_file}")
        
        config = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            raise ImportError(f"Could not load module from {config_file}")
        
        spec.loader.exec_module(config)
        logger.success("Configuration loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        sys.exit(1)

class ERPNextTester:
    def __init__(self, config):
        self.config = config
        self.headers = {
            "Authorization": f"token {config.ERPNEXT_API_KEY}:{config.ERPNEXT_API_SECRET}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        logger.debug("ERPNextTester initialized with config")

    def test_permissions(self):
        """
        Test API user permissions
        """
        logger.info("Testing API Permissions...")
        
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
                    logger.success(f"Can access {name}")
                else:
                    logger.error(f"Cannot access {name}")
                    logger.debug(f"Error Response: {response.text}")
                    all_permissions_ok = False
            except Exception as e:
                logger.error(f"Error checking {name} permissions: {str(e)}")
                all_permissions_ok = False
        
        return all_permissions_ok

    def get_all_employees(self):
        """
        Get list of all employees with their attendance device IDs
        """
        url = f"{self.config.ERPNEXT_URL}/api/resource/Employee"
        try:
            logger.info("Fetching employee list...")
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                employees = response.json().get('data', [])
                if employees:
                    logger.success(f"Found {len(employees)} employees")
                    return employees
            logger.warning("No employees found")
            return []
        except Exception as e:
            logger.error(f"Error fetching employees: {str(e)}")
            return []

    def get_employee_details(self, employee_id):
        """
        Get details for a specific employee
        """
        url = f"{self.config.ERPNEXT_URL}/api/resource/Employee/{employee_id}"
        try:
            logger.info(f"Fetching details for employee {employee_id}")
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json().get('data', {})
            logger.warning(f"No details found for employee {employee_id}")
            return None
        except Exception as e:
            logger.error(f"Error fetching employee details: {str(e)}")
            return None

    def test_checkin_api(self, employee_id=None):
        """
        Test the Employee Checkin API with optional employee ID input
        """
        if employee_id is None:
            logger.info("Starting interactive employee selection")
            print("\n📋 Employee ID Selection:")
            print("1. Enter Employee ID manually")
            print("2. List all employees")
            choice = input("Enter your choice (1/2): ")

            if choice == "2":
                employees = self.get_all_employees()
                if employees:
                    print("\n👥 Available Employees:")
                    for emp in employees:
                        emp_details = self.get_employee_details(emp['name'])
                        if emp_details:
                            print(f"ID: {emp_details.get('attendance_device_id', 'N/A')} - Name: {emp_details.get('employee_name')} ({emp['name']})")
                
            employee_id = input("\n🔑 Enter Employee ID to test: ").strip()
            if not employee_id:
                logger.error("Employee ID is required")
                return False

        logger.info(f"Testing Employee Checkin API for Employee ID: {employee_id}")
        
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
        
        logger.debug(f"Request Data: {json.dumps(test_data, indent=2)}")
        
        try:
            response = requests.post(checkin_url, headers=self.headers, json=test_data)
            logger.info(f"Response Status Code: {response.status_code}")
            logger.debug(f"Response Content: {response.text}")
            
            if response.status_code == 200:
                logger.success("Checkin API Test Successful!")
                return True
            else:
                logger.error("Checkin API Test Failed!")
                try:
                    error_json = json.loads(response.text)
                    if "exception" in error_json:
                        logger.error(f"Error Message: {error_json['exception']}")
                    if "_server_messages" in error_json:
                        logger.error(f"Server Messages: {error_json['_server_messages']}")
                except:
                    logger.error(f"Raw Error: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error making request: {str(e)}")
            return False

    def test_shift_type_api(self):
        """
        Test the Shift Type API
        """
        logger.info("Testing Shift Type API...")
        
        for shift_mapping in self.config.shift_type_device_mapping:
            for shift_name in shift_mapping['shift_type_name']:
                url = f"{self.config.ERPNEXT_URL}/api/resource/Shift Type/{shift_name}"
                
                try:
                    response = requests.get(url, headers=self.headers)
                    if response.status_code == 200:
                        logger.success(f"Can access Shift Type: {shift_name}")
                    else:
                        logger.error(f"Cannot access Shift Type: {shift_name}")
                        logger.debug(f"Error: {response.text}")
                except Exception as e:
                    logger.error(f"Error checking Shift Type {shift_name}: {str(e)}")

def main():
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Load configuration
    logger.info("Starting ERPNext Test Suite")
    config = load_config()
    
    # Create tester instance
    tester = ERPNextTester(config)
    
    # Run all tests
    permissions_ok = tester.test_permissions()
    if permissions_ok:
        tester.test_checkin_api()
        tester.test_shift_type_api()
    else:
        logger.warning("Skipping further tests due to permission issues")
        logger.info("Please fix permissions first")

if __name__ == "__main__":
    main()