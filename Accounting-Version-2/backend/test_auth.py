import requests
import json

# Test login with the superuser
def test_login():
    url = "http://localhost:8000/api/auth/login/"
    data = {
        "username": "user1",
        "password": "Password#1"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            tokens = response.json()
            print("\n✅ Login successful!")
            print(f"Access Token: {tokens['access'][:50]}...")
            print(f"User Info: {tokens['user']}")
            return tokens
        else:
            print("\n❌ Login failed!")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test profile endpoint with token
def test_profile(access_token):
    url = "http://localhost:8000/api/auth/profile/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\nProfile Status Code: {response.status_code}")
        
        if response.status_code == 200:
            profile = response.json()
            print("✅ Profile fetch successful!")
            print(f"Profile: {json.dumps(profile, indent=2)}")
        else:
            print("❌ Profile fetch failed!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Profile Error: {e}")

if __name__ == "__main__":
    print("Testing Lifeline Accounting Authentication API\n")
    
    # Test login
    tokens = test_login()
    
    if tokens:
        # Test profile endpoint
        test_profile(tokens['access'])
