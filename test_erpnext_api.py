import local_config as config
import requests
import json
from datetime import datetime

def test_permissions(base_url, api_key, api_secret):
    """
    Test API user permissions
    """
    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Accept": "application/json"
    }
    
    # Test 1: Check if we can list Employee Checkins
    print("\nTesting permissions...")
    check_url = f"{base_url}/api/resource/Employee Checkin"
    
    try:
        response = requests.get(check_url, headers=headers)
        print(f"List Employee Checkins Permission: {response.status_code}")
        if response.status_code == 200:
            print("✅ Can list Employee Checkins")
        else:
            print("❌ Cannot list Employee Checkins")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error checking permissions: {str(e)}")

def test_checkin_api(base_url, api_key, api_secret):
    """
    Test the Employee Checkin API with correct case for coordinates
    """
    checkin_url = f"{base_url}/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field"
    
    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Note: Using lowercase 'latitude' and 'longitude'
    test_data = {
        "employee_field_value": "9",
        "attendance_device_id": "9",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "device_id": "Chatori_K50ID",
        "log_type": "IN",
        "latitude": "13.3184624",  # Changed from Latitude to latitude
        "longitude": "100.9242073"  # Changed from Longitude to longitude
    }
    
    print("\nTesting Employee Checkin API...")
    print(f"Request Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(checkin_url, headers=headers, json=test_data)
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Checkin API Test Successful!")
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
                
    except Exception as e:
        print(f"\n❌ Error making request: {str(e)}")

if __name__ == "__main__":
    config = {
        "ERPNEXT_URL": "https://chatori.bunchee.online",
        "ERPNEXT_API_KEY": "80843c1f056a1ed",
        "ERPNEXT_API_SECRET": "8a76febe4b3d4f5"
    }
    
    # First test permissions
    test_permissions(
        config["ERPNEXT_URL"],
        config["ERPNEXT_API_KEY"],
        config["ERPNEXT_API_SECRET"]
    )
    
    # Then try the checkin
    test_checkin_api(
        config["ERPNEXT_URL"],
        config["ERPNEXT_API_KEY"],
        config["ERPNEXT_API_SECRET"]
    )